"""Trace pipeline — tasks → solved traces → store (Phase 11, Phase A).

Exit gate for Phase A: a task batch produces traces that survive a save/load
round-trip.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence

from solver.executor import GridSolver
from solver.tasks import FAMILIES, GridTask, make_task_batch
from traces.logger import TraceLogger
from traces.trace_store import TraceStore

__all__ = ["TracePipelineResult", "run_trace_pipeline"]


@dataclass(slots=True)
class TracePipelineResult:
    """Outcome of producing and persisting traces."""

    traces: list[Any] = field(default_factory=list)
    tasks: list[GridTask] = field(default_factory=list)
    store_root: str = ""
    success_count: int = 0
    failure_count: int = 0
    families: list[str] = field(default_factory=list)

    @property
    def n_traces(self) -> int:
        return len(self.traces)

    def to_dict(self) -> dict[str, Any]:
        return {
            "n_traces": self.n_traces,
            "n_tasks": len(self.tasks),
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "families": list(self.families),
            "store_root": self.store_root,
            "trace_ids": [t.trace_id for t in self.traces],
        }


def run_trace_pipeline(
    families: Sequence[str] = FAMILIES,
    *,
    per_family: int = 4,
    seed: int = 0,
    difficulty: float = 0.3,
    store: TraceStore | None = None,
    store_root: str | Path | None = None,
    persist: bool = True,
    solver: GridSolver | None = None,
) -> TracePipelineResult:
    """Generate tasks, solve them, log traces, and optionally persist."""
    solver = solver or GridSolver()
    logger = TraceLogger()

    tasks = make_task_batch(
        tuple(families), per_family=per_family, seed=seed, difficulty=difficulty
    )
    pairs = [(task.to_task(), solver.solve(task)) for task in tasks]
    traces = logger.log_batch(pairs)

    if persist:
        target = store or TraceStore(store_root or "reports/traces")
        target.save_many(traces)
        root = str(target.root)
    else:
        root = str(store.root) if store is not None else ""

    return TracePipelineResult(
        traces=traces,
        tasks=tasks,
        store_root=root,
        success_count=sum(1 for t in traces if t.outcome and t.outcome.success),
        failure_count=sum(1 for t in traces if not (t.outcome and t.outcome.success)),
        families=sorted({t.task_family for t in tasks}),
    )
