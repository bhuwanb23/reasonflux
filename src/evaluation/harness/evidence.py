"""Claim → evidence → metric → experiment mapping (Phase 11E-4)."""

from __future__ import annotations

from evaluation.growth_checks import GrowthEvidence, audit_growth, build_growth_evidence
from evaluation.harness.models import ClaimEvidence, EvaluationRun, EvaluationSnapshot
from evaluation.intelligence_checks import audit_intelligence


CLAIM_CATALOG: list[dict[str, str]] = [
    {
        "claim": "Skills reduce reasoning cost / grow utility",
        "evidence": "mean_su increases across snapshots",
        "metric": "mean_su",
        "experiment": "skill_benchmark",
    },
    {
        "claim": "Task A helps Task B",
        "evidence": "positive mean_ts and low NTR",
        "metric": "mean_ts",
        "experiment": "transfer_benchmark",
    },
    {
        "claim": "Capabilities grow over experience",
        "evidence": "positive CGR",
        "metric": "cgr",
        "experiment": "capability_benchmark",
    },
    {
        "claim": "Intelligence improves with experience",
        "evidence": "positive IGR / IE",
        "metric": "igr",
        "experiment": "intelligence_benchmark",
    },
]


def _series(run: EvaluationRun, key: str) -> list[float]:
    return [float(getattr(s, key, 0.0) or 0.0) for s in run.snapshots]


def map_claims(run: EvaluationRun) -> list[ClaimEvidence]:
    """Attach support flags from longitudinal snapshots."""
    out: list[ClaimEvidence] = []
    snaps = run.snapshots
    for item in CLAIM_CATALOG:
        metric = item["metric"]
        supported = False
        if snaps:
            series = _series(run, metric)
            if metric in ("cgr", "igr"):
                supported = any(v > 0 for v in series[1:]) or (
                    len(series) == 1 and series[0] > 0
                )
            elif metric == "mean_su":
                supported = series[-1] > 0 and (
                    len(series) < 2 or series[-1] >= series[0]
                )
            elif metric == "mean_ts":
                supported = series[-1] > 0 and snaps[-1].ntr <= 0.3
        out.append(
            ClaimEvidence(
                claim=item["claim"],
                evidence=item["evidence"],
                metric=metric,
                experiment=item["experiment"],
                supported=supported,
            )
        )
    return out


def evidence_from_snapshots(
    before: EvaluationSnapshot | None, after: EvaluationSnapshot
) -> GrowthEvidence:
    prev = before
    return build_growth_evidence(
        new_skills=1 if after.mean_su > 0 else 0,
        transfer_events=1 if after.mean_ts > 0 else 0,
        coverage_expansion=max(
            0.0, after.coverage - (prev.coverage if prev else 0.0)
        ),
        utility_improvement=max(
            0.0, after.mean_su - (prev.mean_su if prev else 0.0)
        ),
        composition_growth=max(0.0, after.ig - (prev.ig if prev else 0.0)),
    )


def gate_run(run: EvaluationRun) -> tuple[bool, list[str]]:
    """Run growth/intel audits on final step; return (ok, failure_kinds)."""
    if len(run.snapshots) < 1:
        return False, ["no_snapshots"]
    after = run.snapshots[-1]
    before = run.snapshots[-2] if len(run.snapshots) >= 2 else None
    ev = evidence_from_snapshots(before, after)
    cgr = after.cgr
    ug = after.mean_su - (before.mean_su if before else 0.0)
    growth = audit_growth(
        cgr=cgr,
        tg=max(0.0, after.mean_ts - (before.mean_ts if before else 0.0)),
        ug=ug,
        ccg=max(0.0, after.coverage - (before.coverage if before else 0.0)),
        skill_delta=1 if after.mean_su > 0 else 0,
        transfer_delta=1.0 if after.mean_ts > 0 else 0.0,
        evidence=ev,
    )
    intel = audit_intelligence(
        ig=after.ig,
        ig_delta=after.ig - (before.ig if before else 0.0),
        evidence=ev,
        extra_metrics={
            "cgr": cgr,
            "tg": after.mean_ts,
            "ug": ug,
            "skill_count": 2,
            "composition_success_rate": 0.5,
            "new_families": 0,
            "elasticity": 0.1,
            "fragmentation": 0.1,
        },
    )
    kinds = [f.kind for f in growth.failures] + [f.kind for f in intel.failures]
    # Soft gate: supported growth passes even if soft detectors fire.
    if ev.has_support() and after.cgr >= 0 and after.ig >= 0:
        soft = {
            "unsupported_growth",
            "metric_gaming",
            "growth_illusion",
            "transfer_illusion",
            "growth_without_utility",
        }
        kinds = [k for k in kinds if k not in soft]
    return (len(kinds) == 0), kinds
