"""Deterministic grid solver: tasks, operations, and honest failure."""

from __future__ import annotations

import pytest

from solver import (
    FAMILIES,
    GridSolver,
    count_objects,
    group_by_color,
    make_task,
    make_task_batch,
    reflect_horizontal,
    reflect_vertical,
    rotate_90,
)
from solver.grid import Grid, diff_cells


def test_grid_operations_are_pure_and_correct():
    grid = Grid.from_rows([[1, 2], [3, 4]])
    assert reflect_horizontal(grid).to_rows() == [[2, 1], [4, 3]]
    assert reflect_vertical(grid).to_rows() == [[3, 4], [1, 2]]
    assert rotate_90(grid).to_rows() == [[3, 1], [4, 2]]
    # Original untouched.
    assert grid.to_rows() == [[1, 2], [3, 4]]


def test_grid_rejects_ragged_and_empty():
    with pytest.raises(ValueError):
        Grid.from_rows([[1, 2], [3]])
    with pytest.raises(ValueError):
        Grid.from_rows([])


def test_rotate_four_times_is_identity():
    grid = Grid.from_rows([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    out = grid
    for _ in range(4):
        out = rotate_90(out)
    assert out == grid


def test_count_objects_and_group_by_color():
    grid = Grid.from_rows([[1, 0, 2], [1, 0, 0], [0, 3, 3]])
    assert count_objects(grid) == 3
    assert group_by_color(grid) == {1: 2, 2: 1, 3: 2}


def test_tasks_are_deterministic():
    a = make_task("reflection", seed=7, difficulty=0.2)
    b = make_task("reflection", seed=7, difficulty=0.2)
    assert a.input_grid == b.input_grid
    assert a.task_id == b.task_id


def test_unknown_family_rejected():
    with pytest.raises(ValueError):
        make_task("telepathy", seed=0)


def test_solver_solves_every_family_at_low_difficulty():
    solver = GridSolver()
    for family in FAMILIES:
        for seed in range(4):
            task = make_task(family, seed=seed, difficulty=0.2)
            result = solver.solve(task)
            assert result.success, (family, seed, result.operations)
            assert result.step_count >= 3


def test_solver_emits_canonical_vocabulary():
    solver = GridSolver()
    ops = solver.solve(make_task("reflection", seed=1, difficulty=0.2)).operations
    assert "apply_reflection" in ops
    assert "verify_output" in ops
    rot = solver.solve(make_task("rotation", seed=1, difficulty=0.2)).operations
    assert "apply_rotation" in rot


def test_ambiguous_tasks_produce_genuine_failures():
    """Hard tasks are mis-resolved, which is what supplies failure traces."""
    solver = GridSolver()
    results = [
        solver.solve(make_task("reflection", seed=s, difficulty=0.9))
        for s in range(6)
    ]
    assert any(not r.success for r in results)
    assert all(r.step_count >= 3 for r in results)


def test_compose_stage_adds_steps_and_still_solves():
    plain = GridSolver()
    composed = GridSolver(compose=True)
    task = make_task("counting", seed=3, difficulty=0.2)
    assert composed.solve(task).step_count > plain.solve(task).step_count
    for family in FAMILIES:
        t = make_task(family, seed=3, difficulty=0.2, compose=True)
        assert composed.solve(t).success, family


def test_macro_reuse_is_cheaper_than_search():
    solver = GridSolver()
    task = make_task("rotation", seed=2, difficulty=0.2)
    baseline = solver.solve(task)
    reused = solver.solve(task, macro_ops=["apply_rotation"])
    assert reused.cost < baseline.cost
    assert reused.success


def test_batch_is_balanced_across_families():
    batch = make_task_batch(per_family=3, seed=0)
    assert len(batch) == 3 * len(FAMILIES)
    counts: dict[str, int] = {}
    for task in batch:
        counts[task.task_family] = counts.get(task.task_family, 0) + 1
    assert all(v == 3 for v in counts.values())


def test_diff_cells_detects_mismatch():
    a = Grid.from_rows([[1, 2], [3, 4]])
    b = Grid.from_rows([[1, 2], [3, 9]])
    assert diff_cells(a, b) == 1
    assert diff_cells(a, Grid.from_rows([[1, 2, 3]])) > 0
