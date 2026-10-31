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
