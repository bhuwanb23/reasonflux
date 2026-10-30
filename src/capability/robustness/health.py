"""Capability / portfolio health bands (Phase 11E-5)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Sequence

from capability.library import CapabilityLibrary
from capability.models import Capability
from capability.portfolio import compute_capability_portfolio
from capability.robustness.config import CapabilityRobustnessConfig
from capability.robustness.metrics import (
    capability_health_score,
    capability_stability,
)
from capability.states import CapabilityLifecycle
from skills.library import SkillLibrary


class HealthBand(str, Enum):
    EXCELLENT = "excellent"
    HEALTHY = "healthy"
    STABLE = "stable"
    WEAK = "weak"
    CRITICAL = "critical"


@dataclass(slots=True)
class CapabilityHealth:
    capability_id: str
    chs: float
    cs: float
    band: HealthBand

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "chs": self.chs,
            "cs": self.cs,
            "band": self.band.value,
        }


@dataclass(slots=True)
class PortfolioHealth:
    mean_chs: float
    mean_cs: float
    band: HealthBand
    members: list[CapabilityHealth]

    def to_dict(self) -> dict[str, Any]:
        return {
            "mean_chs": self.mean_chs,
            "mean_cs": self.mean_cs,
            "band": self.band.value,
            "members": [m.to_dict() for m in self.members],
        }


def band_from_chs(chs: float, config: CapabilityRobustnessConfig) -> HealthBand:
    if chs >= config.chs_excellent:
        return HealthBand.EXCELLENT
    if chs >= config.chs_healthy:
        return HealthBand.HEALTHY
    if chs >= config.chs_stable:
        return HealthBand.STABLE
    if chs >= config.chs_weak:
        return HealthBand.WEAK
    return HealthBand.CRITICAL


def score_capability(
    cap: Capability,
    skill_lib: SkillLibrary,
    *,
    utility_series: Sequence[float] | None = None,
    config: CapabilityRobustnessConfig | None = None,
) -> CapabilityHealth:
    config = config or CapabilityRobustnessConfig()
    utils = [
        float(skill_lib.get(sid).utility)  # type: ignore[union-attr]
        for sid in cap.skill_ids
        if skill_lib.get(sid) is not None
    ]
    transfers = [
        float(skill_lib.get(sid).transfer_score or 0.0)  # type: ignore[union-attr]
        for sid in cap.skill_ids
        if skill_lib.get(sid) is not None
    ]
    mean_u = sum(utils) / len(utils) if utils else 0.0
    mean_t = sum(transfers) / len(transfers) if transfers else 0.0
    cov = min(1.0, len(cap.skill_ids) / 10.0)
    conf = float((cap.metadata or {}).get("confidence", 0.5))
    growth = float((cap.metadata or {}).get("cgr", 0.0))
    chs = capability_health_score(
        utility=mean_u,
        transfer=mean_t,
        coverage=cov,
        growth=growth,
        confidence=conf,
    )
    series = list(utility_series) if utility_series is not None else utils or [mean_u]
    cs = capability_stability(series, unstable_var=config.cs_unstable)
    return CapabilityHealth(
        capability_id=cap.capability_id,
        chs=chs,
        cs=cs,
        band=band_from_chs(chs, config),
    )


def score_portfolio(
    cap_lib: CapabilityLibrary,
    skill_lib: SkillLibrary,
    *,
    config: CapabilityRobustnessConfig | None = None,
) -> PortfolioHealth:
    config = config or CapabilityRobustnessConfig()
    members: list[CapabilityHealth] = []
    for cap in cap_lib.list_capabilities():
        if cap.state is CapabilityLifecycle.ARCHIVED:
            continue
        members.append(score_capability(cap, skill_lib, config=config))
    if not members:
        return PortfolioHealth(0.0, 0.0, HealthBand.CRITICAL, [])
    mean_chs = sum(m.chs for m in members) / len(members)
    mean_cs = sum(m.cs for m in members) / len(members)
    # Tie portfolio band to mean CHS; penalize if portfolio CapU is zero.
    port = compute_capability_portfolio(cap_lib, skill_lib, refresh=False)
    if port.mean_capu <= 0:
        mean_chs = min(mean_chs, config.chs_weak - 0.01)
    return PortfolioHealth(
        mean_chs=mean_chs,
        mean_cs=mean_cs,
        band=band_from_chs(mean_chs, config),
        members=members,
    )
