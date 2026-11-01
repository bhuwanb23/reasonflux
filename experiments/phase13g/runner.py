"""Phase 13G discovery, IDT/SCT pipeline, bounded transfer, and capability growth."""
from __future__ import annotations

import random
from collections import Counter
from typing import Any

from capability import CapabilityLibrary
from capability.config import CapabilityConfig
from capability.emerge import propose_capabilities_from_library
from capability.portfolio import compute_capability_portfolio, compute_system_capability_state
from core.invariant import Invariant
from core.skill import Skill, SkillCandidate, compute_scv
from core.states import InvariantState, SkillState
from evaluation.growth_config import GrowthConfig
from evaluation.growth_metrics import compute_ig
from invariants.detector import TraceMiner
from invariants.pattern_mining import MiningConfig
from invariants.specification import InvariantPolicy
from skills.candidate import from_invariant
from skills.config import SkillConfig
from skills.library import SkillLibrary
from skills.qualification import qualify_candidate
from skills.utility import refresh_skill_utility

from .common import (
    DATA, OUT, PROGRAMS, PROGRAM_FAMILY, family_taxonomy, load_named_split, load_task_rows, mean,
    normalized_distance, solve_task, structural_bucket, symmetry_demo_property, task_features, trace_for,
)

MIN_SUPPORT = 5
MIN_APPLICABLE_TRANSFER = 3
PREFIXES = (100, 200, 300, 400, 500, 600)


def discover(discovery_tasks: list[dict[str, Any]], budget: int = 10) -> tuple[list[dict[str, Any]], list[Any]]:
    fixed = []
    traces = []
    for task in discovery_tasks:
        result = solve_task(task, PROGRAMS, budget=budget)
        result["task_id"] = task["task_id"]
        stable = []
        # Stability only examines demonstration order and fixed program order.
        key = int(__import__("hashlib").sha256(("phase13g-stability:" + task["task_id"]).encode()).hexdigest()[:16], 16)
        rng = random.Random(key + 1307)
        for _ in range(10):
            perm = list(task["train"])
            rng.shuffle(perm)
            perm_task = {**task, "train": perm}
            stable.append(solve_task(perm_task, PROGRAMS, budget=budget)["program"])
        result["trace_stability"] = (sum(p == result["program"] for p in stable) / max(1, len(stable))) if result.get("program") else None
        result["stability_n"] = len(stable)
        result["structural_bucket"] = structural_bucket(task)
        result["symmetry_property"] = symmetry_demo_property(task)
        result["trace_schema_valid"] = True
        trace = trace_for(task, result)
        result["trace_exact_fit"] = bool(result["demo_fit"] and trace.outcome and trace.outcome.success)
        fixed.append(result)
        traces.append(trace)
    return fixed, traces


def _miner() -> TraceMiner:
    return TraceMiner(
        config=MiningConfig(min_frequency=MIN_SUPPORT, min_cross_trace=MIN_SUPPORT,
                            max_fragment_length=4, min_core_length=1, successful_trace_bias=True),
        policy=InvariantPolicy(min_frequency=MIN_SUPPORT, min_consistency=1.0,
                               min_task_families=2, min_generality=0.0,
                               require_transfer_evidence=False, min_transfer_events=0),
    )


def mine_invariants(traces: list[Any]) -> tuple[Any, dict[str, Invariant], list[dict[str, Any]]]:
    valid_traces = [t for t in traces if t.outcome and t.outcome.success]
    result = _miner().mine(valid_traces)
    by_program: dict[str, Invariant] = {}
    rows = []
    for inv in result.candidates:
        apps = [s.removeprefix("apply_") for s in inv.pattern_signature if s.startswith("apply_")]
        program = apps[0] if len(apps) == 1 and apps[0] in PROGRAMS else ""
        rows.append({"program": program or "unmapped_signature", "invariant_id": inv.invariant_id,
                     "signature": " ".join(inv.pattern_signature), "frequency": inv.frequency,
                     "consistency": inv.consistency, "generality": inv.generality,
                     "is": inv.strength, "source_trace_count": len(set(inv.source_trace_ids)),
                     "state": inv.state.value, "confidence": inv.confidence.value,
                     "skill_mapping_status": "mapped_to_program" if program else "not_translatable_to_v1_skill"})
        if not program:
            continue
        old = by_program.get(program)
        if old is None or (inv.strength, inv.frequency) > (old.strength, old.frequency):
            by_program[program] = inv
    rows.sort(key=lambda r: (-r["frequency"], r["program"], r["signature"]))
    return result, by_program, rows


def measure_program_transfer(program: str, transfer_tasks: list[dict[str, Any]]) -> dict[str, Any]:
    applicable = successes = failure_fit = 0
    savings: list[float] = []
    events = []
    for task in transfer_tasks:
        one = solve_task(task, [program], budget=1)
        if not one["demo_fit"]:
            continue
        applicable += 1
        baseline = solve_task(task, PROGRAMS, budget=3)
        saved = max(0, int(baseline["candidate_trials"]) - 1)
        savings.append(float(saved))
        ok = bool(one["task_exact"])
        successes += int(ok)
        failure_fit += int(not ok)
        events.append({"task_id": task["task_id"], "program": program,
                       "structural_bucket": structural_bucket(task), "success": ok,
                       "baseline_trials": baseline["candidate_trials"],
                       "skill_trials": 1, "trials_saved": saved,
                       "failure_type": "" if ok else "demo_fit_test_mismatch"})
    return {"program": program, "applicable_tasks": applicable, "successful_tasks": successes,
            "failed_test_tasks": failure_fit,
            "transfer_score": successes / applicable if applicable else 0.0,
            "mean_positive_trials_saved": mean(savings) or 0.0,
            "abstraction_gain": (mean(savings) or 0.0) / len(PROGRAMS),
            "events": events}


def _skill_category(program: str) -> str:
    fam = PROGRAM_FAMILY[program]
    if fam in {"reflection", "rotation"}:
        return fam
    if fam == "translation":
        return "translation"
    if fam == "recoloring":
        return "general"
    return "general"


def build_skills(invariants: dict[str, Invariant], support: Counter[str], transfer_stats: dict[str, dict[str, Any]]) -> tuple[SkillLibrary, list[dict[str, Any]], dict[str, Invariant]]:
    cfg = SkillConfig()
    library = SkillLibrary()
    rows = []
    promoted_invariants: dict[str, Invariant] = {}
    for program in PROGRAMS:
        inv = invariants.get(program)
        if inv is None or support[program] < MIN_SUPPORT:
            continue
        stats = transfer_stats[program]
        if stats["applicable_tasks"] < MIN_APPLICABLE_TRANSFER:
            rows.append({"program": program, "support": support[program], "status": "rejected_insufficient_transfer_applicability", **{k: stats[k] for k in ("applicable_tasks", "successful_tasks", "transfer_score", "abstraction_gain")}})
            continue
        inv.metadata = dict(inv.metadata or {})
        inv.metadata.update({"expected_transfer": stats["transfer_score"],
                             "abstraction_gain": stats["abstraction_gain"],
                             "reasoning_value": stats["abstraction_gain"],
                             "creation_cost": cfg.default_creation_cost,
                             "mvp_category": _skill_category(program),
                             "execution_policy": f"apply_{program}"})
        # Advance invariant through its real lifecycle using only transfer-split evidence.
        if inv.state is InvariantState.CANDIDATE:
            inv.transition_to(InvariantState.DETECTED)
        if inv.state is InvariantState.DETECTED:
            inv.transition_to(InvariantState.VALIDATED)
        if inv.state is InvariantState.VALIDATED:
            inv.transfer_contribution = stats["transfer_score"]
            inv.record_transfer(stats["successful_tasks"])
            inv.transition_to(InvariantState.TRANSFER_VERIFIED)
        if inv.state is InvariantState.TRANSFER_VERIFIED:
            inv.transition_to(InvariantState.SKILL_CANDIDATE)
        reuse = min(1.0, stats["successful_tasks"] / cfg.reuse_norm)
        candidate: SkillCandidate = from_invariant(inv, config=cfg,
                                                   candidate_id=f"ARC13G-{program}")
        candidate.reuse = reuse
        candidate.expected_reuse = reuse
        candidate.transfer_score = float(stats["transfer_score"])
        candidate.expected_transfer = float(stats["transfer_score"])
        candidate.abstraction_gain = float(stats["abstraction_gain"])
        candidate.creation_cost = cfg.default_creation_cost
        candidate.scv = compute_scv(reuse, candidate.abstraction_gain,
                                    candidate.transfer_score, candidate.creation_cost)
        qualification = qualify_candidate(candidate, invariant=inv, library=library,
                                          config=cfg, ntr=(stats["failed_test_tasks"] / max(1, stats["applicable_tasks"])))
        row = {"program": program, "support": support[program],
               "invariant_id": inv.invariant_id, "is": inv.strength,
               "applicable_tasks": stats["applicable_tasks"],
               "successful_tasks": stats["successful_tasks"],
               "transfer_score": stats["transfer_score"],
               "reuse": reuse, "abstraction_gain": candidate.abstraction_gain,
               "creation_cost": candidate.creation_cost, "scv": candidate.scv,
               "qualified": qualification.qualified,
               "qualification_reasons": qualification.reasons,
               "qualification_tests": qualification.tests,
               "status": "promoted" if qualification.qualified else "rejected_qualification"}
        if qualification.qualified:
            skill = Skill.from_candidate(candidate)
            skill.reuse_count = int(stats["successful_tasks"])
            skill.transfer_history = list(stats["events"])
            skill.metadata = {**skill.metadata, "mvp_category": _skill_category(program),
                              "program": program, "invariant_strength": inv.strength,
                              "trace_mined": True}
            skill.transition_to(SkillState.ACTIVE)
            refresh_skill_utility(skill, cfg)
            library.add(skill)
            promoted_invariants[program] = inv
        rows.append(row)
    return library, rows, promoted_invariants


def _memory_program(task: dict[str, Any], discovery_tasks: list[dict[str, Any]],
                    discovery_results: list[dict[str, Any]]) -> str:
    feat = task_features(task)
    choices = []
    for source, result in zip(discovery_tasks, discovery_results):
        if result.get("program"):
            choices.append((normalized_distance(feat, task_features(source)), source["task_id"], result["program"]))
    return min(choices)[2] if choices else ""


def build_arm_orders(discovery_tasks: list[dict[str, Any]], discovery_results: list[dict[str, Any]],
                     support: Counter[str], skill_library: SkillLibrary) -> dict[str, Any]:
    eligible = [p for p in PROGRAMS if support[p] >= MIN_SUPPORT]
    asft_programs = [s.metadata["program"] for s in skill_library.list_skills()]
    asft_programs.sort(key=lambda p: (-support[p], p))
    return {"eligible_programs": eligible, "ASFT": asft_programs,
            "B1_NO_LEARNING": [], "B2_MEMORY_SKILL_STORE": "nearest_episode",
            "B3_RANDOM_SKILL_CREATION": "task_keyed_random", "B4_COMPRESSION_PROXY": "exact_trace_frequency"}


def _order_for(arm: str, task: dict[str, Any], *, orders: dict[str, Any],
               support: Counter[str], discovery_tasks: list[dict[str, Any]],
               discovery_results: list[dict[str, Any]]) -> list[str]:
    fixed = list(PROGRAMS)
    eligible = list(orders["eligible_programs"])
    if arm == "B1_NO_LEARNING":
        return fixed
    if arm == "ASFT":
        learned = list(orders["ASFT"])
    elif arm == "B2_MEMORY_SKILL_STORE":
        retrieved = _memory_program(task, discovery_tasks, discovery_results)
        learned = [retrieved] if retrieved else []
    elif arm == "B3_RANDOM_SKILL_CREATION":
        key = int(__import__("hashlib").sha256(("phase13g-b3:" + task["task_id"]).encode()).hexdigest()[:16], 16)
        learned = list(eligible)
        random.Random(key).shuffle(learned)
    elif arm == "B4_COMPRESSION_PROXY":
        # Exact full-trace signatures only; no motif generalization.
        learned = sorted(eligible, key=lambda p: (-support[p], p))
    else:
        raise ValueError(f"unknown arm {arm}")
    return list(dict.fromkeys(learned + fixed))


def run_arms(tasks: list[dict[str, Any]], *, split: str,
             discovery_tasks: list[dict[str, Any]], discovery_results: list[dict[str, Any]],
             support: Counter[str], orders: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    arms = ("ASFT", "B1_NO_LEARNING", "B2_MEMORY_SKILL_STORE", "B3_RANDOM_SKILL_CREATION", "B4_COMPRESSION_PROXY")
    for task in tasks:
        for arm in arms:
            order = _order_for(arm, task, orders=orders, support=support,
                               discovery_tasks=discovery_tasks, discovery_results=discovery_results)
            result = solve_task(task, order, budget=3)
            rows.append({"split": split, "task_id": task["task_id"], "arm": arm,
                         "program": result["program"], "family": result["family"],
                         "demo_fit": result["demo_fit"], "task_exact": result["task_exact"],
                         "candidate_trials": result["candidate_trials"],
                         "test_pairs": result["test_pairs"],
                         "structural_bucket": structural_bucket(task),
                         "failure_type": result["failure_type"]})
    return rows


def _library_capabilities(library: SkillLibrary) -> tuple[CapabilityLibrary, list[dict[str, Any]]]:
    cap_cfg = CapabilityConfig()
    cap_lib = CapabilityLibrary()
    proposals = propose_capabilities_from_library(library, config=cap_cfg, require_valid=True)
    rows = []
    for cap in proposals:
        cap_lib.add(cap)
        rows.append({"capability_id": cap.capability_id, "type": cap.capability_type.value,
                     "skills": list(cap.skill_ids), "state": cap.state.value,
                     "utility": cap.utility, "coverage": cap.coverage})
    return cap_lib, rows


def growth_series(discovery_traces: list[Any], discovery_tasks: list[dict[str, Any]],
                  transfer_stats: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows, cap_rows = [], []
    prev_c = prev_ts = prev_capu = prev_coverage = 0.0
    for prefix in PREFIXES:
        tasks = discovery_tasks[:prefix]
        traces = discovery_traces[:prefix]
        _, invs, _ = mine_invariants(traces)
        support: Counter[str] = Counter()
        for task, trace in zip(tasks, traces):
            if trace.outcome and trace.outcome.success:
                for step in trace.steps:
                    if step.operation.startswith("apply_"):
                        support[step.operation.removeprefix("apply_")] += 1
        library, skill_rows, _ = build_skills(invs, support, transfer_stats)
        caps, proposals = _library_capabilities(library)
        cap_rows.extend({"discovery_prefix": prefix, **r} for r in proposals)
        gc = GrowthConfig()
        cap_cfg = CapabilityConfig()
        snap = compute_system_capability_state(caps, library, config=cap_cfg,
                                               growth_config=gc, previous_score=prev_c,
                                               new_capability=max(0, len(caps)), dt=1.0)
        portfolio = compute_capability_portfolio(caps, library, cap_cfg, refresh=True)
        current_c = float(snap.capability_score)
        current_ts = mean([float(s.transfer_score) for s in library.list_skills()]) or 0.0
        current_capu = float(portfolio.mean_capu)
        successful_program_families = {PROGRAM_FAMILY[str(s.metadata.get("program"))]
                                       for s in library.list_skills()
                                       if s.metadata.get("program") in PROGRAM_FAMILY
                                       and any(e.get("success") for e in s.transfer_history)}
        current_coverage = len(successful_program_families) / max(1, len(set(PROGRAM_FAMILY.values())))
        has_cap = len(caps) > 0 and len(library) >= 2
        cgr = float(snap.cgr)
        tg, ug, ccg = current_ts - prev_ts, current_capu - prev_capu, current_coverage - prev_coverage
        ig = compute_ig(cgr, tg=tg, ug=ug, ccg=ccg, compg=0.0, growth_config=gc) if has_cap else None
        rows.append({"discovery_prefix": prefix, "n_successful_traces": len(traces),
                     "n_invariants": len(invs), "n_skills": len(library),
                     "n_capabilities": len(caps), "capability_ids": [c.capability_id for c in caps.list_capabilities()],
                     "ct": current_c if has_cap else None, "cgr": cgr if has_cap else None,
                     "mean_ts": current_ts if len(library) else None,
                     "capu": current_capu if has_cap else None,
                     "capability_coverage": current_coverage if has_cap else None,
                     "ig": ig, "ig_status": "available" if ig is not None else "unavailable_no_validated_capability_group",
                     "tg": tg if has_cap else None, "ug": ug if has_cap else None,
                     "ccg": ccg if has_cap else None,
                     "skill_rows": len(skill_rows)})
        prev_c, prev_ts, prev_capu, prev_coverage = current_c, current_ts, current_capu, current_coverage
    return rows, cap_rows


def _coverage_scan(tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for task in tasks:
        row = solve_task(task, PROGRAMS, budget=len(PROGRAMS))
        row.update({"task_id": task["task_id"], "symmetry_property": symmetry_demo_property(task)})
        rows.append(row)
    return rows


def run_phase() -> dict[str, Any]:
    split_manifest = __import__("json").loads((DATA / "split_manifest.json").read_text())
    refs = {name: [r for r in split_manifest["tasks"] if r["split"] == name]
            for name in ("discovery", "transfer", "holdout")}
    discovery_tasks = load_task_rows(refs["discovery"])
    transfer_tasks = load_task_rows(refs["transfer"])
    # Holdout task JSON (including outputs) is deliberately not loaded before the lock.
    holdout_count = len(refs["holdout"])
    discovery_results, traces = discover(discovery_tasks)
    mining, invariants, invariant_rows = mine_invariants(traces)
    support = Counter(r["program"] for r in discovery_results if r.get("demo_fit"))
    transfer_stats = {p: measure_program_transfer(p, transfer_tasks) for p in PROGRAMS}
    library, skill_rows, promoted_invariants = build_skills(invariants, support, transfer_stats)
    orders = build_arm_orders(discovery_tasks, discovery_results, support, library)

    # Freeze and persist all discovery/transfer-derived routing before opening holdout outcomes.
    lock = {"experiment_id": "PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1",
            "holdout_scored": False, "discovery_task_count": len(discovery_tasks),
            "transfer_task_count": len(transfer_tasks), "holdout_task_count": holdout_count,
            "eligible_programs": orders["eligible_programs"], "asft_programs": orders["ASFT"],
            "support": dict(support), "skills": skill_rows,
            "b2_memory_source_count": sum(bool(r.get("program")) for r in discovery_results),
            "decision_rule": "No config, DSL, split, or routing changes after this lock."}
    (OUT / "pre_holdout_lock.json").write_text(__import__("json").dumps(lock, indent=2, sort_keys=True) + "\n")

    transfer_rows = run_arms(transfer_tasks, split="transfer", discovery_tasks=discovery_tasks,
                             discovery_results=discovery_results, support=support, orders=orders)
    growth_rows, capability_rows = growth_series(traces, discovery_tasks, transfer_stats)
    # Only now are final holdout task JSONs loaded and scored.
    holdout_tasks = load_task_rows(refs["holdout"])
    holdout_rows = run_arms(holdout_tasks, split="holdout", discovery_tasks=discovery_tasks,
                            discovery_results=discovery_results, support=support, orders=orders)
    coverage_results = {"discovery": discovery_results,
                        "transfer": _coverage_scan(transfer_tasks),
                        "holdout": _coverage_scan(holdout_tasks)}
    return {"discovery_tasks": discovery_tasks, "transfer_tasks": transfer_tasks,
            "holdout_tasks": holdout_tasks, "coverage_results": coverage_results,
            "discovery_results": discovery_results,
            "traces": traces, "mining": mining, "invariant_rows": invariant_rows,
            "support": support, "transfer_stats": transfer_stats,
            "skill_rows": skill_rows, "skill_library": library,
            "promoted_invariants": promoted_invariants, "orders": orders,
            "transfer_rows": transfer_rows, "holdout_rows": holdout_rows,
            "growth_rows": growth_rows, "capability_rows": capability_rows,
            "mining_stats": mining.statistics.to_dict(), "candidate_count": len(mining.candidates),
            "rejected_candidates": [{"signature": inv.pattern_signature, "reasons": reasons}
                                    for inv, reasons in mining.rejected]}
