from __future__ import annotations

import hashlib
import json
from pathlib import Path

from r24_final.lifecycle import finish_run, protocol_manifest, verify_protocol
from r24_final.schedule import Trial


def finish_generation_run(root: Path, output_dir: Path, trials: tuple[Trial, ...]) -> None:
    verify_protocol(root, output_dir)
    accepted_dir = output_dir / "accepted"
    scheduled = {trial.trial_id: trial for trial in trials}
    present = {path.stem: path for path in accepted_dir.glob("*.json")}
    if set(present) != set(scheduled):
        raise ValueError("accepted outputs must exactly match the frozen schedule")
    outputs: dict[str, dict[str, str]] = {}
    for trial_id, trial in scheduled.items():
        path = present[trial_id]
        raw = _read_object(path, f"invalid accepted output: {trial_id}")
        if raw.get("record_id") != trial.record_id or raw.get("vendor") != trial.vendor:
            raise ValueError(f"accepted output identity mismatch: {trial_id}")
        outputs[trial_id] = {
            "path": str(path.relative_to(output_dir)),
            "sha256": _sha256_file(path),
            "record_id": trial.record_id,
            "vendor": trial.vendor,
            "condition": trial.condition.value,
        }
    finish_run(
        output_dir,
        "completed",
        completed_trials=len(trials),
        schedule_sha256=_sha256_file(root / "schedule.json"),
        accepted_outputs=outputs,
    )


def verify_generation_snapshot(root: Path, run_dir: Path) -> dict[str, object]:
    completed = _read_object(run_dir / "RUN_COMPLETED.json", "generation is not completed")
    started = _read_object(run_dir / "RUN_STARTED.json", "generation has no start manifest")
    if started.get("protocol_sha256") != protocol_manifest(root)["protocol_sha256"]:
        raise ValueError("generation protocol does not match the current protocol")
    outputs = completed.get("accepted_outputs")
    if not isinstance(outputs, dict) or not outputs:
        raise ValueError("generation completion manifest has no sealed outputs")
    for trial_id, item in outputs.items():
        if not isinstance(trial_id, str) or not isinstance(item, dict):
            raise ValueError("generation completion manifest is malformed")
        relative, expected = item.get("path"), item.get("sha256")
        if not isinstance(relative, str) or not isinstance(expected, str):
            raise ValueError("generation output provenance is malformed")
        path = (run_dir / relative).resolve()
        if run_dir.resolve() not in path.parents or not path.is_file():
            raise ValueError(f"sealed generation output is absent: {trial_id}")
        if _sha256_file(path) != expected:
            raise ValueError(f"sealed generation output changed: {trial_id}")
    return completed


def _read_object(path: Path, message: str) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(message) from error
    if not isinstance(value, dict):
        raise ValueError(message)
    return value


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
