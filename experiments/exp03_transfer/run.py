"""exp03_transfer — transfer evaluation entrypoint.

Validates the core thesis: solving task A measurably improves task B. Transfer
is credited only when the reused run is correct *and* cheaper than free search,
and cross-family transfer is only credited where the underlying invariance holds.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
for _p in (_ROOT, _ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from pipelines.invariant_pipeline import run_invariant_pipeline  # noqa: E402
from pipelines.skill_pipeline import run_skill_pipeline  # noqa: E402
from pipelines.trace_pipeline import run_trace_pipeline  # noqa: E402
from solver.tasks import FAMILIES, make_task_batch  # noqa: E402
from transfer.reuse_engine import ReuseEngine  # noqa: E402
from experiments._common import write_experiment, write_figure  # noqa: E402


def main(*, seed: int = 0, per_family: int = 6, write: bool = True) -> dict:
    """Measure transfer per source→target family pair."""
    trace_run = run_trace_pipeline(per_family=per_family, seed=seed, persist=False)
    inv_run = run_invariant_pipeline(trace_run.traces)
    skill_run = run_skill_pipeline(inv_run.promotable)

    engine = ReuseEngine(skill_run.library)
    tasks = make_task_batch(FAMILIES, per_family=2, seed=100, difficulty=0.2)
    results = engine.apply_batch(tasks)

    by_family: dict[str, dict] = {}
    for family in FAMILIES:
        rows = [r for r in results if r.task_family == family]
        applied = [r for r in rows if r.applied]
        credited = [r for r in rows if r.transfer_credit]
        by_family[family] = {
            "attempts": len(rows),
            "applied": len(applied),
            "credited": len(credited),
            "mean_reduction": round(
                sum(r.reasoning_reduction for r in credited) / len(credited), 4
            )
            if credited
            else 0.0,
        }

    records = engine.memory.all_records()
    cross = [r for r in records if r.source_family != r.target_family]
    payload = {
        "experiment": "exp03_transfer",
        "contribution": "transfer",
        "n_transfer_records": len(records),
        "n_cross_family": len(cross),
        "mean_benefit": round(
            sum(r.benefit for r in records) / len(records), 4
        )
        if records
        else 0.0,
        "positive_transfer": len(records) > 0,
        "by_family": by_family,
        "records": [
            {
                "source": r.source_family,
                "target": r.target_family,
                "benefit": round(r.benefit, 4),
                "reduction": round(r.reasoning_reduction, 4),
            }
            for r in records
        ],
    }
    if write:
        payload["artifacts"] = {
            **write_experiment("exp03_transfer", payload, root=_ROOT),
            "figure": write_figure(
                "exp03_transfer_benefit",
                {"benefit": [r.benefit for r in records] or [0.0]},
                title="Transfer benefit per credited reuse",
                ylabel="benefit",
                root=_ROOT,
            ),
        }
    return payload


if __name__ == "__main__":
    out = main()
    print("records=", out["n_transfer_records"], "mean=", out["mean_benefit"])
