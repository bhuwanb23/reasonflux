"""Validation Test 5 — Reasoning value (Phase 11C-3)."""

from __future__ import annotations

from core.invariant import Invariant
from invariants.validation.scores import ValidationConfig, clamp01


def score_reasoning_value(invariant: Invariant) -> float:
    """R in [0, 1]: does this invariant reduce reasoning cost?

    Reads ``metadata['reasoning_value']`` or ``metadata['abstraction_gain']``.
    Defaults to 0.0 (frequent-but-useless patterns fail without an R signal).
    """
    meta = invariant.metadata or {}
    if "reasoning_value" in meta:
        return clamp01(float(meta["reasoning_value"]))
    if "abstraction_gain" in meta:
        return clamp01(float(meta["abstraction_gain"]))
    return 0.0


def passes_reasoning_value(
    r_score: float, config: ValidationConfig | None = None
) -> bool:
    """True when reasoning-value score meets the minimum gate."""
    config = config or ValidationConfig()
    return r_score >= config.min_r
