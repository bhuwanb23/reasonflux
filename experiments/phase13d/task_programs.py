"""Deterministic experiment-local transfer programs and synthetic task recipes."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from .common import FAMILY_FOR_OP
from solver.grid import Grid, count_objects, group_by_color, reflect_horizontal, rotate_90
from solver.tasks import make_task


@dataclass(frozen=True)
class TransferTask:
    experiment_id: str
    task_id: str
    taxonomy: str
    input_family: str
    input_grid: Grid
    ops: tuple[str, ...]
    expected: Any
    run_seed: int
    index: int


def execute_program(grid: Grid, ops: tuple[str, ...] | list[str], prefix_ops: tuple[str, ...] | list[str] = ()) -> Any:
    """Reference semantics: execute in order; include final grid iff transformed."""
    state = grid
    outputs: dict[str, Any] = {}
    target_ops = tuple(ops)
    target_transformed = any(op in {"apply_reflection", "apply_rotation"} for op in target_ops)
    for op in prefix_ops:
        if op == "apply_reflection":
            state = reflect_horizontal(state)
        elif op == "apply_rotation":
            state = rotate_90(state)
        elif op not in {"count_objects", "group_by_color", "count_groups"}:
            raise ValueError(f"unsupported Phase-13D operation: {op}")
    for op in target_ops:
        if op == "apply_reflection":
            state = reflect_horizontal(state)
        elif op == "apply_rotation":
            state = rotate_90(state)
        elif op == "count_objects":
            outputs[op] = count_objects(state)
        elif op == "group_by_color":
            outputs[op] = group_by_color(state)
        elif op == "count_groups":
            outputs[op] = len(group_by_color(state))
        else:
            raise ValueError(f"unsupported Phase-13D operation: {op}")
    if not outputs:
        return state
    if len(target_ops) == 1 and not target_transformed:
        return next(iter(outputs.values()))
    result: dict[str, Any] = {}
    if target_transformed:
        result["grid"] = state.to_rows()
    result.update(outputs)
    return result


def _recipe(experiment_id: str) -> tuple[str, str, tuple[str, ...], tuple[str, ...]]:
    recipes = {
        "EXP-TR-01": ("near", "reflection", ("apply_reflection",), ()),
        "EXP-TR-02": ("near", "rotation", ("apply_rotation",), ()),
        "EXP-TR-03": ("near", "counting", ("count_objects",), ()),
        "EXP-TR-04": ("moderate", "grouping", ("apply_reflection", "group_by_color"), ("apply_reflection",)),
        "EXP-TR-05": ("moderate", "counting", ("apply_rotation", "count_objects"), ("apply_rotation",)),
        "EXP-TR-06": ("moderate", "grouping", ("group_by_color", "count_groups"), ("group_by_color",)),
        "EXP-TR-07": ("compositional", "counting", ("apply_reflection", "count_objects"), ("apply_reflection", "count_objects")),
        "EXP-TR-08": ("compositional", "grouping", ("apply_reflection", "group_by_color"), ("apply_reflection", "group_by_color")),
        "EXP-TR-09": ("compositional", "counting", ("apply_rotation", "count_objects"), ("apply_rotation", "count_objects")),
        "EXP-TR-10": ("structural", "grouping", ("apply_reflection", "apply_rotation", "group_by_color"), ("apply_reflection", "apply_rotation", "group_by_color")),
        "EXP-TR-11": ("structural_novel_order", "grouping", ("apply_rotation", "apply_reflection", "group_by_color", "count_objects"), ("apply_rotation", "apply_reflection", "group_by_color", "count_objects")),
        "EXP-TR-15": ("negative", "counting", ("count_objects",), ()),
        "EXP-TR-16": ("negative", "counting", ("count_objects",), ()),
        "EXP-TR-17": ("negative", "rotation", ("apply_rotation", "count_objects"), ("apply_rotation", "count_objects")),
    }
    return recipes[experiment_id]


def experiment_ids() -> list[str]:
    return [f"EXP-TR-{n:02d}" for n in list(range(1, 12)) + [15, 16, 17]]


def source_skill_ops(experiment_id: str) -> tuple[str, ...]:
    mapping = {
        "EXP-TR-01": ("apply_reflection",), "EXP-TR-02": ("apply_rotation",),
        "EXP-TR-03": ("count_objects",), "EXP-TR-04": ("apply_reflection",),
        "EXP-TR-05": ("apply_rotation",), "EXP-TR-06": ("group_by_color",),
        "EXP-TR-07": ("apply_reflection", "count_objects"),
        "EXP-TR-08": ("apply_reflection", "group_by_color"),
        "EXP-TR-09": ("apply_rotation", "count_objects"),
        "EXP-TR-10": ("apply_reflection", "apply_rotation", "group_by_color"),
        "EXP-TR-11": ("apply_rotation", "apply_reflection", "group_by_color", "count_objects"),
        "EXP-TR-15": ("apply_reflection",), "EXP-TR-16": (),
        "EXP-TR-17": ("apply_reflection", "group_by_color"),
    }
    return mapping[experiment_id]


def make_experiment_tasks(experiment_id: str, run_seed: int, n: int = 10) -> list[TransferTask]:
    taxonomy, input_family, ops, _ = _recipe(experiment_id)
    number = int(experiment_id[-2:])
    if number <= 3:
        offset, slot = 2000, number - 1
    elif number <= 6:
        offset, slot = 3000, number - 4
    elif number <= 9:
        offset, slot = 4000, number - 7
    elif number <= 11:
        offset, slot = 5000, number - 10
    else:
        offset, slot = 6000, number - 15
    tasks = []
    for i in range(n):
        seed = run_seed + offset + slot * 100 + i
        variant = 0 if experiment_id == "EXP-TR-15" else i % 2
        base = make_task(input_family, seed=seed, difficulty=0.35, variant=variant)
        expected = execute_program(base.input_grid, ops)
        tasks.append(TransferTask(
            experiment_id=experiment_id,
            task_id=f"{experiment_id}-s{run_seed}-t{i:02d}",
            taxonomy=taxonomy,
            input_family=input_family,
            input_grid=base.input_grid,
            ops=ops,
            expected=expected,
            run_seed=run_seed,
            index=i,
        ))
    return tasks


def apply_negative_prefix(experiment_id: str, index: int, learned_ops: list[str]) -> tuple[str, ...]:
    if experiment_id == "EXP-TR-15":
        return ("apply_reflection",)
    if experiment_id == "EXP-TR-16":
        return tuple(learned_ops[:1])
    if experiment_id == "EXP-TR-17":
        return ("apply_reflection", "group_by_color")
    return ()


def source_families(ops: tuple[str, ...]) -> list[str]:
    return list(dict.fromkeys(FAMILY_FOR_OP[op] for op in ops))


def normalize_expected(value: Any) -> Any:
    if isinstance(value, Grid):
        return value.to_rows()
    if isinstance(value, dict):
        return {str(k): normalize_expected(v) for k, v in sorted(value.items(), key=lambda p: str(p[0]))}
    if isinstance(value, tuple):
        return [normalize_expected(v) for v in value]
    return value
