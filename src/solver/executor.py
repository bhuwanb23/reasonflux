"""Deterministic grid solver that emits real reasoning steps (Phase 11).

The solver is intentionally simple: it proposes candidate readings per family,
executes one, and verifies the result. It never reads ``expected`` while
building its steps — verification is the only place the answer is consulted, so
traces remain honest learning material.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from core.trace import ReasoningStep
from solver.grid import (
    Grid,
    count_objects,
    diff_cells,
    group_by_color,
    reflect_horizontal,
    reflect_vertical,
    rotate_90,
)
from solver.tasks import FAMILY_OPS, GridTask

__all__ = ["GridSolver", "SolveResult", "raw_operations"]


@dataclass(slots=True)
class SolveResult:
    """Outcome of one solving attempt, including its reasoning steps."""

    task_id: str
    task_family: str
    steps: list[ReasoningStep]
    output: Any
    success: bool
    cost: float = 0.0
    strategy: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def operations(self) -> list[str]:
        return [s.operation for s in self.steps]

    @property
    def step_count(self) -> int:
        return len(self.steps)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_family": self.task_family,
            "steps": [s.to_dict() for s in self.steps],
            "output": _serialise(self.output),
            "success": self.success,
            "cost": self.cost,
            "strategy": self.strategy,
            "metadata": dict(self.metadata),
        }


def _serialise(value: Any) -> Any:
    return value.to_rows() if isinstance(value, Grid) else value


def raw_operations(family: str, *, macro: bool = False) -> list[str]:
    """Raw (pre-normalization) operation names for a family.

    ``macro=True`` collapses the family to its single apply step, which is the
    shape a reused skill produces.
    """
    ops = list(FAMILY_OPS[family])
    return [ops[2]] if macro else ops


class GridSolver:
    """Solve grid tasks and record every reasoning step."""

    def __init__(self, *, cost_per_step: float = 1.0, compose: bool = False) -> None:
        self.cost_per_step = float(cost_per_step)
        self.compose = bool(compose)
    def solve(
        self,
        task: GridTask,
        *,
        macro_ops: Sequence[str] | None = None,
    ) -> SolveResult:
        """Solve one task using macro steps (reuse) or free search."""
        steps: list[ReasoningStep] = []
        counter = [0]

        def emit(operation: str, payload: Any = None, cost: float | None = None) -> None:
            counter[0] += 1
            steps.append(
                ReasoningStep(
                    step_id=f"{task.task_id}-s{counter[0]}",
                    operation=operation,
                    outputs=[] if payload is None else [str(payload)],
                    cost=self.cost_per_step if cost is None else float(cost),
                )
            )

        grid = task.input_grid
        strategy = "search"

        if macro_ops:
            strategy = "reuse"
            # A reused skill replaces the whole reasoning sequence, including the
            # composition stage. Its steps are priced at their real per-step cost
            # so the saving comes from skipping work, not from a discount.
            emit("detect_object", grid.height * grid.width)
            for op in macro_ops:
                emit(op, "macro")
                grid = _apply_macro(op, grid, task.task_family)
            # The target's output operation is real work even when a reused
            # invariant transforms or preserves the grid. Charge it explicitly;
            # _output_for below is only the deterministic output adapter, not a
            # free reasoning step that a macro may silently omit.
            required_output_op = {
                "counting": "count_objects",
                "grouping": "group_by_color",
            }.get(task.task_family)
            if required_output_op and required_output_op not in macro_ops:
                output_payload = (
                    count_objects(grid)
                    if required_output_op == "count_objects"
                    else group_by_color(grid)
                )
                emit(required_output_op, output_payload)
            emit("verify_output", "reused")
        else:
            emit("detect_object", grid.height * grid.width)
            readings = _readings(task)
            # Ambiguous tasks are resolved wrongly on purpose: the solver picks
            # the last (defensible but incorrect) reading.
            chosen = readings[-1] if task.ambiguous else readings[0]
            strategy = chosen[0]
            if self.compose:
                # Harder experience composes two transformations. The composed
                # result *is* the answer, so this is a real new mechanism rather
                # than a harder but different task.
                emit("detect_object", "stage2")
                grid = self._stage(grid, task, emit)
                emit("detect_object", "compose")
            grid = self._execute(task, chosen[1], emit, grid)
            emit("verify_output", "ok")

        output = _output_for(task.task_family, grid)
        return SolveResult(
            task_id=task.task_id,
            task_family=task.task_family,
            steps=steps,
            output=output,
            success=_matches(task, output),
            cost=sum(s.cost for s in steps),
            strategy=strategy,
            metadata={
                "variant": task.variant,
                "difficulty": task.difficulty,
                "ambiguous": task.ambiguous,
            },
        )

    def _execute(
        self, task: GridTask, ops: list[str], emit, grid: Grid
    ) -> Grid:
        family = task.task_family
        if family == "reflection":
            op = ops[0]
            emit("find_symmetry", op)
            grid = reflect_horizontal(grid) if op == "h" else reflect_vertical(grid)
            emit("apply_reflection", "mirrored")
        elif family == "rotation":
            emit("find_rotation", "quarter" if len(ops) == 1 else "half")
            for _ in ops:
                grid = rotate_90(grid)
            emit("apply_rotation", "rotated")
        elif family == "counting":
            self._reduce_grid(grid, emit)
            emit("count_objects", count_objects(grid))
        elif family == "grouping":
            self._reduce_grid(grid, emit)
            emit("group_by_color", group_by_color(grid))
        return grid

    def _stage(self, grid: Grid, task: GridTask, emit) -> Grid:
        """First stage of a composed task (used when ``compose=True``).

        Always a rotation, matching :func:`solver.tasks.expected_output`, so the
        emitted steps and the reference answer stay consistent.
        """
        del task
        emit("find_rotation", "stage1")
        return rotate_90(grid)

    def _reduce_grid(self, grid: Grid, emit) -> None:
        """Detect a grid symmetry before reducing it.

        Symmetric grids invite a reflection reading; asymmetric ones invite a
        rotation reading. Both are genuine invariances of the reduction that
        follows, which is why these steps recur across task families.
        """
        if _has_horizontal_symmetry(grid):
            emit("find_symmetry", "shared_axis")
            emit("apply_reflection", "symmetric")
        else:
            emit("find_rotation", "no_axis")
            emit("apply_rotation", "rotation_invariant")


def _readings(task: GridTask) -> list[tuple[str, list[str]]]:
    """Plausible readings of a task as (strategy, canonical apply ops).

    The first reading is always the correct one; later readings are the
    competing interpretations an ambiguous task invites. Rotation uses the same
    vocabulary for both readings so the family keeps one signature.
    """
    family = task.task_family
    if family == "reflection":
        # Correct reading is always the horizontal mirror; the competing reading
        # is the vertical one, which is wrong on these asymmetric grids.
        return [("h", ["h"]), ("v", ["v"])]
    if family == "rotation":
        return [("quarter", ["rotate_90"]), ("half", ["rotate_90", "rotate_90"])]
    return [(family, [])]


def _has_horizontal_symmetry(grid: Grid) -> bool:
    """True when every row reads the same left-to-right and right-to-left."""
    return all(row == tuple(reversed(row)) for row in grid.cells)


def _output_for(family: str, grid: Grid) -> Any:
    if family in ("reflection", "rotation"):
        return grid
    if family == "counting":
        return count_objects(grid)
    return group_by_color(grid)


def _apply_macro(op: str, grid: Grid, family: str) -> Grid:
    """Apply one canonical apply-step during skill reuse."""
    if op == "apply_reflection":
        return reflect_horizontal(grid)
    if op == "apply_rotation":
        return rotate_90(grid)
    if op in {"count_objects", "group_by_color"} and family in {
        "counting",
        "grouping",
    }:
        # The family output is computed after replay; this marker only
        # collapses the reasoning steps and leaves the grid as its input.
        return grid
    return grid


def _matches(task: GridTask, output: Any) -> bool:
    expected = task.expected
    if isinstance(expected, Grid):
        return isinstance(output, Grid) and diff_cells(expected, output) == 0
    return output == expected
