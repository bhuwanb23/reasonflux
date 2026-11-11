"""Tests for Phase 11C-2 Stage 3 — trace segmentation."""

import pytest

from traces import TraceFragment, segment_trace, segment_traces
from traces.normalizer import NormalizedTrace


def test_ngrams_cover_lengths_and_order():
    frags = segment_trace(
        ["detect_object", "find_symmetry", "apply_reflection", "verify_output"],
        max_length=3,
        min_length=1,
        dedupe=True,
    )
    sigs = [f.signature for f in frags]
    assert ("detect_object",) in sigs
    assert ("find_symmetry", "apply_reflection") in sigs
    assert ("detect_object", "find_symmetry", "apply_reflection") in sigs
    assert all(1 <= f.length <= 3 for f in frags)
    first = next(f for f in frags if f.length == 1)
    assert first.source_index == 0


def test_max_length_bound():
    frags = segment_trace(["a", "b", "c", "d", "e"], max_length=2)
    assert max(f.length for f in frags) == 2


def test_per_trace_dedupe():
    frags = segment_trace(["a", "a", "a"], max_length=2, dedupe=True)
    assert len([f for f in frags if f.signature == ("a",)]) == 1
    assert len([f for f in frags if f.signature == ("a", "a")]) == 1


def test_empty_and_single_step():
    assert segment_trace([]) == []
    single = segment_trace(["only"], max_length=4)
    assert len(single) == 1
    assert single[0].signature == ("only",)


def test_invalid_bounds_raise():
    with pytest.raises(ValueError):
        segment_trace(["a"], max_length=0)
    with pytest.raises(ValueError):
        segment_trace(["a"], min_length=3, max_length=2)


def test_segment_traces_attaches_owner_metadata():
    traces = [
        NormalizedTrace(
            trace_id="tr1",
            task_id="t1",
            task_family="reflection",
            operations=["find_symmetry", "apply_reflection"],
            success=True,
        )
    ]
    frags = segment_traces(traces, max_length=2)
    assert all(f.trace_id == "tr1" for f in frags)
    assert all(f.task_family == "reflection" for f in frags)
    assert isinstance(frags[0], TraceFragment)
