from __future__ import annotations

import pytest
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from representations.r3 import Action
from experiments.phase2ia.runtime_config import build_trace_miner
from traces.normalizer import normalize_trace
from traces.semantic_adapter import (
    TRACE_SCHEMA_VERSION,
    Representation,
    TargetScope,
    adapt_successful_candidate,
    operation_mapping_table,
    validate_semantic_trace,
)

HASH_A = "a" * 64
HASH_B = "b" * 64


def _adapt(rep, operation, **kwargs):
    fields = {
        "task_id": "synthetic-task-1",
        "candidate_id": "synthetic-candidate-1",
        "grammar_hash": HASH_A,
        "implementation_hash": HASH_B,
        "trial_index": 1,
        "trace_id": "trace-fixed-1",
    }
    fields.update(kwargs)
    return adapt_successful_candidate(representation=rep, operation=operation, **fields)


def test_equivalent_r1_grid_and_r3_object_rotation_share_mined_operation_tokens():
    r1 = _adapt(Representation.R1, "rotate_90")
    r3 = _adapt(Representation.R3, Action.make("rotate", k=1))
    assert r1.trace.operations == r3.trace.operations
    norm1, norm3 = normalize_trace(r1.trace), normalize_trace(r3.trace)
    assert norm1.operations == norm3.operations == r1.trace.operations
    assert norm1.metadata == norm3.metadata
    assert r1.trace.operations == [
        "validate_input", "construct_representation", "apply_rotate_90", "verify_demonstrations"
    ]
    assert r1.events[2].target_scope is TargetScope.GRID
    assert r3.events[2].target_scope is TargetScope.OBJECT
    assert "R1" not in str(r1.trace.metadata) and "R3" not in str(r3.trace.metadata)
    assert "candidate_id" not in r1.trace.metadata
    assert "candidate_id" not in r3.trace.metadata


def test_reflection_aliases_match_actual_cell_effect_not_axis_name():
    r1_left_right = _adapt(Representation.R1, "reflect_horizontal")
    r3_left_right = _adapt(Representation.R3, Action.make("reflect_vertical_axis"))
    r1_top_bottom = _adapt(Representation.R1, "reflect_vertical")
    r3_top_bottom = _adapt(Representation.R3, Action.make("reflect_horizontal_axis"))
    assert r1_left_right.trace.operations[2] == r3_left_right.trace.operations[2] == "apply_flip_left_right"
    assert r1_top_bottom.trace.operations[2] == r3_top_bottom.trace.operations[2] == "apply_flip_top_bottom"
    assert r1_left_right.trace.operations[2] != r3_top_bottom.trace.operations[2]


def test_zero_offset_r3_move_maps_to_identity_action():
    r1 = _adapt(Representation.R1, "identity")
    r3 = _adapt(Representation.R3, Action.make("move", dy=0, dx=0))
    assert r1.trace.operations[2] == r3.trace.operations[2] == "apply_identity"


def test_r1_and_r3_translations_share_abstraction_without_mining_parameters():
    r1 = _adapt(Representation.R1, "translate_constant")
    r3 = _adapt(Representation.R3, Action.make("move", dy=-2, dx=1))
    assert r1.trace.operations[2] == r3.trace.operations[2] == "apply_translate"
    assert r3.trace.steps[2].inputs == [{"target_scope": "object"}]
    assert r3.trace.steps[2].outputs == []
    assert r1.trace.steps[2].inputs == [{"target_scope": "grid"}]
    assert r3.events[2].target_scope is TargetScope.OBJECT


def test_independent_semantic_trace_validator_rejects_metadata_leakage():
    from dataclasses import replace
    adapted=_adapt(Representation.R3,Action.make("recolor",color=2))
    validate_semantic_trace(adapted)
    bad=replace(adapted,trace=replace(adapted.trace,metadata={"semantic_trace_schema":TRACE_SCHEMA_VERSION,"candidate_id":"leak"}))
    with pytest.raises(ValueError,match="metadata"):
        validate_semantic_trace(bad)


def test_trace_is_four_steps_and_provenance_is_separate_from_mining_projection():
    adapted = _adapt(Representation.R3, Action.make("recolor", color=0))
    assert len(adapted.trace.steps) == 4
    assert adapted.trace.outcome is not None and adapted.trace.outcome.success
    assert adapted.trace.outcome.result is None
    assert adapted.trace.metadata == {"semantic_trace_schema": TRACE_SCHEMA_VERSION}
    with pytest.raises(ValueError, match="independent task-family"):
        adapted.mining_projection(independent_task_family=" ")
    projected = adapted.mining_projection(independent_task_family="family-x")
    assert projected.metadata == {"task_family": "family-x", "semantic_trace_schema": TRACE_SCHEMA_VERSION}
    assert "R3" not in str(projected.metadata)
    assert adapted.provenance.representation is Representation.R3
    assert adapted.provenance.candidate_id == "synthetic-candidate-1"


def test_unknown_operation_and_invalid_r3_action_fail_closed():
    with pytest.raises(ValueError, match="not in frozen R1 grammar"):
        _adapt(Representation.R1, "unregistered_transform")
    with pytest.raises(ValueError, match="invalid R3 action"):
        _adapt(Representation.R3, Action.make("rotate", k=4))


def test_same_miner_receives_identical_synthetic_r1_r3_candidate_signatures():
    def corpus(rep):
        traces = []
        for i in range(6):
            family = ("synthetic-a" if i < 2 else "synthetic-b" if i < 5 else "synthetic-c")
            op = ("rotate_90" if rep is Representation.R1 else Action.make("rotate", k=1)) if i < 5 else (
                "translate_constant" if rep is Representation.R1 else Action.make("move", dy=1, dx=0)
            )
            adapted = _adapt(rep, op, task_id=f"synthetic-{i}", trace_id=f"{rep.value}-{i}")
            traces.append(adapted.mining_projection(independent_task_family=family))
        return traces

    result_r1 = build_trace_miner().mine(corpus(Representation.R1))
    result_r3 = build_trace_miner().mine(corpus(Representation.R3))
    patterns = lambda result: [(p.signature, p.frequency, tuple(p.task_families)) for p in result.success_patterns]
    candidates = lambda result: [(c.invariant_id, tuple(c.pattern_signature), tuple(c.task_families)) for c in result.candidates]
    assert patterns(result_r1) == patterns(result_r3)
    assert candidates(result_r1) == candidates(result_r3)


def test_provenance_hashes_must_be_sha256_and_trial_stays_within_cap():
    with pytest.raises(ValueError, match="lowercase SHA-256"):
        adapt_successful_candidate(
            representation=Representation.R1, operation="identity", task_id="t", candidate_id="c",
            grammar_hash="not-a-hash", implementation_hash=HASH_B, trial_index=1,
        )
    with pytest.raises(ValueError, match="trial_index"):
        adapt_successful_candidate(
            representation=Representation.R1, operation="identity", task_id="t", candidate_id="c",
            grammar_hash=HASH_A, implementation_hash=HASH_B, trial_index=11,
        )


def test_mapping_table_is_copy_and_uses_only_registered_grammars():
    mapping = operation_mapping_table()
    assert mapping["R1"]["translate_constant"] == "translate"
    assert mapping["R3"]["move"] == "translate"
    assert mapping["R1"]["reflect_horizontal"] == "flip_left_right"
    assert mapping["R3"]["reflect_horizontal_axis"] == "flip_top_bottom"
    mapping["R1"].clear()
    assert operation_mapping_table()["R1"]["identity"] == "identity"
