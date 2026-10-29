"""Portfolio ASU / TSU / PU / UG / NTB."""

import pytest

from core import Skill, SkillState
from skills import (
    PortfolioMetrics,
    SkillLibrary,
    compute_portfolio_metrics,
    refresh_skill_utility,
)


def test_portfolio_metrics():
    lib = SkillLibrary()
    a = Skill(
        skill_id="a",
        abstraction_gain=0.8,
        creation_cost=0.05,
        reuse_count=4,
        reuse_history=[{"impact": 1.0}] * 4,
        transfer_history=[{"success": True, "target_family": "x"}],
        state=SkillState.ACTIVE,
        metadata={"composition_potential": 0.5, "mvp_category": "reflection"},
    )
    b = Skill(
        skill_id="b",
        abstraction_gain=0.2,
        creation_cost=0.1,
        reuse_count=0,
        transfer_history=[{"success": False, "target_family": "y"}],
        state=SkillState.ACTIVE,
    )
    refresh_skill_utility(a)
    refresh_skill_utility(b)
    lib.add(a)
    lib.add(b)

    prev = PortfolioMetrics(asu=0.0)
    metrics = compute_portfolio_metrics(lib, previous=prev)
    assert metrics.skill_count == 2
    assert metrics.tsu == pytest.approx(max(a.utility, b.utility))
    assert metrics.asu == pytest.approx((a.utility + b.utility) / 2)
    assert metrics.pu == pytest.approx(sum(u for u in (a.utility, b.utility) if u > 0))
    assert metrics.ug == pytest.approx(metrics.asu - prev.asu)
    assert metrics.ntb >= 0.0
