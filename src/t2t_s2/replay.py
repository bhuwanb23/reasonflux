"""Bounded source-only trace-to-script R1-Max baseline for S2."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Callable, Iterable

from .world import ACTION, SUCCESS, Effect, KeyDoorState, Trace


@dataclass(frozen=True, slots=True)
class Prediction:
    effect: Effect | None
    status: str
    reason: str

    @property
    def issued(self) -> bool:
        return self.status == "PREDICTED" and self.effect is not None


# Frozen observable feature grammar. It is declared before the S2 run and does
# not include any hidden state, target labels, or learned counterexample update.
FEATURES: tuple[tuple[str, Callable[[KeyDoorState], bool]], ...] = (
    ("adjacent", lambda state: state.adjacent),
    ("door_closed", lambda state: state.door_closed),
    ("has_key", lambda state: state.has_key),
    ("corridor_clear", lambda state: state.corridor_clear),
    ("key_color == door_color", lambda state: state.colors_match()),
)


class R1MaxReplay:
    """Compress examples into the shortest consistent conditional macro.

    R1-Max uses only source traces. It enumerates conjunctions in the frozen
    visible-feature grammar, chooses the shortest rule that exactly reproduces
    all source effect labels, then compiles it as a script (no P2 invariant
    object, lifecycle, or counterexample updates). This deliberately strong
    baseline can express the same simple relation as I0 if the source traces
    support it.
    """

    def __init__(
        self,
        *,
        support_trace_ids: tuple[str, ...],
        negative_trace_ids: tuple[str, ...],
        guard_predicates: tuple[str, ...],
    ):
        self.support_trace_ids = support_trace_ids
        self.negative_trace_ids = negative_trace_ids
        self.guard_predicates = guard_predicates
        self._feature_map = dict(FEATURES)
        self._fitted = True

    @classmethod
    def fit(cls, source_traces: Iterable[Trace]) -> "R1MaxReplay":
        traces = tuple(source_traces)
        if len(traces) < 3:
            raise ValueError("R1-Max requires positive and negative source traces")
        if len({trace.trace_id for trace in traces}) != len(traces):
            raise ValueError("source trace IDs must be unique")
        if any(trace.action != ACTION for trace in traces):
            raise ValueError("R1-Max source traces must use the frozen toy action")
        if any(not trace.state.is_complete() for trace in traces):
            raise ValueError("R1-Max source traces must have complete states")
        positives = tuple(trace for trace in traces if trace.observed_effect.succeeded)
        negatives = tuple(trace for trace in traces if not trace.observed_effect.succeeded)
        if len(positives) < 2 or not negatives:
            raise ValueError("R1-Max requires at least two supports and one negative trace")
        if len({trace.state.key_color for trace in positives}) < 2:
            raise ValueError("R1-Max needs distinct source literals to test slot abstraction")

        feature_map = dict(FEATURES)
        names = tuple(name for name, _ in FEATURES)
        consistent: list[tuple[str, ...]] = []
        for size in range(1, len(names) + 1):
            for subset in combinations(names, size):
                if all(
                    all(feature_map[name](trace.state) for name in subset)
                    == trace.observed_effect.succeeded
                    for trace in traces
                ):
                    consistent.append(subset)
            if consistent:
                break
        if not consistent:
            raise ValueError("no conjunction in the frozen replay grammar fits source traces")
        # FEATURES is in fixed stable order, so this tie rule is deterministic.
        selected = min(consistent, key=lambda subset: tuple(names.index(name) for name in subset))
        return cls(
            support_trace_ids=tuple(trace.trace_id for trace in positives),
            negative_trace_ids=tuple(trace.trace_id for trace in negatives),
            guard_predicates=selected,
        )

    def predict(self, state: KeyDoorState) -> Prediction:
        if not self._fitted or not state.is_complete():
            return Prediction(None, "ABSTAIN", "REQUIRED_FIELD_UNKNOWN_OR_BASELINE_UNFIT")
        macro_applies = all(self._feature_map[name](state) for name in self.guard_predicates)
        return Prediction(
            SUCCESS if macro_applies else Effect(False, False),
            "PREDICTED",
            "COMPILED_SOURCE_MACRO_GUARD" if macro_applies else "COMPILED_SOURCE_MACRO_ELSE",
        )
