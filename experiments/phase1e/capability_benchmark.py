"""Phase 1E independent behavioral-target and decision-rule contracts.

This module defines outcome-side functions only. It does not implement a CGM
score or run task solvers; production predictors are joined after outcomes lock.
"""
from __future__ import annotations
from collections.abc import Mapping, Sequence

BATTERY_TESTS = (
    "A_novel_task_success", "B_transfer_success", "C_task_breadth",
    "D_retention", "E_composition", "F_adaptation",
)
FORBIDDEN_OUTCOME_FIELDS = frozenset({"CGR", "C_t", "IG", "IGR", "IE", "capability_score"})
CAPABILITY_TYPES = {
    "C1_single_skill": "persistent performance across novel instances/surface variants for one skill",
    "C2_multi_skill": "joint task performance requiring at least two skills",
    "C3_transfer": "positive performance on a disjoint task family",
    "C4_compositional": "success on unseen compositions of known components",
    "C5_adaptive": "behavioral improvement after a fixed small demonstration budget",
    "C6_cross_domain": "successful transfer in at least two preregistered domains",
}
SIMPLE_BASELINES = ("past_performance", "experience_count", "memory_strength", "frequency_statistics", "recency_since_related_success")
PRIMARY_PREDICTOR = "CGR_t"


def score_task_output(predicted: str, gold: str) -> float:
    """External correctness score; inputs are task output and evaluator gold only."""
    return 1.0 if str(predicted) == str(gold) else 0.0


def external_battery_score(outcomes: Mapping[str, Sequence[float]]) -> float:
    """Equal-weight average of per-test means of external family-level scores."""
    if set(outcomes) != set(BATTERY_TESTS):
        raise ValueError("outcomes must contain exactly the six preregistered battery tests")
    family_means = []
    for name in BATTERY_TESTS:
        values = list(outcomes[name])
        if not values or any(not 0.0 <= float(v) <= 1.0 for v in values):
            raise ValueError("each battery test needs bounded non-empty family-level external scores")
        family_means.append(sum(map(float, values)) / len(values))
    return sum(family_means) / len(family_means)


def behavioral_growth(pre_score: float, future_score: float) -> float:
    """External behavioral change; no internal capability metric is accepted."""
    return float(future_score) - float(pre_score)


def behavioral_capability_pass(task_count: int, observed_accuracy: float,
                               lower_confidence_bound: float, baseline_accuracy: float,
                               retention_ratio: float, net_utility_gain: float,
                               *, min_tasks: int = 20, min_accuracy: float = 0.70,
                               min_gain: float = 0.05, min_retention: float = 0.90) -> bool:
    """Behavior-only capability gate; no CGR/C_t/IG input is accepted."""
    return (task_count >= min_tasks and observed_accuracy >= min_accuracy
            and lower_confidence_bound >= baseline_accuracy + min_gain
            and retention_ratio >= min_retention and net_utility_gain > 0.0)


def capability_metric_decision(delta_mae: float, ci_low: float, ci_high: float,
                               soi: float = 0.02, *, slope_ci_low: float = 0.0,
                               slope_ci_high: float = 0.0, available: bool = True) -> str:
    """Classify CGR's incremental prediction and expected positive direction.

    Positive delta means adding CGR reduced future behavioral-score MAE. A
    meaningful benefit must also have a positive CGR slope.
    """
    if not available:
        return "unavailable"
    if slope_ci_high < 0.0 or ci_high < -soi:
        return "metric_loses"
    if ci_low > soi and slope_ci_low > 0.0:
        return "metric_wins"
    if ci_low >= -soi and ci_high <= soi:
        return "equivalent_tie"
    return "inconclusive"


def validate_external_outcomes(outcomes: Mapping[str, object]) -> bool:
    """Reject any outcome payload containing CGM/internal predictor fields."""
    return not bool(set(outcomes) & FORBIDDEN_OUTCOME_FIELDS)
