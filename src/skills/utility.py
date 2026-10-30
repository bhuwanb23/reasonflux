"""Skill Utility scoring and economic status (Phase 11D-2)."""

from __future__ import annotations

from core.skill import Skill
from skills.config import SkillConfig
from skills.utility_components import SkillUtilityBreakdown, breakdown_for_skill

EconomicStatus = str  # unproven | useful | core | declining | retirement_candidate


def score_skill_utility(
    skill: Skill, config: SkillConfig | None = None
) -> SkillUtilityBreakdown:
    """Return full SU breakdown for a skill."""
    return breakdown_for_skill(skill, config)


def compute_su(skill: Skill, config: SkillConfig | None = None) -> float:
    """SU = (RCG + TV + CP + RV) − (CC + MC + NR)."""
    return score_skill_utility(skill, config).su


def classify_economic_status(
    skill: Skill,
    breakdown: SkillUtilityBreakdown,
    config: SkillConfig | None = None,
    *,
    previous_su: float | None = None,
) -> EconomicStatus:
    """Map SU / reuse / transfer into economic status (metadata, not SkillState)."""
    config = config or SkillConfig()
    su = breakdown.su
    if su < config.su_min:
        return "retirement_candidate"
    reuse = int(skill.reuse_count or 0)
    transfer_ok = breakdown.tv >= config.core_min_transfer or float(
        skill.transfer_score or 0.0
    ) >= config.core_min_transfer
    if (
        su >= config.core_su
        and reuse >= config.core_min_reuse
        and transfer_ok
    ):
        return "core"
    if previous_su is not None and su < previous_su - 1e-9 and reuse > 0:
        return "declining"
    if reuse == 0 and len(skill.transfer_history or []) <= 1 and su <= config.core_su:
        return "unproven"
    if su > config.su_min:
        return "useful"
    return "retirement_candidate"


def refresh_skill_utility(
    skill: Skill, config: SkillConfig | None = None
) -> SkillUtilityBreakdown:
    """Recompute SU, write skill.utility and economic metadata."""
    config = config or SkillConfig()
    meta = dict(skill.metadata or {})
    previous = meta.get("utility_breakdown") or {}
    previous_su = previous.get("su")
    if previous_su is not None:
        previous_su = float(previous_su)
    breakdown = score_skill_utility(skill, config)
    status = classify_economic_status(
        skill, breakdown, config, previous_su=previous_su
    )
    skill.utility = float(breakdown.su)
    meta["utility_breakdown"] = breakdown.to_dict()
    meta["economic_status"] = status
    meta["retirement_candidate"] = status == "retirement_candidate"
    skill.metadata = meta
    return breakdown
