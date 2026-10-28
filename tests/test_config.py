"""Tests for YAML config loading and the invariant policy binding."""

from pathlib import Path

import pytest

from invariants import InvariantPolicy
from utils.config import load_config, load_default_configs, load_invariant_policy


def test_load_config_returns_mapping(tmp_path: Path):
    path = tmp_path / "c.yaml"
    path.write_text("a: 1\nb: two\n", encoding="utf-8")
    assert load_config(path) == {"a": 1, "b": "two"}


def test_load_config_missing_file_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "nope.yaml")


def test_load_config_rejects_non_mapping(tmp_path: Path):
    path = tmp_path / "list.yaml"
    path.write_text("- 1\n- 2\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_config(path)


def test_load_default_configs_merges_repo_configs():
    merged = load_default_configs(Path("configs"))
    assert "invariants" in merged
    assert "skills" in merged
    assert "metrics" in merged
    assert "project" in merged


def test_load_invariant_policy_from_repo_configs():
    policy = load_invariant_policy(Path("configs"))
    assert isinstance(policy, InvariantPolicy)
    assert policy.min_consistency == pytest.approx(0.6)


def test_load_invariant_policy_falls_back_when_missing(tmp_path: Path):
    policy = load_invariant_policy(tmp_path)
    assert isinstance(policy, InvariantPolicy)
    assert policy.min_frequency == 3
