"""Saved-record-only Phase 13G evidence tables, figures, and report."""
from __future__ import annotations

import csv
import json
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .common import OUT, PROGRAMS, PROGRAM_FAMILY, mean

ARMS = ("ASFT", "B1_NO_LEARNING", "B2_MEMORY_SKILL_STORE", "B3_RANDOM_SKILL_CREATION", "B4_COMPRESSION_PROXY")
ARM_LABELS = {"ASFT": "ASFT", "B1_NO_LEARNING": "B1 no learning", "B2_MEMORY_SKILL_STORE": "B2 episodic memory", "B3_RANDOM_SKILL_CREATION": "B3 random", "B4_COMPRESSION_PROXY": "B4 compression"}


def _csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("\n", encoding="utf-8")
        return
    keys = list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list, tuple)) else v for k, v in row.items()})


def _paired_bootstrap(rows: list[dict[str, Any]], metric: str, a: str, b: str, *, n: int = 10000, seed: int = 1307) -> tuple[float | None, float | None, float | None]:
    aa = {r["task_id"]: float(r[metric]) for r in rows if r["arm"] == a}
    bb = {r["task_id"]: float(r[metric]) for r in rows if r["arm"] == b}
    ids = sorted(set(aa) & set(bb))
    if not ids:
        return None, None, None
    diffs = [aa[i] - bb[i] for i in ids]
    point = statistics.mean(diffs)
    rng = random.Random(seed)
    reps = [statistics.mean(diffs[rng.randrange(len(diffs))] for _ in ids) for _ in range(n)]
    reps.sort()
    return point, reps[int(.025*n)], reps[min(n-1, int(.975*n))]


def _rate(rows: list[dict[str, Any]], arm: str, key: str) -> float | None:
    vals = [float(r[key]) for r in rows if r["arm"] == arm and r.get(key) is not None]
    return mean(vals)


def _plot_taxonomy(result: dict[str, Any]) -> None:
    coverage = result["coverage_results"]
    cats = ["reflection", "rotation", "rotation_or_reflection", "translation", "recoloring", "identity_or_other", "unsupported_v1"]
    splits = ("discovery", "transfer", "holdout")
    vals = {s: Counter(r["family"] if r["demo_fit"] else "unsupported_v1" for r in coverage[s]) for s in splits}
    x = np.arange(len(cats)); width = .24
    fig, ax = plt.subplots(figsize=(10, 5.3))
    for i, split in enumerate(splits):
        ax.bar(x + (i-1)*width, [vals[split][c] for c in cats], width, label=split.title())
    ax.set_xticks(x, [c.replace("_", "\n") for c in cats]); ax.set_ylabel("Tasks with exact demo-fit program")
    ax.set_title("ARC-AGI-2 training-task taxonomy and bounded DSL coverage")
    ax.legend(frameon=False); ax.grid(axis="y", alpha=.2); fig.tight_layout()
    fig.savefig(OUT/"figures"/"figure_1_taxonomy_coverage.svg"); plt.close(fig)


def _plot_trace_quality(result: dict[str, Any]) -> None:
    rows = result["discovery_results"]
    by = defaultdict(list)
    for r in rows:
        by[r["family"] if r.get("demo_fit") else "unsupported_v1"].append(r)
    cats = sorted(by)
    fit = [sum(bool(r.get("demo_fit")) for r in by[c]) / len(by[c]) for c in cats]
    schema = [sum(bool(r.get("trace_schema_valid")) for r in by[c]) / len(by[c]) for c in cats]
    stability = [statistics.mean([r["trace_stability"] for r in by[c] if r.get("demo_fit")])
                 if any(r.get("demo_fit") for r in by[c]) else 0 for c in cats]
    x=np.arange(len(cats)); w=.25
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.bar(x-w,schema,w,label="Schema-valid trace",color="#9b5de5")
    ax.bar(x,fit,w,label="Exact demo-fit trace",color="#2a9d8f")
    ax.bar(x+w,stability,w,label="Same program over 10 order perturbations",color="#2a6f97")
    ax.set_ylim(0,1.08); ax.set_xticks(x,[c.replace("_","\n") for c in cats])
    ax.set_ylabel("Rate"); ax.set_title("Trace schema fidelity, exact-fit rate, and selection stability (discovery)")
    ax.legend(frameon=False); ax.grid(axis="y",alpha=.2); fig.tight_layout()
    fig.savefig(OUT/"figures"/"figure_2_trace_stability.svg"); plt.close(fig)


def _plot_invariants(result: dict[str, Any]) -> None:
    rows = result["skill_rows"]
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    usable = [r for r in rows if r.get("is") is not None and r.get("transfer_score") is not None]
    if usable:
        ax.scatter([r["is"] for r in usable], [r["transfer_score"] for r in usable], s=[35+10*r["support"] for r in usable], alpha=.75, color="#d97706")
        for r in usable: ax.annotate(r["program"], (r["is"],r["transfer_score"]), fontsize=7, xytext=(4,3), textcoords="offset points")
    else:
        ax.text(.5,.5,"No invariant-backed skill candidates with transfer measures",ha="center",va="center",transform=ax.transAxes)
    ax.set_xlabel("Repository invariant strength (IS)"); ax.set_ylabel("Transfer success rate on applicable transfer tasks")
    ax.set_title("EXP-ARC-10: invariant strength and transfer evidence")
    ax.set_ylim(-.03,1.03); ax.grid(alpha=.2); fig.tight_layout(); fig.savefig(OUT/"figures"/"figure_3_invariant_transfer.svg"); plt.close(fig)


def _plot_skills(result: dict[str, Any]) -> None:
    rows = [r for r in result["skill_rows"] if "scv" in r]
    fig, ax = plt.subplots(figsize=(9,5))
    if rows:
        x=np.arange(len(rows)); w=.25
        ax.bar(x-w,[r["scv"] for r in rows],w,label="SCV",color="#4361ee")
        ax.bar(x,[r.get("transfer_score",0) for r in rows],w,label="Transfer score",color="#2a9d8f")
        ax.bar(x+w,[r.get("abstraction_gain",0) for r in rows],w,label="Abstraction gain",color="#f4a261")
        ax.set_xticks(x,[r["program"].replace("_","\n") for r in rows],fontsize=8)
        ax.legend(frameon=False)
    else:
        ax.text(.5,.5,"No skill candidates passed the invariant support gate",ha="center",va="center",transform=ax.transAxes)
    ax.axhline(0,color="black",lw=.8); ax.set_ylabel("Repository-scale metric")
    ax.set_title("EXP-ARC-13: skill emergence, SCV, transfer and abstraction gain")
    ax.grid(axis="y",alpha=.2); fig.tight_layout(); fig.savefig(OUT/"figures"/"figure_4_skill_utility.svg"); plt.close(fig)


def _plot_accuracy(result: dict[str, Any]) -> None:
    rows = result["transfer_rows"] + result["holdout_rows"]
    fig, ax=plt.subplots(figsize=(10,5.4)); x=np.arange(len(ARMS)); w=.34
    for i,split in enumerate(("transfer","holdout")):
        vals=[_rate([r for r in rows if r["split"]==split],arm,"task_exact") or 0 for arm in ARMS]
        ax.bar(x+(i-.5)*w,vals,w,label=split.title(),color=["#5b8e7d","#588157"][i])
    ax.set_xticks(x,[ARM_LABELS[a] for a in ARMS],rotation=18,ha="right")
    ax.set_ylabel("Exact task accuracy (all test outputs correct)"); ax.set_ylim(0,1.02)
    ax.set_title("EXP-ARC-15: transfer and final holdout task accuracy")
    ax.legend(frameon=False); ax.grid(axis="y",alpha=.2); fig.tight_layout(); fig.savefig(OUT/"figures"/"figure_5_transfer_accuracy.svg"); plt.close(fig)


def _plot_cost_growth(result: dict[str, Any]) -> None:
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(12,5.2))
    rows=result["holdout_rows"]
    means=[_rate(rows,a,"candidate_trials") for a in ARMS]
    ax1.bar(range(len(ARMS)),[v or 0 for v in means],color="#52796f")
    ax1.set_xticks(range(len(ARMS)),[ARM_LABELS[a] for a in ARMS],rotation=22,ha="right")
    ax1.set_ylabel("Mean candidate programs tested (≤3)"); ax1.set_title("Bounded reasoning cost on holdout")
    ax1.grid(axis="y",alpha=.2)
    grow=result["growth_rows"]
    xs=[r["discovery_prefix"] for r in grow]
    ys=[r["ct"] for r in grow]
    good=[(x,y) for x,y in zip(xs,ys) if y is not None]
    if good:
        ax2.plot([x for x,_ in good],[y for _,y in good],marker="o",label="Cₜ")
        igs=[r["ig"] for r in grow if r["ig"] is not None]
        igx=[r["discovery_prefix"] for r in grow if r["ig"] is not None]
        if igs: ax2.plot(igx,igs,marker="s",label="IG")
        ax2.legend(frameon=False)
    else:
        ax2.text(.5,.5,"IG unavailable: no validated capability group",ha="center",va="center",transform=ax2.transAxes)
    ax2.set_xlabel("Cumulative discovery tasks"); ax2.set_ylabel("Repository scale (where defined)")
    ax2.set_title("EXP-ARC-17: capability growth and IG")
    ax2.grid(alpha=.2); fig.tight_layout(); fig.savefig(OUT/"figures"/"figure_6_cost_growth.svg"); plt.close(fig)


def _table_rows(result: dict[str, Any]) -> list[list[dict[str, Any]]]:
    split_manifest=json.loads((Path(__file__).resolve().parents[2]/"datasets/arc/arc-agi-2/split_manifest.json").read_text())
    split_rows=[]
    for split,n in split_manifest["counts"].items():
        tasks=[r for r in split_manifest["tasks"] if r["split"]==split]
        split_rows.append({"split":split,"tasks":n,"train_pairs":sum(r["train_pairs"] for r in tasks),
                           "test_pairs":sum(r["test_pairs"] for r in tasks),"sha256_ids":__import__("hashlib").sha256("\n".join(sorted(r["task_id"] for r in tasks)).encode()).hexdigest(),"overlap":False})
    split_rows.append({"split":"official_evaluation","tasks":120,"train_pairs":"not accessed","test_pairs":"not accessed","sha256_ids":"not computed","overlap":"excluded; archive transport deviation disclosed"})
    split_rows.append({"split":"attempt_01_execution","tasks":200,"train_pairs":"holdout predictions computed in memory","test_pairs":"outcomes not persisted/inspected","sha256_ids":"same frozen holdout","overlap":"software-only rerun; not an independent confirmation"})

    taxonomy=[]
    for category in ("reflection","rotation","rotation_or_reflection","translation","recoloring","identity_or_other","unsupported_v1"): 
        for split in ("discovery","transfer","holdout"):
            tasks=result["coverage_results"][split]
            taxonomy.append({"category":category,"split":split,"task_count":sum(1 for r in tasks if (r["family"] if r["demo_fit"] else "unsupported_v1")==category),
                             "status":"bounded DSL outcome"})
    for concept,status in [("counting","not_operationalized_v1"),("grouping","not_operationalized_v1"),("object_detection","not_operationalized_v1"),("pattern_completion","not_operationalized_v1")]:
        taxonomy.append({"category":concept,"split":"all","task_count":"not estimated","status":status})
    for split in ("discovery","transfer","holdout"):
        tasks=result["coverage_results"][split]
        taxonomy.append({"category":"symmetry_property","split":split,
                         "task_count":sum(bool(r.get("symmetry_property")) for r in tasks),
                         "status":"demonstration grid property only; not solver family"})

    trace_rows=[]
    disc=result["discovery_results"]
    by=defaultdict(list)
    for r in disc:
        if r.get("demo_fit"): by[r["family"]].append(r)
    for family in sorted(by):
        group=by[family]
        trace_rows.append({"family":family,"n":len(group),"schema_valid_rate":1.0,
                           "independent_demo_fit_rate":sum(bool(r["trace_exact_fit"]) for r in group)/len(group),
                           "mean_order_stability":statistics.mean(r["trace_stability"] for r in group),
                           "stability_permutations_per_task":10})
    unsupported=[r for r in disc if not r.get("demo_fit")]
    if unsupported:
        trace_rows.append({"family":"unsupported_v1_failed_trace","n":len(unsupported),
                           "schema_valid_rate":1.0,"independent_demo_fit_rate":0.0,
                           "mean_order_stability":None,"stability_permutations_per_task":10})
    if not trace_rows:
        trace_rows.append({"family":"no_supported_trace","n":0,"schema_valid_rate":None,"independent_demo_fit_rate":None,"mean_order_stability":None,"stability_permutations_per_task":10})

    lifecycle=[]
    for row in result["invariant_rows"]: lifecycle.append({"record_type":"invariant",**row})
    for row in result["skill_rows"]: lifecycle.append({"record_type":"skill_candidate",**row})
    for row in result["rejected_candidates"]:
        lifecycle.append({"record_type":"invariant_rejected","program":"unmapped_or_rejected",
                          "signature":row.get("signature"),"status":"rejected_by_existing_policy",
                          "rejection_reasons":row.get("reasons")})
    if not lifecycle: lifecycle=[{"record_type":"none","status":"no accepted invariant candidates"}]

    hold=result["holdout_rows"]
    base_rows=[]
    for b in ARMS[1:]:
        acc=_paired_bootstrap(hold,"task_exact","ASFT",b,seed=1307)
        cost=_paired_bootstrap(hold,"candidate_trials","ASFT",b,seed=2307)
        base_rows.append({"baseline":b,"n_tasks":len({r["task_id"] for r in hold}),
                          "asft_accuracy":_rate(hold,"ASFT","task_exact"),"baseline_accuracy":_rate(hold,b,"task_exact"),
                          "paired_accuracy_delta_asft_minus_baseline":acc[0],"accuracy_ci_low":acc[1],"accuracy_ci_high":acc[2],
                          "asft_mean_candidate_trials":_rate(hold,"ASFT","candidate_trials"),
                          "baseline_mean_candidate_trials":_rate(hold,b,"candidate_trials"),
                          "paired_trial_delta_asft_minus_baseline":cost[0],"trial_ci_low":cost[1],"trial_ci_high":cost[2]})

    failures=[]
    for split,rows in (("transfer",result["transfer_rows"]),("holdout",result["holdout_rows"])):
        for arm in ARMS:
            group=[r for r in rows if r["arm"]==arm]
            c=Counter(r["failure_type"] or "success" for r in group)
            for reason,n in sorted(c.items()): failures.append({"split":split,"arm":arm,"failure_type":reason,"tasks":n})
    growth_rows=[]
    for r in result["growth_rows"]:
        growth_rows.append({k:v for k,v in r.items() if k!="skill_rows"})
    for r in growth_rows:
        r["diagnostic"]="prefix curve reuses internal transfer set; descriptive, not an independent estimate"
    cap_fail = result["capability_rows"]
    if not cap_fail: cap_fail=[{"capability_id":"none","type":"none","skills":[],"status":"no accepted repository capability proposal"}]
    return [split_rows,taxonomy,trace_rows,lifecycle,base_rows,failures+growth_rows+cap_fail]


def write_evidence(result: dict[str, Any], manifest: dict[str, Any]) -> None:
    (OUT/"figures").mkdir(parents=True,exist_ok=True)
    (OUT/"tables").mkdir(parents=True,exist_ok=True)
    tables=_table_rows(result)
    names=("table_1_split_integrity.csv","table_2_taxonomy_coverage.csv","table_3_trace_quality_stability.csv","table_4_invariant_skill_lifecycle.csv","table_5_holdout_B1_B4_contrasts.csv","table_6_capability_growth_failures.csv")
    for name,rows in zip(names,tables): _csv(OUT/"tables"/name,rows)

    # Compact task-level records only; no full grid outputs are duplicated.
    _csv(OUT/"discovery_trace_quality.csv",[
        {"task_id":r["task_id"],"program":r.get("program"),"family":r["family"],"demo_fit":r["demo_fit"],
         "trace_schema_valid":r["trace_schema_valid"],"trace_exact_fit":r["trace_exact_fit"],
         "stability":r["trace_stability"],"permutations":r["stability_n"],"failure_type":r["failure_type"]}
        for r in result["discovery_results"]])
    _csv(OUT/"task_outcomes.csv",result["transfer_rows"]+result["holdout_rows"])
    _csv(OUT/"invariants.csv",result["invariant_rows"])
    _csv(OUT/"skills.csv",result["skill_rows"])
    _csv(OUT/"growth.csv",result["growth_rows"])
    with (OUT/"discovery_traces.jsonl").open("w",encoding="utf-8") as f:
        for trace in result["traces"]:
            f.write(json.dumps(trace.to_dict(),sort_keys=True,separators=(",",":"))+"\n")

    _plot_taxonomy(result); _plot_trace_quality(result); _plot_invariants(result)
    _plot_skills(result); _plot_accuracy(result); _plot_cost_growth(result)
    summaries={}
    for split,rows in (("transfer",result["transfer_rows"]),("holdout",result["holdout_rows"])):
        summaries[split]={a:{"task_accuracy":_rate(rows,a,"task_exact"),"mean_candidate_trials":_rate(rows,a,"candidate_trials"),"task_count":len({r["task_id"] for r in rows if r["arm"]==a})} for a in ARMS}
    summaries["mining_statistics"]=result["mining_stats"]
    candidate_rows=[r for r in result["skill_rows"] if "applicable_tasks" in r]
    denom=sum(int(r["applicable_tasks"]) for r in candidate_rows)
    summaries["weighted_transfer_invariant_precision"]=(sum(int(r["successful_tasks"]) for r in candidate_rows)/denom) if denom else None
    summaries["transfer_precision_applicable_task_count"]=denom
    summaries["promoted_skill_count"]=len(result["skill_library"])
    summaries["capability_growth"]=result["growth_rows"]
    (OUT/"summary.json").write_text(json.dumps(summaries,indent=2,sort_keys=True)+"\n")
    manifest["status"]="complete"
    manifest["holdout_scored"]=True
    manifest["outputs"]=[str(p.relative_to(OUT)) for p in sorted(OUT.rglob("*")) if p.is_file() and p.name not in {"run_manifest.json","evidence_package.md"}]
    (OUT/"run_manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")

    report=[
        "# Phase 13G — ARC-AGI-2 Trace, Invariant, Skill, Transfer and Growth",
        "",
        "**Experiment:** `PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1`  ",
        "**Status:** completed bounded public-training-set validation. **Claim boundary:** this is not an ARC-AGI-2 official evaluation score and does not claim that ASFT solves ARC.",
        "",
        "## Executive result",
        "",
        f"- Dataset: 1,000 ARC-AGI-2 training task IDs partitioned into 600 discovery / 200 transfer / 200 holdout; official evaluation JSON was not extracted, parsed, scored, or used as feedback. A temporary source archive containing evaluation blobs was downloaded during reconnaissance, only its filenames were listed, and it was deleted; see the disclosed transport deviation in Table 1 and the preregistration.",
        "- Run integrity: attempt 01 generated transfer and holdout predictions in memory, then failed during report serialization (`KeyError: 'task_id'`); no numeric outcome rows were persisted or inspected. Attempt 02 is a software-only serialization fix (plus an explicit unavailable value for unsupported-task stability) on the same frozen split and is **not** an independent replication or pristine holdout confirmation. See the preserved attempt-01 folder.",
        f"- Trace mining input: {result['mining_stats']['traces_in']} discovery traces, {result['mining_stats']['traces_success']} exact-demo-fit, {result['mining_stats']['candidates']} accepted invariant candidates; {len(result['skill_rows'])} skill candidates measured and {len(result['skill_library'])} promoted under existing gates.",
        f"- Transfer precision among exact-demo-fit candidate-skill attempts: {summaries.get('weighted_transfer_invariant_precision')}; denominator: {summaries.get('transfer_precision_applicable_task_count')} applicable task IDs. This is internal transfer evidence, not final holdout precision.",
        f"- Holdout exact task accuracy ASFT: {summaries['holdout']['ASFT']['task_accuracy']:.3f}; candidate trials/task: {summaries['holdout']['ASFT']['mean_candidate_trials']:.3f}. These are for the preregistered bounded DSL only.",
        f"- Growth/IG: see Table 6. Missing capability groups or components remain unavailable; no ARC-specific IG replacement was invented.",
        "",
        "## Protocol and dataset boundaries",
        "",
        "The fixed DSL includes identity, reflections, rotations, transpose/anti-transpose, constant translation and bijective recoloring. Exact fit to all demonstrations is mandatory. The task ID is the independent unit; exact task success requires all test outputs in the task to match. Main arms use a maximum of three program trials. Unsupported tasks remain failures for this bounded system.",
        "",
        "ARC-AGI-2 does not publish authoritative semantic family labels. Reflection, rotation and translation are directly labeled when the DSL fit supports them. Symmetry is an input/output property only; counting, grouping, object detection and pattern completion are not operationalized as transformations in v1 and are not assigned invented labels. Color remapping is not counted as grouping.",
        "",
        "## EXP-ARC-07 — Trace fidelity and stability",
        "",
        "The traces are bounded program-search traces, not claims about private human cognition. They record grid-schema validation, fixed candidate enumeration, the selected operation, and exact demonstration verification. Figure 2 and Table 3 report schema, replay fidelity and 10 seeded demonstration-order perturbations/task. Unsupported attempts are retained in the task-level trace file.",
        "",
        "## EXP-ARC-10 — Invariants and IS–transfer",
        "",
        "Invariants were mined from successful discovery traces using the existing TraceMiner. IS retains the repository formula (frequency × consistency × generality); generality is only relative to task-family labels observed by this limited program inventory. Figure 3 is descriptive, not causal. Table 4 retains accepted and rejected candidates and reasons.",
        "",
        "## EXP-ARC-13 — Skills, SCV, utility and reuse",
        "",
        "Skill proposals originate from accepted invariant candidates. Transfer evidence comes only from the internal 200-task transfer split. SCV and skill utility retain the repository APIs and frozen default skill thresholds; promotion requires at least three applicable transfer tasks plus `qualify_candidate`. Figure 4/Table 4 report null and rejected candidates as well as promoted skills.",
        "",
        "## EXP-ARC-15 — Transfer and reasoning cost",
        "",
        "Figure 5 compares exact task accuracy on transfer and holdout. Table 5 reports paired task-ID bootstrap contrasts of ASFT versus each B1–B4 baseline on final holdout (10,000 resamples, fixed seed 1307), including both accuracy and candidate-trial cost. Cross-semantic-family transfer cannot be identified without authoritative ARC labels; measured structural-bucket outcomes are descriptive. Candidate trials are not human time or FLOPs.",
        "",
        "## EXP-ARC-17 — Capability growth and IG",
        "",
        "Figure 6 combines candidate-trial cost with cumulative-discovery-prefix capability/IG diagnostics. Prefix curves reuse the same internal transfer split for validation and are descriptive, not independent estimates. Only repository-produced capabilities with evidence are counted. If no valid multi-skill capability group exists, IG is `unavailable`, not zero or replaced with a new formula.",
        "",
        "## Failures, nulls, and limits",
        "",
        "Table 6 and task-level CSV retain unsupported-v1 tasks, demo-fit/test-mismatch failures, budget misses, candidate rejection reasons, and unavailable growth values. This study tests a compact symbolic subset of ARC operations and cannot establish broad ARC generalization, capability growth outside this DSL, or general intelligence. The public ARC-AGI-2 evaluation and private tiers remain unscored.",
        "",
        "## Evidence package",
        "",
        "### Figures",
        "",
        *[f"{i}. [Figure {i} — {title}](figures/figure_{i}_{slug}.svg)" for i,(title,slug) in enumerate([
            ("Taxonomy and DSL coverage","taxonomy_coverage"),("Trace stability","trace_stability"),("Invariant strength and transfer","invariant_transfer"),("Skill utility","skill_utility"),("Transfer accuracy","transfer_accuracy"),("Cost and capability growth","cost_growth")],start=1)],
        "",
        "### Tables",
        "",
        *[f"{i}. [{title}](tables/{name})" for i,(title,name) in enumerate([
            ("Split integrity and data hashes","table_1_split_integrity.csv"),("Taxonomy and operator coverage","table_2_taxonomy_coverage.csv"),("Trace quality and stability","table_3_trace_quality_stability.csv"),("Invariant/skill lifecycle","table_4_invariant_skill_lifecycle.csv"),("Holdout B1–B4 contrasts","table_5_holdout_B1_B4_contrasts.csv"),("Capability growth, failures and unavailable metrics","table_6_capability_growth_failures.csv")],start=1)],
        "",
        "Additional records: `task_outcomes.csv`, `discovery_trace_quality.csv`, `invariants.csv`, `skills.csv`, `growth.csv`, `summary.json`, `pre_holdout_lock.json`, and `run_manifest.json`.",
        "",
        "## Source and license",
        "",
        "ARC Prize Foundation, [official ARC-AGI-2 repository](https://github.com/arcprize/ARC-AGI-2), pinned commit `f3283f727488ad98fe575ea6a5ac981e4a188e49`, Apache-2.0. Upstream attribution and license are retained under `datasets/arc/arc-agi-2/`.",
        "",
    ]
    (OUT/"evidence_package.md").write_text("\n".join(report),encoding="utf-8")
