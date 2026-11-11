"""Capability Utility (CapU) components."""

from capability import Capability, CapabilityConfig, compute_capability_utility
from core import Skill, SkillState
from skills import SkillLibrary


def test_capu_weighted_components():
    lib = SkillLibrary()
    lib.add(
        Skill(
            skill_id="reflect",
            state=SkillState.ACTIVE,
            utility=0.8,
            transfer_score=0.6,
            transfer_history=[{"target_family": "geo", "success": True}],
            metadata={
                "mvp_category": "reflection",
                "utility_breakdown": {"su": 0.8},
                "composed_from": ["a", "b"],
            },
        )
    )
    lib.add(
        Skill(
            skill_id="rotate",
            state=SkillState.ACTIVE,
            utility=0.4,
            transfer_score=0.2,
            transfer_history=[{"target_family": "geo", "success": True}],
            metadata={
                "mvp_category": "rotation",
                "utility_breakdown": {"su": 0.4},
            },
        )
    )
    cap = Capability(capability_id="geo", skill_ids=["reflect", "rotate"])
    cfg = CapabilityConfig(
        ccov_family_norm=5,
        capu_w_su=0.4,
        capu_w_ts=0.25,
        capu_w_cov=0.2,
        capu_w_comp=0.15,
    )
    bd = compute_capability_utility(cap, lib, cfg, total_families=5)
    assert abs(bd.mean_su - 0.6) < 1e-9
    assert abs(bd.mean_ts - 0.4) < 1e-9
    assert bd.composition_bonus == 0.5  # 1 of 2 composed
    # CCov: geo + cat:reflection + cat:rotation = 3/5
    assert abs(bd.coverage - 0.6) < 1e-9
    expected = 0.4 * 0.6 + 0.25 * 0.4 + 0.2 * 0.6 + 0.15 * 0.5
    assert abs(bd.capu - expected) < 1e-9
    assert "capu_breakdown" in cap.metadata
