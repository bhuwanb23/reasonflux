"""Frozen ten-seed Phase-13D experiment execution and aggregation."""
from __future__ import annotations
import json
from collections import defaultdict
from statistics import mean
from typing import Any
from .common import OUT_DIR, load_config, validate_config
from capability import (CapabilityConfig, CapabilityLibrary, compute_system_capability_state,
                        propose_capabilities_from_library)
from solver.tasks import GridTask
from solver.grid import count_objects
from transfer.reuse_engine import ReuseEngine
from skills.library import SkillLibrary
from .baselines import compression_library
from .policies import init_policy_state, run_policy
from .statistics import metric_bundle, summarize, clustered_pearson
from .task_programs import experiment_ids, make_experiment_tasks, source_skill_ops
from .tasks import train_seed

POLICIES = ["B1_NO_LEARNING", "B2_MEMORY_ONLY", "B3_RANDOM_SKILLS", "B4_COMPRESSION_PROXY",
            "A1_NO_INVARIANTS", "ASFT", "A2_NO_SCT", "A3_NO_PERSISTENCE", "A4_NO_COMPOSITION", "BEST_SINGLE"]


def _seed_cell_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return metric_bundle(rows)


def _safe_reflection_retrieval(pool: list[dict[str, Any]], task) -> dict[str, Any]:
    library = SkillLibrary()
    reflections = [item for item in pool if item["op"] == "apply_reflection"]
    for item in reflections:
        library.add(item["skill"])
    wrapper = GridTask(task_id=task.task_id, task_family="counting", input_grid=task.input_grid,
                       expected=count_objects(task.input_grid), difficulty=0.35, variant=0,
                       metadata={"symmetric": False})
    retrieved = ReuseEngine(library).retrieve(wrapper)
    return {"policy": "SAFE_RETRIEVAL_GUARD", "task_id": task.task_id,
            "reflection_candidates": len(reflections), "rejected": (retrieved is None) if reflections else None,
            "retrieved_skill_id": retrieved.skill_id if retrieved else None,
            "status": "evaluated" if reflections else "unavailable_missing_reflection_skill"}


def run_seed(seed: int, config: dict[str, Any] | None = None) -> dict[str, Any]:
    config = config or load_config()
    validate_config(config)
    trained = train_seed(seed, config)
    pool, examples = trained["pool"], trained["examples"]
    compression = compression_library(examples, slot_budget=len(pool))
    literal_examples = examples[:len(pool)]
    n = int(config["tasks"]["evaluation_tasks_per_cell"])
    task_rows: list[dict[str, Any]] = []
    cell_summaries: list[dict[str, Any]] = []
    training_ids = set(trained["training_task_ids"])
    all_eval_ids: set[str] = set()
    cap_library = CapabilityLibrary()
    previous_c: float | None = None
    previous_cgr: float | None = None
    growth: list[dict[str, Any]] = []
    skill_points: list[dict[str, Any]] = []
    for experiment_id in experiment_ids():
        tasks = make_experiment_tasks(experiment_id, seed, n=n)
        ids = {t.task_id for t in tasks}
        if len(ids) != len(tasks) or ids & training_ids or ids & all_eval_ids:
            raise AssertionError(f"task ID collision in {experiment_id}, seed={seed}")
        all_eval_ids |= ids
        state_policies = POLICIES + ["EXP15_FORCED_REFLECTION", "EXP16_RANDOM_FORCED", "EXP17_WRONG_COMPOSITION"]
        cell_slot = int(experiment_id[-2:])
        states = {policy: init_policy_state(
                    pool, policy,
                    random_seed=seed + int(config["tasks"]["random_policy_seed_offset"]) + cell_slot * 101 + index)
                  for index, policy in enumerate(state_policies)}
        cell_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for task in tasks:
            for policy in POLICIES:
                allow_composition = policy in {"ASFT", "A2_NO_SCT"} and len(task.ops) > 1
                arm_examples = literal_examples if policy == "A1_NO_INVARIANTS" else examples
                row = run_policy(task, policy, pool, arm_examples, compression, state=states[policy],
                                 allow_composition=allow_composition)
                required_source_ops = source_skill_ops(experiment_id)
                available_ops = {s["op"] for s in states["ASFT"]["skills"]}
                source_coverage = (bool(available_ops) if experiment_id == "EXP-TR-16" else
                                   all(op in available_ops for op in required_source_ops))
                row.update({"run_seed": seed, "source_skill_coverage": source_coverage,
                    "required_source_ops": list(required_source_ops),
                    "missing_source_skill_ops": [op for op in required_source_ops if op not in available_ops],
                    "status": "evaluated"})
                cell_rows[policy].append(row)
                task_rows.append(row)
            if experiment_id == "EXP-TR-15":
                row = run_policy(task, "EXP15_FORCED_REFLECTION", pool, examples, compression,
                                 state=states["EXP15_FORCED_REFLECTION"])
                available = bool(row["assigned_application"])
                row.update({"run_seed": seed, "status": "forced_negative_diagnostic" if available else "unavailable_missing_reflection_skill"})
                if available:
                    cell_rows["EXP15_FORCED_REFLECTION"].append(row)
                else:
                    row.update({"P_before": None, "P_after": None, "correct_after": None, "transfer_steps": None})
                task_rows.append(row)
                safe = _safe_reflection_retrieval(pool, task)
                safe.update({"run_seed": seed, "experiment_id": experiment_id, "taxonomy": "negative"})
                task_rows.append(safe)
            elif experiment_id == "EXP-TR-16":
                row = run_policy(task, "EXP16_RANDOM_FORCED", pool, examples, compression,
                                 state=states["EXP16_RANDOM_FORCED"])
                available = bool(row["assigned_application"])
                row.update({"run_seed": seed, "status": "forced_random_diagnostic" if available else "unavailable_missing_random_skill"})
                if available:
                    cell_rows["EXP16_RANDOM_FORCED"].append(row)
                else:
                    row.update({"P_before": None, "P_after": None, "correct_after": None, "transfer_steps": None})
                task_rows.append(row)
            elif experiment_id == "EXP-TR-17":
                row = run_policy(task, "EXP17_WRONG_COMPOSITION", pool, examples, compression,
                                 state=states["EXP17_WRONG_COMPOSITION"])
                available = bool(row["assigned_application"])
                row.update({"run_seed": seed, "status": "forced_wrong_composition_diagnostic" if available else "unavailable_missing_wrong_component_skills"})
                if available:
                    cell_rows["EXP17_WRONG_COMPOSITION"].append(row)
                else:
                    row.update({"P_before": None, "P_after": None, "correct_after": None, "transfer_steps": None})
                task_rows.append(row)
        for policy, rows in cell_rows.items():
            metrics = _seed_cell_metrics(rows)
            cell_summaries.append({"run_seed": seed, "experiment_id": experiment_id,
                                   "policy": policy, "metrics": metrics,
                                   "required_ops": list(tasks[0].ops),
                                   "available_skill_ops": sorted({s["op"] for s in states.get(policy, states["ASFT"])["skills"]})})
        asft_library = states["ASFT"]["library"]
        for capability in propose_capabilities_from_library(asft_library, config=CapabilityConfig(), require_valid=True):
            if cap_library.get(capability.capability_id) is None:
                cap_library.add(capability)
        if len(cap_library):
            snapshot = compute_system_capability_state(cap_library, asft_library,
                config=CapabilityConfig(), previous_score=previous_c, previous_cgr=previous_cgr,
                dt=1.0, refresh_portfolio=True)
            current_c = float(snapshot.capability_score)
            current_cgr = float(snapshot.cgr) if previous_c is not None else None
            status = "evaluated" if current_cgr is not None else "evaluated_initial_CGR_unavailable"
            previous_c, previous_cgr = current_c, current_cgr
        else:
            current_c, current_cgr, status = None, None, "unavailable_no_valid_capability"
        growth.append({"run_seed": seed, "experiment_id": experiment_id,
                       "C_t": current_c, "CGR": current_cgr, "capability_count": len(cap_library),
                       "status": status})
        asft_rows = cell_rows.get("ASFT", [])
        mean_ts = mean([float(r["P_after"]) - float(r["P_before"]) for r in asft_rows]) if asft_rows else None
        for item in states["ASFT"]["skills"]:
            sid = item["skill"].skill_id
            relevant = [r for r in asft_rows if sid in r.get("reused_skill_ids", [])]
            if relevant:
                skill_points.append({"run_seed": seed, "experiment_id": experiment_id,
                    "skill_id": sid, "IS": item["IS"], "SU": float(item["skill"].utility or 0.0),
                    "mean_TS": mean([float(r["P_after"]) - float(r["P_before"]) for r in relevant]),
                    "n_tasks": len(relevant)})
        asft_summary = next((item for item in reversed(cell_summaries)
                             if item["experiment_id"] == experiment_id and item["policy"] == "ASFT"), None)
        if asft_summary is not None:
            asft_summary["mean_ASFT_TS_for_growth"] = mean_ts
    return {"run_seed": seed, "task_rows": task_rows, "cell_summaries": cell_summaries,
            "growth": growth, "skill_points": skill_points,
            "training": {"n_traces": len(trained["trace_run"].traces),
                         "n_candidates": len(trained["mined"].mining.candidates),
                         "n_promotable": len(trained["mined"].promotable),
                         "n_eligible_skills": len(pool), "rejected": trained["rejected"],
                         "skills": [{"skill_id": x["skill"].skill_id, "op": x["op"],
                                     "source_family": x["source_family"], "IS": x["IS"],
                                     "SCV10": x["SCV10"], "signature": x["signature"]} for x in pool]}}


def aggregate(seed_results: list[dict[str, Any]]) -> dict[str, Any]:
    seed_cell: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    by_seed: dict[tuple[int, str, str], dict[str, Any]] = {}
    for result in seed_results:
        for item in result["cell_summaries"]:
            key = (item["experiment_id"], item["policy"])
            seed_cell[key].append(item)
            by_seed[(item["run_seed"], item["experiment_id"], item["policy"])] = item["metrics"]
    cells = {}
    for (exp, policy), entries in sorted(seed_cell.items()):
        metric_names = ["TS", "exact_accuracy", "RCR_steps", "RCR_normalized", "success_gated_fractional_RCR", "TU", "ITS",
                        "reuse_rate", "transfer_success_rate", "NTR_accuracy", "NTR_harm",
                        "operations_count", "retrieval_candidates_evaluated"]
        summary = {"n_seeds": len(entries), "per_seed": {}}
        for metric in metric_names:
            values = []
            for entry in entries:
                raw = entry["metrics"].get(metric)
                if metric == "TS" and isinstance(raw, dict):
                    raw = raw.get("mean")
                if isinstance(raw, (int, float)):
                    values.append(float(raw))
            summary[metric] = summarize(values, seed=13004 + len(exp) + len(policy))
            summary["per_seed"][metric] = values
        summary["solver_search_candidates"] = {"status": "unavailable",
            "reason": "legacy GridSolver exposes no canonical candidate-evaluation counter"}
        cells[f"{exp}|{policy}"] = summary
    comparisons = {}
    exps = sorted({exp for exp, _ in seed_cell})
    for exp in exps:
        base = {seed: by_seed[(seed, exp, "B1_NO_LEARNING")]["TS"]["mean"]
                for seed, e, p in by_seed if e == exp and p == "B1_NO_LEARNING"}
        for policy in [p for e, p in seed_cell if e == exp and p != "B1_NO_LEARNING"]:
            effects = [by_seed[(seed, exp, policy)]["TS"]["mean"] - base[seed]
                       for seed in base if (seed, exp, policy) in by_seed]
            stat = summarize(effects, seed=13077)
            dz = (float(stat["mean"]) / float(stat["sd"])) if stat["mean"] is not None and stat["sd"] not in (None, 0) else None
            comparisons[f"{exp}|{policy}-B1"] = {**stat, "per_seed": effects, "paired_cohens_dz": dz,
                "beats_baseline": bool(stat["ci95"][0] is not None and stat["ci95"][0] > 0)}
    ablations = {}
    for exp in exps:
        if (exp, "ASFT") not in seed_cell:
            continue
        for policy in ["A1_NO_INVARIANTS", "A2_NO_SCT", "A3_NO_PERSISTENCE", "A4_NO_COMPOSITION"]:
            if (exp, policy) not in seed_cell:
                continue
            effects = [by_seed[(seed, exp, "ASFT")]["TS"]["mean"] - by_seed[(seed, exp, policy)]["TS"]["mean"]
                       for seed, e, p in by_seed if e == exp and p == "ASFT" and (seed, exp, policy) in by_seed]
            stat = summarize(effects, seed=13078)
            dz = (float(stat["mean"]) / float(stat["sd"])) if stat["mean"] is not None and stat["sd"] not in (None, 0) else None
            ablations[f"{exp}|ASFT-minus-{policy}"] = {**stat, "per_seed": effects, "paired_cohens_dz": dz,
                "degradation": bool(stat["ci95"][0] is not None and stat["ci95"][0] > 0)}
    growth_points = []
    for result in seed_results:
        for item in result["growth"]:
            if item["CGR"] is not None:
                match = next((x for x in result["cell_summaries"] if x["experiment_id"] == item["experiment_id"] and x["policy"] == "ASFT"), None)
                if match and match.get("mean_ASFT_TS_for_growth") is not None:
                    growth_points.append({"run_seed": result["run_seed"],
                                          "mean_TS": float(match["mean_ASFT_TS_for_growth"]),
                                          "CGR": float(item["CGR"])})
    skill_points = [p for result in seed_results for p in result["skill_points"]]
    correlations = {
        "IS_vs_TS": clustered_pearson(skill_points, "IS", "mean_TS"),
        "SU_vs_TS": clustered_pearson(skill_points, "SU", "mean_TS"),
        "TS_vs_CGR": clustered_pearson(growth_points, "mean_TS", "CGR"),
    }
    return {"cells": cells, "baseline_comparisons": comparisons,
            "ablation_comparisons": ablations, "correlations": correlations,
            "growth_points_n": len(growth_points), "skill_points_n": len(skill_points)}
