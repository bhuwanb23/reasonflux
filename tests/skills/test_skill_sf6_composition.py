"""SF6 composition failure assessment."""

from skills import SkillRobustnessConfig
from skills.composition.models import CompositionCandidate, CompositionState
from skills.robustness.sf_composition import assess_composition_failure


def test_harmful_composition_rejected_and_cost_raised():
    cfg = SkillRobustnessConfig(cu_min_composition=0.0, composition_ncr_limit=0.3)
    bad = CompositionCandidate(
        composition_id="a+b",
        skill_ids=["a", "b"],
        composition_cost=0.1,
        cu=-0.5,
        evidence={"uses": 4, "successes": 1, "failures": 3},
    )
    result = assess_composition_failure(bad, cfg)
    assert result.failed
    assert "low_cu" in result.reasons
    assert "high_ncr" in result.reasons
    assert bad.state is CompositionState.DISCARDED
    assert bad.composition_cost > 0.1
    assert bad.metadata["composition_failure"]["cu"] == -0.5


def test_healthy_composition_passes():
    cfg = SkillRobustnessConfig()
    good = CompositionCandidate(
        composition_id="c+d",
        skill_ids=["c", "d"],
        composition_cost=0.1,
        cu=0.8,
        evidence={"uses": 4, "successes": 4, "failures": 0},
    )
    result = assess_composition_failure(good, cfg)
    assert not result.failed
    assert good.state is CompositionState.CANDIDATE
