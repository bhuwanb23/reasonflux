"""SF7 capability collapse detection."""

from skills import SkillRobustnessConfig
from skills.robustness.sf_capability import detect_capability_collapse


def test_negative_cgr_across_periods_flags_collapse():
    cfg = SkillRobustnessConfig(cgr_collapse=-0.05, collapse_periods=2)
    series = [1.0, 0.9, 0.7, 0.5]
    risk = detect_capability_collapse(series, cfg)
    assert risk.collapsed
    assert risk.periods >= 2
    assert "cgr_negative" in risk.reasons


def test_growth_series_not_collapsed():
    cfg = SkillRobustnessConfig(cgr_collapse=-0.05, collapse_periods=2)
    risk = detect_capability_collapse([0.5, 0.6, 0.7], cfg)
    assert not risk.collapsed
    assert detect_capability_collapse([0.5], cfg).collapsed is False
