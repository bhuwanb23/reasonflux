"""End-to-end tests for Phase 11C-2 TraceMiner orchestration."""

from core import ReasoningStep, ReasoningTrace, TraceOutcome
from invariants import (
    InvariantDetector,
    MiningConfig,
    TraceMiner,
)


def _make_trace(
    trace_id,
    operations,
    *,
    family,
    success=True,
    task_id=None,
):
    steps = [
        ReasoningStep(step_id=f"{trace_id}-s{i}", operation=op)
        for i, op in enumerate(operations, start=1)
    ]
    return ReasoningTrace(
        trace_id=trace_id,
        task_id=task_id or trace_id,
        timestamp=1.0,
        steps=steps,
        outcome=TraceOutcome(success=success),
        metadata={"task_family": family},
    )


REFLECTION_OPS = ["DetectObject", "FindSymmetry", "ApplyReflection", "VerifyOutput"]
ROTATION_OPS = ["DetectObject", "FindRotation", "ApplyRotation", "VerifyOutput"]
# Synonym variant of reflection (Stage 2 example)
REFLECTION_VARIANT = ["LocateObject", "FindMirrorAxis", "Reflect", "Verify"]


def _doc_corpus():
    """Build a corpus matching Phase 11C-2 examples, with enough support."""
    traces = []
    # Reflection traces 1-3 (+ variants to meet min_frequency with mining)
    for i in range(1, 4):
        traces.append(
            _make_trace(f"ref{i}", REFLECTION_OPS, family="reflection")
        )
    traces.append(
        _make_trace("ref4", REFLECTION_VARIANT, family="reflection")
    )
    # Rotation traces (repeat to meet min_frequency=3)
    for i in range(1, 5):
        traces.append(
            _make_trace(f"rot{i}", ROTATION_OPS, family="rotation")
        )
    # One failure reflection-like trace
    traces.append(
        _make_trace(
            "fail1",
            ["DetectObject", "FindSymmetry", "ApplyReflection", "VerifyOutput"],
            family="reflection",
            success=False,
        )
    )
    return traces


def test_end_to_end_reflection_and_rotation_emerge():
    miner = TraceMiner(MiningConfig(min_frequency=3, min_cross_trace=2))
    result = miner.mine(_doc_corpus())

    assert result.statistics.traces_in == 9
    assert result.statistics.traces_success == 8
    assert result.statistics.traces_failure == 1
    assert result.statistics.candidates >= 1

    # Reflection and rotation patterns should appear in success_patterns
    success_sigs = {p.signature for p in result.success_patterns}
    assert ("find_symmetry", "apply_reflection") in success_sigs
    assert ("find_rotation", "apply_rotation") in success_sigs

    # Structures / candidates should distinguish reflection vs rotation
    cores = {s.core for s in result.structures}
    assert any("apply_reflection" in c for c in cores)
    assert any("apply_rotation" in c for c in cores)

    candidate_ops = {
        tuple(c.pattern_signature) for c in result.candidates
    }
    # At least one reflection-like and one rotation-like candidate (or their cores)
    has_reflection = any("apply_reflection" in sig for sig in candidate_ops)
    has_rotation = any("apply_rotation" in sig for sig in candidate_ops)
    # Rejection may filter some; structures should still distinguish
    assert has_reflection or any("apply_reflection" in c for c in cores)
    assert has_rotation or any("apply_rotation" in c for c in cores)


def test_failure_traces_retained_separately():
    miner = TraceMiner(MiningConfig(min_frequency=1, min_cross_trace=1))
    # Two identical failures so they meet min_cross_trace=1 with frequency 1...
    # Use min_frequency=1 to surface failure patterns.
    traces = [
        _make_trace("f1", REFLECTION_OPS, family="reflection", success=False),
        _make_trace("f2", REFLECTION_OPS, family="reflection", success=False),
        _make_trace("f3", REFLECTION_OPS, family="reflection", success=False),
        _make_trace("s1", REFLECTION_OPS, family="reflection", success=True),
        _make_trace("s2", REFLECTION_OPS, family="reflection", success=True),
        _make_trace("s3", REFLECTION_OPS, family="reflection", success=True),
    ]
    result = miner.mine(traces)
    assert result.statistics.traces_failure == 3
    assert result.failure_patterns  # failure mining retained
    assert result.success_patterns


def test_statistics_counts_consistent():
    result = TraceMiner().mine(_doc_corpus())
    stats = result.statistics
    assert stats.traces_success + stats.traces_failure == stats.traces_in
    assert stats.structures == len(result.structures)
    assert stats.candidates == len(result.candidates)
    assert stats.rejected == len(result.rejected)
    assert stats.raw_patterns == len(result.success_patterns) + len(result.failure_patterns)


def test_trace_batch_provider_input():
    class Provider:
        def get_traces(self):
            return _doc_corpus()

    result = TraceMiner(MiningConfig(min_frequency=3)).mine(Provider())
    assert result.statistics.traces_in == 9


def test_invariant_detector_detect_returns_candidates():
    detector = InvariantDetector(MiningConfig(min_frequency=3))
    candidates = detector.detect(_doc_corpus())
    assert isinstance(candidates, list)
    full = detector.mine(_doc_corpus())
    assert len(candidates) == len(full.candidates)


def test_normalization_unifies_synonym_variants_in_mining():
    traces = [
        _make_trace("a", REFLECTION_OPS, family="reflection"),
        _make_trace("b", REFLECTION_VARIANT, family="reflection"),
        _make_trace("c", REFLECTION_OPS, family="reflection"),
    ]
    result = TraceMiner(MiningConfig(min_frequency=3, min_cross_trace=2)).mine(traces)
    # After normalization, reflection pair should hit frequency 3
    sigs = {p.signature for p in result.success_patterns}
    assert ("find_symmetry", "apply_reflection") in sigs
