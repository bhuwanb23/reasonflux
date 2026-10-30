"""ASFT Intelligence Growth Model (Phase 11E-3).

Provides a lightweight, configurable intelligence score and helpers.
"""

from __future__ import annotations

from typing import Mapping

from evaluation.growth_config import GrowthConfig


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
    """Compute IG as weighted sum of components.

    Components: AG, SU, TS, CGR, CP (composition potential), AD (adaptation).
    Defaults use GrowthConfig.ig_weights as a starting point for CGR/related
    weights; remaining components default to equal small shares.
    """
    gc = growth_config or GrowthConfig()
    w = dict(weights or {})
    # base w for CGR-related pieces from growth_config
    w.setdefault("cgr", gc.ig_w_cgr)
    w.setdefault("tg", gc.ig_w_tg)
    w.setdefault("ug", gc.ig_w_ug)
    w.setdefault("ccg", gc.ig_w_ccg)
    w.setdefault("compg", gc.ig_w_compg)
    # Ensure all named components present; map our args into these buckets.
    # We map: cgr->cgr, tg ~ ts, ug ~ su, ccg ~ cp, compg ~ ad (conservative mapping)
    cgr_w = float(w.get("cgr", 0.4))
    tg_w = float(w.get("tg", 0.2))
    ug_w = float(w.get("ug", 0.2))
    ccg_w = float(w.get("ccg", 0.1))
    compg_w = float(w.get("compg", 0.1))

    return (
        cgr_w * float(cgr)
        + tg_w * float(ts)
        + ug_w * float(su)
        + ccg_w * float(cp)
        + compg_w * float(ad)
    )


def compute_igr(current_ig: float, previous_ig: float, dt: float = 1.0) -> float:
    if dt <= 0:
        raise ValueError("dt must be > 0")
    return (float(current_ig) - float(previous_ig)) / float(dt)


def compute_ia(current_igr: float, previous_igr: float, dt: float = 1.0) -> float:
    if dt <= 0:
        raise ValueError("dt must be > 0")
    return (float(current_igr) - float(previous_igr)) / float(dt)


def compute_ie(ig: float, experiences: int | float) -> float:
    """Intelligence efficiency = IG / experiences (0 if experiences==0)."""
    exp = float(experiences or 0.0)
    if exp <= 0:
        return 0.0
    return float(ig) / exp


def compute_elasticity(ig_delta: float, new_families: int, dt: float = 1.0) -> float:
    """Elasticity = (IG change per new family) / dt. Returns 0 if new_families==0."""
    if dt <= 0:
        raise ValueError("dt must be > 0")
    nf = int(new_families or 0)
    if nf <= 0:
        return 0.0
    return float(ig_delta) / float(nf) / float(dt)

