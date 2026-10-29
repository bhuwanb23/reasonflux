"""Library-wide skill robustness audit (Phase 11D-5)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from core.skill import Skill
from skills.library import SkillLibrary
from skills.robustness.config import SkillRobustnessConfig
from skills.robustness.edge_cases import enforce_zombie_archive, is_ancient_core
from skills.robustness.metrics import skill_explosion_ratio, skill_ntr
from skills.robustness.recovery import RecoveryAction, apply_recovery, plan_recovery
from skills.robustness.sf_capability import detect_capability_collapse
from skills.robustness.sf_creation import (
    detect_duplicates,
    detect_premature_skill,
    enforce_library_capacity,
)
from skills.robustness.sf_transfer import apply_transfer_health, assess_negative_transfer
from skills.robustness.taxonomy import FailureDiagnosis, diagnose_skill


@dataclass(slots=True)
class LibraryAuditReport:
    skill_findings: dict[str, list[FailureDiagnosis]] = field(default_factory=dict)
    actions: list[RecoveryAction] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    collapsed: bool = False
    retired: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_findings": {
                k: [d.to_dict() for d in v]
                for k, v in self.skill_findings.items()
            },
            "actions": [a.to_dict() for a in self.actions],
            "metrics": dict(self.metrics),
            "collapsed": self.collapsed,
            "retired": list(self.retired),
        }


def audit_library(
    library: SkillLibrary,
    *,
    config: SkillRobustnessConfig | None = None,
    asu_series: Sequence[float] | None = None,
    families: Sequence[str] | None = None,
    validated_invariants: int = 1,
    apply: bool = False,
) -> LibraryAuditReport:
    """One pass over skills: diagnose SF modes, optionally apply recoveries."""
    config = config or SkillRobustnessConfig()
    report = LibraryAuditReport()
    skills = list(library.list_skills())
    ser = skill_explosion_ratio(len(skills), validated_invariants)
    report.metrics["ser"] = ser
    report.metrics["skill_count"] = len(skills)

    if asu_series is not None:
        collapse = detect_capability_collapse(asu_series, config)
        report.collapsed = collapse.collapsed
        report.metrics["collapse"] = collapse.to_dict()

    action_budget = int(config.audit_max_actions)
    for skill in skills:
        premature = detect_premature_skill(skill, config)
        dups = detect_duplicates(skill, library, config)
        ntr = skill_ntr(skill)
        zombie = bool((skill.metadata or {}).get("zombie")) or (
            int((skill.metadata or {}).get("reactivations", 0) or 0)
            >= config.zombie_permanent_archive_attempts
            and not bool(
                ((skill.metadata or {}).get("last_reactivation") or {}).get(
                    "raised_utility", False
                )
            )
        )
        ancient = is_ancient_core(skill, config)
        diagnoses = diagnose_skill(
            skill,
            config=config,
            ser=ser,
            ntr=ntr,
            is_duplicate=bool(dups),
            is_premature=premature,
            is_zombie=zombie,
            is_ancient_core=ancient,
        )
        if diagnoses:
            report.skill_findings[skill.skill_id] = diagnoses

        if not apply or action_budget <= 0:
            continue

        # Prefer transfer health and premature demotion.
        health = assess_negative_transfer(skill, config)
        if health.action != "none" and action_budget > 0:
            apply_transfer_health(skill, health, library)
            action = plan_recovery(diagnoses[0], config) if diagnoses else None
            if action:
                report.actions.append(action)
            action_budget -= 1
            if skill.state.value == "retired":
                report.retired.append(skill.skill_id)
            continue

        if premature and action_budget > 0 and not ancient:
            action = plan_recovery(diagnoses[0], config) if diagnoses else None
            if action and action.action == "demote":
                apply_recovery(skill, action, library, config)
                report.actions.append(action)
                action_budget -= 1
                continue

        if zombie and action_budget > 0:
            if enforce_zombie_archive(skill, config):
                from skills.robustness.taxonomy import SkillFailure

                action = RecoveryAction(
                    "archive", SkillFailure.EC3, "archived", ["zombie"]
                )
                report.actions.append(action)
                action_budget -= 1

    if apply:
        retired = enforce_library_capacity(library, config)
        report.retired.extend(s.skill_id for s in retired)
        report.metrics["skill_count_after"] = len(library)

    return report
