"""F4 compatibility matrix."""

from core import Invariant, InvariantEvidence
from invariants.robustness import CompatibilityMatrix, are_compatible, compatibility_score


def test_reflect_rotate_conflict():
    reflect = Invariant(
        invariant_id="a",
        pattern_signature=["apply_reflection"],
        frequency=10,
        evidence=InvariantEvidence(observations=10),
    )
    rotate = Invariant(
        invariant_id="b",
        pattern_signature=["apply_rotation"],
        frequency=10,
        evidence=InvariantEvidence(observations=10),
    )
    assert compatibility_score(reflect, rotate) < 0.5
    assert not are_compatible(reflect, rotate)


def test_matrix_register():
    m = CompatibilityMatrix()
    a = Invariant(
        invariant_id="a",
        pattern_signature=["step_a"],
        frequency=5,
        evidence=InvariantEvidence(observations=5),
    )
    b = Invariant(
        invariant_id="b",
        pattern_signature=["step_a", "step_b"],
        frequency=5,
        evidence=InvariantEvidence(observations=5),
    )
    s = m.register(a, b)
    assert m.score("a", "b") == s
