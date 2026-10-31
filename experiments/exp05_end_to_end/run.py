"""exp05_end_to_end — full ASFT pipeline vs baselines vs ablations.

The paper-facing experiment: the complete pipeline must beat every baseline and
degrade under ablation. Ablations reuse the harness transforms in
:mod:`evaluation.harness.baselines` so the comparison is apples to apples.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
for _p in (_ROOT, _ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from baselines.dreamcoder_like.run import run as dreamcoder  # noqa: E402
from baselines.no_learning.run import run as no_learning  # noqa: E402
from baselines.random_skill_creation.run import run as random_skills  # noqa: E402
from baselines.skill_storage.run import run as skill_storage  # noqa: E402
from pipelines.full_asft_pipeline import run_full_asft_pipeline  # noqa: E402
from experiments._common import write_experiment, write_figure  # noqa: E402


def main(*, seed: int = 0, write: bool = True) -> dict:
    """Compare ASFT against all four baselines."""
    full = run_full_asft_pipeline(seed=seed)
    asft = {
        "name": "asft_full",
        "capability_score": round(full.summary["final_capability"], 4),
        "cgr": full.summary["cgr"],
        "ig": round(full.summary["ig"], 4),
        "reuse_credited": full.summary["reuse_credited"],
        "n_skills": full.summary["n_skills"],
    }

    baselines = [no_learning(), skill_storage(), random_skills(), dreamcoder()]
    beaten = all(asft["capability_score"] > b["capability_score"] for b in baselines)

    payload = {
        "experiment": "exp05_end_to_end",
        "contribution": "ASFT",
        "asft": asft,
        "baselines": [
            {
                "name": b["name"],
                "capability_score": round(b["capability_score"], 4),
                "cgr": b["cgr"],
                "ig": round(b["ig"], 4),
                "reuse_credited": b["reuse_credited"],
            }
            for b in baselines
        ],
        "beats_all_baselines": beaten,
        "success": bool(full.success),
        "rounds": [r.to_dict() for r in full.rounds],
        "summary": full.summary,
    }
    if write:
        payload["artifacts"] = {
            **write_experiment("exp05_end_to_end", payload, root=_ROOT),
            "figure": write_figure(
                "exp05_capability_growth",
                {
                    "capability": full.capability_scores,
                    "cgr": full.cgr_series,
                    "ig": full.ig_series,
                },
                title="ASFT capability, CGR, and IG across accumulated experience",
                ylabel="value",
                root=_ROOT,
            ),
        }
    return payload


if __name__ == "__main__":
    out = main()
    print("asft=", out["asft"]["capability_score"], "beats_all=", out["beats_all_baselines"])
