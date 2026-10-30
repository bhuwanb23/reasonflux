"""Capability Utility CapU (Phase 11E-1)."""

from __future__ import annotations

from dataclasses import dataclass

from capability.config import CapabilityConfig
from capability.coverage import compute_coverage
from capability.models import Capability
from skills.library import SkillLibrary
from skills.utility import compute_su


@dataclass(slots=True)
class CapabilityUtilityBreakdown:
    mean_su: float = 0.0
    mean_ts: float = 0.0
    coverage: float = 0.0
    composition_bonus: float = 0.0
    capu: float = 0.0

    def to_dict(self) -> dict[str, float]:
        return {
            "mean_su": self.mean_su,
            "mean_ts": self.mean_ts,
            "coverage": self.coverage,
            "composition_bonus": self.composition_bonus,
            "capu": self.capu,
        }


def _composition_bonus(capability: Capability, library: SkillLibrary) -> float:
    if not capability.skill_ids:
        return 0.0
    composed = 0
    for sid in capability.skill_ids:
        skill = library.get(sid)
        if skill is None:
            continue
        meta = skill.metadata or {}
        if meta.get("composed_from") or meta.get("capability_candidate"):
            composed += 1
    return composed / len(capability.skill_ids)


def compute_capability_utility(
    capability: Capability,
    library: SkillLibrary,
    config: CapabilityConfig | None = None,
    *,
    total_families: int | None = None,
    record_history: bool = True,
) -> CapabilityUtilityBreakdown:
    """CapU = w_su·mean(SU) + w_ts·mean(TS) + w_cov·CCov + w_comp·comp_bonus."""
    config = config or CapabilityConfig()
    sus: list[float] = []
    tss: list[float] = []
    for sid in capability.skill_ids:
        skill = library.get(sid)
        if skill is None:
            continue
        su = float(
            skill.utility
            if (skill.metadata or {}).get("utility_breakdown")
            else compute_su(skill)
        )
        sus.append(su)
        tss.append(float(skill.transfer_score or 0.0))
    mean_su = sum(sus) / len(sus) if sus else 0.0
    mean_ts = sum(tss) / len(tss) if tss else 0.0
    cov = compute_coverage(
        capability, library=library, total_families=total_families, config=config
    )
    bonus = _composition_bonus(capability, library)
    capu = (
        config.capu_w_su * mean_su
        + config.capu_w_ts * mean_ts
        + config.capu_w_cov * cov
        + config.capu_w_comp * bonus
    )
    breakdown = CapabilityUtilityBreakdown(
        mean_su=mean_su,
        mean_ts=mean_ts,
        coverage=cov,
        composition_bonus=bonus,
        capu=float(capu),
    )
    if record_history:
        capability.utility = breakdown.capu
        meta = dict(capability.metadata or {})
        meta["capu_breakdown"] = breakdown.to_dict()
        capability.metadata = meta
        capability.utility_history = list(capability.utility_history or [])
        capability.utility_history.append({"utility": breakdown.capu})
    return breakdown
