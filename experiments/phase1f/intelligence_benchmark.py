"""Phase 1F behavior-only target and IG-validity contract functions.

No task solver, IG implementation, or empirical result generation is included.
"""
from __future__ import annotations
from collections.abc import Mapping, Sequence

BATTERY_TESTS = (
    "A_future_learning_rate", "B_adaptation_speed", "C_novel_environment_success",
    "D_few_shot_acquisition", "E_cross_domain_learning", "F_generalization_retention",
)
INTELLIGENCE_TYPES = {
    "I1_learning_speed": "externally scored improvement per fixed new-example exposure",
    "I2_adaptation": "externally scored recovery after a preregistered rule/distribution shift",
    "I3_transfer": "learning or performance benefit on a disjoint target family/domain",
    "I4_compositional_learning": "acquisition of unseen combinations of known components",
    "I5_generalization": "success on held-out instances/templates beyond demonstrations",
    "I6_knowledge_efficiency": "competence acquired per fixed exposure/resource budget",
}
SIMPLE_BASELINES = (
    "past_performance", "experience_count", "capability_score",
    "memory_strength", "transfer_metrics",
)
RANDOM_BASELINE = "random_chance_baseline"
PRIMARY_PREDICTOR = "IG_t"
KEY_SECONDARY_PREDICTOR = "IGR_t"
PRIMARY_ENDPOINT = "A_future_learning_rate_normalized_auc"
PRIMARY_SOI = 0.02
LEARNING_EXPOSURES = (0, 1, 3, 5)
FORBIDDEN_TARGET_FIELDS = frozenset({
    "IG", "IG_t", "IGR", "IGR_t", "IE", "CGR", "C_t", "capability_score",
    "intelligence_score", "transfer_score", "TS", "CGM_score",
})


def score_task_output(predicted: str, gold: str) -> float:
    """Behavioral correctness from system output and independent evaluator gold."""
    return 1.0 if str(predicted) == str(gold) else 0.0


def learning_curve_auc(scores: Sequence[float], exposures: Sequence[float] = LEARNING_EXPOSURES) -> float:
    """Normalized trapezoidal area under externally scored future learning curve."""
    xs = [float(x) for x in exposures]
    ys = [float(y) for y in scores]
    if len(xs) < 2 or len(xs) != len(ys):
        raise ValueError("scores and exposures must have the same length >= 2")
    if any(not 0.0 <= y <= 1.0 for y in ys):
        raise ValueError("external behavioral scores must be bounded in [0, 1]")
    if any(b <= a for a, b in zip(xs, xs[1:])) or xs[0] < 0 or xs[-1] <= 0:
        raise ValueError("exposures must be nonnegative and strictly increasing")
    area = sum((xs[i+1]-xs[i])*(ys[i+1]+ys[i])/2 for i in range(len(xs)-1))
    return area / (xs[-1]-xs[0])


def behavioral_delta(pre_score: float, post_score: float) -> float:
    """Post-minus-pre external task-behavior change; no internal score input."""
    return float(post_score) - float(pre_score)


def validate_external_outcomes(outcomes: Mapping[str, object]) -> bool:
    """Reject internal intelligence/capability/transfer metrics from target payloads."""
    return not bool(set(outcomes) & FORBIDDEN_TARGET_FIELDS)


def ig_predictive_decision(delta_mae: float, ci_low: float, ci_high: float,
                           soi: float = PRIMARY_SOI, *, slope_ci_low: float = 0.0,
                           slope_ci_high: float = 0.0, available: bool = True) -> str:
    """Classify incremental IG prediction of an external future learning target.

    Positive delta means adding IG reduced held-out target MAE. A win also
    requires the preregistered positive IG-to-learning direction.
    """
    if not available:
        return "unavailable"
    if slope_ci_high < 0.0 or ci_high < -soi:
        return "ig_loses"
    if ci_low > soi and slope_ci_low > 0.0:
        return "ig_wins"
    if ci_low >= -soi and ci_high <= soi:
        return "equivalent_tie"
    return "inconclusive"


def intelligence_claim_decision(confirmatory: Mapping[str, str],
                                replication: Mapping[str, str], *,
                                adequate_power: bool, integrity_pass: bool) -> str:
    """Apply preregistered multi-outcome survival/weakening/retirement rule.

    Survival requires a replicated primary learning win plus a replicated win
    on at least one additional transfer/generalization/adaptation outcome.
    Retirement requires adequately powered tie/loss outcomes on every A-F
    external target in both independent cohorts.
    """
    if not integrity_pass:
        return "unavailable"
    if set(confirmatory) != set(BATTERY_TESTS) or set(replication) != set(BATTERY_TESTS):
        return "unavailable"
    allowed = {"ig_wins", "equivalent_tie", "ig_loses", "inconclusive", "unavailable"}
    all_statuses = list(confirmatory.values()) + list(replication.values())
    if any(v not in allowed for v in all_statuses) or "unavailable" in all_statuses:
        return "unavailable"
    if (confirmatory["A_future_learning_rate"] == "ig_wins"
        and replication["A_future_learning_rate"] == "ig_wins"
        and any(confirmatory[t] == "ig_wins" and replication[t] == "ig_wins"
                for t in ("B_adaptation_speed", "C_novel_environment_success",
                          "E_cross_domain_learning", "F_generalization_retention"))):
        return "claim_survives"
    adverse = {"equivalent_tie", "ig_loses"}
    if (adequate_power
        and all(confirmatory[t] in adverse and replication[t] in adverse for t in BATTERY_TESTS)):
        return "retire_as_intelligence"
    if any(v == "ig_wins" for v in all_statuses):
        return "claim_weakens"
    if any(v == "inconclusive" for v in all_statuses):
        return "inconclusive"
    if all(v in {"equivalent_tie", "ig_loses"} for v in all_statuses):
        return "inconclusive"
    return "claim_weakens"
