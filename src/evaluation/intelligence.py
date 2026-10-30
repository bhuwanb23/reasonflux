"""ASFT Intelligence Growth Model (Phase 11E-3)."""

from __future__ import annotations

from typing import Mapping

from evaluation.growth_config import GrowthConfig

# Maturity stages from phase_11e_3.md
INTELLIGENCE_STAGES = (
    "emerging",
    "developing",
    "generalizing",
    "compositional",
    "adaptive",
)


def intelligence_score(
    ag: float,
    su: float,
    ts: float,
    cgr: float,
    cp: float,
    ad: float,
    *,
    weights: Mapping[str, float] | None = None,
    growth_config: GrowthConfig | None = None,
) -> float:
    """IG = f(AG, SU, TS, CGR, CP, AD) as a weighted sum.

    Default weights (sum to 1.0):
      AG 0.15, SU 0.15, TS 0.20, CGR 0.25, CP 0.15, AD 0.10
    """
    del growth_config  # reserved for future threshold coupling
    defaults = {
        "ag": 0.15,
        "su": 0.15,
        "ts": 0.20,
        "cgr": 0.25,
        "cp": 0.15,
        "ad": 0.10,
    }
    w = {**defaults, **(dict(weights) if weights else {})}
    return (
        float(w["ag"]) * float(ag)
        + float(w["su"]) * float(su)
        + float(w["ts"]) * float(ts)
        + float(w["cgr"]) * float(cgr)
        + float(w["cp"]) * float(cp)
        + float(w["ad"]) * float(ad)
    )


def compute_igr(current_ig: float, previous_ig: float, dt: float = 1.0) -> float:
    """IGR = (IG_t − IG_{t−1}) / Δt."""
    if dt <= 0:
        raise ValueError("dt must be > 0")
    return (float(current_ig) - float(previous_ig)) / float(dt)


def compute_ia(current_igr: float, previous_igr: float, dt: float = 1.0) -> float:
    """IA = (IGR_t − IGR_{t−1}) / Δt."""
    if dt <= 0:
        raise ValueError("dt must be > 0")
    return (float(current_igr) - float(previous_igr)) / float(dt)


def compute_ie(ig: float, experiences: int | float) -> float:
    """IE = IG / Experiences (0 if experiences ≤ 0)."""
    exp = float(experiences or 0.0)
    if exp <= 0:
        return 0.0
    return float(ig) / exp


def compute_elasticity(ig_delta: float, new_families: int, dt: float = 1.0) -> float:
    """Elasticity = (ΔIG / new_families) / Δt."""
    if dt <= 0:
        raise ValueError("dt must be > 0")
    nf = int(new_families or 0)
    if nf <= 0:
        return 0.0
    return float(ig_delta) / float(nf) / float(dt)


def classify_intelligence_stage(
    *,
    skill_count: int = 0,
    transfer_events: int = 0,
    cross_family: bool = False,
    composition_ok: bool = False,
    adaptation_ok: bool = False,
    igr: float = 0.0,
) -> str:
    """Map signals into the Intelligence Maturity Model stage."""
    if adaptation_ok and igr > 0:
        return "adaptive"
    if composition_ok and cross_family:
        return "compositional"
    if cross_family or transfer_events >= 3:
        return "generalizing"
    if skill_count >= 2 and (transfer_events > 0 or igr > 0):
        return "developing"
    return "emerging"
