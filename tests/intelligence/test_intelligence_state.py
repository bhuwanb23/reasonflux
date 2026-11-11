"""Tests for IntelligenceState construction from capability snapshots."""

from capability import (
    Capability,
    CapabilityLibrary,
    compute_capability_portfolio,
    sync_capability_state,
)
from core import CapabilityState, Skill, SkillState
from evaluation import compute_system_intelligence_state
from skills import SkillLibrary


def _geo_setup():
    skills = SkillLibrary()
    skills.add(
        Skill(
            skill_id="s1",
            state=SkillState.ACTIVE,
            utility=0.5,
            transfer_score=0.4,
            transfer_history=[{"target_family": "geo", "success": True}],
            metadata={
                "mvp_category": "geo",
                "utility_breakdown": {"su": 0.5},
            },
        )
    )
    caps = CapabilityLibrary()
    caps.add(Capability(capability_id="cap1", skill_ids=["s1"], utility=0.5))
    return caps, skills


def test_system_intelligence_state_basic():
    caps, skills = _geo_setup()
    state = compute_system_intelligence_state(
        caps, skills, experiences=10, new_families=1
    )
    assert hasattr(state, "ig")
    assert hasattr(state, "igr")
    assert state.portfolio is not None
    assert state.portfolio.n == len(caps)
    assert state.stage in (
        "emerging",
        "developing",
        "generalizing",
        "compositional",
        "adaptive",
    )


def test_write_intel_opt_in_sync():
    caps, skills = _geo_setup()
    intel = compute_system_intelligence_state(caps, skills, experiences=5)
    port = compute_capability_portfolio(caps, skills)
    state = CapabilityState(state_id="sys")
    sync_capability_state(
        state, port, ["cap1"], intel=intel, write_intel=True
    )
    assert state.growth_metrics["ig"] == intel.ig
    assert state.growth_metrics["igr"] == intel.igr
    assert state.metadata["intelligence_stage"] == intel.stage
