"""Deterministic grid solver — produces real reasoning traces (Phase 11)."""

from solver.executor import GridSolver, SolveResult, raw_operations
from solver.grid import (
    Grid,
    count_objects,
    group_by_color,
    reflect_horizontal,
    reflect_vertical,
    rotate_90,
)
from solver.tasks import (
    FAMILIES,
    FAMILY_OPS,
    GridTask,
    expected_output,
    make_task,
    make_task_batch,
)

__all__ = [
    "FAMILIES",
    "FAMILY_OPS",
    "Grid",
    "GridSolver",
    "GridTask",
    "SolveResult",
    "count_objects",
    "expected_output",
    "group_by_color",
    "make_task",
    "make_task_batch",
    "raw_operations",
    "reflect_horizontal",
    "reflect_vertical",
    "rotate_90",
]
