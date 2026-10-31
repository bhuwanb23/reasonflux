"""Run the Phase 13A readiness gates with one governed smoke seed."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT, ROOT / "src"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from baselines.dreamcoder_like.run import run as dreamcoder
from baselines.no_learning.run import run as no_learning
from baselines.random_skill_creation.run import run as random_skills
from baselines.skill_storage.run import run as skill_storage
from experiments._common import write_experiment
from experiments.exp01_invariants.run import main as run_invariants
from experiments.exp02_skills.run import main as run_skills
from experiments.exp03_transfer.run import main as run_transfer
from experiments.exp04_growth.run import main as run_growth
from experiments.exp05_end_to_end.run import main as run_end_to_end


def _check(name: str, condition: bool, details: str) -> dict[str, object]:
    return {"name": name, "passed": bool(condition), "details": details}


def main(*, write: bool = True) -> dict[str, object]:
    """Evaluate IDT, SCT, transfer, CGM, baselines, and reporting gates."""
    checks: list[dict[str, object]] = []
    try:
        invariants = run_invariants(seed=0, write=False)
        checks.append(_check(
            "IDT readiness",
            invariants["n_validated"] > 0 and invariants["is_summary"]["mean"] > 0,
            f"validated={invariants['n_validated']} mean_IS={invariants['is_summary']['mean']}",
        ))
    except Exception as exc:
        checks.append(_check("IDT readiness", False, f"{type(exc).__name__}: {exc}"))

    try:
        skills = run_skills(seed=0, write=False)
        checks.append(_check(
            "SCT readiness",
            skills["admitted"] > 0 and skills["scv_gate_effective"],
            f"admitted={skills['admitted']} mean_SCV={skills['mean_scv']}",
        ))
    except Exception as exc:
        checks.append(_check("SCT readiness", False, f"{type(exc).__name__}: {exc}"))

    try:
        transfer = run_transfer(seed=0, write=False)
        checks.append(_check(
            "Transfer readiness",
            transfer["positive_transfer"] and transfer["mean_benefit"] > 0,
            f"records={transfer['n_transfer_records']} mean_benefit={transfer['mean_benefit']}",
        ))
    except Exception as exc:
        checks.append(_check("Transfer readiness", False, f"{type(exc).__name__}: {exc}"))

    try:
        growth = run_growth(seed=0, write=False)
        checks.append(_check(
            "CGM readiness",
            growth["success"],
            f"CGR={growth['metrics']['CGR']} IG={growth['metrics']['IG']} "
            f"intelligence_harness_success={growth['intelligence_success']}",
        ))
    except Exception as exc:
        checks.append(_check("CGM readiness", False, f"{type(exc).__name__}: {exc}"))

    try:
        e2e = run_end_to_end(seed=0, write=False)
        checks.append(_check(
            "End-to-end baseline readiness",
            e2e["success"] and e2e["beats_all_baselines"],
            f"success={e2e['success']} beats_all={e2e['beats_all_baselines']}",
        ))
    except Exception as exc:
        checks.append(_check(
            "End-to-end baseline readiness", False, f"{type(exc).__name__}: {exc}"
        ))

    try:
        baselines = [no_learning(), skill_storage(), random_skills(), dreamcoder()]
        checks.append(_check(
            "Baseline readiness",
            len(baselines) == 4 and all("capability_score" in row for row in baselines),
            f"baselines={len(baselines)}",
        ))
    except Exception as exc:
        checks.append(_check("Baseline readiness", False, f"{type(exc).__name__}: {exc}"))

    report_path = ROOT / "reports" / "experiments" / "phase13a_gates" / "record.json"
    if write:
        artifacts = write_experiment(
            "phase13a_gates",
            {
                "experiment_id": "PHASE-13A",
                "configuration": {"seed": 0, "mode": "smoke"},
                "results": checks,
                "checks": checks,
                "success": all(bool(check["passed"]) for check in checks),
                "failure_cases": [
                    check for check in checks if not bool(check["passed"])
                ],
                "observations": {
                    "scope": "readiness smoke checks, not formal multi-seed evidence"
                },
            },
            root=ROOT,
        )
        report_path = Path(artifacts["record_json"])

    return {
        "success": all(bool(check["passed"]) for check in checks),
        "checks": checks,
        "report": str(report_path),
    }


if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["success"] else 1)
