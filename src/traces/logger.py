"""Trace Logger — capture solver reasoning into a ReasoningTrace (Phase 11).

Contribution support: IDT. This is the producer that Phase A was missing: it
turns a solved task into the durable learning material the miner consumes.
"""

from __future__ import annotations

import time
import uuid
from typing import Any

from core.states import TraceLifecyclePhase
from core.task import Task
from core.trace import ReasoningTrace, TraceOutcome
from solver.executor import SolveResult

__all__ = ["TraceLogger"]


class TraceLogger:
    """Capture solver steps into a ReasoningTrace."""

    def __init__(self, *, clock: Any = None) -> None:
        """``clock`` is injectable so tests get deterministic timestamps."""
        self._clock = clock or time.time
        self._counter = 0

    def _next_id(self, task_id: str) -> str:
        self._counter += 1
        return f"TR-{task_id}-{self._counter:04d}"

    def log(
        self,
        task: Task,
        result: SolveResult,
        *,
        trace_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ReasoningTrace:
        """Build a trace from a task and its solve result.

        The trace carries ``task_family`` in metadata because the miner is only
        allowed to see traces, never raw ``Task`` objects (Contract 1).
        """
        trace = ReasoningTrace(
            trace_id=trace_id or self._next_id(task.task_id),
            task_id=task.task_id,
            timestamp=float(self._clock()),
            steps=list(result.steps),
            outcome=TraceOutcome(
                success=bool(result.success),
                result=_serialise(result.output),
                cost=float(result.cost),
            ),
            metadata={
                "task_family": task.task_family,
                "difficulty": float(task.difficulty),
                "strategy": result.strategy,
                "step_count": result.step_count,
                **(result.metadata or {}),
                **(metadata or {}),
            },
        )
        trace.transition_to(TraceLifecyclePhase.STORED)
        return trace

    def log_batch(
        self,
        pairs: list[tuple[Task, SolveResult]],
        *,
        metadata: dict[str, Any] | None = None,
    ) -> list[ReasoningTrace]:
        """Log several (task, result) pairs at once."""
        return [self.log(t, r, metadata=metadata) for t, r in pairs]


def _serialise(value: Any) -> Any:
    if hasattr(value, "to_rows"):
        return value.to_rows()
    return value


def new_trace_id() -> str:
    """Random trace id for callers that do not use the logger counter."""
    return f"TR-{uuid.uuid4().hex[:12]}"
