"""Evidence, confidence, and NCR."""

from skills import SkillConfig
from skills.composition.evaluate import (
    compute_composition_confidence,
    record_composition_outcome,
)
from skills.composition.models import CompositionCandidate


def test_outcome_updates_evidence_confidence_ncr():
    cand = CompositionCandidate(
        composition_id="a+b",
        skill_ids=["a", "b"],
        expected_utility=0.5,
        expected_transfer=0.4,
        composition_cost=0.1,
    )
    cfg = SkillConfig()
    record_composition_outcome(
        cand,
        success=True,
        transfer_gain=0.3,
        reasoning_reduction=0.2,
        task_family="fam1",
        config=cfg,
    )
    assert cand.evidence["uses"] == 1
    assert cand.evidence["successes"] == 1
    assert cand.confidence == compute_composition_confidence(cand)
    assert cand.ncr == 0.0

    record_composition_outcome(
        cand, success=False, task_family="fam2", config=cfg
    )
    assert cand.evidence["failures"] == 1
    assert cand.ncr == 0.5
    assert cand.metadata.get("ncr") == 0.5
