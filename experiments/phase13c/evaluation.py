"""Paired held-out execution for Skill and raw-trace memory representations."""
from __future__ import annotations

from statistics import mean
from typing import Any
from core.invariant import Invariant
from core.skill import Skill, SkillCandidate
from evaluation.transfer_metrics import compute_ts
from skills.config import SkillConfig
from skills.library import SkillLibrary
from skills.lifecycle.sweep import evaluate_library_lifecycle
from skills.promotion import promote_skill
from skills.utility import score_skill_utility
from solver.executor import GridSolver
from solver.tasks import GridTask
from transfer.reuse_engine import ReuseEngine
from .scoring import _gate_config
from .tasking import _opportunities


def _summarize_reuse(skill: Skill, rows: list[dict[str, Any]], source_family: str) -> dict[str, Any]:
    applied = [row for row in rows if row["applied"]]
    cross = [row for row in applied if row["task_family"] != source_family]
    if cross:
        before = mean(1.0 / max(float(row["baseline_cost"]), 1e-9) for row in cross)
        after = mean(
            (1.0 / max(float(row["reused_cost"]), 1e-9)) if row["success"] else 0.0
            for row in cross
        )
        ts = compute_ts(before, after)
    else:
        before = after = ts = 0.0
    return {
        "eligible_opportunities": len(rows),
        "applied_attempts": len(applied),
        "successful_applications": sum(bool(row["success"]) for row in applied),
        "credited_reuses": sum(bool(row["transfer_credit"]) for row in applied),
        "failed_applications": sum(not bool(row["success"]) for row in applied),
        "no_match": sum(not bool(row["applied"]) for row in rows),
        "reuse_rate_opportunity": (
            sum(bool(row["transfer_credit"]) for row in applied) / len(rows) if rows else 0.0
        ),
        "TS_cross_family": ts,
        "cross_family_performance_before": before,
        "cross_family_performance_after": after,
        "cross_family_opportunities": len(cross),
        "cross_family_successes": sum(bool(row["transfer_credit"]) for row in cross),
        "unique_skill_reused": int(bool(applied)),
        "reuse_count": int(skill.reuse_count),
    }


def _evaluate_skill(
    inv: Invariant,
    candidate: SkillCandidate,
    trace_run: Any,
    tasks: list[GridTask],
    config: SkillConfig,
    *,
    maintenance_per_opportunity: float,
    lifecycle_enabled: bool = True,
) -> dict[str, Any]:
    gate_cfg = _gate_config(config)
    library = SkillLibrary()
    result = promote_skill(
        candidate,
        invariant=inv,
        library=library,
        config=gate_cfg,
        allow_prior_evidence=True,
    )
    if not result.promoted or result.skill is None:
        return {"created": False, "rejection_reasons": result.reasons, "task_results": []}
    skill = result.skill
    solver = GridSolver()
    engine = ReuseEngine(library, solver=solver, config=config)
    opportunities = _opportunities(inv, tasks, 10)
    if len(opportunities) != 10 or len({task.task_id for task in opportunities}) != 10:
        raise AssertionError("candidate evaluation lacks ten distinct eligible opportunities")
    rows: list[dict[str, Any]] = []
    utility_timeline: list[dict[str, Any]] = []
    for index, task in enumerate(opportunities):
        if lifecycle_enabled:
            evaluate_library_lifecycle(
                library, task_clock=index, config=config, tick_unused=True
            )
        baseline = solver.solve(task)
        reuse = engine.apply(task, baseline=baseline, task_clock=index)
        row = reuse.to_dict()
        rows.append(row)
        breakdown = score_skill_utility(skill, config)
        utility_timeline.append(
            {
                "task_index": index,
                "task_id": task.task_id,
                "state": skill.state.value,
                **breakdown.to_dict(),
            }
        )
    reuse_stats = _summarize_reuse(
        skill,
        rows,
        str((skill.metadata or {}).get("mvp_category", "general")),
    )
    cc = max(0.0, float(candidate.creation_cost))
    total_benefit = sum(float(row["benefit"]) for row in rows)
    net_value = total_benefit - cc - len(opportunities) * maintenance_per_opportunity
    return {
        "created": True,
        "skill": skill,
        "birth": result.birth.to_dict() if result.birth else None,
        "state_at_end": skill.state.value,
        "provisional_at_end": bool((skill.metadata or {}).get("provisional")),
        "creation_cost": cc,
        "maintenance_cost": len(opportunities) * maintenance_per_opportunity,
        "total_success_gated_benefit": total_benefit,
        "realized_net_value": net_value,
        "mean_SU_at_end": float(skill.utility),
        "utility_breakdown_at_end": score_skill_utility(skill, config).to_dict(),
        "reuse_statistics": reuse_stats,
        "utility_timeline": utility_timeline,
        "task_results": rows,
    }


def _evaluate_memory_only(
    inv: Invariant,
    trace_run: Any,
    tasks: list[GridTask],
    *,
    creation_cost: float,
    maintenance_per_opportunity: float,
) -> dict[str, Any]:
    """Raw-trace exemplar retrieval; no Skill or executable skill object is made."""
    source_traces = [
        trace for trace in trace_run.traces
        if set(inv.pattern_signature).issubset({step.operation for step in trace.steps})
    ]
    source_trace = source_traces[0] if source_traces else None
    macro = []
    if source_trace is not None:
        for step in source_trace.steps:
            op = str(step.operation)
            if op.startswith("apply_"):
                macro = [op]
                break
            if op in {"count_objects", "group_by_color"}:
                macro = [op]
                break
    opportunities = _opportunities(inv, tasks, 10)
    if len(opportunities) != 10 or len({task.task_id for task in opportunities}) != 10:
        raise AssertionError("memory evaluation lacks ten distinct eligible opportunities")
    solver = GridSolver()
    rows = []
    for task in opportunities:
        baseline = solver.solve(task)
        if macro:
            reused = solver.solve(task, macro_ops=macro)
            reduction = (
                max(0.0, min(1.0, (baseline.cost - reused.cost) / baseline.cost))
                if baseline.cost > 0 else 0.0
            )
            benefit = reduction if reused.success else 0.0
            rows.append(
                {
                    "task_id": task.task_id,
                    "task_family": task.task_family,
                    "applied": True,
                    "success": bool(reused.success),
                    "baseline_cost": baseline.cost,
                    "reused_cost": reused.cost,
                    "reasoning_reduction": reduction,
                    "benefit": benefit,
                    "transfer_credit": bool(reused.success and benefit > 0.0),
                    "retrieved_trace_id": source_trace.trace_id,
                }
            )
        else:
            rows.append(
                {
                    "task_id": task.task_id,
                    "task_family": task.task_family,
                    "applied": False,
                    "success": bool(baseline.success),
                    "baseline_cost": baseline.cost,
                    "reused_cost": baseline.cost,
                    "reasoning_reduction": 0.0,
                    "benefit": 0.0,
                    "transfer_credit": False,
                    "retrieved_trace_id": "",
                }
            )
    opportunities_n = len(opportunities)
    cc = max(0.0, float(creation_cost)) if source_trace else 0.0
    benefit = sum(float(row["benefit"]) for row in rows)
    net = benefit - cc - opportunities_n * maintenance_per_opportunity if source_trace else 0.0
    return {
        "created": bool(source_trace),
        "representation": "raw_trace_exemplar_no_Skill_object",
        "source_trace_id": source_trace.trace_id if source_trace else "",
        "macro_retrieved": macro,
        "creation_cost_proxy": cc,
        "maintenance_cost": opportunities_n * maintenance_per_opportunity if source_trace else 0.0,
        "total_success_gated_benefit": benefit,
        "realized_net_value": net,
        "task_results": rows,
        "reuse_statistics": {
            "eligible_opportunities": opportunities_n,
            "applied_attempts": sum(bool(row["applied"]) for row in rows),
            "successful_applications": sum(bool(row["success"]) for row in rows if row["applied"]),
            "credited_reuses": sum(bool(row["transfer_credit"]) for row in rows),
            "no_match": sum(not bool(row["applied"]) for row in rows),
        },
    }
