"""Validation Test 4 — Transfer potential (Phase 11C-3)."""

from __future__ import annotations

from core.invariant import Invariant
from invariants.validation.scores import ValidationConfig, clamp01, normalize_count


def score_transfer(
    invariant: Invariant,
    config: ValidationConfig | None = None,
    *,
    override: float | None = None,
) -> float:
    """T in [0, 1]: does this invariant help future tasks?

    Prefer explicit ``override``, then ``transfer_contribution`` if > 0,
    else normalize ``evidence.transfer_events``.
    """
    config = config or ValidationConfig()
    if override is not None:
        return clamp01(override)
    if invariant.transfer_contribution > 0:
        return clamp01(invariant.transfer_contribution)
    return normalize_count(invariant.evidence.transfer_events, config.transfer_norm)


def passes_transfer(
    t_score: float, config: ValidationConfig | None = None
) -> bool:
    """True when transfer score is positive enough for promotion."""
    config = config or ValidationConfig()
    return t_score >= config.min_t
