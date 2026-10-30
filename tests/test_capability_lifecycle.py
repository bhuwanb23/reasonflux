"""Capability lifecycle FSM and advance()."""

import pytest

from capability import (
    Capability,
    CapabilityConfig,
    CapabilityLifecycle,
    InvalidCapabilityTransitionError,
    advance_capability,
    assert_capability_transition,
    can_capability_transition,
    seed_from_skills,
)
from core import Skill, SkillState
from skills import SkillLibrary


def test_transition_table_happy_path():
    assert can_capability_transition(
        CapabilityLifecycle.EMERGING, CapabilityLifecycle.DEVELOPING
    )
    assert can_capability_transition(
        CapabilityLifecycle.ESTABLISHED, CapabilityLifecycle.CORE
    )
    with pytest.raises(InvalidCapabilityTransitionError):
        assert_capability_transition(
            CapabilityLifecycle.ARCHIVED, CapabilityLifecycle.CORE
        )


def test_advance_emerging_to_developing_with_transfer():
    lib = SkillLibrary()
    lib.add(
        Skill(
            skill_id="reflect",
            state=SkillState.ACTIVE,
            transfer_score=0.8,
            utility=0.5,
            transfer_history=[{"success": True, "target_family": "geo"}],
            metadata={"mvp_category": "reflection", "composition_potential": 0.5},
        )
    )
    cap = Capability(capability_id="c1", skill_ids=["reflect"])
    seed_from_skills(cap, lib)
    cfg = CapabilityConfig(min_utility=0.0, min_transfer_events=1)
    advance_capability(cap, library=lib, config=cfg, previous_utility=0.0)
    assert cap.state in (
        CapabilityLifecycle.DEVELOPING,
        CapabilityLifecycle.ESTABLISHED,
        CapabilityLifecycle.CORE,
    )
    assert cap.state is not CapabilityLifecycle.EMERGING


def test_ghost_cannot_establish_without_transfer():
    lib = SkillLibrary()
    lib.add(
        Skill(
            skill_id="lonely",
            state=SkillState.ACTIVE,
            transfer_score=0.0,
            utility=0.5,
            metadata={"mvp_category": "reflection", "composition_potential": 0.5},
        )
    )
    cap = Capability(
        capability_id="ghost",
        skill_ids=["lonely"],
        state=CapabilityLifecycle.DEVELOPING,
        confidence=0.9,
        coverage=0.9,
    )
    cfg = CapabilityConfig(min_transfer_events=1, min_confidence=0.3, min_coverage=0.1)
    advance_capability(cap, library=lib, config=cfg)
    assert cap.state is CapabilityLifecycle.DEVELOPING
