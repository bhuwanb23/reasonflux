"""Composition metrics re-export for evaluation side (Phase 11D-4)."""

from __future__ import annotations

from skills.composition.models import CompositionCandidate
from skills.composition.utility import CompositionUtilityBreakdown, compute_cu


def composition_ncr(candidate: CompositionCandidate) -> float:
    """Negative composition rate."""
    return float(candidate.ncr)


__all__ = [
    "CompositionUtilityBreakdown",
    "composition_ncr",
    "compute_cu",
]
