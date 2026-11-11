"""End-to-end intelligence flow: capability → IG → IGR/IA → audit."""

from capability import Capability, CapabilityLibrary, sync_capability_state
from core import CapabilityState, Skill, SkillState
from evaluation import (
    audit_intelligence,
    build_growth_evidence,
    compute_system_intelligence_state,
)
from skills import SkillLibrary


def test_intelligence_e2e_growth_and_audit():
    skills0 = SkillLibrary()
    skills0.add(
        Skill(
            skill_id="s1",
            state=SkillState.ACTIVE,
            utility=0.4,
            transfer_score=0.3,
            transfer_history=[{"target_family": "geo", "success": True}],
            metadata={
                "mvp_category": "geo",
                "utility_breakdown": {"su": 0.4},
            },
        )
    )
    caps = CapabilityLibrary()
    caps.add(Capability(capability_id="geo", skill_ids=["s1"], utility=0.4))

    snap0 = compute_system_intelligence_state(
        caps, skills0, experiences=5, new_families=1
    )

    skills1 = SkillLibrary()
    skills1.add(
        Skill(
            skill_id="s1",
            state=SkillState.ACTIVE,
            utility=0.8,
            transfer_score=0.7,
            transfer_history=[
                {"target_family": "geo", "success": True},
                {"target_family": "algebra", "success": True},
            ],
            metadata={
                "mvp_category": "geo",
                "utility_breakdown": {"su": 0.8},
                "composed_from": ["a", "b"],
            },
        )
    )
    skills1.add(
        Skill(
            skill_id="s2",
            state=SkillState.ACTIVE,
            utility=0.6,
            transfer_score=0.5,
            transfer_history=[{"target_family": "algebra", "success": True}],
            metadata={
                "mvp_category": "rotation",
                "utility_breakdown": {"su": 0.6},
            },
        )
    )
    caps.get("geo").add_skill("s2")
    caps.get("geo").utility = 0.8

    snap1 = compute_system_intelligence_state(
        caps,
        skills1,
        previous_intel=snap0,
        previous_capability_score=snap0.portfolio.capability_score if snap0.portfolio else 0.0,
        experiences=10,
        new_families=1,
        ad=0.2,
    )
    assert snap1.ig >= snap0.ig or snap1.igr != 0.0

    # Zero / flat then negative trajectory via weaker skills
    skills_weak = SkillLibrary()
    skills_weak.add(
        Skill(
            skill_id="s1",
            state=SkillState.ACTIVE,
            utility=0.05,
            transfer_score=0.05,
            transfer_history=[{"target_family": "geo", "success": True}],
            metadata={"utility_breakdown": {"su": 0.05}, "mvp_category": "geo"},
        )
    )
    weak_caps = CapabilityLibrary()
    weak_caps.add(Capability(capability_id="geo", skill_ids=["s1"], utility=0.05))
    snap_down = compute_system_intelligence_state(
        weak_caps,
        skills_weak,
        previous_intel=snap1,
        previous_capability_score=(
            snap1.portfolio.capability_score if snap1.portfolio else 0.0
        ),
        experiences=12,
    )
    assert snap_down.igr <= snap1.igr

    ev = build_growth_evidence(
        new_skills=1,
        transfer_events=2,
        coverage_expansion=0.1,
        utility_improvement=0.4,
        composition_growth=1.0,
    )
    res = audit_intelligence(
        ig=snap1.ig,
        ig_delta=snap1.ig - snap0.ig,
        evidence=ev,
        extra_metrics={
            "skill_count": 2,
            "tg": 0.4,
            "ug": 0.4,
            "ccg": 0.1,
            "cgr": 0.05,
            "transfer_delta": 1.0,
            "composition_success_rate": 0.9,
            "new_families": 1,
            "elasticity": max(0.05, snap1.elasticity),
            "fragmentation": 0.1,
        },
    )
    assert res.ok

    state = CapabilityState(state_id="sys-intel")
    from capability import compute_capability_portfolio

    port = compute_capability_portfolio(caps, skills1)
    sync_capability_state(
        state, port, ["geo"], intel=snap1, write_intel=True, write_growth=False
    )
    assert "ig" in state.growth_metrics
    assert state.metadata.get("intelligence_stage") == snap1.stage
