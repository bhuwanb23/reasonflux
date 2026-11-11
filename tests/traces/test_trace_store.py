"""Trace producer, persistence, similarity, and clustering."""

from __future__ import annotations

import pytest

from core.states import TraceLifecyclePhase
from invariants.cluster import cluster_traces
from solver import GridSolver, make_task
from traces.logger import TraceLogger
from traces.trace_similarity import sequence_similarity, trace_similarity
from traces.trace_store import TraceStore


def _trace(family: str, seed: int = 0, *, difficulty: float = 0.2):
    solver = GridSolver()
    task = make_task(family, seed=seed, difficulty=difficulty)
    return TraceLogger(clock=lambda: 1.0).log(task.to_task(), solver.solve(task))


def test_logger_builds_a_complete_trace():
    trace = _trace("reflection")
    assert trace.steps
    assert trace.outcome is not None
    assert trace.outcome.success is True
    assert trace.metadata["task_family"] == "reflection"
    assert trace.phase is TraceLifecyclePhase.STORED
    assert trace.total_cost > 0


def test_logger_records_failures_too():
    solver = GridSolver()
    task = make_task("reflection", seed=0, difficulty=0.9)
    trace = TraceLogger().log(task.to_task(), solver.solve(task))
    assert trace.outcome is not None
    assert trace.outcome.success is False


def test_store_round_trip_preserves_trace(tmp_path):
    trace = _trace("rotation", seed=2)
    store = TraceStore(tmp_path)
    store.save(trace)
    loaded = store.load(trace.trace_id, family="rotation")
    assert loaded.trace_id == trace.trace_id
    assert loaded.operations == trace.operations
    assert loaded.outcome is not None
    assert loaded.outcome.success == trace.outcome.success


def test_store_lists_by_family_and_all(tmp_path):
    store = TraceStore(tmp_path)
    store.save_many([_trace("reflection", s) for s in range(2)])
    store.save_many([_trace("counting", s) for s in range(3)])
    assert len(store.list_by_family("reflection")) == 2
    assert len(store.list_by_family("counting")) == 3
    assert len(store.list_by_family("absent")) == 0
    assert store.count() == 5
    assert len(store.load_all()) == 5
    assert store.families() == ["counting", "reflection"]


def test_store_missing_trace_raises(tmp_path):
    store = TraceStore(tmp_path)
    with pytest.raises(FileNotFoundError):
        store.load("nope")


def test_identical_traces_have_similarity_one():
    a = _trace("reflection", seed=1)
    assert trace_similarity(a, a) == pytest.approx(1.0)
    assert sequence_similarity(a, a) == pytest.approx(1.0)


def test_disjoint_families_are_less_similar():
    refl = _trace("reflection", seed=1)
    cnt = _trace("counting", seed=1)
    same = trace_similarity(refl, _trace("reflection", seed=2))
    cross = trace_similarity(refl, cnt)
    assert cross < same


def test_clustering_keeps_distinct_mechanisms_apart():
    """Reflection and rotation are distinct mechanisms; counting/grouping share
    a reduction prefix and legitimately cluster closer (measured ~0.7)."""
    traces = [
        _trace(family, seed=s)
        for family in ("reflection", "rotation", "counting", "grouping")
        for s in range(3)
    ]
    clusters = cluster_traces(traces, threshold=0.85)
    by_family: dict[str, set[str]] = {}
    for cluster in clusters:
        for family in cluster.families:
            by_family.setdefault(family, set()).add(cluster.cluster_id)
    # Reflection and rotation never share a cluster with each other.
    assert by_family["reflection"].isdisjoint(by_family["rotation"])
    covered = set(by_family)
    assert covered == {"reflection", "rotation", "counting", "grouping"}


def test_similarity_separates_mechanisms():
    refl = _trace("reflection", seed=0)
    rot = _trace("rotation", seed=0)
    cnt = _trace("counting", seed=0)
    grp = _trace("grouping", seed=0)
    assert trace_similarity(refl, refl) == pytest.approx(1.0)
    # Distinct mechanisms are clearly further apart than shared-prefix families.
    assert trace_similarity(refl, rot) < trace_similarity(cnt, grp)


def test_cluster_threshold_validates():
    with pytest.raises(ValueError):
        cluster_traces([_trace("reflection")], threshold=1.5)
