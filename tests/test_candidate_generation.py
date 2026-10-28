"""Tests for Phase 11C-2 Stage 6 — candidate generation."""

from core import InvariantState, InvariantType
from invariants import (
    AggregatedStructure,
    InvariantIdentity,
    MinedPattern,
    generate_candidates,
)


def _structure(
    sig,
    *,
    structure_id="S1",
    freq=5,
    families=None,
    variant_sigs=None,
    occurrences=None,
):
    families = families or ["reflection", "counting"]
    rep = MinedPattern(
        pattern_id="P1",
        signature=tuple(sig),
        frequency=freq,
        occurrences=occurrences or freq,
        trace_ids=[f"tr{i}" for i in range(freq)],
        success_count=freq,
        failure_count=0,
        task_families=list(families),
        coverage=0.8,
    )
    variants = [rep]
    if variant_sigs:
        for i, vsig in enumerate(variant_sigs, start=2):
            variants.append(
                MinedPattern(
                    pattern_id=f"P{i}",
                    signature=tuple(vsig),
                    frequency=max(freq - 1, 1),
                    occurrences=max(freq - 1, 1),
                    trace_ids=[f"tr{i}" for i in range(max(freq - 1, 1))],
                    success_count=max(freq - 1, 1),
                    failure_count=0,
                    task_families=list(families),
                    coverage=0.5,
                )
            )
    return AggregatedStructure(
        structure_id=structure_id,
        core=tuple(sig[:2]) if len(sig) >= 2 else tuple(sig),
        representative=rep,
        variants=variants,
        frequency=freq,
        task_families=list(families),
        success_count=freq,
        failure_count=0,
        occurrences=occurrences or freq * len(variants),
    )


def test_candidate_field_mapping():
    result = generate_candidates(
        [_structure(("find_symmetry", "apply_reflection"), freq=5)],
        total_families=4,
        apply_rejections=False,
    )
    assert len(result.candidates) == 1
    inv = result.candidates[0]
    assert inv.state is InvariantState.CANDIDATE
    assert inv.frequency == 5
    assert inv.consistency == 1.0  # representative freq / structure freq
    assert inv.generality == 0.5  # 2 families / 4
    assert inv.evidence.transfer_events == 0
    assert inv.origin == "trace_mining"
    assert inv.pattern_signature == ["find_symmetry", "apply_reflection"]


def test_type_classification_and_confidence():
    result = generate_candidates(
        [_structure(("find_symmetry", "apply_reflection"), families=["reflection"])],
        total_families=2,
        apply_rejections=False,
    )
    inv = result.candidates[0]
    assert inv.invariant_type is InvariantType.PROCEDURAL
    assert inv.confidence is not None


def test_identity_determinism():
    s = _structure(("find_symmetry", "apply_reflection"))
    a = generate_candidates([s], total_families=2, apply_rejections=False).candidates[0]
    b = generate_candidates([s], total_families=2, apply_rejections=False).candidates[0]
    assert a.invariant_id == b.invariant_id
    expected = InvariantIdentity(
        origin="trace_mining",
        pattern_signature=("find_symmetry", "apply_reflection"),
        task_families=("counting", "reflection"),
    ).invariant_id
    assert a.invariant_id == expected


def test_rejection_filtering_recorded():
    # Rare / low frequency structure should hit rare_event when frequency < policy
    rare = _structure(("find_symmetry", "apply_reflection"), freq=1, families=["reflection"])
    rare.frequency = 1
    rare.representative.frequency = 1
    result = generate_candidates([rare], total_families=1, apply_rejections=True)
    assert result.candidates == []
    assert len(result.rejected) == 1
    assert "rare_event" in result.rejected[0][1]


def test_metadata_carries_structure_info():
    result = generate_candidates(
        [_structure(("find_symmetry", "apply_reflection"), structure_id="S9")],
        total_families=2,
        apply_rejections=False,
    )
    meta = result.candidates[0].metadata
    assert meta["structure_id"] == "S9"
    assert meta["pattern_id"] == "P1"
    assert "variant_signatures" in meta
