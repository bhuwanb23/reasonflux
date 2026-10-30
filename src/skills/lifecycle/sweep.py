"""Library-wide lifecycle evaluation pass (Phase 11D-3)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.states import SkillState
from skills.config import SkillConfig
from skills.lifecycle.aging import note_task_tick
from skills.lifecycle.apply import apply_lifecycle
from skills.lifecycle.metrics import LifecycleMetrics, compute_lifecycle_metrics
from skills.lifecycle.policy import decide_lifecycle
from skills.library import SkillLibrary
from skills.portfolio import PortfolioMetrics, compute_portfolio_metrics


@dataclass(slots=True)
class LibraryLifecycleResult:
    """Summary of one evaluate_library_lifecycle pass."""

    changed: list[str] = field(default_factory=list)
    retired: list[str] = field(default_factory=list)
    archived: list[str] = field(default_factory=list)
    dormant: list[str] = field(default_factory=list)
    reactivated: list[str] = field(default_factory=list)
    growing: list[str] = field(default_factory=list)
    core: list[str] = field(default_factory=list)
    metrics: dict[str, LifecycleMetrics] = field(default_factory=dict)
    portfolio: PortfolioMetrics | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "changed": list(self.changed),
            "retired": list(self.retired),
            "archived": list(self.archived),
            "dormant": list(self.dormant),
            "reactivated": list(self.reactivated),
            "growing": list(self.growing),
            "core": list(self.core),
            "metrics": {k: v.to_dict() for k, v in self.metrics.items()},
            "portfolio": self.portfolio.to_dict() if self.portfolio else None,
        }


def evaluate_library_lifecycle(
    library: SkillLibrary,
    *,
    task_clock: int = 0,
    config: SkillConfig | None = None,
    previous_metrics: PortfolioMetrics | None = None,
    tick_unused: bool = True,
) -> LibraryLifecycleResult:
    """One pass over all skills: age ticks, decide, apply, portfolio trend."""
    config = config or SkillConfig()
    result = LibraryLifecycleResult()
    for skill in library.list_skills():
        life = dict((skill.metadata or {}).get("lifecycle") or {})
        # Skip idle tick when reuse already reset counter this period
        # (monitoring note_task_tick(used=True) sets last_used_clock).
        already_used = int(life.get("last_used_clock", -1) or -1) == int(task_clock)
        if (
            tick_unused
            and not already_used
            and skill.state
            in (SkillState.ACTIVE, SkillState.GROWING, SkillState.CORE)
        ):
            note_task_tick(skill, used=False)

        prev_su = None
        life = (skill.metadata or {}).get("lifecycle") or {}
        if "previous_su" in life:
            prev_su = float(life["previous_su"])

        decision = decide_lifecycle(
            skill, task_clock=task_clock, config=config, previous_su=prev_su
        )
        before = skill.state
        apply_lifecycle(skill, decision, config=config)
        snap = compute_lifecycle_metrics(
            skill, task_clock=task_clock, config=config, previous_su=prev_su
        )
        result.metrics[skill.skill_id] = snap

        if skill.state is not before or decision.action != "keep":
            if skill.state is not before:
                result.changed.append(skill.skill_id)
            if decision.action == "retire":
                result.retired.append(skill.skill_id)
            elif decision.action == "archive":
                result.archived.append(skill.skill_id)
            elif decision.action == "dormant":
                result.dormant.append(skill.skill_id)
            elif decision.action == "grow":
                result.growing.append(skill.skill_id)
            elif decision.action == "core":
                result.core.append(skill.skill_id)

    result.portfolio = compute_portfolio_metrics(
        library, previous=previous_metrics, config=config, refresh=True
    )
    return result
