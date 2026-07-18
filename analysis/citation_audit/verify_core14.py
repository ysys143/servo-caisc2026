#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pydantic>=2.11",
# ]
# ///

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Final

from pydantic import ValidationError

from audit_models import (
    AuditManifest,
    CoreManifest,
    CoreSourceRecord,
    CoreSourceState,
    CoreStatusLedger,
)
from verify_audit import AuditFailure, sha256_file, verify_paper, verify_pdf

AUDIT_DIR: Final = Path(__file__).resolve().parent
REPO_ROOT: Final = AUDIT_DIR.parents[2]
DESCRIPTION_MARKER: Final = re.compile(
    r"^SYSTEM_DESCRIPTION_ASSESSED:\s*(\S+)\s*$", re.MULTILINE
)
REQUIRED_HEADINGS: Final = (
    "Source Identity",
    "Full-Text Coverage",
    "Problem and Context",
    "Structure and Argument",
    "Methods and Evidence",
    "Findings",
    "Limitations",
    "Citation Assessments",
    "Korean Parity",
    "Overall Verdict",
    "Completion Checklist",
)


def verify_core_report(
    source: CoreSourceRecord,
    state: CoreSourceState,
    report_path: Path,
) -> None:
    verify_paper(source, state, report_path)  # type: ignore[arg-type]
    text = report_path.read_text()
    missing_headings = tuple(
        heading
        for heading in REQUIRED_HEADINGS
        if len(re.findall(rf"^## {re.escape(heading)}$", text, re.MULTILINE)) != 1
    )
    if missing_headings:
        raise AuditFailure(
            tuple(f"missing required heading: {heading}" for heading in missing_headings)
        )
    values = DESCRIPTION_MARKER.findall(text)
    if values != ["yes"]:
        raise AuditFailure(
            (f"{source.system_id}: supplementary description is not assessed",)
        )


def expected_links_by_key() -> dict[str, tuple[str, ...]]:
    manifest = AuditManifest.model_validate_json((AUDIT_DIR / "manifest.json").read_text())
    return {
        source.key: tuple((*source.en_link_ids, *source.ko_link_ids))
        for source in manifest.sources
    }


def verify_core_baseline(
    manifest: CoreManifest,
    ledger: CoreStatusLedger,
) -> None:
    issues: list[str] = []
    sources = manifest.sources
    system_ids = tuple(source.system_id for source in sources)
    state_ids = tuple(state.system_id for state in ledger.sources)
    if manifest.scope != "tier1_core14" or ledger.scope != manifest.scope:
        issues.append("scope must be tier1_core14")
    if len(sources) != 14 or len(set(system_ids)) != 14:
        issues.append("manifest must contain exactly 14 unique systems")
    if tuple(source.index for source in sources) != tuple(range(1, 15)):
        issues.append("core source indices must be contiguous from 1 to 14")
    if state_ids != system_ids:
        issues.append("status ordering must match core source ordering")
    if len({source.report_path for source in sources}) != len(sources):
        issues.append("core report paths must be unique")

    frozen_paths = (
        (manifest.scope_source, manifest.scope_source_sha256),
        (manifest.description_source, manifest.description_source_sha256),
    )
    for relative_path, expected_hash in frozen_paths:
        path = REPO_ROOT / relative_path
        if not path.is_file() or sha256_file(path) != expected_hash:
            issues.append(f"frozen source drift: {relative_path}")

    expected_links = expected_links_by_key()
    all_links: list[str] = []
    for source, state in zip(sources, ledger.sources, strict=True):
        if state.report_path != source.report_path:
            issues.append(f"{source.system_id}: report path differs in ledger")
        known_links = expected_links.get(source.citation_key or "", ())
        if tuple(source.manuscript_link_ids) != known_links:
            issues.append(f"{source.system_id}: manuscript-link inventory differs")
        all_links.extend(source.manuscript_link_ids)
        verify_pdf(source, issues)  # type: ignore[arg-type]
    if len(all_links) != len(set(all_links)):
        issues.append("core manuscript-link IDs must be unique")
    if issues:
        raise AuditFailure(tuple(issues))


def source_by_id(manifest: CoreManifest, system_id: str) -> CoreSourceRecord:
    matches = tuple(source for source in manifest.sources if source.system_id == system_id)
    if len(matches) != 1:
        raise AuditFailure((f"unknown or duplicate system ID: {system_id}",))
    return matches[0]


def state_by_id(ledger: CoreStatusLedger, system_id: str) -> CoreSourceState:
    matches = tuple(state for state in ledger.sources if state.system_id == system_id)
    if len(matches) != 1:
        raise AuditFailure((f"unknown or duplicate status ID: {system_id}",))
    return matches[0]


def load_artifacts() -> tuple[CoreManifest, CoreStatusLedger]:
    manifest_path = AUDIT_DIR / "core14-manifest.json"
    manifest = CoreManifest.model_validate_json(manifest_path.read_text())
    ledger = CoreStatusLedger.model_validate_json(
        (AUDIT_DIR / "core14-status.json").read_text()
    )
    if ledger.manifest_sha256 != sha256_file(manifest_path):
        raise AuditFailure(("core status ledger points to a different manifest",))
    return manifest, ledger


def verify_core_final(manifest: CoreManifest, ledger: CoreStatusLedger) -> None:
    issues: list[str] = []
    if ledger.active_system_id is not None:
        issues.append("an active core system remains")
    if not ledger.final_gates.is_complete():
        issues.append("core final reconciliation gates are incomplete")
    for source, state in zip(manifest.sources, ledger.sources, strict=True):
        try:
            verify_core_report(source, state, REPO_ROOT / state.report_path)
        except AuditFailure as error:
            issues.extend(error.issues)
    if issues:
        raise AuditFailure(tuple(issues))


def main() -> int:
    try:
        manifest, ledger = load_artifacts()
        arguments = sys.argv[1:]
        if arguments == ["baseline"]:
            verify_core_baseline(manifest, ledger)
            print("CORE14 BASELINE PASS: 14 systems and frozen artifacts verified")
        elif len(arguments) == 2 and arguments[0] == "paper":
            system_id = arguments[1]
            source = source_by_id(manifest, system_id)
            state = state_by_id(ledger, system_id)
            verify_core_report(source, state, REPO_ROOT / state.report_path)
            print(f"CORE14 PAPER PASS: {system_id}")
        elif arguments == ["final"]:
            verify_core_baseline(manifest, ledger)
            verify_core_final(manifest, ledger)
            print("CORE14 FINAL PASS: 14 reports and frozen claims verified")
        else:
            print("usage: verify_core14.py baseline|paper SYSTEM_ID|final", file=sys.stderr)
            return 2
    except (AuditFailure, ValidationError, OSError, subprocess.CalledProcessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
