"""SkillConfig and YAML loader."""

from pathlib import Path

import pytest

from skills import SkillConfig
from utils.config import load_skill_config


def test_skill_config_defaults():
    cfg = SkillConfig()
    assert cfg.skill_creation_threshold == 0.0
    assert cfg.min_its == 0.5
    assert cfg.min_evidence == 3


def test_load_skill_config_from_repo():
    cfg = load_skill_config(Path("configs"))
    assert isinstance(cfg, SkillConfig)
    assert cfg.similarity_merge == pytest.approx(0.85)
    assert cfg.default_creation_cost == pytest.approx(0.1)
    assert cfg.su_min == pytest.approx(0.0)
    assert cfg.library_capacity == 50
    assert cfg.core_su == pytest.approx(0.6)


def test_skill_config_rejects_bad_values():
    with pytest.raises(ValueError):
        SkillConfig(min_evidence=0)
