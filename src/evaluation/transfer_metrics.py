"""Transfer Score (TS) = performance_after − performance_before (CGM)."""

from __future__ import annotations


def compute_ts(performance_before: float, performance_after: float) -> float:
    """Compute system-level Transfer Score between two performance readings."""
    before = float(performance_before)
    after = float(performance_after)
    return after - before
