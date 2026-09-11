"""Pure-Python scientific fallbacks for Wave-4 dependency contingency."""

from __future__ import annotations

import math
from decimal import Decimal
from typing import Sequence


def mean(values: Sequence[Decimal | float | int]) -> float:
    if not values:
        raise ValueError("MEAN_EMPTY_SEQUENCE")
    return float(sum(float(value) for value in values) / len(values))


def pearson_correlation(
    left: Sequence[Decimal | float | int],
    right: Sequence[Decimal | float | int],
) -> float:
    if len(left) != len(right):
        raise ValueError("CORRELATION_LENGTH_MISMATCH")
    if len(left) < 2:
        raise ValueError("CORRELATION_REQUIRES_TWO_OR_MORE")
    left_mean = mean(left)
    right_mean = mean(right)
    numerator = sum(
        (float(a) - left_mean) * (float(b) - right_mean)
        for a, b in zip(left, right, strict=True)
    )
    left_var = sum((float(a) - left_mean) ** 2 for a in left)
    right_var = sum((float(b) - right_mean) ** 2 for b in right)
    denominator = math.sqrt(left_var * right_var)
    if denominator == 0:
        raise ValueError("CORRELATION_ZERO_VARIANCE")
    return numerator / denominator
