from __future__ import annotations

import json

import pytest

from r24_final.evidence import (
    EvidenceError,
    EvidenceItem,
    EvidencePacket,
    validate_envelope,
    validate_quotes,
)
from r24_final.models import (
    CommonEnvelope,
    Diagnostic,
    DiagnosticKind,
    EvidenceExcerpt,
    EvidenceQuote,
    Recommendation,
    SuccessCheck,
)


def test_quote_must_match_frozen_packet_exactly() -> None:
    # Given
    packet = EvidencePacket(
        record_id="R01",
        pdf_id="a" * 64,
        items=(EvidenceItem(evidence_id="E01", page=4, text="exact source passage"),),
    )
    quote = EvidenceQuote(
        evidence_id="E01",
        pdf_id="a" * 64,
        page=4,
        quote="invented passage",
        rationale="supports the channel",
    )

    # When / Then
    with pytest.raises(EvidenceError):
        validate_quotes(packet, (quote,))


def test_envelope_rejects_nonexact_diagnostic_quote() -> None:
    # Given
    packet = EvidencePacket(
        record_id="R01",
        pdf_id="a" * 64,
        items=(EvidenceItem(evidence_id="E01", page=4, text="exact source passage"),),
    )
    excerpt = EvidenceExcerpt(evidence_id="E01", exact_quote="invented passage")
    diagnostic = Diagnostic(
        id="D01",
        statement="A source-grounded issue.",
        kind=DiagnosticKind.RISK,
        evidence_ids=("E01",),
        exact_quotes=(excerpt,),
        consequence="The decision may be unreliable.",
    )
    recommendation = Recommendation(
        id="A01",
        priority_rank=1,
        proposed_action="Evaluate evaluator error on held-out outcomes.",
        linked_diagnostic_ids=("D01",),
        evidence_ids=("E01",),
        exact_quotes=(excerpt,),
        success_check=SuccessCheck(
            observable="Evaluator error is reported.",
            comparator_or_threshold="below a preregistered threshold",
            evidence_needed="Held-out outcomes.",
        ),
    )
    envelope = CommonEnvelope(diagnostics=(diagnostic,), recommendations=(recommendation,))

    # When / Then
    with pytest.raises(EvidenceError):
        validate_envelope(packet, envelope)


def test_packet_model_accepts_the_frozen_on_disk_shape() -> None:
    raw = {
        "schema_version": 1,
        "record_id": "R01",
        "source": {"pdf_sha256": "a" * 64, "page_count": 9},
        "instructions": "Use only these excerpts.",
        "evidence": [
            {"evidence_id": "R01-E01", "pdf_page": 4, "quote": "exact source passage"}
        ],
    }

    packet = EvidencePacket.model_validate_json(json.dumps(raw))

    assert packet.record_id == "R01"
    assert packet.pdf_id == "a" * 64
    assert packet.items[0].page == 4
    assert packet.items[0].text == "exact source passage"


@pytest.mark.parametrize(
    ("pdf_id", "page", "quote", "error"),
    [
        ("R01", 4, "exact source passage", "source identity"),
        ("a" * 64, 5, "exact source passage", "page mismatch"),
        ("a" * 64, 4, "fabricated passage", "frozen packet quotation"),
    ],
)
def test_channel_quote_rejects_each_provenance_failure_independently(
    pdf_id: str, page: int, quote: str, error: str
) -> None:
    packet = EvidencePacket(
        record_id="R01",
        pdf_id="a" * 64,
        items=(EvidenceItem(evidence_id="R01-E01", page=4, text="exact source passage"),),
    )
    candidate = EvidenceQuote(
        evidence_id="R01-E01",
        pdf_id=pdf_id,
        page=page,
        quote=quote,
        rationale="supports the coding",
    )

    with pytest.raises(EvidenceError, match=error):
        validate_quotes(packet, (candidate,))


def test_channel_quote_rejects_unknown_evidence_id() -> None:
    packet = EvidencePacket(
        record_id="R01",
        pdf_id="a" * 64,
        items=(EvidenceItem(evidence_id="R01-E01", page=4, text="exact source passage"),),
    )
    candidate = EvidenceQuote(
        evidence_id="R01-E99",
        pdf_id="a" * 64,
        page=4,
        quote="exact source passage",
        rationale="supports the coding",
    )

    with pytest.raises(EvidenceError, match="unknown evidence id"):
        validate_quotes(packet, (candidate,))
