"""Tests for ValidationScores normalization helpers."""

import pytest

from invariants import ValidationConfig, ValidationScores
from invariants.validation.scores import clamp01, normalize_count
from utils.config import load_validation_config
from pathlib import Path


def test_clamp_and_normalize():
    assert clamp01(1.5) == 1.0
    assert clamp01(-0.2) == 0.0
    assert normalize_count(5, 10) == 0.5
    assert normalize_count(20, 10) == 1.0


def test_score_product():
    scores = ValidationScores(
        frequency=1.0, consistency=0.5, generality=0.5, transfer=0.8, reasoning_value=0.5
    )
    assert scores.score == pytest.approx(0.1)


def test_validation_config_from_repo():
    config = load_validation_config(Path("configs"))
    assert isinstance(config, ValidationConfig)
    assert config.freq_norm == 10
    assert config.min_c == pytest.approx(0.6)


def test_validation_config_rejects_bad_bounds():
    with pytest.raises(ValueError):
        ValidationConfig(freq_norm=0)
    with pytest.raises(ValueError):
        ValidationConfig(min_f=1.5)
