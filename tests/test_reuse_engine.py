"""Reuse engine: transfer is measured, not asserted."""

from __future__ import annotations

import pytest

from baselines.skill_storage.run import run as skill_storage_run
from core.states import SkillState
from pipelines.invariant_pipeline import run_invariant_pipeline
from pipelines.skill_pipeline import run_skill_pipeline
from pipelines.trace_pipeline import run_trace_pipeline
from skills.library import SkillLibrary
from solver import make_task, make_task_batch
from transfer.reuse_engine import ReuseEngine


@pytest.fixture(scope="module")
def learned_library() -> SkillLibrary:
    trace_run = run_trace_pipeline(per_family=6, seed=0, persist=False)
    inv_run = run_invariant_pipeline(trace_run.traces)
    return run_skill_pipeline(inv_run.promotable).library


def test_reuse_collapses_steps_and_credits_transfer(learned_library):
    engine = ReuseEngine(learned_library)
    task = make_task("rotation", seed=10, difficulty=0.2)
    result = engine.apply(task)
    assert result.applied
    assert result.success
    assert result.reused_cost < result.baseline_cost
    assert result.reasoning_reduction > 0
    assert result.transfer_credit is True
    assert engine.memory.all_records()


def test_incorrect_reuse_earns_no_credit(learned_library):
    """A cheaper but wrong run must not be recorded as transfer."""
    engine = ReuseEngine(learned_library)
    # Ambiguous rotations are mis-resolved, so reuse of rotation is wrong.
    failures = [
        engine.apply(make_task("rotation", seed=s, difficulty=0.9)) for s in range(6)
    ]
    for result in failures:
        if not result.success:
            assert result.transfer_credit is False


def test_empty_library_never_fabricates_reduction():
    engine = ReuseEngine(SkillLibrary())
    result = engine.apply(make_task("reflection", seed=1, difficulty=0.2))
    assert result.applied is False
    assert result.reasoning_reduction == 0.0
    assert result.benefit == 0.0
    assert result.reused_cost == result.baseline_cost
    assert not engine.memory.all_records()


def test_symmetry_less_skill_never_applied():
    """A reflection skill cannot serve an asymmetric grid."""
    lib = SkillLibrary()
    from baselines._common import make_skill

    lib.add(
        make_skill(
            "refl",
            category="reflection",
            triggers=["detect_object", "find_symmetry", "apply_reflection"],
        )
    )
    engine = ReuseEngine(lib)
    task = make_task("counting", seed=0, difficulty=0.2, variant=0)
    # Variant 0 counting grids are asymmetric, so the invariance does not hold.
    if not any(row == tuple(reversed(row)) for row in task.input_grid.cells):
        assert engine.retrieve(task) is None


def test_batch_measures_every_task(learned_library):
    engine = ReuseEngine(learned_library)
    batch = make_task_batch(seed=100, per_family=2, difficulty=0.2)
    results = engine.apply_batch(batch)
    assert len(results) == len(batch)
    assert sum(1 for r in results if r.transfer_credit) > 0
    assert all(r.baseline_cost >= 0 for r in results)


def test_reuse_updates_skill_monitoring(learned_library):
    engine = ReuseEngine(learned_library)
    task = make_task("reflection", seed=4, difficulty=0.2)
    before = sum(int(s.reuse_count) for s in learned_library.list_skills())
    result = engine.apply(task)
    after = sum(int(s.reuse_count) for s in learned_library.list_skills())
    if result.applied:
        assert after > before


def test_skill_storage_baseline_uses_same_instrument():
    """Baseline B shares the measurement path, so numbers are comparable."""
    out = skill_storage_run(per_family=4)
    assert out["name"] == "skill_storage"
    assert "capability_score" in out
    assert out["n_skills"] >= 1
