"""T6 -- deterministic DerivedDecisionClaim synthesis (charter B.2/B.3).

`derive_claim` is a pure function: a single functional_relation author-alignment
record (plus the source modality of each proposition it consumes) maps to exactly
one DerivedDecisionClaim over the four frozen axes (charter B.2):

    support_status         supported | unresolved | contradicted | not_applicable
    claim_scope            occurrence | aggregate_run | procedure | architecture
    alignment_kind         source_explicit | author_aligned
    occurrence_resolution  resolved | unresolved | not_applicable

It never reads the retired v4 closure matrix; it restarts from the source
proposition modality and the per-proposition occurrence_class tag (charter B.3:
"reanalysis restarts from the source proposition, not the existing matrix").
component_mapping records do NOT yield claims -- only functional_relation
records do.

Design notes where this implementation pins down the T6 task instructions
(the corpus is 100% single-proposition relations, so these refinements do not
change any shipped claim; they only make the function total and provably
monotone):

  * Multi-proposition "strongest present" (task) is realised as the strongest
    of the per-proposition OUTCOMES under a fixed total order (OUTCOME_STATES).
    For a single consumed proposition -- every relation in the corpus -- this
    reduces to exactly the task's occurrence_class -> claim_scope table, so the
    corpus output is identical either way. Expressing it as a max-over-
    propositions makes derive_claim monotone by construction (charter B.3
    "monotone downgrade"): weakening or dropping evidence can only lower the
    max, never raise it.

  * aggregate_run resolution additionally requires structurally_inferred==false
    (charter B.3: an inferred connection cannot supply a positive witness).
    Every cross_run_trend tag in the corpus has structurally_inferred==false,
    so this never changes a shipped claim; it removes a monotonicity hole for
    synthetic inputs.

  * A consumed proposition's component_mapping-level explicit_denial does NOT by
    itself contradict a functional_relation claim. Per rubric v5-rubric-4 / §2,
    a relation's own denial is carried on its proposition_tags[].polarity; a
    component_mapping polarity=explicit_denial hosts the denial of a proposition
    whose absence statement yields NO functional_relation. C02-P42 is the
    witness: it yields both a positive `generation produces candidate` relation
    (C02-A90) AND a separate component_mapping denial (C02-A88, "the archive"=M
    is not used). The denial is about memory, not about generation; propagating
    it onto A90 would manufacture a false `contradicted`. derive_claim therefore
    reads denial only from the relation's own tags. Consumed cm-denials are
    surfaced in the rationale for audit, never as a verdict. See the T6 report.

  * E<->O_env boundary (charter B.5). For a relation that produces or consumes an
    observation (source_role or target_role == observation, e.g. `O_env produces
    observation`, `observation updates inquiry_state`, `V evaluates observation`),
    boundary_status == boundary_unreported means the source never reported the
    executor/environment boundary, so an observation occurrence cannot be
    confirmed (the charter forbids appointing E as the observation producer by
    fiat). When such a relation would otherwise resolve at occurrence scope,
    occurrence_resolution is lowered resolved -> unresolved while support_status
    is retained at the relation-existence level. This is the point where v5
    diverges from v4.1, which assumed an observation occurrence via a
    producer_event_id. boundary_status == reported leaves the claim unchanged.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .servo_v5_io import ServoV5Error, read_json

ANALYSIS_DIR = Path(__file__).resolve().parent
CASES = ("C01", "C02", "C03", "C04", "C05", "C06")

SCHEMA = "servo_v5_derived_claim"
SCHEMA_DOC = "analysis/servo_v5_source_proposition_schema.md"
STATUS = "draft"


@dataclass(frozen=True, slots=True)
class Outcome:
    """The (support, scope, occurrence) an evidence class licenses at one
    proposition. `rank` orders outcomes strongest (0) to weakest; a claim over
    several propositions takes the strongest (lowest-rank) outcome present."""

    label: str
    support_status: str
    claim_scope: str
    occurrence_resolution: str
    rank: int


# Strongest first. The order is a total order chosen so that every weakening of
# a proposition's evidence (weaker occurrence_class, weaker modality, or
# structurally_inferred flipped true) maps to an outcome of equal-or-higher rank
# (equal-or-weaker claim). test_claim_contract exhaustively verifies that
# invariant over all (occurrence_class x structurally_inferred x modality)
# pairs, so the ordering here is machine-checked, not asserted.
_OUTCOME_TABLE = (
    ("occurrence_resolved", "supported", "occurrence", "resolved"),
    ("aggregate_resolved", "supported", "aggregate_run", "resolved"),
    ("occurrence_open", "unresolved", "occurrence", "unresolved"),
    ("aggregate_supported", "supported", "aggregate_run", "unresolved"),
    ("aggregate_open", "unresolved", "aggregate_run", "unresolved"),
    ("procedure_supported", "supported", "procedure", "not_applicable"),
    ("procedure_open", "unresolved", "procedure", "not_applicable"),
    ("capability_open", "unresolved", "architecture", "unresolved"),
)
OUTCOMES: dict[str, Outcome] = {
    label: Outcome(label, support, scope, occ, rank)
    for rank, (label, support, scope, occ) in enumerate(_OUTCOME_TABLE)
}

# Input-side weakening ranks (independent of the outcome function). Higher =
# stronger evidence. Used only by the monotonicity test to define "weaker
# input"; derive_claim itself does not consult them.
OCCURRENCE_CLASS_STRENGTH = {
    "single_event": 4,
    "cross_run_trend": 3,
    "architecture": 2,
    "habitual_procedure": 2,
    "capability_only": 1,
}
MODALITY_STRENGTH = {
    "directly_reported": 3,
    "reported_as_procedure": 2,
    "reported_only_as_capability": 1,
}
# charter B.5: a reported E<->O_env boundary is stronger evidence than an
# unreported one (weaker boundary -> weaker occurrence). Used by the
# monotonicity test; derive_claim reads boundary_status directly.
BOUNDARY_STRENGTH = {
    "reported": 2,
    "boundary_unreported": 1,
}


def proposition_outcome(
    occurrence_class: str | None, structurally_inferred: bool, modality: str | None
) -> Outcome:
    """The outcome a single consumed proposition licenses.

    claim_scope follows the occurrence_class -> scope table (charter B.2, rubric
    §3); when occurrence_class is absent it falls back to the source modality.
    A resolved occurrence needs a real witness: a single_event that is NOT
    structurally_inferred (charter B.3). capability_only can never establish an
    occurrence, so it lands at architecture scope with occurrence_resolution
    forced to unresolved (never resolved, never not_applicable)."""

    si = bool(structurally_inferred)
    oc = occurrence_class
    m = modality

    if oc == "single_event" or (oc is None and m == "directly_reported"):
        scope = "occurrence"
    elif oc == "cross_run_trend":
        scope = "aggregate_run"
    elif oc == "capability_only" or (oc is None and m == "reported_only_as_capability"):
        scope = "architecture"
    elif oc in ("architecture", "habitual_procedure") or (
        oc is None and m == "reported_as_procedure"
    ):
        scope = "procedure"
    else:
        # No occurrence_class and no modality signal: cannot license anything
        # beyond an unresolved architecture-scope statement.
        scope = "architecture"

    if scope == "occurrence":
        witness = (oc == "single_event") and not si
        return OUTCOMES["occurrence_resolved"] if witness else OUTCOMES["occurrence_open"]
    if scope == "aggregate_run":
        trend_resolved = oc == "cross_run_trend" and m == "directly_reported" and not si
        if trend_resolved:
            return OUTCOMES["aggregate_resolved"]
        if m in ("directly_reported", "reported_as_procedure"):
            return OUTCOMES["aggregate_supported"]
        return OUTCOMES["aggregate_open"]
    if scope == "procedure":
        if m in ("directly_reported", "reported_as_procedure"):
            return OUTCOMES["procedure_supported"]
        return OUTCOMES["procedure_open"]
    # scope == "architecture": capability-only semantics.
    return OUTCOMES["capability_open"]


def strongest_outcome(outcomes: list[Outcome]) -> Outcome:
    return min(outcomes, key=lambda outcome: outcome.rank)


def is_observation_relation(functional_relation: dict) -> bool:
    """Whether the typed relation produces or consumes an observation (charter
    B.5): the E<->O_env boundary rule applies only to these."""

    return "observation" in (
        functional_relation.get("source_role"),
        functional_relation.get("target_role"),
    )


def _tag_index(functional_relation: dict) -> dict[str, dict]:
    return {
        tag["proposition_id"]: tag
        for tag in functional_relation.get("proposition_tags", [])
        if isinstance(tag, dict) and "proposition_id" in tag
    }


def derive_claim(
    functional_relation: dict,
    source_modality_by_pid: dict[str, str],
    denied_proposition_ids: frozenset[str] = frozenset(),
) -> dict:
    """Deterministically map one functional_relation record to one claim body.

    Returns the eight claim fields except claim_id (assigned by the caller in
    file order). Pure: identical inputs -> identical output, no reference to any
    prior claim or the retired closure matrix.
    """

    if functional_relation.get("assertion_kind") != "functional_relation":
        raise ServoV5Error(
            "V5_CLAIM_NOT_A_RELATION",
            f"{functional_relation.get('alignment_id')} is not a functional_relation",
        )

    proposition_ids = list(functional_relation["proposition_ids"])
    tags = _tag_index(functional_relation)
    alignment_kind = (
        "source_explicit"
        if functional_relation.get("basis") == "source_explicit"
        else "author_aligned"
    )

    outcomes: list[Outcome] = []
    drivers: list[tuple[str, str | None, bool, str | None]] = []
    for pid in proposition_ids:
        tag = tags.get(pid, {})
        occurrence_class = tag.get("occurrence_class")
        structurally_inferred = bool(tag.get("structurally_inferred", False))
        modality = source_modality_by_pid.get(pid)
        outcomes.append(
            proposition_outcome(occurrence_class, structurally_inferred, modality)
        )
        drivers.append((pid, occurrence_class, structurally_inferred, modality))

    best = strongest_outcome(outcomes)

    # Denial is read ONLY from the relation's own proposition_tags (see module
    # docstring). A consumed component_mapping denial is noted for audit but is
    # never a verdict.
    denial_pids = [
        pid for pid in proposition_ids if tags.get(pid, {}).get("polarity") == "explicit_denial"
    ]
    consumed_cm_denials = [pid for pid in proposition_ids if pid in denied_proposition_ids]

    if denial_pids:
        support_status = "contradicted"
        occurrence_resolution = "not_applicable"
        rationale = (
            f"explicit_denial on proposition_tag(s) {','.join(denial_pids)} "
            f"-> support_status=contradicted; claim_scope={best.claim_scope} retained "
            f"from occurrence_class; occurrence_resolution=not_applicable "
            f"(positive-occurrence question mooted by denial)."
        )
    else:
        support_status = best.support_status
        occurrence_resolution = best.occurrence_resolution
        rationale = _rationale(best, drivers)
        # charter B.5: unreported E<->O_env boundary cannot confirm an
        # observation occurrence. Lower resolved -> unresolved at occurrence
        # scope; keep support_status (relation exists, occurrence undetermined).
        if (
            is_observation_relation(functional_relation)
            and functional_relation.get("boundary_status") == "boundary_unreported"
            and best.claim_scope == "occurrence"
            and occurrence_resolution == "resolved"
        ):
            occurrence_resolution = "unresolved"
            rationale += (
                " charter B.5: this relation crosses an unreported E<->O_env boundary "
                "(boundary_status=boundary_unreported), so the observation occurrence cannot be "
                "confirmed; occurrence_resolution lowered resolved->unresolved with support_status "
                "retained at the relation-existence level (occurrence undetermined)."
            )
        if consumed_cm_denials:
            rationale += (
                f" [audit: consumed proposition(s) {','.join(consumed_cm_denials)} also carry a "
                f"component_mapping-level explicit_denial about a distinct component; per "
                f"rubric v5-rubric-4 §2 that denial is not propagated to this typed relation.]"
            )

    return {
        "support_status": support_status,
        "claim_scope": best.claim_scope,
        "alignment_kind": alignment_kind,
        "occurrence_resolution": occurrence_resolution,
        "used_alignment_ids": [functional_relation["alignment_id"]],
        "used_proposition_ids": proposition_ids,
        "rationale": rationale,
    }


def _rationale(best: Outcome, drivers: list[tuple[str, str | None, bool, str | None]]) -> str:
    driver = _driving(best, drivers)
    pid, occurrence_class, structurally_inferred, modality = driver
    oc = occurrence_class if occurrence_class is not None else f"(none; modality={modality})"
    head = f"driver={pid} occurrence_class={oc} modality={modality}"
    if best.label == "occurrence_resolved":
        return (
            f"{head}: single_event with structurally_inferred=false is a real occurrence "
            f"witness (charter B.3) -> claim_scope=occurrence, support_status=supported, "
            f"occurrence_resolution=resolved."
        )
    if best.label == "occurrence_open":
        reason = (
            "single_event but structurally_inferred=true (inferred occurrence cannot witness, "
            "charter B.3)"
            if occurrence_class == "single_event"
            else "occurrence-scope proposition without a single_event witness"
        )
        return (
            f"{head}: {reason} -> claim_scope=occurrence, support_status=unresolved, "
            f"occurrence_resolution=unresolved."
        )
    if best.label == "aggregate_resolved":
        return (
            f"{head}: cross_run_trend reported directly (directly_reported, "
            f"structurally_inferred=false) -> claim_scope=aggregate_run, support_status=supported, "
            f"occurrence_resolution=resolved."
        )
    if best.label == "aggregate_supported":
        return (
            f"{head}: cross_run_trend without a directly_reported trend witness "
            f"-> claim_scope=aggregate_run, support_status=supported (procedure/aggregate "
            f"evidence), occurrence_resolution=unresolved."
        )
    if best.label == "aggregate_open":
        return (
            f"{head}: cross_run_trend with no directly_reported/reported_as_procedure evidence "
            f"-> claim_scope=aggregate_run, support_status=unresolved, "
            f"occurrence_resolution=unresolved."
        )
    if best.label == "procedure_supported":
        return (
            f"{head}: {oc} (non-occurrence) with directly_reported/reported_as_procedure evidence "
            f"-> claim_scope=procedure, support_status=supported, "
            f"occurrence_resolution=not_applicable."
        )
    if best.label == "procedure_open":
        return (
            f"{head}: {oc} (non-occurrence) with no directly_reported/reported_as_procedure "
            f"evidence -> claim_scope=procedure, support_status=unresolved, "
            f"occurrence_resolution=not_applicable."
        )
    # capability_open
    return (
        f"{head}: capability_only (reported_only_as_capability) cannot establish an occurrence "
        f"(charter B.3) -> claim_scope=architecture, support_status=unresolved, "
        f"occurrence_resolution=unresolved."
    )


def _driving(
    best: Outcome, drivers: list[tuple[str, str | None, bool, str | None]]
) -> tuple[str, str | None, bool, str | None]:
    for driver in drivers:
        _, occurrence_class, structurally_inferred, modality = driver
        if proposition_outcome(occurrence_class, structurally_inferred, modality).label == best.label:
            return driver
    return drivers[0]


# ---------------------------------------------------------------------------
# Case-level synthesis: read an alignment file + its source ledger, emit the
# derived_claim envelope. One claim per functional_relation, in file order.
# ---------------------------------------------------------------------------


def _modality_by_pid(source_payload: dict) -> dict[str, str]:
    return {
        proposition["proposition_id"]: proposition["modality"]
        for proposition in source_payload.get("propositions", [])
        if isinstance(proposition, dict) and "proposition_id" in proposition
    }


def _denied_proposition_ids(alignment_payload: dict) -> frozenset[str]:
    return frozenset(
        pid
        for record in alignment_payload.get("alignments", [])
        if record.get("assertion_kind") == "component_mapping"
        and record.get("polarity") == "explicit_denial"
        for pid in record.get("proposition_ids", [])
    )


def build_case(case_id: str, analysis_dir: Path = ANALYSIS_DIR) -> dict:
    alignment_payload = read_json(analysis_dir / "servo_v5_alignments" / f"{case_id}.json")
    source_payload = read_json(analysis_dir / "servo_v5_source_propositions" / f"{case_id}.json")
    modality_by_pid = _modality_by_pid(source_payload)
    denied = _denied_proposition_ids(alignment_payload)

    claims: list[dict] = []
    for record in alignment_payload.get("alignments", []):
        if record.get("assertion_kind") != "functional_relation":
            continue
        body = derive_claim(record, modality_by_pid, denied_proposition_ids=denied)
        claim = {"claim_id": f"{case_id}-D{len(claims) + 1:02d}", **body}
        claims.append(claim)

    return {
        "schema": SCHEMA,
        "schema_doc": SCHEMA_DOC,
        "status": STATUS,
        "case_id": case_id,
        "claims": claims,
    }


def write_case(case_id: str, analysis_dir: Path = ANALYSIS_DIR) -> Path:
    payload = build_case(case_id, analysis_dir)
    out_dir = analysis_dir / "servo_v5_claims"
    out_dir.mkdir(exist_ok=True)
    path = out_dir / f"{case_id}.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def main() -> None:
    for case_id in CASES:
        path = write_case(case_id)
        payload = json.loads(path.read_text(encoding="utf-8"))
        print(f"{case_id}: {len(payload['claims'])} claims -> {path}")


if __name__ == "__main__":
    main()
