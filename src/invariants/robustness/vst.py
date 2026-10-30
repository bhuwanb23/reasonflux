"""Variation Survival Test from invariant metadata (F1)."""

from __future__ import annotations

from core.invariant import Invariant
from invariants.robustness.config import RobustnessConfig
from invariants.robustness.metrics import compute_vst, variation_counts_from_metadata


def vst_for_invariant(invariant: Invariant) -> float:
    """Compute VST score for one invariant."""
    success, total = variation_counts_from_metadata(invariant.metadata)
    return compute_vst(success, total)


def passes_vst(invariant: Invariant, config: RobustnessConfig | None = None) -> bool:
    """True when VST meets the minimum threshold."""
    config = config or RobustnessConfig()
    return vst_for_invariant(invariant) >= config.min_vst
