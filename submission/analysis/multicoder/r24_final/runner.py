# /// script
# requires-python = ">=3.12"
# dependencies = ["pydantic>=2.12,<3"]
# ///
# How to run: uv run python -m r24_final.runner

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import ClassVar, Final, Protocol, assert_never, final, override

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter

from r24_final.adapters import Command, Vendor, build_command, subprocess_transport
from r24_final.evidence import EvidencePacket
from r24_final.output_validation import _validate_output
from r24_final.process_sandbox import build_execution_command
from r24_final.schedule import Condition, Trial


EXPECTED_TRIALS: Final = 42
TIMEOUT_SECONDS: Final = 600


class ScheduleEntry(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid", frozen=True)

    trial_id: str = Field(min_length=1)
    vendor: Vendor
    record_id: str = Field(pattern=r"^R\d{2}$")
    condition: Condition
    period: int = Field(ge=1, le=2)
    order: int = Field(ge=0)


@dataclass(frozen=True, slots=True)
class TrialResult:
    trial_id: str
    succeeded: bool
    attempts: int


@dataclass(frozen=True, slots=True)
class AttemptTrace:
    completed: subprocess.CompletedProcess[str]
    command: Command
    transport_failed: bool
    elapsed_seconds: float
    schema_sha256: str
    packet_sha256: str
    execution_arguments: tuple[str, ...]
    sandbox_root: str


@dataclass(frozen=True, slots=True)
class ScheduleError(Exception):
    detail: str

    @override
    def __str__(self) -> str:
        return self.detail


@dataclass(frozen=True, slots=True)
class OutputExistsError(Exception):
    path: Path

    @override
    def __str__(self) -> str:
        return f"refusing to overwrite append-only output: {self.path}"


class Transport(Protocol):
    def __call__(
        self, arguments: tuple[str, ...], prompt: str, cwd: Path, timeout_seconds: int
    ) -> subprocess.CompletedProcess[str]: ...


def load_schedule(path: Path) -> tuple[Trial, ...]:
    entries = TypeAdapter(tuple[ScheduleEntry, ...]).validate_json(path.read_text())
    trials = tuple(
        Trial(
            entry.trial_id,
            entry.vendor.value,
            entry.record_id,
            entry.condition,
            entry.period,
            entry.order,
        )
        for entry in entries
    )
    _verify_schedule(trials)
    return trials


def _verify_schedule(trials: tuple[Trial, ...]) -> None:
    if len(trials) != EXPECTED_TRIALS:
        raise ScheduleError(f"schedule must contain exactly 42 trials, got {len(trials)}")
    if len({trial.trial_id for trial in trials}) != EXPECTED_TRIALS:
        raise ScheduleError("schedule trial identifiers must be unique")
    for vendor in Vendor:
        vendor_trials = tuple(trial for trial in trials if trial.vendor == vendor.value)
        if len(vendor_trials) != 14 or len({trial.record_id for trial in vendor_trials}) != 14:
            raise ScheduleError(f"{vendor.value} must have fourteen unique records")
        if any(trial.condition is not Condition.SERVO for trial in vendor_trials):
            raise ScheduleError("production schedule must be Servo-only")


@final
class ExperimentRunner:
    def __init__(
        self,
        output_root: Path,
        transport: Transport = subprocess_transport,
        timeout_seconds: int = TIMEOUT_SECONDS,
    ) -> None:
        self._output_root = output_root
        self._transport = transport
        self._timeout_seconds = timeout_seconds

    def run_trial(
        self,
        trial: Trial,
        prompt: str,
        schema_path: Path,
        packet: EvidencePacket,
    ) -> TrialResult:
        for attempt in (1, 2):
            trace = self._attempt(trial, prompt, schema_path, packet)
            validation_error = None
            normalized_output = trace.completed.stdout.strip()
            if not trace.transport_failed:
                normalized_output, validation_error = _validate_output(
                    trial, trace.completed.stdout, packet, trace.command.requested_model
                )
            self._write_attempt(trial, trace, attempt, prompt, validation_error)
            if not trace.transport_failed:
                if validation_error is None:
                    accepted = self._output_root / "accepted" / f"{trial.trial_id}.json"
                    accepted.parent.mkdir(parents=True, exist_ok=True)
                    _write_new(accepted, normalized_output)
                    return TrialResult(trial.trial_id, True, attempt)
                if attempt == 2:
                    self._write_rejected(trial, normalized_output, validation_error)
        return TrialResult(trial.trial_id, False, 2)

    def _write_rejected(self, trial: Trial, output: str, reason: str) -> None:
        directory = self._output_root / "rejected"
        directory.mkdir(parents=True, exist_ok=True)
        _write_new(directory / f"{trial.trial_id}.json", output)
        _write_new(directory / f"{trial.trial_id}.reason.txt", reason)

    def _attempt(
        self,
        trial: Trial,
        prompt: str,
        schema_path: Path,
        packet: EvidencePacket,
    ) -> AttemptTrace:
        with tempfile.TemporaryDirectory(prefix="servo-r24-") as temporary:
            sandbox = Path(temporary)
            input_dir = sandbox / "input"
            input_dir.mkdir()
            (sandbox / "output").mkdir()
            staged_schema = input_dir / "response.schema.json"
            shutil.copyfile(schema_path, staged_schema)
            _write_new(input_dir / "prompt.txt", prompt)
            _write_new(
                input_dir / "packet.json",
                packet.model_dump_json(indent=2, by_alias=True),
            )
            command = build_command(trial, Path("input/response.schema.json"), sandbox)
            _write_new(
                sandbox / "run-manifest.json",
                json.dumps(
                    {
                        "trial_id": trial.trial_id,
                        "vendor": trial.vendor,
                        "requested_model": command.requested_model,
                        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                        "schema_sha256": hashlib.sha256(staged_schema.read_bytes()).hexdigest(),
                    },
                    indent=2,
                    sort_keys=True,
                ),
            )
            started = time.monotonic()
            try:
                completed = self._transport(
                    command.arguments, prompt, sandbox, self._timeout_seconds
                )
            except subprocess.TimeoutExpired as error:
                completed = subprocess.CompletedProcess(
                    command.arguments,
                    124,
                    stdout=_timeout_text(error.stdout),
                    stderr="timeout",
                )
            except OSError as error:
                completed = subprocess.CompletedProcess(
                    command.arguments, 127, stdout="", stderr=str(error)
                )
            elapsed = time.monotonic() - started
            return AttemptTrace(
                completed=completed,
                command=command,
                transport_failed=completed.returncode != 0,
                elapsed_seconds=elapsed,
                schema_sha256=hashlib.sha256(staged_schema.read_bytes()).hexdigest(),
                packet_sha256=hashlib.sha256(
                    packet.model_dump_json(by_alias=True).encode()
                ).hexdigest(),
                execution_arguments=build_execution_command(command.arguments),
                sandbox_root=str(sandbox),
            )

    def _write_attempt(
        self,
        trial: Trial,
        trace: AttemptTrace,
        attempt: int,
        prompt: str,
        validation_error: str | None,
    ) -> None:
        directory = self._output_root / "trials" / trial.trial_id
        directory.mkdir(parents=True, exist_ok=True)
        stem = directory / f"attempt-{attempt}"
        metadata = {
            "trial": asdict(trial),
            "attempt": attempt,
            "timestamp_utc": datetime.now(UTC).isoformat(),
            "elapsed_seconds": trace.elapsed_seconds,
            "requested_model": trace.command.requested_model,
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "schema_sha256": trace.schema_sha256,
            "packet_sha256": trace.packet_sha256,
            "argv_sha256": hashlib.sha256(
                json.dumps(trace.execution_arguments, separators=(",", ":")).encode()
            ).hexdigest(),
            "returncode": trace.completed.returncode,
            "stdout_sha256": hashlib.sha256(trace.completed.stdout.encode()).hexdigest(),
            "stderr_sha256": hashlib.sha256(trace.completed.stderr.encode()).hexdigest(),
            "validation_error": validation_error,
            "sandbox_root": trace.sandbox_root,
        }
        _write_new(stem.with_suffix(".stdout.txt"), trace.completed.stdout)
        _write_new(stem.with_suffix(".stderr.txt"), trace.completed.stderr)
        _write_new(stem.with_suffix(".json"), json.dumps(metadata, indent=2, default=str))


def _write_new(path: Path, content: str) -> None:
    try:
        with path.open("x", encoding="utf-8") as handle:
            _ = handle.write(content)
    except FileExistsError as error:
        raise OutputExistsError(path) from error


def _timeout_text(value: bytes | str | None) -> str:
    match value:
        case bytes():
            return value.decode(errors="replace")
        case str():
            return value
        case None:
            return ""
        case unreachable:
            assert_never(unreachable)
