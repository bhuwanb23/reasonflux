"""Load YAML configuration from configs/."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

__all__ = [
    "DEFAULT_CONFIG_DIR",
    "load_config",
    "load_default_configs",
    "load_invariant_policy",
    "load_mining_config",
    "load_robustness_config",
    "load_capability_config",
    "load_growth_config",
    "load_harness_config",
    "load_skill_config",
    "load_skill_robustness_config",
    "load_capability_robustness_config",
    "load_transfer_config",
    "load_validation_config",
]

DEFAULT_CONFIG_DIR = Path("configs")


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML config file into a dict."""
    target = Path(path)
    if not target.exists():
        raise FileNotFoundError(f"Config file not found: {target}")
    data = yaml.safe_load(target.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected a mapping in {target}, got {type(data).__name__}")
    return data


def load_default_configs(config_dir: str | Path = DEFAULT_CONFIG_DIR) -> dict[str, Any]:
    """Merge default, thresholds, metrics, and experiments configs.

    Later files override earlier ones, key by key at the top level.
    """
    directory = Path(config_dir)
    merged: dict[str, Any] = {}
    for name in ("default.yaml", "thresholds.yaml", "metrics.yaml", "experiments.yaml"):
        path = directory / name
        if path.exists():
            merged.update(load_config(path))
    return merged


def load_invariant_policy(config_dir: str | Path = DEFAULT_CONFIG_DIR) -> Any:
    """Build an InvariantPolicy from configs/thresholds.yaml.

    Reads the ``invariants`` mapping; unknown keys are ignored.
    """
    from invariants.specification import InvariantPolicy

    path = Path(config_dir) / "thresholds.yaml"
    if not path.exists():
        return InvariantPolicy()
    data = load_config(path).get("invariants") or {}
    return InvariantPolicy.from_dict(data)


def load_mining_config(config_dir: str | Path = DEFAULT_CONFIG_DIR) -> Any:
    """Build a MiningConfig from configs/thresholds.yaml.

    Reads the ``mining`` mapping; unknown keys are ignored.
    """
    from invariants.pattern_mining import MiningConfig

    path = Path(config_dir) / "thresholds.yaml"
    if not path.exists():
        return MiningConfig()
    data = load_config(path).get("mining") or {}
    return MiningConfig.from_dict(data)


def load_validation_config(config_dir: str | Path = DEFAULT_CONFIG_DIR) -> Any:
    """Build a ValidationConfig from configs/thresholds.yaml."""
    from invariants.validation.scores import ValidationConfig

    path = Path(config_dir) / "thresholds.yaml"
    if not path.exists():
        return ValidationConfig()
    data = load_config(path).get("validation") or {}
    return ValidationConfig.from_dict(data)


def load_transfer_config(config_dir: str | Path = DEFAULT_CONFIG_DIR) -> Any:
    """Build a TransferConfig from configs/thresholds.yaml."""
    from transfer.metrics import TransferConfig

    path = Path(config_dir) / "thresholds.yaml"
    if not path.exists():
        return TransferConfig()
    data = load_config(path).get("transfer") or {}
    return TransferConfig.from_dict(data)


def load_robustness_config(config_dir: str | Path = DEFAULT_CONFIG_DIR) -> Any:
    """Build a RobustnessConfig from configs/thresholds.yaml."""
    from invariants.robustness.config import RobustnessConfig

    path = Path(config_dir) / "thresholds.yaml"
    if not path.exists():
        return RobustnessConfig()
    data = load_config(path).get("robustness") or {}
    return RobustnessConfig.from_dict(data)


def load_skill_config(config_dir: str | Path = DEFAULT_CONFIG_DIR) -> Any:
    """Build a SkillConfig from configs/thresholds.yaml."""
    from skills.config import SkillConfig

    path = Path(config_dir) / "thresholds.yaml"
    if not path.exists():
        return SkillConfig()
    data = load_config(path).get("skills") or {}
    return SkillConfig.from_dict(data)


def load_skill_robustness_config(config_dir: str | Path = DEFAULT_CONFIG_DIR) -> Any:
    """Build a SkillRobustnessConfig from configs/thresholds.yaml."""
    from skills.robustness.config import SkillRobustnessConfig

    path = Path(config_dir) / "thresholds.yaml"
    if not path.exists():
        return SkillRobustnessConfig()
    data = load_config(path).get("skill_robustness") or {}
    return SkillRobustnessConfig.from_dict(data)


def load_capability_config(config_dir: str | Path = DEFAULT_CONFIG_DIR) -> Any:
    """Build a CapabilityConfig from configs/thresholds.yaml."""
    from capability.config import CapabilityConfig

    path = Path(config_dir) / "thresholds.yaml"
    if not path.exists():
        return CapabilityConfig()
    data = load_config(path).get("capability") or {}
    return CapabilityConfig.from_dict(data)


def load_growth_config(config_dir: str | Path = DEFAULT_CONFIG_DIR) -> Any:
    """Build a GrowthConfig from configs/thresholds.yaml."""
    from evaluation.growth_config import GrowthConfig

    path = Path(config_dir) / "thresholds.yaml"
    if not path.exists():
        return GrowthConfig()
    data = load_config(path).get("growth") or {}
    return GrowthConfig.from_dict(data)


def load_harness_config(config_dir: str | Path = DEFAULT_CONFIG_DIR) -> Any:
    """Build a HarnessConfig from configs/thresholds.yaml."""
    from evaluation.harness.config import HarnessConfig

    path = Path(config_dir) / "thresholds.yaml"
    if not path.exists():
        return HarnessConfig()
    data = load_config(path).get("evaluation") or {}
    return HarnessConfig.from_dict(data)


def load_capability_robustness_config(
    config_dir: str | Path = DEFAULT_CONFIG_DIR,
) -> Any:
    """Build a CapabilityRobustnessConfig from configs/thresholds.yaml."""
    from capability.robustness.config import CapabilityRobustnessConfig

    path = Path(config_dir) / "thresholds.yaml"
    if not path.exists():
        return CapabilityRobustnessConfig()
    data = load_config(path).get("capability_robustness") or {}
    return CapabilityRobustnessConfig.from_dict(data)