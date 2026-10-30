"""Robustness metrics: IER, VST, TC, TFD (Phase 11C-5)."""

from __future__ import annotations

from typing import Sequence


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def compute_ier(invariant_count: int, trace_count: int) -> float:
    """Invariant Explosion Ratio = invariants / traces."""
    if trace_count <= 0:
        return float(invariant_count) if invariant_count > 0 else 0.0
    return float(invariant_count) / trace_count


def compute_vst(successful_variations: int, total_variations: int) -> float:
    """Variation Survival Test = successful / total."""
    if total_variations <= 0:
        return 1.0
    return _clamp01(successful_variations / total_variations)


def compute_tc(consistent_steps: int, total_steps: int) -> float:
    """Trace consistency = consistent steps / total steps."""
    if total_steps <= 0:
        return 1.0
    return _clamp01(consistent_steps / total_steps)


def compute_tfd(unique_families: int, total_tasks: int) -> float:
    """Task family diversity = unique families / total tasks."""
    if total_tasks <= 0:
        return 0.0
    return _clamp01(unique_families / total_tasks)


def variation_counts_from_metadata(metadata: dict | None) -> tuple[int, int]:
    """Derive successful/total variation probes from invariant metadata."""
    meta = metadata or {}
    variations = meta.get("variations") or []
    failed = meta.get("failed_variations") or []
    if variations:
        total = len(variations)
        failed_set = {str(f).lower() for f in failed}
        success = sum(
            1 for v in variations if str(v).lower() not in failed_set
        )
        return success, total
    markers = {"color", "shape", "position", "count"}
    failed_set = {str(f).lower() for f in failed if str(f).lower() in markers}
    if failed_set:
        total = len(markers)
        success = total - len(failed_set)
        return max(0, success), total
    return len(markers), len(markers)
