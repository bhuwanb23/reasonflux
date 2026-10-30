"""ReasoningTrace — raw learning material for ASFT (Phase 11B-1 Object 2)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from core.states import (
    TRACE_PHASE_TRANSITIONS,
    TraceLifecyclePhase,
    assert_transition,
)


@dataclass(slots=True)
class ReasoningStep:
    """A single cognitive operation within a reasoning trace."""

    step_id: str
    operation: str
    inputs: list[Any] = field(default_factory=list)
    outputs: list[Any] = field(default_factory=list)
    cost: float = 0.0
    duration: float = 0.0
    dependencies: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.step_id:
            raise ValueError("step_id must be non-empty")
        if not self.operation:
            raise ValueError("operation must be non-empty")
        if self.cost < 0:
            raise ValueError("cost must be >= 0")
        if self.duration < 0:
            raise ValueError("duration must be >= 0")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ReasoningStep:
        return cls(
            step_id=data["step_id"],
            operation=data["operation"],
            inputs=list(data.get("inputs") or []),
            outputs=list(data.get("outputs") or []),
            cost=float(data.get("cost", 0.0)),
            duration=float(data.get("duration", 0.0)),
            dependencies=list(data.get("dependencies") or []),
        )


@dataclass(slots=True)
class TraceOutcome:
    """Outcome of a traced task attempt."""

    success: bool
    result: Any = None
    cost: float = 0.0

    def __post_init__(self) -> None:
        if self.cost < 0:
            raise ValueError("outcome cost must be >= 0")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TraceOutcome:
        return cls(
            success=bool(data["success"]),
            result=data.get("result"),
            cost=float(data.get("cost", 0.0)),
        )


@dataclass(slots=True)
class ReasoningTrace:
    """Structured record of how a task was solved.

    Invariant Detector contracts consume traces only — not raw Tasks.
    """

    trace_id: str
    task_id: str
    timestamp: float
    steps: list[ReasoningStep] = field(default_factory=list)
    outcome: TraceOutcome | None = None
    invariant_ids: list[str] = field(default_factory=list)
    skill_ids: list[str] = field(default_factory=list)
    phase: TraceLifecyclePhase = TraceLifecyclePhase.CREATED
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.trace_id:
            raise ValueError("trace_id must be non-empty")
        if not self.task_id:
            raise ValueError("task_id must be non-empty")
        if self.timestamp < 0:
            raise ValueError("timestamp must be >= 0")
        if not isinstance(self.phase, TraceLifecyclePhase):
            self.phase = TraceLifecyclePhase(self.phase)

    @property
    def total_cost(self) -> float:
        step_cost = sum(s.cost for s in self.steps)
        outcome_cost = self.outcome.cost if self.outcome else 0.0
        return step_cost if step_cost > 0 else outcome_cost

    @property
    def operations(self) -> list[str]:
        return [s.operation for s in self.steps]

    def transition_to(self, new_phase: TraceLifecyclePhase) -> None:
        assert_transition(self.phase, new_phase, TRACE_PHASE_TRANSITIONS, "trace")
        self.phase = new_phase

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "task_id": self.task_id,
            "timestamp": self.timestamp,
            "steps": [s.to_dict() for s in self.steps],
            "outcome": self.outcome.to_dict() if self.outcome else None,
            "invariant_ids": list(self.invariant_ids),
            "skill_ids": list(self.skill_ids),
            "phase": self.phase.value,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ReasoningTrace:
        outcome_raw = data.get("outcome")
        return cls(
            trace_id=data["trace_id"],
            task_id=data["task_id"],
            timestamp=float(data["timestamp"]),
            steps=[ReasoningStep.from_dict(s) for s in data.get("steps") or []],
            outcome=TraceOutcome.from_dict(outcome_raw) if outcome_raw else None,
            invariant_ids=list(data.get("invariant_ids") or []),
            skill_ids=list(data.get("skill_ids") or []),
            phase=TraceLifecyclePhase(data.get("phase", TraceLifecyclePhase.CREATED.value)),
            metadata=dict(data.get("metadata") or {}),
        )
