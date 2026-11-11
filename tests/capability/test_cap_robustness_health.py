"""CHS / CS health bands."""

from capability.library import CapabilityLibrary
from capability.models import Capability
from capability.robustness.config import CapabilityRobustnessConfig
from capability.robustness.health import HealthBand, score_capability, score_portfolio
from capability.robustness.metrics import capability_health_score, capability_stability
from core.skill import Skill
from core.states import SkillState
from skills.library import SkillLibrary


def test_chs_and_cs_helpers():
    chs = capability_health_score(
        utility=0.9, transfer=0.9, coverage=0.9, growth=0.1, confidence=0.9
    )
    assert chs >= 0.7
    cs = capability_stability([0.5, 0.51, 0.49], unstable_var=0.3)
    assert cs > 0.9


def test_band_and_portfolio():
    skills = SkillLibrary()
    skills.add(
        Skill(
            skill_id="s1",
            state=SkillState.ACTIVE,
            utility=0.8,
            transfer_score=0.7,
        )
    )
    caps = CapabilityLibrary()
    caps.add(
        Capability(
            capability_id="c1",
            skill_ids=["s1"],
            utility=0.8,
            confidence=0.7,
            metadata={"cgr": 0.05, "confidence": 0.7},
        )
    )
    h = score_capability(caps.get("c1"), skills)
    assert h.band in HealthBand
    assert 0.0 <= h.chs <= 1.0
    port = score_portfolio(caps, skills, config=CapabilityRobustnessConfig())
    assert port.mean_chs >= 0.0
    assert len(port.members) == 1
