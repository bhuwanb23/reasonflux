"""Deterministic grid task generator for the four MVP families (Phase 11).

Tasks are synthetic but real: every task has a known correct output computed by
executing the family's reference operation on the input grid. Difficulty raises
the chance that a plausible-but-wrong heuristic is used, which is what produces
genuine failure traces for the miner.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from core.task import Task
from solver.grid import (
    Grid,
    count_objects,
    group_by_color,
    reflect_horizontal,
    reflect_vertical,
    rotate_90,
)

__all__ = [
    "FAMILIES",
    "GridTask",
    "expected_output",
    "make_task",
    "make_task_batch",
]

FAMILIES = ("reflection", "rotation", "counting", "grouping")

#: Canonical operation names per family, in execution order.
FAMILY_OPS: dict[str, tuple[str, ...]] = {
    "reflection": ("detect_object", "find_symmetry", "apply_reflection", "verify_output"),
    "rotation": ("detect_object", "find_rotation", "apply_rotation", "verify_output"),
    "counting": ("detect_object", "count_objects", "verify_output"),
    "grouping": ("detect_object", "group_by_color", "verify_output"),
}

#: Raw spellings used to exercise the normalizer's synonym map.
OP_VARIANTS: dict[str, tuple[str, ...]] = {
    "detect_object": ("DetectObject", "LocateObject"),
    "find_symmetry": ("FindSymmetry", "FindMirrorAxis"),
    "apply_reflection": ("ApplyReflection", "Reflect"),
    "find_rotation": ("FindRotation",),
    "apply_rotation": ("ApplyRotation", "Rotate"),
    "count_objects": ("CountObjects", "Count"),
    "group_by_color": ("GroupByColor",),
    "verify_output": ("VerifyOutput", "Verify"),
}


@dataclass(slots=True)
class GridTask:
    """A grid task with its reference output."""

    task_id: str
    task_family: str
    input_grid: Grid
    expected: Any
    difficulty: float = 0.0
    variant: int = 0
    ambiguous: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_task(self) -> Task:
        """Adapt to the core object so trace metadata flows through normally."""
        expected = self.expected
        if isinstance(expected, Grid):
            expected = expected.to_rows()
        return Task(
            task_id=self.task_id,
            task_family=self.task_family,
            input_state=self.input_grid.to_rows(),
            expected_outcome=expected,
            difficulty=self.difficulty,
            metadata={**self.metadata, "variant": self.variant},
        )


def _random_grid(rng: random.Random, *, size: int, palette: int = 4) -> Grid:
    rows: list[list[int]] = []
    # Fill entirely so the grid is asymmetric: a vertically mirrored candidate
    # then produces a genuinely wrong answer on ambiguous tasks.
    for _ in range(size):
        rows.append([rng.randrange(0, palette) for _ in range(size)])
    if all(c == 0 for row in rows for c in row):
        rows[0][0] = 1
    return Grid.from_rows(rows)


def _blob_grid(
    rng: random.Random, *, size: int, blobs: int, symmetric: bool = False
) -> Grid:
    """Sparse grid with a few separated blobs (used for counting/grouping).

    ``symmetric`` mirrors the left half onto the right, which gives the solver a
    real symmetry axis to detect. That is what lets reflection structure recur
    outside the reflection family — the cross-family recurrence the theory
    predicts, not a contrived overlap.
    """
    cells = [[0] * size for _ in range(size)]
    colors = list(range(1, 5))
    placed = 0
    attempts = 0
    half = (size + 1) // 2
    while placed < blobs and attempts < size * size * 4:
        attempts += 1
        r, c = rng.randrange(size), rng.randrange(half if symmetric else size)
        if any(
            cells[rr][cc] != 0
            for rr in range(max(0, r - 1), min(size, r + 2))
            for cc in range(max(0, c - 1), min(size, c + 2))
        ):
            continue
        cells[r][c] = rng.choice(colors)
        if symmetric:
            cells[r][size - 1 - c] = cells[r][c]
        placed += 1
    if placed == 0:
        cells[0][0] = 1
    return Grid.from_rows(cells)


def expected_output(family: str, grid: Grid, *, variant: int = 0) -> Any:
    """Reference output for ``family`` on ``grid``.

    The reflection target is always the horizontal mirror. ``variant`` only
    changes the *spelling* of the operations (exercising the normalizer), never
    the arithmetic — otherwise a single reusable skill could not know which axis
    to apply and reuse would be unwinnable by construction.
    """
    if family == "reflection":
        return reflect_horizontal(grid)
    if family == "rotation":
        return rotate_90(grid) if variant % 2 == 0 else rotate_90(rotate_90(grid))
    if family == "counting":
        return count_objects(grid)
    if family == "grouping":
        return group_by_color(grid)
    raise ValueError(f"unknown task family: {family!r}")


def make_task(
    family: str,
    *,
    seed: int = 0,
    difficulty: float = 0.3,
    variant: int = 0,
) -> GridTask:
    """Build a deterministic task. Same arguments always yield the same task."""
    if family not in FAMILIES:
        raise ValueError(f"unknown task family: {family!r}")
    if not 0.0 <= float(difficulty) <= 1.0:
        raise ValueError("difficulty must be in [0, 1]")

    rng = random.Random(f"{family}:{seed}:{variant}")
    size = 3 + int(float(difficulty) * 3)  # 3..6
    # Variant 1 for counting/grouping uses a symmetric grid so the solver has a
    # genuine symmetry axis to detect before reducing the task.
    symmetric = family in ("counting", "grouping") and variant % 2 == 1
    if family in ("counting", "grouping"):
        grid = _blob_grid(rng, size=size, blobs=max(2, size - 1), symmetric=symmetric)
    else:
        grid = _random_grid(rng, size=size)
    expected = expected_output(family, grid, variant=variant)

    # High difficulty marks the task ambiguous: more than one transform reading
    # is defensible, so the solver's first choice may be wrong.
    ambiguous = float(difficulty) >= 0.7
    return GridTask(
        task_id=f"{family}-{seed}-v{variant}",
        task_family=family,
        input_grid=grid,
        expected=expected,
        difficulty=float(difficulty),
        variant=variant,
        ambiguous=ambiguous,
        metadata={
            "task_family": family,
            "seed": seed,
            "size": size,
            "ambiguous": ambiguous,
            "symmetric": symmetric,
        },
    )


def make_task_batch(
    families: tuple[str, ...] = FAMILIES,
    *,
    per_family: int = 4,
    seed: int = 0,
    difficulty: float = 0.3,
) -> list[GridTask]:
    """Build a balanced batch across families, alternating spelling variants."""
    out: list[GridTask] = []
    for i in range(per_family):
        for family in families:
            out.append(
                make_task(
                    family,
                    seed=seed + i,
                    difficulty=difficulty,
                    variant=i % 2,
                )
            )
    return out
