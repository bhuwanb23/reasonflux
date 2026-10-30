"""Strength vs confidence independence."""

from capability import (
    Capability,
    CapabilityConfig,
    compute_confidence,
    compute_strength,
    seed_from_skills,
)
from core import Skill, SkillState
from skills import SkillLibrary


def test_strength_vs_confidence_independence():
    lib = SkillLibrary()
    lib.add(
        Skill(
            skill_id="s1",
            state=SkillState.ACTIVE,
            reuse_count=8,
            transfer_score=0.9,
            utility=0.9,
            transfer_history=[{"target_family": "geo", "success": True}],
            metadata={"utility_breakdown": {"su": 0.9}, "mvp_category": "geo"},
        )
    )
    cap = Capability(
        capability_id="c1",
        skill_ids=["s1"],
        utility_history=[{"utility": 0.5}, {"utility": 0.51}],
    )
    seed_from_skills(cap, lib)
    cfg = CapabilityConfig()
    strength = compute_strength(cap, lib, cfg)
    confidence = compute_confidence(cap, lib, cfg)
    assert 0.0 <= strength <= 1.0
    assert 0.0 <= confidence <= 1.0

    # CapU high but no transfer evidence on a second ghost-like cap:
    ghost = Capability(
        capability_id="g",
        skill_ids=["s1"],
        utility=0.95,
        utility_history=[{"utility": 0.95}],
    )
    # Clear evidence and membership transfer count via empty evidence buckets.
    ghost.evidence = {"skills": [], "transfer": [], "utility": [], "growth": []}
    ghost.transfer_history = []
    # Confidence still reads skill transfer_history from library members.
    conf_with_skill_transfer = compute_confidence(ghost, lib, cfg)
    assert conf_with_skill_transfer > 0

    empty_lib = SkillLibrary()
    conf_no_skills = compute_confidence(
        Capability(capability_id="empty", skill_ids=[], utility=0.99),
        empty_lib,
        cfg,
    )
    # Confidence independent of CapU: empty membership → low confidence despite high CapU
    # on a different object; empty skill_ids → evidence_score uses max(1,0)=1 → 0.
    assert conf_no_skills < 0.2
