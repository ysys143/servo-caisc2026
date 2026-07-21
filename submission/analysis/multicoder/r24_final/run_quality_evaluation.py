from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import time
from dataclasses import asdict
from pathlib import Path
from typing import Annotated, Final

import typer
from pydantic import ValidationError

from r24_final.adapters import build_command, subprocess_transport
from r24_final.generation_snapshot import verify_generation_snapshot
from r24_final.lifecycle import (
    finish_run,
    start_run,
    verify_protocol,
    verify_smoke_gate,
)
from r24_final.recommendation_quality import (
    JudgeTrial,
    QualityJudgment,
    anonymous_pair,
    build_judge_schedule,
    build_quality_prompt,
    schedule_sha256,
    validate_quality_judgment,
)
from r24_final.output_validation import _single_json_document
from r24_final.schedule import Condition, Trial


ROOT: Final = Path(__file__).resolve().parent
app = typer.Typer(add_completion=False, no_args_is_help=False)


@app.command()
def main(
    generation_run: Annotated[Path, typer.Option("--generation-run")] = ROOT / "runs" / "r24-run-004",
    dry_run: Annotated[bool, typer.Option("--dry-run/--execute")] = True,
) -> None:
    _require_complete_generation(generation_run)
    trials = build_judge_schedule(tuple(f"R{i:02d}" for i in range(1, 15)))
    quality_dir = generation_run / "recommendation-quality"
    if dry_run:
        typer.echo(json.dumps({"judge_trials": len(trials), "schedule_sha256": schedule_sha256(trials)}, sort_keys=True))
        return
    verify_smoke_gate(ROOT)
    if quality_dir.exists():
        raise typer.BadParameter(f"quality output already exists: {quality_dir}")
    start_run(ROOT, quality_dir)
    _write_new(quality_dir / "schedule.json", json.dumps([asdict(t) for t in trials], indent=2))
    _write_new(quality_dir / "quality.schema.json", json.dumps(QualityJudgment.model_json_schema(), indent=2, sort_keys=True))
    completed = 0
    try:
        for trial in trials:
            verify_protocol(ROOT, quality_dir)
            if not _run_trial(generation_run, quality_dir, trial):
                finish_run(quality_dir, "failed", completed_trials=completed, failed_trial=trial.trial_id)
                raise typer.Exit(1)
            completed += 1
    except BaseException as error:
        if not (quality_dir / "RUN_FAILED.json").exists():
            finish_run(quality_dir, "stopped", completed_trials=completed, reason=type(error).__name__)
        raise
    finish_run(quality_dir, "completed", completed_trials=completed)


def _require_complete_generation(run_dir: Path) -> None:
    try:
        completed = verify_generation_snapshot(ROOT, run_dir)
    except ValueError as error:
        raise typer.BadParameter(str(error)) from error
    outputs = completed.get("accepted_outputs")
    if not isinstance(outputs, dict) or len(outputs) != 84:
        raise typer.BadParameter("quality judging requires a sealed 84-output generation run")


def _run_trial(run_dir: Path, quality_dir: Path, judge: JudgeTrial) -> bool:
    prompt = build_quality_prompt(ROOT, run_dir, judge)
    pair = anonymous_pair(run_dir, judge)
    schema_path = quality_dir / "quality.schema.json"
    command_trial = Trial(judge.trial_id, judge.judge_vendor, judge.record_id, Condition.BASELINE, 1, 0)
    with tempfile.TemporaryDirectory(prefix="servo-r24-quality-") as temporary:
        sandbox = Path(temporary)
        input_dir = sandbox / "input"
        input_dir.mkdir()
        (sandbox / "output").mkdir()
        staged_schema = input_dir / "response.schema.json"
        shutil.copyfile(schema_path, staged_schema)
        _write_new(input_dir / "prompt.txt", prompt)
        command = build_command(command_trial, Path("input/response.schema.json"), sandbox)
        _write_new(
            sandbox / "run-manifest.json",
            json.dumps(
                {
                    "trial_id": judge.trial_id,
                    "judge_vendor": judge.judge_vendor,
                    "requested_model": command.requested_model,
                },
                indent=2,
                sort_keys=True,
            ),
        )
        started = time.monotonic()
        try:
            completed = subprocess_transport(command.arguments, prompt, sandbox, 600)
        except (OSError, subprocess.TimeoutExpired) as error:
            completed = subprocess.CompletedProcess(command.arguments, 124, stdout="", stderr=str(error))
        elapsed = time.monotonic() - started
    normalized = _single_json_document(completed.stdout)
    validation_error: str | None = None
    try:
        result = QualityJudgment.model_validate_json(normalized)
        validate_quality_judgment(result, judge, pair)
    except (ValidationError, ValueError) as error:
        validation_error = str(error)
    trial_dir = quality_dir / "trials" / judge.trial_id
    trial_dir.mkdir(parents=True)
    _write_new(trial_dir / "stdout.txt", completed.stdout)
    _write_new(trial_dir / "stderr.txt", completed.stderr)
    _write_new(trial_dir / "metadata.json", json.dumps({"trial": asdict(judge), "elapsed_seconds": elapsed, "returncode": completed.returncode, "validation_error": validation_error}, indent=2))
    if completed.returncode != 0 or validation_error is not None:
        rejected = quality_dir / "rejected"
        rejected.mkdir(exist_ok=True)
        _write_new(rejected / f"{judge.trial_id}.json", normalized)
        _write_new(
            rejected / f"{judge.trial_id}.reason.txt",
            validation_error or f"transport return code {completed.returncode}",
        )
        return False
    accepted = quality_dir / "accepted"
    accepted.mkdir(exist_ok=True)
    _write_new(accepted / f"{judge.trial_id}.json", normalized)
    return True


def _write_new(path: Path, content: str) -> None:
    with path.open("x", encoding="utf-8") as handle:
        _ = handle.write(content)


if __name__ == "__main__":
    app()
