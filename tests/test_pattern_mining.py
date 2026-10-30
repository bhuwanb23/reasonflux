"""Tests for Phase 11C-2 Stage 4 — pattern extraction."""

import pytest

from invariants import extract_patterns, mine_patterns
from traces import TraceFragment


def _frag(sig, *, tid, family="reflection", success=True):
    return TraceFragment(
        signature=tuple(sig),
        source_index=0,
        trace_id=tid,
        task_id=tid,
        task_family=family,
        success=success,
    )


def test_frequency_and_cross_trace_constraints():
    # Appears in only one trace → rejected
    frags = [_frag(("a", "b"), tid="tr1"), _frag(("a", "b"), tid="tr1")]
    assert extract_patterns(frags, total_traces=1, min_frequency=2, min_cross_trace=2) == []

    # Appears in three traces → accepted
    frags = [
        _frag(("find_symmetry", "apply_reflection"), tid="tr1"),
        _frag(("find_symmetry", "apply_reflection"), tid="tr2"),
        _frag(("find_symmetry", "apply_reflection"), tid="tr3"),
    ]
    patterns = extract_patterns(frags, total_traces=3, min_frequency=3, min_cross_trace=2)
    assert len(patterns) == 1
    assert patterns[0].frequency == 3
    assert patterns[0].coverage == pytest.approx(1.0)


def test_success_vs_failure_counters():
    frags = [
        _frag(("x", "y"), tid="tr1", success=True),
        _frag(("x", "y"), tid="tr2", success=True),
        _frag(("x", "y"), tid="tr3", success=False),
    ]
    patterns = extract_patterns(frags, total_traces=3, min_frequency=2, min_cross_trace=2)
    assert patterns[0].success_count == 2
    assert patterns[0].failure_count == 1


def test_coverage_math():
    frags = [
        _frag(("a",), tid="tr1"),
        _frag(("a",), tid="tr2"),
        _frag(("b",), tid="tr3"),
    ]
    patterns = extract_patterns(frags, total_traces=4, min_frequency=2, min_cross_trace=2)
    assert patterns[0].signature == ("a",)
    assert patterns[0].coverage == pytest.approx(0.5)


def test_deterministic_ordering():
    frags = [
        _frag(("b", "c"), tid="tr1"),
        _frag(("b", "c"), tid="tr2"),
        _frag(("b", "c"), tid="tr3"),
        _frag(("a",), tid="tr1"),
        _frag(("a",), tid="tr2"),
        _frag(("a",), tid="tr3"),
        _frag(("a",), tid="tr4"),
    ]
    patterns = extract_patterns(frags, total_traces=4, min_frequency=2, min_cross_trace=2)
    # Higher frequency first
    assert patterns[0].signature == ("a",)
    assert patterns[0].frequency == 4


def test_mine_patterns_delegates():
    frags = [
        _frag(("p", "q"), tid="tr1"),
        _frag(("p", "q"), tid="tr2"),
        _frag(("p", "q"), tid="tr3"),
    ]
    assert mine_patterns(frags, total_traces=3, min_frequency=3) == extract_patterns(
        frags, total_traces=3, min_frequency=3
    )


def test_task_families_collected():
    frags = [
        _frag(("a", "b"), tid="tr1", family="reflection"),
        _frag(("a", "b"), tid="tr2", family="counting"),
        _frag(("a", "b"), tid="tr3", family="reflection"),
    ]
    patterns = extract_patterns(frags, total_traces=3, min_frequency=2, min_cross_trace=2)
    assert set(patterns[0].task_families) == {"reflection", "counting"}
