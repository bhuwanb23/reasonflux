"""Calibration-only stage: seeds 15–19 and frozen selection parameters."""
from __future__ import annotations

import json
from typing import Any
from pipelines.invariant_pipeline import run_invariant_pipeline
from skills.config import SkillConfig
from .common import OUT_DIR, _config_digest, _quantile, load_config
from .scoring import _candidate_score, _eligible_pool
from .tasking import _enforce_opportunity_horizon, _task_batches


def run_calibration_seed(run_seed: int) -> dict[str, Any]:
    config_data = load_config()
    skill_config = SkillConfig()
    trace_run, eval_tasks = _task_batches(run_seed, config_data)
    inv_run = run_invariant_pipeline(trace_run.traces, bootstrap=True)
    eligible, rejected = _eligible_pool(inv_run.promotable, skill_config)
    eligible, rejected = _enforce_opportunity_horizon(
        eligible, rejected, eval_tasks,
        int(config_data["tasks"]["evaluation_opportunities_per_candidate"]),
    )
    candidates = [
        {
            "invariant_id": item["invariant"].invariant_id,
            "signature": list(item["invariant"].pattern_signature),
            "category": str((item["candidate"].metadata or {}).get("mvp_category", "general")),
            "frequency": int(item["invariant"].frequency),
            "task_families": list(item["invariant"].task_families),
            **item["score"],
        }
        for item in eligible
    ]
    return {
        "seed": run_seed,
        "discovery_seed": run_seed + config_data["tasks"]["discovery_seed_offset"],
        "discovery_trace_count": len(trace_run.traces),
        "promotable_count": len(inv_run.promotable),
        "eligible_candidate_count": len(eligible),
        "birth_count_at_zero": sum(row["SCV10"] > 0 for row in candidates),
        "candidate_rows": candidates,
        "rejected_candidates": rejected,
    }


def run_calibration(*, write: bool = True) -> dict[str, Any]:
    """Run only seeds 15--19 and freeze calibration-derived values."""
    config_data = load_config()
    seeds = tuple(config_data["seeds"]["calibration"])
    if len(seeds) != 5 or set(seeds) & set(config_data["seeds"]["confirmation"]):
        raise ValueError("invalid Phase 13C calibration/confirmation split")
    raw = [run_calibration_seed(seed) for seed in seeds]
    candidate_rows = [row for seed in raw for row in seed["candidate_rows"]]
    scores = [float(row["SCV10"]) for row in candidate_rows]
    eligible_count = sum(int(seed["eligible_candidate_count"]) for seed in raw)
    birth_count = sum(int(seed["birth_count_at_zero"]) for seed in raw)
    p_random = birth_count / eligible_count if eligible_count else 0.0
    frozen = {
        "protocol_id": "PHASE-13C-SCT-V1",
        "calibration_seeds": list(seeds),
        "confirmation_seeds": list(config_data["seeds"]["confirmation"]),
        "config_sha256": _config_digest(config_data),
        "candidate_count": len(candidate_rows),
        "eligible_candidate_count": eligible_count,
        "birth_count_at_primary_threshold": birth_count,
        "random_create_probability": p_random,
        "thresholds": {
            "low_q25": _quantile(scores, 0.25),
            "medium_q50": _quantile(scores, 0.50),
            "high_q75": _quantile(scores, 0.75),
            "primary": 0.0,
        },
        "mc_per_opportunity_primary": 0.06,
        "mc_sensitivity": list(MC_SENSITIVITY),
        "calibration_candidate_scv10_values": scores,
        "calibration_results": raw,
        "confirmation_opened": False,
    }
    if write:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        (OUT_DIR / "calibration.json").write_text(
            json.dumps(frozen, indent=2, sort_keys=True), encoding="utf-8"
        )
        (OUT_DIR / "calibration_frozen.json").write_text(
            json.dumps({k: v for k, v in frozen.items() if k != "calibration_results"}, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        lines = [
            "# Phase 13C calibration (seeds 15–19)",
            "",
            "Calibration only; not confirmatory evidence.",
            f"- Eligible candidates: {eligible_count}",
            f"- SCT births at primary threshold: {birth_count}",
            f"- Frozen random-create probability: {p_random:.6f}",
            f"- Low/medium/high cutoffs: {frozen['thresholds']['low_q25']:.6f} / {frozen['thresholds']['medium_q50']:.6f} / {frozen['thresholds']['high_q75']:.6f}",
            "- Confirmation seeds remain unopened by this stage.",
        ]
        (OUT_DIR / "calibration_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return frozen
