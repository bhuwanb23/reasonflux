"""Write raw Phase 13E records, six paper tables, figures, and report."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .figures import create_figures
from .statistics import build_analysis, summarize

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "experiments" / "PHASE-13E-CAP-GROWTH-V1"


def _jsonable(value: Any) -> Any:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, ensure_ascii=False)
    return value


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("status\nno_rows\n", encoding="utf-8")
        return
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _jsonable(value) for key, value in row.items()})


def _fmt(value: Any, digits: int = 4) -> str:
    if value is None:
        return "unavailable"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def _markdown_table(rows: list[dict[str, Any]], columns: list[tuple[str, str]]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(label for _, label in columns) + " |"
    rule = "|" + "|".join("---" for _ in columns) + "|"
    body = ["| " + " | ".join(_fmt(row.get(key)) for key, _ in columns) + " |" for row in rows]
    return "\n".join([header, rule, *body])


def _table_rows(analysis: dict[str, Any], metric_names: list[str]) -> list[dict[str, Any]]:
    source = analysis["arm_metrics"]
    return [r for r in source if r["metric"] in metric_names]


def _round_table_rows(rounds: list[dict[str, Any]], metrics: list[str]) -> list[dict[str, Any]]:
    arms = sorted({str(r["arm"]) for r in rounds})
    out: list[dict[str, Any]] = []
    for arm in arms:
        for round_no in range(1, 5):
            rows = [r for r in rounds if r["arm"] == arm and int(r["round"]) == round_no]
            for metric in metrics:
                out.append({"arm": arm, "round": round_no, "metric": metric, **summarize(r.get(metric) for r in rows)})
    return out


def write_evidence_package(run: dict[str, Any], manifest: dict[str, Any]) -> Path:
    analysis = build_analysis(run)
    flat = analysis["flattened"]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "figures").mkdir(exist_ok=True)
    (OUT / "tables").mkdir(exist_ok=True)
    (OUT / "run_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    (OUT / "run_records.json").write_text(json.dumps(run, indent=2, sort_keys=True), encoding="utf-8")
    (OUT / "analysis.json").write_text(json.dumps({k: v for k, v in analysis.items() if k != "flattened"}, indent=2, sort_keys=True), encoding="utf-8")
    _write_csv(OUT / "seed_round_arm.csv", flat["rounds"])
    _write_csv(OUT / "task_level.csv", flat["tasks"])
    _write_csv(OUT / "composition_task_level.csv", flat["composition"])
    _write_csv(OUT / "capability_formation.csv", flat["formations"])
    _write_csv(OUT / "robustness_probes.csv", flat["robustness"])
    _write_csv(OUT / "skill_lifecycle.csv", flat["skill_lifecycle"])
    _write_csv(OUT / "seed_summary.csv", analysis["seed_summaries"])
    _write_csv(OUT / "tables" / "table_1_capability_evolution.csv", _round_table_rows(flat["rounds"], ["ct", "cgr", "n_capabilities", "new_capabilities", "fragmentation_ratio", "saturation_ratio", "composition_skill_count"]))
    _write_csv(OUT / "tables" / "table_2_coverage_statistics.csv", _round_table_rows(flat["rounds"], ["portfolio_coverage", "supported_family_coverage", "ccg"]))
    utility_table = _round_table_rows(flat["rounds"], ["capu", "mean_skill_utility_su", "mean_transfer_score_ts", "ug", "ig", "igr", "ie"])
    utility_table.extend(r for r in _table_rows(analysis, ["ie_slope", "mean_composition_incremental_gain", "composition_success_rate", "mean_composition_validation_gain"]))
    _write_csv(OUT / "tables" / "table_3_utility_statistics.csv", utility_table)
    _write_csv(OUT / "tables" / "table_4_baseline_comparison.csv", [r for r in analysis["paired_contrasts"] if r["contrast"].split(" - ")[-1].startswith("B")])
    _write_csv(OUT / "tables" / "table_5_ablation_comparison.csv", [r for r in analysis["paired_contrasts"] if r["contrast"].split(" - ")[-1].startswith("A")])
    _write_csv(OUT / "tables" / "table_6_correlations.csv", analysis["correlations"] + [analysis["prediction"]])
    figures = create_figures(flat["rounds"], flat["composition"], OUT / "figures")

    asft = [r for r in analysis["arm_metrics"] if r["arm"] == "ASFT"]
    primary_metrics = ["ct", "cgr", "portfolio_coverage", "capu", "ig", "igr", "ie", "ie_slope", "task_utility"]
    summary_rows = [r for r in asft if r["metric"] in primary_metrics]
    posthoc = manifest.get("posthoc_analysis") or {}
    posthoc_note = (
        f" Posthoc audit: {posthoc.get('reason')} Saved-record SHA-256 `{posthoc.get('saved_records_sha256_before')}`; posthoc analysis source SHA-256 `{posthoc.get('posthoc_source_tree_sha256')}`. Benchmark rerun: `{posthoc.get('benchmark_rerun')}`."
        if posthoc else ""
    )
    criteria_rows = [
        {
            "criterion": row.get("criterion"),
            "status": row.get("status"),
            "observed": row.get("observed", row.get("observed_mean", row.get("observed_r", row.get("metrics", row.get("ci95_low", ""))))),
            "ci95_low": row.get("ci95_low"),
            "reason": row.get("reason", ""),
        }
        for row in analysis["decisions"]
    ]
    evidence = [
        "# Phase 13E Capability Growth Evidence Package",
        "",
        f"**Experiment:** `{run['experiment_id']}`  ",
        f"**Confirmation status:** {manifest.get('status', 'complete')}  ",
        f"**Seeds:** {', '.join(str(s['seed']) for s in run['seeds'])}  ",
        "**Benchmark scope:** synthetic ReasonFlux grid tasks only; no ARC/external validation.  ",
        f"**Frozen config SHA-256:** `{manifest.get('config_sha256', 'not recorded')}`  ",
        f"**Frozen source-tree SHA-256:** `{manifest.get('source_tree_sha256', 'not recorded')}`",
        "",
        "## Preregistered primary outcomes (ASFT)",
        "",
        _markdown_table(summary_rows, [("metric", "Metric"), ("n", "n seeds"), ("mean", "Mean"), ("sd", "SD"), ("ci95_low", "95% CI low"), ("ci95_high", "95% CI high")]),
        "",
        "## Preregistered criterion decisions",
        "",
        _markdown_table(criteria_rows, [("criterion", "Criterion"), ("status", "Decision"), ("observed", "Observed"), ("ci95_low", "95% CI low"), ("reason", "Reason")]),
        "",
        "## Correlations and prediction",
        "",
        _markdown_table(analysis["correlations"], [("correlation", "Association"), ("n", "n seeds"), ("pearson_r", "Pearson r"), ("ci95_low", "Fisher CI low"), ("ci95_high", "Fisher CI high"), ("status", "Status")]),
        "",
        f"Future prediction (C_t at round t → task utility in round t+1): **r={_fmt(analysis['prediction'].get('pearson_r'))}**, 95% cluster-bootstrap CI [{_fmt(analysis['prediction'].get('ci95_low'))}, {_fmt(analysis['prediction'].get('ci95_high'))}], status `{analysis['prediction'].get('status')}` (10 seed clusters maximum).",
        "",
        "## Figures",
        "",
    ]
    for path in figures:
        evidence.append(f"- [{path.stem}]({path.relative_to(OUT).as_posix()})")
    evidence.extend([
        "",
        "## Tables and raw evidence",
        "",
        "- `tables/table_1_capability_evolution.csv` — Table 1, capability evolution.",
        "- `tables/table_2_coverage_statistics.csv` — Table 2, coverage statistics.",
        "- `tables/table_3_utility_statistics.csv` — Table 3, capability/skill utility and intelligence metrics.",
        "- `tables/table_4_baseline_comparison.csv` — Table 4, paired mandatory baseline contrasts.",
        "- `tables/table_5_ablation_comparison.csv` — Table 5, paired ablation contrasts.",
        "- `tables/table_6_correlations.csv` — Table 6, preregistered correlations and future prediction.",
        "- `seed_round_arm.csv`, `task_level.csv`, `composition_task_level.csv`, `capability_formation.csv`, `skill_lifecycle.csv`, `robustness_probes.csv`, and `seed_summary.csv` retain seed/task/round-level data.",
        "- `run_records.json` retains candidate rejections, all seed outputs, and task-level records; `frozen_run_manifest.json` preserves hashes recorded before seed 60 and `run_manifest.json` records completion status.",
        "",
        "## Interpretation and caveats",
        "",
        f"Capability formation is counted only after the existing proposal and validity checks. Empty or unavailable portfolios are not assigned favorable synthetic values. The two IG pathways in the repository remain distinct; only `growth_metrics.compute_ig` with the preregistered GrowthConfig weights is confirmatory. Positive correlations are descriptive at n=10 and do not establish causality. A5_NO_CGM is intentionally behavior-matched and its growth metrics are masked, so it is not a performance comparator. B4_COMPRESSION_PROXY is not canonical DreamCoder. The adversarial dummy-skill test and seeded regression probe are reported separately from learned outcomes. Prior Phase 13C/13D evidence and its limitations remain unchanged.{posthoc_note}",
        "",
        "## EXP-CAP-01–22 mapping",
        "",
        "| Experiments | Evidence in this package |",
        "|---|---|",
        "| 01–02 formation and membership | `capability_formation.csv`, capability counts, states, member categories, category purity, target-family Jaccard |",
        "| 03–05 trajectory, CGR, seed stability | Figures 1–2, Table 1, seed-level CI and monotonicity |",
        "| 06–08 coverage | Figure 3, Table 2, family support and round deltas |",
        "| 09–11 utility and reuse/transfer | Figure 4, Table 3, task rows linking capability-related utility to transfer/reuse |",
        "| 12–14 composition and higher order | Figure 5, composition task data and composition lifecycle; unavailable components remain explicitly unavailable |",
        "| 15–18 IG, IGR, efficiency, prediction | Figure 6, Table 3, Table 6, `analysis.json` |",
        "| 19–22 fragmentation, saturation, regression, metric gaming | `fragmentation_ratio` and API audit in `seed_round_arm.csv`; `saturation_ratio` by round; copied-portfolio removal and 20-dummy-skill probes in `robustness_probes.csv` |",
        "",
        "## Frozen files",
        "",
        "The protocol and config were frozen before confirmation. This package does not alter Phase 13C/13D run records or historical evidence.",
    ])
    report = OUT / "evidence_package.md"
    report.write_text("\n".join(evidence), encoding="utf-8")
    return report
