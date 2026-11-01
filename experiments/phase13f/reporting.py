"""Write Phase 13F tables, figures, raw records, and publication summary."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .common import OUT
from .figures import create_figures
from .statistics import ABLATIONS, BASELINES, build_analysis


def _json(value: Any) -> Any:
    return json.dumps(value, sort_keys=True, ensure_ascii=False) if isinstance(value, (dict, list, tuple)) else value


def _csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("status\nno_rows\n", encoding="utf-8")
        return
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: _json(v) for k, v in row.items()})


def _fmt(x: Any) -> str:
    return "NA" if x is None else (f"{x:.4f}" if isinstance(x, (int, float)) else str(x))


def _table(rows: list[dict[str, Any]], fields: list[tuple[str, str]]) -> str:
    if not rows:
        return "_No applicable outcomes._"
    header = "| " + " | ".join(label for _, label in fields) + " |"
    rule = "|" + "|".join("---" for _ in fields) + "|"
    body = ["| " + " | ".join(_fmt(r.get(key)) for key, _ in fields) + " |" for r in rows]
    return "\n".join([header, rule, *body])


def _stat(analysis: dict[str, Any], arm: str, metric: str) -> dict[str, Any] | None:
    return next((r for r in analysis["arm_metrics"] if r["arm"] == arm and r["metric"] == metric), None)


def _contrast(analysis: dict[str, Any], arm: str, metric: str) -> dict[str, Any] | None:
    return next((r for r in analysis["paired_contrasts"] if r["contrast"] == f"ASFT - {arm}" and r["metric"] == metric), None)


def _metrics(analysis: dict[str, Any], arms: list[str]) -> list[dict[str, Any]]:
    return [r for r in analysis["arm_metrics"] if r["arm"] in arms and r["metric"] in {"IS", "SU", "TS", "cgr", "ig", "mean_task_utility_all_tasks", "mean_compose_task_utility", "mean_heldout_composition_incremental_gain", "mean_skill_count_persistent", "mean_skill_count_created"}]


def write_package(run: dict[str, Any], manifest: dict[str, Any]) -> Path:
    analysis = build_analysis(run)
    flat = analysis["flattened"]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "tables").mkdir(exist_ok=True)
    (OUT / "figures").mkdir(exist_ok=True)
    (OUT / "run_records.json").write_text(json.dumps(run, indent=2, sort_keys=True), encoding="utf-8")
    (OUT / "run_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    (OUT / "analysis.json").write_text(json.dumps({k: v for k, v in analysis.items() if k != "flattened"}, indent=2, sort_keys=True), encoding="utf-8")
    _csv(OUT / "seed_round_arm.csv", flat["rounds"])
    _csv(OUT / "task_level.csv", flat["tasks"])
    _csv(OUT / "composition_task_level.csv", flat["composition"])
    _csv(OUT / "capability_formation.csv", flat["formation"])
    _csv(OUT / "skill_lifecycle.csv", flat["lifecycle"])
    _csv(OUT / "seed_summary.csv", analysis["seed_summaries"])
    candidate_rows = []
    for seed_record in run["seeds"]:
        first_rows = {r["arm"]: r for r in seed_record["round_rows"] if int(r["round"]) == 1}
        for arm, row in first_rows.items():
            candidate_rows.append({"seed": seed_record["seed"], "arm": arm,
                "qualified_candidate_count": seed_record.get("qualified_candidate_count"),
                "constructed_skill_count": row.get("skill_count_created"),
                "persistent_skill_count_round1": row.get("skill_count_persistent")})
    _csv(OUT / "candidate_selection.csv", candidate_rows)
    base_table = _metrics(analysis, ["ASFT", *BASELINES])
    abl_table = _metrics(analysis, ["ASFT", *ABLATIONS])
    _csv(OUT / "tables/table_1_baselines.csv", base_table)
    _csv(OUT / "tables/table_2_ablations.csv", abl_table)
    _csv(OUT / "tables/table_3_effect_sizes.csv", analysis["paired_contrasts"])
    _csv(OUT / "tables/table_4_sensitivity.csv", [r for r in analysis["arm_metrics"] if r["arm"] == "ASFT" or r["arm"].startswith("SENS_")])
    matrix = []
    for arm in analysis["arms"]:
        row: dict[str, Any] = {"arm": arm}
        for metric, label in (("IS", "IS"), ("SU", "SU"), ("TS", "TS"), ("cgr", "CGR"), ("ig", "IG"), ("mean_task_utility_all_tasks", "task_utility")):
            result = next((x for x in analysis["arm_metrics"] if x["arm"] == arm and x["metric"] == metric), None)
            row[label] = result.get("mean") if result else None
        matrix.append(row)
    _csv(OUT / "master_result_matrix.csv", matrix)
    figures = create_figures(analysis, OUT / "figures")
    baseline_decisions = [r for r in analysis["decisions"] if r["criterion"].startswith("ASFT_beats_")]
    abl_decisions = [r for r in analysis["decisions"] if r["criterion"].startswith("component_effect_")]
    baseline_effects = []
    for arm in BASELINES:
        utility = _contrast(analysis, arm, "mean_task_utility_all_tasks")
        cgr = _contrast(analysis, arm, "mean_cgr")
        baseline_effects.append(f"- **{arm}:** task utility Δ={_fmt(utility.get('mean') if utility else None)} (95% CI {_fmt(utility.get('ci95_low') if utility else None)} to {_fmt(utility.get('ci95_high') if utility else None)}); CGR Δ={_fmt(cgr.get('mean') if cgr else None)} (95% CI {_fmt(cgr.get('ci95_low') if cgr else None)} to {_fmt(cgr.get('ci95_high') if cgr else None)}).")
    key_effects = []
    for arm in ("A1_NO_IDT", "A2_NO_SCV", "A2_1_RANDOM_SCV", "A2_2_NO_LIFECYCLE", "A2_3_NO_COMPOSITION", "A3_NO_CAPABILITY_LAYER", "X1_NO_TRANSFER", "X4_NO_CAPABILITY_FORMATION"):
        pieces = []
        for metric, label in (("mean_task_utility_all_tasks", "utility"), ("mean_compose_task_utility", "composed-task utility"), ("mean_cgr", "CGR")):
            r = _contrast(analysis, arm, metric)
            if r and r.get("n", 0):
                pieces.append(f"Δ {label}={_fmt(r.get('mean'))} [CI {_fmt(r.get('ci95_low'))}, {_fmt(r.get('ci95_high'))}]")
        key_effects.append(f"- **{arm}:** " + "; ".join(pieces) + ".")
    candidate_lines = []
    for arm in ("ASFT", "A1_1_FREQUENCY_ONLY", "A2_NO_SCV", "A2_1_RANDOM_SCV", "B3_RANDOM_SKILL_CREATION", "SENS_SCV_Q25", "SENS_SCV_Q75"):
        rows = [r for r in candidate_rows if r["arm"] == arm]
        created = [float(r["constructed_skill_count"]) for r in rows if r.get("constructed_skill_count") is not None]
        eligible = [float(r["qualified_candidate_count"]) for r in rows if r.get("qualified_candidate_count") is not None]
        if rows:
            candidate_lines.append(f"- {arm}: mean constructed skills {_fmt(sum(created)/len(created) if created else None)}; mean common eligible pool {_fmt(sum(eligible)/len(eligible) if eligible else None)}.")
    sensitivity_lines = []
    for arm in ("SENS_SCV_Q25", "ASFT", "SENS_SCV_Q75", "SENS_IS_7_5", "SENS_IS_10", "SENS_COMP_LOOSE", "SENS_COMP_STRICT"):
        row = _stat(analysis, arm, "mean_task_utility_all_tasks")
        if row:
            sensitivity_lines.append(f"- {arm}: task utility {_fmt(row.get('mean'))} (95% CI {_fmt(row.get('ci95_low'))} to {_fmt(row.get('ci95_high'))}).")
    report = [
        "# Phase 13F — Baseline & Ablation Evidence",
        "",
        f"**Experiment:** `{run['experiment_id']}`  ",
        f"**Status:** {manifest.get('status', 'complete')}  ",
        f"**Seeds:** {', '.join(str(s) for s in analysis['seeds'])} (independent units, n=10)  ",
        "**Scope:** synthetic ReasonFlux grid tasks; no ARC/external validation.  ",
        f"**Frozen config SHA-256:** `{manifest.get('config_sha256')}`  ",
        f"**Frozen source-tree SHA-256:** `{manifest.get('source_tree_sha256')}`",
        "",
        "## Outcome summary",
        "",
        "The complete criterion table follows. For quick interpretation, the paired baseline differences (ASFT minus comparator) are:",
        *baseline_effects,
        "",
        "Key component contrasts (positive Δ favors ASFT; metrics are not interchangeable):",
        *key_effects,
        "",
        "Candidate selection / budget evidence (key for interpreting no-SCV and randomized controls):",
        *candidate_lines,
        "",
        "Fixed sensitivity-point task-utility estimates:",
        *sensitivity_lines,
        "",
        "## Primary comparisons",
        "",
        "Paired 95% t intervals use seed-level differences. ASFT beats a baseline only when both the task-utility and CGR paired lower bounds are positive, as preregistered. These are decisions, not narrative overrides.",
        "",
        _table(baseline_decisions, [("criterion", "Comparison"), ("status", "Decision")]),
        "",
        "## Component ablations",
        "",
        _table(abl_decisions, [("criterion", "Intervention"), ("status", "Outcome")]),
        "",
        "## Required evidence tables",
        "",
        "- `tables/table_1_baselines.csv`: B1–B4 vs ASFT, means, SDs, CIs by metric.",
        "- `tables/table_2_ablations.csv`: contribution and cross-component ablations.",
        "- `tables/table_3_effect_sizes.csv`: paired differences, 95% CIs, Cohen dz, and Hedges g.",
        "- `tables/table_4_sensitivity.csv`: fixed SCV, invariant-strength, and composition requirements.",
        "- `master_result_matrix.csv`: IS, SU, TS, CGR, IG, and task utility across every arm.",
        "- `candidate_selection.csv`: common eligible pool versus constructed/persistent skill counts by seed and arm.",
        "",
        "## Figures",
        "",
    ]
    report.extend(f"- [{p.stem}]({p.relative_to(OUT).as_posix()})" for p in figures)
    report += ["", "## Interpretation limits", "",
        "IS is invariant strength (not a global intelligence score); it is not applicable to raw episodic memory and no-learning arms. SU/TS use repository skill utility and successful observed transfer. CGR/IG use the Phase 13E-frozen pathway and weights. B4 is a compression-only proxy, not canonical DreamCoder. A3 and X4's CGR/IG changes are structural consequences of removing capability formation/measurement, not task-performance gains; A3.1/A3.2 are not performance comparators. X3 tests retention after one-shot discovery; the current runner has no online invariant-mining loop, so a null difference is not evidence that memory is universally unnecessary. Paired standardized effect sizes can be very large when seed-difference SDs are near zero; prioritize raw paired differences and CIs. CIs are per-contrast and are not multiplicity-adjusted; secondary comparisons are exploratory. Attempt 01 was interrupted and is excluded; its manifests/note are preserved in `../PHASE-13F-BASELINE-ABLATION-V1-ATTEMPT-01-INTERRUPTED/`. Previous Phase 13C/13D/13E artifacts were not edited or pooled into the seed-level estimates.",
        "", "## Raw records and audit", "",
        "`run_records.json` preserves all candidate rejections and per-seed outcomes; `seed_round_arm.csv`, `task_level.csv`, `composition_task_level.csv`, `capability_formation.csv`, and `skill_lifecycle.csv` preserve analysis units. The pre-run manifest contains frozen config, preregistration, and source hashes.",
        "", "## EXP-ABL mapping", "",
        "Q1–Q2: Table 1 and Figure 1. Q3–Q4: A2/A1 arms and Tables 2–3. Q5–Q6: X1/A2.3 and composition rows. Q7: paired effect-size table, descriptive ranking only. Q8: A3/A3.2/X4, master matrix, and growth-measurement status.",
        "", "Phase 13F results do not establish external ARC validity, and no criterion is promoted to a pass because it was expected to succeed."]
    path = OUT / "evidence_package.md"
    posthoc = manifest.get("posthoc_analysis")
    if posthoc:
        report += ["", "## Posthoc analysis audit", "", f"{posthoc.get('reason')} Saved-record SHA-256 `{posthoc.get('saved_records_sha256_before')}`; posthoc analysis source SHA-256 `{posthoc.get('posthoc_source_tree_sha256')}`. Benchmark rerun: `{posthoc.get('benchmark_rerun')}`."]
    path.write_text("\n".join(report), encoding="utf-8")
    return path
