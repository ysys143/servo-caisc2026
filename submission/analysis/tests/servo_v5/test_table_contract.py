"""G3 -- evidence-table contract tests for build_servo_v5_tables.py (T11 v3).

Pins the three tables to contract section C: Table A (policy, per case), Table B1
(observation-evaluation boundary, case-level), Table B2 (relation/evidence, per
functional relation). Guards the column set, the derivations, the separate
support/occurrence columns, the two footnotes, and byte-stability of the shipped
.tex artifacts against a fresh regeneration.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from analysis.build_servo_v5_tables import (
    ALIGNMENTS_DIR,
    CASE_IDS,
    CLAIMS_DIR,
    build_boundary_table,
    build_policy_table,
    build_relations_table,
    cross_check,
    evidence_mode,
    load_case_family,
    load_policy,
    observation_evaluation_boundary,
    validate,
)

REPOSITORY = Path(__file__).resolve().parents[3]
ANALYSIS_DIR = REPOSITORY / "analysis"


@pytest.fixture(scope="module")
def data():
    claims = load_case_family(CLAIMS_DIR, "claims")
    alignments = load_case_family(ALIGNMENTS_DIR, "alignments")
    policy = load_policy()
    validate(claims, alignments, policy)
    return claims, alignments, policy


# ---------------------------------------------------------------------------
# Table A -- policy columns and values
# ---------------------------------------------------------------------------


def _header_line(tabular: str) -> str:
    lines = tabular.splitlines()
    top = next(i for i, line in enumerate(lines) if line.startswith(r"\toprule"))
    return lines[top + 1]


def test_policy_has_exactly_the_seven_contract_columns(data) -> None:
    _claims, _alignments, policy = data
    body = build_policy_table(policy)
    header = _header_line(body)
    for column in (
        "Case",
        "Selection signal",
        "Follow-up (control) dependence",
        "Selection-purpose facets",
        "Candidate-selection rule",
        "Design-selection rule",
        "Candidate-execution rule",
    ):
        assert column in header, f"missing Table A column: {column}"
    # header has exactly seven columns (six &-separators): the design-selection
    # rule (reviewer Item 2) is a column separate from candidate-selection rule.
    assert header.count("&") == 6


def test_policy_has_no_explicit_bed_or_generation_scope_column(data) -> None:
    _claims, _alignments, policy = data
    header = _header_line(build_policy_table(policy))
    for forbidden in ("explicit_bed", "explicit\\_bed", "BED", "generation_scope", "generation\\_scope"):
        assert forbidden not in header, f"Table A header must not contain a {forbidden} column"


def test_policy_c05_keeps_objective_separate_from_rules(data) -> None:
    _claims, _alignments, policy = data
    body = build_policy_table(policy)
    c05_row = next(line for line in body.splitlines() if line.startswith("C05 &"))
    # objective facets present
    assert "uncertainty\\_reduction" in c05_row
    assert "hypothesis\\_model\\_discrimination" in c05_row
    # candidate rules are exhaustive / all_selected, NOT a performance objective
    assert "exhaustive" in c05_row
    assert "all\\_selected" in c05_row
    assert "performance\\_improvement" not in c05_row


def test_policy_c05_design_axis_is_standard_and_coverage_not_discrimination(data) -> None:
    # reviewer Item 2: C05's design axis is separate from its candidate axis.
    # The bounded sparkes2010 source reports a model-prescribed assay
    # (fixed_or_standard_design) with a Latin-square layout (coverage_or_factorial)
    # -- NOT a discrimination-directed experiment selection (that is king2004
    # cited background, excluded from the frozen C05 source). "Tested all
    # hypotheses" (all_selected, above) is a candidate fact, not design evidence.
    _claims, _alignments, policy = data
    assert set(policy["C05"]["design_selection_rule"]) == {
        "fixed_or_standard_design",
        "coverage_or_factorial",
    }
    body = build_policy_table(policy)
    c05_row = next(line for line in body.splitlines() if line.startswith("C05 &"))
    assert "fixed\\_or\\_standard\\_design" in c05_row
    assert "coverage\\_or\\_factorial" in c05_row
    assert "discrimination\\_directed" not in c05_row
    # No case in the corpus is coded discrimination/information/cost-directed.
    for case_id in CASE_IDS:
        design = set(policy[case_id]["design_selection_rule"])
        assert design <= {"fixed_or_standard_design", "coverage_or_factorial"}, (
            case_id,
            design,
        )


def test_policy_footnote_i_corpus_level_not_reported(data) -> None:
    _claims, _alignments, policy = data
    body = build_policy_table(policy)
    assert (
        "None of the bounded sources reports an explicit posterior or "
        "expected-information-gain criterion; this is a corpus-level reporting "
        "observation, not evidence of field-wide absence." in body
    )


# ---------------------------------------------------------------------------
# Table B1 -- observation-evaluation boundary (case-level)
# ---------------------------------------------------------------------------


def test_boundary_table_has_four_columns_and_six_cases(data) -> None:
    _claims, alignments, _policy = data
    body, verdicts = build_boundary_table(alignments)
    header = _header_line(body)
    for column in ("Case", "Observation source", "Evaluation target", "O--V boundary"):
        assert column in header
    assert set(verdicts) == set(CASE_IDS)


def test_boundary_verdicts_are_in_domain_and_all_separated(data) -> None:
    _claims, alignments, _policy = data
    _body, verdicts = build_boundary_table(alignments)
    domain = {"separated", "boundary_unreported", "merged", "n.a."}
    assert set(verdicts.values()) <= domain
    # every bounded source reports the O_env<->V split in at least one relation
    assert all(v == "separated" for v in verdicts.values()), verdicts


def test_boundary_derivation_branches() -> None:
    def rel(source, relation, target, boundary):
        return {
            "assertion_kind": "functional_relation",
            "source_role": source,
            "relation_type": relation,
            "target_role": target,
            "boundary_status": boundary,
        }

    # a reported evaluation->observation split => separated
    obs, ev, boundary = observation_evaluation_boundary(
        [rel("environment", "produces", "observation", "boundary_unreported"),
         rel("evaluation", "evaluates", "observation", "reported")]
    )
    assert obs == ["environment"] and "observation" in ev and boundary == "separated"

    # evaluation->observation relations exist but none reports the split
    _obs, _ev, boundary = observation_evaluation_boundary(
        [rel("evaluation", "evaluates", "observation", "boundary_unreported")]
    )
    assert boundary == "boundary_unreported"

    # no evaluation-of-observation relation at all => n.a.
    _obs, _ev, boundary = observation_evaluation_boundary(
        [rel("evaluation", "evaluates", "candidate", "reported")]
    )
    assert boundary == "n.a."


# ---------------------------------------------------------------------------
# Table B2 -- relation / evidence (per functional relation)
# ---------------------------------------------------------------------------


def test_relations_support_and_occurrence_are_separate_columns(data) -> None:
    claims, alignments, _policy = data
    body, _counts = build_relations_table(claims, alignments)
    header = _header_line(body)
    # display header is "Source support" (OD-5); the underlying claim field
    # stays support_status (checked separately below).
    assert "Source support" in header
    assert "Support status" not in header
    assert "Occurrence resolution" in header
    assert "Evidence mode" in header
    # five columns => four &-separators; the two are never merged
    assert header.count("&") == 4


def test_relations_table_is_a_longtable_with_expected_label(data) -> None:
    claims, alignments, _policy = data
    body, _counts = build_relations_table(claims, alignments)
    assert body.startswith(r"\begin{longtable}")
    assert r"\end{longtable}" in body
    assert r"\label{tab:servo-v5-relations}" in body
    assert r"\caption{" in body
    # header + continuation notice repeat on every page
    assert r"\endfirsthead" in body
    assert r"\endhead" in body
    assert r"\endfoot" in body
    assert r"\endlastfoot" in body
    assert body.count(r"\end{tabular}") == 0


def test_relations_support_uses_supported_not_resolved(data) -> None:
    claims, alignments, _policy = data
    body, _counts = build_relations_table(claims, alignments)
    assert r"support status uses \texttt{supported} (not \texttt{resolved})" in body


def test_relations_footnote_ii_mapping_and_non_ordinal(data) -> None:
    claims, alignments, _policy = data
    body, _counts = build_relations_table(claims, alignments)
    for fragment in (
        r"\texttt{architecture} $\to$ structural organization",
        r"\texttt{capability} $\to$ what the system can or is designed to do",
        r"\texttt{procedure} $\to$ specified operational sequence",
        r"\texttt{aggregate} $\to$ repetition or result without event identity",
        r"\texttt{occurrence} $\to$ bounded event-level instance",
    ):
        assert fragment in body, f"missing evidence-mode mapping: {fragment}"
    assert (
        "Evidence modes identify the kind of proposition supported by the source "
        "and are not treated as an ordinal scale of system quality or closure." in body
    )


def test_relations_row_count_matches_distinct_tuples(data) -> None:
    claims, alignments, _policy = data
    _body, counts = build_relations_table(claims, alignments)
    assert counts["rows_total"] == sum(counts["rows_per_case"].values())
    # one row per distinct (case, functional-relation tuple, support, occurrence,
    # evidence-mode) combination, so the three evidence axes on a row correspond.
    assert counts["rows_total"] == 108


def test_evidence_mode_mapping() -> None:
    assert evidence_mode({"claim_scope": "occurrence", "support_status": "supported"}) == "occurrence"
    assert evidence_mode({"claim_scope": "aggregate_run", "support_status": "contradicted"}) == "aggregate"
    assert evidence_mode({"claim_scope": "procedure", "support_status": "supported"}) == "procedure"
    # architecture splits by support_status
    assert evidence_mode({"claim_scope": "architecture", "support_status": "unresolved"}) == "capability"
    assert evidence_mode({"claim_scope": "architecture", "support_status": "supported"}) == "architecture"


# ---------------------------------------------------------------------------
# Cross-checks
# ---------------------------------------------------------------------------


def test_cross_check_corpus_totals(data) -> None:
    claims, alignments, policy = data
    _body, relation_counts = build_relations_table(claims, alignments)
    result = cross_check(claims, relation_counts)
    assert result["claims_total"] == 240
    assert result["claims_occurrence_established_global"] == 35
    # formal epistemic-utility is not_reported for every case (footnote, not a column)
    assert all(
        policy[case_id]["formal_epistemic_utility_evidence"].strip().lower() == "not_reported"
        for case_id in CASE_IDS
    )


# ---------------------------------------------------------------------------
# Byte-stability of the shipped .tex artifacts
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "filename, builder",
    [
        ("tbl-servo-v5-policy.tex", "policy"),
        ("tbl-servo-v5-boundary.tex", "boundary"),
        ("tbl-servo-v5-relations.tex", "relations"),
    ],
)
def test_shipped_table_body_is_a_byte_stable_regeneration(data, filename, builder) -> None:
    claims, alignments, policy = data
    if builder == "policy":
        body = build_policy_table(policy)
    elif builder == "boundary":
        body, _ = build_boundary_table(alignments)
    else:
        body, _ = build_relations_table(claims, alignments)
    on_disk = (ANALYSIS_DIR / filename).read_text(encoding="utf-8")
    assert body in on_disk, f"{filename} is stale; re-run analysis/build_servo_v5_tables.py"
