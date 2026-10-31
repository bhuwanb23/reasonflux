"""Robustness metrics: FR, CSR, CHS, CS, NTR/TG helpers (Phase 11E-5)."""

from __future__ import annotations

from typing import Sequence

from capability.library import CapabilityLibrary
from capability.states import CapabilityLifecycle
from evaluation.growth_metrics import compute_saturation_ratio
from skills.library import SkillLibrary


def fragmentation_ratio(
    capability_library: CapabilityLibrary, skill_library: SkillLibrary
) -> float:
    """FR = |capabilities| / |skills| (non-archived)."""
    n_skills = max(1, len(skill_library))
    n_caps = sum(
        1
        for c in capability_library.list_capabilities()
        if c.state is not CapabilityLifecycle.ARCHIVED
    )
    return float(n_caps) / float(n_skills)


def saturation_ratio(new_cap: float, existing_cap: float) -> float:
    return compute_saturation_ratio(new_cap, existing_cap)


def mean_transfer_score(skill_library: SkillLibrary) -> float:
    skills = skill_library.list_skills()
    if not skills:
        return 0.0
    return sum(float(s.transfer_score or 0.0) for s in skills) / len(skills)


def negative_transfer_rate(skill_library: SkillLibrary) -> float:
    attempts = 0
    negative = 0
    for s in skill_library.list_skills():
        for ev in s.transfer_history or []:
            attempts += 1
            if not bool(ev.get("success", True)):
                negative += 1
    return (negative / attempts) if attempts else 0.0


def transfer_growth(prev_ts: float, curr_ts: float) -> float:
    return float(curr_ts) - float(prev_ts)


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def capability_health_score(
    *,
    utility: float,
    transfer: float,
    coverage: float,
    growth: float,
    confidence: float = 0.5,
) -> float:
    """CHS = weighted mean of utility/transfer/coverage/growth/confidence."""
    g = _clamp01(0.5 + 0.5 * float(growth))  # map small CGR into [0,1]
    return _clamp01(
        0.25 * float(utility)
        + 0.25 * float(transfer)
        + 0.2 * float(coverage)
        + 0.15 * g
        + 0.15 * float(confidence)
    )


def capability_stability(
    series: Sequence[float], *, unstable_var: float = 0.3
) -> float:
    """CS = 1 − normalized variance of a metric series."""
    vals = [float(x) for x in series]
    if len(vals) < 2:
        return 0.5
    mean = sum(vals) / len(vals)
    var = sum((x - mean) ** 2 for x in vals) / len(vals)
    # Soft-normalize by unstable_var threshold.
    return _clamp01(1.0 - var / max(unstable_var, 1e-9))


def series_cgr_signs(cgr_series: Sequence[float]) -> tuple[int, int]:
    """Return (negative_count, positive_count) ignoring zeros."""
    neg = sum(1 for x in cgr_series if float(x) < -1e-12)
    pos = sum(1 for x in cgr_series if float(x) > 1e-12)
    return neg, pos
