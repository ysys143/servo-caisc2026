# /// script
# requires-python = ">=3.12"
# dependencies = ["pydantic>=2.12,<3", "typer>=0.21,<1"]
# ///
# How to run: PYTHONPATH=analysis/multicoder uv run python -m r24_final.run_experiment --dry-run

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Annotated, Final, assert_never

import typer
from pydantic import TypeAdapter

from r24_final.assets import schedule_json, servo_json_schema
from r24_final.generation_snapshot import finish_generation_run
from r24_final.lifecycle import (
    finish_run,
    start_run,
    verify_protocol,
    verify_smoke_gate,
)
from r24_final.runner import ExperimentRunner, load_schedule
from r24_final.evidence import EvidencePacket
from r24_final.schedule import Condition


ROOT: Final = Path(__file__).resolve().parent
SEED: Final = 20260720
app = typer.Typer(add_completion=False, no_args_is_help=False)


type JsonValue = None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
JSON_ADAPTER: Final = TypeAdapter(JsonValue)


def prepare_assets(root: Path) -> None:
    record_ids = tuple(f"R{index:02d}" for index in range(1, 15))
    _write_frozen(root / "schedule.json", schedule_json(record_ids, SEED))
    schemas = {"servo.schema.json": servo_json_schema()}
    for filename, schema in schemas.items():
        encoded = json.dumps(schema, indent=2, sort_keys=True).encode()
        _write_frozen(root / filename, encoded)
        _write_frozen(root / "schemas" / filename, encoded)


def build_prompt(root: Path, record_id: str, condition: Condition, vendor: str) -> str:
    packet = (root / "packets" / f"{record_id}.json").read_text(encoding="utf-8")
    match condition:
        case Condition.BASELINE:
            instructions = (root / "baseline_prompt.md").read_text(encoding="utf-8")
            schema = (root / "baseline.schema.json").read_text()
            manual = ""
        case Condition.SERVO:
            instructions = (root / "servo_prompt.md").read_text(encoding="utf-8")
            schema = (root / "servo.schema.json").read_text()
            manual = (root / "coding_manual.md").read_text(encoding="utf-8")
        case unreachable:
            assert_never(unreachable)
    return "\n\n".join(
        (
            instructions,
            manual,
            f"Scheduled metadata: record_id={record_id}; vendor={vendor}. Use the CLI model identifier as model_id.",
            f"Anonymous source packet:\n{packet}",
            f"Required JSON schema:\n{schema}",
        )
    )


@app.command()
def main(
    dry_run: Annotated[bool, typer.Option("--dry-run/--execute")] = True,
    output_dir: Annotated[Path, typer.Option("--output-dir")] = ROOT / "runs" / "r24-run-005",
) -> None:
    prepare_assets(ROOT)
    schedule = load_schedule(ROOT / "schedule.json")
    prompt_hashes = tuple(
        hashlib.sha256(
            build_prompt(ROOT, trial.record_id, trial.condition, trial.vendor).encode()
        ).hexdigest()
        for trial in schedule
    )
    if dry_run:
        typer.echo(
            json.dumps(
                {
                    "trial_count": len(schedule),
                    "unique_prompt_count": len(set(prompt_hashes)),
                    "schedule_sha256": hashlib.sha256(
                        (ROOT / "schedule.json").read_bytes()
                    ).hexdigest(),
                },
                sort_keys=True,
            )
        )
        return
    try:
        verify_smoke_gate(ROOT)
    except ValueError as error:
        raise typer.BadParameter(str(error)) from error
    try:
        start_run(ROOT, output_dir)
    except FileExistsError as error:
        raise typer.BadParameter(str(error)) from error
    _write_versions(output_dir)
    runner = ExperimentRunner(output_dir)
    completed = 0
    try:
        for trial in schedule:
            verify_protocol(ROOT, output_dir)
            schema_path = ROOT / f"{trial.condition.value}.schema.json"
            prompt = build_prompt(ROOT, trial.record_id, trial.condition, trial.vendor)
            packet = EvidencePacket.model_validate_json(
                (ROOT / "packets" / f"{trial.record_id}.json").read_text(encoding="utf-8")
            )
            result = runner.run_trial(trial, prompt, schema_path, packet)
            typer.echo(f"{trial.trial_id}: {'accepted' if result.succeeded else 'failed'}")
            if not result.succeeded:
                finish_run(output_dir, "failed", completed_trials=completed, failed_trial=trial.trial_id)
                raise typer.Exit(1)
            completed += 1
        verify_protocol(ROOT, output_dir)
    except BaseException as error:
        if not any(output_dir.glob("RUN_FAILED.json")):
            finish_run(
                output_dir,
                "stopped",
                completed_trials=completed,
                reason=type(error).__name__,
            )
        raise
    finish_generation_run(ROOT, output_dir, schedule)


def _write_frozen(path: Path, expected: bytes) -> None:
    if path.exists():
        existing_value = JSON_ADAPTER.validate_json(path.read_text(encoding="utf-8"))
        expected_value = JSON_ADAPTER.validate_json(expected)
        if existing_value != expected_value:
            raise typer.BadParameter(f"frozen asset differs from generated content: {path}")
        return
    _ = path.write_bytes(expected)


def _write_versions(output_dir: Path) -> None:
    versions: dict[str, str] = {}
    for executable in ("claude", "codex", "agy"):
        completed = subprocess.run(
            (executable, "--version"), capture_output=True, text=True, timeout=10, check=False
        )
        versions[executable] = (completed.stdout + completed.stderr).strip()
    _ = (output_dir / "cli_versions.json").write_text(
        json.dumps(versions, indent=2, sort_keys=True), encoding="utf-8"
    )


if __name__ == "__main__":
    app()
