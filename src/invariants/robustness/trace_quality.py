"""Noisy trace down-weighting (F6)."""

from __future__ import annotations

from invariants.robustness.config import RobustnessConfig
from invariants.robustness.metrics import compute_tc


def trace_weight(tc: float, config: RobustnessConfig | None = None) -> float:
    """Weight for mining/validation; below min_tc uses TC as weight."""
    config = config or RobustnessConfig()
    tc = max(0.0, min(1.0, float(tc)))
    if tc >= config.min_tc:
        return 1.0
    return tc


def weight_from_steps(
    consistent_steps: int, total_steps: int, config: RobustnessConfig | None = None
) -> float:
    return trace_weight(compute_tc(consistent_steps, total_steps), config)
