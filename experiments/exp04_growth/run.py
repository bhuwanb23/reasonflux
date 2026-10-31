"""exp04_growth — Capability Growth Metrics (CGM) evaluation entrypoint."""

from __future__ import annotations

from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parents[2]
for _p in (_ROOT, _ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

EXPERIMENT_META = {
    "experiment_id": "EXP-04",
    "hypothesis": "Accumulated experience increases capability and intelligence.",
    "claim": "CGM",
    "primary_metrics": ["CGR", "IG", "IGR", "coverage"],
    "success_thresholds": {"cgr": 0.01, "ig": 0.0},
    "failure_thresholds": {"cgr": 0.0, "ig": 0.0},
}

from pipelines.evaluation_pipeline import run_evaluation_pipeline
from experiments._common import default_seeds, run_multi_seed


def main(*, seed: int = 0, write: bool = True) -> dict:
    """Run capability + intelligence-oriented harness benchmarks."""
    cap = run_evaluation_pipeline(
        level="capability", seed=seed, run_id=f"exp04_cap_{seed}", write=write
    )
    intel = run_evaluation_pipeline(
        level="intelligence", seed=seed, run_id=f"exp04_intel_{seed}", write=write
    )
    cap_stats = cap["result"]["stats"]
    intel_stats = intel["result"]["stats"]
    metrics = {
        "CGR": cap_stats["cgr"]["mean"],
        "IG": intel_stats["ig"]["mean"],
        "IGR": intel_stats["igr"]["mean"],
        "coverage": cap["result"]["snapshots"][-1]["coverage"],
    }
    success = bool(
        cap["success"]
        and metrics["CGR"] > EXPERIMENT_META["success_thresholds"]["cgr"]
        and metrics["IG"] > EXPERIMENT_META["success_thresholds"]["ig"]
    )
    return {
        "experiment_id": "EXP-04",
        "seed": seed,
        "dataset_version": "synthetic-v1",
        "metrics": metrics,
        "success": success,
        "intelligence_success": bool(intel["success"]),
        "capability": cap,
        "intelligence": intel,
    }


def main_multi(*, seeds: tuple[int, ...] | None = None, write: bool = True) -> dict:
    """Run EXP-04 under the governed multi-seed policy."""
    return run_multi_seed(
        main,
        seeds=seeds or default_seeds(Path(__file__).resolve().parents[2]),
        metric_paths={
            "CGR": "metrics.CGR",
            "IG": "metrics.IG",
            "IGR": "metrics.IGR",
            "coverage": "metrics.coverage",
        },
        experiment_id="EXP-04",
        thresholds=EXPERIMENT_META["success_thresholds"],
        write=write,
        root=Path(__file__).resolve().parents[2],
    )


if __name__ == "__main__":
    out = main()
    print("success=", out["success"])
    print("intelligence_harness_success=", out["intelligence_success"])
