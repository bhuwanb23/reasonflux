"""Edge cases EC1–EC4 (Phase 11D-5)."""

from __future__ import annotations

from core.skill import Skill
from core.states import SkillState
from skills.lifecycle.biography import append_biography_event
from skills.robustness.config import SkillRobustnessConfig


def rare_high_value_override(
    skill: Skill, config: SkillRobustnessConfig | None = None
) -> bool:
    """EC1: high transfer overrides low frequency / evidence floors."""
    config = config or SkillRobustnessConfig()
    ts = float(skill.transfer_score or 0.0)
    return ts >= float(config.transfer_override_min)


def is_ancient_core(
    skill: Skill, config: SkillRobustnessConfig | None = None
) -> bool:
    """EC2: historically crucial core skill — do not retire for inactivity."""
    config = config or SkillRobustnessConfig()
    life = dict((skill.metadata or {}).get("lifecycle") or {})
    age = int(life.get("age_tasks", 0) or 0)
    peak = (skill.metadata or {}).get("biography") or {}
    peak_u = 0.0
    if isinstance(peak.get("peak_utility"), dict):
        peak_u = float(peak["peak_utility"].get("utility", 0.0) or 0.0)
    historical = max(float(skill.utility or 0.0), peak_u)
    return (
        skill.state is SkillState.CORE
        or (
            age >= int(config.ancient_core_min_age)
            and historical > float(config.su_min)
            and int(skill.reuse_count or 0) >= 3
        )
    )


def enforce_zombie_archive(
    skill: Skill, config: SkillRobustnessConfig | None = None
) -> bool:
    """EC3: repeated failed reactivations → permanent archive.

    Returns True only when the skill actually reached ARCHIVED.
    """
    config = config or SkillRobustnessConfig()
    meta = dict(skill.metadata or {})
    attempts = int(meta.get("reactivations", 0) or 0)
    last = dict(meta.get("last_reactivation") or {})
    raised = bool(last.get("raised_utility", False))
    threshold = int(config.zombie_permanent_archive_attempts)
    if attempts < threshold or raised:
        return False
    if skill.state is SkillState.ARCHIVED:
        return False

    # Walk any live state to RETIRED, then ARCHIVED.
    if skill.state is SkillState.CANDIDATE:
        skill.transition_to(SkillState.RETIRED)
    elif skill.state is SkillState.PROMOTED:
        skill.transition_to(SkillState.RETIRED)
    elif skill.state is SkillState.ACTIVE:
        skill.transition_to(SkillState.RETIRED)
    elif skill.state is SkillState.GROWING:
        skill.transition_to(SkillState.RETIRED)
    elif skill.state is SkillState.CORE:
        skill.transition_to(SkillState.RETIRED)
    elif skill.state is SkillState.DORMANT:
        skill.transition_to(SkillState.RETIRED)
    if skill.state is SkillState.RETIRED:
        skill.transition_to(SkillState.ARCHIVED)
    if skill.state is not SkillState.ARCHIVED:
        return False

    meta["permanent_archive"] = True
    meta["zombie"] = True
    skill.metadata = meta
    append_biography_event(skill, "archived", {"reason": "zombie"})
    return True


def detect_cannibalization(
    candidate: Skill,
    core_skill: Skill,
    config: SkillRobustnessConfig | None = None,
) -> bool:
    """EC4: candidate steals retrieval from a better core skill."""
    config = config or SkillRobustnessConfig()
    cand_u = float(candidate.utility or 0.0)
    core_u = float(core_skill.utility or 0.0)
    if core_u <= 0:
        return False
    ratio = cand_u / core_u if core_u else 0.0
    # Cannibalization: candidate weaker than core but still capturing slots.
    if cand_u < core_u and ratio < float(config.cannibalization_ratio):
        # Also require overlapping triggers.
        a = {str(t).lower() for t in (candidate.trigger_conditions or [])}
        b = {str(t).lower() for t in (core_skill.trigger_conditions or [])}
        if a & b:
            return True
    return False
