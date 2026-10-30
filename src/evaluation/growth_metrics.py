"""Capability Growth Rate (CGR) and Intelligence Growth (IG) — Phase 11E-2."""

from __future__ import annotations

from typing import Sequence

from capability.config import CapabilityConfig
from capability.library import CapabilityLibrary
from capability.models import Capability
from capability.states import CapabilityLifecycle
from capability.utility import compute_capability_utility
from evaluation.growth_config import GrowthConfig
from skills.library import SkillLibrary


def capability_score(
    capability: Capability,
    *,
    library: SkillLibrary,
    config: CapabilityConfig | None = None,
    growth_config: GrowthConfig | None = None,
    total_families: int | None = None,
    record_history: bool = False,
) -> float:
    """C_t = w_su·mean(SU) + w_ts·mean(TS) + w_cov·CCov + w_comp·CP.

    Reuses CapU breakdown; growth_config weights override CapU weights when set.
    """
    config = config or CapabilityConfig()
    gc = growth_config or GrowthConfig()
    # Temporarily apply growth weights via a shallow CapU config copy.
    weighted = CapabilityConfig(
        min_skills=config.min_skills,
        min_transfer_events=config.min_transfer_events,
        min_utility=config.min_utility,
        min_confidence=config.min_confidence,
        min_coverage=config.min_coverage,
        ccov_family_norm=config.ccov_family_norm,
        capu_w_su=gc.w_su,
        capu_w_ts=gc.w_ts,
        capu_w_cov=gc.w_cov,
        capu_w_comp=gc.w_comp,
        strength_reuse_norm=config.strength_reuse_norm,
        core_min_strength=config.core_min_strength,
        core_min_confidence=config.core_min_confidence,
        decline_ug=config.decline_ug,
        overlap_similarity=config.overlap_similarity,
        max_capabilities=config.max_capabilities,
        monolith_skill_fraction=config.monolith_skill_fraction,
        archive_low_utility_periods=config.archive_low_utility_periods,
        skill_count_norm=config.skill_count_norm,
    )
    breakdown = compute_capability_utility(
        capability,
        library,
        weighted,
        total_families=total_families,
        record_history=record_history,
    )
    return float(breakdown.capu)


def compute_portfolio_capability(
    capability_library: CapabilityLibrary,
    skill_library: SkillLibrary,
    *,
    config: CapabilityConfig | None = None,
    growth_config: GrowthConfig | None = None,
    total_families: int | None = None,
) -> float:
    """System-level C_t = mean capability_score over non-archived capabilities."""
    caps = [
        c
        for c in capability_library.list_capabilities()
        if c.state is not CapabilityLifecycle.ARCHIVED
    ]
    if not caps:
        return 0.0
    scores = [
        capability_score(
            c,
            library=skill_library,
            config=config,
            growth_config=growth_config,
            total_families=total_families,
            record_history=False,
        )
        for c in caps
    ]
    return sum(scores) / len(scores)


def compute_cg_rate(
    current_c: float, previous_c: float, dt: float = 1.0
) -> float:
    """CGR = (C_t − C_{t−1}) / Δt."""
    if dt <= 0:
        raise ValueError("dt must be > 0")
    return (float(current_c) - float(previous_c)) / float(dt)


def compute_cgr(
    series_of_c: Sequence[float] | None = None,
    *,
    current_c: float | None = None,
    previous_c: float | None = None,
    dt: float = 1.0,
) -> float:
    """Capability Growth Rate from a series or an explicit pair."""
    if series_of_c is not None:
        vals = [float(x) for x in series_of_c]
        if len(vals) < 2:
            return 0.0
        return compute_cg_rate(vals[-1], vals[-2], dt=dt)
    if current_c is None or previous_c is None:
        raise ValueError("provide series_of_c or both current_c and previous_c")
    return compute_cg_rate(current_c, previous_c, dt=dt)


def compute_ca(
    current_cgr: float, previous_cgr: float, dt: float = 1.0
) -> float:
    """Capability Acceleration CA = (CGR_t − CGR_{t−1}) / Δt."""
    if dt <= 0:
        raise ValueError("dt must be > 0")
    return (float(current_cgr) - float(previous_cgr)) / float(dt)


def compute_saturation_ratio(new_cap: float, existing_cap: float) -> float:
    """CSR = NewCapability / ExistingCapability (0 if existing ≤ 0)."""
    existing = float(existing_cap)
    if existing <= 0:
        return 0.0 if float(new_cap) <= 0 else 1.0
    return float(new_cap) / existing


def compute_ig(
    cgr: float,
    tg: float = 0.0,
    ug: float = 0.0,
    ccg: float = 0.0,
    compg: float = 0.0,
    *,
    weights: dict[str, float] | None = None,
    growth_config: GrowthConfig | None = None,
) -> float:
    """IG = w_cgr·CGR + w_tg·TG + w_ug·UG + w_ccg·CCG + w_compg·CompG."""
    gc = growth_config or GrowthConfig()
    w = weights or gc.ig_weights()
    return (
        float(w.get("cgr", gc.ig_w_cgr)) * float(cgr)
        + float(w.get("tg", gc.ig_w_tg)) * float(tg)
        + float(w.get("ug", gc.ig_w_ug)) * float(ug)
        + float(w.get("ccg", gc.ig_w_ccg)) * float(ccg)
        + float(w.get("compg", gc.ig_w_compg)) * float(compg)
    )


# Growth state labels from CGR / CA / CSR.
GROWTH_STATES = (
    "emerging",
    "growing",
    "accelerating",
    "mature",
    "saturated",
    "declining",
)


def classify_growth_state(
    cgr: float,
    *,
    ca: float = 0.0,
    csr: float = 1.0,
    growth_config: GrowthConfig | None = None,
    has_history: bool = True,
) -> str:
    """Map CGR / CA / CSR into a growth state label."""
    gc = growth_config or GrowthConfig()
    if not has_history:
        return "emerging"
    if cgr < -1e-9:
        return "declining"
    if csr <= gc.saturation_low_csr and abs(cgr) <= gc.skill_count_illusion_max_cgr:
        return "saturated"
    if ca > 1e-9 and cgr > 1e-9:
        return "accelerating"
    if cgr > 1e-9:
        return "growing"
    if abs(cgr) <= gc.skill_count_illusion_max_cgr:
        return "mature"
    return "growing"
