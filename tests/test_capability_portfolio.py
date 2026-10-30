"""Portfolio aggregates and sync into CapabilityState."""

from capability import (
    Capability,
    CapabilityLibrary,
    CapabilityLifecycle,
    CapabilityType,
    compute_capability_portfolio,
    sync_capability_state,
)
from core import CapabilityState, Skill, SkillState
from skills import SkillLibrary


def test_portfolio_and_sync():
    skills = SkillLibrary()
    skills.add(
        Skill(
            skill_id="s1",
            state=SkillState.ACTIVE,
            utility=0.5,
            transfer_score=0.5,
            transfer_history=[{"target_family": "geo", "success": True}],
            metadata={"mvp_category": "geo", "utility_breakdown": {"su": 0.5}},
        )
    )
    caps = CapabilityLibrary()
    caps.add(
        Capability(
            capability_id="core-cap",
            skill_ids=["s1"],
            state=CapabilityLifecycle.CORE,
            capability_type=CapabilityType.ATOMIC,
        )
    )
    caps.add(
        Capability(
            capability_id="emergent-cap",
            skill_ids=["s1"],
            state=CapabilityLifecycle.DEVELOPING,
            capability_type=CapabilityType.EMERGENT,
        )
    )
    port = compute_capability_portfolio(caps, skills)
    assert port.n == 2
    assert port.core_count == 1
    assert port.emergent_count == 1
    assert port.mean_capu >= 0.0

    state = CapabilityState(state_id="sys-1")
    sync_capability_state(state, port, ["core-cap", "emergent-cap"])
    assert state.growth_metrics["mean_capu"] == port.mean_capu
    assert state.growth_metrics["core_count"] == 1.0
    assert state.metadata["capability_ids"] == ["core-cap", "emergent-cap"]
