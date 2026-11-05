"""Deterministic all-context and per-cell scoring; no suite is loaded or run here."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .arms import Prediction
from .world import Effect, NO_EFFECT, SUCCESS


@dataclass(frozen=True, slots=True)
class EligibleContext:
    context_id: str
    cell_id: str
    observed_effect: Effect


@dataclass(frozen=True, slots=True)
class PredictionRecord:
    context_id: str
    arm_id: str
    prediction: Prediction | None


@dataclass(frozen=True, slots=True)
class ScoreSummary:
    arm_id: str
    cell_id: str | None
    denominator: int
    correct: int
    wrong: int
    abstained: int
    invalid: int
    missing: int
    accuracy: float | None
    coverage: float | None


@dataclass(frozen=True, slots=True)
class ScoreReport:
    all_context: dict[str, ScoreSummary]
    by_cell: dict[tuple[str, str], ScoreSummary]


def _valid_effect(effect: Effect | None) -> bool:
    return effect in {SUCCESS, NO_EFFECT}


def _summary(
    *, arm_id: str, cell_id: str | None, contexts: tuple[EligibleContext, ...],
    prediction_index: dict[str, Prediction | None],
) -> ScoreSummary:
    correct = wrong = abstained = invalid = missing = 0
    for context in contexts:
        if context.context_id not in prediction_index:
            missing += 1
            continue
        prediction = prediction_index[context.context_id]
        if prediction is None:
            missing += 1
            continue
        if prediction.status == "ABSTAIN" and prediction.effect is None:
            abstained += 1
            continue
        if prediction.status != "PREDICTED" or not _valid_effect(prediction.effect):
            invalid += 1
            continue
        if prediction.effect == context.observed_effect:
            correct += 1
        else:
            wrong += 1
    denominator = len(contexts)
    covered = correct + wrong
    return ScoreSummary(
        arm_id=arm_id,
        cell_id=cell_id,
        denominator=denominator,
        correct=correct,
        wrong=wrong,
        abstained=abstained,
        invalid=invalid,
        missing=missing,
        accuracy=(correct / denominator) if denominator else None,
        coverage=(covered / denominator) if denominator else None,
    )


def aggregate_all_context_scores(
    *,
    eligible_contexts: Iterable[EligibleContext],
    predictions: Iterable[PredictionRecord],
    arm_ids: Iterable[str],
    expected_cell_ids: Iterable[str] | None = None,
) -> ScoreReport:
    """Score every eligible context; missing/abstain/invalid all remain zero.

    Unknown required states have no simulator effect label and therefore are not
    valid `EligibleContext` rows; handle those as predeclared abstention diagnostics,
    not as silently omitted scored outcomes.
    """
    contexts = tuple(eligible_contexts)
    if not contexts:
        raise ValueError("eligible context manifest must be non-empty")
    raw_arms = tuple(arm_ids)
    arms = tuple(dict.fromkeys(raw_arms))
    if not arms or any(not arm for arm in arms):
        raise ValueError("at least one non-empty arm ID is required")
    if len(arms) != len(raw_arms):
        raise ValueError("arm IDs must be unique")
    context_by_id = {context.context_id: context for context in contexts}
    if len(context_by_id) != len(contexts) or any(not context.context_id or not context.cell_id for context in contexts):
        raise ValueError("eligible context IDs and cell IDs must be non-empty and unique")
    if any(not _valid_effect(context.observed_effect) for context in contexts):
        raise ValueError("each scored eligible context needs a known exact world outcome")
    arm_set = set(arms)
    indexed: dict[tuple[str, str], Prediction | None] = {}
    for record in predictions:
        if record.arm_id not in arm_set:
            raise ValueError(f"prediction uses undeclared arm: {record.arm_id}")
        if record.context_id not in context_by_id:
            raise ValueError(f"prediction uses ineligible/unknown context: {record.context_id}")
        key = (record.arm_id, record.context_id)
        if key in indexed:
            raise ValueError("duplicate prediction record for arm/context")
        indexed[key] = record.prediction
    raw_cells = tuple(expected_cell_ids) if expected_cell_ids is not None else tuple(context.cell_id for context in contexts)
    declared_cells = tuple(dict.fromkeys(raw_cells))
    if any(not cell for cell in declared_cells):
        raise ValueError("expected cell IDs must be non-empty")
    if len(declared_cells) != len(raw_cells):
        raise ValueError("expected cell IDs must be unique")
    if any(context.cell_id not in declared_cells for context in contexts):
        raise ValueError("eligible context has an undeclared cell ID")

    overall: dict[str, ScoreSummary] = {}
    by_cell: dict[tuple[str, str], ScoreSummary] = {}
    for arm in arms:
        overall[arm] = _summary(
            arm_id=arm,
            cell_id=None,
            contexts=contexts,
            prediction_index={
                context_id: indexed[(arm, context_id)]
                for context_id in context_by_id
                if (arm, context_id) in indexed
            },
        )
        for cell in declared_cells:
            cell_contexts = tuple(context for context in contexts if context.cell_id == cell)
            by_cell[(arm, cell)] = _summary(
                arm_id=arm,
                cell_id=cell,
                contexts=cell_contexts,
                prediction_index={
                    context.context_id: indexed[(arm, context.context_id)]
                    for context in cell_contexts
                    if (arm, context.context_id) in indexed
                },
            )
    return ScoreReport(all_context=overall, by_cell=by_cell)
