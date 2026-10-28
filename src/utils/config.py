"""Load YAML configuration from configs/."""

from pathlib import Path
from typing import Any


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML config file into a dict."""
    raise NotImplementedError("load_config is not implemented yet")


def load_default_configs(config_dir: str | Path = "configs") -> dict[str, Any]:
    """Merge default, thresholds, metrics, and experiments configs."""
    raise NotImplementedError("load_default_configs is not implemented yet")
