"""Evaluation pipeline — run harness benchmarks and write reports (Phase 11E-4)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from evaluation.harness.config import HarnessConfig
from evaluation.harness.models import EvaluationRun
from evaluation.harness.runner import run_benchmark
from evaluation.reports import write_report
from utils.config import load_harness_config


def run_evaluation_pipeline(
    level: str = "capability",
    *,
    baseline: str | None = None,
    ablation: str | None = None,
    config: HarnessConfig | None = None,
    out_dir: str | Path | None = None,
    write: bool = True,
    run_id: str | None = None,
) -> dict[str, Any]:
    """Compute CGM-layer metrics via harness and optionally emit reports."""
    cfg = config or load_harness_config()
    level = level or cfg.default_level
    result: EvaluationRun = run_benchmark(
        level,
        baseline=baseline,
        ablation=ablation,
        config=cfg,
        run_id=run_id,
    )
    paths: dict[str, Any] = {}
    if write:
        target = out_dir or cfg.report_dir
        paths = {
            str(k): str(v)
            for k, v in write_report(result, out_dir=target).items()
        }
    return {
        "result": result.to_dict(),
        "success": result.success,
        "maturity": result.maturity,
        "paths": paths,
    }
