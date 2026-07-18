from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class StrictModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class WorkStatus(StrEnum):
    PENDING = "pending"
    IDENTITY_CHECKED = "identity_checked"
    READING = "reading"
    CLAIM_CHECK = "claim_check"
    QA = "qa"
    COMPLETE = "complete"
    BLOCKED = "blocked"


class GateState(StrictModel):
    identity: bool = False
    full_text: bool = False
    source_analysis: bool = False
    citations: bool = False
    korean_parity: bool = False
    self_qa: bool = False

    def is_complete(self) -> bool:
        return all(
            (
                self.identity,
                self.full_text,
                self.source_analysis,
                self.citations,
                self.korean_parity,
                self.self_qa,
            )
        )


class FinalGateState(StrictModel):
    joint_citations_reconciled: bool = False
    korean_parity_reconciled: bool = False
    manual_qa_complete: bool = False

    def is_complete(self) -> bool:
        return all(
            (
                self.joint_citations_reconciled,
                self.korean_parity_reconciled,
                self.manual_qa_complete,
            )
        )


class ManuscriptSnapshot(StrictModel):
    path: str
    sha256: str
    citation_commands: int
    citation_links: int
    unique_keys: int


class CitationLink(StrictModel):
    id: str
    command_id: str
    language: str
    line: int
    section: str
    key: str
    command_keys: tuple[str, ...]
    context: str


class SourceRecord(StrictModel):
    index: int
    key: str
    bib_type: str
    pdf_path: str
    pdf_sha256: str
    page_count: int
    version_status: str
    en_link_ids: tuple[str, ...]
    ko_link_ids: tuple[str, ...]


class AuditManifest(StrictModel):
    schema_version: int
    created_at: str
    references_path: str
    references_sha256: str
    manuscripts: tuple[ManuscriptSnapshot, ...]
    source_order: tuple[str, ...]
    links: tuple[CitationLink, ...]
    sources: tuple[SourceRecord, ...]


class SourceState(StrictModel):
    key: str
    status: WorkStatus
    report_path: str
    gates: GateState = GateState()
    started_at: str | None = None
    completed_at: str | None = None
    overall_verdict: str | None = None


class StatusLedger(StrictModel):
    schema_version: int
    manifest_sha256: str
    active_key: str | None
    final_gates: FinalGateState = FinalGateState()
    sources: tuple[SourceState, ...]


class ReportMarkers(StrictModel):
    audit_complete: str
    pages_covered: str
    en_links_covered: str
    ko_links_covered: str
    verdict: str
