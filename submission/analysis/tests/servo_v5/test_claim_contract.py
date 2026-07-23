"""T6 -- derive_claim contract, property, and corpus-integration tests.

Unit tests pin one branch each of the deterministic rule (charter B.2/B.3).
Property tests establish the two invariants the charter demands of the whole
function: idempotence (a derived claim is a fixed point) and monotone downgrade
(weakening evidence never strengthens the claim). Integration tests assert the
six shipped claim files re-derive byte-stably and validate clean.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

import pytest

from analysis.servo_v5_claim import (
    BOUNDARY_STRENGTH,
    CASES,
    MODALITY_STRENGTH,
    OCCURRENCE_CLASS_STRENGTH,
    OUTCOMES,
    build_case,
    derive_claim,
    proposition_outcome,
)
from analysis.servo_v5_io import ServoV5Error
from analysis.servo_v5_schema import validate_file

REPOSITORY = Path(__file__).resolve().parents[3]
ANALYSIS_DIR = REPOSITORY / "analysis"


def _relation(
    *,
    alignment_id: str = "C01-A01",
    basis: str = "author_aligned",
    pid: str = "C01-P01",
    occurrence_class: str | None = None,
    structurally_inferred: bool = False,
    polarity: str = "neutral",
    source_role: str = "generation",
    target_role: str = "candidate",
    boundary_status: str = "reported",
) -> dict:
    tag: dict = {
        "proposition_id": pid,
        "structurally_inferred": structurally_inferred,
        "polarity": polarity,
    }
    if occurrence_class is not None:
        tag["occurrence_class"] = occurrence_class
    return {
        "alignment_id": alignment_id,
        "proposition_ids": [pid],
        "assertion_kind": "functional_relation",
        "basis": basis,
        "boundary_status": boundary_status,
        "source_role": source_role,
        "relation_type": "produces",
        "target_role": target_role,
        "temporal_scope": "per_step",
        "proposition_tags": [tag],
    }


def _axes(claim: dict) -> tuple[str, str, str, str]:
    return (
        claim["support_status"],
        claim["claim_scope"],
        claim["alignment_kind"],
        claim["occurrence_resolution"],
    )


# Representative (occurrence_class, structurally_inferred, modality) for each
# outcome state -- the canonical proposition that re-derives that state. Used by
# the idempotence fixed-point test and to keep the 8 branches enumerated.
REPRESENTATIVE = {
    "occurrence_resolved": ("single_event", False, "directly_reported"),
    "aggregate_resolved": ("cross_run_trend", False, "directly_reported"),
    "occurrence_open": ("single_event", True, "directly_reported"),
    "aggregate_supported": ("cross_run_trend", False, "reported_as_procedure"),
    "aggregate_open": ("cross_run_trend", False, "reported_only_as_capability"),
    "procedure_supported": ("architecture", False, "reported_as_procedure"),
    "procedure_open": ("architecture", False, "reported_only_as_capability"),
    "capability_open": ("capability_only", False, "reported_only_as_capability"),
}


# ---------------------------------------------------------------------------
# Unit branches (charter B.2/B.3)
# ---------------------------------------------------------------------------


def test_single_event_non_inferred_is_occurrence_resolved_supported() -> None:
    claim = derive_claim(
        _relation(occurrence_class="single_event"), {"C01-P01": "directly_reported"}
    )
    assert _axes(claim) == ("supported", "occurrence", "author_aligned", "resolved")


def test_structurally_inferred_single_event_is_unresolved() -> None:
    # charter B.3: an inferred occurrence cannot supply a positive witness.
    claim = derive_claim(
        _relation(occurrence_class="single_event", structurally_inferred=True),
        {"C01-P01": "directly_reported"},
    )
    assert claim["support_status"] == "unresolved"
    assert claim["claim_scope"] == "occurrence"
    assert claim["occurrence_resolution"] == "unresolved"


def test_capability_only_forces_occurrence_resolution_unresolved() -> None:
    # charter B.3: capability cannot establish an occurrence -- never resolved,
    # never not_applicable, always unresolved.
    claim = derive_claim(
        _relation(occurrence_class="capability_only"),
        {"C01-P01": "reported_only_as_capability"},
    )
    assert claim["claim_scope"] == "architecture"
    assert claim["support_status"] == "unresolved"
    assert claim["occurrence_resolution"] == "unresolved"


def test_explicit_denial_tag_is_contradicted() -> None:
    claim = derive_claim(
        _relation(occurrence_class="cross_run_trend", polarity="explicit_denial"),
        {"C01-P01": "directly_reported"},
    )
    assert claim["support_status"] == "contradicted"
    assert claim["occurrence_resolution"] == "not_applicable"


def test_cross_run_trend_directly_reported_is_aggregate_resolved() -> None:
    claim = derive_claim(
        _relation(occurrence_class="cross_run_trend"), {"C01-P01": "directly_reported"}
    )
    assert _axes(claim) == ("supported", "aggregate_run", "author_aligned", "resolved")


def test_procedure_class_with_procedure_modality_is_supported_not_applicable() -> None:
    claim = derive_claim(
        _relation(occurrence_class="habitual_procedure"),
        {"C01-P01": "reported_as_procedure"},
    )
    assert _axes(claim) == ("supported", "procedure", "author_aligned", "not_applicable")


def test_procedure_class_without_procedure_evidence_is_unresolved() -> None:
    claim = derive_claim(
        _relation(occurrence_class="architecture"),
        {"C01-P01": "reported_only_as_capability"},
    )
    assert claim["claim_scope"] == "procedure"
    assert claim["support_status"] == "unresolved"
    assert claim["occurrence_resolution"] == "not_applicable"


def test_alignment_kind_tracks_basis() -> None:
    explicit = derive_claim(
        _relation(occurrence_class="single_event", basis="source_explicit"),
        {"C01-P01": "directly_reported"},
    )
    aligned = derive_claim(
        _relation(occurrence_class="single_event", basis="author_aligned"),
        {"C01-P01": "directly_reported"},
    )
    assert explicit["alignment_kind"] == "source_explicit"
    assert aligned["alignment_kind"] == "author_aligned"


def test_observation_relation_boundary_unreported_demotes_occurrence() -> None:
    # charter B.5 (the C01-A15 case): environment produces observation, single_event,
    # boundary_unreported -> occurrence resolved is lowered to unresolved, support kept.
    claim = derive_claim(
        _relation(
            occurrence_class="single_event",
            source_role="environment",
            target_role="observation",
            boundary_status="boundary_unreported",
        ),
        {"C01-P01": "directly_reported"},
    )
    assert claim["claim_scope"] == "occurrence"
    assert claim["support_status"] == "supported"
    assert claim["occurrence_resolution"] == "unresolved"
    assert "charter B.5" in claim["rationale"]


def test_observation_relation_boundary_reported_keeps_resolution() -> None:
    claim = derive_claim(
        _relation(
            occurrence_class="single_event",
            source_role="environment",
            target_role="observation",
            boundary_status="reported",
        ),
        {"C01-P01": "directly_reported"},
    )
    assert claim["occurrence_resolution"] == "resolved"
    assert "charter B.5" not in claim["rationale"]


def test_boundary_unreported_on_non_observation_relation_is_ignored() -> None:
    # The boundary rule only touches observation relations; a generation relation
    # with boundary_unreported still resolves its occurrence.
    claim = derive_claim(
        _relation(
            occurrence_class="single_event",
            source_role="generation",
            target_role="candidate",
            boundary_status="boundary_unreported",
        ),
        {"C01-P01": "directly_reported"},
    )
    assert claim["occurrence_resolution"] == "resolved"


def test_component_mapping_denial_is_not_propagated_to_the_relation() -> None:
    # C02-P42 in the corpus: a positive `generation produces candidate` relation
    # whose consumed proposition ALSO carries a component_mapping denial about a
    # distinct component (memory). The denial must not contradict the relation.
    relation = _relation(occurrence_class="habitual_procedure", basis="source_explicit")
    claim = derive_claim(
        relation,
        {"C01-P01": "directly_reported"},
        denied_proposition_ids=frozenset({"C01-P01"}),
    )
    assert claim["support_status"] == "supported"
    assert "not propagated" in claim["rationale"]


def test_component_mapping_record_is_rejected() -> None:
    record = {
        "alignment_id": "C01-A01",
        "proposition_ids": ["C01-P01"],
        "assertion_kind": "component_mapping",
        "basis": "author_aligned",
        "boundary_status": "reported",
        "source_term": "Coscientist",
        "component": "G",
    }
    with pytest.raises(ServoV5Error):
        derive_claim(record, {"C01-P01": "directly_reported"})


# ---------------------------------------------------------------------------
# Property: every branch is reachable and each outcome triple is distinct
# ---------------------------------------------------------------------------


def test_every_outcome_state_is_reachable_and_distinct() -> None:
    triples = set()
    for label, (oc, si, m) in REPRESENTATIVE.items():
        outcome = proposition_outcome(oc, si, m)
        assert outcome.label == label
        triples.add((outcome.support_status, outcome.claim_scope, outcome.occurrence_resolution))
    assert len(triples) == len(OUTCOMES)


# ---------------------------------------------------------------------------
# Property: idempotence (derive over derive == derive)
# ---------------------------------------------------------------------------


def test_derive_is_deterministic() -> None:
    relation = _relation(occurrence_class="single_event")
    first = derive_claim(relation, {"C01-P01": "directly_reported"})
    second = derive_claim(relation, {"C01-P01": "directly_reported"})
    assert first == second


def test_idempotence_derived_claim_is_a_fixed_point() -> None:
    # Derive a claim, canonicalise it back to the representative proposition of
    # its own (support, scope, occurrence) triple, re-derive: the triple is a
    # fixed point -- derive(canonical(derive(x))) == derive(x).
    triple_to_label = {
        (o.support_status, o.claim_scope, o.occurrence_resolution): label
        for label, o in OUTCOMES.items()
    }
    for _, (oc, si, m) in REPRESENTATIVE.items():
        claim = derive_claim(_relation(occurrence_class=oc, structurally_inferred=si), {"C01-P01": m})
        triple = (claim["support_status"], claim["claim_scope"], claim["occurrence_resolution"])
        oc2, si2, m2 = REPRESENTATIVE[triple_to_label[triple]]
        again = derive_claim(_relation(occurrence_class=oc2, structurally_inferred=si2), {"C01-P01": m2})
        assert (again["support_status"], again["claim_scope"], again["occurrence_resolution"]) == triple


# ---------------------------------------------------------------------------
# Property: monotone downgrade (charter B.3)
# ---------------------------------------------------------------------------


def _claim_rank(claim: dict) -> int:
    triple = (claim["support_status"], claim["claim_scope"], claim["occurrence_resolution"])
    return _STRENGTH_RANK[triple]


# Full-claim strength order = the per-proposition OUTCOMES order with the
# boundary-demoted occurrence state (supported, occurrence, unresolved) inserted
# just below occurrence_resolved and above aggregate_resolved. charter B.5: an
# occurrence whose E<->O_env boundary is unreported is weaker than a witnessed
# occurrence, yet the relation is still supported -- so it must outrank a
# resolved aggregate for the monotonicity order to stay consistent (weakening
# single_event->cross_run_trend under boundary_unreported must not strengthen).
_STRENGTH_BASE = [
    (o.support_status, o.claim_scope, o.occurrence_resolution)
    for o in sorted(OUTCOMES.values(), key=lambda o: o.rank)
]
_STRENGTH_ORDER = _STRENGTH_BASE[:1] + [("supported", "occurrence", "unresolved")] + _STRENGTH_BASE[1:]
_STRENGTH_RANK = {triple: rank for rank, triple in enumerate(_STRENGTH_ORDER)}


def test_per_proposition_outcome_is_exhaustively_monotone() -> None:
    # Over ALL (occurrence_class x structurally_inferred x modality) pairs: if
    # input a is weaker-or-equal to input b on every axis, its outcome is never
    # stronger (rank never lower). This machine-checks the OUTCOMES ordering.
    classes = list(OCCURRENCE_CLASS_STRENGTH)
    modalities = list(MODALITY_STRENGTH)
    combos = [(oc, si, m) for oc in classes for si in (False, True) for m in modalities]

    def weaker_or_equal(a: tuple, b: tuple) -> bool:
        (oc_a, si_a, m_a), (oc_b, si_b, m_b) = a, b
        return (
            OCCURRENCE_CLASS_STRENGTH[oc_a] <= OCCURRENCE_CLASS_STRENGTH[oc_b]
            and MODALITY_STRENGTH[m_a] <= MODALITY_STRENGTH[m_b]
            and si_a >= si_b  # True (inferred, weaker) >= False
        )

    for b in combos:
        for a in combos:
            if weaker_or_equal(a, b):
                assert proposition_outcome(*a).rank >= proposition_outcome(*b).rank, (a, b)


def test_monotonicity_weakening_never_strengthens_the_claim() -> None:
    rng = random.Random(20260723)
    classes = list(OCCURRENCE_CLASS_STRENGTH)
    modalities = list(MODALITY_STRENGTH)
    boundaries = list(BOUNDARY_STRENGTH)

    def weaker_class(oc: str) -> str:
        return rng.choice(
            [c for c in classes if OCCURRENCE_CLASS_STRENGTH[c] <= OCCURRENCE_CLASS_STRENGTH[oc]]
        )

    def weaker_modality(m: str) -> str:
        return rng.choice(
            [x for x in modalities if MODALITY_STRENGTH[x] <= MODALITY_STRENGTH[m]]
        )

    def weaker_boundary(b: str) -> str:
        return rng.choice(
            [x for x in boundaries if BOUNDARY_STRENGTH[x] <= BOUNDARY_STRENGTH[b]]
        )

    def make(props: list[tuple[str, bool, str]], roles: tuple[str, str], boundary: str) -> tuple[dict, dict]:
        source_role, target_role = roles
        pids = [f"C01-P{i + 1:02d}" for i in range(len(props))]
        tags = [
            {
                "proposition_id": pid,
                "occurrence_class": oc,
                "structurally_inferred": si,
                "polarity": "neutral",
            }
            for pid, (oc, si, _) in zip(pids, props)
        ]
        record = {
            "alignment_id": "C01-A01",
            "proposition_ids": pids,
            "assertion_kind": "functional_relation",
            "basis": "author_aligned",
            "boundary_status": boundary,
            "source_role": source_role,
            "relation_type": "produces",
            "target_role": target_role,
            "temporal_scope": "per_step",
            "proposition_tags": tags,
        }
        modality = {pid: m for pid, (_, _, m) in zip(pids, props)}
        return record, modality

    # roles are structural identity, not evidence: held fixed between the strong
    # and weak variant. An observation relation exposes the charter-B.5 boundary
    # rule; a generation relation does not.
    role_choices = [("environment", "observation"), ("observation", "inquiry_state"), ("generation", "candidate")]

    for _ in range(6000):
        roles = rng.choice(role_choices)
        strong_boundary = rng.choice(boundaries)
        strong = [
            (rng.choice(classes), rng.choice([False, True]), rng.choice(modalities))
            for _ in range(rng.randint(1, 3))
        ]
        strong_record, strong_mod = make(strong, roles, strong_boundary)
        strong_claim = derive_claim(strong_record, strong_mod)

        kept = [p for p in strong if rng.random() > 0.3] or [strong[0]]
        weak = [
            (weaker_class(oc), si or rng.choice([False, True]), weaker_modality(m))
            for (oc, si, m) in kept
        ]
        weak_record, weak_mod = make(weak, roles, weaker_boundary(strong_boundary))
        weak_claim = derive_claim(weak_record, weak_mod)

        # Higher rank == weaker. Weakening (weaker tags, dropped propositions, or a
        # weaker boundary) must never lower the rank.
        assert _claim_rank(weak_claim) >= _claim_rank(strong_claim), (strong, weak, roles)


# ---------------------------------------------------------------------------
# Integration: the six shipped claim files
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("case_id", CASES)
def test_shipped_claim_file_validates_clean(case_id: str) -> None:
    errors = validate_file(ANALYSIS_DIR / "servo_v5_claims" / f"{case_id}.json", "derived_claim")
    assert errors == [], [str(error) for error in errors]


@pytest.mark.parametrize("case_id", CASES)
def test_shipped_claim_file_is_a_byte_stable_regeneration(case_id: str) -> None:
    on_disk = json.loads(
        (ANALYSIS_DIR / "servo_v5_claims" / f"{case_id}.json").read_text(encoding="utf-8")
    )
    assert on_disk == build_case(case_id, ANALYSIS_DIR)


@pytest.mark.parametrize("case_id", CASES)
def test_one_claim_per_functional_relation(case_id: str) -> None:
    alignments = json.loads(
        (ANALYSIS_DIR / "servo_v5_alignments" / f"{case_id}.json").read_text(encoding="utf-8")
    )["alignments"]
    relation_ids = [a["alignment_id"] for a in alignments if a["assertion_kind"] == "functional_relation"]
    claims = json.loads(
        (ANALYSIS_DIR / "servo_v5_claims" / f"{case_id}.json").read_text(encoding="utf-8")
    )["claims"]
    # exactly one claim per functional_relation, and no component_mapping claims
    assert len(claims) == len(relation_ids)
    assert [c["used_alignment_ids"][0] for c in claims] == relation_ids
