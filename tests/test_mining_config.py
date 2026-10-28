"""Tests for mining config YAML binding."""

from pathlib import Path

import pytest

from invariants import MiningConfig
from utils.config import load_mining_config


def test_load_mining_config_from_repo():
    config = load_mining_config(Path("configs"))
    assert isinstance(config, MiningConfig)
    assert config.min_frequency == 3
    assert config.min_cross_trace == 2
    assert config.max_fragment_length == 4
    assert config.min_core_length == 2
    assert config.successful_trace_bias is True


def test_load_mining_config_defaults_when_missing(tmp_path: Path):
    config = load_mining_config(tmp_path)
    assert config == MiningConfig()


def test_mining_config_from_dict_ignores_unknown():
    config = MiningConfig.from_dict({"min_frequency": 5, "unknown": True})
    assert config.min_frequency == 5


def test_mining_config_rejects_invalid():
    with pytest.raises(ValueError):
        MiningConfig(min_frequency=0)
    with pytest.raises(ValueError):
        MiningConfig(min_cross_trace=0)
    with pytest.raises(ValueError):
        MiningConfig(max_fragment_length=0)
