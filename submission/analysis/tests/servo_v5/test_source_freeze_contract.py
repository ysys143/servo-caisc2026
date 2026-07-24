from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import pytest

from analysis.servo_v5_freeze import (
    T5_CONSUMABLE_FIELDS,
    build_manifest,
    project_source_proposition,
    validate_context_note,
    validate_manifest,
    validate_readiness,
    validate_warning_dispositions,
)
from analysis.servo_v5_verify import verify_root

REPOSITORY = Path(__file__).resolve().parents[3]
REAL_ANALYSIS_DIR = REPOSITORY / "analysis"
# See test_verify_contract.py for why this is overridable: SERVO_V5_CORPUS_ROOT
# lets an unzipped supplement point at the corpus explicitly; without it, a
# skip here is not a pass -- source fidelity was not checked.
CORPUS_ROOT = (
    Path(os.environ["SERVO_V5_CORPUS_ROOT"])
    if os.environ.get("SERVO_V5_CORPUS_ROOT")
    else REPOSITORY.parent.parent / "ai_scientist"
)
SOURCE_DIRNAME = "servo_v5_source_propositions"

requires_corpus = pytest.mark.skipif(
    not CORPUS_ROOT.is_dir() or shutil.which("pdftotext") is None,
    reason="source corpus or pdftotext unavailable",
)


def _copy_freeze_inputs(tmp_path: Path) -> Path:
    target = tmp_path / "analysis"
    target.mkdir()
    for name in (
        "servo_v5_charter.md",
        "servo_v5_schema.yaml",
        "servo_v5_source_proposition_schema.md",
        "servo_v5_warning_dispositions.json",
    ):
        shutil.copyfile(REAL_ANALYSIS_DIR / name, target / name)
    shutil.copytree(REAL_ANALYSIS_DIR / SOURCE_DIRNAME, target / SOURCE_DIRNAME)
    return target


def test_alignment_projection_excludes_noncanonical_context() -> None:
    proposition = {
        "proposition_id": "C01-P01",
        "locator": {"pdf_page": 1},
        "exact_quote": "A directly reported source sentence.",
        "modality": "directly_reported",
        "named_actors": ["agent"],
        "named_inputs": ["input"],
        "named_outputs": ["output"],
        "source_context_note": "This note must never be a T5 input.",
    }

    projected = project_source_proposition(proposition)

    assert set(projected) == set(T5_CONSUMABLE_FIELDS)
    assert "source_context_note" not in projected


def test_source_context_note_rejects_servo_semantic_alignment() -> None:
    issues = validate_context_note(
        "C01",
        "C01-P01",
        "This is a memory-update relation used by the policy.",
    )

    assert {issue.code for issue in issues} == {"V5_SOURCE_SEMANTIC_LEAK"}


def test_warning_disposition_gate_rejects_an_unreviewed_warning(tmp_path: Path) -> None:
    analysis_dir = _copy_freeze_inputs(tmp_path)
    warnings = [
        "V5_MODALITY_LINT_CAPABILITY case=C99 proposition=C99-P01 "
        "modality=directly_reported: quote carries capability/possibility markers"
    ]

    issues = validate_warning_dispositions(analysis_dir, warnings)

    # The single injected C99 warning is unreviewed -> V5_WARNING_DISPOSITION_MISSING.
    # The real dispositions copied by _copy_freeze_inputs are all status=active but
    # absent from this one-item warning list, so V5_WARNING_DISPOSITION_STALE co-occurs
    # for them. This test asserts only that an unreviewed warning is rejected.
    assert "V5_WARNING_DISPOSITION_MISSING" in {issue.code for issue in issues}


def test_freeze_manifest_detects_changed_source_ledger(tmp_path: Path) -> None:
    analysis_dir = _copy_freeze_inputs(tmp_path)
    manifest = build_manifest(analysis_dir, [])
    path = analysis_dir / "servo_v5_source_freeze_manifest.json"
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    c01 = analysis_dir / SOURCE_DIRNAME / "C01.json"
    payload = json.loads(c01.read_text(encoding="utf-8"))
    payload["coverage_note"] += " changed after freeze"
    c01.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    issues = validate_manifest(analysis_dir, [])

    assert {issue.code for issue in issues} == {"V5_SOURCE_FREEZE_STALE"}


def test_freeze_manifest_binds_six_frozen_cases() -> None:
    manifest = build_manifest(REAL_ANALYSIS_DIR, [])

    assert set(manifest["cases"]) == {"C01", "C02", "C03", "C04", "C05", "C06"}
    assert all(case["status"] == "frozen" for case in manifest["cases"].values())
    assert all(case["proposition_count"] > 0 for case in manifest["cases"].values())


@requires_corpus
def test_current_source_layer_passes_the_t5_readiness_gate() -> None:
    pdf_errors, warnings = verify_root(REAL_ANALYSIS_DIR, CORPUS_ROOT)
    assert pdf_errors == []

    issues = validate_readiness(REAL_ANALYSIS_DIR, warnings)

    assert issues == [], [str(issue) for issue in issues]
