from __future__ import annotations

import random
from dataclasses import dataclass
from enum import StrEnum
from typing import Final


VENDORS: Final = ("claude", "codex", "gemini")


class Condition(StrEnum):
    BASELINE = "baseline"
    SERVO = "servo"


@dataclass(frozen=True, slots=True)
class Trial:
    trial_id: str
    vendor: str
    record_id: str
    condition: Condition
    period: int
    order: int


def build_schedule(record_ids: tuple[str, ...], seed: int) -> tuple[Trial, ...]:
    if len(record_ids) != 14 or len(set(record_ids)) != 14:
        raise ValueError("schedule requires fourteen unique records")
    trials: list[Trial] = []
    for vendor_index, vendor in enumerate(VENDORS):
        ordered = list(record_ids)
        random.Random(seed + vendor_index).shuffle(ordered)
        for index, record_id in enumerate(ordered):
            trials.append(
                Trial(
                    f"{vendor}-{record_id}-servo",
                    vendor,
                    record_id,
                    Condition.SERVO,
                    1,
                    index,
                )
            )
    return tuple(sorted(trials, key=lambda trial: (trial.vendor, trial.order)))
