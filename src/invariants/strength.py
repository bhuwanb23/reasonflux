"""Invariant Strength (IS) = frequency × consistency × generality (IDT)."""

from __future__ import annotations

from core.invariant import Invariant

__all__ = [
    "MINIMUM_INVARIANT_STRENGTH",
    "compute_invariant_strength",
    "is_above_threshold",
]

#: Default floor from configs/thresholds.yaml (invariants.minimum_invariant_strength).
MINIMUM_INVARIANT_STRENGTH: float = 5.0


def compute_invariant_strength(
    frequency: float, consistency: float, generality: float
) -> float:
    """Compute IS for an invariant candidate.

    Args:
        frequency: Number of traces containing the pattern (>= 0).
        consistency: Stability of the pattern across occurrences, in [0, 1].
        generality: Breadth across task families, in [0, 1].

    Returns:
        frequency × consistency × generality.
    """
    if frequency < 0:
        raise ValueError("frequency must be >= 0")
    if not 0.0 <= consistency <= 1.0:
        raise ValueError("consistency must be in [0, 1]")
    if not 0.0 <= generality <= 1.0:
        raise ValueError("generality must be in [0, 1]")
    return float(frequency) * float(consistency) * float(generality)


def is_above_threshold(
    invariant: Invariant, threshold: float = MINIMUM_INVARIANT_STRENGTH
) -> bool:
    """True when the invariant's strength meets or exceeds ``threshold``."""
    return invariant.strength >= threshold
