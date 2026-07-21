from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from r24_final.runner import (
    Condition,
    ExperimentRunner,
    ScheduleError,
    Trial,
    Vendor,
    build_command,
    load_schedule,
    _validate_output,
)
from r24_final.adapters import Command, CommandPolicyError, validate_command
from r24_final.assets import schedule_json
from r24_final.evidence import EvidenceItem, EvidencePacket


def _trial(
    vendor: Vendor = Vendor.CODEX, condition: Condition = Condition.BASELINE
) -> Trial:
    return Trial(
        trial_id="codex-R01-baseline",
        vendor=vendor,
        record_id="R01",
        condition=condition,
        period=1,
        order=1,
    )


def _baseline_payload(vendor: Vendor, quote: str = "source text") -> dict[str, object]:
    return {
        "record_id": "R01",
        "vendor": vendor.value,
        "model_id": "untrusted self-report",
        "memo": "Evidence-bound baseline memo.",
        "envelope": {
            "diagnostics": [{
                "id": "D01",
                "statement": "The source does not report a reliability test.",
                "kind": "missing_evidence",
                "evidence_ids": ["E01"],
                "exact_quotes": [{"evidence_id": "E01", "exact_quote": quote}],
                "consequence": "Reliability remains unestablished.",
            }],
            "recommendations": [{
                "id": "A01",
                "priority_rank": 1,
                "proposed_action": "Obtain independent evidence.",
                "linked_diagnostic_ids": ["D01"],
                "evidence_ids": ["E01"],
                "exact_quotes": [{"evidence_id": "E01", "exact_quote": quote}],
                "success_check": {
                    "observable": "A reliability result is reported.",
                    "comparator_or_threshold": "against a stated baseline",
                    "evidence_needed": "Held-out outcomes.",
                },
            }],
        },
    }


def _packet() -> EvidencePacket:
    return EvidencePacket(
        record_id="R01",
        pdf_id="a" * 64,
        items=(EvidenceItem(evidence_id="E01", page=4, text="source text"),),
    )


def _servo_payload(vendor: Vendor, pdf_id: str) -> dict[str, object]:
    payload = _baseline_payload(vendor)
    del payload["memo"]
    payload.update({
        "channels": [{
            "channel_id": "V01",
            "operational_status": "implemented",
            "target_property": ["task_performance"],
            "evidence_source": ["benchmark_metric"],
            "evaluator_substrate": ["statistical_model"],
            "decision_role": ["search_control"],
            "feedback_path": ["policy_control"],
            "external_independence": "internal_separate_component",
            "reliability_evidence_type": ["none_reported"],
            "reliability_finding": "not_established",
            "experimental_fidelity": ["computational_experiment"],
            "quotes": [{
                "evidence_id": "E01",
                "pdf_id": pdf_id,
                "page": 4,
                "quote": "source text",
                "rationale": "supports the coding",
            }],
        }],
        "policy_type": ["adaptive"],
        "memory_structure": ["journal"],
        "human_authority": {
            "generator": [],
            "executor": [],
            "validator": [],
            "memory": [],
            "policy": [],
        },
    })
    return payload


def test_command_disables_fallback_and_persistent_sessions(tmp_path: Path) -> None:
    # Given
    schema_path = tmp_path / "input" / "response.schema.json"
    schema_path.parent.mkdir()
    schema_path.write_text('{"type":"object"}', encoding="utf-8")

    # When
    command = build_command(_trial(), Path("input/response.schema.json"), tmp_path)

    # Then
    assert "--ephemeral" in command.arguments
    assert "--ignore-user-config" in command.arguments
    assert "--ignore-rules" in command.arguments
    assert 'web_search="disabled"' in command.arguments
    assert "--fallback-model" not in command.arguments

    claude_command = build_command(
        _trial(Vendor.CLAUDE), Path("input/response.schema.json"), tmp_path
    )
    assert "--safe-mode" in claude_command.arguments
    assert "--tools" in claude_command.arguments
    assert "--json-schema" in claude_command.arguments

    gemini_command = build_command(
        _trial(Vendor.GEMINI), Path("input/response.schema.json"), tmp_path
    )
    assert gemini_command.arguments[-1] == "--prompt"


def test_command_policy_rejects_unknown_and_duplicate_flags(tmp_path: Path) -> None:
    schema_path = tmp_path / "input" / "response.schema.json"
    schema_path.parent.mkdir()
    schema_path.write_text('{"type":"object"}', encoding="utf-8")
    command = build_command(_trial(), Path("input/response.schema.json"), tmp_path)

    with pytest.raises(CommandPolicyError, match="unknown"):
        validate_command(
            Command((*command.arguments[:-1], "--mystery", command.arguments[-1]), command.vendor, command.requested_model)
        )
    with pytest.raises(CommandPolicyError, match="duplicate"):
        validate_command(
            Command((*command.arguments[:-1], "--ephemeral", command.arguments[-1]), command.vendor, command.requested_model)
        )


def test_schedule_rejects_less_than_42_trials(tmp_path: Path) -> None:
    # Given
    schedule_path = tmp_path / "schedule.json"
    schedule_path.write_text(
        json.dumps(
            [
                {
                    "trial_id": "codex-R01-baseline",
                    "vendor": "codex",
                    "record_id": "R01",
                    "condition": "baseline",
                    "period": 1,
                    "order": 1,
                }
            ]
        ),
        encoding="utf-8",
    )

    # When / Then
    with pytest.raises(ScheduleError, match="42"):
        load_schedule(schedule_path)


def test_schedule_rejects_retired_baseline_condition(tmp_path: Path) -> None:
    # Given
    schedule_path = tmp_path / "schedule.json"
    raw = json.loads(
        schedule_json(tuple(f"R{index:02d}" for index in range(1, 15)), 20260720)
    )
    raw[0]["condition"] = "baseline"
    schedule_path.write_text(json.dumps(raw), encoding="utf-8")

    # When / Then
    with pytest.raises(ScheduleError, match="Servo-only"):
        load_schedule(schedule_path)


def test_runner_retries_transport_failure_exactly_once(tmp_path: Path) -> None:
    # Given
    calls: list[tuple[str, ...]] = []
    schema_path = tmp_path / "schema.json"
    schema_path.write_text('{"type":"object"}', encoding="utf-8")

    def transport(
        arguments: tuple[str, ...], prompt: str, cwd: Path, timeout_seconds: int
    ) -> subprocess.CompletedProcess[str]:
        del prompt, cwd, timeout_seconds
        calls.append(arguments)
        return subprocess.CompletedProcess(arguments, 75, stdout="", stderr="network")

    runner = ExperimentRunner(output_root=tmp_path / "outputs", transport=transport)

    # When
    result = runner.run_trial(
        trial=_trial(),
        prompt="fixed prompt",
        schema_path=schema_path,
        packet=_packet(),
    )

    # Then
    assert result.succeeded is False
    assert len(calls) == 2
    assert calls[0] == calls[1]
    assert len(list((tmp_path / "outputs" / "trials").rglob("attempt-*.json"))) == 2


def test_runner_retries_invalid_output_exactly_once(tmp_path: Path) -> None:
    # Given
    calls = 0
    schema_path = tmp_path / "schema.json"
    schema_path.write_text('{"type":"object"}', encoding="utf-8")

    def transport(
        arguments: tuple[str, ...], prompt: str, cwd: Path, timeout_seconds: int
    ) -> subprocess.CompletedProcess[str]:
        del prompt, cwd, timeout_seconds
        nonlocal calls
        calls += 1
        return subprocess.CompletedProcess(arguments, 0, stdout="not json", stderr="")

    runner = ExperimentRunner(output_root=tmp_path / "outputs", transport=transport)

    # When
    result = runner.run_trial(
        trial=_trial(Vendor.CLAUDE),
        prompt="fixed prompt",
        schema_path=schema_path,
        packet=_packet(),
    )

    # Then
    assert result.succeeded is False
    assert calls == 2


def test_runner_can_accept_second_attempt_after_invalid_first(tmp_path: Path) -> None:
    # Given
    calls = 0
    schema_path = tmp_path / "schema.json"
    schema_path.write_text('{"type":"object"}', encoding="utf-8")
    valid = _baseline_payload(Vendor.CLAUDE)

    def transport(
        arguments: tuple[str, ...], prompt: str, cwd: Path, timeout_seconds: int
    ) -> subprocess.CompletedProcess[str]:
        del prompt, cwd, timeout_seconds
        nonlocal calls
        calls += 1
        stdout = "not json" if calls == 1 else json.dumps(valid)
        return subprocess.CompletedProcess(arguments, 0, stdout=stdout, stderr="")

    output_root = tmp_path / "outputs"
    runner = ExperimentRunner(output_root=output_root, transport=transport)

    # When
    result = runner.run_trial(
        trial=_trial(Vendor.CLAUDE),
        prompt="fixed prompt",
        schema_path=schema_path,
        packet=_packet(),
    )

    # Then
    assert result.succeeded is True
    assert result.attempts == 2
    assert calls == 2
    assert len(list((output_root / "trials").rglob("attempt-*.json"))) == 2
    assert not (output_root / "rejected").exists()


def test_runner_rejects_fenced_json_and_does_not_accept_it(
    tmp_path: Path,
) -> None:
    # Given
    payload = {
        "record_id": "R01",
        "vendor": "gemini",
        "model_id": "gemini-2.5-pro",
        "memo": "Evidence-bound baseline memo.",
        "envelope": {
            "diagnostics": [{
                "id": "D01",
                "statement": "The source does not report a reliability test.",
                "kind": "missing_evidence",
                "evidence_ids": ["E01"],
                "exact_quotes": [{"evidence_id": "E01", "exact_quote": "source text"}],
                "consequence": "Reliability remains unestablished.",
            }],
            "recommendations": [{
                "id": "A01",
                "priority_rank": 1,
                "proposed_action": "Obtain independent evidence.",
                "linked_diagnostic_ids": ["D01"],
                "evidence_ids": ["E01"],
                "exact_quotes": [{"evidence_id": "E01", "exact_quote": "source text"}],
                "success_check": {
                    "observable": "A reliability result is reported.",
                    "comparator_or_threshold": "against a stated baseline",
                    "evidence_needed": "Held-out outcomes.",
                },
            }],
        },
    }
    raw = f"```json\n{json.dumps(payload)}\n```\n"

    def transport(
        arguments: tuple[str, ...], prompt: str, cwd: Path, timeout_seconds: int
    ) -> subprocess.CompletedProcess[str]:
        del prompt, cwd, timeout_seconds
        return subprocess.CompletedProcess(arguments, 0, stdout=raw, stderr="")

    output_root = tmp_path / "outputs"
    runner = ExperimentRunner(output_root=output_root, transport=transport)
    schema_path = tmp_path / "schema.json"
    schema_path.write_text('{"type":"object"}', encoding="utf-8")

    # When
    result = runner.run_trial(
        trial=_trial(Vendor.GEMINI),
        prompt="fixed prompt",
        schema_path=schema_path,
        packet=_packet(),
    )

    # Then
    accepted = output_root / "accepted" / "codex-R01-baseline.json"
    rejected = output_root / "rejected" / "codex-R01-baseline.json"
    assert result.succeeded is False
    assert not accepted.exists()
    assert "```" in rejected.read_text()


def test_each_attempt_uses_an_isolated_staged_directory(tmp_path: Path) -> None:
    # Given
    observed: list[tuple[Path, tuple[str, ...]]] = []

    def transport(
        arguments: tuple[str, ...], prompt: str, cwd: Path, timeout_seconds: int
    ) -> subprocess.CompletedProcess[str]:
        del prompt, timeout_seconds
        observed.append((cwd, tuple(path.name for path in cwd.iterdir())))
        return subprocess.CompletedProcess(arguments, 0, stdout="{}", stderr="")

    runner = ExperimentRunner(output_root=tmp_path / "outputs", transport=transport)
    schema_path = tmp_path / "schema.json"
    schema_path.write_text('{"type":"object"}', encoding="utf-8")

    # When
    runner.run_trial(
        trial=_trial(Vendor.GEMINI),
        prompt="fixed prompt",
        schema_path=schema_path,
        packet=_packet(),
    )

    # Then
    assert set(observed[0][1]) == {"input", "output", "run-manifest.json"}
    assert not observed[0][0].exists()


@pytest.mark.parametrize(
    ("vendor", "requested_model"),
    [
        (Vendor.CLAUDE, "claude-opus-4-8"),
        (Vendor.CODEX, "gpt-5.5"),
        (Vendor.GEMINI, "Gemini 3.1 Pro (High)"),
    ],
)
def test_common_post_response_hook_injects_runtime_model_provenance(
    vendor: Vendor, requested_model: str
) -> None:
    normalized, error = _validate_output(
        _trial(vendor),
        json.dumps(_baseline_payload(vendor)),
        _packet(),
        requested_model,
    )

    assert error is None
    assert json.loads(normalized)["model_id"] == requested_model


@pytest.mark.parametrize("vendor", list(Vendor))
def test_common_post_response_hook_rejects_fabricated_envelope_quote(
    vendor: Vendor,
) -> None:
    normalized, error = _validate_output(
        _trial(vendor),
        json.dumps(_baseline_payload(vendor, quote="fabricated")),
        _packet(),
        "runtime-owned-model",
    )

    assert json.loads(normalized)["model_id"] == "runtime-owned-model"
    assert error is not None
    assert "frozen packet quotation" in error


@pytest.mark.parametrize("vendor", list(Vendor))
def test_common_post_response_hook_rejects_record_id_instead_of_pdf_hash(
    vendor: Vendor,
) -> None:
    normalized, error = _validate_output(
        _trial(vendor, Condition.SERVO),
        json.dumps(_servo_payload(vendor, pdf_id="R01")),
        _packet(),
        "runtime-owned-model",
    )

    assert json.loads(normalized)["model_id"] == "runtime-owned-model"
    assert error is not None
    assert "source identity" in error


def test_common_post_response_hook_rejects_duplicate_json_keys() -> None:
    raw = json.dumps(_baseline_payload(Vendor.CODEX))
    raw = raw.replace('"record_id": "R01"', '"record_id": "R01", "record_id": "R02"', 1)

    _, error = _validate_output(_trial(), raw, _packet(), "runtime-owned-model")

    assert error is not None
    assert "duplicate JSON key" in error


def test_common_post_response_hook_rejects_nonfinite_json_numbers() -> None:
    raw = json.dumps(_baseline_payload(Vendor.CODEX)).replace(
        '"priority_rank": 1', '"priority_rank": NaN', 1
    )

    _, error = _validate_output(_trial(), raw, _packet(), "runtime-owned-model")

    assert error is not None
    assert "non-finite JSON number" in error
