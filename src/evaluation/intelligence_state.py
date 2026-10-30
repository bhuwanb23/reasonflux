"""IntelligenceState dataclasses and system-level helpers (Phase 11E-3)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from capability.library import CapabilityLibrary
from evaluation.growth_config import GrowthConfig
from evaluation.intelligence import (
    classify_intelligence_stage,
    compute_elasticity,
    compute_ia,
    compute_ie,
    compute_igr,
    intelligence_score,
)
from skills.library import SkillLibrary


@dataclass(slots=True)
class IntelligencePortfolioMetrics:
    capability_score: float = 0.0
    n: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_score": float(self.capability_score),
            "n": int(self.n),
        }


@dataclass(slots=True)
class IntelligenceState:
    ig: float = 0.0
    igr: float = 0.0
    ia: float = 0.0
    ie: float = 0.0
    elasticity: float = 0.0
    stage: str = "emerging"
    portfolio: IntelligencePortfolioMetrics | None = None
    timestamp: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ig": float(self.ig),
            "igr": float(self.igr),
            "ia": float(self.ia),
            "ie": float(self.ie),
            "elasticity": float(self.elasticity),
            "stage": self.stage,
            "portfolio": self.portfolio.to_dict() if self.portfolio else None,
            "timestamp": float(self.timestamp),
            "metadata": dict(self.metadata or {}),
        }


def compute_system_intelligence_state(
    capability_library: CapabilityLibrary,
    skill_library: SkillLibrary,
    *,
    previous_intel: IntelligenceState | None = None,
    previous_capability_score: float | None = None,
    previous_ig: float | None = None,
    experiences: int | float = 0,
    new_families: int = 0,
    dt: float = 1.0,
    growth_config: GrowthConfig | None = None,
    ag: float = 0.0,
    su: float = 0.0,
    ts: float = 0.0,
    cp: float = 0.0,
    ad: float = 0.0,
) -> IntelligenceState:
    """Build IntelligenceState from CGM outputs + optional component proxies."""
    # Lazy import avoids evaluation ↔ capability.portfolio circular import.
    from capability.portfolio import compute_system_capability_state

    sys = compute_system_capability_state(
        capability_library,
        skill_library,
        previous_score=previous_capability_score,
        dt=dt,
        growth_config=growth_config,
    )
    cap_score = float(sys.capability_score)
    cgr = float(sys.cgr)

    # Prefer explicit component args; fall back to portfolio proxies.
    mean_su = su if su else float(
        (sys.portfolio.mean_capu if sys.portfolio else 0.0) or 0.0
    )
    mean_ts = ts
    if mean_ts == 0.0:
        vals = [
            float(s.transfer_score or 0.0)
            for s in skill_library.list_skills()
        ]
        mean_ts = sum(vals) / len(vals) if vals else 0.0

    ig = intelligence_score(
        ag=ag,
        su=mean_su,
        ts=mean_ts,
        cgr=cgr,
        cp=cp,
        ad=ad,
        growth_config=growth_config,
    )

    if previous_ig is not None:
        prev_ig = float(previous_ig)
    elif previous_intel is not None:
        prev_ig = float(previous_intel.ig)
    else:
        prev_ig = 0.0

    igr = compute_igr(ig, prev_ig, dt=dt)
    prev_igr = float(previous_intel.igr) if previous_intel is not None else 0.0
    ia = compute_ia(igr, prev_igr, dt=dt)
    ie = compute_ie(ig, experiences)
    elasticity = compute_elasticity(ig - prev_ig, new_families, dt=dt)

    n_skills = len(skill_library)
    transfer_events = sum(len(s.transfer_history or []) for s in skill_library.list_skills())
    families = {
        str((e or {}).get("target_family") or "").lower()
        for s in skill_library.list_skills()
        for e in (s.transfer_history or [])
        if (e or {}).get("target_family")
    }
    composed = any(
        (s.metadata or {}).get("composed_from") or (s.metadata or {}).get("capability_candidate")
        for s in skill_library.list_skills()
    )
    stage = classify_intelligence_stage(
        skill_count=n_skills,
        transfer_events=transfer_events,
        cross_family=len(families) >= 2,
        composition_ok=composed,
        adaptation_ok=ad > 0 and igr > 0,
        igr=igr,
    )

    return IntelligenceState(
        ig=ig,
        igr=igr,
        ia=ia,
        ie=ie,
        elasticity=elasticity,
        stage=stage,
        portfolio=IntelligencePortfolioMetrics(
            capability_score=cap_score, n=len(capability_library)
        ),
        timestamp=0.0,
        metadata={"cgr": cgr, "capability_score": cap_score},
    )
