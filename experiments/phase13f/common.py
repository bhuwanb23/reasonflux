"""Phase 13F frozen config, task streams, and runtime names."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from experiments.phase13e.arms import ArmRuntime
from experiments.phase13e.common import build_round_tasks, discover, task_utility

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "experiments/phase13f/config.json"
OUT = ROOT / "reports/experiments/PHASE-13F-BASELINE-ABLATION-V1"


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def names(config: dict[str, Any]) -> list[str]:
    arms = config["arms"]
    sensitivity = ["SENS_SCV_Q25", "SENS_SCV_Q75", "SENS_IS_7_5", "SENS_IS_10", "SENS_COMP_LOOSE", "SENS_COMP_STRICT"]
    return [arms["primary"], *arms["baselines"], *arms["ablations"], *sensitivity]
