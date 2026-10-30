"""Propose capabilities from anchors / categories / composition candidates."""

from capability import (
    CapabilityType,
    propose_capabilities_from_library,
)
from core import Skill, SkillState
from skills import SkillLibrary


def _xfer(fam="geo"):
    return [{"target_family": fam, "success": True}]


def test_propose_atomic_composite_emergent():
    lib = SkillLibrary()
    lib.add(
        Skill(
            skill_id="anchor",
            state=SkillState.CORE,
            utility=0.6,
            transfer_score=0.5,
            transfer_history=_xfer(),
            metadata={
                "mvp_category": "reflection",
                "utility_breakdown": {"su": 0.6},
                "capability_anchor": True,
            },
        )
    )
    lib.add(
        Skill(
            skill_id="reflect-a",
            state=SkillState.ACTIVE,
            utility=0.5,
            transfer_score=0.4,
            transfer_history=_xfer("geo"),
            metadata={
                "mvp_category": "reflection",
                "utility_breakdown": {"su": 0.5},
            },
        )
    )
    lib.add(
        Skill(
            skill_id="reflect-b",
            state=SkillState.ACTIVE,
            utility=0.5,
            transfer_score=0.4,
            transfer_history=_xfer("algebra"),
            metadata={
                "mvp_category": "reflection",
                "utility_breakdown": {"su": 0.5},
            },
        )
    )
    lib.add(
        Skill(
            skill_id="comp-a",
            state=SkillState.ACTIVE,
            utility=0.5,
            transfer_history=_xfer(),
            metadata={
                "mvp_category": "rotation",
                "utility_breakdown": {"su": 0.5},
                "capability_candidate": True,
                "composed_from": ["x", "y"],
            },
        )
    )
    lib.add(
        Skill(
            skill_id="comp-b",
            state=SkillState.ACTIVE,
            utility=0.5,
            transfer_history=_xfer(),
            metadata={
                "mvp_category": "rotation",
                "utility_breakdown": {"su": 0.5},
                "capability_candidate": True,
            },
        )
    )

    proposed = propose_capabilities_from_library(lib, require_valid=True)
    types = {c.capability_type for c in proposed}
    assert CapabilityType.ATOMIC in types
    assert CapabilityType.COMPOSITE in types
    assert CapabilityType.EMERGENT in types
    assert CapabilityType.CROSS_DOMAIN in types
    assert any(c.capability_id.startswith("cap-atomic-") for c in proposed)
    assert any(c.capability_id == "cap-composite-reflection" for c in proposed)
