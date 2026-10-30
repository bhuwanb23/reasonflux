"""Statistical summaries for harness metrics (Phase 11E-4)."""

from __future__ import annotations

import math
from typing import Sequence


def _sorted(values: Sequence[float]) -> list[float]:
    return sorted(float(v) for v in values)


def mean(values: Sequence[float]) -> float:
    vals = list(values)
    if not vals:
        return 0.0
    return sum(float(v) for v in vals) / len(vals)


def median(values: Sequence[float]) -> float:
    vals = _sorted(values)
    if not vals:
        return 0.0
    n = len(vals)
    mid = n // 2
    if n % 2 == 1:
        return vals[mid]
    return 0.5 * (vals[mid - 1] + vals[mid])


def variance(values: Sequence[float], *, sample: bool = True) -> float:
    vals = [float(v) for v in values]
    n = len(vals)
    if n == 0:
        return 0.0
    if sample and n < 2:
        return 0.0
    m = mean(vals)
    denom = (n - 1) if sample else n
    return sum((x - m) ** 2 for x in vals) / denom


def confidence_interval(
    values: Sequence[float], *, z: float = 1.96
) -> tuple[float, float]:
    """Approximate 95% CI via normal: mean ± z * se."""
    vals = [float(v) for v in values]
    n = len(vals)
    if n == 0:
        return (0.0, 0.0)
    m = mean(vals)
    if n == 1:
        return (m, m)
    se = math.sqrt(variance(vals) / n)
    half = float(z) * se
    return (m - half, m + half)


def summarize(values: Sequence[float], *, z: float = 1.96) -> dict[str, float]:
    lo, hi = confidence_interval(values, z=z)
    return {
        "mean": mean(values),
        "median": median(values),
        "variance": variance(values),
        "ci_low": lo,
        "ci_high": hi,
        "n": float(len(list(values))),
    }
