"""Tests for ReasoningTrace and related types."""

import pytest

from core import (
    InvalidStateTransitionError,
    ReasoningStep,
    ReasoningTrace,
    TraceLifecyclePhase,
    TraceOutcome,
)


def _sample_trace() -> ReasoningTrace:
    steps = [
        ReasoningStep(step_id="s1", operation="detect_object", cost=1.0, duration=0.1),
        ReasoningStep(
            step_id="s2",
            operation="apply_reflection",
            cost=2.0,
            duration=0.2,
            dependencies=["s1"],
        ),
    ]
    return ReasoningTrace(
        trace_id="tr1",
        task_id="t1",
        timestamp=1.0,
        steps=steps,
        outcome=TraceOutcome(success=True, result="ok", cost=0.5),
    )


def test_trace_total_cost_and_operations():
    trace = _sample_trace()
    assert trace.total_cost == 3.0
    assert trace.operations == ["detect_object", "apply_reflection"]


def test_trace_legal_phase_transitions():
    trace = _sample_trace()
    assert trace.phase == TraceLifecyclePhase.CREATED
    trace.transition_to(TraceLifecyclePhase.STORED)
    trace.transition_to(TraceLifecyclePhase.USED_FOR_MINING)
    trace.transition_to(TraceLifecyclePhase.ARCHIVED)
    assert trace.phase == TraceLifecyclePhase.ARCHIVED


def test_trace_illegal_phase_transition():
    trace = _sample_trace()
    with pytest.raises(InvalidStateTransitionError):
        trace.transition_to(TraceLifecyclePhase.ARCHIVED)


def test_trace_dict_round_trip():
    trace = _sample_trace()
    restored = ReasoningTrace.from_dict(trace.to_dict())
    assert restored.trace_id == trace.trace_id
    assert restored.operations == trace.operations
    assert restored.outcome is not None
    assert restored.outcome.success is True
    assert restored.phase == TraceLifecyclePhase.CREATED


def test_step_rejects_negative_cost():
    with pytest.raises(ValueError, match="cost"):
        ReasoningStep(step_id="s1", operation="x", cost=-1)
