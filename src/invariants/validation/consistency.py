"""Validation Test 2 — Consistency (Phase 11C-3)."""

from __future__ import annotations

from core.invariant import Invariant
from invariants.validation.scores import ValidationConfig, clamp01


def score_consistency(invariant: Invariant) -> float:
    """C in [0, 1]: does the structure remain stable?"""
    return clamp01(invariant.consistency)


def passes_consistency(
    c_score: float, config: ValidationConfig | None = None
) -> bool:
    """True when consistency meets the minimum gate."""
    config = config or ValidationConfig()
    return c_score >= config.min_c
