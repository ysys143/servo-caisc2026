#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pydantic>=2.11",
# ]
# ///

# ─── How to run ───
# 1. Install uv (if not installed):
#      curl -LsSf https://astral.sh/uv/install.sh | sh
# 2. Run directly (no venv, no pip install needed):
#      uv run verify_audit.py baseline|paper KEY|final
# 3. Or make executable and run:
#      chmod +x verify_audit.py && ./verify_audit.py baseline
# ──────────────────

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Final, assert_never

from pydantic import ValidationError

from audit_models import (
    AuditManifest,
    CitationLink,
    ReportMarkers,
    SourceRecord,
    SourceState,
    StatusLedger,
    WorkStatus,
)

AUDIT_DIR: Final = Path(__file__).resolve().parent
REPO_ROOT: Final = AUDIT_DIR.parents[2]
MARKER_PATTERN: Final = re.compile(
    r"^(AUDIT_COMPLETE|PAGES_COVERED|EN_LINKS_COVERED|"
    r"KO_LINKS_COVERED|VERDICT):\s*(.+)$",
    re.MULTILINE,
)
PLACEHOLDER_PATTERN: Final = re.compile(r"\b(?:TODO|TBD)\b", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class AuditFailure(RuntimeError):
    issues: tuple[str, ...]

    def __str__(self) -> str:
        return "; ".join(self.issues)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_markers(text: str) -> ReportMarkers:
    raw = {name.lower(): value.strip() for name, value in MARKER_PATTERN.findall(text)}
    try:
        return ReportMarkers.model_validate(raw)
    except ValidationError as error:
        raise AuditFailure(("required report markers are incomplete",)) from error


def covered_ids(value: str) -> frozenset[str]:
    if value == "none":
        return frozenset()
    return frozenset(item.strip() for item in value.split(",") if item.strip())


def verify_paper(source: SourceRecord, state: SourceState, report_path: Path) -> None:
    issues: list[str] = []
    match state.status:
        case WorkStatus.COMPLETE:
            pass
        case (
            WorkStatus.PENDING
            | WorkStatus.IDENTITY_CHECKED
            | WorkStatus.READING
            | WorkStatus.CLAIM_CHECK
            | WorkStatus.QA
            | WorkStatus.BLOCKED
        ):
            issues.append(f"{source.key}: status is not complete")
        case unreachable:
            assert_never(unreachable)
    if not state.gates.is_complete():
        issues.append(f"{source.key}: completion gates are incomplete")
    if not report_path.is_file():
        issues.append(f"{source.key}: report is missing")
        raise AuditFailure(tuple(issues))

    text = report_path.read_text()
    markers = parse_markers(text)
    if markers.audit_complete != "yes":
        issues.append(f"{source.key}: AUDIT_COMPLETE is not yes")
    if markers.pages_covered != f"1-{source.page_count}":
        issues.append(f"{source.key}: full PDF page coverage is incomplete")
    if covered_ids(markers.en_links_covered) != frozenset(source.en_link_ids):
        issues.append(f"{source.key}: English citation-link coverage differs")
    if covered_ids(markers.ko_links_covered) != frozenset(source.ko_link_ids):
        issues.append(f"{source.key}: Korean citation-link coverage differs")
    if state.overall_verdict != markers.verdict:
        issues.append(f"{source.key}: report and ledger verdicts differ")
    if PLACEHOLDER_PATTERN.search(text):
        issues.append(f"{source.key}: report contains a placeholder")
    if issues:
        raise AuditFailure(tuple(issues))


def verify_baseline(manifest: AuditManifest, ledger: StatusLedger) -> None:
    issues: list[str] = []
    expected_keys = tuple(manifest.source_order)
    source_keys = tuple(source.key for source in manifest.sources)
    state_keys = tuple(state.key for state in ledger.sources)
    if len(expected_keys) != 59 or len(set(expected_keys)) != 59:
        issues.append("manifest must contain exactly 59 unique source keys")
    if source_keys != expected_keys or state_keys != expected_keys:
        issues.append("source and status ordering must match source_order")
    for snapshot in manifest.manuscripts:
        path = REPO_ROOT / snapshot.path
        if sha256_file(path) != snapshot.sha256:
            issues.append(f"manuscript drift: {snapshot.path}")
    references_path = REPO_ROOT / manifest.references_path
    if sha256_file(references_path) != manifest.references_sha256:
        issues.append("bibliography drift")
    link_ids = tuple(link.id for link in manifest.links)
    if len(link_ids) != len(set(link_ids)):
        issues.append("citation-link IDs must be unique")
    verify_link_counts(manifest, issues)
    for source in manifest.sources:
        verify_pdf(source, issues)
    if issues:
        raise AuditFailure(tuple(issues))


def verify_link_counts(manifest: AuditManifest, issues: list[str]) -> None:
    for snapshot in manifest.manuscripts:
        language = "EN" if snapshot.path.endswith("main.tex") else "KO"
        links = tuple(link for link in manifest.links if link.language == language)
        if len(links) != snapshot.citation_links:
            issues.append(f"{language}: citation-link count differs")
        if len({link.key for link in links}) != snapshot.unique_keys:
            issues.append(f"{language}: unique-key count differs")


def verify_pdf(source: SourceRecord, issues: list[str]) -> None:
    path = Path(source.pdf_path)
    if not path.is_file():
        issues.append(f"{source.key}: PDF is missing")
        return
    if sha256_file(path) != source.pdf_sha256:
        issues.append(f"{source.key}: PDF drift")
    result = subprocess.run(
        ("pdfinfo", str(path)), check=True, capture_output=True, text=True
    )
    page_line = next(line for line in result.stdout.splitlines() if line.startswith("Pages:"))
    if int(page_line.split(":", 1)[1].strip()) != source.page_count:
        issues.append(f"{source.key}: PDF page count differs")


def source_by_key(manifest: AuditManifest, key: str) -> SourceRecord:
    matches = tuple(source for source in manifest.sources if source.key == key)
    if len(matches) != 1:
        raise AuditFailure((f"unknown or duplicate source key: {key}",))
    return matches[0]


def state_by_key(ledger: StatusLedger, key: str) -> SourceState:
    matches = tuple(state for state in ledger.sources if state.key == key)
    if len(matches) != 1:
        raise AuditFailure((f"unknown or duplicate status key: {key}",))
    return matches[0]


def load_artifacts() -> tuple[AuditManifest, StatusLedger]:
    manifest = AuditManifest.model_validate_json((AUDIT_DIR / "manifest.json").read_text())
    ledger = StatusLedger.model_validate_json((AUDIT_DIR / "status.json").read_text())
    expected_hash = sha256_file(AUDIT_DIR / "manifest.json")
    if ledger.manifest_sha256 != expected_hash:
        raise AuditFailure(("status ledger points to a different manifest",))
    return manifest, ledger


def verify_final(manifest: AuditManifest, ledger: StatusLedger) -> None:
    issues: list[str] = []
    if ledger.active_key is not None:
        issues.append("an active source remains")
    if not ledger.final_gates.is_complete():
        issues.append("final reconciliation gates are incomplete")
    for source, state in zip(manifest.sources, ledger.sources, strict=True):
        try:
            verify_paper(source, state, REPO_ROOT / state.report_path)
        except AuditFailure as error:
            issues.extend(error.issues)
    if issues:
        raise AuditFailure(tuple(issues))


def main() -> int:
    try:
        manifest, ledger = load_artifacts()
        match sys.argv[1:]:
            case ["baseline"]:
                verify_baseline(manifest, ledger)
                print("BASELINE PASS: 59 sources and frozen artifacts verified")
            case ["paper", key]:
                source = source_by_key(manifest, key)
                state = state_by_key(ledger, key)
                verify_paper(source, state, REPO_ROOT / state.report_path)
                print(f"PAPER PASS: {key}")
            case ["final"]:
                verify_baseline(manifest, ledger)
                verify_final(manifest, ledger)
                print("FINAL PASS: 59 reports and all citation links verified")
            case _:
                print("usage: verify_audit.py baseline|paper KEY|final", file=sys.stderr)
                return 2
    except (AuditFailure, ValidationError, OSError, subprocess.CalledProcessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
