"""Invariant explosion ratio monitoring (F2)."""

from __future__ import annotations

from invariants.robustness.config import RobustnessConfig
from invariants.robustness.metrics import compute_ier


def ier_level(ier: float, config: RobustnessConfig | None = None) -> str:
    """Return ok, warn, or restrict for an IER reading."""
    config = config or RobustnessConfig()
    if ier >= config.ier_restrict:
        return "restrict"
    if ier >= config.ier_warn:
        return "warn"
    return "ok"


def should_restrict_promotion(ier: float, config: RobustnessConfig | None = None) -> bool:
    """True when explosion ratio blocks new promotions."""
    config = config or RobustnessConfig()
    return ier >= config.ier_restrict


def monitor_ier(
    invariant_count: int, trace_count: int, config: RobustnessConfig | None = None
) -> dict:
    """Return IER value and severity level."""
    config = config or RobustnessConfig()
    ier = compute_ier(invariant_count, trace_count)
    return {"ier": ier, "level": ier_level(ier, config)}
