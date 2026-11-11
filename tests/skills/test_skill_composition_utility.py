"""CU formula components."""

import pytest

from skills import SkillConfig, compute_cu
from skills.composition.models import CompositionCandidate
from skills.composition.utility import composition_cost_for


def test_cu_formula():
    cfg = SkillConfig(compose_cost_base=0.1)
    cand = CompositionCandidate(
        composition_id="a+b",
        skill_ids=["a", "b"],
        composition_cost=composition_cost_for(2, cfg),
    )
    bd = compute_cu(
        cand,
        transfer_gain=0.4,
        reasoning_reduction=0.3,
        reuse_potential=0.2,
        config=cfg,
    )
    assert bd.composition_cost == pytest.approx(0.1)
    assert bd.cu == pytest.approx(0.4 + 0.3 + 0.2 - 0.1)
    assert cand.cu == pytest.approx(bd.cu)
    assert "cu_breakdown" in cand.metadata
