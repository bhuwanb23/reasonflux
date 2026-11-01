"""Post-run reporting correction: read saved Phase-13D rows only; never reruns tasks."""
from __future__ import annotations
import csv
import json
from pathlib import Path
from statistics import mean
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from experiments.phase13d.statistics import summarize
SEEDS = list(range(50, 60))
CORE = [f"EXP-TR-{n:02d}" for n in range(1, 12)]
BASELINES = ["B1_NO_LEARNING", "B2_MEMORY_ONLY", "B3_RANDOM_SKILLS", "B4_COMPRESSION_PROXY"]


def read_inputs():
    runs = [json.loads((HERE / f"seed_{seed}.json").read_text()) for seed in SEEDS]
    rows = [json.loads(line) for line in (HERE / "task_level.jsonl").read_text().splitlines() if line]
    aggregate = json.loads((HERE / "aggregate_metrics.json").read_text())
    manifest = json.loads((HERE / "preregistration_hashes.json").read_text())
    if any(run.get("frozen_root_sha256") != manifest["root_sha256"] for run in runs):
        raise ValueError("seed checkpoint does not match frozen source/config/protocol hash")
    return runs, rows, aggregate, manifest


def cell_metrics(runs):
    out = {}
    for run in runs:
        seed = int(run["run_seed"])
        for item in run["cell_summaries"]:
            out[(seed, item["experiment_id"], item["policy"])] = item["metrics"]
    return out


def criterion(values):
    stats = summarize(values, seed=13201)
    positives = sum(float(v) > 0 for v in values)
    stable = bool(stats["n"] >= 10 and stats["mean"] is not None and stats["mean"] > 0
                  and stats["ci95"][0] is not None and stats["ci95"][0] > 0 and positives >= 8)
    stats.update({"positive_seeds": positives, "stable_positive": stable,
                  "status": "unavailable" if stats["n"] < 10 else ("passed" if stable else "failed")})
    return stats


def per_seed_effect(metrics, exp, policy_a, policy_b, metric="TS"):
    values = []
    for seed in SEEDS:
        a = metrics.get((seed, exp, policy_a), {}).get(metric)
        b = metrics.get((seed, exp, policy_b), {}).get(metric)
        if metric == "TS":
            a = a.get("mean") if isinstance(a, dict) else a
            b = b.get("mean") if isinstance(b, dict) else b
        if a is not None and b is not None:
            values.append(float(a) - float(b))
    return values


def main():
    runs, rows, frozen_aggregate, manifest = read_inputs()
    metrics = cell_metrics(runs)
    coverage = {}
    activity = {}
    for exp in CORE:
        for seed in SEEDS:
            subset = [r for r in rows if r.get("run_seed") == seed and r.get("experiment_id") == exp and r.get("policy") == "ASFT"]
            coverage[(seed, exp)] = bool(subset) and all(bool(r.get("source_skill_coverage")) for r in subset)
            activity[(seed, exp)] = {
                "source_coverage": coverage[(seed, exp)],
                "composition_candidates": sum(bool(r.get("composition_candidate")) for r in subset),
                "composition_active": sum(bool(r.get("composition_active")) for r in subset),
            }
    coverage_rows = []
    experiment_metrics = {}
    for exp in CORE:
        available = sum(coverage[(seed, exp)] for seed in SEEDS)
        ts_values = [metrics[(seed, exp, "ASFT")]["TS"]["mean"] for seed in SEEDS
                     if (seed, exp, "ASFT") in metrics]
        ts_stat = criterion(ts_values)
        if available == 0:
            status = "unavailable_missing_source_skill"
        else:
            status = ts_stat["status"]
        active = sum(activity[(seed, exp)]["composition_active"] for seed in SEEDS)
        candidates = sum(activity[(seed, exp)]["composition_candidates"] for seed in SEEDS)
        experiment_metrics[exp] = {"source_skill_coverage_seeds": available, "seed_count": len(SEEDS),
            "source_skill_coverage_rate": available / len(SEEDS), "ASFT_TS_full_cohort": ts_stat,
            "status": status, "composition_candidates": candidates,
            "composition_active_task_applications": active}
        coverage_rows.append({"experiment_id": exp, "covered_seeds": available, "total_seeds": len(SEEDS),
            "coverage_rate": available / len(SEEDS), "mean_ASFT_TS": ts_stat["mean"],
            "ASFT_TS_ci95_low": ts_stat["ci95"][0], "ASFT_TS_ci95_high": ts_stat["ci95"][1],
            "composition_candidates": candidates, "composition_active": active, "status": status})

    pairwise_rows = []
    per_exp_baselines = {}
    pooled_baselines = {}
    for baseline in BASELINES:
        per_seed = {seed: [] for seed in SEEDS}
        per_exp_baselines[baseline] = {}
        for exp in CORE:
            effects = per_seed_effect(metrics, exp, "ASFT", baseline)
            stat = summarize(effects, seed=13202)
            per_exp_baselines[baseline][exp] = {**stat, "per_seed": effects}
            for index, value in enumerate(effects):
                per_seed[SEEDS[index]].append(value)
            pairwise_rows.append({"experiment_id": exp, "contrast": f"ASFT - {baseline}",
                "mean_TS_difference": stat["mean"], "sd": stat["sd"],
                "ci95_low": stat["ci95"][0], "ci95_high": stat["ci95"][1], "n_seeds": stat["n"]})
        pooled = [mean(values) for values in per_seed.values() if values]
        pooled_baselines[baseline] = criterion(pooled)
    # Additional controls distinguish multiple individual skills from actual composition.
    comp_exps = [f"EXP-TR-{n:02d}" for n in range(7, 12)]
    comp_single = []
    comp_a4 = []
    comp_rcr = []
    comp_acc = []
    for seed in SEEDS:
        by_seed_ts = []
        by_seed_a4 = []
        by_seed_rcr = []
        by_seed_acc = []
        for exp in comp_exps:
            by_seed_ts.append(per_seed_effect(metrics, exp, "ASFT", "BEST_SINGLE")[seed - SEEDS[0]])
            by_seed_a4.append(per_seed_effect(metrics, exp, "ASFT", "A4_NO_COMPOSITION")[seed - SEEDS[0]])
            asft = metrics[(seed, exp, "ASFT")]
            best = metrics[(seed, exp, "BEST_SINGLE")]
            by_seed_rcr.append(float(asft["success_gated_fractional_RCR"]) - float(best["success_gated_fractional_RCR"]))
            by_seed_acc.append(float(asft["exact_accuracy"]) - float(best["exact_accuracy"]))
        comp_single.append(mean(by_seed_ts)); comp_a4.append(mean(by_seed_a4))
        comp_rcr.append(mean(by_seed_rcr)); comp_acc.append(mean(by_seed_acc))
    composition = {
        "ASFT_minus_best_single_TS_full_cohort": criterion(comp_single),
        "ASFT_minus_best_single_success_gated_RCR": criterion(comp_rcr),
        "ASFT_minus_best_single_exact_accuracy": summarize(comp_acc, seed=13203),
        "ASFT_minus_no_composition_TS": summarize(comp_a4, seed=13204),
        "composition_active_task_applications": sum(bool(r.get("composition_active")) for r in rows if r.get("policy") == "ASFT"),
        "required_component_coverage_seeds": {exp: experiment_metrics[exp]["source_skill_coverage_seeds"] for exp in comp_exps},
        "status": "unavailable_missing_component_skills" if all(experiment_metrics[e]["source_skill_coverage_seeds"] == 0 for e in comp_exps)
                  else "unavailable_no_composition_application" if not any(bool(r.get("composition_active")) for r in rows if r.get("policy") == "ASFT")
                  else "evaluated",
    }
    # Ablation effects are pooled by independent seed; A4 is not testable without component skills.
    ablations = {}
    for ablation in ("A1_NO_INVARIANTS", "A2_NO_SCT", "A3_NO_PERSISTENCE", "A4_NO_COMPOSITION"):
        relevant = comp_exps if ablation == "A4_NO_COMPOSITION" else CORE
        by_seed = []
        for seed in SEEDS:
            deltas = []
            for exp in relevant:
                vals = per_seed_effect(metrics, exp, "ASFT", ablation)
                if len(vals) == len(SEEDS): deltas.append(vals[seed - SEEDS[0]])
            if deltas: by_seed.append(mean(deltas))
        ablations[ablation] = criterion(by_seed)
        if ablation == "A4_NO_COMPOSITION" and composition["status"] != "evaluated":
            ablations[ablation]["status"] = "unavailable_missing_component_skills"

    taxonomy_map = {"near": CORE[:3], "moderate": CORE[3:6], "compositional": CORE[6:9], "structural": CORE[9:11]}
    taxonomy = {}
    for label, exps in taxonomy_map.items():
        per_seed = []
        for seed in SEEDS:
            vals = [metrics[(seed, exp, "ASFT")]["TS"]["mean"] for exp in exps]
            per_seed.append(mean(vals))
        stat = criterion(per_seed)
        missing = [e for e in exps if experiment_metrics[e]["source_skill_coverage_seeds"] == 0]
        taxonomy[label] = {**stat, "missing_source_cells": missing,
            "coverage_qualified_status": "unavailable" if missing else stat["status"]}

    # Negative-transfer checks use saved task rows; no metrics are recomputed from synthetic tasks.
    safe_all = [r for r in rows if r.get("policy") == "SAFE_RETRIEVAL_GUARD"]
    safe = [r for r in safe_all if r.get("status") == "evaluated"]
    forced = [r for r in rows if r.get("policy") in {"EXP15_FORCED_REFLECTION", "EXP16_RANDOM_FORCED", "EXP17_WRONG_COMPOSITION"}
              and str(r.get("status", "")).startswith("forced_")]
    safe_rate = mean([float(bool(r.get("rejected"))) for r in safe]) if safe else None
    forced_ntr = mean([float(not bool(r.get("correct_after"))) for r in forced]) if forced else None
    forced_harm = mean([float(float(r["P_after"]) < float(r["P_before"])) for r in forced]) if forced else None
    negative_status = "unavailable" if not safe or not forced else ("passed" if safe_rate == 1 and (forced_ntr or 0)+(forced_harm or 0)>0 else "failed")
    cgr_seed_means = {}
    c_score_means = {}
    for run in runs:
        cgr_values = [float(x["CGR"]) for x in run["growth"] if x.get("CGR") is not None]
        c_values = [float(x["C_t"]) for x in run["growth"] if x.get("C_t") is not None]
        if cgr_values: cgr_seed_means[int(run["run_seed"])] = mean(cgr_values)
        if c_values: c_score_means[int(run["run_seed"])] = mean(c_values)
    cgr_growth = summarize(list(cgr_seed_means.values()), seed=13205)
    cgr_growth["available_seeds"] = len(cgr_seed_means)
    cgr_growth["missing_seeds"] = len(SEEDS) - len(cgr_seed_means)
    cgr_growth["trend"] = "positive" if cgr_growth["mean"] is not None and cgr_growth["mean"] > 0 else (
        "negative" if cgr_growth["mean"] is not None and cgr_growth["mean"] < 0 else "zero_or_unavailable")
    c_score = summarize(list(c_score_means.values()), seed=13206)
    c_score["available_seeds"] = len(c_score_means)
    correlations = frozen_aggregate["correlations"]
    association = {k: ("unavailable" if correlations[k]["r"] is None else ("passed" if correlations[k]["r"] > 0 else "failed"))
                   for k in ("IS_vs_TS", "SU_vs_TS", "TS_vs_CGR")}
    all_baselines = "passed" if all(v["status"] == "passed" for v in pooled_baselines.values()) else (
        "failed" if any(v["status"] == "failed" for v in pooled_baselines.values()) else "unavailable")
    criteria = {
        "note": "Corrected post-hoc aggregation of saved frozen-run task rows; no tasks, seeds, or outcomes rerun or altered.",
        "frozen_source_config_protocol_sha256": manifest["root_sha256"],
        "overall_criteria_status": {
            "positive_transfer_across_all_requested_cells": "failed" if any(x["status"] == "failed" for x in experiment_metrics.values()) else ("unavailable" if any("unavailable" in x["status"] for x in experiment_metrics.values()) else "passed"), 
            "positive_cost_reduction_success_gated": criterion([mean([metrics[(seed,e,"ASFT")]["success_gated_fractional_RCR"] for e in CORE]) for seed in SEEDS])["status"],
            "skill_reuse_observed": "passed" if any(metrics[(seed,e,"ASFT")]["reuse_count"] > 0 for seed in SEEDS for e in CORE) else "failed",
            "outperform_all_mandatory_baselines": all_baselines,
            "full_composition_and_structural_transfer": composition["status"],
            "ablation_degradation": "failed" if any(v["status"] == "failed" for v in ablations.values()) else ("unavailable" if any("unavailable" in v["status"] for v in ablations.values()) else "passed"),
            "negative_transfer_detection": negative_status,
            "IS_and_SU_association_with_TS": "failed" if any(association[k] == "failed" for k in ("IS_vs_TS","SU_vs_TS")) else ("unavailable" if any(association[k] == "unavailable" for k in ("IS_vs_TS","SU_vs_TS")) else "passed"),
            "TS_CGR_association": association["TS_vs_CGR"],
        },
        "ASFT_minus_each_mandatory_baseline_pooled": pooled_baselines,
        "pairwise_baseline_effects_by_experiment": per_exp_baselines,
        "experiment_source_coverage_and_TS": experiment_metrics,
        "taxonomy_pooled_TS_and_coverage": taxonomy,
        "composition_diagnostics": composition,
        "ablation_diagnostics": ablations,
        "negative_transfer": {"safe_evaluable_n": len(safe), "safe_missing_n": len(safe_all)-len(safe),
            "safe_rejection_rate": safe_rate, "forced_evaluable_n": len(forced),
            "forced_accuracy_NTR": forced_ntr, "forced_harm_rate": forced_harm, "status": negative_status},
        "capability_growth_descriptive": {"mean_C_t_by_seed": c_score, "mean_CGR_by_seed": cgr_growth},
        "correlations": correlations,
        "association_status": association,
    }
    (HERE / "posthoc_corrected_criteria.json").write_text(json.dumps(criteria, indent=2, sort_keys=True, allow_nan=False) + "\n")
    with (HERE / "posthoc_experiment_coverage.csv").open("w", newline="") as f:
        w=csv.DictWriter(f, fieldnames=list(coverage_rows[0])); w.writeheader(); w.writerows(coverage_rows)
    with (HERE / "posthoc_pairwise_baselines.csv").open("w", newline="") as f:
        fields=["experiment_id","contrast","mean_TS_difference","sd","ci95_low","ci95_high","n_seeds"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(pairwise_rows)
    lines=["# Phase 13D post-hoc reporting correction", "",
        "This analysis reads the saved `task_level.jsonl` and per-seed checkpoint records only. It does not regenerate tasks, rerun a solver, change the frozen protocol, or alter any outcome.",
        "", "## Why this addendum exists", "",
        "The frozen report aggregator stored policy-versus-B1 contrasts but its criterion dashboard looked up ASFT-versus-B2/B3/B4 and ASFT-versus-best-single under keys it had not created. Those comparisons appeared as `n=0`/unavailable. In addition, the frozen dashboard treated partial transfer on complex programs as evidence of composition without checking source-component coverage or actual composition activation. The raw task and seed records are intact; this addendum recomputes pairwise statistics and reports coverage explicitly.",
        "", "## Corrected decision status", "", "```json", json.dumps(criteria["overall_criteria_status"],indent=2,sort_keys=True), "```", "",
        "## Main interpretation", "",
        "- The training pipeline produced only reflection and rotation skills in all ten seeds. No counting or grouping source skill was born; EXP-TR-03, EXP-TR-06, and all composition/structural cells therefore lack the preregistered required source skills.",
        "- The full composition/structural arm had zero composition candidates and zero active composition applications. Positive TS on EXP-TR-07–11 is partial multi-skill/individual-operation reuse with missing operations solved by the reference fallback, not evidence that a composed skill transferred.",
        "- A4 (no composition) matches ASFT on the EXP-TR-07–11 TS outcomes; no incremental composition effect was observed. The composition endpoint remains unavailable because all required component-skill coverage was absent.",
        "- ASFT-versus-B1/B2/B3/B4 direct paired results are in `posthoc_corrected_criteria.json` and `posthoc_pairwise_baselines.csv`. The compression proxy is still not DreamCoder.",
        f"- Capability-growth summary: mean per-seed CGR {cgr_growth['mean']:.6f} across {cgr_growth['available_seeds']} evaluable seeds (trend: {cgr_growth['trend']}); the positive TS↔CGR correlation is associational and does not imply positive net growth.",
        "- Original `criteria.json`, `aggregate_metrics.json`, and frozen code remain untouched for audit. This addendum is the corrected comparison view; the hash manifest still identifies the frozen run source.",
        "", "Reanalysis code: `posthoc_reanalysis.py`; this file is not part of the preregistered runtime hash set. No new seed was opened."]
    (HERE / "posthoc_analysis.md").write_text("\n".join(lines)+"\n")
    print(criteria["overall_criteria_status"])
    print('coverage table:', HERE / 'posthoc_experiment_coverage.csv')
    print('corrected criteria:', HERE / 'posthoc_corrected_criteria.json')

if __name__ == "__main__":
    main()
