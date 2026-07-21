from __future__ import annotations

from enum import StrEnum
from typing import Annotated, ClassVar

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FrozenModel(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid", frozen=True)


class OperationalStatus(StrEnum):
    IMPLEMENTED = "implemented"
    PROPOSED = "proposed_not_exercised"
    EXTERNAL = "external"
    NOT_REPORTED = "not_reported"
    UNCLEAR = "unclear"


class TargetProperty(StrEnum):
    EXECUTABILITY = "executability"
    SPECIFICATION = "specification_compliance"
    PERFORMANCE = "task_performance"
    CORRECTNESS = "correctness_or_formal_validity"
    EMPIRICAL = "empirical_adequacy"
    REPRODUCIBILITY = "reproducibility"
    NOVELTY = "novelty"
    SIGNIFICANCE = "significance"
    AGGREGATE = "aggregate_quality"
    NOT_REPORTED = "not_reported"


class EvidenceSource(StrEnum):
    EXECUTION = "execution_trace"
    BENCHMARK = "benchmark_metric"
    STATISTICAL = "statistical_test"
    PHYSICAL = "physical_measurement"
    REPLICATION = "replication"
    PRIOR_ART = "prior_art_corpus"
    ARTIFACT = "artifact_review"
    HUMAN = "human_judgment"
    NOT_REPORTED = "not_reported"


class EvaluatorSubstrate(StrEnum):
    PROGRAM = "deterministic_program"
    STATISTICAL = "statistical_model"
    FORMAL = "formal_kernel"
    LLM = "llm"
    HUMAN = "human"
    HYBRID = "hybrid"
    NOT_REPORTED = "not_reported"


class DecisionRole(StrEnum):
    DIAGNOSTIC = "diagnostic"
    RANKING = "ranking"
    SEARCH = "search_control"
    STAGE = "stage_transition"
    MEMORY = "memory_admission"
    TERMINAL = "terminal_assessment"
    ACCEPTANCE = "final_acceptance"
    EXTERNAL = "external_assessment"
    NOT_REPORTED = "not_reported"


class FeedbackPath(StrEnum):
    TERMINAL = "terminal_only"
    MEMORY_UPDATE = "memory_update"
    CANDIDATE_REVISION = "candidate_revision"
    POLICY_CONTROL = "policy_control"
    STAGE_TRANSITION = "stage_transition"
    EXTERNAL = "external_only"
    UNCLEAR = "unclear"


class ExternalIndependence(StrEnum):
    SELF = "internal_self_evaluation"
    SEPARATE = "internal_separate_component"
    EXTERNAL_DEPENDENT = "external_nonindependent"
    EXTERNAL_INDEPENDENT = "external_independent"
    NOT_REPORTED = "not_reported"


class ReliabilityEvidence(StrEnum):
    NONE = "none_reported"
    DISCRIMINATION = "discrimination_study"
    AGREEMENT = "agreement_study"
    BIAS = "systematic_error_or_bias_test"
    EXTERNAL = "property_specific_external_validation"
    CALIBRATION = "probabilistic_calibration_analysis"


class ReliabilityFinding(StrEnum):
    NOT_EVALUATED = "not_evaluated"
    NOT_ESTABLISHED = "not_established"
    ERROR = "evidence_of_error_or_bias"
    POSITIVE = "positive_property_specific_evidence"
    MIXED = "mixed"
    UNCLEAR = "unclear"


class Fidelity(StrEnum):
    PROXY = "simulation_or_proxy"
    COMPUTATIONAL = "computational_experiment"
    ORACLE = "computational_oracle_or_benchmark"
    ROBOTIC = "robotic_experiment"
    PHYSICAL = "physical_assay"
    NOT_APPLICABLE = "not_applicable"
    NOT_REPORTED = "not_reported"


class ClosureStatus(StrEnum):
    OPEN = "open"
    PARTIAL = "partial"
    CLOSED = "closed"
    UNCLEAR = "unclear"


class EvidenceQuote(FrozenModel):
    evidence_id: Annotated[str, Field(min_length=1)]
    pdf_id: Annotated[str, Field(min_length=1)]
    page: Annotated[int, Field(ge=1)]
    quote: Annotated[str, Field(min_length=1)]
    rationale: Annotated[str, Field(min_length=1)]


class ValidatorChannel(FrozenModel):
    channel_id: Annotated[str, Field(min_length=1)]
    operational_status: OperationalStatus
    target_property: frozenset[TargetProperty]
    evidence_source: frozenset[EvidenceSource]
    evaluator_substrate: frozenset[EvaluatorSubstrate]
    decision_role: frozenset[DecisionRole]
    feedback_path: frozenset[FeedbackPath]
    external_independence: ExternalIndependence
    reliability_evidence_type: frozenset[ReliabilityEvidence]
    reliability_finding: ReliabilityFinding
    experimental_fidelity: frozenset[Fidelity]
    quotes: Annotated[tuple[EvidenceQuote, ...], Field(min_length=1)]


class HumanAuthority(FrozenModel):
    generator: frozenset[str]
    executor: frozenset[str]
    validator: frozenset[str]
    memory: frozenset[str]
    policy: frozenset[str]


class DiagnosticKind(StrEnum):
    REPORTED_FAILURE = "reported_failure"
    RISK = "risk"
    AMBIGUITY = "ambiguity"
    MISSING_EVIDENCE = "missing_evidence"


class EvidenceExcerpt(FrozenModel):
    evidence_id: Annotated[str, Field(min_length=1)]
    exact_quote: Annotated[str, Field(min_length=1)]


class Diagnostic(FrozenModel):
    id: Annotated[str, Field(min_length=1)]
    statement: Annotated[str, Field(min_length=1)]
    kind: DiagnosticKind
    evidence_ids: Annotated[tuple[str, ...], Field(min_length=1)]
    exact_quotes: Annotated[tuple[EvidenceExcerpt, ...], Field(min_length=1)]
    consequence: Annotated[str, Field(min_length=1)]

    @model_validator(mode="after")
    def align_evidence(self) -> Diagnostic:
        excerpt_ids = {excerpt.evidence_id for excerpt in self.exact_quotes}
        if excerpt_ids != set(self.evidence_ids):
            raise ValueError("diagnostic evidence ids and exact quotes must match")
        return self


class SuccessCheck(FrozenModel):
    observable: Annotated[str, Field(min_length=1)]
    comparator_or_threshold: Annotated[str, Field(min_length=1)]
    evidence_needed: Annotated[str, Field(min_length=1)]


class Recommendation(FrozenModel):
    id: Annotated[str, Field(min_length=1)]
    priority_rank: Annotated[int, Field(ge=1, le=3)]
    proposed_action: Annotated[str, Field(min_length=1)]
    linked_diagnostic_ids: Annotated[tuple[str, ...], Field(min_length=1)]
    evidence_ids: Annotated[tuple[str, ...], Field(min_length=1)]
    exact_quotes: Annotated[tuple[EvidenceExcerpt, ...], Field(min_length=1)]
    success_check: SuccessCheck

    @model_validator(mode="after")
    def align_evidence(self) -> Recommendation:
        excerpt_ids = {excerpt.evidence_id for excerpt in self.exact_quotes}
        if excerpt_ids != set(self.evidence_ids):
            raise ValueError("recommendation evidence ids and exact quotes must match")
        return self


class CommonEnvelope(FrozenModel):
    diagnostics: tuple[Diagnostic, ...]
    recommendations: Annotated[tuple[Recommendation, ...], Field(min_length=1, max_length=3)]

    @model_validator(mode="after")
    def validate_recommendation_links(self) -> CommonEnvelope:
        diagnostic_sequence = tuple(diagnostic.id for diagnostic in self.diagnostics)
        if len(diagnostic_sequence) != len(set(diagnostic_sequence)):
            raise ValueError("diagnostic ids must be unique")
        recommendation_ids = tuple(item.id for item in self.recommendations)
        if len(recommendation_ids) != len(set(recommendation_ids)):
            raise ValueError("recommendation ids must be unique")
        diagnostic_ids = set(diagnostic_sequence)
        for recommendation in self.recommendations:
            if not set(recommendation.linked_diagnostic_ids) <= diagnostic_ids:
                raise ValueError("recommendation references an unknown diagnostic")
        ranks = {recommendation.priority_rank for recommendation in self.recommendations}
        if ranks != set(range(1, len(self.recommendations) + 1)):
            raise ValueError("recommendation priority ranks must be unique and contiguous from one")
        return self


class ServoCoding(FrozenModel):
    record_id: Annotated[str, Field(pattern=r"^R\d{2}$")]
    vendor: Annotated[str, Field(min_length=1)]
    model_id: Annotated[str, Field(min_length=1)]
    channels: Annotated[tuple[ValidatorChannel, ...], Field(min_length=1)]
    policy_type: frozenset[str]
    memory_structure: frozenset[str]
    human_authority: HumanAuthority
    envelope: CommonEnvelope

    @model_validator(mode="after")
    def channel_ids_are_unique(self) -> ServoCoding:
        identifiers = tuple(channel.channel_id for channel in self.channels)
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("validator channel ids must be unique")
        return self


class BaselineCoding(FrozenModel):
    record_id: Annotated[str, Field(pattern=r"^R\d{2}$")]
    vendor: Annotated[str, Field(min_length=1)]
    model_id: Annotated[str, Field(min_length=1)]
    memo: Annotated[str, Field(min_length=1)]
    envelope: CommonEnvelope


def derive_closure(paths: frozenset[FeedbackPath]) -> ClosureStatus:
    if FeedbackPath.UNCLEAR in paths:
        return ClosureStatus.UNCLEAR
    if paths & {FeedbackPath.POLICY_CONTROL, FeedbackPath.STAGE_TRANSITION}:
        return ClosureStatus.CLOSED
    if paths & {FeedbackPath.MEMORY_UPDATE, FeedbackPath.CANDIDATE_REVISION}:
        return ClosureStatus.PARTIAL
    return ClosureStatus.OPEN
