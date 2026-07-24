from __future__ import annotations

import json
import shutil
from pathlib import Path

from analysis.servo_v5_schema import validate_file, validate_root

REPOSITORY = Path(__file__).resolve().parents[3]
REAL_ANALYSIS_DIR = REPOSITORY / "analysis"
REAL_C01 = REAL_ANALYSIS_DIR / "servo_v5_source_propositions" / "C01.json"


def _temp_analysis_root(
    tmp_path: Path,
    mutate_first_proposition: dict | None = None,
    alignment_records: list[dict] | None = None,
) -> Path:
    root = tmp_path / "analysis"
    root.mkdir()
    shutil.copyfile(REAL_ANALYSIS_DIR / "servo_v5_schema.yaml", root / "servo_v5_schema.yaml")
    shutil.copyfile(REAL_ANALYSIS_DIR / "servo2_cases.csv", root / "servo2_cases.csv")
    props_dir = root / "servo_v5_source_propositions"
    props_dir.mkdir()
    payload = json.loads(REAL_C01.read_text(encoding="utf-8"))
    if mutate_first_proposition:
        payload["propositions"][0].update(mutate_first_proposition)
    (props_dir / "C01.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if alignment_records is not None:
        align_dir = root / "servo_v5_alignments"
        align_dir.mkdir()
        (align_dir / "C01.json").write_text(
            json.dumps(_alignment_payload(*alignment_records), indent=2), encoding="utf-8"
        )
    return root


# ---------------------------------------------------------------------------
# author_alignment fixtures (charter B.7). No real alignment data exists yet
# (T5); these are synthetic records exercising the assertion_kind grammar.
# ---------------------------------------------------------------------------


def _alignment_payload(*records: dict) -> dict:
    return {
        "schema": "servo_v5_author_alignment",
        "schema_doc": "analysis/servo_v5_source_proposition_schema.md",
        "status": "draft",
        "case_id": "C01",
        "alignments": list(records),
    }


def _valid_component_mapping_alignment() -> dict:
    return {
        "alignment_id": "C01-A01",
        "proposition_ids": ["C01-P01"],
        "assertion_kind": "component_mapping",
        "basis": "source_explicit",
        "boundary_status": "reported",
        "source_term": "Docs searcher module",
        "component": "G",
    }


def _valid_functional_relation_alignment() -> dict:
    return {
        "alignment_id": "C01-A02",
        "proposition_ids": ["C01-P01"],
        "assertion_kind": "functional_relation",
        "basis": "source_explicit",
        "boundary_status": "reported",
        "source_role": "observation",
        "relation_type": "updates",
        "target_role": "inquiry_state",
        "temporal_scope": "cross_step",
    }


def _write_alignment_file(tmp_path: Path, *records: dict) -> Path:
    root = tmp_path / "analysis"
    root.mkdir()
    shutil.copyfile(REAL_ANALYSIS_DIR / "servo_v5_schema.yaml", root / "servo_v5_schema.yaml")
    align_dir = root / "servo_v5_alignments"
    align_dir.mkdir()
    path = align_dir / "C01.json"
    path.write_text(json.dumps(_alignment_payload(*records), indent=2), encoding="utf-8")
    return path


def test_real_c01_pilot_validates_with_zero_errors() -> None:
    errors = validate_file(REAL_C01, "source_proposition")
    assert errors == [], f"pilot ledger must validate clean: {[str(e) for e in errors]}"


def test_forbidden_field_yields_source_judgment_leak(tmp_path: Path) -> None:
    root = _temp_analysis_root(tmp_path, mutate_first_proposition={"support_status": "supported"})
    errors = validate_file(root / "servo_v5_source_propositions" / "C01.json", "source_proposition")
    codes = {error.code for error in errors}
    assert codes == {"V5_SOURCE_JUDGMENT_LEAK"}, [str(error) for error in errors]


def test_upward_reference_to_alignment_is_rejected(tmp_path: Path) -> None:
    root = _temp_analysis_root(tmp_path, mutate_first_proposition={"alignment_id": "C01-A01"})
    errors = validate_file(root / "servo_v5_source_propositions" / "C01.json", "source_proposition")
    assert errors, "a proposition carrying an alignment_id must be rejected"
    assert {error.code for error in errors} == {"V5_SOURCE_JUDGMENT_LEAK"}, [str(error) for error in errors]


def test_validate_root_is_fail_closed_on_missing_downstream_families(tmp_path: Path) -> None:
    # Build a minimal analysis root with only servo_v5_source_propositions
    # populated (no author_alignment/derived_claim/policy dirs). validate_root
    # must report all three downstream families as missing rather than
    # silently skipping them. Isolated in tmp_path so this doesn't depend on
    # which families happen to be populated in the real repository.
    root = _temp_analysis_root(tmp_path)
    errors = validate_root(root)
    codes = {error.code for error in errors}
    assert "V5_FAMILY_DIR_MISSING" in codes
    missing_families = {error.family for error in errors if error.code == "V5_FAMILY_DIR_MISSING"}
    assert missing_families == {"author_alignment", "derived_claim", "policy"}


# ---------------------------------------------------------------------------
# author_alignment assertion_kind grammar (charter B.7)
# ---------------------------------------------------------------------------


def test_valid_component_mapping_alignment_validates_clean(tmp_path: Path) -> None:
    path = _write_alignment_file(tmp_path, _valid_component_mapping_alignment())
    errors = validate_file(path, "author_alignment")
    assert errors == [], [str(error) for error in errors]


def test_valid_functional_relation_alignment_validates_clean(tmp_path: Path) -> None:
    path = _write_alignment_file(tmp_path, _valid_functional_relation_alignment())
    errors = validate_file(path, "author_alignment")
    assert errors == [], [str(error) for error in errors]


def test_functional_relation_carrying_component_is_rejected(tmp_path: Path) -> None:
    record = _valid_functional_relation_alignment()
    record["component"] = "G"
    path = _write_alignment_file(tmp_path, record)
    errors = validate_file(path, "author_alignment")
    codes = {error.code for error in errors}
    assert codes == {"V5_ALIGNMENT_KIND_FIELD_MISMATCH"}, [str(error) for error in errors]


def test_component_mapping_missing_component_is_rejected(tmp_path: Path) -> None:
    record = _valid_component_mapping_alignment()
    del record["component"]
    path = _write_alignment_file(tmp_path, record)
    errors = validate_file(path, "author_alignment")
    codes = {error.code for error in errors}
    assert codes == {"V5_ALIGNMENT_MISSING_FIELD"}, [str(error) for error in errors]


def test_alignment_reference_to_unknown_proposition_is_rejected(tmp_path: Path) -> None:
    record = _valid_component_mapping_alignment()
    record["proposition_ids"] = ["C01-P99"]
    root = _temp_analysis_root(tmp_path, alignment_records=[record])
    errors = validate_root(root)
    codes = {error.code for error in errors}
    assert "V5_REFERENCE_UNKNOWN" in codes, [str(error) for error in errors]


# ---------------------------------------------------------------------------
# proposition_tags (rubric section 3, charter B.8): T6 derive_claim inputs,
# optional and restricted to functional_relation records.
# ---------------------------------------------------------------------------


def test_functional_relation_with_valid_proposition_tags_validates_clean(tmp_path: Path) -> None:
    record = _valid_functional_relation_alignment()
    record["proposition_tags"] = [
        {
            "proposition_id": "C01-P01",
            "occurrence_class": "single_event",
            "structurally_inferred": False,
            "polarity": "neutral",
        }
    ]
    path = _write_alignment_file(tmp_path, record)
    errors = validate_file(path, "author_alignment")
    assert errors == [], [str(error) for error in errors]


def test_functional_relation_with_omitted_occurrence_class_validates_clean(tmp_path: Path) -> None:
    # occurrence_class is optional (rubric v5-rubric-3 §3): a tag entry
    # without it is still valid.
    record = _valid_functional_relation_alignment()
    record["proposition_tags"] = [
        {"proposition_id": "C01-P01", "structurally_inferred": False, "polarity": "neutral"}
    ]
    path = _write_alignment_file(tmp_path, record)
    errors = validate_file(path, "author_alignment")
    assert errors == [], [str(error) for error in errors]


def test_proposition_tags_on_component_mapping_is_rejected(tmp_path: Path) -> None:
    record = _valid_component_mapping_alignment()
    record["proposition_tags"] = [{"proposition_id": "C01-P01"}]
    path = _write_alignment_file(tmp_path, record)
    errors = validate_file(path, "author_alignment")
    codes = {error.code for error in errors}
    assert codes == {"V5_ALIGNMENT_KIND_FIELD_MISMATCH"}, [str(error) for error in errors]


def test_proposition_tag_with_unknown_proposition_id_is_rejected(tmp_path: Path) -> None:
    record = _valid_functional_relation_alignment()
    record["proposition_tags"] = [{"proposition_id": "C01-P99"}]
    path = _write_alignment_file(tmp_path, record)
    errors = validate_file(path, "author_alignment")
    codes = {error.code for error in errors}
    assert codes == {"V5_ALIGNMENT_TAG_UNKNOWN_PROPOSITION"}, [str(error) for error in errors]


def test_proposition_tag_with_bad_polarity_is_rejected(tmp_path: Path) -> None:
    record = _valid_functional_relation_alignment()
    record["proposition_tags"] = [{"proposition_id": "C01-P01", "polarity": "strongly_opposed"}]
    path = _write_alignment_file(tmp_path, record)
    errors = validate_file(path, "author_alignment")
    codes = {error.code for error in errors}
    assert codes == {"V5_ENUM_INVALID"}, [str(error) for error in errors]


def test_proposition_tag_with_bad_occurrence_class_is_rejected(tmp_path: Path) -> None:
    record = _valid_functional_relation_alignment()
    record["proposition_tags"] = [{"proposition_id": "C01-P01", "occurrence_class": "one_off"}]
    path = _write_alignment_file(tmp_path, record)
    errors = validate_file(path, "author_alignment")
    codes = {error.code for error in errors}
    assert codes == {"V5_ENUM_INVALID"}, [str(error) for error in errors]


def test_proposition_tag_with_unlisted_key_is_rejected(tmp_path: Path) -> None:
    record = _valid_functional_relation_alignment()
    record["proposition_tags"] = [{"proposition_id": "C01-P01", "confidence": "high"}]
    path = _write_alignment_file(tmp_path, record)
    errors = validate_file(path, "author_alignment")
    codes = {error.code for error in errors}
    assert codes == {"V5_ALIGNMENT_TAG_FIELD_UNKNOWN"}, [str(error) for error in errors]


def test_proposition_tag_with_removed_bool_key_is_rejected(tmp_path: Path) -> None:
    # describes_single_event/describes_cross_run_trend were subsumed by
    # occurrence_class (rubric v5-rubric-3 §3) and are no longer allowed keys.
    record = _valid_functional_relation_alignment()
    record["proposition_tags"] = [{"proposition_id": "C01-P01", "describes_single_event": True}]
    path = _write_alignment_file(tmp_path, record)
    errors = validate_file(path, "author_alignment")
    codes = {error.code for error in errors}
    assert codes == {"V5_ALIGNMENT_TAG_FIELD_UNKNOWN"}, [str(error) for error in errors]


# ---------------------------------------------------------------------------
# v5-rubric-4 schema-structure gaps (six-case full-run verdict): generation
# ROLE, capability_only occurrence_class, polarity on component_mapping,
# 3-digit alignment_id.
# ---------------------------------------------------------------------------


def _valid_generation_relation_alignment() -> dict:
    # GAP 2: generator edges now carry source_role=generation instead of the
    # inquiry_state / candidate->candidate self-loop proxies.
    return {
        "alignment_id": "C01-A03",
        "proposition_ids": ["C01-P01"],
        "assertion_kind": "functional_relation",
        "basis": "source_explicit",
        "boundary_status": "reported",
        "source_role": "generation",
        "relation_type": "produces",
        "target_role": "candidate",
        "temporal_scope": "per_step",
    }


def test_generation_source_role_validates_clean(tmp_path: Path) -> None:
    path = _write_alignment_file(tmp_path, _valid_generation_relation_alignment())
    errors = validate_file(path, "author_alignment")
    assert errors == [], [str(error) for error in errors]


def test_generation_target_role_validates_clean(tmp_path: Path) -> None:
    record = _valid_generation_relation_alignment()
    record["source_role"] = "candidate"
    record["relation_type"] = "revises"
    record["target_role"] = "generation"
    path = _write_alignment_file(tmp_path, record)
    errors = validate_file(path, "author_alignment")
    assert errors == [], [str(error) for error in errors]


def test_capability_only_occurrence_class_validates_clean(tmp_path: Path) -> None:
    # GAP 1: reported_only_as_capability modality now maps to
    # occurrence_class=capability_only.
    record = _valid_functional_relation_alignment()
    record["proposition_tags"] = [
        {"proposition_id": "C01-P01", "occurrence_class": "capability_only"}
    ]
    path = _write_alignment_file(tmp_path, record)
    errors = validate_file(path, "author_alignment")
    assert errors == [], [str(error) for error in errors]


def test_polarity_on_component_mapping_validates_clean(tmp_path: Path) -> None:
    # GAP 1: absence/denial statements that yield only a component_mapping can
    # now carry an optional top-level polarity=explicit_denial.
    record = _valid_component_mapping_alignment()
    record["polarity"] = "explicit_denial"
    path = _write_alignment_file(tmp_path, record)
    errors = validate_file(path, "author_alignment")
    assert errors == [], [str(error) for error in errors]


def test_polarity_on_functional_relation_is_rejected(tmp_path: Path) -> None:
    # Top-level polarity is restricted to component_mapping; functional_relation
    # records carry polarity inside proposition_tags instead.
    record = _valid_functional_relation_alignment()
    record["polarity"] = "explicit_denial"
    path = _write_alignment_file(tmp_path, record)
    errors = validate_file(path, "author_alignment")
    codes = {error.code for error in errors}
    assert codes == {"V5_ALIGNMENT_KIND_FIELD_MISMATCH"}, [str(error) for error in errors]


def test_bad_polarity_on_component_mapping_is_rejected(tmp_path: Path) -> None:
    record = _valid_component_mapping_alignment()
    record["polarity"] = "strongly_opposed"
    path = _write_alignment_file(tmp_path, record)
    errors = validate_file(path, "author_alignment")
    codes = {error.code for error in errors}
    assert codes == {"V5_ENUM_INVALID"}, [str(error) for error in errors]


def test_three_digit_alignment_id_validates_clean(tmp_path: Path) -> None:
    # GAP 3: alignment_id widened to 3 digits (C06 produced 119 records).
    record = _valid_functional_relation_alignment()
    record["alignment_id"] = "C01-A119"
    path = _write_alignment_file(tmp_path, record)
    errors = validate_file(path, "author_alignment")
    assert errors == [], [str(error) for error in errors]


def test_four_digit_alignment_id_is_rejected(tmp_path: Path) -> None:
    record = _valid_functional_relation_alignment()
    record["alignment_id"] = "C01-A1199"
    path = _write_alignment_file(tmp_path, record)
    errors = validate_file(path, "author_alignment")
    codes = {error.code for error in errors}
    assert codes == {"V5_ID_PATTERN_INVALID"}, [str(error) for error in errors]


def test_three_digit_proposition_id_is_rejected(tmp_path: Path) -> None:
    # GAP 3 widened alignment ids ONLY; proposition ids stay 2-digit.
    root = _temp_analysis_root(tmp_path, mutate_first_proposition={"proposition_id": "C01-P100"})
    errors = validate_file(root / "servo_v5_source_propositions" / "C01.json", "source_proposition")
    codes = {error.code for error in errors}
    assert "V5_ID_PATTERN_INVALID" in codes, [str(error) for error in errors]


# ---------------------------------------------------------------------------
# policy: seven-axis BED-lens decomposition (charter B.4, schema-v3
# re-derivation per contract section B, 2026-07-23). The explicit_bed
# compliance model (mechanism_labels / purpose_facets / explicit_bed_evidence
# + V5_POLICY_EXPLICIT_BED_EVIDENCE_MISSING) was retired earlier; the v3
# re-derivation retired the old `none` control_dependence (split into
# fixed_or_predefined vs not_reported), the `performance`/`exploration`
# selection_objective labels and the `expected_discrimination_selected`
# execution rule, and added the generation_scope and candidate_selection_rule
# axes.
# ---------------------------------------------------------------------------


def _valid_policy_payload() -> dict:
    return {
        "schema": "servo_v5_policy",
        "status": "draft",
        "case_id": "C01",
        "control_dependence": ["failure", "observation_result"],
        "selection_signal": ["reaction yield", "prior-round observations"],
        "selection_objective": ["local_repair", "performance_improvement"],
        "generation_scope": ["fixed_space"],
        "candidate_selection_rule": ["sequential_choice"],
        "design_selection_rule": ["fixed_or_standard_design"],
        "candidate_execution_rule": ["one_at_a_time", "until_success"],
        "formal_epistemic_utility_evidence": "not_reported",
        "rationale": "grounded in C01-P01/C01-P90.",
    }


def _write_policy_file(tmp_path: Path, payload: dict) -> Path:
    root = tmp_path / "analysis"
    root.mkdir()
    shutil.copyfile(REAL_ANALYSIS_DIR / "servo_v5_schema.yaml", root / "servo_v5_schema.yaml")
    policy_dir = root / "servo_v5_policy"
    policy_dir.mkdir()
    path = policy_dir / "C01.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def test_valid_policy_record_validates_clean(tmp_path: Path) -> None:
    path = _write_policy_file(tmp_path, _valid_policy_payload())
    errors = validate_file(path, "policy")
    assert errors == [], [str(error) for error in errors]


def test_policy_missing_axis_is_rejected(tmp_path: Path) -> None:
    payload = _valid_policy_payload()
    del payload["candidate_execution_rule"]
    path = _write_policy_file(tmp_path, payload)
    errors = validate_file(path, "policy")
    assert "V5_ENVELOPE_FIELD_MISSING" in {error.code for error in errors}, [str(e) for e in errors]


def test_policy_bad_enum_value_is_rejected(tmp_path: Path) -> None:
    payload = _valid_policy_payload()
    payload["selection_objective"] = ["local_repair", "world_domination"]
    path = _write_policy_file(tmp_path, payload)
    errors = validate_file(path, "policy")
    assert {error.code for error in errors} == {"V5_ENUM_INVALID"}, [str(e) for e in errors]


def test_policy_empty_selection_signal_is_rejected(tmp_path: Path) -> None:
    payload = _valid_policy_payload()
    payload["selection_signal"] = []
    path = _write_policy_file(tmp_path, payload)
    errors = validate_file(path, "policy")
    assert "V5_FIELD_EMPTY" in {error.code for error in errors}, [str(e) for e in errors]


def test_policy_missing_formal_epistemic_utility_evidence_is_rejected(tmp_path: Path) -> None:
    payload = _valid_policy_payload()
    del payload["formal_epistemic_utility_evidence"]
    path = _write_policy_file(tmp_path, payload)
    errors = validate_file(path, "policy")
    assert "V5_ENVELOPE_FIELD_MISSING" in {error.code for error in errors}, [str(e) for e in errors]


def test_policy_retired_explicit_bed_field_is_rejected(tmp_path: Path) -> None:
    # The retired compliance model's fields are no longer part of the envelope.
    payload = _valid_policy_payload()
    payload["mechanism_labels"] = ["explicit_bed"]
    path = _write_policy_file(tmp_path, payload)
    errors = validate_file(path, "policy")
    assert "V5_ENVELOPE_FIELD_UNKNOWN" in {error.code for error in errors}, [str(e) for e in errors]


# --- schema-v3 new axes: generation_scope, candidate_selection_rule ---------


def test_policy_missing_generation_scope_is_rejected(tmp_path: Path) -> None:
    payload = _valid_policy_payload()
    del payload["generation_scope"]
    path = _write_policy_file(tmp_path, payload)
    errors = validate_file(path, "policy")
    assert "V5_ENVELOPE_FIELD_MISSING" in {error.code for error in errors}, [str(e) for e in errors]


def test_policy_missing_candidate_selection_rule_is_rejected(tmp_path: Path) -> None:
    payload = _valid_policy_payload()
    del payload["candidate_selection_rule"]
    path = _write_policy_file(tmp_path, payload)
    errors = validate_file(path, "policy")
    assert "V5_ENVELOPE_FIELD_MISSING" in {error.code for error in errors}, [str(e) for e in errors]


def test_policy_bad_generation_scope_enum_is_rejected(tmp_path: Path) -> None:
    payload = _valid_policy_payload()
    payload["generation_scope"] = ["fixed_space", "wander_freely"]
    path = _write_policy_file(tmp_path, payload)
    errors = validate_file(path, "policy")
    assert {error.code for error in errors} == {"V5_ENUM_INVALID"}, [str(e) for e in errors]


def test_policy_bad_candidate_selection_rule_enum_is_rejected(tmp_path: Path) -> None:
    payload = _valid_policy_payload()
    payload["candidate_selection_rule"] = ["vibes"]
    path = _write_policy_file(tmp_path, payload)
    errors = validate_file(path, "policy")
    assert {error.code for error in errors} == {"V5_ENUM_INVALID"}, [str(e) for e in errors]


# --- schema-v3+ new axis: design_selection_rule (reviewer Item 2) ------------
# The action is a=(h,d,P,f): design_selection_rule (how the experimental
# design/assay d is chosen) is a separate axis from candidate_selection_rule
# (which candidate hypotheses h are chosen).


def test_policy_missing_design_selection_rule_is_rejected(tmp_path: Path) -> None:
    payload = _valid_policy_payload()
    del payload["design_selection_rule"]
    path = _write_policy_file(tmp_path, payload)
    errors = validate_file(path, "policy")
    assert "V5_ENVELOPE_FIELD_MISSING" in {error.code for error in errors}, [str(e) for e in errors]


def test_policy_bad_design_selection_rule_enum_is_rejected(tmp_path: Path) -> None:
    payload = _valid_policy_payload()
    payload["design_selection_rule"] = ["intuition_directed"]
    path = _write_policy_file(tmp_path, payload)
    errors = validate_file(path, "policy")
    assert {error.code for error in errors} == {"V5_ENUM_INVALID"}, [str(e) for e in errors]


def test_policy_design_selection_rule_coverage_and_discrimination_validate_clean(tmp_path: Path) -> None:
    # Both the reported-in-corpus value (coverage_or_factorial) and the
    # not-observed-but-defined value (discrimination_directed) are legal enum
    # members: the axis can express a discrimination-directed design even though
    # no bounded source reports one.
    payload = _valid_policy_payload()
    payload["design_selection_rule"] = ["coverage_or_factorial", "discrimination_directed"]
    path = _write_policy_file(tmp_path, payload)
    errors = validate_file(path, "policy")
    assert errors == [], [str(error) for error in errors]


# --- schema-v3 retired enum values are now rejected -------------------------


def test_policy_retired_control_dependence_none_is_rejected(tmp_path: Path) -> None:
    # `none` was split into fixed_or_predefined (confirmed outcome-independence)
    # and not_reported (source silence); the bare `none` value is gone.
    payload = _valid_policy_payload()
    payload["control_dependence"] = ["none"]
    path = _write_policy_file(tmp_path, payload)
    errors = validate_file(path, "policy")
    assert {error.code for error in errors} == {"V5_ENUM_INVALID"}, [str(e) for e in errors]


def test_policy_retired_selection_objective_exploration_is_rejected(tmp_path: Path) -> None:
    payload = _valid_policy_payload()
    payload["selection_objective"] = ["exploration"]
    path = _write_policy_file(tmp_path, payload)
    errors = validate_file(path, "policy")
    assert {error.code for error in errors} == {"V5_ENUM_INVALID"}, [str(e) for e in errors]


def test_policy_not_reported_selection_objective_validates_clean(tmp_path: Path) -> None:
    # OD-M6: not_reported is a legal selection_objective value -- used when the
    # bounded source establishes no uncertainty- or discrimination-DIRECTED
    # objective (e.g. C05: measurement-power design + confirm/refute capability,
    # but Adam tests ALL hypotheses, so no experiment is SELECTED). Read
    # silence/capability as not_reported, never as a directed objective.
    payload = _valid_policy_payload()
    payload["selection_objective"] = ["not_reported"]
    path = _write_policy_file(tmp_path, payload)
    errors = validate_file(path, "policy")
    assert errors == [], [str(error) for error in errors]


def test_policy_retired_execution_rule_expected_discrimination_is_rejected(tmp_path: Path) -> None:
    # expected_discrimination_selected mixed objective into the execution rule
    # and was deleted; a discrimination OBJECTIVE lives in selection_objective.
    payload = _valid_policy_payload()
    payload["candidate_execution_rule"] = ["expected_discrimination_selected"]
    path = _write_policy_file(tmp_path, payload)
    errors = validate_file(path, "policy")
    assert {error.code for error in errors} == {"V5_ENUM_INVALID"}, [str(e) for e in errors]


# --- fixed_or_predefined vs not_reported are distinct, both valid -----------


def test_policy_fixed_or_predefined_control_dependence_validates_clean(tmp_path: Path) -> None:
    # Confirmed outcome-independence in the source (e.g. C04-P23, C05-P13..P16).
    payload = _valid_policy_payload()
    payload["control_dependence"] = ["fixed_or_predefined", "observation_result"]
    path = _write_policy_file(tmp_path, payload)
    errors = validate_file(path, "policy")
    assert errors == [], [str(error) for error in errors]


def test_policy_not_reported_control_dependence_validates_clean(tmp_path: Path) -> None:
    # Undeterminable from the bounded public source; NEVER read as fixed.
    payload = _valid_policy_payload()
    payload["control_dependence"] = ["not_reported"]
    path = _write_policy_file(tmp_path, payload)
    errors = validate_file(path, "policy")
    assert errors == [], [str(error) for error in errors]


def test_policy_fixed_or_predefined_and_not_reported_are_distinct_values(tmp_path: Path) -> None:
    # The two former-`none` dispositions are separate enum members: swapping one
    # in does not make the other legal, so a typo mixing them is not silently
    # accepted. Here `not_stated` (neither valid value) must be rejected.
    payload = _valid_policy_payload()
    payload["control_dependence"] = ["not_stated"]
    path = _write_policy_file(tmp_path, payload)
    errors = validate_file(path, "policy")
    assert {error.code for error in errors} == {"V5_ENUM_INVALID"}, [str(e) for e in errors]
