from __future__ import annotations

from pathlib import Path

import pytest

from audit_models import GateState, SourceRecord, SourceState, WorkStatus
from verify_audit import AuditFailure, verify_paper


def source_record() -> SourceRecord:
    return SourceRecord(
        index=1,
        key="example2026",
        bib_type="article",
        pdf_path="/tmp/example.pdf",
        pdf_sha256="a" * 64,
        page_count=3,
        version_status="exact",
        en_link_ids=("EN-C001:example2026",),
        ko_link_ids=("KO-C001:example2026",),
    )


def complete_state(report_path: Path) -> SourceState:
    return SourceState(
        key="example2026",
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


def test_verify_paper_accepts_exact_page_and_link_coverage(tmp_path: Path) -> None:
    # Given
    report_path = tmp_path / "report.md"
    report_path.write_text(
        "\n".join(
            (
                "# Report",
                "AUDIT_COMPLETE: yes",
                "PAGES_COVERED: 1-3",
                "EN_LINKS_COVERED: EN-C001:example2026",
                "KO_LINKS_COVERED: KO-C001:example2026",
                "VERDICT: clean",
            )
        )
    )

    # When
    verify_paper(source_record(), complete_state(report_path), report_path)

    # Then: no exception means every required marker matched the ledger.


def test_verify_paper_rejects_a_missing_korean_link(tmp_path: Path) -> None:
    # Given
    report_path = tmp_path / "report.md"
    report_path.write_text(
        "\n".join(
            (
                "# Report",
                "AUDIT_COMPLETE: yes",
                "PAGES_COVERED: 1-3",
                "EN_LINKS_COVERED: EN-C001:example2026",
                "KO_LINKS_COVERED: none",
                "VERDICT: clean",
            )
        )
    )

    # When / Then
    with pytest.raises(AuditFailure, match="Korean citation-link coverage"):
        verify_paper(source_record(), complete_state(report_path), report_path)


def test_verify_paper_rejects_incomplete_gates(tmp_path: Path) -> None:
    # Given
    report_path = tmp_path / "report.md"
    report_path.write_text(
        "\n".join(
            (
                "# Report",
                "AUDIT_COMPLETE: yes",
                "PAGES_COVERED: 1-3",
                "EN_LINKS_COVERED: EN-C001:example2026",
                "KO_LINKS_COVERED: KO-C001:example2026",
                "VERDICT: clean",
            )
        )
    )
    state = complete_state(report_path).model_copy(
        update={"gates": GateState(identity=True)}
    )

    # When / Then
    with pytest.raises(AuditFailure, match="completion gates"):
        verify_paper(source_record(), state, report_path)
