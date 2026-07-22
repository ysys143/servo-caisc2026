from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from .servo_v5_io import ServoV5Error, read_json, sha256
from .servo_v5_schema import ValidationError, load_contract, validate_file

# Unicode dash family that must collapse to ASCII "-" before quote/page-text
# comparison: hyphen, non-breaking hyphen, figure dash, en dash, em dash,
# horizontal bar, minus sign. PDF text extractors are inconsistent about
# which of these a given typeset dash comes out as.
_DASH_CHARS = "‐‑‒–—―−"
_DASH_TRANSLATION = str.maketrans({char: "-" for char in _DASH_CHARS})
_WHITESPACE_RUN = re.compile(r"\s+")
_ELLIPSIS_MARKER = "[...]"

# A source line that wraps mid-word leaves a literal "<word>- <continuation>"
# once whitespace is collapsed to a single space (e.g. "nota- tion"). This
# fallback is tried only after a direct match fails, because the same
# "letter-space-letter" shape is indistinguishable from a genuine compound
# hyphen that happens to fall at a line break -- collapsing it unconditionally
# would risk silently rejoining a real hyphenated word pair.
_HYPHEN_LINEBREAK = re.compile(r"(?<=[a-z])- (?=[a-z])")

# pdftotext/OCR occasionally insert a spurious space just inside a bracket
# pair (kerning/word-spacing heuristic, e.g. "( JSON)" for source "(JSON)",
# or OCR's "[5.4.0 ]" for source "[5.4.0]"). Safe to normalize
# unconditionally in both cases: prose never legitimately pads the inside
# of "(...)"/"[...]" with whitespace, and this runs after the "[...]"
# ellipsis marker is matched downstream in quote_fragments, which contains
# no internal whitespace for these substitutions to disturb.
_PAREN_OPEN_SPACE = re.compile(r"([(\[])\s+")
_PAREN_CLOSE_SPACE = re.compile(r"\s+([)\]])")

# Running headers/footers (page number | journal name | volume | date) land
# mid-stream in linear text extraction when a two-column article's footer
# sits between the bottom of one column and the top of the next -- both the
# text layer and OCR reproduce this same interposition (confirmed on C01
# page 5: "...Interestingly, the 574 | Nature | Vol 624 | 21/28 December
# 2023 base DBU..." breaks what is a single contiguous sentence in the
# source). Pipe-delimited running heads are a common convention across
# journals and a "|" essentially never appears in quoted prose, so any
# inline run carrying two or more pipes is safe to strip unconditionally.
_RUNNING_HEADER = re.compile(r"[^\n|]*(?:\|[^\n|]*){2,}")

# Warn-only modality lint (charter B.1 modality is grammatical, not
# judgment -- these are heuristics for a human to double check, not gates).
_CAPABILITY_MARKERS = ("can ", "capable", "ability to", "potential", "proof of concept")
_PROCEDURE_MARKERS = ("the system then", "is then")


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = _RUNNING_HEADER.sub(" ", text)
    text = text.translate(_DASH_TRANSLATION)
    text = _WHITESPACE_RUN.sub(" ", text)
    text = _PAREN_OPEN_SPACE.sub(r"\1", text)
    text = _PAREN_CLOSE_SPACE.sub(r"\1", text)
    return text.strip().lower()


def quote_fragments(exact_quote: str) -> list[str]:
    normalized = normalize_text(exact_quote)
    parts = normalized.split(_ELLIPSIS_MARKER)
    return [fragment for fragment in (part.strip() for part in parts) if fragment]


def dehyphenate(page_text_norm: str) -> str:
    return _HYPHEN_LINEBREAK.sub("", page_text_norm)


def fragments_found_in_order(page_text_norm: str, fragments: list[str]) -> bool:
    cursor = 0
    for fragment in fragments:
        index = page_text_norm.find(fragment, cursor)
        if index == -1:
            return False
        cursor = index + len(fragment)
    return True


def quote_found_on_page(page_text_norm: str, fragments: list[str]) -> bool:
    return fragments_found_in_order(page_text_norm, fragments) or fragments_found_in_order(
        dehyphenate(page_text_norm), fragments
    )


def _select_backend() -> str:
    # pdftotext (poppler) is tried first: a head-to-head comparison against
    # pypdf/pdfplumber/pdfminer on the real C01 pilot PDF (a two-column
    # Nature layout) showed poppler's default reading-order/line-join
    # heuristics leave fewer mid-word line-wrap artifacts than the other
    # three, and it ships with the repo's toolchain already (no new
    # dependency). The Python libraries remain as fallback for environments
    # without poppler installed.
    if shutil.which("pdftotext"):
        return "pdftotext"
    for module_name, backend in (
        ("pypdf", "pypdf"),
        ("pdfplumber", "pdfplumber"),
        ("pdfminer.high_level", "pdfminer"),
    ):
        try:
            __import__(module_name)
        except ImportError:
            continue
        return backend
    raise ServoV5Error(
        "V5_PDF_BACKEND_MISSING",
        "no PDF text extractor available (tried the pdftotext binary, pypdf, "
        "pdfplumber, and pdfminer.six) -- install one rather than skip the quote gate",
    )


@lru_cache(maxsize=None)
def _backend() -> str:
    return _select_backend()


@lru_cache(maxsize=None)
def extract_page_text(pdf_path: Path, page: int) -> str:
    """1-indexed physical page -> raw extracted text (not yet normalized)."""
    backend = _backend()
    if backend == "pypdf":
        from pypdf import PdfReader

        reader = PdfReader(str(pdf_path))
        return reader.pages[page - 1].extract_text() or ""
    if backend == "pdfplumber":
        import pdfplumber

        with pdfplumber.open(pdf_path) as document:
            return document.pages[page - 1].extract_text() or ""
    if backend == "pdfminer":
        from pdfminer.high_level import extract_text

        return extract_text(str(pdf_path), page_numbers=[page - 1])
    # backend == "pdftotext"
    result = subprocess.run(
        ["pdftotext", "-f", str(page), "-l", str(page), str(pdf_path), "-"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise ServoV5Error("V5_PDF_EXTRACTION_FAILED", f"{pdf_path}#{page}: {result.stderr.strip()}")
    return result.stdout


@lru_cache(maxsize=None)
def extract_page_text_ocr(pdf_path: Path, page: int) -> str:
    """OCR fallback (pdftoppm + tesseract), tried only when the PDF's own
    text layer fails to yield a match. Real gotcha found in the pilot: at
    least one source PDF (C01, Boiko 2023) has a corrupted font ToUnicode
    CMap where the glyph for an en dash decodes as ASCII "3" and the glyph
    for a right curly apostrophe decodes as "9" -- confirmed identical
    across four independent text-layer extractors (pdftotext, pypdf,
    pdfplumber, pymupdf), so no choice of text-layer backend can recover
    the correct character. OCR reads the rendered pixels instead of the
    (broken) character codes and is unaffected by this class of corruption.
    Returns "" if tesseract/pdftoppm are unavailable -- this is a fallback,
    not required infrastructure, so its absence must not abort the gate."""
    if not (shutil.which("pdftoppm") and shutil.which("tesseract")):
        return ""
    with tempfile.TemporaryDirectory() as tmp_name:
        prefix = Path(tmp_name) / "page"
        render = subprocess.run(
            ["pdftoppm", "-png", "-r", "300", "-f", str(page), "-l", str(page), str(pdf_path), str(prefix)],
            capture_output=True,
            text=True,
            check=False,
        )
        if render.returncode != 0:
            return ""
        images = sorted(Path(tmp_name).glob("page-*.png"))
        if not images:
            return ""
        ocr = subprocess.run(
            ["tesseract", str(images[0]), "stdout"],
            capture_output=True,
            text=True,
            check=False,
        )
        return ocr.stdout if ocr.returncode == 0 else ""


@dataclass(frozen=True, slots=True)
class PdfIndex:
    by_hash: dict[str, Path]
    by_name: dict[str, list[Path]]


def _pdf_index(source_root: Path) -> PdfIndex:
    """Index every PDF under source_root by both content hash and filename
    (hidden dirs skipped: .git/.claude/etc. hold duplicate worktree copies
    that only slow the scan). Two indices, not one, so a file that exists
    under the expected name but with different bytes (V5_SOURCE_PDF_HASH_
    MISMATCH -- a real tamper/stale-copy signal) is distinguishable from no
    matching file existing anywhere (V5_SOURCE_PDF_MISSING); a hash-only
    index can never observe a mismatch, since a lookup that finds anything
    has, by construction, already found a hash-equal file."""
    if not source_root.is_dir():
        raise ServoV5Error("V5_SOURCE_ROOT_MISSING", str(source_root))
    root = source_root.resolve()
    by_hash: dict[str, Path] = {}
    by_name: dict[str, list[Path]] = {}
    for path in sorted(source_root.rglob("*.pdf")):
        if any(part.startswith(".") for part in path.relative_to(source_root).parts):
            continue
        if path.is_symlink():
            continue
        resolved = path.resolve()
        if not resolved.is_relative_to(root):
            continue
        by_hash[sha256(path)] = path
        by_name.setdefault(path.name, []).append(path)
    return PdfIndex(by_hash=by_hash, by_name=by_name)


def _modality_lint(case_id: str, proposition_id: str, quote: str, modality: str) -> list[str]:
    lowered = quote.lower()
    warnings: list[str] = []
    if modality != "reported_only_as_capability" and any(marker in lowered for marker in _CAPABILITY_MARKERS):
        warnings.append(
            f"V5_MODALITY_LINT_CAPABILITY case={case_id} proposition={proposition_id} "
            f"modality={modality}: quote carries capability/possibility markers"
        )
    if modality != "reported_as_procedure" and any(marker in lowered for marker in _PROCEDURE_MARKERS):
        warnings.append(
            f"V5_MODALITY_LINT_PROCEDURE case={case_id} proposition={proposition_id} "
            f"modality={modality}: quote carries procedure-frame markers"
        )
    return warnings


def verify_case(path: Path, pdf_index: PdfIndex, source_root: Path) -> tuple[list[ValidationError], list[str]]:
    family = "source_proposition"
    case_id = path.stem

    schema_errors = validate_file(path, family)
    if schema_errors:
        # A malformed file cannot be trusted enough to verify against the
        # PDF -- report the schema failure and stop here for this case.
        return schema_errors, []

    payload = read_json(path)
    expected_sha = payload["source_pdf_sha256"]
    pdf_path = pdf_index.by_hash.get(expected_sha)
    if pdf_path is None:
        name_candidates = pdf_index.by_name.get(payload.get("source_pdf_name", ""), [])
        if name_candidates:
            tampered_path = name_candidates[0]
            return [
                ValidationError(
                    "V5_SOURCE_PDF_HASH_MISMATCH",
                    family,
                    case_id,
                    "",
                    f"expected={expected_sha} actual={sha256(tampered_path)} path={tampered_path}",
                )
            ], []
        return [
            ValidationError(
                "V5_SOURCE_PDF_MISSING",
                family,
                case_id,
                "",
                f"no PDF under {source_root} has sha256={expected_sha} "
                f"(source_pdf_name={payload.get('source_pdf_name')!r})",
            )
        ], []

    errors: list[ValidationError] = []
    warnings: list[str] = []
    for proposition in payload["propositions"]:
        proposition_id = proposition["proposition_id"]
        page = proposition["locator"]["pdf_page"]
        quote = proposition["exact_quote"]
        page_text_norm = normalize_text(extract_page_text(pdf_path, page))
        fragments = quote_fragments(quote)
        found = quote_found_on_page(page_text_norm, fragments)
        if not found:
            # Text-layer extraction failed -- fall back to OCR before
            # declaring the quote unfound (see extract_page_text_ocr).
            ocr_text = extract_page_text_ocr(pdf_path, page)
            if ocr_text:
                found = quote_found_on_page(normalize_text(ocr_text), fragments)
        if not found:
            errors.append(
                ValidationError("V5_QUOTE_NOT_FOUND", family, case_id, proposition_id, f"pdf_page={page}")
            )
        warnings.extend(_modality_lint(case_id, proposition_id, quote, proposition.get("modality", "")))
    return errors, warnings


def verify_root(analysis_dir: Path, source_root: Path) -> tuple[list[ValidationError], list[str]]:
    contract = load_contract(analysis_dir)
    props_dir = analysis_dir / contract.directories["source_proposition"]
    if not props_dir.is_dir():
        return [ValidationError("V5_FAMILY_DIR_MISSING", "source_proposition", "", "", str(props_dir))], []

    pdf_index = _pdf_index(source_root)
    errors: list[ValidationError] = []
    warnings: list[str] = []
    for path in sorted(props_dir.glob("*.json")):
        case_errors, case_warnings = verify_case(path, pdf_index, source_root)
        errors.extend(case_errors)
        warnings.extend(case_warnings)
    return errors, warnings


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(prog="servo-v5-verify")
    value.add_argument(
        "--root",
        type=Path,
        required=True,
        help="directory containing analysis/ (i.e. the analysis-parent, e.g. submission/)",
    )
    value.add_argument(
        "--source-root",
        type=Path,
        default=Path("../ai_scientist"),
        help="corpus root to scan for source PDFs by sha256 (default: ../ai_scientist relative to cwd)",
    )
    return value


def run(arguments: list[str]) -> int:
    options = parser().parse_args(arguments)
    analysis_dir = options.root.resolve() / "analysis"
    source_root = options.source_root.resolve()
    try:
        errors, warnings = verify_root(analysis_dir, source_root)
    except ServoV5Error as error:
        print(str(error), file=sys.stderr)
        return 1

    for warning in warnings:
        print(f"WARN {warning}")
    if errors:
        for error in errors:
            print(str(error), file=sys.stderr)
        print(f"SERVO_V5_VERIFY_FAILED: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(f"SERVO_V5_VERIFY_OK: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
