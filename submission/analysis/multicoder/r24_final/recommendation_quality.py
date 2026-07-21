from __future__ import annotations

import hashlib
import json
import random
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path
from typing import Annotated, ClassVar, Final

from pydantic import BaseModel, ConfigDict, Field, model_validator

from r24_final.models import BaselineCoding, ServoCoding
from r24_final.schedule import VENDORS


QUALITY_SEED: Final = 20260721


class FrozenModel(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid", frozen=True)


class Preference(StrEnum):
    A = "A"
    B = "B"
    TIE = "tie"
    NOT_JUDGABLE = "not_judgable"


class Dimension(StrEnum):
    EVIDENCE = "evidence_support"
    FIT = "diagnosis_remedy_fit"
    ACTIONABILITY = "actionability"
    VERIFIABILITY = "success_check_verifiability"
    SCOPE = "scope_proportionality"
    COVERAGE = "set_coverage_nonredundancy"


class DimensionScore(FrozenModel):
    dimension: Dimension
    score: Annotated[int, Field(ge=0, le=2)]
    recommendation_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    rationale: Annotated[str, Field(min_length=1)]


class SetScore(FrozenModel):
    label: Annotated[str, Field(pattern=r"^[AB]$")]
    dimensions: Annotated[tuple[DimensionScore, ...], Field(min_length=6, max_length=6)]

    @model_validator(mode="after")
    def dimensions_are_complete(self) -> SetScore:
        if {item.dimension for item in self.dimensions} != set(Dimension):
            raise ValueError("each rubric dimension must occur exactly once")
        return self


class QualityJudgment(FrozenModel):
    pair_id: Annotated[str, Field(min_length=1)]
    judge_vendor: Annotated[str, Field(min_length=1)]
    scores: Annotated[tuple[SetScore, ...], Field(min_length=2, max_length=2)]
    preference: Preference
    comparative_rationale: Annotated[str, Field(min_length=1)]

    @model_validator(mode="after")
    def labels_are_complete(self) -> QualityJudgment:
        if {score.label for score in self.scores} != {"A", "B"}:
            raise ValueError("judgment must score A and B exactly once")
        return self


@dataclass(frozen=True, slots=True)
class JudgeTrial:
    trial_id: str
    pair_id: str
    record_id: str
    origin_vendor: str
    judge_vendor: str
    display_order: tuple[str, str]


def build_judge_schedule(record_ids: tuple[str, ...], seed: int = QUALITY_SEED) -> tuple[JudgeTrial, ...]:
    trials: list[JudgeTrial] = []
    pair_number = 0
    for origin_index, origin in enumerate(VENDORS):
        judges = tuple(vendor for vendor in VENDORS if vendor != origin)
        for record_index, record_id in enumerate(record_ids):
            pair_number += 1
            pair_id = f"P{pair_number:03d}"
            baseline_first = random.Random(seed + origin_index * 100 + record_index).choice((True, False))
            first = ("baseline", "servo") if baseline_first else ("servo", "baseline")
            first_judge_index = random.Random(
                seed + 10_000 + origin_index * 100 + record_index
            ).choice((0, 1))
            for judge_index, judge in enumerate(judges):
                order: tuple[str, str] = first if judge_index == first_judge_index else (first[1], first[0])
                trials.append(JudgeTrial(f"judge-{judge}-{pair_id}", pair_id, record_id, origin, judge, order))
    return tuple(trials)


def anonymous_pair(run_dir: Path, trial: JudgeTrial) -> dict[str, object]:
    outputs: dict[str, dict[str, object]] = {}
    for condition in ("baseline", "servo"):
        period = _period_for(run_dir, trial.origin_vendor, trial.record_id, condition)
        path = run_dir / "accepted" / f"{trial.origin_vendor}-{trial.record_id}-{period}.json"
        raw = json.loads(path.read_text(encoding="utf-8"))
        model = BaselineCoding.model_validate(raw) if condition == "baseline" else ServoCoding.model_validate(raw)
        outputs[condition] = {
            "diagnostics": [item.model_dump(mode="json") for item in model.envelope.diagnostics],
            "recommendations": [item.model_dump(mode="json") for item in model.envelope.recommendations],
        }
    return {label: outputs[condition] for label, condition in zip(("A", "B"), trial.display_order, strict=True)}


def build_quality_prompt(root: Path, run_dir: Path, trial: JudgeTrial) -> str:
    packet = (root / "packets" / f"{trial.record_id}.json").read_text(encoding="utf-8")
    pair = json.dumps(anonymous_pair(run_dir, trial), indent=2, sort_keys=True)
    schema = json.dumps(QualityJudgment.model_json_schema(), indent=2, sort_keys=True)
    return "\n\n".join((
        (root / "recommendation_rubric.md").read_text(encoding="utf-8"),
        "Return JSON only. Do not infer facts outside the packet. Judge A and B independently before selecting a preference.",
        f"Pair metadata: pair_id={trial.pair_id}; judge_vendor={trial.judge_vendor}.",
        f"Anonymous source packet:\n{packet}",
        f"Blinded recommendation sets:\n{pair}",
        f"Required JSON schema:\n{schema}",
    ))


def validate_quality_judgment(
    judgment: QualityJudgment,
    trial: JudgeTrial,
    pair: dict[str, object],
) -> None:
    if judgment.pair_id != trial.pair_id or judgment.judge_vendor != trial.judge_vendor:
        raise ValueError("pair_id or judge_vendor mismatch")
    for set_score in judgment.scores:
        candidate = pair[set_score.label]
        if not isinstance(candidate, dict):
            raise ValueError(f"malformed anonymous set {set_score.label}")
        recommendations = candidate.get("recommendations")
        diagnostics = candidate.get("diagnostics")
        if not isinstance(recommendations, list) or not isinstance(diagnostics, list):
            raise ValueError(f"malformed anonymous set {set_score.label}")
        recommendation_ids = {
            item.get("id") for item in recommendations if isinstance(item, dict)
        }
        evidence_ids = {
            evidence_id
            for collection in (recommendations, diagnostics)
            for item in collection
            if isinstance(item, dict)
            for evidence_id in item.get("evidence_ids", [])
            if isinstance(evidence_id, str)
        }
        for dimension in set_score.dimensions:
            if not dimension.recommendation_ids:
                raise ValueError("every dimension score must identify a recommendation")
            if not set(dimension.recommendation_ids) <= recommendation_ids:
                raise ValueError("dimension cites an unknown recommendation_id")
            if not dimension.evidence_ids:
                raise ValueError("every dimension score must identify packet evidence")
            if not set(dimension.evidence_ids) <= evidence_ids:
                raise ValueError("dimension cites evidence absent from the anonymous set")


def schedule_sha256(trials: tuple[JudgeTrial, ...]) -> str:
    raw = json.dumps([asdict(trial) for trial in trials], sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()


def _period_for(run_dir: Path, vendor: str, record_id: str, condition: str) -> int:
    for period in (1, 2):
        path = run_dir / "accepted" / f"{vendor}-{record_id}-{period}.json"
        if not path.is_file():
            continue
        raw = json.loads(path.read_text(encoding="utf-8"))
        is_servo = "channels" in raw
        if (condition == "servo") == is_servo:
            return period
    raise FileNotFoundError(f"missing paired {condition} output for {vendor}/{record_id}")
