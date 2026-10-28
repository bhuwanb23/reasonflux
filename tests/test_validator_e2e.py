"""End-to-end mine → validate: high-value promotable set."""

from core import (
    Invariant,
    InvariantEvidence,
    InvariantState,
    ReasoningStep,
    ReasoningTrace,
    TraceOutcome,
)
from invariants import (
    InvariantDetector,
    MiningConfig,
    ValidationConfig,
    validate_and_rank,
)


def _trace(tid, ops, family, success=True):
    steps = [
        ReasoningStep(step_id=f"{tid}-{i}", operation=op)
        for i, op in enumerate(ops, start=1)
    ]
    return ReasoningTrace(
        trace_id=tid,
        task_id=tid,
        timestamp=1.0,
        steps=steps,
        outcome=TraceOutcome(success=success),
        metadata={"task_family": family},
    )


def test_validate_and_rank_promotes_high_value_only():
    reflection = Invariant(
        invariant_id="INV-ref",
        pattern_signature=["find_symmetry", "apply_reflection"],
        frequency=12,
        consistency=0.91,
        generality=0.78,
        transfer_contribution=0.72,
        evidence=InvariantEvidence(
            observations=12, transfer_events=3, task_families=["reflection", "counting"]
        ),
        state=InvariantState.CANDIDATE,
        metadata={"reasoning_value": 0.67},
    )
    verify = Invariant(
        invariant_id="INV-ver",
        pattern_signature=["verify_output"],
        frequency=40,
        consistency=1.0,
        generality=1.0,
        transfer_contribution=0.0,
        evidence=InvariantEvidence(observations=40, transfer_events=0),
        state=InvariantState.CANDIDATE,
        metadata={},
    )
    noise = Invariant(
        invariant_id="INV-noise",
        pattern_signature=["reflect:blue_triangle"],
        frequency=8,
        consistency=0.9,
        generality=0.5,
        transfer_contribution=0.5,
        state=InvariantState.CANDIDATE,
        metadata={"reasoning_value": 0.5, "failed_variations": ["color"]},
    )

    result = validate_and_rank(
        [reflection, verify, noise],
        config=ValidationConfig(),
    )
    promotable_ids = {i.invariant_id for i in result.promotable}
    assert "INV-ref" in promotable_ids
    assert "INV-ver" not in promotable_ids
    assert "INV-noise" not in promotable_ids
    assert result.statistics.promotable >= 1
    assert result.statistics.promotable < result.statistics.candidates_in


def test_detector_detect_and_validate():
    reflection_ops = ["DetectObject", "FindSymmetry", "ApplyReflection", "VerifyOutput"]
    traces = [
        _trace(f"r{i}", reflection_ops, "reflection") for i in range(1, 5)
    ]
    # Inject transfer/reasoning via validate transfer_scores after mining
    detector = InvariantDetector(
        MiningConfig(min_frequency=3, min_cross_trace=2),
        validation_config=ValidationConfig(min_r=0.0, min_t=0.0),
    )
    mining = detector.mine(traces)
    # Annotate candidates with reasoning_value so R gate can pass when enabled
    for cand in mining.candidates:
        cand.metadata["reasoning_value"] = 0.5
        cand.transfer_contribution = 0.5
        cand.evidence.transfer_events = 2
    result = detector.validate(mining.candidates)
    assert result.statistics.candidates_in == len(mining.candidates)
    assert result.ranked
