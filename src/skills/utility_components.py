"""SU component calculators — RCG, TV, CP, RV, CC, MC, NR (Phase 11D-2)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.skill import Skill
from skills.config import SkillConfig


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


@dataclass(slots=True)
class SkillUtilityBreakdown:
    """Benefit − cost decomposition for Skill Utility."""

    rcg: float = 0.0
    tv: float = 0.0
    cp: float = 0.0
    rv: float = 0.0
    cc: float = 0.0
    mc: float = 0.0
    nr: float = 0.0
    su: float = 0.0

    @property
    def benefit(self) -> float:
        return self.rcg + self.tv + self.cp + self.rv

    @property
    def cost(self) -> float:
        return self.cc + self.mc + self.nr

    def to_dict(self) -> dict[str, float]:
        return {
            "rcg": self.rcg,
            "tv": self.tv,
            "cp": self.cp,
            "rv": self.rv,
            "cc": self.cc,
            "mc": self.mc,
            "nr": self.nr,
            "su": self.su,
            "benefit": self.benefit,
            "cost": self.cost,
        }


def compute_rcg(skill: Skill) -> float:
    """RCG = RC_before − RC_after, or abstraction_gain proxy."""
    meta = skill.metadata or {}
    if "rc_before" in meta and "rc_after" in meta:
        before = float(meta["rc_before"])
        after = float(meta["rc_after"])
        if before > 0:
            return _clamp01((before - after) / before)
        return _clamp01(before - after)
    return _clamp01(skill.abstraction_gain)


def compute_tv(skill: Skill, config: SkillConfig | None = None) -> float:
    """TV = transfer_success_rate × task_coverage."""
    config = config or SkillConfig()
    history = list(skill.transfer_history or [])
    if not history:
        # Fall back to birth-time transfer score lightly.
        return _clamp01(float(skill.transfer_score) * 0.5)
    successes = sum(1 for e in history if e.get("success", True))
    rate = successes / len(history)
    families = {
        str(e.get("target_family", "")).strip()
        for e in history
        if e.get("success", True) and e.get("target_family")
    }
    coverage = len(families) / config.tv_coverage_norm
    return _clamp01(rate * coverage)


def compute_cp(skill: Skill, config: SkillConfig | None = None) -> float:
    """Composition potential from metadata or MVP-category heuristic."""
    config = config or SkillConfig()
    meta = skill.metadata or {}
    if "composition_potential" in meta:
        return _clamp01(float(meta["composition_potential"]))
    category = str(meta.get("mvp_category", "general"))
    # Specialized / literal-heavy signatures → lower CP.
    sig = list(skill.trigger_conditions or meta.get("pattern_signature") or [])
    if any(":" in str(s) for s in sig):
        return _clamp01(config.default_cp * 0.3)
    if category in ("reflection", "rotation", "counting", "grouping"):
        return _clamp01(max(config.default_cp, 0.5))
    return _clamp01(config.default_cp)


def compute_rv(skill: Skill, config: SkillConfig | None = None) -> float:
    """RV = normalized reuse_count × average impact."""
    config = config or SkillConfig()
    count = int(skill.reuse_count or 0)
    events = list(skill.reuse_history or [])
    impacts = [float(e.get("impact", 1.0)) for e in events]
    avg_impact = sum(impacts) / len(impacts) if impacts else 1.0
    return _clamp01(count / config.reuse_norm) * _clamp01(avg_impact)


def compute_mc(skill: Skill, config: SkillConfig | None = None) -> float:
    """Maintenance = base + per-skill storage weight."""
    config = config or SkillConfig()
    return max(0.0, float(config.base_maintenance) + 0.01)


def compute_nr(skill: Skill, config: SkillConfig | None = None) -> float:
    """NR = negative_transfer_rate × impact."""
    config = config or SkillConfig()
    history = list(skill.transfer_history or [])
    meta = skill.metadata or {}
    evidence = meta.get("evidence") or {}
    negatives = list(evidence.get("negative") or [])
    failed = sum(1 for e in history if not e.get("success", True))
    attempts = len(history)
    if attempts == 0:
        ntr = min(1.0, len(negatives) / 3.0) if negatives else 0.0
    else:
        ntr = failed / attempts
    return _clamp01(ntr * float(config.ntr_impact))


def breakdown_for_skill(
    skill: Skill, config: SkillConfig | None = None
) -> SkillUtilityBreakdown:
    """Assemble full SU breakdown."""
    config = config or SkillConfig()
    rcg = compute_rcg(skill)
    tv = compute_tv(skill, config)
    cp = compute_cp(skill, config)
    rv = compute_rv(skill, config)
    cc = max(0.0, float(skill.creation_cost))
    mc = compute_mc(skill, config)
    nr = compute_nr(skill, config)
    su = (rcg + tv + cp + rv) - (cc + mc + nr)
    return SkillUtilityBreakdown(
        rcg=rcg, tv=tv, cp=cp, rv=rv, cc=cc, mc=mc, nr=nr, su=su
    )
