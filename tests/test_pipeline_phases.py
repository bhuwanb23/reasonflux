"""Phase pipelines: A (traces) → B (invariants) → C (skills)."""

from __future__ import annotations

import pytest

from core.states import InvariantState, SkillState
from evaluation.invariant_metrics import compute_is, mean_is, summarize_is
from invariants.strength import compute_invariant_strength
from pipelines.invariant_pipeline import run_invariant_pipeline
from pipelines.skill_pipeline import run_skill_pipeline
from pipelines.trace_pipeline import run_trace_pipeline
from traces.trace_store import TraceStore


def test_trace_pipeline_produces_and_persists(tmp_path):
    result = run_trace_pipeline(per_family=3, seed=0, store_root=tmp_path)
    assert result.n_traces == 12
    assert result.success_count + result.failure_count == result.n_traces
    assert result.success_count > 0
    store = TraceStore(tmp_path)
    assert store.count() == result.n_traces
    assert len(store.load_all()) == result.n_traces


def test_trace_pipeline_can_skip_persistence():
    result = run_trace_pipeline(per_family=2, seed=0, persist=False)
    assert result.n_traces == 8
    assert result.store_root == ""


def test_invariant_pipeline_finds_shared_structure():
    trace_run = run_trace_pipeline(per_family=6, seed=0, persist=False)
    result = run_invariant_pipeline(trace_run.traces)
    assert result.n_traces == 24
    assert result.candidates
    signatures = {tuple(inv.pattern_signature) for inv in result.candidates}
    assert any("apply_reflection" in sig for sig in signatures)
    assert any("apply_rotation" in sig for sig in signatures)


def test_invariant_pipeline_handles_empty_input():
    result = run_invariant_pipeline([])
    assert result.n_traces == 0
    assert result.candidates == []


def test_invariant_pipeline_accepts_a_store(tmp_path):
    trace_run = run_trace_pipeline(per_family=4, seed=0, store_root=tmp_path)
    result = run_invariant_pipeline(TraceStore(tmp_path))
    assert result.n_traces == len(trace_run.traces)
    assert result.candidates


def test_priors_are_trace_derived_and_bounded():
    trace_run = run_trace_pipeline(per_family=6, seed=0, persist=False)
    result = run_invariant_pipeline(trace_run.traces)
    for inv in result.validation.validated:
        meta = inv.metadata or {}
        assert 0.0 <= float(meta["reasoning_value"]) <= 1.0
        assert 0.0 <= float(inv.transfer_contribution) <= 1.0
        assert meta.get("transfer_verified") is False


def test_prior_never_overwrites_measured_transfer():
    from invariants.sct_priors import attach_sct_priors

    trace_run = run_trace_pipeline(per_family=4, seed=0, persist=False)
    result = run_invariant_pipeline(trace_run.traces)
    inv = result.validation.validated[0]
    inv.transfer_contribution = 0.9
    attach_sct_priors([inv], mean_trace_length=4.0, n_families=4)
    assert inv.transfer_contribution == pytest.approx(0.9)


def test_promotable_invariants_reach_sct_state():
    trace_run = run_trace_pipeline(per_family=6, seed=0, persist=False)
    result = run_invariant_pipeline(trace_run.traces)
    for inv in result.promotable:
        assert inv.state is InvariantState.SKILL_CANDIDATE


def test_skill_pipeline_promotes_and_rejects():
    trace_run = run_trace_pipeline(per_family=6, seed=0, persist=False)
    inv_run = run_invariant_pipeline(trace_run.traces)
    skill_run = run_skill_pipeline(inv_run.promotable)
    assert skill_run.promoted
    for skill in skill_run.promoted:
        assert skill.state is SkillState.ACTIVE
        assert skill.trigger_conditions
    assert len(skill_run.library) == len(skill_run.promoted)


def test_skill_pipeline_accumulates_into_existing_library():
    trace_run = run_trace_pipeline(per_family=6, seed=0, persist=False)
    inv_run = run_invariant_pipeline(trace_run.traces)
    first = run_skill_pipeline(inv_run.promotable)
    size = len(first.library)
    second = run_skill_pipeline(inv_run.promotable, library=first.library)
    assert len(second.library) >= size
    # Re-promoting the same invariants must not duplicate skills.
    assert len(second.library) == size


def test_compute_is_matches_single_formula():
    trace_run = run_trace_pipeline(per_family=4, seed=0, persist=False)
    inv_run = run_invariant_pipeline(trace_run.traces)
    inv = inv_run.candidates[0]
    assert compute_is(inv) == pytest.approx(
        compute_invariant_strength(
            float(inv.frequency), float(inv.consistency), float(inv.generality)
        )
    )
    assert mean_is([inv]) == pytest.approx(compute_is(inv))
    summary = summarize_is([inv])
    assert summary["n"] == 1.0
    assert summary["max"] == pytest.approx(compute_is(inv))
