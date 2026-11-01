"""EXP-IDT-14: controlled stress test for frequency-confounded invariants.

This is a supplemental exploratory benchmark. It does not modify the original
synthetic-v1 Phase 13B evidence or closure gate.
"""

from __future__ import annotations

import copy
import json
import random
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT, ROOT / "src"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from core.trace import ReasoningStep
from evaluation.invariant_metrics import compute_is
from evaluation.stats import summarize_metrics
from evaluation.transfer_metrics import compute_ts
from experiments._common import write_experiment_record
from pipelines.invariant_pipeline import run_invariant_pipeline
from pipelines.trace_pipeline import run_trace_pipeline
from skills.library import SkillLibrary
from skills.pipeline import create_skills_from_invariants
from solver.executor import GridSolver
from solver.tasks import FAMILIES, make_task, make_task_batch
from transfer.reuse_engine import ReuseEngine

CONFIG_PATH = ROOT / "configs" / "idt_confounded_benchmark.yaml"
CONFONDER = "normalize_grid"
INJECTED_FAMILIES = frozenset({"reflection", "rotation", "counting"})
SEEDS = (10, 11, 12, 13, 14)


def _config() -> dict[str, Any]:
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))


def _discovery_traces(seed: int) -> tuple[list[Any], list[Any]]:
    """Generate the base traces, then insert the predeclared no-op marker."""
    base = run_trace_pipeline(
        FAMILIES, per_family=12, seed=seed, difficulty=0.2, persist=False
    )
    confounded = []
    for original in base.traces:
        trace = copy.deepcopy(original)
        family = str(trace.metadata.get("task_family", ""))
        if family in INJECTED_FAMILIES:
            trace.steps.insert(
                1,
                ReasoningStep(
                    step_id=f"{trace.trace_id}-exp14-noop",
                    operation=CONFONDER,
                    inputs=[],
                    outputs=["no-op; benchmark confound only"],
                    cost=0.0,
                ),
            )
            trace.metadata = {
                **trace.metadata,
                "exp14_role": "frequent_nontransfer_noop",
            }
        confounded.append(trace)
    return list(base.traces), confounded


def _tasks(task_seed: int) -> list[Any]:
    tasks = make_task_batch(
        FAMILIES,
        per_family=3,
        seed=task_seed,
        difficulty=0.2,
    )
    tasks.extend(
        [
            make_task(
                "counting", seed=task_seed + 100, variant=1, difficulty=0.2
            ),
            make_task(
                "grouping", seed=task_seed + 101, variant=1, difficulty=0.2
            ),
        ]
    )
    return tasks


def _semantic_key(invariant: Any) -> str:
    operations = [str(op) for op in invariant.pattern_signature]
    for operation in operations:
        if operation in {"find_symmetry", "apply_reflection"}:
            return "reflection"
        if operation in {"find_rotation", "apply_rotation"}:
            return "rotation"
    return " ".join(operations)


def _unique_order(items: list[Any]) -> list[Any]:
    ordered = []
    seen: set[str] = set()
    for item in items:
        key = _semantic_key(item)
        if key in seen:
            continue
        seen.add(key)
        ordered.append(item)
    return ordered


def _candidate_transfer(
    invariant_id: str,
    skill_by_invariant: dict[str, Any],
    tasks: list[Any],
) -> dict[str, Any]:
    """Probe measured reuse for one candidate; non-executable candidates score 0."""
    skill = skill_by_invariant.get(invariant_id)
    if skill is None:
        return {
            "invariant_id": invariant_id,
            "applied_attempts": 0,
            "target_families": [],
            "TS": 0.0,
            "TU": 0.0,
            "task_results": [],
        }

    library = SkillLibrary()
    library.add(type(skill).from_dict(skill.to_dict()))
    engine = ReuseEngine(library, solver=GridSolver())
    results = engine.apply_batch(tasks)
    rows = [row for row in results if row.applied]
    if not rows:
        return {
            "invariant_id": invariant_id,
            "applied_attempts": 0,
            "target_families": [],
            "TS": 0.0,
            "TU": 0.0,
            "task_results": [],
        }

    performance_before = sum(
        1.0 / max(row.baseline_cost, 1e-9) for row in rows
    ) / len(rows)
    performance_after = sum(
        1.0 / max(row.reused_cost, 1e-9)
        for row in rows
        if row.success
    ) / len(rows)
    ts = compute_ts(performance_before, performance_after)
    attempts = len(rows)
    credited = sum(bool(row.transfer_credit) for row in rows)
    success_rate = credited / max(1, attempts)
    mean_reduction = sum(row.benefit for row in rows) / max(1, attempts)
    target_families = sorted({row.task_family for row in rows})
    coverage = len(target_families) / len(FAMILIES)
    tu = success_rate * coverage * mean_reduction

    return {
        "invariant_id": invariant_id,
        "applied_attempts": attempts,
        "credited_reuses": credited,
        "target_families": target_families,
        "mean_baseline_cost": sum(row.baseline_cost for row in rows) / attempts,
        "mean_reused_cost": sum(row.reused_cost for row in rows) / attempts,
        "mean_reasoning_reduction": mean_reduction,
        "TS": ts,
        "TU": tu,
        "task_results": [row.to_dict() for row in rows],
    }


def _score_at_k(order: list[Any], tu_by_id: dict[str, float], k: int) -> float:
    top = order[:k]
    return sum(tu_by_id.get(item.invariant_id, 0.0) for item in top) / max(1, k)


def run_one(seed: int) -> dict[str, Any]:
    """Run EXP-IDT-14 for one run seed."""
    base_traces, traces = _discovery_traces(seed)
    invariant_run = run_invariant_pipeline(traces, bootstrap=True)
    candidate_pool = [
        row.invariant
        for row in (
            invariant_run.validation.ranked if invariant_run.validation else []
        )
    ]
    skill_result = create_skills_from_invariants(
        invariant_run.promotable,
        allow_prior_evidence=True,
    )
    skill_by_invariant = {
        skill.source_invariant_id: skill
        for skill in skill_result.promoted
        if skill.source_invariant_id
    }

    calibration_tasks = _tasks(1000 + seed)
    evaluation_tasks = _tasks(2000 + seed)
    calibration_rows = {
        invariant.invariant_id: _candidate_transfer(
            invariant.invariant_id, skill_by_invariant, calibration_tasks
        )
        for invariant in candidate_pool
    }
    evaluation_rows = {
        invariant.invariant_id: _candidate_transfer(
            invariant.invariant_id, skill_by_invariant, evaluation_tasks
        )
        for invariant in candidate_pool
    }
    calibration_tu = {
        invariant_id: row["TU"] for invariant_id, row in calibration_rows.items()
    }
    evaluation_tu = {
        invariant_id: row["TU"] for invariant_id, row in evaluation_rows.items()
    }

    frequency_order = _unique_order(
        sorted(candidate_pool, key=lambda inv: (-inv.frequency, inv.invariant_id))
    )
    no_transfer_order = _unique_order(
        sorted(candidate_pool, key=lambda inv: (-compute_is(inv), inv.invariant_id))
    )
    transfer_order = _unique_order(
        sorted(
            candidate_pool,
            key=lambda inv: (
                -calibration_tu.get(inv.invariant_id, 0.0),
                0
                if any(str(op).startswith("apply_") for op in inv.pattern_signature)
                else 1,
                inv.invariant_id,
            ),
        )
    )
    rng = random.Random(seed + 7919)
    random_orders = []
    for _ in range(16):
        order = list(candidate_pool)
        rng.shuffle(order)
        random_orders.append(_unique_order(order))
    random_score = sum(
        _score_at_k(order, evaluation_tu, 1) for order in random_orders
    ) / len(random_orders)

    metrics = {
        "ASFT": _score_at_k(transfer_order, evaluation_tu, 1),
        "frequency_only": _score_at_k(frequency_order, evaluation_tu, 1),
        "no_transfer": _score_at_k(no_transfer_order, evaluation_tu, 1),
        "random_pattern": random_score,
    }
    metrics.update(
        {
            "ASFT_advantage": metrics["ASFT"] - metrics["frequency_only"],
            "ASFT_minus_no_transfer": metrics["ASFT"] - metrics["no_transfer"],
            "ASFT_minus_random": metrics["ASFT"] - metrics["random_pattern"],
        }
    )
    max_k = min(
        len(transfer_order), len(frequency_order), len(no_transfer_order)
    )
    ranking_diagnostics = {
        "primary_top_k": 1,
        "transfer_order": [
            {"semantic_key": _semantic_key(inv), "invariant_id": inv.invariant_id}
            for inv in transfer_order
        ],
        "frequency_order": [
            {"semantic_key": _semantic_key(inv), "invariant_id": inv.invariant_id}
            for inv in frequency_order
        ],
        "no_transfer_order": [
            {"semantic_key": _semantic_key(inv), "invariant_id": inv.invariant_id}
            for inv in no_transfer_order
        ],
        "mean_held_out_TU_at_k": {
            str(k): {
                "ASFT": _score_at_k(transfer_order, evaluation_tu, k),
                "frequency_only": _score_at_k(frequency_order, evaluation_tu, k),
                "no_transfer": _score_at_k(no_transfer_order, evaluation_tu, k),
            }
            for k in range(1, max_k + 1)
        },
        "random_permutations": 16,
    }
    candidate_rows = []
    for inv in sorted(candidate_pool, key=lambda item: (-compute_is(item), item.invariant_id)):
        candidate_rows.append(
            {
                "invariant_id": inv.invariant_id,
                "signature": list(inv.pattern_signature),
                "semantic_key": _semantic_key(inv),
                "frequency": inv.frequency,
                "consistency": inv.consistency,
                "generality": inv.generality,
                "IS": compute_is(inv),
                "task_families": list(inv.task_families),
                "has_skill": inv.invariant_id in skill_by_invariant,
                "calibration": calibration_rows[inv.invariant_id],
                "evaluation": evaluation_rows[inv.invariant_id],
            }
        )

    injected = [
        trace
        for trace in traces
        if trace.metadata.get("exp14_role") == "frequent_nontransfer_noop"
    ]
    payload = {
        "experiment_id": "EXP-IDT-14",
        "claim": "IDT",
        "seed": seed,
        "dataset_version": "synthetic-confounded-v1",
        "configuration": {
            "base_dataset": "synthetic-v1",
            "per_family": 12,
            "injected_operation": CONFONDER,
            "injected_families": sorted(INJECTED_FAMILIES),
            "injected_trace_count": len(injected),
            "base_trace_count": len(base_traces),
            "calibration_task_seed": 1000 + seed,
            "evaluation_task_seed": 2000 + seed,
            "primary_top_k": 1,
            "secondary_top_k": [2],
        },
        "metrics": metrics,
        "candidate_count": len(candidate_pool),
        "skill_count": len(skill_by_invariant),
        "candidate_rows": candidate_rows,
        "ranking_diagnostics": ranking_diagnostics,
        "failure_cases": [],
    }
    payload["stress_test_success"] = all(
        metrics["ASFT"] > metrics[name]
        for name in ("frequency_only", "no_transfer", "random_pattern")
    )
    return payload


def run_exp14(*, seeds: tuple[int, ...] = SEEDS, write: bool = False) -> dict[str, Any]:
    """Run the five-seed supplemental stress test and optionally save reports."""
    if len(seeds) < 5 or len(set(seeds)) < 5:
        raise ValueError("EXP-IDT-14 requires at least five unique run seeds")
    raw = [run_one(seed) for seed in seeds]
    metric_names = (
        "ASFT",
        "frequency_only",
        "no_transfer",
        "random_pattern",
        "ASFT_advantage",
        "ASFT_minus_no_transfer",
        "ASFT_minus_random",
    )
    stats = summarize_metrics(
        {
            name: [float(item["metrics"][name]) for item in raw]
            for name in metric_names
        }
    )
    # Every run has the same number of semantic candidates; report all shared k.
    max_common_k = min(
        max(
            int(k)
            for k in item["ranking_diagnostics"]["mean_held_out_TU_at_k"]
        )
        for item in raw
    )
    top_k_statistics = {}
    for k in range(1, max_common_k + 1):
        top_k_statistics[str(k)] = {
            method: summarize_metrics(
                {
                    method: [
                        float(
                            item["ranking_diagnostics"]["mean_held_out_TU_at_k"][str(k)][method]
                        )
                        for item in raw
                    ]
                }
            )[method]
            for method in ("ASFT", "frequency_only", "no_transfer")
        }
    result = {
        "experiment_id": "EXP-IDT-14",
        "claim": "IDT",
        "dataset_version": "synthetic-confounded-v1",
        "configuration": _config(),
        "seeds": list(seeds),
        "metrics": {name: item["mean"] for name, item in stats.items()},
        "statistics": stats,
        "top_k_statistics": top_k_statistics,
        "raw_results": raw,
        "stress_test_success": all(item["stress_test_success"] for item in raw),
        "failure_cases": [
            f"seed {item['seed']}: ASFT did not strictly beat all controls"
            for item in raw
            if not item["stress_test_success"]
        ],
        "interpretation": (
            "Supplemental controlled stress test only; it does not alter the "
            "original synthetic-v1 Phase 13B gate or close Phase 13B."
        ),
    }
    if write:
        record_artifacts = write_experiment_record(
            "EXP-IDT-14", result, root=ROOT
        )
        result["artifacts"] = record_artifacts
        output_dir = ROOT / "reports" / "experiments" / "EXP-IDT-14"
        (output_dir / "candidate_rankings.json").write_text(
            json.dumps(
                [
                    {
                        "seed": item["seed"],
                        "candidate_rows": item["candidate_rows"],
                        "ranking_diagnostics": item["ranking_diagnostics"],
                    }
                    for item in raw
                ],
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        markdown = [
            "# EXP-IDT-14 — Confounded-Frequency Stress Test",
            "",
            f"- Exploratory; original Phase 13B gate unchanged.",
            f"- Stress test pass: `{result['stress_test_success']}`",
            f"- Seeds: `{list(seeds)}`",
            "",
            "## Top-1 held-out transfer utility",
            "",
            "| Method | Mean | SD | 95% normal CI |",
            "|---|---:|---:|---:|",
        ]
        for name, label in (
            ("ASFT", "Transfer-aware"),
            ("frequency_only", "Frequency-only"),
            ("no_transfer", "No-transfer / IS-only"),
            ("random_pattern", "Random"),
        ):
            item = stats[name]
            markdown.append(
                f"| {label} | {item['mean']:.6f} | {item['std']:.6f} | "
                f"{item['ci_low']:.6f}–{item['ci_high']:.6f} |"
            )
        markdown.extend(
            [
                "",
                "## Paired ranking differences",
                "",
                f"- ASFT − frequency: `{stats['ASFT_advantage']['mean']:.6f}`",
                f"- ASFT − no-transfer: `{stats['ASFT_minus_no_transfer']['mean']:.6f}`",
                f"- ASFT − random: `{stats['ASFT_minus_random']['mean']:.6f}`",
                "",
                "## Mean held-out TU by k",
                "",
                "| k | ASFT | Frequency-only | No-transfer |",
                "|---:|---:|---:|---:|",
            ]
        )
        for k, methods in top_k_statistics.items():
            markdown.append(
                f"| {k} | {methods['ASFT']['mean']:.6f} | "
                f"{methods['frequency_only']['mean']:.6f} | "
                f"{methods['no_transfer']['mean']:.6f} |"
            )
        markdown.extend(
            [
                "",
                "This is a designed no-op-confound stress test, not evidence that "
                "the original Phase 13B gate passed or that the result generalizes beyond this simulator.",
                "",
            ]
        )
        (output_dir / "summary.md").write_text("\n".join(markdown), encoding="utf-8")
    return result


if __name__ == "__main__":
    output = run_exp14(write=True)
    print(
        json.dumps(
            {
                "stress_test_success": output["stress_test_success"],
                "seeds": output["seeds"],
                "metrics": output["metrics"],
                "failure_cases": output["failure_cases"],
                "original_phase13b_gate_changed": False,
            },
            indent=2,
        )
    )
    raise SystemExit(0 if output["stress_test_success"] else 1)
