"""Confirmatory stage aggregation, result serialization, and text/CSV reports."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from evaluation.stats import summarize_metrics
from .common import MC_SENSITIVITY, OUT_DIR, _config_digest, load_config
from .confirmation_seed import run_confirmation_seed
from .statistics import _bootstrap_mean_ci, _correlation_report


def run_confirmation(*, write: bool = True) -> dict[str, Any]:
    """Run only confirmation seeds after a saved calibration freeze exists."""
    config_data = load_config()
    if not OUT_DIR.exists() or not (OUT_DIR / "calibration_frozen.json").exists():
        raise FileNotFoundError("Run Phase 13C calibration before confirmation")
    frozen = json.loads((OUT_DIR / "calibration_frozen.json").read_text(encoding="utf-8"))
    if frozen.get("config_sha256") != _config_digest(config_data):
        raise ValueError("frozen calibration/config hash mismatch")
    seeds = list(config_data["seeds"]["confirmation"])
    if len(seeds) != 10 or set(seeds) & set(frozen["calibration_seeds"]):
        raise ValueError("invalid Phase 13C confirmation seed split")
    raw = [run_confirmation_seed(seed, frozen) for seed in seeds]
    candidate_rows = [
        {"seed": record["seed"], **candidate}
        for record in raw
        for candidate in record["candidates"]
    ]
    arm_names = ("SCT", "NEVER_CREATE", "ALWAYS_CREATE", "RANDOM_CREATE", "MEMORY_ONLY")
    arm_by_seed = {
        arm: [float(record["arm_mean_net_values"][arm]) for record in raw]
        for arm in arm_names
    }
    arm_stats = summarize_metrics(arm_by_seed)
    contrast_names = ("NEVER_CREATE", "ALWAYS_CREATE", "RANDOM_CREATE", "MEMORY_ONLY")
    contrast_by_seed = {
        control: [float(record["paired_contrasts"][f"SCT_minus_{control}"]) for record in raw]
        for control in contrast_names
    }
    contrast_stats = summarize_metrics(contrast_by_seed)
    arm_bootstrap_ci = {
        arm: list(_bootstrap_mean_ci(values, seed=14000 + i))
        for i, (arm, values) in enumerate(arm_by_seed.items())
    }
    contrast_bootstrap_ci = {
        control: list(_bootstrap_mean_ci(values, seed=15000 + i))
        for i, (control, values) in enumerate(contrast_by_seed.items())
    }
    mc_sensitivity_stats = {
        f"MC={mc:.2f}": summarize_metrics({
            arm: [float(record["arm_mean_net_values_by_mc"][arm][f"{mc:.2f}"]) for record in raw]
            for arm in arm_names
        })
        for mc in MC_SENSITIVITY
    }
    threshold_names = sorted({name for record in raw for name in record["threshold_sensitivity"]})
    threshold_sensitivity_stats = summarize_metrics({
        name: [float(record["threshold_sensitivity"].get(name, 0.0)) for record in raw]
        for name in threshold_names
    })
    threshold_sensitivity_bootstrap_ci = {
        name: list(_bootstrap_mean_ci(values, seed=16000 + i))
        for i, (name, values) in enumerate({
            name: [float(record["threshold_sensitivity"].get(name, 0.0)) for record in raw]
            for name in threshold_names
        }.items())
    }
    lifecycle_ablation_stats = summarize_metrics({
        name: [float(record["lifecycle_ablation"][field]) for record in raw]
        for name, field in (
            ("lifecycle_enabled", "lifecycle_enabled_mean_net_value"),
            ("lifecycle_disabled", "lifecycle_disabled_mean_net_value"),
            ("enabled_minus_disabled", "paired_difference_enabled_minus_disabled"),
        )
    })
    lifecycle_ablation_bootstrap_ci = {
        name: list(_bootstrap_mean_ci(
            [float(record["lifecycle_ablation"][field]) for record in raw],
            seed=17000 + i,
        ))
        for i, (name, field) in enumerate((
            ("lifecycle_enabled", "lifecycle_enabled_mean_net_value"),
            ("lifecycle_disabled", "lifecycle_disabled_mean_net_value"),
            ("enabled_minus_disabled", "paired_difference_enabled_minus_disabled"),
        ))
    }
    correlations = _correlation_report(candidate_rows, seeds)
    strict_success = all(
        contrast_bootstrap_ci[control][0] > 0.0 for control in contrast_names
    )
    result = {
        "experiment_id": "PHASE-13C-SCT-V1",
        "claim": "SCT",
        "dataset_version": "synthetic-sct-v1",
        "seeds": seeds,
        "calibration_seeds": frozen["calibration_seeds"],
        "configuration": config_data,
        "calibration_frozen": {k: v for k, v in frozen.items() if k not in {"calibration_results", "calibration_candidate_scv10_values"}},
        "primary_outcome": {
            "arm_statistics": arm_stats,
            "arm_seed_cluster_bootstrap_ci95": arm_bootstrap_ci,
            "paired_contrast_statistics": contrast_stats,
            "paired_contrast_seed_cluster_bootstrap_ci95": contrast_bootstrap_ci,
            "strict_superiority_success": strict_success,
            "rule": "paired seed-resampled 95% CI lower bound > 0 vs each of never, always, random, and memory-only",
        },
        "scv10_statistics": summarize_metrics({
            "SCV10": [float(row["SCV10"]) for row in candidate_rows]
        }),
        "mc_sensitivity": mc_sensitivity_stats,
        "threshold_sensitivity": {
            "statistics": threshold_sensitivity_stats,
            "seed_cluster_bootstrap_ci95": threshold_sensitivity_bootstrap_ci,
        },
        "lifecycle_ablation": {
            "statistics": lifecycle_ablation_stats,
            "seed_cluster_bootstrap_ci95": lifecycle_ablation_bootstrap_ci,
        },
        "composition_ablation": "composition benefit and held-out reuse are compared against paired best-single results in composition.csv",
        "no_scv_ablation": "ALWAYS_CREATE matched arm; it bypasses only SCV selection after common non-SCV eligibility",
        "scv_predictiveness": correlations,
        "raw_results": raw,
        "candidate_level_results": candidate_rows,
        "failure_cases": [case for record in raw for case in record["failure_cases"]],
        "interpretation": (
            "Controlled synthetic SCT evidence only. Legacy EXP-02 is preliminary; "
            "Phase 13B remains failed and is not changed by this result."
        ),
    }
    if write:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        (OUT_DIR / "record.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        (OUT_DIR / "skill_births.json").write_text(
            json.dumps(
                [
                    {"seed": record["seed"], "candidate": candidate["invariant_id"],
                     "signature": candidate["signature"], "category": candidate["category"],
                     "SCV10": candidate["SCV10"], "arms": {
                         arm: {"selected": candidate["arms"][arm].get("selected"),
                               "created": candidate["arms"][arm].get("created"),
                               "state_at_end": candidate["arms"][arm].get("state_at_end")}
                         for arm in arm_names
                     }}
                    for record in raw for candidate in record["candidates"]
                ],
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        (OUT_DIR / "correlations.json").write_text(json.dumps(correlations, indent=2, sort_keys=True), encoding="utf-8")
        summary = _render_summary(result)
        (OUT_DIR / "summary.md").write_text(summary, encoding="utf-8")
        _write_csvs(raw, candidate_rows, OUT_DIR)
        # Schema label specific to this experiment; don't use Phase 13A's generic label.
        record_path = OUT_DIR / "record.json"
        result["record_schema"] = "phase-13c-sct-v1"
        record_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


def _render_summary(result: dict[str, Any]) -> str:
    primary = result["primary_outcome"]
    lines = [
        "# Phase 13C — SCT Validation (synthetic-sct-v1)",
        "",
        "Confirmatory block: seeds 20–29. Calibration block: seeds 15–19.",
        "Results are conditional on the current synthetic invariant/task generator; they do not validate ARC or repair Phase 13B.",
        "",
        f"- Strict SCT superiority gate: **{primary['strict_superiority_success']}**",
        f"- Unique eligible candidate rows: {len(result['candidate_level_results'])}",
        "",
        "## Primary net value by creation policy",
        "",
        "| Policy | Mean | SD | Normal 95% CI | Seed-bootstrap 95% CI |",
        "|---|---:|---:|---:|---:|",
    ]
    for arm, stats in primary["arm_statistics"].items():
        ci = primary["arm_seed_cluster_bootstrap_ci95"][arm]
        lines.append(f"| {arm} | {stats['mean']:.6f} | {stats['std']:.6f} | {stats['ci_low']:.6f}–{stats['ci_high']:.6f} | {ci[0]:.6f}–{ci[1]:.6f} |")
    lines += ["", "## Paired SCT-minus-control contrasts", "", "| Control | Mean | SD | Normal 95% CI | Seed-bootstrap 95% CI |", "|---|---:|---:|---:|---:|"]
    for control, stats in primary["paired_contrast_statistics"].items():
        ci = primary["paired_contrast_seed_cluster_bootstrap_ci95"][control]
        lines.append(f"| {control} | {stats['mean']:.6f} | {stats['std']:.6f} | {stats['ci_low']:.6f}–{stats['ci_high']:.6f} | {ci[0]:.6f}–{ci[1]:.6f} |")
    lines += ["", "## SCV10 predictiveness (seed-cluster bootstrap)", "", "| Predictor | Spearman ρ | 95% cluster-bootstrap CI | n candidates |", "|---|---:|---:|---:|"]
    for key, item in result["scv_predictiveness"]["scv_predictors_of_future_net_value"].items():
        ci = item["seed_cluster_bootstrap_ci95"]
        lines.append(f"| {key} | {item['spearman']:.6f} | {ci[0]:.6f}–{ci[1]:.6f} | {item['candidate_n']} |")
    lines += ["", "## Skill utility associations (descriptive, seed-cluster bootstrap)", "", "| Association | Spearman ρ | 95% cluster-bootstrap CI |", "|---|---:|---:|"]
    for key, item in result["scv_predictiveness"]["utility_associations"].items():
        ci = item["seed_cluster_bootstrap_ci95"]
        lines.append(f"| {key} | {item['spearman']:.6f} | {ci[0]:.6f}–{ci[1]:.6f} |")
    lines += ["", "## Sensitivity and ablations", ""]
    lines.append("Primary MC is a modeled normalized maintenance cost, not empirical compute cost.")
    lines.append("")
    lines.append("| MC per eligible opportunity | SCT mean net value |")
    lines.append("|---:|---:|")
    for label, by_arm in result["mc_sensitivity"].items():
        mc_value = label.split("=", 1)[1]
        lines.append(f"| {mc_value} | {by_arm['SCT']['mean']:.6f} |")
    lines += ["", "| Threshold | Mean net value |", "|---|---:|"]
    for name, stats in result["threshold_sensitivity"]["statistics"].items():
        lines.append(f"| {name} | {stats['mean']:.6f} |")
    lines += ["", "| Lifecycle mode | Mean net value |", "|---|---:|"]
    for name, stats in result["lifecycle_ablation"]["statistics"].items():
        lines.append(f"| {name} | {stats['mean']:.6f} |")
    lines += ["", "No-SCV ablation is the matched ALWAYS_CREATE arm. Composition is tested against paired best-single results and on a separate task stream.", ""]
    family_counts: dict[str, int] = {}
    for row in result["candidate_level_results"]:
        family_counts[row["category"]] = family_counts.get(row["category"], 0) + 1
    lines += ["", "## Candidate birth categories", "", "| Category | Candidate rows |", "|---|---:|"]
    for category, count in sorted(family_counts.items()):
        lines.append(f"| {category} | {count} |")
    lines += [
        "",
        "Detailed evidence: `skill_births.json`, `candidate_level.csv`, `matched_controls.csv`, `mc_sensitivity.csv`, `threshold_sensitivity.csv`, `reuse_statistics.csv`, `utility_trajectories.csv`, `lifecycle.csv`, `lifecycle_ablation.csv`, and `composition.csv`.",
        "",
        "Nulls, rejected candidates, failed applications, no-match opportunities, and missing-family compositions are retained in the full record.",
        "",
    ]
    return "\n".join(lines)


def _write_csvs(raw: list[dict[str, Any]], candidates: list[dict[str, Any]], directory: Path) -> None:
    import csv
    with (directory / "candidate_level.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "seed", "invariant_id", "signature", "category", "frequency",
            "task_families", "SCV10", "p_reuse", "AG", "TS", "CC", "MC",
            "shadow_realized_net_value", "shadow_mean_SU_at_end",
            "shadow_reuse_count", "shadow_TS_cross_family",
            "no_lifecycle_realized_net_value",
        ])
        writer.writeheader()
        for row in candidates:
            writer.writerow({key: json.dumps(row.get(key)) if isinstance(row.get(key), (list, dict)) else row.get(key) for key in writer.fieldnames})
    reuse_rows = []
    utility_rows = []
    lifecycle_rows = []
    composition_rows = []
    for record in raw:
        for candidate in record["candidates"]:
            for arm, result in candidate["arms"].items():
                reuse_rows.append({"seed": record["seed"], "invariant_id": candidate["invariant_id"], "arm": arm, **result.get("reuse_statistics", {})})
                for point in result.get("utility_timeline", []):
                    utility_rows.append({"seed": record["seed"], "invariant_id": candidate["invariant_id"], "arm": arm, **point})
        lifecycle_rows.extend({"seed": record["seed"], **row} for row in record["lifecycle"])
        composition_rows.extend({"seed": record["seed"], **row} for row in record["composition"])
    policy_rows = []
    mc_rows = []
    threshold_rows = []
    lifecycle_ablation_rows = []
    for record in raw:
        for arm, value in record["arm_mean_net_values"].items():
            policy_rows.append({"seed": record["seed"], "policy": arm, "mean_net_value": value})
        for arm, mc_values in record["arm_mean_net_values_by_mc"].items():
            for mc, value in mc_values.items():
                mc_rows.append({"seed": record["seed"], "policy": arm, "MC_per_opportunity": mc, "mean_net_value": value})
        for threshold, value in record["threshold_sensitivity"].items():
            threshold_rows.append({"seed": record["seed"], "threshold": threshold, "mean_net_value": value})
        lifecycle_ablation_rows.append({"seed": record["seed"], **record["lifecycle_ablation"]})

    all_rows = (
        ("reuse_statistics.csv", reuse_rows),
        ("utility_trajectories.csv", utility_rows),
        ("lifecycle.csv", lifecycle_rows),
        ("composition.csv", composition_rows),
        ("matched_controls.csv", policy_rows),
        ("mc_sensitivity.csv", mc_rows),
        ("threshold_sensitivity.csv", threshold_rows),
        ("lifecycle_ablation.csv", lifecycle_ablation_rows),
    )
    for filename, rows in all_rows:
        if not rows:
            (directory / filename).write_text("\n", encoding="utf-8")
            continue
        fields = sorted({key for row in rows for key in row})
        with (directory / filename).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            for row in rows:
                writer.writerow({key: json.dumps(value) if isinstance(value, (list, dict)) else value for key, value in row.items()})
