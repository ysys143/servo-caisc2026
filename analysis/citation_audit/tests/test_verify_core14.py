from __future__ import annotations

from pathlib import Path

import pytest

from audit_models import CoreSourceRecord, CoreSourceState, GateState, WorkStatus
from verify_audit import AuditFailure
from verify_core14 import verify_core_report


def core_source() -> CoreSourceRecord:
    return CoreSourceRecord(
        index=1,
        system_id="example_system",
        name="Example System",
        citation_key="example2026",
        pdf_path="/tmp/example.pdf",
        pdf_sha256="a" * 64,
        page_count=3,
        version_status="exact",
        manuscript_link_ids=(
            "EN-C001:example2026",
            "KO-C001:example2026",
        ),
        supplementary_description="A frozen system claim.",
        report_path="report.md",
    )


def complete_state(report_path: Path) -> CoreSourceState:
    return CoreSourceState(
        system_id="example_system",
        status=WorkStatus.COMPLETE,
        report_path=str(report_path),
        gates=GateState(
            identity=True,
            full_text=True,
            source_analysis=True,
            citations=True,
            korean_parity=True,
            self_qa=True,
        ),
        overall_verdict="clean",
    )


def report_text(*, description_assessed: str = "yes") -> str:
    headings = (
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
    return "\n".join(
        (
            "# Report",
            *(f"## {heading}" for heading in headings),
            "AUDIT_COMPLETE: yes",
            "PAGES_COVERED: 1-3",
            "EN_LINKS_COVERED: EN-C001:example2026",
            "KO_LINKS_COVERED: KO-C001:example2026",
            f"SYSTEM_DESCRIPTION_ASSESSED: {description_assessed}",
            "VERDICT: clean",
        )
    )


def test_verify_core_report_accepts_description_and_exact_link_coverage(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "report.md"
    report_path.write_text(report_text())

    verify_core_report(core_source(), complete_state(report_path), report_path)


def test_verify_core_report_rejects_missing_description_assessment(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "report.md"
    report_path.write_text(report_text().replace("SYSTEM_DESCRIPTION_ASSESSED: yes\n", ""))

    with pytest.raises(AuditFailure, match="supplementary description"):
        verify_core_report(core_source(), complete_state(report_path), report_path)


def test_verify_core_report_rejects_negative_description_assessment(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "report.md"
    report_path.write_text(report_text(description_assessed="no"))

    with pytest.raises(AuditFailure, match="supplementary description"):
        verify_core_report(core_source(), complete_state(report_path), report_path)


def test_verify_core_report_rejects_a_missing_required_heading(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "report.md"
    report_path.write_text(report_text().replace("## Limitations\n", ""))

    with pytest.raises(AuditFailure, match="missing required heading: Limitations"):
        verify_core_report(core_source(), complete_state(report_path), report_path)
