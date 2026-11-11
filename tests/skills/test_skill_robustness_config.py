"""SkillRobustnessConfig defaults, validation, and YAML loading."""

import pytest

from skills.robustness import SkillRobustnessConfig
from utils.config import load_skill_robustness_config


def test_defaults_and_yaml_load():
    cfg = SkillRobustnessConfig()
    assert cfg.ser_restrict >= cfg.ser_warn
    assert cfg.ntr_warn < cfg.ntr_restrict < cfg.ntr_retire
    loaded = load_skill_robustness_config()
    assert loaded.ser_warn == pytest.approx(0.5)
    assert loaded.audit_max_actions >= 1


def test_invalid_thresholds_raise():
    with pytest.raises(ValueError):
        SkillRobustnessConfig(ser_warn=0.9, ser_restrict=0.5)
    with pytest.raises(ValueError):
        SkillRobustnessConfig(ntr_warn=0.6, ntr_restrict=0.3, ntr_retire=0.5)
    with pytest.raises(ValueError):
        SkillRobustnessConfig(min_evidence_promote=0)


def test_from_dict_ignores_unknown_keys():
    cfg = SkillRobustnessConfig.from_dict({"ser_warn": 0.4, "bogus": 1})
    assert cfg.ser_warn == pytest.approx(0.4)
