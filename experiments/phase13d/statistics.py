"""Seed-cluster statistics and frozen Phase-13D metric formulas."""
from __future__ import annotations
import math
import random
from statistics import mean, stdev
from typing import Any
from .common import STEP_PENALTY
from transfer.metrics import compute_its, compute_tu
from evaluation.transfer_metrics import compute_ts


def performance(correct: bool, steps: float) -> float:
    return float(bool(correct)) - STEP_PENALTY * float(steps)


def summarize(values: list[float], *, n_boot: int = 5000, seed: int = 13004) -> dict[str, Any]:
    if not values:
        return {"n": 0, "mean": None, "sd": None, "ci95": [None, None]}
    mu = mean(values)
    sd = stdev(values) if len(values) > 1 else 0.0
    rng = random.Random(seed)
    boots = [mean(rng.choices(values, k=len(values))) for _ in range(n_boot)]
    boots.sort()
    lo = boots[int(0.025 * (n_boot - 1))]
    hi = boots[int(0.975 * (n_boot - 1))]
    return {"n": len(values), "mean": mu, "sd": sd, "ci95": [lo, hi]}


def metric_bundle(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {"n": 0, "status": "unavailable"}
    ts_values = [compute_ts(float(r["P_before"]), float(r["P_after"])) for r in rows]
    baseline_steps = sum(float(r["baseline_steps"]) for r in rows)
    transfer_steps = sum(float(r["transfer_steps"]) for r in rows)
    success = sum(bool(r["correct_after"]) for r in rows) / len(rows)
    attempted = [r for r in rows if r.get("assigned_application")]
    harmful = [r for r in attempted if float(r["P_after"]) < float(r["P_before"])]
    failed = [r for r in attempted if not r.get("correct_after")]
    attempted_benefits = [max(0.0, float(r["P_after"]) - float(r["P_before"])) for r in attempted]
    fractional = [
        max(0.0, min(1.0, (float(r["baseline_steps"]) - float(r["transfer_steps"])) / float(r["baseline_steps"])))
        for r in rows if bool(r["correct_after"]) and float(r["baseline_steps"]) > 0
    ]
    coverage = len({r["taxonomy"] for r in rows if r.get("reused")}) / max(1, len({r["taxonomy"] for r in rows}))
    reduction = mean(fractional) if fractional else 0.0
    return {
        "n": len(rows),
        "status": "evaluated",
        "TS": summarize(ts_values),
        "exact_accuracy": mean(float(r["correct_after"]) for r in rows),
        "baseline_accuracy": mean(float(r["correct_before"]) for r in rows),
        "RCR_steps": baseline_steps - transfer_steps,
        "RCR_normalized": (baseline_steps - transfer_steps) / baseline_steps if baseline_steps else None,
        "success_gated_fractional_RCR": reduction,
        "TU": compute_tu(success, reduction, coverage),
        "ITS": compute_its(len(attempted), attempted_benefits),
        "reuse_count": sum(bool(r.get("reused")) for r in rows),
        "reuse_rate": sum(bool(r.get("reused")) for r in rows) / len(rows),
        "transfer_success_count": sum(bool(r.get("assigned_application")) and bool(r.get("correct_after"))
                                        and float(r["P_after"]) > float(r["P_before"]) for r in rows),
        "transfer_success_rate": (sum(bool(r.get("assigned_application")) and bool(r.get("correct_after"))
                                       and float(r["P_after"]) > float(r["P_before"]) for r in rows) / len(attempted)) if attempted else None,
        "NTR_accuracy": len(failed) / len(attempted) if attempted else None,
        "NTR_harm": len(harmful) / len(attempted) if attempted else None,
        "attempts": len(attempted),
        "no_match": sum(not bool(r.get("reused")) for r in rows),
        "operations_count": sum(len(r.get("ops", [])) for r in rows),
        "retrieval_candidates_evaluated": sum(int(r.get("retrieval_candidates_evaluated", 0)) for r in rows),
        "solver_search_candidates": None,
        "per_task_TS": ts_values,
    }


def _correlation(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) != len(ys) or len(xs) < 3:
        return None
    mx, my = mean(xs), mean(ys)
    dx, dy = [x - mx for x in xs], [y - my for y in ys]
    vx, vy = sum(x*x for x in dx), sum(y*y for y in dy)
    if vx == 0 or vy == 0:
        return None
    return sum(a*b for a, b in zip(dx, dy)) / math.sqrt(vx*vy)


def clustered_pearson(points: list[dict[str, Any]], x_key: str, y_key: str,
                      *, cluster_key: str = "run_seed", n_boot: int = 2000,
                      seed: int = 13141) -> dict[str, Any]:
    groups: dict[Any, list[dict[str, Any]]] = {}
    for point in points:
        groups.setdefault(point[cluster_key], []).append(point)
    clusters = sorted(groups, key=str)
    xs = [float(p[x_key]) for p in points]
    ys = [float(p[y_key]) for p in points]
    estimate = _correlation(xs, ys)
    if estimate is None:
        return {"r": None, "n": len(points), "n_clusters": len(clusters),
                "ci95": [None, None], "status": "insufficient_or_zero_variance"}
    rng = random.Random(seed)
    boot = []
    for _ in range(n_boot):
        sample = [rng.choice(clusters) for _ in clusters]
        sampled = [p for cluster in sample for p in groups[cluster]]
        value = _correlation([float(p[x_key]) for p in sampled],
                             [float(p[y_key]) for p in sampled])
        if value is not None:
            boot.append(value)
    boot.sort()
    if len(boot) < max(100, n_boot // 10):
        ci = [None, None]
    else:
        ci = [boot[int(0.025 * (len(boot) - 1))], boot[int(0.975 * (len(boot) - 1))]]
    return {"r": estimate, "n": len(points), "n_clusters": len(clusters),
            "ci95": ci, "status": "cluster_bootstrap_descriptive"}
