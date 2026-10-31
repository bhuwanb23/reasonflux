"""Invariant-related metrics (IS and helpers) for CGM / IDT evaluation.

The IS formula has exactly one implementation,
:func:`invariants.strength.compute_invariant_strength`. This module is the
reporting-side adapter so evaluation code never re-derives it.
"""

from __future__ import annotations

from typing import Sequence

from core.invariant import Invariant
from invariants.strength import (
    MINIMUM_INVARIANT_STRENGTH,
    compute_invariant_strength,
    is_above_threshold,
)

__all__ = [
    "compute_is",
    "is_abstraction_gain_positive",
    "mean_is",
    "summarize_is",
]


def compute_is(invariant: Invariant) -> float:
    """Invariant Strength of a concrete invariant."""
    return compute_invariant_strength(
        float(invariant.frequency),
        float(invariant.consistency),
        float(invariant.generality),
    )


def mean_is(invariants: Sequence[Invariant]) -> float:
    """Average IS across a set of invariants (0.0 when empty)."""
    if not invariants:
        return 0.0
    return sum(compute_is(i) for i in invariants) / len(invariants)


def summarize_is(
    invariants: Sequence[Invariant],
    threshold: float = MINIMUM_INVARIANT_STRENGTH,
) -> dict[str, float]:
    """Counts and spread, suitable for a paper table row."""
    scores = [compute_is(i) for i in invariants]
    return {
        "n": float(len(scores)),
        "mean": (sum(scores) / len(scores)) if scores else 0.0,
        "max": max(scores) if scores else 0.0,
        "min": min(scores) if scores else 0.0,
        "above_threshold": float(
            sum(1 for i in invariants if is_above_threshold(i, threshold))
        ),
        "threshold": float(threshold),
    }


def is_abstraction_gain_positive(skill_ag: float) -> bool:
    """AG > 0 is the SCT precondition that reasoning cost actually fell."""
    return float(skill_ag) > 0.0
