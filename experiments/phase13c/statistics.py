"""Seed-cluster resampling and rank correlations for Phase 13C reports."""
from __future__ import annotations

import random
from statistics import mean
from typing import Any
from .common import _quantile


def _bootstrap_mean_ci(values: list[float], *, seed: int, n_boot: int = 4000) -> tuple[float, float]:
    if not values:
        return (0.0, 0.0)
    rng = random.Random(seed)
    draws = []
    for _ in range(n_boot):
        sample = [rng.choice(values) for _ in values]
        draws.append(mean(sample))
    return _quantile(draws, 0.025), _quantile(draws, 0.975)


def _rank(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and values[order[j]] == values[order[i]]:
            j += 1
        rank = (i + 1 + j) / 2.0
        for index in order[i:j]:
            ranks[index] = rank
        i = j
    return ranks


def _spearman(x: list[float], y: list[float]) -> float:
    if len(x) < 2 or len(x) != len(y):
        return 0.0
    rx, ry = _rank(x), _rank(y)
    mx, my = mean(rx), mean(ry)
    numerator = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    denominator = math.sqrt(
        sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)
    )
    return numerator / denominator if denominator else 0.0


def _correlation_report(rows: list[dict[str, Any]], seeds: list[int]) -> dict[str, Any]:
    metrics = {
        "SCV10": [float(row["SCV10"]) for row in rows],
        "frequency": [float(row["frequency"]) for row in rows],
        "p_reuse": [float(row["p_reuse"]) for row in rows],
        "AG": [float(row["AG"]) for row in rows],
        "TS": [float(row["TS"]) for row in rows],
    }
    net = [float(row["shadow_realized_net_value"]) for row in rows]
    utility = [float(row["shadow_mean_SU_at_end"]) for row in rows]
    reuse_count = [float(row["shadow_reuse_count"]) for row in rows]
    transfer = [float(row["shadow_TS_cross_family"]) for row in rows]
    by_seed = {seed: [i for i, row in enumerate(rows) if row["seed"] == seed] for seed in seeds}

    def report_corr(left: list[float], right: list[float], salt: int) -> dict[str, Any]:
        boot = []
        rng = random.Random(13000 + len(rows) + salt)
        for _ in range(2000):
            sampled_seeds = [rng.choice(seeds) for _ in seeds]
            indices = [i for seed in sampled_seeds for i in by_seed.get(seed, [])]
            boot.append(_spearman([left[i] for i in indices], [right[i] for i in indices]))
        return {
            "spearman": _spearman(left, right),
            "seed_cluster_bootstrap_ci95": [_quantile(boot, 0.025), _quantile(boot, 0.975)] if boot else [0.0, 0.0],
            "candidate_n": len(rows),
            "seed_n": len(seeds),
        }

    predictors = {name: report_corr(values, net, i) for i, (name, values) in enumerate(metrics.items())}
    utility_associations = {
        "SU_vs_future_net_value": report_corr(utility, net, 21),
        "SU_vs_reuse_count": report_corr(utility, reuse_count, 22),
        "SU_vs_cross_family_transfer": report_corr(utility, transfer, 23),
    }
    return {"scv_predictors_of_future_net_value": predictors, "utility_associations": utility_associations}
