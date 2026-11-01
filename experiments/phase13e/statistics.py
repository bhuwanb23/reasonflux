"""Seed-level statistics and preregistered decision rules for Phase 13E."""
from __future__ import annotations

import math
import random
from collections import defaultdict
from statistics import mean, stdev
from typing import Any, Iterable

T95_BY_DF = {1: 12.706205, 2: 4.302653, 3: 3.182446, 4: 2.776445, 5: 2.570582, 6: 2.446912, 7: 2.364624, 8: 2.306004, 9: 2.262157}
BOOTSTRAP_SEED = 87213


def summarize(values: Iterable[float | None]) -> dict[str, Any]:
    vals = [float(v) for v in values if v is not None and math.isfinite(float(v))]
    n = len(vals)
    avg = mean(vals) if vals else None
    sd = stdev(vals) if n > 1 else (0.0 if n == 1 else None)
    critical = T95_BY_DF.get(n - 1, 1.96) if n > 1 else None
    half = critical * sd / math.sqrt(n) if critical is not None else None
    return {"n": n, "mean": avg, "sd": sd, "ci95_low": avg - half if half is not None else None, "ci95_high": avg + half if half is not None else None}


def pearson(x: list[float], y: list[float]) -> float | None:
    if len(x) != len(y) or len(x) < 3:
        return None
    mx, my = mean(x), mean(y)
    dx, dy = [v - mx for v in x], [v - my for v in y]
    denom = math.sqrt(sum(v * v for v in dx) * sum(v * v for v in dy))
    return sum(a * b for a, b in zip(dx, dy)) / denom if denom > 1e-12 else None


def _fisher_ci(rvalue: float | None, n: int) -> tuple[float | None, float | None]:
    if rvalue is None or n <= 3:
        return None, None
    r = max(-0.999999, min(0.999999, float(rvalue)))
    z = 0.5 * math.log((1.0 + r) / (1.0 - r))
    half = 1.96 / math.sqrt(n - 3)
    return math.tanh(z - half), math.tanh(z + half)


def flatten(run: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    rounds: list[dict[str, Any]] = []
    tasks: list[dict[str, Any]] = []
    comps: list[dict[str, Any]] = []
    formations: list[dict[str, Any]] = []
    robustness: list[dict[str, Any]] = []
    lifecycle: list[dict[str, Any]] = []
    for seed in run["seeds"]:
        rounds.extend(seed["round_rows"])
        tasks.extend(seed["task_rows"])
        comps.extend(seed["composition_rows"])
        formations.extend(seed["formation_rows"])
        robustness.append({"seed": int(seed["seed"]), **seed.get("robustness", {})})
        lifecycle.extend(seed.get("skill_lifecycle_rows", []))
    return rounds, tasks, comps, formations, robustness, lifecycle


def _by_seed_arm(rows: list[dict[str, Any]]) -> dict[tuple[int, str], list[dict[str, Any]]]:
    out: dict[tuple[int, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        out[(int(row["seed"]), str(row["arm"]))].append(row)
    return out


def build_analysis(run: dict[str, Any]) -> dict[str, Any]:
    rounds, tasks, comps, formations, robustness, lifecycle = flatten(run)
    round_index = _by_seed_arm(rounds)
    task_index = _by_seed_arm(tasks)
    comp_index = _by_seed_arm(comps)
    arms = sorted({str(r["arm"]) for r in rounds})
    seeds = sorted({int(r["seed"]) for r in rounds})
    metric_names = ["ct", "cgr", "capu", "portfolio_coverage", "supported_family_coverage", "mean_skill_utility_su", "mean_transfer_score_ts", "ig", "igr", "ie", "task_utility", "n_capabilities", "new_capabilities", "fragmentation_ratio", "saturation_ratio", "composition_skill_count", "ccg", "ug"]
    arm_metrics: list[dict[str, Any]] = []
    seed_summaries: list[dict[str, Any]] = []
    for arm in arms:
        arm_seed_rows = []
        for seed in seeds:
            rs = sorted(round_index.get((seed, arm), []), key=lambda r: int(r["round"]))
            if not rs:
                continue
            tr = task_index.get((seed, arm), [])
            cs = comp_index.get((seed, arm), [])
            seed_row: dict[str, Any] = {"seed": seed, "arm": arm}
            for metric in metric_names:
                vals = [r.get(metric) for r in rs]
                finite = [float(v) for v in vals if v is not None]
                seed_row[f"mean_{metric}"] = mean(finite) if finite else None
                seed_row[f"final_{metric}"] = rs[-1].get(metric)
            utilities = [float(t["task_utility"]) for t in tr]
            seed_row["mean_task_utility_all_tasks"] = mean(utilities) if utilities else None
            seed_row["valid_capability_any_round"] = any(int(r.get("n_capabilities", 0) or 0) > 0 for r in rs)
            seed_row["fragmentation_failure_any_round"] = any(
                any(str(f.get("kind")) == "fragmentation" for f in (r.get("representation_failures") or []))
                for r in rs
            )
            seed_row["stable_capability_two_rounds"] = any(
                bool(set(rs[i].get("capability_ids") or []) & set(rs[i + 1].get("capability_ids") or []))
                for i in range(len(rs) - 1)
            )
            seed_row["natural_saturation_last_two_rounds"] = len(rs) >= 4 and all(str(r.get("growth_state", "")) == "saturated" for r in rs[-2:])
            seed_row["monotonic_ct"] = all(
                rs[i + 1].get("ct") is not None and rs[i].get("ct") is not None and float(rs[i + 1]["ct"]) >= float(rs[i]["ct"])
                for i in range(len(rs) - 1)
            )
            evaluated = [c for c in cs if c.get("status") == "evaluated" and c.get("evaluation_role") == "heldout_confirmation"]
            validation = [c for c in cs if c.get("status") == "evaluated" and c.get("evaluation_role") == "promotion_validation"]
            ie_values = [float(r["ie"]) for r in rs if r.get("ie") is not None]
            ie_x = list(range(1, len(ie_values) + 1))
            ie_x_mean = mean(ie_x) if ie_x else 0.0
            seed_row["ie_slope"] = (sum((x - ie_x_mean) * (y - mean(ie_values)) for x, y in zip(ie_x, ie_values)) / sum((x - ie_x_mean) ** 2 for x in ie_x)) if len(ie_values) >= 2 else None
            seed_row["mean_composition_incremental_gain"] = mean(float(c["incremental_gain"]) for c in evaluated) if evaluated else None
            seed_row["composition_success_rate"] = mean(float(bool(c["success"])) for c in evaluated) if evaluated else None
            seed_row["mean_composition_validation_gain"] = mean(float(c["incremental_gain"]) for c in validation) if validation else None
            seed_row["mean_composition_count"] = seed_row.get("mean_composition_skill_count")
            arm_seed_rows.append(seed_row)
            seed_summaries.append(seed_row)
        for metric in metric_names + ["ie_slope", "mean_task_utility_all_tasks", "mean_composition_incremental_gain", "composition_success_rate", "mean_composition_validation_gain"]:
            custom_metrics = {"ie_slope", "mean_task_utility_all_tasks", "mean_composition_incremental_gain", "composition_success_rate", "mean_composition_validation_gain"}
            vals = [r.get(metric) if metric in custom_metrics else r.get(f"mean_{metric}") for r in arm_seed_rows]
            arm_metrics.append({"arm": arm, "metric": metric, **summarize(vals)})
    stats_by_arm = {(r["arm"], r["metric"]): r for r in arm_metrics}

    # Paired full-vs-baseline and full-vs-ablation contrasts, within seed.
    paired: list[dict[str, Any]] = []
    controls = ["B1_NO_LEARNING", "B2_SKILL_STORAGE_ONLY", "B3_RANDOM_SKILL_CREATION", "B4_COMPRESSION_PROXY"]
    for control in controls:
        for metric in ("final_ct", "mean_task_utility_all_tasks"):
            diffs = []
            for seed in seeds:
                a = next((r for r in seed_summaries if r["seed"] == seed and r["arm"] == "ASFT"), None)
                b = next((r for r in seed_summaries if r["seed"] == seed and r["arm"] == control), None)
                if a and b and a.get(metric) is not None and b.get(metric) is not None:
                    diffs.append(float(a[metric]) - float(b[metric]))
            paired.append({"contrast": f"ASFT - {control}", "metric": metric, **summarize(diffs)})
    for control in ("A1_NO_IDT", "A2_NO_SCT", "A3_NO_SKILL_LIBRARY", "A4_NO_COMPOSITION"):
        diffs = []
        for seed in seeds:
            a = next((r for r in seed_summaries if r["seed"] == seed and r["arm"] == "ASFT"), None)
            b = next((r for r in seed_summaries if r["seed"] == seed and r["arm"] == control), None)
            if a and b and a.get("mean_cgr") is not None and b.get("mean_cgr") is not None:
                diffs.append(float(a["mean_cgr"]) - float(b["mean_cgr"]))
        paired.append({"contrast": f"ASFT - {control}", "metric": "mean_cgr", **summarize(diffs)})

    # Preregistered seed-mean correlations, n=10 independent seed summaries.
    primary = [r for r in seed_summaries if r["arm"] == "ASFT"]
    correlation_specs = [
        ("TS_to_CGR", "mean_mean_transfer_score_ts", "mean_cgr"),
        ("SU_to_CGR", "mean_mean_skill_utility_su", "mean_cgr"),
        ("coverage_to_IG", "mean_supported_family_coverage", "mean_ig"),
        ("composition_to_IG", "mean_composition_skill_count", "mean_ig"),
    ]
    correlations = []
    for name, xkey, ykey in correlation_specs:
        pairs = [(r.get(xkey), r.get(ykey)) for r in primary if r.get(xkey) is not None and r.get(ykey) is not None]
        x = [float(p[0]) for p in pairs]
        y = [float(p[1]) for p in pairs]
        rvalue = pearson(x, y)
        ci_low, ci_high = _fisher_ci(rvalue, len(pairs))
        correlations.append({"correlation": name, "x": xkey, "y": ykey, "n": len(pairs), "pearson_r": rvalue, "ci95_low": ci_low, "ci95_high": ci_high, "ci_method": "Fisher z", "status": "available" if rvalue is not None else "unavailable_constant_or_insufficient"})
    accepted_caps: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in formations:
        if row.get("arm") == "ASFT" and row.get("accepted"):
            accepted_caps[int(row["seed"])].append(row)
    cap_value_rows = []
    for seed in seeds:
        rows = accepted_caps.get(seed, [])
        cap_value_rows.append({
            "seed": seed,
            "capu": mean(float(r["utility"]) for r in rows) if rows else None,
            "member_ts": mean(float(r["mean_member_ts"]) for r in rows if r.get("mean_member_ts") is not None) if any(r.get("mean_member_ts") is not None for r in rows) else None,
            "member_reuse": mean(float(r["mean_member_reuse_count"]) for r in rows if r.get("mean_member_reuse_count") is not None) if any(r.get("mean_member_reuse_count") is not None for r in rows) else None,
        })
    for name, key in (("capability_utility_to_transfer", "member_ts"), ("capability_utility_to_reuse", "member_reuse")):
        pairs = [(r["capu"], r[key]) for r in cap_value_rows if r["capu"] is not None and r[key] is not None]
        rvalue = pearson([float(p[0]) for p in pairs], [float(p[1]) for p in pairs])
        ci_low, ci_high = _fisher_ci(rvalue, len(pairs))
        correlations.append({"correlation": name, "x": "per_seed_mean_capability_utility", "y": f"per_seed_mean_{key}", "n": len(pairs), "pearson_r": rvalue, "ci95_low": ci_low, "ci95_high": ci_high, "ci_method": "Fisher z", "status": "available" if rvalue is not None else "unavailable_constant_or_insufficient"})

    # Three next-round prediction pairs per seed; resample whole seeds to retain clustering.
    pred_clusters: list[list[tuple[float, float]]] = []
    for seed in seeds:
        rs = sorted(round_index.get((seed, "ASFT"), []), key=lambda r: int(r["round"]))
        pairs = [(float(rs[i]["ct"]), float(rs[i + 1]["task_utility"])) for i in range(min(3, len(rs) - 1)) if rs[i].get("ct") is not None]
        if pairs:
            pred_clusters.append(pairs)
    pred_pairs = [p for group in pred_clusters for p in group]
    pred_r = pearson([p[0] for p in pred_pairs], [p[1] for p in pred_pairs])
    rng = random.Random(BOOTSTRAP_SEED)
    boot: list[float] = []
    if len(pred_clusters) >= 5:
        for _ in range(4000):
            sampled = [pred_clusters[rng.randrange(len(pred_clusters))] for _ in pred_clusters]
            vals = [p for group in sampled for p in group]
            r = pearson([p[0] for p in vals], [p[1] for p in vals])
            if r is not None:
                boot.append(r)
    pred = {
        "n_seed_clusters": len(pred_clusters),
        "n_seed_round_pairs": len(pred_pairs),
        "pearson_r": pred_r,
        "ci95_low": sorted(boot)[int(0.025 * (len(boot) - 1))] if boot else None,
        "ci95_high": sorted(boot)[int(0.975 * (len(boot) - 1))] if boot else None,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "bootstrap_replicates": 4000,
        "status": "available" if pred_r is not None and boot else "unavailable_insufficient_or_constant",
    }

    # Fixed acceptance criteria, evaluated without outcome-dependent thresholds.
    decisions: list[dict[str, Any]] = []
    for item in correlations:
        rvalue = item.get("pearson_r")
        decisions.append({"criterion": f"{item['correlation']}_directional_association", "observed_r": rvalue, "ci95_low": item.get("ci95_low"), "ci95_high": item.get("ci95_high"), "n": item.get("n"), "status": "positive_descriptive" if rvalue is not None and float(rvalue) > 0 else "not_positive_or_unavailable"})
    emergence = sum(1 for r in primary if r.get("stable_capability_two_rounds"))
    decisions.append({"criterion": "replicated_capability_emergence", "observed": f"{emergence}/10 seeds with a capability persisting across consecutive rounds", "threshold": "at least 8/10", "status": "pass" if emergence >= 8 else "fail"})
    post_comp_growth = 0
    for seed in seeds:
        rs = sorted(round_index.get((seed, "ASFT"), []), key=lambda r: int(r["round"]))
        cs = [c for c in comp_index.get((seed, "ASFT"), []) if c.get("status") == "evaluated" and c.get("evaluation_role") == "heldout_confirmation" and c.get("success")]
        if len(rs) >= 4 and cs and int(rs[3].get("n_capabilities", 0) or 0) > int(rs[1].get("n_capabilities", 0) or 0):
            post_comp_growth += 1
    decisions.append({"criterion": "EXP-CAP-12_postcomposition_capability_count_growth", "observed": f"{post_comp_growth}/10 seeds had more capabilities in round 4 than round 2 with a successful held-out composition", "status": "descriptive_not_a_pass_gate"})
    emergent_ids = {(int(r["seed"]), str(r.get("capability_id"))) for r in formations if r.get("arm") == "ASFT" and r.get("accepted") and r.get("type") == "emergent"}
    decisions.append({"criterion": "EXP-CAP-14_higher_order_emergent_capability", "observed": f"{len(emergent_ids)} seed-capability occurrences with accepted emergent type", "status": "available" if emergent_ids else "unavailable_no_valid_higher_order_cluster"})
    for metric, label in [("cgr", "positive_CGR"), ("ig", "positive_IG"), ("igr", "positive_IGR"), ("ccg", "positive_coverage_growth"), ("ug", "positive_utility_growth"), ("ie_slope", "positive_IE_trend")]:
        result = stats_by_arm.get(("ASFT", metric), {})
        lo = result.get("ci95_low")
        ok = result.get("mean") is not None and float(result["mean"]) > 0 and lo is not None and float(lo) > 0
        decisions.append({"criterion": label, "observed_mean": result.get("mean"), "ci95_low": lo, "status": "pass" if ok else "fail_or_null"})
    for control in controls:
        matches = [r for r in paired if r["contrast"] == f"ASFT - {control}"]
        ok = len(matches) == 2 and all(r.get("ci95_low") is not None and float(r["ci95_low"]) > 0 for r in matches)
        decisions.append({"criterion": f"ASFT_beats_{control}", "metrics": {r["metric"]: {"mean": r.get("mean"), "ci95_low": r.get("ci95_low")} for r in matches}, "status": "pass" if ok else "fail_or_null"})
    for control in ("A1_NO_IDT", "A2_NO_SCT", "A3_NO_SKILL_LIBRARY", "A4_NO_COMPOSITION"):
        result = next((r for r in paired if r["contrast"] == f"ASFT - {control}" and r["metric"] == "mean_cgr"), {})
        decisions.append({"criterion": f"ablation_reduces_growth_{control}", "observed_mean_difference": result.get("mean"), "ci95_low": result.get("ci95_low"), "status": "pass" if result.get("ci95_low") is not None and float(result["ci95_low"]) > 0 else "fail_or_null"})
    comp_vals = [r.get("mean_composition_incremental_gain") for r in primary]
    comp_summary = summarize(comp_vals)
    decisions.append({"criterion": "composition_creates_value", "observed_mean": comp_summary["mean"], "ci95_low": comp_summary["ci95_low"], "status": "pass" if comp_summary["ci95_low"] is not None and float(comp_summary["ci95_low"]) > 0 else "fail_or_null_or_unavailable"})
    decisions.append({"criterion": "A5_NO_CGM", "status": "unavailable_by_design", "reason": "A5 preserves ASFT behavior and masks all growth measurements"})
    decisions.append({"criterion": "growth_predicts_future_performance", "observed_r": pred["pearson_r"], "ci95_low": pred["ci95_low"], "status": "pass" if pred["ci95_low"] is not None and float(pred["ci95_low"]) > 0 else "fail_or_null_or_unavailable"})
    monotonic = sum(1 for r in primary if r.get("monotonic_ct"))
    decisions.append({"criterion": "trajectory_monotonicity_descriptive", "observed": f"{monotonic}/10 seeds", "status": "descriptive_not_a_pass_gate"})
    saturated = sum(1 for r in primary if r.get("natural_saturation_last_two_rounds"))
    decisions.append({"criterion": "EXP-CAP-20_natural_saturation", "observed": f"{saturated}/10 seeds saturated in both final rounds by the frozen CGM classifier", "status": "descriptive_not_a_pass_gate"})
    fragmented = sum(1 for r in primary if r.get("fragmentation_failure_any_round"))
    decisions.append({"criterion": "EXP-CAP-19_fragmentation", "observed": f"{fragmented}/10 ASFT seeds had a frozen representation-audit fragmentation failure", "status": "descriptive_not_a_pass_gate"})
    regression_rows = [r.get("regression", {}) for r in robustness]
    regression_eval = [r for r in regression_rows if r.get("status") == "evaluated"]
    regression_detected = sum(1 for r in regression_eval if r.get("decrease_detected"))
    decisions.append({"criterion": "EXP-CAP-21_regression_probe", "observed": f"{regression_detected}/{len(regression_eval)} evaluated probes detected decline", "status": "reported_not_a_cohort_pass_gate" if regression_eval else "unavailable"})
    illusion_rows = [r.get("growth_illusion", {}) for r in robustness]
    illusion_eval = [r for r in illusion_rows if r.get("status") == "evaluated" and not r.get("baseline_empty")]
    illusion_pass = sum(1 for r in illusion_eval if r.get("unchanged_within_tolerance"))
    decisions.append({"criterion": "EXP-CAP-22_dummy_skill_invariance", "observed": f"{illusion_pass}/{len(illusion_eval)} evaluated probes unchanged", "status": "reported_not_a_cohort_pass_gate" if illusion_eval else "unavailable"})

    return {
        "arm_metrics": arm_metrics,
        "seed_summaries": seed_summaries,
        "paired_contrasts": paired,
        "correlations": correlations,
        "prediction": pred,
        "robustness": robustness,
        "decisions": decisions,
        "flattened": {"rounds": rounds, "tasks": tasks, "composition": comps, "formations": formations, "robustness": robustness, "skill_lifecycle": lifecycle},
    }
