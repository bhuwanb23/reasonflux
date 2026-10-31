"""exp02_skills — Skill Creation Trigger Theory (SCT) evaluation entrypoint.

Validates: the SCV gate admits justified skills and rejects unjustified ones,
and that admitted skills are actually reusable afterwards.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
for _p in (_ROOT, _ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

EXPERIMENT_META = {
    "experiment_id": "EXP-02",
    "hypothesis": "Useful skills emerge when skill creation value exceeds the gate.",
    "claim": "SCT",
    "primary_metrics": ["SCV", "SU", "reuse", "health"],
    "success_thresholds": {"admitted": 1, "strict_gate_reduction": True},
    "failure_thresholds": {"admitted": 0, "strict_gate_reduction": False},
}

from pipelines.invariant_pipeline import run_invariant_pipeline  # noqa: E402
from pipelines.skill_pipeline import run_skill_pipeline  # noqa: E402
from pipelines.trace_pipeline import run_trace_pipeline  # noqa: E402
from skills.config import SkillConfig  # noqa: E402
from experiments._common import default_seeds, run_multi_seed, write_experiment  # noqa: E402


def main(*, seed: int = 0, per_family: int = 6, write: bool = True) -> dict:
    """Run the SCV decision at the default and at a prohibitive threshold.

    Skills are admitted as *provisional trials* (on trace-derived priors) because
    mining cannot supply transfer evidence. Their admission is an experiment, not
    a claim of utility.
    """
    trace_run = run_trace_pipeline(per_family=per_family, seed=seed, persist=False)
    inv_run = run_invariant_pipeline(trace_run.traces, bootstrap=True)
    promotable = list(inv_run.promotable)

    default_run = run_skill_pipeline(promotable, allow_prior_evidence=True)
    strict_run = run_skill_pipeline(
        promotable,
        config=SkillConfig(skill_creation_threshold=100.0),
        allow_prior_evidence=True,
    )

    admitted = [
        {
            "skill_id": s.skill_id,
            "triggers": " -> ".join(s.trigger_conditions),
            "scv": round(float(s.scv or 0.0), 4),
            "utility": round(float(s.utility or 0.0), 4),
            "provisional": bool((s.metadata or {}).get("provisional")),
        }
        for s in default_run.promoted
    ]
    payload = {
        "experiment": "exp02_skills",
        "experiment_id": "EXP-02",
        "seed": seed,
        "dataset_version": "synthetic-v1",
        "configuration": {"per_family": per_family},
        "thresholds": EXPERIMENT_META["success_thresholds"],
        "contribution": "SCT",
        "n_promotable_invariants": len(promotable),
        "admitted": len(default_run.promoted),
        "admitted_provisional": sum(1 for s in default_run.promoted
                                    if (s.metadata or {}).get("provisional")),
        "rejected_at_default": len(default_run.rejected),
        "admitted_at_strict_threshold": len(strict_run.promoted),
        "scv_gate_effective": len(strict_run.promoted) < len(default_run.promoted),
        "mean_scv": round(
            sum(float(s.scv or 0.0) for s in default_run.promoted)
            / len(default_run.promoted),
            4,
        )
        if default_run.promoted
        else 0.0,
        "mean_su": round(
            sum(float(s.utility or 0.0) for s in default_run.promoted)
            / len(default_run.promoted),
            4,
        )
        if default_run.promoted
        else 0.0,
        "metrics": {
            "SCV": round(
                sum(float(s.scv or 0.0) for s in default_run.promoted)
                / len(default_run.promoted),
                4,
            )
            if default_run.promoted
            else 0.0,
            "SU": round(
                sum(float(s.utility or 0.0) for s in default_run.promoted)
                / len(default_run.promoted),
                4,
            )
            if default_run.promoted
            else 0.0,
        },
        "skills": admitted,
        "rejection_reasons": [
            {"invariant_id": inv.invariant_id, "reasons": ", ".join(reasons)}
            for inv, reasons in default_run.rejected
        ],
    }
    if write:
        payload["artifacts"] = write_experiment(
            "exp02_skills", payload, root=_ROOT
        )
    return payload


def main_multi(*, seeds: tuple[int, ...] | None = None, write: bool = True) -> dict:
    """Run EXP-02 under the governed multi-seed policy."""
    return run_multi_seed(
        main,
        seeds=seeds or default_seeds(_ROOT),
        metric_paths={"SCV": "mean_scv", "SU": "mean_su"},
        experiment_id="EXP-02",
        configuration={"per_family": 6},
        thresholds=EXPERIMENT_META["success_thresholds"],
        write=write,
        root=_ROOT,
    )


if __name__ == "__main__":
    out = main()
    print("admitted=", out["admitted"], "strict=", out["admitted_at_strict_threshold"])
