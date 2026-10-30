"""Claim → evidence → metric → experiment mapping (Phase 11E-4/5)."""

from __future__ import annotations

from capability.robustness.config import CapabilityRobustnessConfig
from capability.robustness.gates import validate_growth_claim
from evaluation.growth_checks import GrowthEvidence, audit_growth, build_growth_evidence
from evaluation.harness.config import HarnessConfig
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


def _delta(after: EvaluationSnapshot, before: EvaluationSnapshot | None, key: str) -> float:
    curr = float(getattr(after, key, 0.0) or 0.0)
    prev = float(getattr(before, key, 0.0) or 0.0) if before else 0.0
    return curr - prev


def evidence_from_snapshots(
    before: EvaluationSnapshot | None, after: EvaluationSnapshot
) -> GrowthEvidence:
    return build_growth_evidence(
        new_skills=1 if after.mean_su > (before.mean_su if before else 0.0) else 0,
        transfer_events=1 if after.mean_ts > (before.mean_ts if before else 0.0) else 0,
        coverage_expansion=max(0.0, _delta(after, before, "coverage")),
        utility_improvement=max(0.0, _delta(after, before, "mean_su")),
        composition_growth=max(0.0, _delta(after, before, "ig")),
    )


def gate_run(
    run: EvaluationRun,
    config: HarnessConfig | None = None,
) -> tuple[bool, list[str]]:
    """Validate growth claim; return (ok, failure_kinds).

    When ``hard_validation`` is True (default), acceptance requires the
    multi-signal hard gate; soft-filtering of gaming/illusion kinds is disabled.
    """
    cfg = config or HarnessConfig()
    if len(run.snapshots) < 1:
        return False, ["no_snapshots"]
    after = run.snapshots[-1]
    before = run.snapshots[-2] if len(run.snapshots) >= 2 else None
    # Longitudinal deltas (first→last) for the hard gate; adjacent for audits.
    origin = run.snapshots[0]
    ev = evidence_from_snapshots(origin, after)
    adj_ev = evidence_from_snapshots(before, after)

    transfer_delta = _delta(after, origin, "mean_ts")
    utility_delta = _delta(after, origin, "mean_su")
    coverage_delta = _delta(after, origin, "coverage")
    adj_ug = _delta(after, before, "mean_su")
    adj_tg = _delta(after, before, "mean_ts")
    adj_ccg = _delta(after, before, "coverage")

    meta = after.metadata or {}
    origin_meta = origin.metadata or {}
    skill_delta = max(
        0,
        int(meta.get("skill_count", 0) or 0)
        - int(origin_meta.get("skill_count", 0) or 0),
    )
    if skill_delta <= 0 and utility_delta > 0:
        skill_delta = 1
    skill_count = int(meta.get("skill_count", 0) or 0)
    if skill_count <= 0:
        skill_count = max(1, skill_delta + (1 if after.mean_su > 0 else 0))

    cgr = after.cgr
    ug = adj_ug
    tg = adj_tg

    growth = audit_growth(
        cgr=cgr,
        tg=max(0.0, tg),
        ug=ug,
        ccg=max(0.0, adj_ccg),
        skill_delta=skill_delta,
        transfer_delta=max(0.0, transfer_delta),
        evidence=adj_ev,
    )
    intel = audit_intelligence(
        ig=after.ig,
        ig_delta=after.ig - (before.ig if before else 0.0),
        evidence=adj_ev,
        extra_metrics={
            "cgr": cgr,
            "tg": after.mean_ts,
            "ug": ug,
            "ccg": adj_ccg,
            "skill_count": skill_count,
            "skill_delta": skill_delta,
            "transfer_delta": transfer_delta,
            "composition_success_rate": float(
                meta.get("composition_success_rate", 0.5)
            ),
            "new_families": int(meta.get("new_families", 0) or 0),
            "elasticity": float(meta.get("elasticity", 0.1)),
            "fragmentation": float(meta.get("fragmentation", 0.1)),
        },
    )
    kinds = [f.kind for f in growth.failures] + [f.kind for f in intel.failures]

    if cfg.hard_validation:
        rob = CapabilityRobustnessConfig(hard_validation=True, require_evidence=True)
        claim = validate_growth_claim(
            transfer_delta=transfer_delta,
            utility_delta=utility_delta,
            coverage_delta=coverage_delta,
            evidence=ev,
            skill_delta=skill_delta,
            cgr=cgr,
            config=rob,
        )
        if not claim.accepted:
            kinds = list(dict.fromkeys(kinds + claim.reasons))
            return False, kinds
        # Hard multi-signal rule passed — do not soft-filter; still report audit
        # kinds but they do not veto an evidence-backed multi-signal claim.
        return True, kinds

    # Legacy soft gate (hard_validation=False).
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
