from __future__ import annotations

import pytest

from r24_final.recommendation_quality import (
    QualityJudgment,
    build_judge_schedule,
    validate_quality_judgment,
)


def test_quality_schedule_uses_two_nonoriginating_judges_and_reverses_order() -> None:
    trials = build_judge_schedule(tuple(f"R{i:02d}" for i in range(1, 15)))
    assert len(trials) == 84
    assert len({trial.trial_id for trial in trials}) == 84
    for pair_id in {trial.pair_id for trial in trials}:
        pair = [trial for trial in trials if trial.pair_id == pair_id]
        assert len(pair) == 2
        assert all(trial.judge_vendor != trial.origin_vendor for trial in pair)
        assert pair[1].display_order == tuple(reversed(pair[0].display_order))
        assert all(trial.origin_vendor not in trial.pair_id for trial in pair)


def test_quality_schedule_randomizes_orientation_assignment_across_judges() -> None:
    trials = build_judge_schedule(tuple(f"R{i:02d}" for i in range(1, 15)))
    first_orientation_judges = {
        pair[0].judge_vendor
        for pair_id in {trial.pair_id for trial in trials}
        if (pair := [trial for trial in trials if trial.pair_id == pair_id])
        and pair[0].display_order == ("baseline", "servo")
    }
    assert len(first_orientation_judges) > 1


def test_quality_gate_rejects_unknown_recommendation_reference() -> None:
    trial = build_judge_schedule(("R01",))[0]
    dimensions = [
        {
            "dimension": dimension,
            "score": 1,
            "recommendation_ids": ["UNKNOWN"],
            "evidence_ids": ["R01-E01"],
            "rationale": "reason",
        }
        for dimension in (
            "evidence_support",
            "diagnosis_remedy_fit",
            "actionability",
            "success_check_verifiability",
            "scope_proportionality",
            "set_coverage_nonredundancy",
        )
    ]
    judgment = QualityJudgment.model_validate(
        {
            "pair_id": trial.pair_id,
            "judge_vendor": trial.judge_vendor,
            "scores": [
                {"label": "A", "dimensions": dimensions},
                {"label": "B", "dimensions": dimensions},
            ],
            "preference": "tie",
            "comparative_rationale": "reason",
        }
    )
    pair = {
        label: {
            "recommendations": [{"id": "R1", "evidence_ids": ["R01-E01"]}],
            "diagnostics": [],
        }
        for label in ("A", "B")
    }
    with pytest.raises(ValueError, match="unknown recommendation_id"):
        validate_quality_judgment(judgment, trial, pair)
