"""RCG / TV / RV / NR / MC component math."""

import pytest

from core import Skill, SkillState
from skills import SkillConfig
from skills.utility_components import (
    compute_mc,
    compute_nr,
    compute_rcg,
    compute_rv,
    compute_tv,
)


def _skill(**kwargs):
    base = dict(
        skill_id="sk1",
        abstraction_gain=0.8,
        transfer_score=0.7,
        creation_cost=0.1,
        reuse_count=0,
        state=SkillState.ACTIVE,
        metadata={"mvp_category": "reflection"},
    )
    base.update(kwargs)
    return Skill(**base)


def test_rcg_from_abstraction_and_rc_delta():
    assert compute_rcg(_skill()) == pytest.approx(0.8)
    s = _skill(metadata={"rc_before": 10, "rc_after": 4})
    assert compute_rcg(s) == pytest.approx(0.6)


def test_tv_from_transfer_history():
    s = _skill(
        transfer_history=[
            {"success": True, "target_family": "a"},
            {"success": True, "target_family": "b"},
            {"success": False, "target_family": "c"},
        ]
    )
    # success rate 2/3, coverage 2/5
    assert compute_tv(s, SkillConfig(tv_coverage_norm=5)) == pytest.approx(
        (2 / 3) * (2 / 5)
    )


def test_rv_and_nr_and_mc():
    s = _skill(reuse_count=5, reuse_history=[{"impact": 1.0}] * 5)
    assert compute_rv(s, SkillConfig(reuse_norm=10)) == pytest.approx(0.5)
    s2 = _skill(
        transfer_history=[
            {"success": False, "target_family": "x"},
            {"success": False, "target_family": "y"},
        ]
    )
    assert compute_nr(s2, SkillConfig(ntr_impact=1.0)) == pytest.approx(1.0)
    assert compute_mc(s, SkillConfig(base_maintenance=0.05)) == pytest.approx(0.06)
