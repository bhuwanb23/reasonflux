"""Software-only checks on tiny development fixtures; not an S3 evaluation suite."""

from __future__ import annotations

import json
from itertools import product

import pytest

from t2t_s3.arms import (
    I0Invariant,
    Prediction,
    R0RawReplay,
    R1ParameterizedReplay,
    R2CompressedReplay,
    R3GrammarReplay,
    R4ReplayMax,
)
from t2t_s3.eventlog import append_event, prediction_event
from t2t_s3.generator import (
    TransformationRecipe,
    apply_recipe,
    appearance_shift_recipe,
    composed_surface_recipe,
    identity_shift_recipe,
    layout_shift_recipe,
    role_layout_recipe,
)
from t2t_s3.scoring import EligibleContext, PredictionRecord, aggregate_all_context_scores
from t2t_s3.world import (
    NO_EFFECT,
    SUCCESS,
    Effect,
    ObjectKind,
    RelationalUnlockWorld,
    UnlockAction,
    UnlockObject,
    UnlockState,
    UnlockTrace,
)


def fit_development(model_type, traces):
    """Explicit opt-in: development fixtures are never accepted as source by default."""
    return model_type.fit(traces, allow_development=True)


def development_source() -> tuple[UnlockTrace, UnlockTrace]:
    """Two hand-built examples for algorithm checks; not assigned to an S3 split."""
    objects = (
        UnlockObject("key-A", ObjectKind.KEY, 0, 0, "red", "square", "target-A"),
        UnlockObject("target-A", ObjectKind.TARGET, 1, 0, "blue", "circle", closed=True),
        UnlockObject("target-B", ObjectKind.TARGET, 0, 1, "green", "triangle", closed=True),
    )
    positive_state = UnlockState("dev-positive", objects, 0, 0, True)
    positive_action = UnlockAction("key-A", "target-A")
    negative_state = UnlockState("dev-negative", objects, 0, 0, True)
    negative_action = UnlockAction("key-A", "target-B")
    return (
        UnlockTrace("dev-trace-positive", positive_state, positive_action, SUCCESS, "SYNTHETIC_DEVELOPMENT"),
        UnlockTrace("dev-trace-negative", negative_state, negative_action, NO_EFFECT, "SYNTHETIC_DEVELOPMENT"),
    )


def r4_development_competence_fixture() -> tuple[UnlockTrace, ...]:
    """Source-contrast fixture for R4's preconditions; never an S3 suite."""
    objects = (
        UnlockObject("key-A", ObjectKind.KEY, 0, 0, "red", "square", "target-A"),
        UnlockObject("key-B", ObjectKind.KEY, 0, 1, "yellow", "diamond", "target-B"),
        UnlockObject("target-A", ObjectKind.TARGET, 1, 0, "blue", "circle", closed=True),
        UnlockObject("target-B", ObjectKind.TARGET, 0, 1, "green", "triangle", closed=True),
        UnlockObject("distractor-key", ObjectKind.DISTRACTOR, 0, 0, "red", "square", "target-A", closed=True),
        UnlockObject("distractor-target", ObjectKind.DISTRACTOR, -1, 0, "gray", "pentagon", "distractor-target", closed=True),
    )

    def make_trace(trace_id: str, state: UnlockState, action: UnlockAction) -> UnlockTrace:
        effect = RelationalUnlockWorld.step(state, action)
        assert effect in {SUCCESS, NO_EFFECT}
        return UnlockTrace(trace_id, state, action, effect, "SYNTHETIC_DEVELOPMENT")

    agent = (0, 0)
    return (
        make_trace("r4-dev-positive", UnlockState("r4-dev-positive-context", objects, *agent, True), UnlockAction("key-A", "target-A")),
        make_trace("r4-dev-wrong-relation", UnlockState("r4-dev-wrong-relation-context", objects, *agent, True), UnlockAction("key-A", "target-B")),
        make_trace(
            "r4-dev-open-target",
            UnlockState(
                "r4-dev-open-target-context",
                tuple(
                    UnlockObject(o.object_id, o.kind, o.x, o.y, o.color, o.shape, o.opens_target_id, False)
                    if o.object_id == "target-A" else o for o in objects
                ),
                *agent,
                True,
            ),
            UnlockAction("key-A", "target-A"),
        ),
        make_trace("r4-dev-nonadjacent", UnlockState("r4-dev-nonadjacent-context", objects, 4, 4, True), UnlockAction("key-A", "target-A")),
        make_trace("r4-dev-blocked-path", UnlockState("r4-dev-blocked-path-context", objects, *agent, False), UnlockAction("key-A", "target-A")),
        make_trace("r4-dev-wrong-key", UnlockState("r4-dev-wrong-key-context", objects, *agent, True), UnlockAction("distractor-key", "target-A")),
        make_trace(
            "r4-dev-wrong-target-role",
            UnlockState(
                "r4-dev-wrong-target-context",
                tuple(
                    UnlockObject(o.object_id, o.kind, o.x, o.y, o.color, o.shape, "distractor-target", o.closed)
                    if o.object_id == "key-A" else o
                    for o in objects
                ),
                *agent,
                True,
            ),
            UnlockAction("key-A", "distractor-target"),
        ),
        make_trace("r4-dev-wrong-both-roles", UnlockState("r4-dev-wrong-both-context", objects, *agent, True), UnlockAction("distractor-target", "distractor-target")),
        make_trace(
            "r4-dev-known-absent-key",
            UnlockState("r4-dev-no-key-context", tuple(o for o in objects if o.kind is not ObjectKind.KEY), *agent, True),
            UnlockAction("absent-key", "target-A"),
        ),
    )


def test_world_uses_typed_relation_and_exact_no_effect():
    positive, negative = development_source()
    assert RelationalUnlockWorld.step(positive.state, positive.action) == SUCCESS
    assert RelationalUnlockWorld.step(negative.state, negative.action) == NO_EFFECT


def test_named_transformation_recipe_families_preserve_world_relation():
    positive, _ = development_source()
    for recipe in (
        identity_shift_recipe(positive.state),
        appearance_shift_recipe(positive.state),
        layout_shift_recipe(),
        role_layout_recipe(positive.state),
        composed_surface_recipe(positive.state),
    ):
        transformed = apply_recipe(positive.state, recipe)
        action = UnlockAction(
            dict(recipe.rename_ids).get("key-A", "key-A"),
            dict(recipe.rename_ids).get("target-A", "target-A"),
        )
        assert RelationalUnlockWorld.step(transformed, action) == SUCCESS
    with pytest.raises(ValueError, match="one-to-one"):
        TransformationRecipe("bad-appearance", recolor=(("red", "x"), ("blue", "x"))).as_surface_transform()


def test_r0_replays_observable_state_not_context_metadata():
    positive, _ = development_source()
    arm = fit_development(R0RawReplay, (positive,))
    same_observation_new_metadata = UnlockState(
        "different-logging-id", positive.state.objects, positive.state.agent_x,
        positive.state.agent_y, positive.state.path_clear,
    )
    assert arm.predict(same_observation_new_metadata, positive.action).effect == SUCCESS
    renamed = apply_recipe(
        positive.state,
        TransformationRecipe(
            "id-shift",
            rename_ids=(("key-A", "key-X"), ("target-A", "target-X"), ("target-B", "target-Y")),
        ),
    )
    assert arm.predict(renamed, UnlockAction("key-X", "target-X")).status == "ABSTAIN"


def test_r1_r2_r3_and_r4_have_declared_expressivity_boundary():
    positive, negative = development_source()
    traces = (positive, negative)
    fresh_positive = apply_recipe(
        positive.state,
        TransformationRecipe(
            "new-surface",
            rename_ids=(("key-A", "key-new"), ("target-A", "target-new"), ("target-B", "target-other")),
            recolor=(("red", "amber"), ("blue", "violet"), ("green", "silver")),
            reshape=(("square", "hex"), ("circle", "star"), ("triangle", "oval")),
            translation=(3, -2),
            rotate_quarters=1,
            reverse_object_order=True,
        ),
    )
    fresh_action = UnlockAction("key-new", "target-new")
    assert RelationalUnlockWorld.step(fresh_positive, fresh_action) == SUCCESS
    r1 = fit_development(R1ParameterizedReplay, traces)
    assert r1.source_trace_ids == (positive.trace_id, negative.trace_id)
    assert r1.predict(fresh_positive, fresh_action).effect == SUCCESS
    compressed = fit_development(R2CompressedReplay, traces)
    assert compressed.source_trace_ids == (positive.trace_id, negative.trace_id)
    assert compressed.unique_template_count == 2
    assert compressed.source_trace_count == 2
    assert compressed.predict(fresh_positive, fresh_action).effect == SUCCESS
    assert fit_development(R3GrammarReplay, traces).predict(fresh_positive, fresh_action).status == "ABSTAIN"

    sparse_r4 = fit_development(R4ReplayMax, traces)
    open_target = UnlockState(
        "dev-open-unseen",
        tuple(
            UnlockObject(o.object_id, o.kind, o.x, o.y, o.color, o.shape, o.opens_target_id, False)
            if o.object_id == "target-A" else o
            for o in positive.state.objects
        ),
        positive.state.agent_x,
        positive.state.agent_y,
        positive.state.path_clear,
    )
    assert sparse_r4.predict(open_target, positive.action).effect == SUCCESS  # insufficient source contrasts

    competent_fixture = r4_development_competence_fixture()
    r4 = fit_development(R4ReplayMax, competent_fixture)
    assert "key_unlocks_selected_target" in r4.feature_names
    assert r4.predict(fresh_positive, fresh_action).effect == SUCCESS
    assert r4.predict(fresh_positive, UnlockAction("key-new", "target-other")).effect == NO_EFFECT
    assert r4.predict(competent_fixture[2].state, competent_fixture[2].action).effect == NO_EFFECT
    assert r4.predict(competent_fixture[3].state, competent_fixture[3].action).effect == NO_EFFECT
    assert r4.predict(competent_fixture[4].state, competent_fixture[4].action).effect == NO_EFFECT


def test_i0_is_typed_relation_model_and_unknowns_abstain():
    positive, negative = development_source()
    model = fit_development(I0Invariant, (positive, negative))
    assert model.predict(positive.state, positive.action).effect == SUCCESS
    assert model.predict(negative.state, negative.action).effect == NO_EFFECT
    unknown = UnlockState("dev-unknown", positive.state.objects, 0, 0, None)
    assert model.predict(unknown, positive.action).status == "ABSTAIN"
    assert RelationalUnlockWorld.step(unknown, positive.action) is None


def test_known_absence_is_distinct_from_unknown_and_yields_no_effect():
    state = UnlockState(
        "dev-no-key",
        (UnlockObject("target-A", ObjectKind.TARGET, 1, 0, "blue", "circle", closed=True),),
        0,
        0,
        True,
    )
    action = UnlockAction("absent-key", "target-A")
    assert state.is_complete()
    assert RelationalUnlockWorld.step(state, action) == NO_EFFECT


def test_prediction_logging_does_not_include_observed_outcome(tmp_path):
    positive, _ = development_source()
    prediction = fit_development(I0Invariant, development_source()).predict(positive.state, positive.action)
    event = prediction_event(
        event_id="dev-event-1",
        package_version="dev-only",
        arm_id="I0",
        cell_id="dev-cell",
        state=positive.state,
        action=positive.action,
        prediction=prediction,
    )
    destination = tmp_path / "audit.jsonl"
    append_event(destination, event)
    record = json.loads(destination.read_text(encoding="utf-8"))
    assert record["event_type"] == "prediction"
    assert "observed_effect" not in record["payload"]
    assert record["payload"]["status"] == "PREDICTED"


def test_source_fit_rejects_non_synthetic_and_inconsistent_r4_labels():
    positive, _ = development_source()
    with pytest.raises(ValueError, match="allow_development"):
        R4ReplayMax.fit((positive,))
    non_synthetic = UnlockTrace("bad-source", positive.state, positive.action, SUCCESS, "EXTERNAL")
    with pytest.raises(ValueError, match="synthetic"):
        R4ReplayMax.fit((non_synthetic,))
    conflicting = UnlockTrace("r4-conflict", positive.state, positive.action, NO_EFFECT, "SYNTHETIC_DEVELOPMENT")
    with pytest.raises(ValueError, match="conflict"):
        R4ReplayMax.fit((positive, conflicting), allow_development=True)
    partial = UnlockTrace("bad-partial", positive.state, positive.action, Effect(True, False), "SYNTHETIC_DEVELOPMENT")
    with pytest.raises(ValueError, match="partial effects"):
        R4ReplayMax.fit((partial,), allow_development=True)


def test_r4_compiler_from_source_contrasts_matches_relation_on_all_abstract_rows():
    model = fit_development(R4ReplayMax, r4_development_competence_fixture())
    for bits in product((False, True), repeat=len(model.feature_names)):
        expected = SUCCESS if all(bits) else NO_EFFECT
        assert model.predict_feature_vector(dict(zip(model.feature_names, bits))) == expected


def test_replay_compiler_abstains_on_dangling_relation_metadata():
    fitted = fit_development(R4ReplayMax, r4_development_competence_fixture())
    positive, _ = development_source()
    malformed_objects = tuple(
        UnlockObject(o.object_id, o.kind, o.x, o.y, o.color, o.shape, "missing-target", o.closed)
        if o.object_id == "key-A" else o
        for o in positive.state.objects
    )
    malformed = UnlockState("dev-dangling", malformed_objects, 0, 0, True)
    assert fitted.predict(malformed, positive.action).status == "ABSTAIN"


def test_scoring_keeps_missing_abstain_invalid_and_empty_cells_in_denominator():
    eligible = (
        EligibleContext("dev-c1", "dev-cell-a", SUCCESS),
        EligibleContext("dev-c2", "dev-cell-a", NO_EFFECT),
        EligibleContext("dev-c3", "dev-cell-b", SUCCESS),
    )
    predictions = (
        PredictionRecord("dev-c1", "I0", Prediction(SUCCESS, "PREDICTED", "dev")),
        PredictionRecord("dev-c2", "I0", Prediction(None, "ABSTAIN", "dev")),
        PredictionRecord("dev-c1", "R4", Prediction(NO_EFFECT, "PREDICTED", "dev")),
        PredictionRecord("dev-c2", "R4", Prediction(NO_EFFECT, "PREDICTED", "dev")),
        PredictionRecord("dev-c3", "R4", Prediction(Effect(True, False), "PREDICTED", "invalid")),
    )
    report = aggregate_all_context_scores(
        eligible_contexts=eligible,
        predictions=predictions,
        arm_ids=("I0", "R4"),
        expected_cell_ids=("dev-cell-a", "dev-cell-b", "dev-empty"),
    )
    i0 = report.all_context["I0"]
    assert (i0.denominator, i0.correct, i0.abstained, i0.missing, i0.accuracy, i0.coverage) == (3, 1, 1, 1, 1 / 3, 1 / 3)
    r4 = report.all_context["R4"]
    assert (r4.denominator, r4.correct, r4.wrong, r4.invalid, r4.accuracy) == (3, 1, 1, 1, 1 / 3)
    assert report.by_cell[("I0", "dev-empty")].denominator == 0
    assert report.by_cell[("I0", "dev-empty")].accuracy is None
