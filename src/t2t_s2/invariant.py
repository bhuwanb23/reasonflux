"""Minimal one-family invariant fit and counterexample boundary update."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .replay import Prediction
from .world import ACTION, KeyDoorState, Trace, SUCCESS, Effect


@dataclass(frozen=True, slots=True)
class BoundaryVersion:
    version_id: str
    requires_color_match: bool = False
    predecessor_id: str | None = None

    def applicable(self, state: KeyDoorState) -> bool:
        if not state.is_complete() or not state.base_conditions_hold():
            return False
        return not self.requires_color_match or state.colors_match()


@dataclass(frozen=True, slots=True)
class CounterexampleRecord:
    record_id: str
    state: KeyDoorState
    predicted_skill_effect: Effect
    observed_effect: Effect
    provenance: str = "SYNTHETIC_FIXTURE"


class InvariantI0:
    """Fit one predeclared color-equality relation from synthetic traces.

    This is deliberately not a general invariant-discovery system. The
    candidate vocabulary contains exactly one relation for this toy world.
    """

    relation_id = "synthetic:relation:key-color-equals-door-color:v1"
    candidate_predicate = "key_color == door_color"

    def __init__(self, support_trace_ids: tuple[str, ...], negative_trace_ids: tuple[str, ...]):
        self.support_trace_ids = support_trace_ids
        self.negative_trace_ids = negative_trace_ids
        self.fitted = True

    @classmethod
    def fit(cls, source_traces: Iterable[Trace]) -> "InvariantI0":
        traces = tuple(source_traces)
        positives = tuple(trace for trace in traces if trace.observed_effect.succeeded)
        hard_negatives = tuple(
            trace
            for trace in traces
            if not trace.observed_effect.succeeded and trace.state.base_conditions_hold()
        )
        if not positives or not hard_negatives:
            raise ValueError("the relation needs both positive and base-matched negative source evidence")
        if any(trace.action != ACTION for trace in traces):
            raise ValueError("the one-family fit requires the frozen synthetic action")
        if any(not trace.state.is_complete() for trace in traces):
            raise ValueError("the one-family fit requires fully observed synthetic states")
        if any(
            (trace.state.base_conditions_hold() and trace.state.colors_match())
            != trace.observed_effect.succeeded
            for trace in traces
        ):
            raise ValueError("source labels are inconsistent with the predeclared relation family")
        if any(not trace.state.colors_match() for trace in positives):
            raise ValueError("positive examples contradict the predeclared color-match candidate")
        if any(trace.state.colors_match() for trace in hard_negatives):
            raise ValueError("base-matched negative evidence contradicts the candidate relation")
        return cls(
            support_trace_ids=tuple(trace.trace_id for trace in positives),
            negative_trace_ids=tuple(trace.trace_id for trace in hard_negatives),
        )

    def predict_effect(self, state: KeyDoorState) -> Prediction:
        if not self.fitted or not state.is_complete():
            return Prediction(None, "ABSTAIN", "REQUIRED_FIELD_UNKNOWN_OR_MODEL_UNFIT")
        successful = state.base_conditions_hold() and state.colors_match()
        effect = SUCCESS if successful else Effect(False, False)
        return Prediction(effect, "PREDICTED", self.candidate_predicate)

    @staticmethod
    def initial_boundary() -> BoundaryVersion:
        # The deliberately broad, frozen I0 guard is based on positive-source
        # base predicates; counterexample updating is disabled for the N arm.
        return BoundaryVersion("synthetic:boundary:G0", requires_color_match=False)

    @staticmethod
    def predict_skill_effect(state: KeyDoorState, boundary: BoundaryVersion) -> Effect | None:
        # Separate skill activation prediction used for B: when the proposed
        # skill's guard admits a state, it predicts the intended open-and-enter
        # effect. N scores the general transition predictor above.
        return SUCCESS if boundary.applicable(state) else None


class BoundaryLearner:
    """Append one verified scope counterexample and propose a successor guard."""

    def __init__(self) -> None:
        self.counterexample_ledger: list[CounterexampleRecord] = []

    def refine(
        self,
        parent: BoundaryVersion,
        counterexample: CounterexampleRecord,
        positive_supports: tuple[Trace, ...],
    ) -> BoundaryVersion:
        if any(record.record_id == counterexample.record_id for record in self.counterexample_ledger):
            raise ValueError("counterexample record ID must be unique")
        if parent.requires_color_match:
            raise ValueError("this S2 update is defined only for the frozen broad G0 boundary")
        if not parent.applicable(counterexample.state):
            raise ValueError("counterexample must be admitted by the parent boundary")
        if counterexample.predicted_skill_effect != SUCCESS or counterexample.observed_effect.succeeded:
            raise ValueError("counterexample must contradict the admitted skill effect")
        if counterexample.state.colors_match():
            raise ValueError("the predeclared color-match predicate does not distinguish this CE")
        if not positive_supports:
            raise ValueError("at least one source support is required")
        if any(
            not trace.observed_effect.succeeded
            or not parent.applicable(trace.state)
            or not trace.state.colors_match()
            for trace in positive_supports
        ):
            raise ValueError("color-match must be known true in all declared positive supports")

        # Append the evidence record; the immutable parent is not modified.
        self.counterexample_ledger.append(counterexample)
        return BoundaryVersion(
            version_id=f"{parent.version_id}:successor:color-match",
            requires_color_match=True,
            predecessor_id=parent.version_id,
        )
