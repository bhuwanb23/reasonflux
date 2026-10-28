"""Validation Test 1 — Frequency (Phase 11C-3)."""

from __future__ import annotations

from core.invariant import Invariant
from invariants.validation.scores import ValidationConfig, normalize_count


def score_frequency(
    invariant: Invariant, config: ValidationConfig | None = None
) -> float:
    """F in [0, 1]: how often the structure occurs."""
    config = config or ValidationConfig()
    return normalize_count(invariant.frequency, config.freq_norm)


def passes_frequency(
    f_score: float, config: ValidationConfig | None = None
) -> bool:
    """True when frequency score meets the minimum gate."""
    config = config or ValidationConfig()
    return f_score >= config.min_f
