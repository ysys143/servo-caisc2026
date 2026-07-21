from __future__ import annotations

import itertools
import math
from collections.abc import Sequence


def fleiss_kappa(ratings: Sequence[Sequence[int]]) -> float:
    if not ratings:
        return math.nan
    raters = sum(ratings[0])
    if raters < 2 or any(sum(row) != raters for row in ratings):
        return math.nan
    categories = len(ratings[0])
    if categories == 0 or any(len(row) != categories for row in ratings):
        return math.nan
    observed = sum(
        (sum(count * count for count in row) - raters) / (raters * (raters - 1))
        for row in ratings
    ) / len(ratings)
    totals = [sum(row[index] for row in ratings) for index in range(categories)]
    proportions = [total / (len(ratings) * raters) for total in totals]
    expected = sum(proportion * proportion for proportion in proportions)
    if math.isclose(expected, 1.0):
        return math.nan
    return (observed - expected) / (1.0 - expected)


def masi_distance(left: frozenset[str], right: frozenset[str]) -> float:
    union = left | right
    if not union:
        return 0.0
    intersection = left & right
    if left == right:
        weight = 1.0
    elif left.issubset(right) or right.issubset(left):
        weight = 2.0 / 3.0
    elif intersection:
        weight = 1.0 / 3.0
    else:
        weight = 0.0
    return 1.0 - weight * len(intersection) / len(union)


def mean_pairwise_jaccard(values: Sequence[frozenset[str]]) -> float:
    pairs = tuple(itertools.combinations(values, 2))
    informative = tuple((left, right) for left, right in pairs if left or right)
    if not informative:
        return math.nan
    return sum(len(left & right) / len(left | right) for left, right in informative) / len(
        informative
    )


def nominal_agreement(values: Sequence[str]) -> float:
    pairs = tuple(itertools.combinations(values, 2))
    if not pairs:
        return math.nan
    return sum(left == right for left, right in pairs) / len(pairs)


def krippendorff_alpha_masi(units: Sequence[Sequence[frozenset[str]]]) -> float:
    observed_pairs = tuple(
        pair for unit in units for pair in itertools.combinations(unit, 2)
    )
    if not observed_pairs:
        return math.nan
    observed = sum(masi_distance(left, right) for left, right in observed_pairs) / len(
        observed_pairs
    )
    pooled = tuple(value for unit in units for value in unit)
    expected_pairs = tuple(itertools.combinations(pooled, 2))
    expected = sum(masi_distance(left, right) for left, right in expected_pairs) / len(
        expected_pairs
    )
    if math.isclose(expected, 0.0):
        return math.nan
    return 1.0 - observed / expected
