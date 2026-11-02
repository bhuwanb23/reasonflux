"""Phase 1G stage-separation and protocol-integrity contract functions.

This module does not implement ARC program search or generate task outcomes.
"""
from __future__ import annotations
from collections.abc import Mapping, Sequence

PIPELINE_STAGES = (
    "representation_coverage", "trace_generation", "invariant_discovery",
    "skill_formation", "transfer", "capability", "accuracy",
)
FORBIDDEN_INTERNAL_FIELDS = frozenset({
    "IG", "IGR", "IE", "CGR", "C_t", "CGM_score", "capability_score",
    "internal_transfer_score", "TS", "invariant_strength_internal",
})
VALID_STAGE_STATES = frozenset({"activated", "not_activated", "inconclusive", "unavailable"})


def score_task_output(predicted: object, gold: object) -> bool:
    """Exact behavioral task score from prediction and independent evaluator gold."""
    return predicted == gold


def rate_observation(successes: int, opportunities: int) -> dict[str, object]:
    """Return a stage-specific rate while preserving zero vs unavailable."""
    s, n = int(successes), int(opportunities)
    if s < 0 or n < 0 or s > n:
        raise ValueError("counts must satisfy 0 <= successes <= opportunities")
    if n == 0:
        return {"status": "unavailable", "rate": None, "successes": s, "opportunities": n}
    return {"status": "observed", "rate": s / n, "successes": s, "opportunities": n}


def coverage_rate(covered_tasks: int, total_tasks: int) -> dict[str, object]:
    """Operational demo-fit/representation coverage; not task accuracy."""
    return rate_observation(covered_tasks, total_tasks)


def accuracy_rate(exact_correct_tasks: int, scored_tasks: int) -> dict[str, object]:
    """Exact task accuracy from independent evaluator scoring; not coverage."""
    return rate_observation(exact_correct_tasks, scored_tasks)


def partial_pixel_accuracy(correct_pixels: int, scored_pixels: int) -> dict[str, object]:
    """Pixel-level partial accuracy with its own pixel denominator."""
    return rate_observation(correct_pixels, scored_pixels)


def family_accuracy(counts: Mapping[str, tuple[int, int]]) -> dict[str, dict[str, object]]:
    """Per-family exact-task rates; never substitute coverage or pooled accuracy."""
    return {family: rate_observation(correct, total)
            for family, (correct, total) in counts.items()}


def stage_activation(activated_units: int, eligible_units: int, *, minimum: int = 1,
                     adequate_denominator: bool = True) -> str:
    """Classify a mechanism stage without collapsing zero and no denominator."""
    a, n, m = int(activated_units), int(eligible_units), int(minimum)
    if a < 0 or n < 0 or a > n or m < 1:
        raise ValueError("counts must be nonnegative, activated <= eligible, and minimum >= 1")
    if n == 0:
        return "unavailable"
    if not adequate_denominator:
        return "inconclusive"
    return "activated" if a >= m else "not_activated"


def mechanism_chain_status(stage_statuses: Mapping[str, str]) -> str:
    """Summarize only the chain status; preserve and report each stage separately."""
    if set(stage_statuses) != set(PIPELINE_STAGES):
        return "unavailable"
    values = list(stage_statuses.values())
    if any(v not in VALID_STAGE_STATES for v in values):
        return "unavailable"
    if all(v == "activated" for v in values):
        return "chain_activated"
    if any(v == "not_activated" for v in values):
        return "chain_break_observed"
    if any(v == "unavailable" for v in values):
        return "chain_unavailable"
    return "inconclusive"


def budget_contract(config_budget: int, scored_arm_budgets: Sequence[int], *,
                    full_scan_budget: int | None = None,
                    full_scan_declared_diagnostic: bool = False) -> bool:
    """Require config/runtime parity; allow larger scans only as declared diagnostics."""
    cfg = int(config_budget)
    arms = [int(v) for v in scored_arm_budgets]
    if cfg < 1 or not arms or any(v < 1 for v in arms) or any(v != cfg for v in arms):
        return False
    if full_scan_budget is None:
        return True
    scan = int(full_scan_budget)
    if scan < 1:
        return False
    if scan > cfg:
        return bool(full_scan_declared_diagnostic)
    if scan != cfg:
        return False
    return True


def protocol_integrity_status(*, budget_consistent: bool | None,
                              holdout_locked_before_run: bool | None,
                              holdout_single_use: bool | None,
                              evaluator_isolated: bool | None,
                              failure_logging_complete: bool | None) -> str:
    """Check required protocol controls; missing evidence is unavailable, not pass."""
    checks = (budget_consistent, holdout_locked_before_run, holdout_single_use,
              evaluator_isolated, failure_logging_complete)
    if any(v is False for v in checks):
        return "fail"
    if any(v is None for v in checks):
        return "unavailable"
    return "pass"


def validate_external_outcomes(payload: Mapping[str, object]) -> bool:
    """Reject internal ASFT scores from coverage-independent outcome payloads."""
    return not bool(set(payload) & FORBIDDEN_INTERNAL_FIELDS)
