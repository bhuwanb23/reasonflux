"""F5 sparse evidence."""

from core import Invariant, InvariantEvidence, InvariantState
from invariants.robustness import RobustnessConfig, evaluate_hard_gate
from invariants.validation import ValidationScores


def _scores():
    return ValidationScores(
        frequency=0.8,
        consistency=0.9,
        generality=0.5,
        transfer=0.7,
        reasoning_value=0.6,
        pass_frequency=True,
        pass_consistency=True,
        pass_generality=True,
        pass_transfer=True,
        pass_reasoning=True,
    )


def test_below_min_evidence_not_promotable():
    inv = Invariant(
        invariant_id="INV-r",
        pattern_signature=["reflect"],
        frequency=10,
        consistency=0.9,
        generality=0.5,
        state=InvariantState.VALIDATED,
        task_families=["a", "b"],
        evidence=InvariantEvidence(observations=2),
    )
    result = evaluate_hard_gate(inv, _scores(), robustness_config=RobustnessConfig())
    assert not result.promotable
    assert "insufficient_evidence" in result.reasons
