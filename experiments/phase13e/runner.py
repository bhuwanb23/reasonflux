"""Confirmatory Phase 13E seed-block runner."""
from __future__ import annotations

from typing import Any

from evaluation.growth_config import GrowthConfig
from solver.executor import GridSolver
from skills.config import SkillConfig
from skills.lifecycle import apply_lifecycle, evaluate_lifecycle
from skills.monitoring import record_negative, record_reuse
from skills.utility import refresh_skill_utility
from transfer.reuse_engine import ReuseEngine

from .arms import build_arms, form_capabilities, record_composition_task
from .common import build_round_tasks, capability_config_from_json, discover, growth_config_from_json, load_config, task_utility
from .metrics import summarize_round
from .robustness import run_isolated_robustness


def _macro_for(skill: Any) -> list[str]:
    triggers = list(skill.trigger_conditions or [])
    for op in triggers:
        text = str(op)
        if text.startswith("apply_"):
            return [text]
        if text == "find_symmetry":
            return ["apply_reflection"]
        if text == "find_rotation":
            return ["apply_rotation"]
    return []


def _advance_storage_only_lifecycle(runtime: Any, task_clock: int, config: SkillConfig) -> list[dict[str, Any]]:
    """Allow B2's existing skill lifecycle to yield only atomic core capabilities."""
    if not runtime.atomic_only:
        return []
    rows = []
    for skill in runtime.library.list_skills():
        if skill.state.value not in {"active", "growing", "core"}:
            continue
        lifecycle = dict((skill.metadata or {}).get("lifecycle") or {})
        previous_su = float(lifecycle.get("previous_su", skill.utility or 0.0))
        decision = evaluate_lifecycle(skill, task_clock=task_clock, config=config, previous_su=previous_su)
        before = skill.state.value
        apply_lifecycle(skill, decision, config=config)
        rows.append({
            "arm": runtime.arm,
            "skill_id": skill.skill_id,
            "from_state": before,
            "to_state": skill.state.value,
            "action": decision.action,
            "reasons": list(decision.reasons),
            "task_clock": int(task_clock),
        })
    return rows


def _refresh_measured_transfer(skill: Any, config: SkillConfig) -> None:
    events = [e for e in skill.transfer_history or [] if e.get("success")]
    skill.transfer_score = sum(float(e.get("benefit", 0.0) or 0.0) for e in events) / len(events) if events else 0.0
    meta = dict(skill.metadata or {})
    meta["transfer_score_source"] = "mean_observed_successful_transfer_benefit"
    skill.metadata = meta
    refresh_skill_utility(skill, config)


def _run_task(runtime: Any, task: Any, clock: int, config: SkillConfig) -> tuple[dict[str, Any], Any]:
    solver = GridSolver(compose=bool((task.metadata or {}).get("compose")))
    baseline = solver.solve(task)
    reuse_payload: dict[str, Any]
    observed = baseline
    composed_skill = runtime.library.get(runtime.composition_skill_id) if runtime.composition_skill_id else None
    if runtime.enabled_library and composed_skill is not None and bool((task.metadata or {}).get("compose")):
        component_ids = list((composed_skill.metadata or {}).get("composed_from") or [])
        macros = [op for sid in component_ids for op in _macro_for(runtime.library.get(sid))] if component_ids else []
        reused = solver.solve(task, macro_ops=macros) if macros else baseline
        reduction = max(0.0, min(1.0, (baseline.cost - reused.cost) / baseline.cost)) if baseline.cost else 0.0
        benefit = reduction if reused.success else 0.0
        observed = reused
        if reused.success:
            record_reuse(composed_skill, task_id=task.task_id, detail={"family": task.task_family, "benefit": benefit}, config=config, task_clock=clock)
        else:
            record_negative(composed_skill, reason="composition_reuse_incorrect", detail={"task_id": task.task_id, "family": task.task_family}, config=config)
        refresh_skill_utility(composed_skill, config)
        reuse_payload = {
            "task_id": task.task_id, "task_family": task.task_family, "applied": bool(macros),
            "success": bool(reused.success), "skill_id": composed_skill.skill_id,
            "baseline_cost": float(baseline.cost), "reused_cost": float(reused.cost),
            "reasoning_reduction": float(reduction), "benefit": float(benefit),
            "transfer_credit": bool(reused.success and benefit > 0.0),
            "metadata": {"execution": "promoted_ordered_composition", "component_skill_ids": component_ids},
        }
    elif runtime.enabled_library and len(runtime.library):
        engine = ReuseEngine(runtime.library, solver=solver, config=config)
        result = engine.apply(task, baseline=baseline, task_clock=clock)
        observed = result.result if result.applied and result.result is not None else baseline
        if result.transfer_credit:
            skill = runtime.library.get(result.skill_id)
            if skill is not None:
                _refresh_measured_transfer(skill, config)
        reuse_payload = result.to_dict()
    else:
        reuse_payload = {
            "task_id": task.task_id,
            "task_family": task.task_family,
            "applied": False,
            "success": bool(baseline.success),
            "skill_id": "",
            "baseline_cost": float(baseline.cost),
            "reused_cost": float(baseline.cost),
            "reasoning_reduction": 0.0,
            "benefit": 0.0,
            "transfer_credit": False,
            "metadata": {"reason": "learning_or_library_disabled"},
        }
    row = {
        "arm": runtime.arm,
        "task_id": task.task_id,
        "task_family": task.task_family,
        "round": int(task.metadata["phase13e_round"]),
        "variant": int(task.variant),
        "compose_task": bool((task.metadata or {}).get("compose")),
        "symmetric": bool((task.metadata or {}).get("symmetric")),
        "baseline_success": bool(baseline.success),
        "baseline_cost": float(baseline.cost),
        "observed_success": bool(observed.success),
        "observed_cost": float(observed.cost),
        "task_utility": task_utility(bool(observed.success), float(observed.cost)),
        "reuse": reuse_payload,
    }
    return row, baseline


def run_seed(seed: int, config: dict[str, Any] | None = None) -> dict[str, Any]:
    """Run one complete, paired seed across all frozen arms."""
    cfg = config or load_config()
    discovery = discover(int(seed), cfg)
    runtimes = build_arms(int(seed), discovery, cfg)
    seed_round_rows: list[dict[str, Any]] = []
    task_rows: list[dict[str, Any]] = []
    composition_rows: list[dict[str, Any]] = []
    formation_rows: list[dict[str, Any]] = []
    skill_lifecycle_rows: list[dict[str, Any]] = []
    discovery_experiences = len(discovery["trace_run"].traces)
    for round_index in range(int(cfg["rounds"]["count"])):
        tasks = build_round_tasks(int(seed), round_index, cfg)
        # The same task objects and IDs are replayed for every arm within a seed.
        for runtime in runtimes.values():
            utilities: list[float] = []
            for j, task in enumerate(tasks):
                row, baseline = _run_task(runtime, task, discovery_experiences + round_index * len(tasks) + j, SkillConfig())
                if row["compose_task"] and not runtime.enable_composition:
                    composition_rows.append({
                        "seed": int(seed), "round": round_index + 1,
                        "arm": runtime.arm, "task_id": task.task_id,
                        "evaluation_role": "promotion_validation" if round_index == 2 else "heldout_confirmation",
                        "status": "disabled_by_preregistered_arm",
                    })
                elif row["compose_task"] and runtime.enable_composition:
                    candidate = runtime.composition
                    if candidate is None:
                        from .arms import propose_composition
                        candidate = propose_composition(runtime, SkillConfig())
                        runtime.composition = candidate
                    if candidate is not None:
                        macros: list[str] = []
                        for sid in candidate.order:
                            skill = runtime.library.get(sid)
                            if skill is not None:
                                macros.extend(_macro_for(skill))
                        comp_row = record_composition_task(runtime, task, baseline, macros, SkillConfig())
                        if comp_row is not None:
                            comp_row.update({"seed": int(seed), "round": round_index + 1, "arm": runtime.arm, "evaluation_role": "promotion_validation" if round_index == 2 else "heldout_confirmation"})
                            composition_rows.append(comp_row)
                    else:
                        composition_rows.append({
                            "seed": int(seed), "round": round_index + 1,
                            "arm": runtime.arm, "task_id": task.task_id,
                            "evaluation_role": "promotion_validation" if round_index == 2 else "heldout_confirmation",
                            "status": "unavailable_no_learned_proposal",
                        })
                task_rows.append({"seed": int(seed), **row})
                utilities.append(float(row["task_utility"]))
            task_clock = discovery_experiences + (round_index + 1) * len(tasks)
            lifecycle = _advance_storage_only_lifecycle(runtime, task_clock, SkillConfig())
            skill_lifecycle_rows.extend({"seed": int(seed), "round": round_index + 1, **item} for item in lifecycle)
            prior_live_caps = 0 if runtime.mask_growth else sum(1 for c in runtime.capabilities.list_capabilities() if c.state.value != "archived")
            formation = form_capabilities(runtime, config=capability_config_from_json(cfg))
            if runtime.mask_growth:
                new_caps = 0
            else:
                live_caps = sum(1 for c in runtime.capabilities.list_capabilities() if c.state.value != "archived")
                new_caps = max(0, live_caps - prior_live_caps)
            if not runtime.mask_growth:
                formation_rows.extend({"seed": int(seed), "round": round_index + 1, "arm": runtime.arm, **f} for f in formation)
            previous_row = next((r for r in reversed(seed_round_rows) if r["arm"] == runtime.arm), None)
            previous = previous_row["_next_state"] if previous_row else None
            summary = summarize_round(
                runtime,
                round_index=round_index,
                previous=previous,
                experiences=discovery_experiences + (round_index + 1) * len(tasks),
                task_utility_mean=sum(utilities) / len(utilities) if utilities else 0.0,
                new_capabilities=new_caps,
                config=cfg,
            )
            summary["seed"] = int(seed)
            seed_round_rows.append(summary)
    # Remove internal hand-off state from persisted public records.
    for row in seed_round_rows:
        row.pop("_next_state", None)
    robustness = run_isolated_robustness(
        runtimes["ASFT"],
        capability_config=capability_config_from_json(cfg),
        growth_config=growth_config_from_json(cfg),
    )
    return {
        "seed": int(seed),
        "trace_count": len(discovery["trace_run"].traces),
        "invariant_candidate_count": len(discovery["invariant_run"].candidates),
        "promotable_count": len(discovery["invariant_run"].promotable),
        "qualified_candidate_count": len(discovery["candidates"]),
        "candidate_rejections": discovery["rejected"],
        "round_rows": seed_round_rows,
        "task_rows": task_rows,
        "composition_rows": composition_rows,
        "formation_rows": formation_rows,
        "skill_lifecycle_rows": skill_lifecycle_rows,
        "robustness": robustness,
    }


def run_confirmation(config: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = config or load_config()
    return {
        "experiment_id": cfg["experiment_id"],
        "config": cfg,
        "seeds": [run_seed(seed, cfg) for seed in cfg["seeds"]],
    }
