"""Capability evidence buckets and seed_from_skills."""

from capability import (
    Capability,
    CapabilityEvidence,
    append_growth_evidence,
    append_transfer_evidence,
    seed_from_skills,
)
from core import Skill, SkillState
from skills import SkillLibrary


def test_evidence_buckets_and_seed():
    lib = SkillLibrary()
    lib.add(
        Skill(
            skill_id="reflect",
            state=SkillState.ACTIVE,
            utility=0.5,
            transfer_score=0.4,
            transfer_history=[{"target_family": "geo", "success": True}],
            metadata={"mvp_category": "reflection"},
        )
    )
    cap = Capability(capability_id="c", skill_ids=["reflect"])
    ev = seed_from_skills(cap, lib)
    assert any(e["skill_id"] == "reflect" for e in ev.skills)
    assert len(ev.transfer) >= 1
    append_transfer_evidence(cap, target_family="algebra", success=True)
    append_growth_evidence(cap, delta=0.1)
    restored = CapabilityEvidence.from_dict(cap.evidence)
    assert len(restored.transfer) >= 2
    assert len(restored.growth) == 1
