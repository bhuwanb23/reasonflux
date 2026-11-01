"""Frozen Phase 13E task streams and common discovery pipeline."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from capability.config import CapabilityConfig
from evaluation.growth_config import GrowthConfig
from pipelines.invariant_pipeline import run_invariant_pipeline
from pipelines.trace_pipeline import run_trace_pipeline
from solver.tasks import FAMILIES, GridTask, make_task
from experiments.phase13c.scoring import _eligible_pool
from skills.config import SkillConfig

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "experiments" / "phase13e" / "config.json"


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def capability_config_from_json(config: dict[str, Any]) -> CapabilityConfig:
    raw = config["capability_config"]
    weights = raw["capu_weights"]
    return CapabilityConfig(
        min_skills=int(raw["min_skills"]),
        min_transfer_events=int(raw["min_transfer_events"]),
        min_utility=float(raw["min_utility"]),
        min_confidence=float(raw["min_confidence"]),
        min_coverage=float(raw["min_coverage"]),
        ccov_family_norm=int(raw["ccov_family_norm"]),
        capu_w_su=float(weights["su"]),
        capu_w_ts=float(weights["ts"]),
        capu_w_cov=float(weights["coverage"]),
        capu_w_comp=float(weights["composition"]),
        max_capabilities=int(raw["max_capabilities"]),
    )


def growth_config_from_json(config: dict[str, Any]) -> GrowthConfig:
    raw = config["growth_config"]
    ct, ig = raw["ct_weights"], raw["ig_weights"]
    return GrowthConfig(
        w_su=float(ct["su"]), w_ts=float(ct["ts"]),
        w_cov=float(ct["coverage"]), w_comp=float(ct["composition"]),
        ig_w_cgr=float(ig["cgr"]), ig_w_tg=float(ig["tg"]),
        ig_w_ug=float(ig["ug"]), ig_w_ccg=float(ig["ccg"]),
        ig_w_compg=float(ig["compg"]),
        default_dt=float(raw["dt_per_round"]),
        saturation_low_csr=float(raw["saturation_low_csr"]),
        skill_count_illusion_max_cgr=float(raw["skill_count_illusion_max_cgr"]),
    )


def discover(seed: int, config: dict[str, Any] | None = None) -> dict[str, Any]:
    """Generate a common, outcome-independent candidate pool for every arm."""
    cfg = config or load_config()
    spec = cfg["discovery"]
    trace_seed = int(seed) + int(spec["seed_offset"])
    trace_run = run_trace_pipeline(
        FAMILIES,
        per_family=int(spec["traces_per_family"]),
        seed=trace_seed,
        difficulty=float(spec["difficulty"]),
        persist=False,
    )
    inv_run = run_invariant_pipeline(trace_run.traces, bootstrap=True)
    candidates, rejected = _eligible_pool(inv_run.promotable, SkillConfig())
    return {
        "trace_run": trace_run,
        "invariant_run": inv_run,
        "candidates": candidates,
        "rejected": rejected,
        "trace_seed": trace_seed,
    }


def build_round_tasks(seed: int, round_index: int, config: dict[str, Any] | None = None) -> list[GridTask]:
    """Build identical held-out tasks for all arms in a seed/round."""
    cfg = config or load_config()
    spec = cfg["rounds"]
    out: list[GridTask] = []
    per_family = int(spec["tasks_per_family_per_round"])
    base_seed = int(seed) + int(spec["seed_offset"]) + int(round_index) * 100
    for i in range(per_family):
        for family in FAMILIES:
            variant = i % 2
            if round_index == 0 and family in {"counting", "grouping"}:
                variant = 0
            compose = round_index >= 2 and family == "reflection"
            task = make_task(
                family,
                seed=base_seed + i,
                difficulty=float(spec["difficulty"]),
                variant=variant,
                compose=compose,
            )
            # Round 2's paired odd variants are explicitly the symmetric
            # counting/grouping opportunities declared in the protocol.
            task.metadata["phase13e_round"] = int(round_index) + 1
            out.append(task)
    return out


def task_utility(success: bool, cost: float) -> float:
    """Preregistered synthetic task utility: accuracy minus cost/100."""
    return float(bool(success)) - float(cost) / 100.0


def signature_of_trace(trace: Any) -> tuple[str, ...]:
    return tuple(str(step.operation) for step in (trace.steps or []))


def family_of_trace(trace: Any) -> str:
    meta = trace.metadata or {}
    family = meta.get("task_family") or meta.get("family")
    if family:
        return str(family)
    task_id = str(trace.task_id)
    return task_id.split("-", 1)[0]
