"""Tests for Phase 11C-2 Stage 5 — pattern aggregation."""

from invariants import (
    AggregatedStructure,
    MinedPattern,
    aggregate_patterns,
    longest_common_contiguous_subsequence,
    patterns_share_core,
)


def _pat(sig, *, pid="P1", freq=3, families=None, traces=None):
    return MinedPattern(
        pattern_id=pid,
        signature=tuple(sig),
        frequency=freq,
        occurrences=freq,
        trace_ids=traces or [f"tr{i}" for i in range(freq)],
        success_count=freq,
        failure_count=0,
        task_families=families or ["reflection"],
        coverage=0.5,
    )


def test_longest_common_contiguous_subsequence():
    assert longest_common_contiguous_subsequence(
        ("find_symmetry", "apply_reflection"),
        ("detect_object", "find_symmetry", "apply_reflection"),
    ) == ("find_symmetry", "apply_reflection")


def test_doc_abc_reflection_example_aggregates_to_one():
    # Pattern A / B / C from Phase 11C-2 Stage 5
    a = _pat(("find_symmetry", "apply_reflection"), pid="A", freq=5, traces=["t1", "t2", "t3", "t4", "t5"])
    b = _pat(
        ("detect_object", "find_symmetry", "apply_reflection"),
        pid="B",
        freq=4,
        traces=["t1", "t2", "t3", "t6"],
    )
    c = _pat(
        ("find_symmetry", "apply_reflection", "verify_output"),
        pid="C",
        freq=3,
        traces=["t1", "t2", "t7"],
    )
    structures = aggregate_patterns([a, b, c], min_core_length=2)
    assert len(structures) == 1
    assert isinstance(structures[0], AggregatedStructure)
    assert structures[0].core == ("find_symmetry", "apply_reflection")
    assert structures[0].representative.pattern_id == "A"  # highest frequency
    assert len(structures[0].variants) == 3


def test_rotation_stays_separate_from_reflection():
    reflection = _pat(("find_symmetry", "apply_reflection"), pid="R", freq=4)
    rotation = _pat(
        ("find_rotation", "apply_rotation"),
        pid="O",
        freq=4,
        families=["rotation"],
        traces=["r1", "r2", "r3", "r4"],
    )
    structures = aggregate_patterns([reflection, rotation], min_core_length=2)
    assert len(structures) == 2
    cores = {s.core for s in structures}
    assert ("find_symmetry", "apply_reflection") in cores
    assert ("find_rotation", "apply_rotation") in cores


def test_patterns_share_core_threshold():
    a = _pat(("find_symmetry", "apply_reflection"))
    b = _pat(("detect_object", "find_symmetry", "apply_reflection"))
    c = _pat(("find_rotation", "apply_rotation"))
    assert patterns_share_core(a, b, min_core_length=2)
    assert not patterns_share_core(a, c, min_core_length=2)


def test_no_over_merge_unrelated_families():
    counting = _pat(("count_objects", "verify_output"), pid="C", families=["counting"], traces=["c1", "c2", "c3"])
    reflection = _pat(("find_symmetry", "apply_reflection"), pid="R", traces=["r1", "r2", "r3"])
    structures = aggregate_patterns([counting, reflection], min_core_length=2)
    assert len(structures) == 2


def test_empty_input():
    assert aggregate_patterns([]) == []
