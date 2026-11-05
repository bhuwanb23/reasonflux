"""Frozen R0-R4 replay ladder and I0 invariant predictor for S3."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable, Mapping

from .world import (
    Effect,
    NO_EFFECT,
    SUCCESS,
    RelationalUnlockWorld,
    UnlockAction,
    UnlockState,
    UnlockTrace,
    validate_trace,
)


@dataclass(frozen=True, slots=True)
class Prediction:
    effect: Effect | None
    status: str
    reason: str
    source_trace_ids: tuple[str, ...] = ()

    @property
    def issued(self) -> bool:
        return self.status == "PREDICTED" and self.effect is not None


def _trace_signature(trace: UnlockTrace) -> tuple:
    return (
        RelationalUnlockWorld.exact_state_signature(trace.state),
        trace.action.key_id,
        trace.action.target_id,
    )


def _query_signature(state: UnlockState, action: UnlockAction) -> tuple:
    # context_id is logging metadata only, never an observable predictor input.
    return (RelationalUnlockWorld.exact_state_signature(state), action.key_id, action.target_id)


def _validated_traces(
    traces: Iterable[UnlockTrace], *, allow_development: bool = False
) -> tuple[UnlockTrace, ...]:
    records = tuple(traces)
    if not records:
        raise ValueError("arm fitting requires source traces")
    if len({trace.trace_id for trace in records}) != len(records):
        raise ValueError("source trace IDs must be unique")
    for trace in records:
        validate_trace(trace)
        if trace.provenance == "SYNTHETIC_DEVELOPMENT" and not allow_development:
            raise ValueError("development fixtures require explicit allow_development=True")
    return records


class R0RawReplay:
    """Exact ordered-example replay; only observable state/action values match."""

    def __init__(self, trace_effects: dict[tuple, tuple[Effect, tuple[str, ...]]], source_trace_ids: tuple[str, ...]):
        self._trace_effects = trace_effects
        self.source_trace_ids = source_trace_ids

    @classmethod
    def fit(cls, traces: Iterable[UnlockTrace], *, allow_development: bool = False) -> "R0RawReplay":
        records = _validated_traces(traces, allow_development=allow_development)
        exact: dict[tuple, tuple[Effect, tuple[str, ...]]] = {}
        for trace in records:
            signature = _trace_signature(trace)
            previous = exact.get(signature)
            if previous is not None and previous[0] != trace.observed_effect:
                raise ValueError("conflicting source effects for an identical R0 trace")
            ids = () if previous is None else previous[1]
            exact[signature] = (trace.observed_effect, ids + (trace.trace_id,))
        return cls(exact, tuple(trace.trace_id for trace in records))

    def predict(self, state: UnlockState, action: UnlockAction) -> Prediction:
        if not state.is_complete():
            return Prediction(None, "ABSTAIN", "REQUIRED_STATE_UNKNOWN", self.source_trace_ids)
        match = self._trace_effects.get(_query_signature(state, action))
        if match is None:
            return Prediction(None, "ABSTAIN", "NO_EXACT_TRACE_MATCH", self.source_trace_ids)
        effect, trace_ids = match
        return Prediction(effect, "PREDICTED", "EXACT_RAW_TRACE", trace_ids)


class R1ParameterizedReplay:
    """Typed role-slot macro; rebinds IDs, but does not check unlock relation."""

    def __init__(self, *, source_trace_ids: tuple[str, ...], expected_success: Effect):
        self.source_trace_ids = source_trace_ids
        self.expected_success = expected_success

    @classmethod
    def fit(cls, traces: Iterable[UnlockTrace], *, allow_development: bool = False) -> "R1ParameterizedReplay":
        records = _validated_traces(traces, allow_development=allow_development)
        positives = tuple(trace for trace in records if trace.observed_effect.success)
        if not positives:
            raise ValueError("R1 requires at least one successful source macro")
        if any(not trace.state.object_by_id(trace.action.key_id) for trace in positives):
            raise ValueError("R1 positive trace is missing its key slot")
        if any(not trace.state.object_by_id(trace.action.target_id) for trace in positives):
            raise ValueError("R1 positive trace is missing its target slot")
        return cls(
            # Record the complete shared input manifest even though this macro
            # derives its action template from positive examples only.
            source_trace_ids=tuple(trace.trace_id for trace in records),
            expected_success=positives[0].observed_effect,
        )

    def predict(self, state: UnlockState, action: UnlockAction) -> Prediction:
        if not state.is_complete():
            return Prediction(None, "ABSTAIN", "REQUIRED_STATE_UNKNOWN", self.source_trace_ids)
        if state.has_dangling_relations():
            return Prediction(None, "ABSTAIN", "DANGLING_RELATION", self.source_trace_ids)
        key = state.object_by_id(action.key_id)
        target = state.object_by_id(action.target_id)
        if key is None or target is None:
            return Prediction(None, "ABSTAIN", "SLOT_BINDING_MISSING", self.source_trace_ids)
        if target.closed is not True or not RelationalUnlockWorld.adjacent(state, target) or state.path_clear is not True:
            return Prediction(None, "ABSTAIN", "SOURCE_MACRO_PRECONDITION_FAILED", self.source_trace_ids)
        # This intentionally strong slot baseline maps new IDs by their declared
        # visible roles. It does not inspect opens_target_id; R4 tests that rule.
        if key.kind.value != "KEY" or target.kind.value != "TARGET":
            return Prediction(None, "ABSTAIN", "TYPED_SLOT_MISMATCH", self.source_trace_ids)
        return Prediction(self.expected_success, "PREDICTED", "TYPED_PARAMETERIZED_MACRO", self.source_trace_ids)


class R2CompressedReplay:
    """R1 macro plus lossless deduplication of exact source trace templates."""

    def __init__(
        self, replay: R1ParameterizedReplay, *, templates: tuple[tuple, ...], source_trace_count: int
    ):
        self._replay = replay
        self.templates = templates
        self.unique_template_count = len(templates)
        self.source_trace_count = source_trace_count
        self.source_trace_ids = replay.source_trace_ids

    @classmethod
    def fit(cls, traces: Iterable[UnlockTrace], *, allow_development: bool = False) -> "R2CompressedReplay":
        records = _validated_traces(traces, allow_development=allow_development)
        replay = R1ParameterizedReplay.fit(records, allow_development=allow_development)
        template_map: dict[tuple, Effect] = {}
        for trace in records:
            signature = _trace_signature(trace)
            previous = template_map.get(signature)
            if previous is not None and previous != trace.observed_effect:
                raise ValueError("conflicting source effects for an identical R2 template")
            template_map[signature] = trace.observed_effect
        templates = tuple((signature, effect) for signature, effect in template_map.items())
        return cls(replay, templates=templates, source_trace_count=len(records))

    def predict(self, state: UnlockState, action: UnlockAction) -> Prediction:
        prediction = self._replay.predict(state, action)
        return Prediction(prediction.effect, prediction.status, "COMPRESSED_" + prediction.reason, prediction.source_trace_ids)


UNARY_FEATURES: tuple[str, ...] = (
    "key_is_key",
    "target_is_target",
    "target_closed",
    "agent_adjacent",
    "path_clear",
)
RELATIONAL_FEATURE = "key_unlocks_selected_target"
R4_FEATURES: tuple[str, ...] = UNARY_FEATURES + (RELATIONAL_FEATURE,)


def _fit_feature_table(
    traces: tuple[UnlockTrace, ...], feature_names: tuple[str, ...]
) -> dict[tuple[bool, ...], Effect | None]:
    """Compile an exact source-supported truth table; None marks conflicts."""
    table: dict[tuple[bool, ...], Effect | None] = {}
    for trace in traces:
        features = RelationalUnlockWorld.source_only_features(trace.state, trace.action)
        if features is None:
            continue
        row = tuple(features[name] for name in feature_names)
        label = trace.observed_effect
        if row not in table:
            table[row] = label
        elif table[row] != label:
            table[row] = None
    return table


def _table_prediction(
    table: Mapping[tuple[bool, ...], Effect | None],
    feature_names: tuple[str, ...],
    state: UnlockState,
    action: UnlockAction,
    source_trace_ids: tuple[str, ...],
    arm_reason: str,
) -> Prediction:
    features = RelationalUnlockWorld.source_only_features(state, action)
    if features is None:
        return Prediction(None, "ABSTAIN", "REQUIRED_STATE_UNKNOWN", source_trace_ids)
    if state.has_dangling_relations():
        return Prediction(None, "ABSTAIN", "DANGLING_RELATION", source_trace_ids)
    row = tuple(features[name] for name in feature_names)
    if row not in table:
        return Prediction(None, "ABSTAIN", "UNSEEN_FEATURE_VECTOR", source_trace_ids)
    effect = table[row]
    if effect is None:
        return Prediction(None, "ABSTAIN", "CONFLICTING_SOURCE_FEATURE_VECTOR", source_trace_ids)
    return Prediction(effect, "PREDICTED", arm_reason, source_trace_ids)


class R3GrammarReplay:
    """Exact source-derived decision table over unary visible predicates."""

    def __init__(self, table: dict[tuple[bool, ...], Effect | None], source_trace_ids: tuple[str, ...]):
        self.table = table
        self.feature_names = UNARY_FEATURES
        self.source_trace_ids = source_trace_ids

    @classmethod
    def fit(cls, traces: Iterable[UnlockTrace], *, allow_development: bool = False) -> "R3GrammarReplay":
        records = _validated_traces(traces, allow_development=allow_development)
        table = _fit_feature_table(records, UNARY_FEATURES)
        return cls(table, tuple(trace.trace_id for trace in records))

    def predict(self, state: UnlockState, action: UnlockAction) -> Prediction:
        return _table_prediction(
            self.table, self.feature_names, state, action, self.source_trace_ids, "R3_UNARY_DECISION_TABLE"
        )


@dataclass(frozen=True, slots=True)
class _TreeLeaf:
    effect: Effect


@dataclass(frozen=True, slots=True)
class _TreeTest:
    feature_index: int
    when_false: "_DecisionTree"
    when_true: "_DecisionTree"


_DecisionTree = _TreeLeaf | _TreeTest


def _tree_key(tree: _DecisionTree) -> tuple:
    if isinstance(tree, _TreeLeaf):
        return (0, int(tree.effect.success))
    return (1, tree.feature_index, _tree_key(tree.when_false), _tree_key(tree.when_true))


def _minimum_consistent_tree(
    labeled_rows: Mapping[tuple[bool, ...], Effect],
) -> _DecisionTree:
    """Find the minimum-node decision tree over the fixed six-Boolean grammar.

    Each predicate may be tested at most once per path. Ties minimize the
    recursive serialization, which gives fixed feature order and false-first
    branch order. Memoization spans at most the subsets induced by six predicates.
    """
    rows = tuple(sorted(labeled_rows.items(), key=lambda item: item[0]))

    @lru_cache(maxsize=None)
    def solve(row_indices: tuple[int, ...], remaining: tuple[int, ...]) -> _DecisionTree:
        labels = {rows[index][1] for index in row_indices}
        if len(labels) == 1:
            return _TreeLeaf(next(iter(labels)))
        candidates: list[_DecisionTree] = []
        for feature_index in remaining:
            false_rows = tuple(index for index in row_indices if not rows[index][0][feature_index])
            true_rows = tuple(index for index in row_indices if rows[index][0][feature_index])
            if not false_rows or not true_rows:
                continue
            next_remaining = tuple(index for index in remaining if index != feature_index)
            false_tree = solve(false_rows, next_remaining)
            true_tree = solve(true_rows, next_remaining)
            candidates.append(_TreeTest(feature_index, false_tree, true_tree))
        if not candidates:
            raise ValueError("conflicting labels cannot be separated by the frozen R4 predicates")
        return min(candidates, key=lambda tree: (1 + _tree_node_count(tree.when_false) + _tree_node_count(tree.when_true), _tree_key(tree)))

    def _tree_node_count(tree: _DecisionTree) -> int:
        if isinstance(tree, _TreeLeaf):
            return 0
        return 1 + _tree_node_count(tree.when_false) + _tree_node_count(tree.when_true)

    return solve(tuple(range(len(rows))), tuple(range(len(R4_FEATURES))))


class R4ReplayMax:
    """Minimum source-consistent Boolean decision script over six frozen predicates."""

    def __init__(self, tree: _DecisionTree, source_trace_ids: tuple[str, ...]):
        self.tree = tree
        self.feature_names = R4_FEATURES
        self.source_trace_ids = source_trace_ids

    @classmethod
    def fit(cls, traces: Iterable[UnlockTrace], *, allow_development: bool = False) -> "R4ReplayMax":
        records = _validated_traces(traces, allow_development=allow_development)
        labeled_rows: dict[tuple[bool, ...], Effect] = {}
        for trace in records:
            features = RelationalUnlockWorld.source_only_features(trace.state, trace.action)
            if features is None:
                raise ValueError("R4 source trace has unknown required features")
            row = tuple(features[name] for name in R4_FEATURES)
            previous = labeled_rows.get(row)
            if previous is not None and previous != trace.observed_effect:
                raise ValueError("R4 source labels conflict for an identical six-feature vector")
            labeled_rows[row] = trace.observed_effect
        tree = _minimum_consistent_tree(labeled_rows)
        return cls(tree, tuple(trace.trace_id for trace in records))

    def predict_feature_vector(self, values: Mapping[str, bool]) -> Effect:
        """Evaluate the frozen Boolean script on a complete abstract feature row."""
        if set(values) != set(self.feature_names) or any(type(values[name]) is not bool for name in self.feature_names):
            raise ValueError("R4 requires exactly one Boolean value for every frozen feature")
        row = tuple(values[name] for name in self.feature_names)
        node = self.tree
        while isinstance(node, _TreeTest):
            node = node.when_true if row[node.feature_index] else node.when_false
        return node.effect

    def predict(self, state: UnlockState, action: UnlockAction) -> Prediction:
        features = RelationalUnlockWorld.source_only_features(state, action)
        if features is None:
            return Prediction(None, "ABSTAIN", "REQUIRED_STATE_UNKNOWN", self.source_trace_ids)
        if state.has_dangling_relations():
            return Prediction(None, "ABSTAIN", "DANGLING_RELATION", self.source_trace_ids)
        effect = self.predict_feature_vector(features)
        return Prediction(effect, "PREDICTED", "R4_MINIMUM_SOURCE_BOOLEAN_TREE", self.source_trace_ids)


def _i0_relation_success(state: UnlockState, action: UnlockAction) -> bool:
    if not state.is_complete() or state.has_dangling_relations():
        return False
    key = state.object_by_id(action.key_id)
    target = state.object_by_id(action.target_id)
    if key is None or target is None:
        return False
    return bool(
        key.kind.value == "KEY"
        and target.kind.value == "TARGET"
        and key.opens_target_id == target.object_id
        and target.closed is True
        and abs(state.agent_x - target.x) + abs(state.agent_y - target.y) == 1
        and state.path_clear is True
    )


class I0Invariant:
    """Explicit typed relational predictor, fit-checked on source traces."""

    relation_id = "synthetic:unlock-relation:typed-target-reference:v1"

    def __init__(self, source_trace_ids: tuple[str, ...]):
        self.source_trace_ids = source_trace_ids

    @classmethod
    def fit(cls, traces: Iterable[UnlockTrace], *, allow_development: bool = False) -> "I0Invariant":
        records = _validated_traces(traces, allow_development=allow_development)
        if not any(trace.observed_effect.success for trace in records):
            raise ValueError("I0 requires a positive source example")
        for trace in records:
            if _i0_relation_success(trace.state, trace.action) != trace.observed_effect.success:
                raise ValueError("source labels conflict with the predeclared I0 relation")
        return cls(tuple(trace.trace_id for trace in records))

    def predict(self, state: UnlockState, action: UnlockAction) -> Prediction:
        if not state.is_complete() or state.has_dangling_relations():
            return Prediction(None, "ABSTAIN", "REQUIRED_STATE_UNKNOWN_OR_DANGLING_REF", self.source_trace_ids)
        effect = SUCCESS if _i0_relation_success(state, action) else NO_EFFECT
        return Prediction(effect, "PREDICTED", self.relation_id, self.source_trace_ids)
