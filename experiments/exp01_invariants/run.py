"""exp01_invariants — Invariant Discovery Theory (IDT) evaluation entrypoint.

Validates: invariants are discovered from real traces, reflection/rotation
structure separates, and IS ranks them as expected.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
for _p in (_ROOT, _ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from evaluation.invariant_metrics import compute_is, summarize_is  # noqa: E402
from pipelines.invariant_pipeline import run_invariant_pipeline  # noqa: E402
from pipelines.trace_pipeline import run_trace_pipeline  # noqa: E402
from experiments._common import write_experiment, write_figure  # noqa: E402


def main(*, seed: int = 0, per_family: int = 6, write: bool = True) -> dict:
    """Mine invariants from solver traces and report their strength."""
    trace_run = run_trace_pipeline(per_family=per_family, seed=seed, persist=False)
    inv_run = run_invariant_pipeline(trace_run.traces)
    validated = list(inv_run.validation.validated) if inv_run.validation else []

    rows = [
        {
            "signature": " -> ".join(inv.pattern_signature),
            "frequency": inv.frequency,
            "consistency": round(inv.consistency, 3),
            "generality": round(inv.generality, 3),
            "is": round(compute_is(inv), 3),
            "families": ", ".join(inv.task_families),
        }
        for inv in validated
    ]
    rows.sort(key=lambda r: -r["is"])

    payload = {
        "experiment": "exp01_invariants",
        "contribution": "IDT",
        "n_traces": trace_run.n_traces,
        "n_candidates": len(inv_run.candidates),
        "n_validated": len(validated),
        "is_summary": {k: round(v, 4) for k, v in summarize_is(validated).items()},
        "reflection_found": any("apply_reflection" in inv.pattern_signature for inv in validated),
        "rotation_found": any("apply_rotation" in inv.pattern_signature for inv in validated),
        "invariants": rows,
    }
    if write:
        payload["artifacts"] = {
            **write_experiment("exp01_invariants", payload, root=_ROOT),
            "figure": write_figure(
                "exp01_is_by_invariant",
                {r["signature"][:28]: [r["is"]] for r in rows} or {"none": [0.0]},
                title="Invariant Strength by discovered invariant",
                ylabel="IS",
                root=_ROOT,
            ),
        }
    return payload


if __name__ == "__main__":
    out = main()
    print("validated=", out["n_validated"], "reflection=", out["reflection_found"])
    print("rotation=", out["rotation_found"])
