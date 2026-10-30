"""E2E: geometric cluster from reflection+rotation; portfolio; ghost blocked."""

from capability import (
    Capability,
    CapabilityConfig,
    CapabilityLibrary,
    CapabilityLifecycle,
    CapabilityType,
    advance_capability,
    compute_capability_portfolio,
    detect_ghost,
    propose_capabilities_from_library,
    seed_from_skills,
    sync_capability_state,
    validate_capability,
)
from core import CapabilityState, Skill, SkillState
from skills import SkillLibrary


def test_geometric_cluster_portfolio_and_ghost_blocked():
    skills = SkillLibrary()
    for sid, cat, fam in (
        ("reflect", "reflection", "geo"),
        ("rotate", "rotation", "geo"),
        ("translate", "translation", "algebra"),
    ):
        skills.add(
            Skill(
                skill_id=sid,
                state=SkillState.ACTIVE,
                utility=0.55,
                transfer_score=0.5,
                reuse_count=3,
                transfer_history=[{"target_family": fam, "success": True}],
                metadata={
                    "mvp_category": cat,
                    "utility_breakdown": {"su": 0.55},
                    "composition_potential": 0.5,
                },
            )
        )
    skills.add(
        Skill(
            skill_id="geo-anchor",
            state=SkillState.CORE,
            utility=0.7,
            transfer_score=0.8,
            transfer_history=[{"target_family": "geo", "success": True}],
            metadata={
                "mvp_category": "reflection",
                "utility_breakdown": {"su": 0.7},
                "capability_anchor": True,
            },
        )
    )

    proposed = propose_capabilities_from_library(skills, require_valid=True)
    assert proposed
    # Multi-membership: reflection skills may appear in atomic + composite
    reflection_caps = [c for c in proposed if "reflect" in c.skill_ids or "geo-anchor" in c.skill_ids]
    assert reflection_caps

    cap_lib = CapabilityLibrary()
    for cap in proposed:
        if cap_lib.get(cap.capability_id) is None:
            cap_lib.add(cap)

    # Advance an emerging composite toward developing
    composite = next(
        (c for c in proposed if c.capability_type is CapabilityType.COMPOSITE),
        proposed[0],
    )
    cfg = CapabilityConfig(min_utility=0.0, min_transfer_events=1)
    if composite.state is CapabilityLifecycle.EMERGING:
        advance_capability(composite, library=skills, config=cfg, previous_utility=0.0)
        assert composite.state in (
            CapabilityLifecycle.DEVELOPING,
            CapabilityLifecycle.ESTABLISHED,
            CapabilityLifecycle.CORE,
        )

    port = compute_capability_portfolio(cap_lib, skills, cfg)
    assert port.n >= 1
    state = CapabilityState(state_id="sys-geo")
    sync_capability_state(
        state, port, [c.capability_id for c in cap_lib.list_capabilities()]
    )
    assert "mean_capu" in state.growth_metrics
    assert state.metadata.get("capability_ids")

    # Ghost blocked: no transfer → cannot validate / establish
    ghost_skill = Skill(
        skill_id="lonely",
        state=SkillState.ACTIVE,
        utility=0.9,
        metadata={"utility_breakdown": {"su": 0.9}, "mvp_category": "reflection"},
    )
    skills.add(ghost_skill)
    ghost = Capability(
        capability_id="ghost-cap",
        skill_ids=["lonely"],
        state=CapabilityLifecycle.DEVELOPING,
        confidence=0.99,
        coverage=0.99,
        utility=0.9,
    )
    assert not validate_capability(ghost, skills, cfg).valid
    assert detect_ghost(ghost, skills) is not None
    advance_capability(ghost, library=skills, config=cfg)
    assert ghost.state is not CapabilityLifecycle.ESTABLISHED
    assert ghost.state is not CapabilityLifecycle.CORE
