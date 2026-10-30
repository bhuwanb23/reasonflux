"""Capability validity constraints."""

from capability import Capability, CapabilityConfig, validate_capability
from core import Skill, SkillState
from skills import SkillLibrary


def test_empty_and_no_transfer_rejected():
    lib = SkillLibrary()
    empty = Capability(capability_id="empty", skill_ids=[])
    cfg = CapabilityConfig(min_skills=1, min_transfer_events=1)
    r1 = validate_capability(empty, lib, cfg)
    assert not r1.valid
    assert "min_skills" in r1.reasons

    lib.add(
        Skill(
            skill_id="lonely",
            state=SkillState.ACTIVE,
            utility=0.4,
            metadata={"utility_breakdown": {"su": 0.4}},
        )
    )
    no_xfer = Capability(capability_id="ghost", skill_ids=["lonely"])
    r2 = validate_capability(no_xfer, lib, cfg)
    assert not r2.valid
    assert "transfer" in r2.reasons


def test_valid_with_transfer():
    lib = SkillLibrary()
    lib.add(
        Skill(
            skill_id="ok",
            state=SkillState.ACTIVE,
            utility=0.4,
            transfer_history=[{"target_family": "geo", "success": True}],
            metadata={"utility_breakdown": {"su": 0.4}, "mvp_category": "geo"},
        )
    )
    cap = Capability(capability_id="ok-cap", skill_ids=["ok"])
    r = validate_capability(cap, lib, CapabilityConfig())
    assert r.valid
