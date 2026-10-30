"""Validation Test 3 — Generality (Phase 11C-3)."""

from __future__ import annotations

from core.invariant import Invariant
from invariants.validation.scores import ValidationConfig, clamp01


def score_generality(invariant: Invariant) -> float:
    """G in [0, 1]: can this invariant survive task variation?"""
    return clamp01(invariant.generality)


def passes_generality(
    g_score: float, config: ValidationConfig | None = None
) -> bool:
    """True when generality meets the minimum gate."""
    config = config or ValidationConfig()
    return g_score >= config.min_g
