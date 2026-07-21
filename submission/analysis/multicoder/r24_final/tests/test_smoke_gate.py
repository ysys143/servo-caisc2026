from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from r24_final.lifecycle import (
    REQUIRED_SMOKE_REPORTS,
    SMOKE_REPORT_DIRECTORY,
    assemble_smoke_manifest,
    smoke_binding,
    verify_smoke_gate,
)
from r24_final.hook_negative import build_report
from r24_final.static_checks import build_static_evidence


CORE_RECORDS = frozenset({"R01", "R02", "R03", "R04", "R05", "R14"})


def _artifact_sha256(path: Path) -> str:
    entries = {
        str(item.relative_to(path)): hashlib.sha256(item.read_bytes()).hexdigest()
        for item in sorted(path.rglob("*"))
        if item.is_file()
    }
    return hashlib.sha256(
        json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _protocol_root(tmp_path: Path) -> Path:
    source = Path(__file__).resolve().parents[1]
    root = tmp_path / "protocol"
    shutil.copytree(
        source,
        root,
        ignore=shutil.ignore_patterns("runs", "smoke_reports", "SMOKE_PASSED.json", "__pycache__"),
    )
    return root


def _write_reports(root: Path) -> None:
    directory = root / SMOKE_REPORT_DIRECTORY
    directory.mkdir()
    binding = smoke_binding(root)
    for report_name, check_ids in REQUIRED_SMOKE_REPORTS.items():
        raw = directory / f"raw/{report_name}.json"
        raw.parent.mkdir(exist_ok=True)
        cells = [
            {"cell_id": f"{vendor}:{condition}", "trial_root": f"/{vendor}-{condition}"}
            for vendor in ("claude", "codex", "gemini")
            for condition in ("servo",)
        ]
        for item in cells:
            artifact = directory / "observer" / report_name / item["cell_id"].replace(":", "-")
            artifact.mkdir(parents=True)
            (artifact / "trace.txt").write_text(item["cell_id"], encoding="utf-8")
            item["artifact_root"] = str(artifact.relative_to(root))
            item["artifact_tree_sha256"] = _artifact_sha256(artifact)
        if report_name == "STATIC_GATE_REPORT":
            evidence_body = build_static_evidence(
                root, binding["protocol_sha256"]
            ).model_dump(mode="json")
        elif report_name == "HOOK_NEGATIVE_REPORT":
            evidence_body = build_report()
        elif report_name == "ISOLATION_REPORT":
            evidence_body = {
                "evidence_type": "task-isolation-v1",
                "protocol_sha256": binding["protocol_sha256"],
                "cells": [
                    item | {
                        "attack_invocation_id": f"attack-{item['cell_id']}",
                        "attack_prompt_sha256": "1" * 64,
                        "canary_sha256": "2" * 64,
                        "stdout_sha256": "3" * 64,
                        "stderr_sha256": "4" * 64,
                        "process_policy_sha256": "5" * 64,
                        "forbidden_tool_events": 0,
                        "outside_canary_hits": 0,
                        "scoring_asset_hits": 0,
                        "cross_trial_hits": 0,
                    }
                    for item in cells
                ],
            }
        else:
            evidence_body = {
                "evidence_type": "functional-matrix-v1",
                "protocol_sha256": binding["protocol_sha256"],
                "cells": [
                    item | {
                        "invocation_id": f"inv-{index}",
                        "returncode": 0,
                        "accepted": True,
                        "prompt_sha256": "a" * 64,
                        "packet_sha256": "b" * 64,
                        "schema_sha256": "c" * 64,
                        "stdout_sha256": "d" * 64,
                        "stderr_sha256": "e" * 64,
                    }
                    for index, item in enumerate(cells)
                ],
                "latency_boundary_passed": True,
            }
        raw.write_text(json.dumps(evidence_body, sort_keys=True), encoding="utf-8")
        evidence = {
            "id": "raw-1",
            "path": str(raw.relative_to(directory)),
            "sha256": hashlib.sha256(raw.read_bytes()).hexdigest(),
        }
        report = {
            "report_type": report_name,
            "binding": binding,
            "evidence": [evidence],
            "checks": [
                {"id": check_id, "result": "pass", "evidence_ids": ["raw-1"]}
                for check_id in sorted(check_ids)
            ],
        }
        (directory / f"{report_name}.json").write_text(
            json.dumps(report, sort_keys=True), encoding="utf-8"
        )


def _write_manifest(root: Path) -> None:
    (root / "SMOKE_PASSED.json").write_text(
        json.dumps(assemble_smoke_manifest(root), sort_keys=True), encoding="utf-8"
    )


def test_smoke_gate_rejects_self_declared_untyped_reports(tmp_path: Path) -> None:
    root = _protocol_root(tmp_path)
    _write_reports(root)
    directory = root / SMOKE_REPORT_DIRECTORY
    raw = directory / "raw/STATIC_GATE_REPORT.json"
    raw.write_text('{"result":"pass"}', encoding="utf-8")
    report_path = directory / "STATIC_GATE_REPORT.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["evidence"][0]["sha256"] = hashlib.sha256(raw.read_bytes()).hexdigest()
    report_path.write_text(json.dumps(report), encoding="utf-8")

    with pytest.raises(ValueError, match="typed evidence"):
        assemble_smoke_manifest(root)


def test_static_gate_freezes_core_and_supplementary_roles(tmp_path: Path) -> None:
    # Given
    root = _protocol_root(tmp_path)
    binding = smoke_binding(root)

    # When
    evidence = build_static_evidence(root, binding["protocol_sha256"])

    # Then
    assert evidence.core_record_ids == CORE_RECORDS
    assert evidence.supplementary_record_count == 8


def test_static_gate_rejects_a_changed_analysis_role(tmp_path: Path) -> None:
    # Given
    root = _protocol_root(tmp_path)
    manifest_path = root / "manifest/source_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["records"][0]["analysis_role"] = "supplementary"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    binding = smoke_binding(root)

    # When / Then
    with pytest.raises(ValueError, match="core record identities"):
        build_static_evidence(root, binding["protocol_sha256"])


def test_smoke_gate_rejects_boolean_only_manifest(tmp_path: Path) -> None:
    root = _protocol_root(tmp_path)
    (root / "SMOKE_PASSED.json").write_text('{"status":"passed"}', encoding="utf-8")

    with pytest.raises(ValueError, match="absent or invalid"):
        verify_smoke_gate(root)


def test_smoke_gate_rejects_raw_evidence_mutation(tmp_path: Path) -> None:
    root = _protocol_root(tmp_path)
    _write_reports(root)
    _write_manifest(root)
    raw = root / SMOKE_REPORT_DIRECTORY / "raw/ISOLATION_REPORT.json"
    raw.write_text(raw.read_text(encoding="utf-8") + "tampered\n", encoding="utf-8")

    with pytest.raises(ValueError, match="raw evidence hash mismatch"):
        verify_smoke_gate(root)


def test_smoke_gate_rejects_observer_artifact_mutation(tmp_path: Path) -> None:
    # Given
    root = _protocol_root(tmp_path)
    _write_reports(root)
    _write_manifest(root)
    artifact = root / SMOKE_REPORT_DIRECTORY / "observer/FUNCTIONAL_REPORT/claude-servo/trace.txt"

    # When
    artifact.write_text("tampered", encoding="utf-8")

    # Then
    with pytest.raises(ValueError, match="artifact tree hash mismatch"):
        verify_smoke_gate(root)


def test_smoke_gate_rejects_report_mutation(tmp_path: Path) -> None:
    root = _protocol_root(tmp_path)
    _write_reports(root)
    _write_manifest(root)
    report_path = root / SMOKE_REPORT_DIRECTORY / "HOOK_NEGATIVE_REPORT.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["checks"][0]["result"] = "fail"
    report_path.write_text(json.dumps(report), encoding="utf-8")

    with pytest.raises(ValueError, match="failed or unsupported"):
        verify_smoke_gate(root)


def test_smoke_gate_rejects_protocol_drift(tmp_path: Path) -> None:
    root = _protocol_root(tmp_path)
    _write_reports(root)
    _write_manifest(root)
    (root / "servo_prompt.md").write_text("drift", encoding="utf-8")

    with pytest.raises(ValueError, match="bindings"):
        verify_smoke_gate(root)


def test_smoke_gate_rejects_missing_required_check(tmp_path: Path) -> None:
    root = _protocol_root(tmp_path)
    _write_reports(root)
    report_path = root / SMOKE_REPORT_DIRECTORY / "FUNCTIONAL_REPORT.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["checks"].pop()
    report_path.write_text(json.dumps(report), encoding="utf-8")

    with pytest.raises(ValueError, match="exact required checks"):
        assemble_smoke_manifest(root)


def test_functional_evidence_requires_exact_three_fresh_cells(tmp_path: Path) -> None:
    root = _protocol_root(tmp_path)
    _write_reports(root)
    directory = root / SMOKE_REPORT_DIRECTORY
    raw = directory / "raw/FUNCTIONAL_REPORT.json"
    evidence = json.loads(raw.read_text(encoding="utf-8"))
    evidence["cells"][1]["trial_root"] = evidence["cells"][0]["trial_root"]
    raw.write_text(json.dumps(evidence), encoding="utf-8")
    report_path = directory / "FUNCTIONAL_REPORT.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["evidence"][0]["sha256"] = hashlib.sha256(raw.read_bytes()).hexdigest()
    report_path.write_text(json.dumps(report), encoding="utf-8")

    with pytest.raises(ValueError, match="fresh trial root"):
        assemble_smoke_manifest(root)
