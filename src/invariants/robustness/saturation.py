"""Transfer saturation — diminishing returns (E4)."""

from __future__ import annotations

from invariants.robustness.config import RobustnessConfig


def diminishing_transfer_utility(
    success_count: int,
    base_tu: float,
    config: RobustnessConfig | None = None,
) -> float:
    """Effective TU after saturation_k successful reuses."""
    config = config or RobustnessConfig()
    base = max(0.0, min(1.0, float(base_tu)))
    k = config.saturation_k
    if success_count <= k:
        return base
    excess = success_count - k
    factor = 1.0 / (1.0 + 0.2 * excess)
    return max(0.0, min(1.0, base * factor))
