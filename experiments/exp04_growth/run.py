"""exp04_growth — Capability Growth Metrics (CGM) evaluation entrypoint."""

from __future__ import annotations

from pipelines.evaluation_pipeline import run_evaluation_pipeline


def main() -> dict:
    """Run capability + intelligence-oriented harness benchmarks."""
    cap = run_evaluation_pipeline(level="capability", run_id="exp04_cap")
    intel = run_evaluation_pipeline(level="intelligence", run_id="exp04_intel")
    return {"capability": cap, "intelligence": intel}


if __name__ == "__main__":
    out = main()
    print("capability_success=", out["capability"]["success"])
    print("intelligence_success=", out["intelligence"]["success"])
