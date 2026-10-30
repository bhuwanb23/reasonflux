"""Composition necessity trigger — compose only when SC < TR (Phase 11D-4)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from core.skill import Skill
from skills.config import SkillConfig


def _norm_set(items: Sequence[str]) -> set[str]:
    return {str(x).lower().strip() for x in items if str(x).strip()}


def skill_coverage(skill: Skill, requirements: Sequence[str]) -> float:
    """Fraction of task requirements covered by skill trigger_conditions."""
    req = _norm_set(requirements)
    if not req:
        return 1.0
    triggers = _norm_set(skill.trigger_conditions or [])
    if not triggers:
        return 0.0
    return len(req & triggers) / len(req)


def covers_all(skill: Skill, requirements: Sequence[str]) -> bool:
    req = _norm_set(requirements)
    if not req:
        return True
    return req <= _norm_set(skill.trigger_conditions or [])


@dataclass(slots=True)
class ComposeTriggerResult:
    """Whether composition should be attempted for a task."""

    should_compose: bool
    reasons: list[str] = field(default_factory=list)
    uncovered: list[str] = field(default_factory=list)
    best_single_coverage: float = 0.0
    covering_skill_id: str | None = None

    def to_dict(self) -> dict:
        return {
            "should_compose": self.should_compose,
            "reasons": list(self.reasons),
            "uncovered": list(self.uncovered),
            "best_single_coverage": self.best_single_coverage,
            "covering_skill_id": self.covering_skill_id,
        }


def should_compose(
    task_requirements: Sequence[str],
    skills: Sequence[Skill],
    config: SkillConfig | None = None,
) -> ComposeTriggerResult:
    """Compose only when no individual skill covers all requirements."""
    del config  # reserved for future coverage thresholds
    req = _norm_set(task_requirements)
    if not req:
        return ComposeTriggerResult(
            should_compose=False,
            reasons=["empty_requirements"],
        )
    if not skills:
        return ComposeTriggerResult(
            should_compose=False,
            reasons=["no_skills"],
            uncovered=sorted(req),
        )

    best = 0.0
    best_id: str | None = None
    for skill in skills:
        cov = skill_coverage(skill, task_requirements)
        if cov > best:
            best = cov
            best_id = skill.skill_id
        if covers_all(skill, task_requirements):
            return ComposeTriggerResult(
                should_compose=False,
                reasons=["single_skill_covers"],
                uncovered=[],
                best_single_coverage=1.0,
                covering_skill_id=skill.skill_id,
            )

    # Uncovered relative to union of all skills (informational).
    union: set[str] = set()
    for skill in skills:
        union |= _norm_set(skill.trigger_conditions or [])
    uncovered = sorted(req - union)
    return ComposeTriggerResult(
        should_compose=True,
        reasons=["sc_lt_tr"],
        uncovered=uncovered if uncovered else sorted(req),
        best_single_coverage=best,
        covering_skill_id=best_id,
    )
