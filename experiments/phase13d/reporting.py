"""Paper-ready Phase-13D tables, figures, and criterion status report."""
from __future__ import annotations
import csv
import json
from pathlib import Path
from statistics import mean
from typing import Any
from .statistics import summarize
from .common import OUT_DIR, canonical_json


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False, default=str) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    columns = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns or ["status"])
        writer.writeheader()
        writer.writerows(rows)


def _cell_metric(aggregate: dict[str, Any], exp: str, policy: str, metric: str) -> dict[str, Any] | None:
    item = aggregate["cells"].get(f"{exp}|{policy}")
    return item.get(metric) if item else None


def _seed_values(aggregate: dict[str, Any], exp: str, policy: str, metric: str) -> list[float]:
    item = aggregate["cells"].get(f"{exp}|{policy}")
    return list(item.get("per_seed", {}).get(metric, [])) if item else []


def _criterion(values: list[float]) -> dict[str, Any]:
    stat = summarize(values, seed=13131)
    signs = sum(x > 0 for x in values)
    return {**stat, "positive_seeds": signs,
            "stable_positive": bool(stat["mean"] is not None and stat["mean"] > 0
                                     and stat["ci95"][0] is not None and stat["ci95"][0] > 0
                                     and signs >= 8)}


def evaluate_criteria(aggregate: dict[str, Any], seed_results: list[dict[str, Any]]) -> dict[str, Any]:
    core = [f"EXP-TR-{n:02d}" for n in range(1, 12)]
    taxonomy = {f"EXP-TR-{n:02d}": "near" for n in range(1, 4)}
    taxonomy.update({f"EXP-TR-{n:02d}": "moderate" for n in range(4, 7)})
    taxonomy.update({f"EXP-TR-{n:02d}": "compositional" for n in range(7, 10)})
    taxonomy.update({"EXP-TR-10": "structural", "EXP-TR-11": "structural"})
    seeds = sorted(result["run_seed"] for result in seed_results)
    per_seed = {result["run_seed"]: result for result in seed_results}
    by_taxonomy: dict[str, list[float]] = {}
    for group in sorted(set(taxonomy.values())):
        values = []
        for seed in seeds:
            cell_values = []
            for exp in core:
                if taxonomy[exp] != group:
                    continue
                row = next((x for x in per_seed[seed]["cell_summaries"]
                            if x["experiment_id"] == exp and x["policy"] == "ASFT"), None)
                if row:
                    cell_values.append(float(row["metrics"]["TS"]["mean"]))
            if cell_values:
                values.append(mean(cell_values))
        by_taxonomy[group] = values
    positive_ts = {group: _criterion(values) for group, values in by_taxonomy.items()}
    for group, stat in positive_ts.items():
        stat["TS_approximately_zero"] = bool(stat["mean"] is not None and -0.01 <= stat["mean"] <= 0.01)
        stat["status"] = "unavailable" if stat["n"] < 10 else ("passed" if stat["stable_positive"] else "failed")

    rcr_by_seed: dict[int, list[float]] = {seed: [] for seed in seeds}
    gated_rcr_by_seed: dict[int, list[float]] = {seed: [] for seed in seeds}
    reuse_rates: list[float] = []
    for exp in core:
        vals = _seed_values(aggregate, exp, "ASFT", "RCR_normalized")
        gated_vals = _seed_values(aggregate, exp, "ASFT", "success_gated_fractional_RCR")
        for index, value in enumerate(vals):
            if index < len(seeds):
                rcr_by_seed[seeds[index]].append(float(value))
        for index, value in enumerate(gated_vals):
            if index < len(seeds):
                gated_rcr_by_seed[seeds[index]].append(float(value))
        reuse = _cell_metric(aggregate, exp, "ASFT", "reuse_rate")
        if reuse and reuse["mean"] is not None:
            reuse_rates.append(float(reuse["mean"]))
    rcr_stat = _criterion([mean(v) for v in rcr_by_seed.values() if v])
    rcr_stat["status"] = "unavailable" if rcr_stat["n"] < 10 else ("passed" if rcr_stat["stable_positive"] else "failed")
    gated_rcr_stat = _criterion([mean(v) for v in gated_rcr_by_seed.values() if v])
    gated_rcr_stat["status"] = "unavailable" if gated_rcr_stat["n"] < 10 else ("passed" if gated_rcr_stat["stable_positive"] else "failed")
    reuse_status = "unavailable" if not reuse_rates else ("passed" if any(v > 0 for v in reuse_rates) else "failed")

    comp_exps = [f"EXP-TR-{n:02d}" for n in range(7, 12)]
    comp_struct = {exp: aggregate["baseline_comparisons"].get(f"{exp}|ASFT-B1", {}) for exp in comp_exps}
    comp_seed: dict[int, list[float]] = {seed: [] for seed in seeds}
    best_single_seed: dict[int, list[float]] = {seed: [] for seed in seeds}
    comp_rcr_seed: dict[int, list[float]] = {seed: [] for seed in seeds}
    comp_accuracy_seed: dict[int, list[float]] = {seed: [] for seed in seeds}
    for exp in comp_exps:
        for index, value in enumerate(comp_struct[exp].get("per_seed", [])):
            if index < len(seeds): comp_seed[seeds[index]].append(float(value))
        effect = aggregate["baseline_comparisons"].get(f"{exp}|ASFT-BEST_SINGLE", {})
        for index, value in enumerate(effect.get("per_seed", [])):
            if index < len(seeds): best_single_seed[seeds[index]].append(float(value))
        asft_rcr = _seed_values(aggregate, exp, "ASFT", "success_gated_fractional_RCR")
        single_rcr = _seed_values(aggregate, exp, "BEST_SINGLE", "success_gated_fractional_RCR")
        asft_acc = _seed_values(aggregate, exp, "ASFT", "exact_accuracy")
        single_acc = _seed_values(aggregate, exp, "BEST_SINGLE", "exact_accuracy")
        for index in range(min(len(seeds), len(asft_rcr), len(single_rcr), len(asft_acc), len(single_acc))):
            comp_rcr_seed[seeds[index]].append(float(asft_rcr[index]) - float(single_rcr[index]))
            comp_accuracy_seed[seeds[index]].append(float(asft_acc[index]) - float(single_acc[index]))
    comp_stat = _criterion([mean(v) for v in comp_seed.values() if v])
    comp_stat["status"] = "unavailable" if comp_stat["n"] < 10 else ("passed" if comp_stat["stable_positive"] else "failed")
    comp_ts_single = _criterion([mean(v) for v in best_single_seed.values() if v])
    comp_rcr_single = _criterion([mean(v) for v in comp_rcr_seed.values() if v])
    comp_acc_values = [mean(v) for v in comp_accuracy_seed.values() if v]
    comp_acc_stat = summarize(comp_acc_values, seed=13143)
    comp_available = min(comp_ts_single["n"], comp_rcr_single["n"], comp_acc_stat["n"]) >= 10
    comp_pass = (comp_available and comp_ts_single["stable_positive"]
                 and comp_rcr_single["stable_positive"]
                 and comp_acc_stat["mean"] is not None and comp_acc_stat["mean"] >= 0)
    comp_vs_single = {"TS_difference": comp_ts_single, "RCR_difference": comp_rcr_single,
                      "exact_accuracy_difference": comp_acc_stat,
                      "status": "unavailable" if not comp_available else ("passed" if comp_pass else "failed")}

    baseline_effects = {}
    baseline_names = ("B1_NO_LEARNING", "B2_MEMORY_ONLY", "B3_RANDOM_SKILLS", "B4_COMPRESSION_PROXY")
    for baseline in baseline_names:
        pooled_by_seed: dict[int, list[float]] = {seed: [] for seed in seeds}
        for exp in core:
            effect = aggregate["baseline_comparisons"].get(f"{exp}|ASFT-{baseline}")
            if effect:
                for index, value in enumerate(effect.get("per_seed", [])):
                    if index < len(seeds): pooled_by_seed[seeds[index]].append(float(value))
        stat = _criterion([mean(values) for values in pooled_by_seed.values() if values])
        stat["status"] = "unavailable" if stat["n"] < 10 else ("passed" if stat["stable_positive"] else "failed")
        baseline_effects[baseline] = stat

    ablation_effects = {}
    for policy in ("A1_NO_INVARIANTS", "A2_NO_SCT", "A3_NO_PERSISTENCE", "A4_NO_COMPOSITION"):
        cells = [f"EXP-TR-{n:02d}" for n in range(7, 12)] if policy == "A4_NO_COMPOSITION" else core
        effects_by_seed: dict[int, list[float]] = {seed: [] for seed in seeds}
        for exp in cells:
            effect = aggregate["ablation_comparisons"].get(f"{exp}|ASFT-minus-{policy}")
            if effect:
                for index, value in enumerate(effect.get("per_seed", [])):
                    if index < len(seeds): effects_by_seed[seeds[index]].append(float(value))
        stat = _criterion([mean(values) for values in effects_by_seed.values() if values])
        stat["status"] = "unavailable" if stat["n"] < 10 else ("passed" if stat["stable_positive"] else "failed")
        ablation_effects[policy] = stat

    safe_all = [row for result in seed_results for row in result["task_rows"] if row.get("policy") == "SAFE_RETRIEVAL_GUARD"]
    safe = [row for row in safe_all if row.get("status") == "evaluated"]
    forced = [row for result in seed_results for row in result["task_rows"]
              if row.get("policy") in {"EXP15_FORCED_REFLECTION", "EXP16_RANDOM_FORCED", "EXP17_WRONG_COMPOSITION"}
              and str(row.get("status", "")).startswith("forced_")]
    rejection = sum(bool(row.get("rejected")) for row in safe) / len(safe) if safe else None
    forced_ntr = sum(not bool(row.get("correct_after")) for row in forced) / len(forced) if forced else None
    forced_harm = sum(float(row["P_after"]) < float(row["P_before"]) for row in forced) / len(forced) if forced else None
    negative_status = "unavailable" if not safe or not forced else ("passed" if rejection == 1.0 and (forced_ntr or 0) + (forced_harm or 0) > 0 else "failed")

    correlations = aggregate["correlations"]
    association_status = {}
    for name in ("IS_vs_TS", "SU_vs_TS"):
        r = correlations.get(name, {}).get("r")
        association_status[name] = "unavailable" if r is None else ("passed" if r > 0 else "failed")
    ts_cgr_r = correlations.get("TS_vs_CGR", {}).get("r")
    association_status["TS_vs_CGR"] = "unavailable" if ts_cgr_r is None else ("passed" if ts_cgr_r > 0 else "failed")
    overall = {
        "positive_transfer_across_taxonomies": "passed" if positive_ts and all(x["status"] == "passed" for x in positive_ts.values()) else ("unavailable" if not positive_ts else "failed"),
        "positive_reasoning_cost_reduction": gated_rcr_stat["status"],
        "successful_skill_reuse": reuse_status,
        "composition_and_structural_value_vs_best_single": comp_vs_single["status"],
        "composition_and_structural_transfer_vs_no_learning": comp_stat["status"],
        "outperform_all_mandatory_baselines": "passed" if all(v["status"] == "passed" for v in baseline_effects.values()) else ("failed" if any(v["status"] == "failed" for v in baseline_effects.values()) else "unavailable"),
        "ablation_degradation": "passed" if all(v["status"] == "passed" for v in ablation_effects.values()) else ("failed" if any(v["status"] == "failed" for v in ablation_effects.values()) else "unavailable"),

        "negative_transfer_detected_correctly": negative_status,
        "invariant_skill_transfer_association": "passed" if all(association_status[x] == "passed" for x in ("IS_vs_TS", "SU_vs_TS")) else ("failed" if any(association_status[x] == "failed" for x in ("IS_vs_TS", "SU_vs_TS")) else "unavailable"),
        "capability_growth_association": association_status["TS_vs_CGR"],
    }
    return {
        "overall_criteria_status": overall,
        "positive_TS_by_taxonomy": positive_ts,
        "positive_RCR_normalized_raw": rcr_stat,
        "positive_success_gated_RCR": gated_rcr_stat,
        "successful_reuse_observed": any(v > 0 for v in reuse_rates) if reuse_rates else None,
        "composition_structural_vs_B1": {"summary": comp_stat, "per_experiment": comp_struct},
        "composition_structural_vs_best_single": comp_vs_single,
        "ASFT_pooled_vs_baselines": baseline_effects,
        "ablation_degradation": ablation_effects,
        "negative_transfer": {"safe_reflection_retrieval_n": len(safe),
            "safe_reflection_retrieval_unavailable_n": len(safe_all) - len(safe),
            "safe_reflection_rejection_rate": rejection, "forced_diagnostic_n": len(forced),
            "forced_accuracy_NTR": forced_ntr, "forced_harm_rate": forced_harm,
            "status": negative_status},
        "association_status": association_status,
        "seed_count": len(seeds),
        "criteria_are_descriptive_not_guaranteed": True,
    }


def _figures(out: Path, aggregate: dict[str, Any], seed_results: list[dict[str, Any]]) -> list[str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    names = []
    fig, ax = plt.subplots(figsize=(10, 3.4))
    boxes = ["Near", "Moderate", "Compositional", "Structural"]
    for i, label in enumerate(boxes):
        x = i * 2.1
        ax.add_patch(plt.Rectangle((x, 0.62), 1.7, 0.32, facecolor="#e8eef6", edgecolor="#243b53", linewidth=1.4))
        ax.text(x + 0.85, 0.78, label, ha="center", va="center", fontsize=9)
        if i < len(boxes) - 1:
            ax.annotate("", (x + 2.05, 0.78), (x + 1.72, 0.78), arrowprops={"arrowstyle": "->", "color": "#52606d"})
    ax.text(3.2, 0.45, "Transfer distance / composition complexity increases →", ha="center", fontsize=8)
    ax.annotate("negative-transfer checks span task families", (4.0, 0.28), (4.0, 0.45), arrowprops={"arrowstyle": "->", "linestyle": "--", "color": "#b23a48"}, ha="center", fontsize=8, color="#8a1c2c")
    ax.add_patch(plt.Rectangle((2.95, 0.02), 2.1, 0.22, facecolor="#fff0f0", edgecolor="#b23a48", linewidth=1.4))
    ax.text(4.0, 0.13, "Negative transfer / guardrails", ha="center", va="center", fontsize=8, color="#8a1c2c")
    ax.set(xlim=(-0.2, 8.5), ylim=(0, 1), title="Phase 13D transfer taxonomy")
    ax.axis("off")
    path = out / "figure_01_transfer_taxonomy.svg"; fig.savefig(path, bbox_inches="tight"); plt.close(fig); names.append(path.name)

    exps = [f"EXP-TR-{n:02d}" for n in range(1, 12)]
    labels = [e.replace("EXP-TR-", "") for e in exps]
    vals = [_cell_metric(aggregate, e, "ASFT", "TS")["mean"] if _cell_metric(aggregate, e, "ASFT", "TS") else 0 for e in exps]
    lo = [_cell_metric(aggregate, e, "ASFT", "TS")["ci95"][0] if _cell_metric(aggregate, e, "ASFT", "TS") else 0 for e in exps]
    hi = [_cell_metric(aggregate, e, "ASFT", "TS")["ci95"][1] if _cell_metric(aggregate, e, "ASFT", "TS") else 0 for e in exps]
    fig, ax = plt.subplots(figsize=(10, 4)); ax.bar(labels, vals, color="#2f6690")
    ax.errorbar(range(len(vals)), vals, yerr=[[v-a for v,a in zip(vals,lo)],[b-v for v,b in zip(vals,hi)]], fmt="none", ecolor="#102a43", capsize=3)
    ax.axhline(0, color="black", linewidth=.8); ax.set(title="ASFT transfer score by experiment", ylabel="Mean TS (seed-level 95% CI)", xlabel="Experiment")
    path = out / "figure_02_TS_by_family.svg"; fig.savefig(path, bbox_inches="tight"); plt.close(fig); names.append(path.name)

    rcr = [_cell_metric(aggregate, e, "ASFT", "RCR_normalized")["mean"] if _cell_metric(aggregate, e, "ASFT", "RCR_normalized") else 0 for e in exps]
    fig, ax = plt.subplots(figsize=(10, 4)); ax.bar(labels, rcr, color="#3a7d44"); ax.axhline(0, color="black", linewidth=.8)
    ax.set(title="Matched reasoning-cost reduction", ylabel="Normalized RCR", xlabel="Experiment")
    path = out / "figure_03_reasoning_cost_reduction.svg"; fig.savefig(path, bbox_inches="tight"); plt.close(fig); names.append(path.name)

    growth_by_exp: dict[str, list[float]] = {}
    cgr_by_exp: dict[str, list[float]] = {}
    for result in seed_results:
        for row in result["growth"]:
            if row["C_t"] is not None:
                growth_by_exp.setdefault(row["experiment_id"], []).append(float(row["C_t"]))
            if row["CGR"] is not None:
                cgr_by_exp.setdefault(row["experiment_id"], []).append(float(row["CGR"]))
    glabels = sorted(growth_by_exp)
    gvals = [mean(growth_by_exp[k]) for k in glabels]
    fig, ax = plt.subplots(figsize=(10, 4)); ax.plot(range(len(gvals)), gvals, marker="o", color="#7b2cbf", label="C_t")
    ax2 = ax.twinx()
    cvals = [mean(cgr_by_exp[k]) if cgr_by_exp.get(k) else 0.0 for k in glabels]
    ax2.plot(range(len(gvals)), cvals, marker="s", linestyle="--", color="#2a9d8f", label="CGR")
    ax.set_xticks(range(len(gvals)), [x[-2:] for x in glabels]); ax.set(title="Capability portfolio and growth rate across transfer blocks", ylabel="C_t", xlabel="Experiment block")
    ax2.set_ylabel("CGR")
    handles, labels_ = ax.get_legend_handles_labels(); handles2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(handles + handles2, labels_ + labels2, loc="best")
    path = out / "figure_04_transfer_growth.svg"; fig.savefig(path, bbox_inches="tight"); plt.close(fig); names.append(path.name)

    nlabels = ["EXP15 forced reflection", "EXP16 random", "EXP17 wrong composition"]
    ns = ["EXP15_FORCED_REFLECTION", "EXP16_RANDOM_FORCED", "EXP17_WRONG_COMPOSITION"]
    ts, harm = [], []
    for policy in ns:
        vals = [r for result in seed_results for r in result["task_rows"]
                if r.get("policy") == policy and str(r.get("status", "")).startswith("forced_")]
        ts.append(mean([float(r["P_after"]) - float(r["P_before"]) for r in vals]) if vals else 0)
        harm.append(mean([float(r["P_after"]) < float(r["P_before"]) for r in vals]) if vals else 0)
    fig, ax = plt.subplots(figsize=(8, 4)); x = range(len(ns)); width = .38
    ax.bar([i-width/2 for i in x], ts, width, label="Mean TS", color="#d1495b")
    ax.bar([i+width/2 for i in x], harm, width, label="Harm rate", color="#edae49")
    ax.axhline(0, color="black", linewidth=.8); ax.set_xticks(list(x), nlabels, rotation=15, ha="right"); ax.legend()
    ax.set(title="Positive and negative transfer diagnostics", ylabel="Effect / rate")
    path = out / "figure_05_positive_negative_transfer.svg"; fig.savefig(path, bbox_inches="tight"); plt.close(fig); names.append(path.name)
    return names


def write_package(seed_results: list[dict[str, Any]], aggregate: dict[str, Any], hashes: dict[str, Any], out_dir: Path = OUT_DIR) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    all_rows = [row for result in seed_results for row in result["task_rows"]]
    with (out_dir / "task_level.jsonl").open("w", encoding="utf-8") as handle:
        for row in all_rows:
            handle.write(json.dumps(row, sort_keys=True, default=str) + "\n")
    _write_json(out_dir / "seed_metrics.json", [result["cell_summaries"] for result in seed_results])
    _write_json(out_dir / "training_pools.json", [{"run_seed": r["run_seed"], **r["training"]} for r in seed_results])
    _write_json(out_dir / "growth_timeline.json", [r["growth"] for r in seed_results])
    _write_json(out_dir / "skill_points.json", [r["skill_points"] for r in seed_results])
    _write_json(out_dir / "aggregate_metrics.json", aggregate)
    _write_json(out_dir / "hashes.json", hashes)
    criteria = evaluate_criteria(aggregate, seed_results)
    _write_json(out_dir / "criteria.json", criteria)
    tables = []
    taxonomy_map = {"near": range(1,4), "moderate": range(4,7), "compositional": range(7,10), "structural": range(10,12)}
    for title, numbers in taxonomy_map.items():
        rows = []
        for number in numbers:
            exp = f"EXP-TR-{number:02d}"
            for policy in ["ASFT", "BEST_SINGLE", "B1_NO_LEARNING", "B2_MEMORY_ONLY", "B3_RANDOM_SKILLS", "B4_COMPRESSION_PROXY"]:
                cell = aggregate["cells"].get(f"{exp}|{policy}")
                if cell:
                    rows.append({"experiment_id": exp, "policy": policy,
                                 **{m: cell[m]["mean"] for m in ("TS", "exact_accuracy", "RCR_normalized", "success_gated_fractional_RCR", "TU", "ITS", "reuse_rate", "transfer_success_rate", "NTR_accuracy", "NTR_harm", "operations_count", "retrieval_candidates_evaluated")}})
        name = f"table_{title}.csv"; _write_csv(out_dir / name, rows); tables.append(name)
    baseline_rows = [{"comparison": k, "mean_effect": v["mean"], "sd": v["sd"], "ci95_low": v["ci95"][0], "ci95_high": v["ci95"][1], "paired_cohens_dz": v["paired_cohens_dz"], "beats_baseline": v["beats_baseline"]} for k,v in aggregate["baseline_comparisons"].items()]
    ablation_rows = [{"comparison": k, "mean_effect": v["mean"], "sd": v["sd"], "ci95_low": v["ci95"][0], "ci95_high": v["ci95"][1], "paired_cohens_dz": v["paired_cohens_dz"], "degradation": v["degradation"]} for k,v in aggregate["ablation_comparisons"].items()]
    _write_csv(out_dir / "table_matched_baselines.csv", baseline_rows); tables.append("table_matched_baselines.csv")
    _write_csv(out_dir / "table_matched_ablations.csv", ablation_rows); tables.append("table_matched_ablations.csv")
    figures = _figures(out_dir, aggregate, seed_results)
    summary = {"criteria": criteria, "correlations": aggregate["correlations"], "figures": figures, "tables": tables,
               "task_level_rows": len(all_rows), "seed_count": len(seed_results)}
    _write_json(out_dir / "summary.json", summary)
    lines = ["# Phase 13D Transfer v1 — results", "", f"**Seeds:** {len(seed_results)}; **task-level rows:** {len(all_rows)}.",
             "**Dataset:** synthetic-transfer-v1. This is not ARC evidence. B4 is a compression proxy, not DreamCoder.",
             "", "## Frozen criteria", "", "```json", json.dumps(criteria, indent=2, sort_keys=True), "```", "",
             "## Correlations", "", "```json", json.dumps(aggregate["correlations"], indent=2, sort_keys=True), "```", "",
             "## Evidence package", "", "Figures: " + ", ".join(figures), "", "Tables: " + ", ".join(tables), "",
             "Search candidate evaluations remain null where the legacy solver exposes no canonical counter. All task/seed outcomes, including failures and unavailable cells, are in the JSONL and seed-level records."]
    (out_dir / "phase13d_results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary
