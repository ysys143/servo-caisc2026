from __future__ import annotations

import json
from pathlib import Path

import pytest

from r24_final.generation_snapshot import finish_generation_run
from r24_final.lifecycle import finish_run, start_run
from r24_final.schedule import Condition, Trial


def _protocol_root(tmp_path: Path) -> Path:
    root = tmp_path / "protocol"
    (root / "packets").mkdir(parents=True)
    (root / "probes").mkdir()
    from r24_final.lifecycle import PROTOCOL_FILES
    for name in PROTOCOL_FILES:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}" if name.endswith(".json") else name)
    (root / "packets" / "R01.json").write_text("{}")
    (root / "probes" / "R01.json").write_text("{}")
    return root


def test_run_lifecycle_is_append_only_and_hashes_protocol(tmp_path: Path) -> None:
    root = _protocol_root(tmp_path)
    run = tmp_path / "run-003"
    start_run(root, run)
    started = json.loads((run / "RUN_STARTED.json").read_text())
    assert len(started["protocol_sha256"]) == 64
    finish_run(run, "completed", completed_trials=84)
    with pytest.raises(FileExistsError):
        finish_run(run, "failed")


def test_start_refuses_any_existing_run_directory(tmp_path: Path) -> None:
    root = _protocol_root(tmp_path)
    run = tmp_path / "run-003"
    run.mkdir()
    with pytest.raises(FileExistsError, match="already exists"):
        start_run(root, run)


def test_generation_completion_binds_exact_scheduled_outputs(tmp_path: Path) -> None:
    root = _protocol_root(tmp_path)
    run = tmp_path / "run-004"
    start_run(root, run)
    accepted = run / "accepted"
    accepted.mkdir()
    trials = tuple(
        Trial(f"codex-R{index:02d}-1", "codex", f"R{index:02d}", Condition.BASELINE, 1, index)
        for index in range(1, 3)
    )
    for trial in trials:
        (accepted / f"{trial.trial_id}.json").write_text(
            json.dumps({"record_id": trial.record_id, "vendor": trial.vendor}), encoding="utf-8"
        )

    finish_generation_run(root, run, trials)
    completed = json.loads((run / "RUN_COMPLETED.json").read_text())

    assert set(completed["accepted_outputs"]) == {trial.trial_id for trial in trials}
    assert all(len(item["sha256"]) == 64 for item in completed["accepted_outputs"].values())


def test_generation_completion_rejects_extra_output(tmp_path: Path) -> None:
    root = _protocol_root(tmp_path)
    run = tmp_path / "run-004"
    start_run(root, run)
    accepted = run / "accepted"
    accepted.mkdir()
    trial = Trial("codex-R01-1", "codex", "R01", Condition.BASELINE, 1, 0)
    (accepted / f"{trial.trial_id}.json").write_text(
        '{"record_id":"R01","vendor":"codex"}', encoding="utf-8"
    )
    (accepted / "unexpected.json").write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="exactly match"):
        finish_generation_run(root, run, (trial,))
