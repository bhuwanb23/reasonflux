"""SF1 premature creation, SF2 explosion, SF3 duplicates (Phase 11D-5)."""

from __future__ import annotations

from core.skill import Skill
from core.states import SkillState
from skills.lifecycle.biography import append_biography_event
from skills.library import SkillLibrary
from skills.robustness.config import SkillRobustnessConfig
from skills.robustness.metrics import skill_explosion_ratio


def _evidence_count(skill: Skill) -> int:
    meta = skill.metadata or {}
    evidence = meta.get("evidence") or {}
    discovery = list(evidence.get("discovery") or [])
    utility = list(evidence.get("utility") or [])
    transfer = list(evidence.get("transfer") or [])
    return max(len(discovery), len(utility), len(transfer), int(skill.reuse_count or 0))


def detect_premature_skill(
    skill: Skill, config: SkillRobustnessConfig | None = None
) -> bool:
    """True when evidence/confidence/transfer floors are not met."""
    config = config or SkillRobustnessConfig()
    conf = float((skill.metadata or {}).get("confidence", 0.0) or 0.0)
    evidence = _evidence_count(skill)
    ts = float(skill.transfer_score or 0.0)
    if evidence < int(config.min_evidence_promote):
        return True
    if conf < float(config.min_confidence_promote):
        return True
    if ts < 0.1 and evidence < int(config.min_evidence_promote) + 1:
        return True
    return False


def demote_skill(skill: Skill, library: SkillLibrary | None = None) -> Skill:
    """Active-tier → PROMOTED → CANDIDATE for requalification.

    CORE skills are capability anchors and are not demoted by SF1 recovery.
    """
    del library  # library kept for API symmetry; skill mutated in place
    if skill.state is SkillState.CORE:
        return skill
    active_tier = {
        SkillState.ACTIVE,
        SkillState.GROWING,
    }
    if skill.state in active_tier:
        skill.transition_to(SkillState.PROMOTED)
    if skill.state is SkillState.PROMOTED:
        skill.transition_to(SkillState.CANDIDATE)
    append_biography_event(
        skill, "failure", {"kind": "demote", "state": skill.state.value}
    )
    meta = dict(skill.metadata or {})
    meta["demoted"] = True
    skill.metadata = meta
    return skill


def should_restrict_skill_promotion(
    ser: float, config: SkillRobustnessConfig | None = None
) -> bool:
    config = config or SkillRobustnessConfig()
    return float(ser) >= float(config.ser_restrict)


def ser_level(
    skills: int, validated_invariants: int, config: SkillRobustnessConfig | None = None
) -> str:
    """Return ok | warn | restrict for SER."""
    config = config or SkillRobustnessConfig()
    ser = skill_explosion_ratio(skills, validated_invariants)
    if ser >= config.ser_restrict:
        return "restrict"
    if ser >= config.ser_warn:
        return "warn"
    return "ok"


def enforce_library_capacity(
    library: SkillLibrary,
    config: SkillRobustnessConfig | None = None,
) -> list[Skill]:
    """Retire weakest live skills until live count ≤ capacity. Returns retired."""
    config = config or SkillRobustnessConfig()
    capacity = int(config.library_capacity)

    def _live() -> list[Skill]:
        return [
            s
            for s in library.list_skills()
            if s.state not in (SkillState.RETIRED, SkillState.ARCHIVED)
        ]

    skills = _live()
    if len(skills) <= capacity:
        return []
    # Prefer non-core, low utility first.
    ranked = sorted(
        skills,
        key=lambda s: (
            s.state is SkillState.CORE,
            float(s.utility or 0.0),
            int(s.reuse_count or 0),
            s.skill_id,
        ),
    )
    retired: list[Skill] = []
    for skill in ranked:
        if len(_live()) <= capacity:
            break
        if skill.state in (SkillState.RETIRED, SkillState.ARCHIVED, SkillState.CORE):
            continue
        # Walk to retired when possible.
        if skill.state in (
            SkillState.ACTIVE,
            SkillState.GROWING,
            SkillState.PROMOTED,
            SkillState.DORMANT,
            SkillState.CANDIDATE,
        ):
            skill.transition_to(SkillState.RETIRED)
            retired.append(skill)
            append_biography_event(skill, "retired", {"reason": "capacity"})
    return retired


def detect_duplicates(
    skill: Skill,
    library: SkillLibrary,
    config: SkillRobustnessConfig | None = None,
) -> list[tuple[Skill, float]]:
    """Similar live skills; retired/archived corpses and empty signatures ignored."""
    config = config or SkillRobustnessConfig()
    sig = [str(t) for t in (skill.trigger_conditions or []) if str(t).strip()]
    if not sig:
        return []
    hits = library.find_similar(sig, float(config.duplicate_similarity))
    return [
        (s, score)
        for s, score in hits
        if s.skill_id != skill.skill_id
        and s.state not in (SkillState.RETIRED, SkillState.ARCHIVED)
    ]


def merge_skills(
    keep: Skill,
    drop: Skill,
    library: SkillLibrary,
) -> Skill:
    """Consolidate histories into keep; retire drop."""
    keep.reuse_history = list(keep.reuse_history or []) + list(drop.reuse_history or [])
    keep.transfer_history = list(keep.transfer_history or []) + list(
        drop.transfer_history or []
    )
    keep.reuse_count = int(keep.reuse_count or 0) + int(drop.reuse_count or 0)
    meta = dict(keep.metadata or {})
    merged = list(meta.get("merged_from") or [])
    merged.append(drop.skill_id)
    meta["merged_from"] = merged
    keep.metadata = meta
    append_biography_event(
        keep, "growth", {"kind": "merge", "from": drop.skill_id}
    )
    if drop.state not in (SkillState.RETIRED, SkillState.ARCHIVED):
        if drop.state is SkillState.CANDIDATE:
            drop.transition_to(SkillState.RETIRED)
        elif drop.state is SkillState.PROMOTED:
            drop.transition_to(SkillState.RETIRED)
        elif drop.state in (
            SkillState.ACTIVE,
            SkillState.GROWING,
            SkillState.CORE,
            SkillState.DORMANT,
        ):
            drop.transition_to(SkillState.RETIRED)
    append_biography_event(drop, "retired", {"reason": "merged_into", "keep": keep.skill_id})
    # Ensure both remain in library (retired ≠ deleted).
    if library.get(keep.skill_id) is None:
        library.add(keep)
    if library.get(drop.skill_id) is None:
        library.add(drop)
    return keep
