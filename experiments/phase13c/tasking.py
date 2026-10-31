"""Task-stream construction and pre-outcome opportunity eligibility."""
from __future__ import annotations

from typing import Any
from core.invariant import Invariant
from pipelines.trace_pipeline import run_trace_pipeline
from solver.tasks import FAMILIES, GridTask, make_task_batch


def _macro_ops_for_signature(signature: list[str] | tuple[str, ...]) -> list[str]:
    for operation in signature:
        op = str(operation)
        if op.startswith("apply_"):
            return [op]
        if op == "find_symmetry":
            return ["apply_reflection"]
        if op == "find_rotation":
            return ["apply_rotation"]
        if op in {"count_objects", "group_by_color"}:
            return [op]
    return []


def _is_eligible_opportunity(inv: Invariant, task: GridTask) -> bool:
    """Pre-outcome task eligibility; includes reflection cross-family symmetry."""
    signature = list(inv.pattern_signature)
    macro = _macro_ops_for_signature(signature)
    source = str((inv.metadata or {}).get("mvp_category", ""))
    if not source:
        source = str((inv.metadata or {}).get("task_family", ""))
    if macro and source == task.task_family:
        return True
    if (
        macro == ["apply_reflection"]
        and task.task_family in {"counting", "grouping"}
        and bool(task.metadata.get("symmetric"))
    ):
        return True
    # Mined invariants can be shared across their observed task families even
    # when the category heuristic is absent; this is fixed before evaluation.
    return task.task_family in set(inv.task_families or [])


def _opportunities(inv: Invariant, all_tasks: list[GridTask], n: int = 10) -> list[GridTask]:
    eligible = [task for task in all_tasks if _is_eligible_opportunity(inv, task)]
    by_family: dict[str, list[GridTask]] = {}
    for task in eligible:
        by_family.setdefault(task.task_family, []).append(task)
    families = sorted(by_family)
    chosen: list[GridTask] = []
    cursor = {family: 0 for family in families}
    while len(chosen) < n:
        advanced = False
        for family in families:
            if cursor[family] < len(by_family[family]) and len(chosen) < n:
                chosen.append(by_family[family][cursor[family]])
                cursor[family] += 1
                advanced = True
        if not advanced:
            break
    return chosen


def _enforce_opportunity_horizon(
    eligible: list[dict[str, Any]],
    rejected: list[dict[str, Any]],
    tasks: list[GridTask],
    horizon: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Keep only candidates with the full predeclared held-out opportunity horizon."""
    kept = []
    for item in eligible:
        inv = item["invariant"]
        opportunities = _opportunities(inv, tasks, horizon)
        if len(opportunities) == horizon and len({task.task_id for task in opportunities}) == horizon:
            kept.append(item)
        else:
            rejected.append({
                "invariant_id": inv.invariant_id,
                "signature": list(inv.pattern_signature),
                "reasons": ["insufficient_distinct_heldout_opportunities"],
                "available_opportunities": len(opportunities),
                "required_opportunities": horizon,
                "SCV10": item["score"]["SCV10"],
            })
    return kept, rejected


def _task_batches(run_seed: int, config_data: dict[str, Any]) -> tuple[Any, list[GridTask]]:
    discovery_seed = run_seed + int(config_data["tasks"]["discovery_seed_offset"])
    evaluation_seed = run_seed + int(config_data["tasks"]["evaluation_seed_offset"])
    trace_run = run_trace_pipeline(
        FAMILIES,
        per_family=int(config_data["tasks"]["discovery_traces_per_family"]),
        seed=discovery_seed,
        difficulty=0.3,
        persist=False,
    )
    eval_tasks = make_task_batch(
        FAMILIES,
        per_family=int(config_data["tasks"]["evaluation_opportunities_per_candidate"]),
        seed=evaluation_seed,
        difficulty=0.3,
    )
    discovery_ids = {task.task_id for task in trace_run.tasks}
    evaluation_ids = {task.task_id for task in eval_tasks}
    if discovery_ids & evaluation_ids:
        raise AssertionError("discovery/evaluation task ID overlap")
    return trace_run, eval_tasks
