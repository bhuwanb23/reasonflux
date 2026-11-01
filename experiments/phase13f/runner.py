"""Phase 13F paired seed runner; outcomes are independent of report generation."""
from __future__ import annotations

from typing import Any

from capability import advance_capability
from experiments.phase13e.arms import propose_composition, record_composition_task
from experiments.phase13e.metrics import summarize_round
from experiments.phase13e.runner import _macro_for
from skills.config import SkillConfig
from skills.lifecycle import apply_lifecycle, evaluate_lifecycle
from solver.executor import GridSolver

from .arms import build_arms, form, run_task
from .common import build_round_tasks, discover, load_config


def _lifecycle(runtime: Any, task_clock: int, config: SkillConfig) -> list[dict[str, Any]]:
    if not runtime.lifecycle_enabled:
        return [{"arm": runtime.arm, "action": "disabled_by_arm", "task_clock": task_clock}]
    rows = []
    for skill in runtime.library.list_skills():
        if skill.state.value not in {"active", "growing", "core"}:
            continue
        life = dict((skill.metadata or {}).get("lifecycle") or {})
        previous_su = float(life.get("previous_su", skill.utility or 0.0))
        decision = evaluate_lifecycle(skill, task_clock=task_clock, config=config, previous_su=previous_su)
        before = skill.state.value
        apply_lifecycle(skill, decision, config=config)
        rows.append({"arm": runtime.arm, "skill_id": skill.skill_id, "from_state": before,
                     "to_state": skill.state.value, "action": decision.action,
                     "reasons": list(decision.reasons), "task_clock": int(task_clock)})
    return rows


def _compose_row(runtime: Any, task: Any, baseline: Any, config: SkillConfig, seed: int, round_no: int) -> dict[str, Any]:
    if runtime.composition is None:
        runtime.composition = propose_composition(runtime, config)
    if runtime.composition is None:
        return {"seed": seed, "round": round_no, "arm": runtime.arm, "task_id": task.task_id,
                "evaluation_role": "promotion_validation" if round_no == 3 else "heldout_confirmation",
                "status": "unavailable_no_learned_proposal"}
    macros = []
    for sid in runtime.composition.order:
        skill = runtime.library.get(sid)
        if skill is not None:
            macros.extend(_macro_for(skill))
    row = record_composition_task(runtime, task, baseline, macros, config)
    row.update({"seed": seed, "round": round_no, "arm": runtime.arm,
                "evaluation_role": "promotion_validation" if round_no == 3 else "heldout_confirmation"})
    return row


def _mean_is(runtime: Any, strength_by_id: dict[str, float]) -> float | None:
    vals = [strength_by_id[s.source_invariant_id] for s in runtime.library.list_skills()
            if s.source_invariant_id in strength_by_id]
    return sum(vals) / len(vals) if vals else None


def _promoted_composition_row(runtime: Any, task: Any, row: dict[str, Any], seed: int, round_no: int) -> dict[str, Any]:
    comp_skill = runtime.library.get(runtime.composition_skill_id)
    component_ids = list((comp_skill.metadata or {}).get("composed_from") or []) if comp_skill else []
    solver = GridSolver(compose=True)
    baseline = solver.solve(task)
    single_costs = []
    for sid in component_ids:
        skill = runtime.library.get(sid)
        macros = _macro_for(skill) if skill is not None else []
        single = solver.solve(task, macro_ops=macros) if macros else baseline
        single_costs.append((float(single.cost), bool(single.success)))
    base = float(baseline.cost)
    single_benefits = [max(0.0, min(1.0, (base - cost) / base)) for cost, success in single_costs if base and success]
    single_benefit = max(single_benefits, default=0.0)
    best_single_cost = base * (1.0 - single_benefit)
    composed_cost = float(row["observed_cost"])
    composed_benefit = max(0.0, min(1.0, (base - composed_cost) / base)) if base and row["observed_success"] else 0.0
    return {"seed": seed, "round": round_no, "arm": runtime.arm, "task_id": task.task_id,
        "evaluation_role": "promotion_validation" if round_no == 3 else "heldout_confirmation",
        "status": "evaluated_promoted_chain", "success": bool(row["observed_success"]),
        "baseline_cost": base, "composed_cost": composed_cost,
        "best_single_cost": best_single_cost, "composition_benefit": composed_benefit,
        "best_single_benefit": single_benefit,
        "incremental_gain": composed_benefit - single_benefit if row["observed_success"] else 0.0}


def run_seed(seed: int, config: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = config or load_config()
    discovery = discover(seed, cfg)
    runtimes = build_arms(seed, discovery, cfg)
    strengths = {item["invariant"].invariant_id: float(item["invariant"].strength) for item in discovery["candidates"]}
    rounds: list[dict[str, Any]] = []
    tasks_out: list[dict[str, Any]] = []
    compositions: list[dict[str, Any]] = []
    formations: list[dict[str, Any]] = []
    lifecycles: list[dict[str, Any]] = []
    trace_count = len(discovery["trace_run"].traces)
    for round_index in range(int(cfg["rounds"]["count"])):
        round_no = round_index + 1
        tasks = build_round_tasks(seed, round_index, cfg)
        for runtime in runtimes.values():
            arm_cfg = runtime.skill_config
            utilities = []
            for task_index, task in enumerate(tasks):
                clock = trace_count + round_index * len(tasks) + task_index
                row, baseline = run_task(runtime, task, clock)
                tasks_out.append({"seed": seed, **row})
                utilities.append(float(row["task_utility"]))
                if row["compose_task"]:
                    if runtime.composition_skill_id and runtime.enabled_library:
                        compositions.append(_promoted_composition_row(runtime, task, row, seed, round_no))
                    elif runtime.enable_composition:
                        compositions.append(_compose_row(runtime, task, baseline, arm_cfg, seed, round_no))
                    else:
                        compositions.append({"seed": seed, "round": round_no, "arm": runtime.arm,
                            "task_id": task.task_id, "evaluation_role": "promotion_validation" if round_no == 3 else "heldout_confirmation",
                            "status": "disabled_by_preregistered_arm"})
            task_clock = trace_count + (round_index + 1) * len(tasks)
            lifecycles.extend({"seed": seed, "round": round_no, **r} for r in _lifecycle(runtime, task_clock, arm_cfg))
            before = sum(c.state.value != "archived" for c in runtime.capabilities.list_capabilities())
            formed = form(runtime, cfg)
            after = sum(c.state.value != "archived" for c in runtime.capabilities.list_capabilities())
            formations.extend({"seed": seed, "round": round_no, "arm": runtime.arm, **e} for e in formed)
            previous = next((r.get("_state") for r in reversed(rounds) if r["arm"] == runtime.arm), None)
            summary = summarize_round(runtime, round_index=round_index, previous=previous,
                experiences=trace_count + (round_index + 1) * len(tasks),
                task_utility_mean=sum(utilities) / len(utilities) if utilities else 0.0,
                new_capabilities=max(0, after - before), config=cfg)
            summary["seed"] = seed
            summary["IS"] = _mean_is(runtime, strengths)
            active_skills = [s for s in runtime.library.list_skills() if not (s.metadata or {}).get("provisional")]
            summary["SU"] = sum(float(s.utility or 0.0) for s in active_skills) / len(active_skills) if active_skills else None
            summary["TS"] = sum(float(s.transfer_score or 0.0) for s in active_skills) / len(active_skills) if active_skills else None
            summary["skill_count_created"] = runtime.created_skill_count
            summary["skill_count_persistent"] = len(runtime.library)
            summary["lifecycle_enabled"] = runtime.lifecycle_enabled
            if runtime.independent_capabilities:
                caps = [c for c in runtime.capabilities.list_capabilities() if c.state.value != "archived"]
                summary["independent_capability_count"] = len(caps)
                summary["independent_capability_mean_utility"] = sum(float(c.utility or 0.0) for c in caps) / len(caps) if caps else None
            if runtime.arm == "X3_NO_EXPERIENCE_MEMORY":
                summary["experience_memory"] = "discovery_traces_discarded_after_creation"
            if runtime.arm == "X2_NO_SKILL_LIBRARY":
                summary["skill_count_created"] = runtime.created_skill_count
            summary["_state"] = {"ct": float(summary.get("ct") or 0.0),
                "tg": float(summary.get("mean_transfer_score_ts") or 0.0),
                "ug": float(summary.get("capu") or 0.0),
                "supported_coverage": float(summary.get("supported_family_coverage") or 0.0),
                "comp": float(summary.get("composition_skill_count") or 0.0),
                "ig": float(summary.get("ig") or 0.0)}
            rounds.append(summary)
    for row in rounds:
        row.pop("_state", None)
    return {"seed": seed, "trace_count": trace_count,
        "invariant_candidate_count": len(discovery["invariant_run"].candidates),
        "promotable_count": len(discovery["invariant_run"].promotable),
        "qualified_candidate_count": len(discovery["candidates"]),
        "candidate_rejections": discovery["rejected"], "round_rows": rounds,
        "task_rows": tasks_out, "composition_rows": compositions,
        "formation_rows": formations, "lifecycle_rows": lifecycles}


def run_confirmation(config: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = config or load_config()
    return {"experiment_id": cfg["experiment_id"], "config": cfg,
            "seeds": [run_seed(int(seed), cfg) for seed in cfg["seeds"]]}
