from __future__ import annotations

import math

from r24_final.agreement import (
    fleiss_kappa,
    krippendorff_alpha_masi,
    mean_pairwise_jaccard,
    masi_distance,
)


def test_fleiss_is_undefined_for_constant_category() -> None:
    # Given
    ratings = ((3, 0), (3, 0))

    # When
    result = fleiss_kappa(ratings)

    # Then
    assert math.isnan(result)


def test_masi_penalizes_disjoint_sets_fully() -> None:
    # Given / When
    result = masi_distance(frozenset({"a"}), frozenset({"b"}))

    # Then
    assert result == 1.0


def test_empty_sets_do_not_inflate_jaccard() -> None:
    # Given / When
    result = mean_pairwise_jaccard((frozenset(), frozenset(), frozenset()))

    # Then
    assert math.isnan(result)


def test_masi_alpha_is_one_for_identical_nonconstant_units() -> None:
    # Given
    units = (
        (frozenset({"a"}), frozenset({"a"}), frozenset({"a"})),
        (frozenset({"b"}), frozenset({"b"}), frozenset({"b"})),
    )

    # When
    result = krippendorff_alpha_masi(units)

    # Then
    assert result == 1.0
