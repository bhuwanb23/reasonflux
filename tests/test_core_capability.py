"""Tests for CapabilityState."""

import pytest

from core import (
    CapabilityState,
    InvalidStateTransitionError,
    SystemCapabilityPhase,
)


def test_capability_phase_transitions():
    state = CapabilityState(state_id="cap-1", skill_ids=["SK-1"])
    assert state.phase == SystemCapabilityPhase.COLD_START
    state.transition_to(SystemCapabilityPhase.EMERGING_SKILLS)
    state.transition_to(SystemCapabilityPhase.TRANSFER_ENABLED)
    state.transition_to(SystemCapabilityPhase.CAPABILITY_GROWTH)
    with pytest.raises(InvalidStateTransitionError):
        state.transition_to(SystemCapabilityPhase.COLD_START)


def test_capability_snapshot_appends_history():
    state = CapabilityState(
        state_id="cap-1",
        transfer_metrics={"TS": 0.4},
        growth_metrics={"CGR": 0.1},
        timestamp=10.0,
    )
    snap = state.snapshot()
    assert snap["transfer_metrics"]["TS"] == 0.4
    assert len(state.history) == 1


def test_capability_dict_round_trip():
    state = CapabilityState(
        state_id="cap-2",
        skill_ids=["a", "b"],
        phase=SystemCapabilityPhase.EMERGING_SKILLS,
        transfer_metrics={"TS": 1.0},
        growth_metrics={"IG": 0.2},
    )
    restored = CapabilityState.from_dict(state.to_dict())
    assert restored.phase == SystemCapabilityPhase.EMERGING_SKILLS
    assert restored.skill_ids == ["a", "b"]
    assert restored.growth_metrics["IG"] == pytest.approx(0.2)
