"""Seed-level Phase 13F summaries, paired effects, and criterion decisions."""
from __future__ import annotations

import math
import random
from statistics import mean, stdev
from typing import Any

from experiments.phase13e.statistics import summarize

BASELINES = ["B1_NO_LEARNING", "B2_MEMORY_SKILL_STORE", "B3_RANDOM_SKILL_CREATION", "B4_COMPRESSION_PROXY"]
ABLATIONS = ["A1_NO_IDT", "A1_1_FREQUENCY_ONLY", "A2_NO_SCV", "A2_1_RANDOM_SCV", "A2_2_NO_LIFECYCLE", "A2_3_NO_COMPOSITION", "A3_NO_CAPABILITY_LAYER", "A3_1_NO_GROWTH_TRACKING", "A3_2_INDEPENDENT_CAPABILITIES", "X1_NO_TRANSFER", "X2_NO_SKILL_LIBRARY", "X3_NO_EXPERIENCE_MEMORY", "X4_NO_CAPABILITY_FORMATION"]
METRICS = ["IS", "SU", "TS", "cgr", "ig", "portfolio_coverage", "task_utility", "skill_count_created"]


def _flatten(run: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    out = {key: [] for key in ("rounds", "tasks", "composition", "formation", "lifecycle")}
    for seed in run["seeds"]:
        out["rounds"].extend(seed.get("round_rows", []))
        out["tasks"].extend(seed.get("task_rows", []))
        out["composition"].extend(seed.get("composition_rows", []))
        out["formation"].extend(seed.get("formation_rows", []))
        out["lifecycle"].extend(seed.get("lifecycle_rows", []))
    return out


def _mean(values: list[Any]) -> float | None:
    xs = [float(x) for x in values if x is not None and math.isfinite(float(x))]
    return mean(xs) if xs else None


def _effect(diffs: list[float]) -> dict[str, Any]:
    result = summarize(diffs)
    n = result["n"]
    sd = result["sd"]
    dz = (result["mean"] / sd) if sd not in (None, 0.0) else None
    df = n - 1
    correction = 1.0 - 3.0 / (4.0 * df - 1.0) if df > 0 else None
    result["cohen_dz"] = dz
    result["hedges_g"] = dz * correction if dz is not None and correction is not None else None
    result["effect_size_status"] = "available" if dz is not None else "undefined_zero_or_insufficient_sd"
    return result


def _seed_summary(flat: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    index: dict[tuple[int, str], list[dict[str, Any]]] = {}
    for row in flat["rounds"]:
        index.setdefault((int(row["seed"]), str(row["arm"])), []).append(row)
    tasks: dict[tuple[int, str], list[dict[str, Any]]] = {}
    for row in flat["tasks"]:
        tasks.setdefault((int(row["seed"]), str(row["arm"])), []).append(row)
    out = []
    for (seed, arm), rows in sorted(index.items()):
        item: dict[str, Any] = {"seed": seed, "arm": arm}
        for metric in METRICS:
            item[f"mean_{metric}"] = _mean([r.get(metric) for r in rows])
            item[f"final_{metric}"] = next((r.get(metric) for r in sorted(rows, key=lambda x: x["round"], reverse=True) if r.get(metric) is not None), None)
        task_rows = tasks.get((seed, arm), [])
        item["mean_task_utility_all_tasks"] = _mean([r.get("task_utility") for r in task_rows])
        item["mean_compose_task_utility"] = _mean([r.get("task_utility") for r in task_rows if r.get("compose_task")])
        comp_rows = [r for r in flat["composition"] if int(r.get("seed", -1)) == seed and r.get("arm") == arm and r.get("evaluation_role") == "heldout_confirmation" and r.get("incremental_gain") is not None]
        item["mean_heldout_composition_incremental_gain"] = _mean([r.get("incremental_gain") for r in comp_rows])
        item["success_rate"] = _mean([float(bool(r.get("observed_success"))) for r in task_rows])
        item["mean_skill_count_persistent"] = _mean([r.get("skill_count_persistent") for r in rows])
        item["n_tasks"] = len(task_rows)
        out.append(item)
    return out


def build_analysis(run: dict[str, Any]) -> dict[str, Any]:
    flat = _flatten(run)
    summaries = _seed_summary(flat)
    arms = sorted({str(r["arm"]) for r in summaries})
    metrics = METRICS + ["mean_task_utility_all_tasks", "mean_compose_task_utility", "mean_heldout_composition_incremental_gain", "success_rate", "mean_skill_count_persistent"]
    arm_metrics = []
    for arm in arms:
        rows = [r for r in summaries if r["arm"] == arm]
        for metric in metrics:
            values = [r.get(f"mean_{metric}") if metric in METRICS else r.get(metric) for r in rows]
            arm_metrics.append({"arm": arm, "metric": metric, **summarize(values)})
    by_seed = {(r["seed"], r["arm"]): r for r in summaries}
    contrasts = []
    comparisons = BASELINES + ABLATIONS
    for other in comparisons:
        for metric in ("mean_task_utility_all_tasks", "mean_compose_task_utility", "mean_heldout_composition_incremental_gain", "mean_cgr", "mean_ig", "mean_TS", "mean_SU", "mean_IS"):
            diffs = [float(by_seed[(s, "ASFT")][metric]) - float(by_seed[(s, other)][metric])
                     for s in sorted({r["seed"] for r in summaries})
                     if by_seed.get((s, "ASFT"), {}).get(metric) is not None and by_seed.get((s, other), {}).get(metric) is not None]
            contrasts.append({"contrast": f"ASFT - {other}", "metric": metric, **_effect(diffs)})
    decisions = []
    for other in BASELINES:
        rows = [r for r in contrasts if r["contrast"] == f"ASFT - {other}" and r["metric"] in {"mean_task_utility_all_tasks", "mean_cgr"}]
        ok = len(rows) == 2 and all(r.get("ci95_low") is not None and r["ci95_low"] > 0 for r in rows)
        decisions.append({"criterion": f"ASFT_beats_{other}", "status": "pass" if ok else "fail_or_null", "outcomes": rows})
    for other in ABLATIONS:
        outcomes = {"mean_task_utility_all_tasks", "mean_cgr"}
        if other == "A2_3_NO_COMPOSITION":
            outcomes.add("mean_compose_task_utility")
        rows = [r for r in contrasts if r["contrast"] == f"ASFT - {other}" and r["metric"] in outcomes]
        positive = any(r.get("ci95_low") is not None and r["ci95_low"] > 0 for r in rows)
        decisions.append({"criterion": f"component_effect_{other}", "status": "positive_on_at_least_one_preregistered_outcome" if positive else "mixed_or_unavailable", "outcomes": rows})
    sensitivity = [r for r in arm_metrics if r["arm"].startswith("SENS_")]
    return {"flattened": flat, "seed_summaries": summaries, "arm_metrics": arm_metrics,
            "paired_contrasts": contrasts, "decisions": decisions, "sensitivity": sensitivity,
            "arms": arms, "seeds": sorted({r["seed"] for r in summaries})}
