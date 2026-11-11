"""Focused tests for the synthetic-only T2T-S2 key/door mechanism check."""

from __future__ import annotations

import pytest

from t2t_s2.evaluation import evaluate_boundary, evaluate_prediction_accuracy
from t2t_s2.invariant import BoundaryLearner, CounterexampleRecord, InvariantI0
from t2t_s2.replay import R1MaxReplay
from t2t_s2.run import frozen_b_holdout, frozen_n_holdout, frozen_source_traces, run_s2
from t2t_s2.world import ACTION, NO_EFFECT, SUCCESS, KeyDoorState, KeyDoorWorld


def state(
    key: str,
    door: str,
    *,
    context: str = "test",
    has_key: bool = True,
    corridor_clear: bool = True,
) -> KeyDoorState:
    return KeyDoorState(context, True, True, has_key, corridor_clear, key, door)


def test_world_transition_is_deterministic_and_uses_only_declared_fields():
    assert KeyDoorWorld.step(state("blue", "blue")) == SUCCESS
    assert KeyDoorWorld.step(state("red", "blue")) == NO_EFFECT
    assert KeyDoorWorld.step(state("blue", "blue", has_key=False)) == NO_EFFECT
    assert KeyDoorWorld.step(state("blue", "blue", corridor_clear=False)) == NO_EFFECT
    with pytest.raises(ValueError):
        KeyDoorWorld.step(state("blue", "blue"), action="UNDECLARED_ACTION")


def test_r1_max_compresses_source_supports_and_fails_closed_off_template():
    source = frozen_source_traces()
    replay = R1MaxReplay.fit(source)
    assert len(replay.support_trace_ids) == 2
    assert len(replay.negative_trace_ids) == 6
    assert replay.guard_predicates == (
        "adjacent", "door_closed", "has_key", "corridor_clear", "key_color == door_color"
    )

    # New matching literals bind through the compiled conditional macro.
    assert replay.predict(state("yellow", "yellow")).effect == SUCCESS
    # A novel mismatch is handled by the source-fitted macro's else branch.
    novel_mismatch = replay.predict(state("amber", "violet"))
    assert novel_mismatch.status == "PREDICTED"
    assert novel_mismatch.effect == NO_EFFECT
    assert replay.predict(state("blue", "blue", has_key=False)).effect == NO_EFFECT


def test_i0_predicts_exact_one_step_effect_for_complete_states():
    model = InvariantI0.fit(frozen_source_traces())
    assert model.predict_effect(state("cyan", "cyan")).effect == SUCCESS
    assert model.predict_effect(state("cyan", "red")).effect == NO_EFFECT
    assert model.predict_effect(state("cyan", "cyan", has_key=False)).effect == NO_EFFECT
    unknown = KeyDoorState("unknown", True, True, True, True, None, "blue")
    assert model.predict_effect(unknown).status == "ABSTAIN"


def test_claim_n_uses_all_contexts_and_counts_abstention_as_incorrect():
    source = frozen_source_traces()
    replay = R1MaxReplay.fit(source)
    model = InvariantI0.fit(source)
    holdout = frozen_n_holdout()
    scored = evaluate_prediction_accuracy(
        ((item, KeyDoorWorld.step(item)) for item in holdout),
        {"I0": model.predict_effect, "R1-Max": replay.predict},
    )
    assert scored["denominator"] == 8
    assert scored["arms"]["I0"]["correct"] == 8
    assert scored["arms"]["R1-Max"]["correct"] == 8
    assert scored["arms"]["R1-Max"]["abstain"] == 0
    assert scored["arms"]["R1-Max"]["accuracy"] == 1.0


def test_counterexample_appends_successor_boundary_without_mutating_parent():
    source = frozen_source_traces()
    supports = tuple(trace for trace in source if trace.observed_effect == SUCCESS)
    ce = next(trace for trace in source if trace.state.context_id == "SRC-CE-red-blue")
    model = InvariantI0.fit(source)
    parent = model.initial_boundary()
    predicted = model.predict_skill_effect(ce.state, parent)
    assert predicted == SUCCESS
    assert ce.observed_effect == NO_EFFECT

    record = CounterexampleRecord("synthetic:ce:one", ce.state, predicted, ce.observed_effect)
    learner = BoundaryLearner()
    successor = learner.refine(parent, record, supports)
    assert not parent.requires_color_match
    assert successor.requires_color_match
    assert successor.predecessor_id == parent.version_id
    assert len(learner.counterexample_ledger) == 1
    assert not successor.applicable(state("red", "blue"))
    assert successor.applicable(state("yellow", "yellow"))


def test_b_holdout_is_fresh_and_boundary_improves_without_losing_true_coverage():
    source = frozen_source_traces()
    supports = tuple(trace for trace in source if trace.observed_effect == SUCCESS)
    ce = next(trace for trace in source if trace.state.context_id == "SRC-CE-red-blue")
    model = InvariantI0.fit(source)
    parent = model.initial_boundary()
    predicted = model.predict_skill_effect(ce.state, parent)
    record = CounterexampleRecord("synthetic:ce:one", ce.state, predicted, ce.observed_effect)
    successor = BoundaryLearner().refine(parent, record, supports)

    holdout = frozen_b_holdout()
    assert all(item.context_id != ce.state.context_id for item in holdout)
    result = evaluate_boundary(holdout, {"G0": parent, "G1": successor})
    g0, g1 = result["boundaries"]["G0"], result["boundaries"]["G1"]
    assert g0["false_activation"] == 2
    assert g0["non_applicable"] == 4
    assert g1["false_activation"] == 0
    assert g1["non_applicable"] == 4
    assert g0["true_admitted"] == g1["true_admitted"] == 2
    assert g0["true_applicable"] == g1["true_applicable"] == 2


def test_boundary_refuses_duplicate_or_non_scope_counterexamples():
    source = frozen_source_traces()
    supports = tuple(trace for trace in source if trace.observed_effect == SUCCESS)
    ce = next(trace for trace in source if trace.state.context_id == "SRC-CE-red-blue")
    model = InvariantI0.fit(source)
    parent = model.initial_boundary()
    learner = BoundaryLearner()
    record = CounterexampleRecord(
        "synthetic:ce:duplicate", ce.state, SUCCESS, ce.observed_effect
    )
    learner.refine(parent, record, supports)
    with pytest.raises(ValueError, match="unique"):
        learner.refine(parent, record, supports)

    matching = state("yellow", "yellow")
    false_ce = CounterexampleRecord("synthetic:ce:false", matching, SUCCESS, SUCCESS)
    with pytest.raises(ValueError, match="contradict"):
        BoundaryLearner().refine(parent, false_ce, supports)


def test_frozen_run_reports_predeclared_n_and_b_decisions():
    result = run_s2()
    assert result["not_arc_or_benchmark"] is True
    assert result["n_decision_grade_status"] == "N-BLOCKED"
    assert result["b_scope_status"] == "FINITE_SYNTHETIC_FIXTURE_ONLY"
    assert result["n_result"]["decision"] == "N-FAIL"
    assert result["n_result"]["arms"]["I0"]["accuracy"] == 1.0
    assert result["n_result"]["arms"]["R1-Max"]["accuracy"] == 1.0
    assert result["n_result"]["delta_accuracy_I0_minus_R1"] == 0.0
    assert result["b_result"]["decision"] == "B-PASS"
    assert result["b_result"]["refinement"]["counterexample_not_in_holdout"] is True
    assert result["b_result"]["refinement"]["append_only_counterexample_count"] == 1
