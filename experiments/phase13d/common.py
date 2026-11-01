"""Frozen Phase-13D configuration and small shared definitions."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any
import yaml

ROOT = Path(__file__).resolve().parents[2]
for _path in (ROOT, ROOT / "src"):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))
CONFIG_PATH = ROOT / "configs" / "phase13d_transfer_v1.yaml"
OUT_DIR = ROOT / "reports" / "experiments" / "PHASE-13D-TRANSFER-V1"
ALLOWED_OPS = ("apply_reflection", "apply_rotation", "count_objects", "group_by_color", "count_groups")
TRANSFORMS = {"apply_reflection", "apply_rotation"}
OP_COST = {"apply_reflection": 3, "apply_rotation": 3, "count_objects": 2, "group_by_color": 2, "count_groups": 2}
STEP_PENALTY = 0.02
FAMILY_FOR_OP = {
    "apply_reflection": "reflection", "apply_rotation": "rotation",
    "count_objects": "counting", "group_by_color": "grouping", "count_groups": "counting",
}


def load_config() -> dict[str, Any]:
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def validate_config(config: dict[str, Any]) -> None:
    expected = {"baseline_transform_steps": 3, "baseline_reducer_steps": 2,
                "final_verification_steps": 1, "learned_single_skill_steps": 2,
                "composition_selection_steps": 1, "composition_operation_execution_steps": 1,
                "forced_skill_steps": 2}
    declared = config.get("cost_model", {})
    if any(int(declared.get(key, -1)) != value for key, value in expected.items()):
        raise ValueError("cost_model does not match the preregistered evaluator contract")
    if float(config.get("performance", {}).get("step_penalty", -1)) != 0.02:
        raise ValueError("performance.step_penalty differs from frozen preregistration")
    if len(config.get("seeds", {}).get("confirmation", [])) != 10:
        raise ValueError("Phase 13D confirmation requires exactly ten frozen seeds")
