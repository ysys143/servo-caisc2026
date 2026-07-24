from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import pytest

from analysis.servo_v5_verify import (
    PdfIndex,
    dehyphenate,
    fragments_found_in_order,
    normalize_text,
    quote_fragments,
    quote_found_on_page,
    verify_case,
    verify_root,
)

REPOSITORY = Path(__file__).resolve().parents[3]
REAL_ANALYSIS_DIR = REPOSITORY / "analysis"
REAL_C01 = REAL_ANALYSIS_DIR / "servo_v5_source_propositions" / "C01.json"

# The real corpus (a sibling repository, not part of this git tree) is only
# present on machines that have it checked out next to CAISc_2026. Set
# SERVO_V5_CORPUS_ROOT to point at it explicitly (e.g. when running from an
# unzipped supplement, which has no fixed position relative to the corpus);
# without it, this falls back to the CAISc_2026-relative default. Tests that
# need to read the actual PDF skip gracefully when neither resolves to a
# real corpus, per the T2 task's explicit instruction, so CI without the
# private corpus still runs -- but note that a skip is not a pass: a green
# run without SERVO_V5_CORPUS_ROOT (or the default sibling checkout) has not
# verified source fidelity.
CORPUS_ROOT = (
    Path(os.environ["SERVO_V5_CORPUS_ROOT"])
    if os.environ.get("SERVO_V5_CORPUS_ROOT")
    else REPOSITORY.parent.parent / "ai_scientist"
)
BOIKO_PDF = (
    CORPUS_ROOT
    / "1_AI_Scientist_Core"
    / "Core_Systems"
    / "Boiko 2023 - Autonomous Chemical Research with LLMs.pdf"
)
_HAVE_CORPUS = BOIKO_PDF.is_file()
_HAVE_PDFTOTEXT = shutil.which("pdftotext") is not None
requires_corpus = pytest.mark.skipif(
    not (_HAVE_CORPUS and _HAVE_PDFTOTEXT),
    reason="private corpus (../ai_scientist) or pdftotext not available on this machine",
)


def _temp_analysis_root(tmp_path: Path, mutate_first_proposition: dict | None = None) -> Path:
    root = tmp_path / "analysis"
    root.mkdir()
    shutil.copyfile(REAL_ANALYSIS_DIR / "servo_v5_schema.yaml", root / "servo_v5_schema.yaml")
    shutil.copyfile(REAL_ANALYSIS_DIR / "servo2_cases.csv", root / "servo2_cases.csv")
    props_dir = root / "servo_v5_source_propositions"
    props_dir.mkdir()
    payload = json.loads(REAL_C01.read_text(encoding="utf-8"))
    if mutate_first_proposition:
        payload["propositions"][0].update(mutate_first_proposition)
    (props_dir / "C01.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return root


# --- normalization unit tests: no corpus or PDF backend required ----------


def test_normalize_text_unifies_dash_family_and_case():
    variants = ["heater‐shaker", "heater–shaker", "heater—shaker", "heater−shaker"]
    assert len({normalize_text(v) for v in variants}) == 1
    assert normalize_text("HEATER–SHAKER") == "heater-shaker"


def test_normalize_text_collapses_whitespace_runs():
    assert normalize_text("a\n\n  b\t\tc") == "a b c"


def test_normalize_text_strips_spurious_space_inside_brackets():
    # pdftotext/OCR artifact: "( JSON)" for source "(JSON)", "[5.4.0 ]" for "[5.4.0]".
    assert normalize_text("format ( JSON) now") == "format (json) now"
    assert normalize_text("undec[5.4.0 ]ene") == "undec[5.4.0]ene"


def test_normalize_text_strips_pipe_delimited_running_header():
    raw = "reaction). Interestingly, the\n574 | Nature | Vol 624 | 21/28 December 2023\n\nbase DBU is selected"
    assert normalize_text(raw) == "reaction). interestingly, the base dbu is selected"


def test_quote_fragments_splits_on_ellipsis_marker_and_strips_each_side():
    fragments = quote_fragments("Alpha beta [...] gamma delta")
    assert fragments == ["alpha beta", "gamma delta"]


def test_fragments_found_in_order_requires_correct_order():
    # This is a synthetic miniature of the real C01-P08 finding: both
    # fragments are individually present on the page, but the quote's own
    # "[...]" splice implies an order the source does not support.
    page = "b comes first in the source. a comes second in the source."
    fragments = ["a comes second", "b comes first"]
    assert fragments_found_in_order(page, fragments) is False
    assert fragments_found_in_order(page, list(reversed(fragments))) is True


def test_dehyphenate_joins_line_wrap_but_leaves_real_compounds_alone():
    assert dehyphenate("object nota- tion (json)") == "object notation (json)"
    # A genuine compound hyphen has no space after it -- must not be touched.
    assert dehyphenate("a well-known result") == "a well-known result"


def test_quote_found_on_page_uses_dehyphenation_as_fallback_only():
    page = normalize_text("the player wrote its actions in javascript object nota-\ntion format.")
    fragments = quote_fragments("its actions in javascript object notation format.")
    assert quote_found_on_page(page, fragments) is True


# --- sha256 / PDF-resolution gate: tmp_path only, no real PDF needed ------


def test_missing_pdf_is_fail_closed(tmp_path: Path):
    root = _temp_analysis_root(tmp_path)
    empty_corpus = tmp_path / "empty_corpus"
    empty_corpus.mkdir()
    errors, warnings = verify_case(
        root / "servo_v5_source_propositions" / "C01.json",
        PdfIndex(by_hash={}, by_name={}),
        empty_corpus,
    )
    assert [error.code for error in errors] == ["V5_SOURCE_PDF_MISSING"]
    assert warnings == []


def test_right_name_wrong_bytes_is_hash_mismatch_not_missing(tmp_path: Path):
    # A file with the expected filename exists but its content does not
    # hash to source_pdf_sha256 -- this must report tamper/staleness
    # (V5_SOURCE_PDF_HASH_MISMATCH), not be conflated with "nowhere found".
    root = _temp_analysis_root(tmp_path)
    tampered = tmp_path / "Boiko 2023 - Autonomous Chemical Research with LLMs.pdf"
    tampered.write_bytes(b"not the real PDF bytes")
    index = PdfIndex(by_hash={}, by_name={tampered.name: [tampered]})
    errors, warnings = verify_case(root / "servo_v5_source_propositions" / "C01.json", index, tmp_path)
    assert [error.code for error in errors] == ["V5_SOURCE_PDF_HASH_MISMATCH"]
    assert warnings == []


def test_schema_gate_runs_before_pdf_gate(tmp_path: Path):
    # A judgment-leak field must be caught by the schema gate and must not
    # proceed to attempt PDF resolution at all (family dir stays untouched).
    root = _temp_analysis_root(tmp_path, mutate_first_proposition={"support_status": "supported"})
    errors, warnings = verify_case(
        root / "servo_v5_source_propositions" / "C01.json", PdfIndex(by_hash={}, by_name={}), tmp_path
    )
    assert {error.code for error in errors} == {"V5_SOURCE_JUDGMENT_LEAK"}
    assert warnings == []


# --- real corpus: quote-in-PDF gate against the actual pilot PDF ---------


@requires_corpus
def test_real_c01_pilot_verifies_against_the_actual_pdf():
    errors, warnings = verify_root(REAL_ANALYSIS_DIR, CORPUS_ROOT)
    codes = {(error.code, error.record_id) for error in errors}
    # C01-P08 previously spliced two clauses across a "[...]" in an order the
    # source does not support; the verify gate correctly flagged it as
    # V5_QUOTE_NOT_FOUND (confirmed via both the pdftotext text layer and an
    # independent OCR pass). A curator (2026-07-23) fixed the pilot ledger:
    # P08 now quotes only "...the strategy of Coscientist changes among runs
    # (Fig. 5f)" and the mistakes sentence was split out into P14. All 14 C01
    # propositions now verify clean, so this asserts errors == [] (the tighten
    # the original author of this test explicitly anticipated).
    assert codes == set(), [str(error) for error in errors]
    assert all(warning for warning in warnings) or warnings == []


@requires_corpus
def test_corrupted_quote_in_a_temp_copy_is_rejected(tmp_path: Path):
    # Negative demo: mutate a known-good proposition's exact_quote to text
    # that never appeared in the source, in a throwaway copy, and confirm
    # the gate reports V5_QUOTE_NOT_FOUND for exactly that record. The real
    # C01.json is never touched.
    root = tmp_path / "analysis"
    root.mkdir()
    shutil.copyfile(REAL_ANALYSIS_DIR / "servo_v5_schema.yaml", root / "servo_v5_schema.yaml")
    shutil.copyfile(REAL_ANALYSIS_DIR / "servo2_cases.csv", root / "servo2_cases.csv")
    props_dir = root / "servo_v5_source_propositions"
    props_dir.mkdir()
    payload = json.loads(REAL_C01.read_text(encoding="utf-8"))
    for proposition in payload["propositions"]:
        if proposition["proposition_id"] == "C01-P05":
            proposition["exact_quote"] = "This sentence was never printed anywhere in the source PDF."
    (props_dir / "C01.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    errors, _ = verify_root(root, CORPUS_ROOT)
    codes = {(error.code, error.record_id) for error in errors}
    assert ("V5_QUOTE_NOT_FOUND", "C01-P05") in codes, [str(error) for error in errors]
