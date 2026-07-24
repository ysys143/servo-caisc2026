"""M8 provenance-chain contract: fail-closed on any broken link."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from analysis.servo_v5_provenance import ROOT_NAME, verify_root, write_root

SUBMISSION_ROOT = Path(__file__).resolve().parents[3]
ANALYSIS = SUBMISSION_ROOT / "analysis"


def _codes(errors: list[str]) -> set[str]:
    return {e.split(":", 1)[0] for e in errors}


# --- the shipped tree must verify (stale-provenance guard) -----------------


def test_provenance_root_verifies_on_shipped_tree() -> None:
    errors = verify_root(SUBMISSION_ROOT)
    assert errors == [], f"shipped provenance root is stale; re-run --emit. {errors}"


# --- sandbox for mutation tests --------------------------------------------


@pytest.fixture()
def sandbox(tmp_path: Path) -> Path:
    """A minimal, self-consistent copy of the tree with a freshly emitted root."""
    dst = tmp_path / "submission"
    (dst / "release").mkdir(parents=True)
    shutil.copytree(ANALYSIS, dst / "analysis")
    for name in ("main_post-submit.tex", "references.bib", "SUPPLEMENT_README.md",
                 "servo_caiscfp2026_post-submit.pdf"):
        shutil.copyfile(SUBMISSION_ROOT / name, dst / name)
    shutil.copyfile(
        SUBMISSION_ROOT / "release" / "EXTERNAL_PUBLICATION.json",
        dst / "release" / "EXTERNAL_PUBLICATION.json",
    )
    write_root(dst)
    assert verify_root(dst) == []
    return dst


def _append(path: Path, data: bytes = b"\n# tamper\n") -> None:
    path.write_bytes(path.read_bytes() + data)


@pytest.mark.parametrize(
    "relpath, expected",
    [
        ("analysis/servo_v5_claims/C05.json", "V5_PROVENANCE_INTERP_SHA_MISMATCH"),
        ("analysis/servo_v5_alignments/C01.json", "V5_PROVENANCE_INTERP_SHA_MISMATCH"),
        ("analysis/servo_v5_policy/C05.json", "V5_PROVENANCE_INTERP_SHA_MISMATCH"),
        ("analysis/servo_v5_source_propositions/C01.json", "V5_PROVENANCE_SOURCE_SHA_MISMATCH"),
        ("analysis/tbl-servo-v5-relations.tex", "V5_PROVENANCE_EVIDENCE_OUTPUT_MISMATCH"),
        ("main_post-submit.tex", "V5_PROVENANCE_TEX_MISMATCH"),
        ("servo_caiscfp2026_post-submit.pdf", "V5_PROVENANCE_PDF_MISMATCH"),
        ("SUPPLEMENT_README.md", "V5_PROVENANCE_SUPPLEMENT_SHA_MISMATCH"),
    ],
)
def test_mutation_is_caught(sandbox: Path, relpath: str, expected: str) -> None:
    _append(sandbox / relpath)
    assert expected in _codes(verify_root(sandbox))


def test_added_supplement_file_is_caught(sandbox: Path) -> None:
    (sandbox / "analysis" / "unexpected_extra.md").write_text("stray\n", encoding="utf-8")
    assert "V5_PROVENANCE_SUPPLEMENT_ADDED" in _codes(verify_root(sandbox))


def test_removed_supplement_file_is_caught(sandbox: Path) -> None:
    (sandbox / "references.bib").unlink()
    codes = _codes(verify_root(sandbox))
    assert "V5_PROVENANCE_SUPPLEMENT_REMOVED" in codes


def test_missing_root_is_caught(sandbox: Path) -> None:
    (sandbox / "analysis" / ROOT_NAME).unlink()
    assert "V5_PROVENANCE_ROOT_MISSING" in _codes(verify_root(sandbox))


def test_tampered_table_also_breaks_manuscript_edge(sandbox: Path) -> None:
    # A table change must surface both as a stale evidence output and as a
    # broken tables->manuscript edge (the \input hash no longer matches).
    _append(sandbox / "analysis" / "tbl-servo-v5-policy.tex")
    codes = _codes(verify_root(sandbox))
    assert "V5_PROVENANCE_EVIDENCE_OUTPUT_MISMATCH" in codes
    assert "V5_PROVENANCE_MANUSCRIPT_TABLE_MISMATCH" in codes


# --- release gate is fail-closed when the local tree is ahead --------------


def test_release_gate_fails_when_assets_do_not_match(sandbox: Path) -> None:
    # The sandbox EXTERNAL_PUBLICATION points at the published v5.0.4 zip hash,
    # but the sandbox's deterministic rebuild differs -> release gate must fail.
    codes = _codes(verify_root(sandbox, release=True))
    assert "V5_PROVENANCE_RELEASE_ZIP_MISMATCH" in codes


def test_internal_verify_ignores_release_binding(sandbox: Path) -> None:
    # Internal scope must stay green even though the release binding is stale.
    assert verify_root(sandbox, release=False) == []
