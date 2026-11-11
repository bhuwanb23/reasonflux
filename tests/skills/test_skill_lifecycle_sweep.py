"""End-to-end library lifecycle sweep (Phase 11D-3)."""

from core import Skill, SkillState
from skills import (
    SkillConfig,
    SkillLibrary,
    evaluate_library_lifecycle,
    reactivate_skill,
    refresh_skill_utility,
    retrieve_skills,
)


def test_library_sweep_core_survives_weak_retires_dormant_preserved():
    cfg = SkillConfig(
        growing_ug=0.5,  # suppress incidental grow
        dormant_after_tasks=10,
        retire_low_su_periods=3,
        retire_min_age_tasks=20,
        retire_max_reuse=1,
        retire_max_ts=0.1,
        archive_after_tasks=100,
        core_su=0.3,
        su_min=0.0,
    )

    core = Skill(
        skill_id="core",
        abstraction_gain=0.9,
        transfer_score=0.8,
        creation_cost=0.05,
        reuse_count=6,
        reuse_history=[{"impact": 1.0}] * 6,
        transfer_history=[
            {"success": True, "target_family": f"f{i}"} for i in range(3)
        ],
        state=SkillState.CORE,
        metadata={
            "composition_potential": 0.6,
            "capability_anchor": True,
            "lifecycle": {"tasks_since_use": 0, "age_tasks": 30, "previous_su": 0.5},
        },
    )
    refresh_skill_utility(core)

    weak = Skill(
        skill_id="weak",
        abstraction_gain=0.0,
        transfer_score=0.0,
        creation_cost=1.0,
        reuse_count=0,
        state=SkillState.ACTIVE,
        metadata={
            "composition_potential": 0.0,
            "lifecycle": {
                "age_tasks": 25,
                "low_su_streak": 2,
                "tasks_since_use": 0,
            },
        },
    )
    refresh_skill_utility(weak)

    dormant = Skill(
        skill_id="dorm",
        abstraction_gain=0.5,
        transfer_score=0.4,
        creation_cost=0.05,
        reuse_count=2,
        state=SkillState.DORMANT,
        metadata={
            "composition_potential": 0.3,
            "lifecycle": {"tasks_since_use": 12, "age_tasks": 20},
        },
    )
    refresh_skill_utility(dormant)

    lib = SkillLibrary()
    for s in (core, weak, dormant):
        lib.add(s)

    result = evaluate_library_lifecycle(lib, task_clock=40, config=cfg)
    assert core.state is SkillState.CORE
    assert weak.state is SkillState.RETIRED
    assert "weak" in result.retired
    assert dormant.state is SkillState.DORMANT
    assert lib.get("weak") is weak  # retired ≠ deleted
    assert retrieve_skills(lib)  # core still retrievable

    # Reactivate dormant on new evidence
    revived = reactivate_skill(
        dormant,
        evidence_count=3,
        expected_su=0.4,
        config=cfg,
        task_clock=41,
    )
    assert revived.success
    assert dormant.state is SkillState.ACTIVE
