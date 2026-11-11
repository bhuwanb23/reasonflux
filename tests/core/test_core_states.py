"""Tests for lifecycle transition tables."""

import pytest

from core import (
    CAPABILITY_PHASE_TRANSITIONS,
    INVARIANT_TRANSITIONS,
    SKILL_TRANSITIONS,
    TRACE_PHASE_TRANSITIONS,
    InvalidStateTransitionError,
    InvariantState,
    SkillState,
    SystemCapabilityPhase,
    TraceLifecyclePhase,
    assert_transition,
    can_transition,
)


def test_skill_happy_path():
    assert can_transition(SkillState.CANDIDATE, SkillState.PROMOTED, SKILL_TRANSITIONS)
    assert can_transition(SkillState.PROMOTED, SkillState.ACTIVE, SKILL_TRANSITIONS)
    assert can_transition(SkillState.ACTIVE, SkillState.GROWING, SKILL_TRANSITIONS)
    assert can_transition(SkillState.GROWING, SkillState.CORE, SKILL_TRANSITIONS)
    assert can_transition(SkillState.ACTIVE, SkillState.DORMANT, SKILL_TRANSITIONS)
    assert can_transition(SkillState.DORMANT, SkillState.ACTIVE, SKILL_TRANSITIONS)
    assert can_transition(SkillState.ACTIVE, SkillState.RETIRED, SKILL_TRANSITIONS)
    assert can_transition(SkillState.RETIRED, SkillState.ARCHIVED, SKILL_TRANSITIONS)


def test_skill_fsm_allows_reactivation_path():
    """FSM permits RETIRED/ARCHIVED → ACTIVE; evidence gates are in reactivate_skill."""
    assert can_transition(SkillState.RETIRED, SkillState.ACTIVE, SKILL_TRANSITIONS)
    assert can_transition(SkillState.ARCHIVED, SkillState.ACTIVE, SKILL_TRANSITIONS)
    assert_transition(
        SkillState.RETIRED, SkillState.ACTIVE, SKILL_TRANSITIONS, "skill"
    )


def test_skill_fsm_allows_demotion_path():
    """Phase 11D-5: active-tier → PROMOTED → CANDIDATE demotion."""
    for state in (SkillState.ACTIVE, SkillState.GROWING, SkillState.CORE):
        assert can_transition(state, SkillState.PROMOTED, SKILL_TRANSITIONS)
    assert can_transition(SkillState.PROMOTED, SkillState.CANDIDATE, SKILL_TRANSITIONS)
    # No shortcut from active-tier straight to CANDIDATE.
    assert not can_transition(SkillState.ACTIVE, SkillState.CANDIDATE, SKILL_TRANSITIONS)


def test_invariant_happy_path():
    assert can_transition(
        InvariantState.DETECTED, InvariantState.VALIDATED, INVARIANT_TRANSITIONS
    )
    assert can_transition(
        InvariantState.VALIDATED, InvariantState.STRONG, INVARIANT_TRANSITIONS
    )
    assert can_transition(
        InvariantState.STRONG, InvariantState.ARCHIVED, INVARIANT_TRANSITIONS
    )


def test_invariant_cannot_skip_to_strong():
    assert not can_transition(
        InvariantState.DETECTED, InvariantState.STRONG, INVARIANT_TRANSITIONS
    )


def test_capability_and_trace_tables():
    assert can_transition(
        SystemCapabilityPhase.COLD_START,
        SystemCapabilityPhase.EMERGING_SKILLS,
        CAPABILITY_PHASE_TRANSITIONS,
    )
    assert can_transition(
        TraceLifecyclePhase.CREATED,
        TraceLifecyclePhase.STORED,
        TRACE_PHASE_TRANSITIONS,
    )
    assert not can_transition(
        TraceLifecyclePhase.CREATED,
        TraceLifecyclePhase.USED_FOR_MINING,
        TRACE_PHASE_TRANSITIONS,
    )
