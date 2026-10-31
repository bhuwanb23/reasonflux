"""Canonical metric governance for Phase 13 experiments."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class MetricDefinition:
    name: str
    formula: str
    interpretation: str
    valid_range: str
    failure_condition: str


METRICS: dict[str, MetricDefinition] = {
    "IS": MetricDefinition(
        "IS", "frequency * consistency * generality", "invariant strength",
        "[0, inf)", "<= 0",
    ),
    "SCV": MetricDefinition(
        "SCV", "expected benefit - creation cost", "skill creation value",
        "(-inf, inf)", "<= 0",
    ),
    "SU": MetricDefinition(
        "SU", "skill utility breakdown", "skill usefulness after costs",
        "(-inf, inf)", "<= 0",
    ),
    "TS": MetricDefinition(
        "TS", "performance_after - performance_before", "transfer score",
        "(-inf, inf)", "<= 0",
    ),
    "TU": MetricDefinition(
        "TU", "transfer benefit per reuse", "transfer utility",
        "(-inf, inf)", "<= 0",
    ),
    "NTR": MetricDefinition(
        "NTR", "reasoning reduction / baseline cost",
        "normalized transfer reduction", "(-inf, inf)", "<= 0",
    ),
    "CGR": MetricDefinition(
        "CGR", "(C_t - C_(t-1)) / delta_t", "capability growth rate",
        "(-inf, inf)", "<= 0",
    ),
    "IG": MetricDefinition(
        "IG", "weighted intelligence growth components", "intelligence growth",
        "(-inf, inf)", "<= 0",
    ),
    "IGR": MetricDefinition(
        "IGR", "(IG_t - IG_(t-1)) / delta_t", "intelligence growth rate",
        "(-inf, inf)", "<= 0",
    ),
    "COVERAGE": MetricDefinition(
        "coverage", "covered task-family proportion", "capability coverage",
        "[0, 1]", "<= 0",
    ),
    "IP": MetricDefinition(
        "IP", "valid_invariants / detected_invariants",
        "invariant precision", "[0, 1]", "< 0.70",
    ),
    "IR": MetricDefinition(
        "IR", "discovered_expected / expected_invariants",
        "invariant recall", "[0, 1]", "< 0.75",
    ),
    "VST": MetricDefinition(
        "VST", "successful_variations / total_variations",
        "variation survival", "[0, 1]", "< 0.60",
    ),
    "PEARSON": MetricDefinition(
        "PEARSON", "corr(IS, TS)", "linear IS-transfer correlation",
        "[-1, 1]", "<= 0",
    ),
    "SPEARMAN": MetricDefinition(
        "SPEARMAN", "corr(rank(IS), rank(TS))",
        "rank IS-transfer correlation", "[-1, 1]", "<= 0",
    ),
    "RANK_STABILITY": MetricDefinition(
        "RANK_STABILITY", "overlap(top_k_clean, top_k_perturbed) / k",
        "invariant ranking stability", "[0, 1]", "< 0.60",
    ),
    "DISCOVERY": MetricDefinition(
        "DISCOVERY", "expected_invariant_found", "discovery success",
        "[0, 1]", "< 1",
    ),
    "RANK": MetricDefinition(
        "RANK", "rank of expected invariant", "discovery rank",
        "[0, inf)", "== 0",
    ),
    "CONFIDENCE": MetricDefinition(
        "CONFIDENCE", "mean evidence confidence", "invariant confidence",
        "[0, 1]", "< 0.70",
    ),
    "SPARSE_MEAN_IS": MetricDefinition(
        "SPARSE_MEAN_IS", "mean IS under sparse traces",
        "sparse-data invariant strength", "[0, inf)", "< 0",
    ),
    "CLEAN_MEAN_IS": MetricDefinition(
        "CLEAN_MEAN_IS", "mean IS under full traces",
        "reference invariant strength", "[0, inf)", "< 0",
    ),
    "SPARSE_CANDIDATES": MetricDefinition(
        "SPARSE_CANDIDATES", "candidate count under sparse traces",
        "sparse candidate count", "[0, inf)", "< 0",
    ),
    "CLEAN_CANDIDATES": MetricDefinition(
        "CLEAN_CANDIDATES", "candidate count under full traces",
        "reference candidate count", "[0, inf)", "< 0",
    ),
    "ASFT": MetricDefinition(
        "ASFT", "valid top-k invariants / k", "ASFT ranking quality",
        "[0, 1]", "< 0.70",
    ),
    "FREQUENCY_ONLY": MetricDefinition(
        "FREQUENCY_ONLY", "valid top-k frequency-ranked invariants / k",
        "frequency-only ranking quality", "[0, 1]", "< 0.70",
    ),
    "RANDOM_PATTERN": MetricDefinition(
        "RANDOM_PATTERN", "valid top-k random patterns / k",
        "random-pattern quality", "[0, 1]", "< 0.70",
    ),
}


def metric_definition(name: str) -> dict[str, str]:
    """Return a JSON-friendly definition for a governed metric."""
    try:
        key = str(name).upper()
        return asdict(METRICS[key])
    except KeyError as exc:
        raise KeyError(f"Unknown governed metric: {name}") from exc


def metric_definitions(names: list[str] | None = None) -> dict[str, dict[str, str]]:
    """Return definitions for selected metrics, or all governed metrics."""
    selected = list(METRICS) if names is None else names
    return {name.upper(): metric_definition(name) for name in selected}
