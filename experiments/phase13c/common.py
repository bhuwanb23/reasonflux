"""Shared paths, frozen config access, and score helpers for Phase 13C."""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any
import yaml

ROOT = Path(__file__).resolve().parents[2]
for _path in (ROOT, ROOT / "src"):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))
CONFIG_PATH = ROOT / "configs" / "phase13c_sct_v1.yaml"
OUT_DIR = ROOT / "reports" / "experiments" / "PHASE-13C-SCT-V1"
MC_SENSITIVITY = (0.00, 0.03, 0.06, 0.12)


def load_config() -> dict[str, Any]:
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))


def clip01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _quantile(values: list[float], probability: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(float(x) for x in values)
    position = (len(ordered) - 1) * probability
    low = int(math.floor(position))
    high = int(math.ceil(position))
    if low == high:
        return ordered[low]
    weight = position - low
    return ordered[low] * (1.0 - weight) + ordered[high] * weight


def _config_digest(config_data: dict[str, Any]) -> str:
    encoded = json.dumps(config_data, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()
