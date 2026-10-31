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
        "TS", "performance_after - performance_before",
        "transfer score (normalized reasoning-efficiency gain)",
        "(-inf, inf)", "<= 0",
    ),
    "TU": MetricDefinition(
        "TU", "transfer_success * coverage * reasoning_reduction",
        "transfer utility",
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
    "SPARSE_STRONG_FRACTION": MetricDefinition(
        "SPARSE_STRONG_FRACTION", "strong sparse invariants / sparse invariants",
        "sparse over-promotion rate", "[0, 1]", "> clean rate",
    ),
    "CLEAN_STRONG_FRACTION": MetricDefinition(
        "CLEAN_STRONG_FRACTION", "strong full-data invariants / full invariants",
        "reference strong-confidence rate", "[0, 1]", "< 0",
    ),
    "SPARSE_PRECISION": MetricDefinition(
        "SPARSE_PRECISION", "valid sparse invariants / sparse invariants",
        "sparse-data precision", "[0, 1]", "< 0.70",
    ),
    "SPARSE_RECALL": MetricDefinition(
        "SPARSE_RECALL", "discovered sparse expected / expected invariants",
        "sparse-data recall", "[0, 1]", "< 0",
    ),
    "ASFT": MetricDefinition(
        "ASFT", "mean TU of top-k transfer-aware invariants",
        "ASFT transfer-aware ranking utility", "(-inf, inf)", "<= baseline",
    ),
    "FREQUENCY_ONLY": MetricDefinition(
        "FREQUENCY_ONLY", "mean TU of top-k frequency-ranked invariants",
        "frequency-only ranking utility", "(-inf, inf)", ">= ASFT",
    ),
    "NO_TRANSFER": MetricDefinition(
        "NO_TRANSFER", "mean TU of top-k IS-ranked invariants",
        "transfer-blind intrinsic-strength ranking utility",
        "(-inf, inf)", ">= ASFT",
    ),
    "RANDOM_PATTERN": MetricDefinition(
        "RANDOM_PATTERN", "mean TU of top-k random patterns",
        "random-pattern ranking utility", "(-inf, inf)", ">= ASFT",
    ),
    "ASFT_ADVANTAGE": MetricDefinition(
        "ASFT_ADVANTAGE", "ASFT TU - frequency-only TU",
        "transfer-aware ranking advantage", "(-inf, inf)", "<= 0",
    ),
    "ASFT_VALID_TOP_RATE": MetricDefinition(
        "ASFT_VALID_TOP_RATE", "valid ASFT top-k / k",
        "validity of ASFT top-k", "[0, 1]", "< 0.70",
    ),
    "FREQUENCY_VALID_TOP_RATE": MetricDefinition(
        "FREQUENCY_VALID_TOP_RATE", "valid frequency top-k / k",
        "validity of frequency top-k", "[0, 1]", "< 0.70",
    ),
    "CROSS_FAMILY_REUSE": MetricDefinition(
        "CROSS_FAMILY_REUSE", "credited reuse across source and target families",
        "cross-family transfer count", "[0, inf)", "== 0",
    ),
    "CROSS_FAMILY_REUSE_RATE": MetricDefinition(
        "CROSS_FAMILY_REUSE_RATE",
        "cross-family credited reuse / credited reuse",
        "normalized cross-family transfer rate", "[0, 1]", "== 0",
    ),
    "CORRELATION_N": MetricDefinition(
        "CORRELATION_N", "number of invariant-level transfer pairs",
        "correlation sample size", "[0, inf)", "< 4",
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
    return {str(name): metric_definition(name) for name in selected}
