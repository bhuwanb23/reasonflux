"""Focused idle/dormancy/reactivation study, isolated from primary tasks."""
from __future__ import annotations

from statistics import mean
from typing import Any
from core.skill import Skill
from skills.config import SkillConfig
from skills.library import SkillLibrary
from skills.lifecycle.sweep import evaluate_library_lifecycle
from skills.reactivation import reactivate_skill
from solver.executor import GridSolver
from solver.tasks import FAMILIES, make_task
from transfer.reuse_engine import ReuseEngine
from .arms import _clone_skill


def _run_lifecycle(
    skill: Skill, run_seed: int, config: SkillConfig, *, probe_seed_offset: int
) -> dict[str, Any]:
    library = SkillLibrary()
    library.add(_clone_skill(skill))
    isolated = library.get(skill.skill_id)
    assert isolated is not None
    transitions = [{"task_clock": 0, "state": isolated.state.value, "action": "birth_or_validation"}]
    for clock in range(1, config.dormant_after_tasks + 1):
        result = evaluate_library_lifecycle(
            library, task_clock=clock + 10, config=config, tick_unused=True
        )
        transitions.append(
            {
                "task_clock": clock + 10,
                "state": isolated.state.value,
                "action": "idle_tick",
                "dormant": isolated.skill_id in result.dormant,
            }
        )
    dormant_state = isolated.state.value
    # Evidence is obtained on an isolated shadow copy before asking the lifecycle
    # gate to reactivate; those probes do not mutate the dormant original.
    shadow = _clone_skill(isolated)
    shadow.state = type(shadow.state).ACTIVE
    category = str((shadow.metadata or {}).get("mvp_category", "rotation"))
    probe_family = category if category in FAMILIES else "rotation"
    probe_tasks = [
        make_task(
            probe_family,
            seed=run_seed + probe_seed_offset + i,
            variant=i % 2,
            difficulty=0.2,
        )
        for i in range(2)
    ]
    probe_library = SkillLibrary()
    probe_library.add(shadow)
    engine = ReuseEngine(probe_library, solver=GridSolver(), config=config)
    probe = [engine.apply(task, task_clock=20 + i).to_dict() for i, task in enumerate(probe_tasks)]
    evidence_count = sum(bool(row["transfer_credit"]) for row in probe)
    expected_su = mean(float(row["benefit"]) for row in probe) if probe else 0.0
    from skills.reactivation import reactivate_skill
    react = reactivate_skill(
        isolated,
        evidence_count=evidence_count,
        expected_su=expected_su,
        config=config,
        task_clock=30,
    )
    transitions.append(
        {
            "task_clock": 30,
            "state": isolated.state.value,
            "action": "reactivation_attempt",
            "success": react.success,
            "evidence_count": evidence_count,
            "expected_su": expected_su,
            "probe_task_results": probe,
        }
    )
    return {
        "skill_id": isolated.skill_id,
        "state_before_idle": transitions[0]["state"],
        "state_after_idle": dormant_state,
        "dormant_observed": dormant_state == "dormant",
        "reactivation_succeeded": react.success,
        "final_state": isolated.state.value,
        "transitions": transitions,
    }
