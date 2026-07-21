from __future__ import annotations

import pytest
from pydantic import ValidationError

from r24_final.assets import baseline_json_schema, servo_json_schema
from r24_final.models import (
    ClosureStatus,
    CommonEnvelope,
    Diagnostic,
    DiagnosticKind,
    EvidenceExcerpt,
    FeedbackPath,
    Recommendation,
    ServoCoding,
    SuccessCheck,
    derive_closure,
)


def test_coding_rejects_quote_without_evidence_reference() -> None:
    # Given
    raw = {
        "record_id": "R01",
        "vendor": "codex",
        "model_id": "snapshot",
        "channels": [{"channel_id": "v1", "quotes": []}],
    }

    # When / Then
    with pytest.raises(ValidationError):
        ServoCoding.model_validate(raw)


def test_closure_is_closed_when_policy_feedback_is_implemented() -> None:
    # Given
    paths = frozenset({FeedbackPath.POLICY_CONTROL})

    # When
    result = derive_closure(paths)

    # Then
    assert result is ClosureStatus.CLOSED


def test_closure_is_partial_for_revision_only() -> None:
    # Given
    paths = frozenset({FeedbackPath.CANDIDATE_REVISION})

    # When
    result = derive_closure(paths)

    # Then
    assert result is ClosureStatus.PARTIAL


def test_recommendation_links_diagnostic_and_observable_success_check() -> None:
    # Given
    quote = EvidenceExcerpt(evidence_id="E01", exact_quote="source text")
    diagnostic = Diagnostic(
        id="D01",
        statement="The operational gate is not identified.",
        kind=DiagnosticKind.MISSING_EVIDENCE,
        evidence_ids=("E01",),
        exact_quotes=(quote,),
        consequence="Search-control reliability cannot be assessed.",
    )
    recommendation = Recommendation(
        id="A01",
        priority_rank=1,
        proposed_action="Document the controlling component and feedback path.",
        linked_diagnostic_ids=("D01",),
        evidence_ids=("E01",),
        exact_quotes=(quote,),
        success_check=SuccessCheck(
            observable="The source identifies the controlling component.",
            comparator_or_threshold="present",
            evidence_needed="A documented feedback path.",
        ),
    )

    # When
    envelope = CommonEnvelope(diagnostics=(diagnostic,), recommendations=(recommendation,))

    # Then
    assert envelope.recommendations[0].linked_diagnostic_ids == ("D01",)


def test_provider_schemas_omit_unsupported_unique_items_keyword() -> None:
    # Given / When
    schemas = (baseline_json_schema(), servo_json_schema())

    # Then
    assert all("uniqueItems" not in str(schema) for schema in schemas)
