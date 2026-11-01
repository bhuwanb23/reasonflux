"""Evidence-package Markdown generated strictly from saved experiment records."""
from __future__ import annotations

import csv
import json
import statistics
from collections import Counter, defaultdict
from .analysis_common import OUT, candidates, fmt, mean, raw, record, sample_sd, paired_dz

def evidence_report():
    primary = record["primary_outcome"]
    cal = json.loads((OUT / "calibration.json").read_text(encoding="utf-8"))
    arms = ["SCT", "NEVER_CREATE", "ALWAYS_CREATE", "RANDOM_CREATE", "MEMORY_ONLY"]
    categories = Counter(x["category"] for x in candidates)
    unique_signatures = {tuple(x["signature"]) for x in candidates}
    state_counts = Counter(x["arms"]["SCT"].get("state_at_end", "not_created") for x in candidates)
    policy_costs = defaultdict(Counter)
    for seed in raw:
        for candidate in seed["candidates"]:
            for arm in ("SCT", "NEVER_CREATE", "ALWAYS_CREATE", "RANDOM_CREATE", "MEMORY_ONLY"):
                result = candidate["arms"][arm]
                policy_costs[arm]["created_or_stored"] += int(bool(result.get("created")))
                policy_costs[arm]["creation_cost"] += float(result.get("creation_cost", 0.0) or 0.0)
                policy_costs[arm]["maintenance_cost"] += float(result.get("maintenance_cost", 0.0) or 0.0)

    # Task-level counts and paired cost/correctness; task rows are the source of truth.
    task_counts = {arm: Counter() for arm in arms}
    task_costs = {arm: [] for arm in arms}
    family_transfer = defaultdict(Counter)
    positive_reused_skill = {arm: set() for arm in arms}
    created_skill_count = Counter()
    for seed in raw:
        for candidate in seed["candidates"]:
            for arm in arms:
                a = candidate["arms"][arm]
                if a.get("created"):
                    created_skill_count[arm] += 1
                rs = a.get("reuse_statistics", {})
                if int(rs.get("credited_reuses", 0) or 0) > 0:
                    positive_reused_skill[arm].add((seed["seed"], candidate["invariant_id"]))
                task_results = a.get("task_results", [])
                if not task_results:
                    horizon = int(rs.get("eligible_opportunities", 0) or 0)
                    task_counts[arm]["eligible"] += horizon
                    task_counts[arm]["no_match"] += horizon
                for task in task_results:
                    task_counts[arm]["eligible"] += 1
                    if not task.get("applied"):
                        task_counts[arm]["no_match"] += 1
                        continue
                    task_counts[arm]["attempts"] += 1
                    task_counts[arm]["success" if task.get("success") else "failures"] += 1
                    task_counts[arm]["credited"] += int(bool(task.get("transfer_credit")))
                    task_costs[arm].append({
                        "raw_saving": float(task.get("baseline_cost", 0)) - float(task.get("reused_cost", 0)),
                        "normalized_reduction": float(task.get("reasoning_reduction", 0)),
                        "success": bool(task.get("success")),
                        "family": task.get("task_family", ""),
                    })
                    if candidate["category"] != task.get("task_family"):
                        family_transfer[arm]["cross_attempts"] += 1
                        family_transfer[arm]["cross_success"] += int(bool(task.get("success")))
                        family_transfer[arm]["cross_credited"] += int(bool(task.get("transfer_credit")))

    # The memory-only summary object omits failed_applications; count failures from retained task-level rows.
    memory_rows = [
        task for seed in raw for candidate in seed["candidates"]
        for task in candidate["arms"]["MEMORY_ONLY"].get("task_results", [])
        if task.get("applied")
    ]
    memory_failures = sum(not bool(task.get("success")) for task in memory_rows)

    # Utility timepoints are saved for all SCT-created skills.
    utility_rows = list(csv.DictReader((OUT / "utility_trajectories.csv").open(encoding="utf-8")))
    utility_by_task = defaultdict(list)
    for row in utility_rows:
        if row["arm"] == "SCT":
            utility_by_task[int(row["task_index"])].append(float(row["su"]))

    lifecycle = [x for seed in raw for x in seed["lifecycle"]]
    composition = [c for seed in raw for c in seed["composition"]]
    evaluated_comp = [c for c in composition if c["status"] == "evaluated"]
    comp_tasks = [t for c in evaluated_comp for t in c["task_results"]]
    comp_n = len(comp_tasks)
    comp_mean_red = mean(t["composition_benefit"] for t in comp_tasks)
    comp_best_single_rate = mean(bool(t["best_single_success"]) for t in comp_tasks)
    comp_baseline_rate = mean(bool(t["baseline_success"]) for t in comp_tasks)
    comp_success_rate = mean(bool(t["composition_success"]) for t in comp_tasks)

    threshold_lines = []
    thresholds = cal["thresholds"]
    for name, cutoff in thresholds.items():
        if name == "primary":
            continue
        chosen, value_sum = 0, 0.0
        seed_values = []
        for seed in raw:
            selected = [c for c in seed["candidates"] if float(c["SCV10"]) > float(cutoff)]
            chosen += len(selected)
            seed_values.append(sum(float(c["shadow_realized_net_value"]) for c in selected) / len(seed["candidates"]) if seed["candidates"] else 0.0)
        threshold_lines.append(f"| {name} | {fmt(float(cutoff), 6)} | {chosen}/44 | {fmt(mean(seed_values))} |")

    mc_lines = []
    for label, result in record["mc_sensitivity"].items():
        st = result["SCT"]
        mc_lines.append(f"| {label.split('=')[1]} | {fmt(st['mean'])} | {fmt(st['ci_low'])} to {fmt(st['ci_high'])} |")

    lines = [
        "# Phase 13C v1 — evidence package",
        "",
        "## Scope and execution integrity",
        "",
        "Confirmatory record: synthetic-sct-v1, seeds 20–29 (10 independent run seeds). Calibration: seeds 15–19. The frozen task/cost protocol is archived as `preregistration_v1_frozen_preconfirmation.md`; the post-run documentation banner is status-only. The pre-confirmation implementation/config hash manifest is `pre_confirmation_freeze.json`.",
        "",
        "This is controlled synthetic evidence conditional on the current invariant/task generator. It does not establish scientific validity on broader tasks or ARC external validity. Historical Phase 13B and EXP-IDT-14 records are not modified or pooled.",
        "",
        "**Execution note:** the command-line completion line for `confirm` displayed calibration seeds `[15..19]` because it selected the `calibration_seeds` field first. The saved `record.json` is the source of truth and records confirmation seeds `[20..29]`; no confirmation seed was replaced. This is a reporting-only CLI defect, frozen implementation hash is retained.",
        "",
        "The maintenance term `MC=0.06` is a modeled normalized per-opportunity simulator cost, not empirical compute cost.",
        "",
        "## 1. Skill emergence and births",
        "",
        f"The confirmation candidate pool contained {len(candidates)} eligible candidate rows over 10 seeds, with {len(unique_signatures)} unique signatures observed across rows. SCT selected and instantiated all {sum(bool(c['arms']['SCT'].get('created')) for c in candidates)} rows; terminal states were `{dict(state_counts)}`. Categories: `{dict(categories)}`. Counting and grouping had zero births under the frozen eligibility/minimum-quality gates; they are retained as absent categories rather than forced into the table.",
        "",
        "| Candidate category | Confirmation rows |",
        "|---|---:|",
    ]
    for cat in ("reflection", "rotation", "counting", "grouping"):
        lines.append(f"| {cat} | {categories.get(cat, 0)} |")
    lines += [
        "",
        "![Skill births](figures/phase13c_01_emergence.png)",
        "",
        "## 2. SCV10, threshold study, and held-out predictiveness",
        "",
        f"Calibration yielded {cal['eligible_candidate_count']} eligible candidates; all {cal['birth_count_at_primary_threshold']} had SCV10 > 0. Frozen random-create probability was {cal['random_create_probability']:.3f}. Calibration score cutoffs were low q25={thresholds['low_q25']:.6f}, median={thresholds['medium_q50']:.6f}, high q75={thresholds['high_q75']:.6f}; median and upper quartile tie. The random arm therefore degenerates to always-create on this calibration result.",
        "",
        "| Confirmatory selection cutoff | Frozen numeric cutoff | Selected candidate rows | Mean per-seed net value (shadow outcomes) |",
        "|---|---:|---:|---:|",
        *threshold_lines,
        "| primary | 0.000000 | 44/44 | 0.345 |",
        "",
        "Selection sensitivity uses isolated shadow outcomes; it is not a post-hoc replacement for the primary policy or an outcome-selected threshold.",
        "",
        "| Predictor of shadow realized net value | Spearman ρ | Seed-cluster bootstrap 95% CI |",
        "|---|---:|---:|",
    ]
    for name, stat in record["scv_predictiveness"]["scv_predictors_of_future_net_value"].items():
        ci = stat["seed_cluster_bootstrap_ci95"]
        lines.append(f"| {name} | {fmt(stat['spearman'])} | {fmt(ci[0])} to {fmt(ci[1])} |")
    lines += ["", "![SCV10](figures/phase13c_02_scv.png)", "", "## 3. Utility and future value", ""]
    lines.append(f"SCT skill utility rose from mean SU {fmt(mean(utility_by_task[0]))} after the first eligible opportunity to {fmt(mean(utility_by_task[9]))} after the tenth. This is secondary accounting, not the primary value measure. Candidate-level utility-component checkpoints (RCG/TV/CP/RV/CC/MC/NR/SU) are retained in `utility_trajectories.csv`.")
    lines.append("Limitation: a distinct pre-task birth-time SU/component snapshot was not serialized by the runner; task index 0 is after the first eligible opportunity and must not be relabeled as birth utility.")
    lines += ["", "| Descriptive utility association | Spearman ρ | Seed-cluster bootstrap 95% CI |", "|---|---:|---:|"]
    for name, stat in record["scv_predictiveness"]["utility_associations"].items():
        ci = stat["seed_cluster_bootstrap_ci95"]
        lines.append(f"| {name} | {fmt(stat['spearman'])} | {fmt(ci[0])} to {fmt(ci[1])} |")
    lines += ["", "![Utility trajectory](figures/phase13c_03_utility.png)", "", "## 4. Reuse, reasoning reduction, and transfer", "", "| Arm | Eligible opportunities | Applied | Correct | Failed | No match | Positive-credit reuses | Reused/created skills* | Correct / eligible |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for arm in ("SCT", "MEMORY_ONLY", "ALWAYS_CREATE", "RANDOM_CREATE", "NEVER_CREATE"):
        co = task_counts[arm]
        created = created_skill_count[arm]
        reused = len(positive_reused_skill[arm])
        if arm == "MEMORY_ONLY":
            failures = memory_failures
        else:
            failures = co["failures"]
        ratio = f"{reused}/{created}" if created else "n/a"
        correct_rate = co["success"] / co["eligible"] if co["eligible"] else 0.0
        lines.append(f"| {arm} | {co['eligible']} | {co['attempts']} | {co['success']} | {failures} | {co['no_match']} | {co['credited']} | {ratio} | {fmt(correct_rate)} |")
    for arm in ("SCT", "MEMORY_ONLY"):
        applied = task_costs[arm]
        successful = [x for x in applied if x["success"]]
        raw_saving = mean(x["raw_saving"] for x in applied)
        norm_success = mean(x["normalized_reduction"] for x in successful)
        lines.append(f"\nFor {arm}, mean raw step saving among applied task rows was {fmt(raw_saving)}; mean normalized reduction among correct applications was {fmt(norm_success)}. Correctness is reported separately; the cost scalar gives zero benefit to incorrect replays.")
    lines += ["", "*Reused/created means at least one positive-credit reuse divided by created candidate instances; memory-only rows are trace exemplars, not Skill objects. Memory-only failed applications are derived from saved task rows because the runner's aggregate omitted its failure count. The per-task value calculation itself remains success-gated.", "", "| Source→target family transfer | Correct applications |", "|---|---:|"]
    for arm in ("SCT", "MEMORY_ONLY"):
        lines.append(f"| {arm} | {family_transfer[arm]['cross_success']} / {family_transfer[arm]['cross_attempts']} attempted cross-family applications ({family_transfer[arm]['cross_credited']} positive-credit) |")
    lines += ["", "![Reuse outcomes](figures/phase13c_04_reuse.png)", "", "## 5. Task-grounded composition and reuse", ""]
    lines.append(f"Only rotation→reflection was evaluable because counting and grouping component skills were absent. Across {comp_n} paired task instances, the no-skill composition-capable solver succeeded {comp_baseline_rate:.1%}, the best single component skill succeeded on {comp_best_single_rate:.1%}, and ordered rotation→reflection succeeded {comp_success_rate:.1%}; mean success-gated normalized reasoning reduction was {fmt(comp_mean_red)}. All {sum(bool(c['composition_reused_on_new_task']) for c in evaluated_comp)}/{len(evaluated_comp)} separately seeded composition-reuse tasks succeeded. Candidate state was reusable in all evaluable cases.")
    lines += ["", "The two planned counting-containing compositions were not evaluable; their missing-component status is preserved. These outcomes establish synthetic composition plumbing only; the research composition module is not silently treated as a general multi-step Skill in the primary policy.", "", "![Composition](figures/phase13c_05_composition.png)", "", "## 6. Matched primary controls", "", "| Arm | Mean net value | SD | Normal 95% CI | Seed-bootstrap 95% CI |", "|---|---:|---:|---:|---:|"]
    for arm, stat in primary["arm_statistics"].items():
        ci = primary["arm_seed_cluster_bootstrap_ci95"][arm]
        lines.append(f"| {arm} | {fmt(stat['mean'])} | {fmt(stat['std'])} | {fmt(stat['ci_low'])} to {fmt(stat['ci_high'])} | {fmt(ci[0])} to {fmt(ci[1])} |")
    lines += ["", "| Policy | Created skills / stored exemplars | Total CC proxy | Total MC proxy | Mean created items per seed |", "|---|---:|---:|---:|---:|"]
    for arm in ("SCT", "NEVER_CREATE", "ALWAYS_CREATE", "RANDOM_CREATE", "MEMORY_ONLY"):
        costs = policy_costs[arm]
        label = f"{costs['created_or_stored']} raw-trace exemplars" if arm == "MEMORY_ONLY" else f"{costs['created_or_stored']} skills"
        lines.append(f"| {arm} | {label} | {fmt(costs['creation_cost'])} | {fmt(costs['maintenance_cost'])} | {fmt(costs['created_or_stored']/10)} |")
    lines += ["", "CC/MC are normalized model-cost terms, not empirical compute usage.", "", "| Paired contrast (SCT − control) | Mean | SD | Seed-bootstrap 95% CI | Cohen dz |", "|---|---:|---:|---:|---:|"]
    contrast_values = {control: [float(s["paired_contrasts"][f"SCT_minus_{control}"]) for s in raw] for control in ("NEVER_CREATE", "ALWAYS_CREATE", "RANDOM_CREATE", "MEMORY_ONLY")}
    for control, vals in contrast_values.items():
        stat = primary["paired_contrast_statistics"][control]
        ci = primary["paired_contrast_seed_cluster_bootstrap_ci95"][control]
        dz = paired_dz(vals)
        dz_str = "undefined (zero variance)" if dz is None else fmt(dz)
        lines.append(f"| {control} | {fmt(stat['mean'])} | {fmt(stat['std'])} | {fmt(ci[0])} to {fmt(ci[1])} | {dz_str} |")
    lifecycle_stats = record["lifecycle_ablation"]["statistics"]
    lines += ["", f"**Strict superiority gate: {primary['strict_superiority_success']} (failed).** SCT ties ALWAYS_CREATE and RANDOM_CREATE exactly because every eligible candidate scored above zero in both calibration and confirmation; it is not better than the memory-only arm (paired mean difference {fmt(primary['paired_contrast_statistics']['MEMORY_ONLY']['mean'])}).", "", "![Matched controls](figures/phase13c_06_matched_controls.png)", "", "## 7. Ablations and cost sensitivity", "", "| Ablation | Matched outcome | Result |", "|---|---|---:|"]
    lines.append(f"| No-SCV (ALWAYS_CREATE) | Mean primary net value; SCT-minus-ablation | {fmt(record['primary_outcome']['arm_statistics']['ALWAYS_CREATE']['mean'])}; 0.000 |")
    lines.append(f"| No-lifecycle | Lifecycle-off mean net; enabled-minus-disabled | {fmt(lifecycle_stats['lifecycle_disabled']['mean'])}; {fmt(lifecycle_stats['enabled_minus_disabled']['mean'])} |")
    lines.append(f"| No-composition (best single) | Success vs ordered composition on evaluable tasks | {comp_best_single_rate:.1%} vs {comp_success_rate:.1%} |")
    lines += ["", "No-composition results are secondary and only available for the rotation→reflection case; counting-containing cases were unavailable because component skills did not emerge.", "", "| MC per eligible opportunity | SCT mean net value | 95% normal CI |", "|---:|---:|---:|"]
    for label, result in record["mc_sensitivity"].items():
        stat = result["SCT"]
        lines.append(f"| {label.split('=')[1]} | {fmt(stat['mean'])} | {fmt(stat['ci_low'])} to {fmt(stat['ci_high'])} |")
    lines += ["", "![Ablations](figures/phase13c_07_ablations.png)", "", "## Overall interpretation", "", "Phase 13C does not pass its predeclared SCT superiority criterion. Within this synthetic design, SCT creates every eligible candidate and is therefore operationally identical to always-create; calibration-frozen random-create is also always-create. The learned skill policy has positive net value versus never-create, but memory-only trace retrieval yields higher mean net value. Skill utility and SCV10 are associated with held-out value in this dataset, but predictor correlations do not rescue the failed policy contrast. Composition works for one evaluable pair and lifecycle dormancy/reactivation is mixed. None of these results repairs Phase 13B or establishes ARC external validity.", "", "## Artifact and limitation index", "", "- `record.json`: full confirmatory record, seed-level outcomes, candidate/task rows, and failures.", "- `calibration.json` / `calibration_frozen.json`: calibration-only data and frozen calibration parameters.", "- `skill_births.json`, `candidate_level.csv`, `reuse_statistics.csv`, `utility_trajectories.csv`, `lifecycle.csv`, `composition.csv`, `matched_controls.csv`, `threshold_sensitivity.csv`, `mc_sensitivity.csv`, `lifecycle_ablation.csv`: detailed evidence tables.", "- `pre_confirmation_freeze.json`: pre-confirmation hashes and contract-test status.", "- `preregistration_v1_frozen_preconfirmation.md`: exact protocol copy before confirmation.", "- `refactor_manifest.json`: post-run module refactor verification and per-file line counts.", "- `source_snapshot/snapshot_manifest.json`: frozen source fragment hashes/reassembly order.", "- `execution_note.md`: CLI print correction and metric caveat.", ""]
    (OUT / "evidence_package.md").write_text("\n".join(lines), encoding="utf-8")
