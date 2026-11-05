"""Finite-fixture scoring for the frozen S2 N and B outcomes."""

from __future__ import annotations

from typing import Callable, Iterable, Mapping

from .invariant import BoundaryVersion
from .replay import Prediction
from .world import Effect, KeyDoorState, KeyDoorWorld


Predictor = Callable[[KeyDoorState], Prediction]


def evaluate_prediction_accuracy(
    cases: Iterable[tuple[KeyDoorState, Effect]],
    predictors: Mapping[str, Predictor],
) -> dict:
    frozen_cases = tuple(cases)
    if not frozen_cases:
        raise ValueError("prediction evaluation requires at least one held-out case")
    rows: list[dict] = []
    arm_counts = {
        name: {"correct": 0, "issued": 0, "abstain": 0}
        for name in predictors
    }
    for state, truth in frozen_cases:
        case_row = {"context_id": state.context_id, "truth": _effect_dict(truth), "arms": {}}
        for name, predictor in predictors.items():
            prediction = predictor(state)
            correct = prediction.issued and prediction.effect == truth
            counts = arm_counts[name]
            counts["issued"] += int(prediction.issued)
            counts["abstain"] += int(not prediction.issued)
            counts["correct"] += int(correct)
            case_row["arms"][name] = {
                "status": prediction.status,
                "reason": prediction.reason,
                "predicted_effect": _effect_dict(prediction.effect),
                "correct": bool(correct),
            }
        rows.append(case_row)
    arm_results = {}
    denominator = len(frozen_cases)
    for name, counts in arm_counts.items():
        arm_results[name] = {
            **counts,
            "denominator_all_contexts": denominator,
            "accuracy": counts["correct"] / denominator,
            "coverage": counts["issued"] / denominator,
        }
    return {"denominator": denominator, "arms": arm_results, "rows": rows}


def evaluate_boundary(
    cases: Iterable[KeyDoorState],
    boundaries: Mapping[str, BoundaryVersion],
) -> dict:
    frozen_cases = tuple(cases)
    if not frozen_cases:
        raise ValueError("boundary evaluation requires at least one held-out case")
    counts = {
        name: {
            "admitted": 0,
            "true_admitted": 0,
            "false_activation": 0,
            "false_rejection": 0,
            "true_applicable": 0,
            "non_applicable": 0,
        }
        for name in boundaries
    }
    rows=[]
    for state in frozen_cases:
        truth = KeyDoorWorld.applicable(state)
        row={"context_id": state.context_id, "truth_applicable": truth, "boundaries": {}}
        for name, boundary in boundaries.items():
            admitted = boundary.applicable(state)
            c=counts[name]
            c["admitted"] += int(admitted)
            c["true_admitted"] += int(admitted and truth)
            c["false_activation"] += int(admitted and not truth)
            c["false_rejection"] += int(not admitted and truth)
            c["true_applicable"] += int(truth)
            c["non_applicable"] += int(not truth)
            row["boundaries"][name] = {"admitted": admitted, "correct": admitted == truth}
        rows.append(row)
    results={}
    for name, c in counts.items():
        results[name] = {
            **c,
            "total_contexts": len(frozen_cases),
            "false_activation_rate_among_non_applicable": _ratio(c["false_activation"], c["non_applicable"]),
            "false_activation_rate_among_admitted": _ratio(c["false_activation"], c["admitted"]),
            "applicable_context_coverage": _ratio(c["true_admitted"], c["true_applicable"]),
            "total_coverage": c["admitted"] / len(frozen_cases),
        }
    return {"denominator": len(frozen_cases), "boundaries": results, "rows": rows}


def _ratio(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def _effect_dict(effect: Effect | None) -> dict | None:
    if effect is None:
        return None
    return {"door_open": effect.door_open, "agent_advanced": effect.agent_advanced}
