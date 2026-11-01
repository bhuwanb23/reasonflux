"""Seed-disjoint trace discovery and frozen skill candidate construction."""
from __future__ import annotations
from typing import Any
from .common import ALLOWED_OPS
from pipelines.trace_pipeline import TracePipelineResult
from pipelines.invariant_pipeline import run_invariant_pipeline
from solver.tasks import FAMILIES, make_task
from solver.executor import GridSolver
from traces.logger import TraceLogger
from skills.config import SkillConfig
from skills.library import SkillLibrary
from skills.promotion import promote_skill
from experiments.phase13c.scoring import _candidate_score, _eligible_pool, _gate_config
from experiments.phase13c.tasking import _macro_ops_for_signature


def train_seed(run_seed: int, config: dict[str, Any]) -> dict[str, Any]:
    n = int(config["tasks"]["training_traces_per_family"])
    train_seed = run_seed + int(config["tasks"]["training_seed_offset"])
    difficulty = float(config["tasks"].get("difficulty_training", 0.3))
    tasks = [make_task(family, seed=train_seed + index, difficulty=difficulty, variant=0)
             for index in range(n) for family in FAMILIES]
    solver = GridSolver()
    logger = TraceLogger(clock=lambda: float(train_seed))
    pairs = [(task.to_task(), solver.solve(task)) for task in tasks]
    traces = logger.log_batch(pairs)
    trace_run = TracePipelineResult(
        traces=traces, tasks=tasks, store_root="",
        success_count=sum(bool(trace.outcome and trace.outcome.success) for trace in traces),
        failure_count=sum(not bool(trace.outcome and trace.outcome.success) for trace in traces),
        families=list(FAMILIES),
    )
    mined = run_invariant_pipeline(trace_run.traces, validate=True, attach_priors=True, bootstrap=True)
    promotable = list(mined.promotable)
    skill_config = SkillConfig()
    eligible, rejected = _eligible_pool(promotable, skill_config)
    pool: list[dict[str, Any]] = []
    for item in eligible:
        inv = item["invariant"]
        macro = _macro_ops_for_signature(inv.pattern_signature)
        if len(macro) != 1 or macro[0] not in ALLOWED_OPS:
            rejected.append({"invariant_id": inv.invariant_id, "reasons": ["unsupported_or_non_atomic_macro"]})
            continue
        library = SkillLibrary()
        candidate, _ = _candidate_score(inv, skill_config)
        promoted = promote_skill(candidate, invariant=inv, library=library,
                                 config=_gate_config(skill_config), allow_prior_evidence=True)
        if not promoted.promoted or promoted.skill is None:
            rejected.append({"invariant_id": inv.invariant_id, "reasons": list(promoted.reasons or ["promotion_failed"])})
            continue
        skill = promoted.skill
        pool.append({
            "skill": skill,
            "op": macro[0],
            "family": str((skill.metadata or {}).get("mvp_category", "general")),
            "invariant_id": inv.invariant_id,
            "IS": float(inv.strength or 0.0),
            "SCV10": float(item["score"]["SCV10"]),
            "signature": list(inv.pattern_signature),
            "source_family": str((inv.metadata or {}).get("mvp_category", "general")),
        })
    examples = []
    for task, trace in zip(trace_run.tasks, trace_run.traces):
        family_op = {"reflection": "apply_reflection", "rotation": "apply_rotation",
                     "counting": "count_objects", "grouping": "group_by_color"}.get(task.task_family)
        if family_op and trace.outcome and trace.outcome.success:
            examples.append({"task_id": task.task_id, "family": task.task_family,
                             "op": family_op, "grid": task.input_grid,
                             "trace_id": trace.trace_id,
                             "steps": [s.operation for s in trace.steps]})
    return {"seed": run_seed, "trace_run": trace_run, "mined": mined,
            "pool": pool, "rejected": rejected, "examples": examples,
            "training_task_ids": [t.task_id for t in trace_run.tasks]}
