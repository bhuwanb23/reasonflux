"""Layer evaluators wrapping existing CGM metrics (Phase 11E-4)."""

from __future__ import annotations

from capability.library import CapabilityLibrary
from capability.portfolio import compute_system_capability_state
from evaluation.harness.config import HarnessConfig
from evaluation.harness.models import EvaluationSnapshot, LayerResult
from evaluation.intelligence_state import compute_system_intelligence_state
from skills.library import SkillLibrary


def evaluate_invariant_layer(
    skill_library: SkillLibrary, config: HarnessConfig | None = None
) -> LayerResult:
    """Proxy IS from skill metadata / categories present."""
    del config
    cats = set()
    for s in skill_library.list_skills():
        cat = str((s.metadata or {}).get("mvp_category") or "").strip().lower()
        if cat and cat != "general":
            cats.add(cat)
    n = len(skill_library)
    precision = min(1.0, len(cats) / max(1, n)) if n else 0.0
    is_proxy = float(len(cats))
    passed = len(cats) >= 1 and n >= 1
    return LayerResult(
        "invariant",
        passed,
        {"is_proxy": is_proxy, "precision": precision, "n_categories": float(len(cats))},
        notes=[] if passed else ["no_categories"],
    )


def evaluate_skill_layer(
    skill_library: SkillLibrary, config: HarnessConfig | None = None
) -> LayerResult:
    cfg = config or HarnessConfig()
    skills = skill_library.list_skills()
    if not skills:
        return LayerResult("skill", False, {}, ["empty_library"])
    mean_su = sum(float(s.utility or 0.0) for s in skills) / len(skills)
    reuse = sum(int(s.reuse_count or 0) for s in skills)
    mean_ts = sum(float(s.transfer_score or 0.0) for s in skills) / len(skills)
    health = max(0.0, min(1.0, 0.4 * mean_su + 0.3 * mean_ts + 0.3 * min(1.0, reuse / 5.0)))
    passed = mean_su > 0 and reuse >= cfg.min_reuse_success and mean_ts >= 0
    return LayerResult(
        "skill",
        passed,
        {
            "mean_su": mean_su,
            "reuse": float(reuse),
            "mean_ts": mean_ts,
            "health": health,
        },
        notes=[] if passed else ["weak_skills"],
    )


def evaluate_transfer_layer(
    skill_library: SkillLibrary, config: HarnessConfig | None = None
) -> LayerResult:
    cfg = config or HarnessConfig()
    attempts = 0
    negative = 0
    successes = 0
    families: set[str] = set()
    for s in skill_library.list_skills():
        for ev in s.transfer_history or []:
            attempts += 1
            ok = bool(ev.get("success", True))
            if ok:
                successes += 1
            else:
                negative += 1
            fam = str(ev.get("target_family") or "").strip().lower()
            if fam:
                families.add(fam)
    mean_ts = 0.0
    skills = skill_library.list_skills()
    if skills:
        mean_ts = sum(float(s.transfer_score or 0.0) for s in skills) / len(skills)
    ntr = (negative / attempts) if attempts else 0.0
    tu = mean_ts * (successes / max(1, attempts)) * min(1.0, len(families) / 3.0)
    passed = mean_ts > 0 and ntr <= cfg.max_ntr_success and attempts > 0
    return LayerResult(
        "transfer",
        passed,
        {
            "mean_ts": mean_ts,
            "tu": tu,
            "ntr": ntr,
            "diversity": float(len(families)),
            "attempts": float(attempts),
        },
        notes=[] if passed else ["weak_transfer"],
    )


def evaluate_capability_layer(
    capability_library: CapabilityLibrary,
    skill_library: SkillLibrary,
    *,
    previous_score: float | None = None,
    previous_cgr: float | None = None,
    config: HarnessConfig | None = None,
) -> LayerResult:
    cfg = config or HarnessConfig()
    snap = compute_system_capability_state(
        capability_library,
        skill_library,
        previous_score=previous_score,
        previous_cgr=previous_cgr,
        dt=cfg.default_dt,
    )
    cov = float(snap.portfolio.total_coverage if snap.portfolio else 0.0)
    passed = (
        snap.cgr >= cfg.min_cgr_success
        or (previous_score is None and snap.capability_score > 0)
    ) and snap.capability_score >= 0
    # For first snapshot without history, require positive score + non-empty caps
    if previous_score is None:
        passed = snap.capability_score > 0 and len(capability_library) > 0
    else:
        passed = snap.cgr >= cfg.min_cgr_success
    return LayerResult(
        "capability",
        passed,
        {
            "capability_score": snap.capability_score,
            "cgr": snap.cgr,
            "coverage": cov,
            "n_caps": float(len(capability_library)),
        },
        notes=[] if passed else ["stagnant_capability"],
    )


def evaluate_intelligence_layer(
    capability_library: CapabilityLibrary,
    skill_library: SkillLibrary,
    *,
    previous_ig: float | None = None,
    previous_score: float | None = None,
    experiences: int = 10,
    config: HarnessConfig | None = None,
) -> LayerResult:
    cfg = config or HarnessConfig()
    composed = any(
        (s.metadata or {}).get("composed_from") for s in skill_library.list_skills()
    )
    intel = compute_system_intelligence_state(
        capability_library,
        skill_library,
        previous_ig=previous_ig,
        previous_capability_score=previous_score,
        experiences=experiences,
        dt=cfg.default_dt,
        cp=0.3 if composed else 0.0,
        ad=0.2 if composed else 0.0,
        new_families=1 if composed else 0,
    )
    if previous_ig is None:
        passed = intel.ig > 0
    else:
        # Accept positive IGR, or non-decreasing IG with positive IE.
        passed = (
            intel.igr >= cfg.min_igr_success
            or (intel.ig >= float(previous_ig) and intel.ie > 0)
        )
    return LayerResult(
        "intelligence",
        passed,
        {
            "ig": intel.ig,
            "igr": intel.igr,
            "ie": intel.ie,
            "elasticity": intel.elasticity,
        },
        notes=[] if passed else ["weak_intelligence"],
    )


def build_snapshot(
    step: int,
    capability_library: CapabilityLibrary,
    skill_library: SkillLibrary,
    *,
    previous_score: float | None = None,
    previous_ig: float | None = None,
    experiences: int = 10,
    config: HarnessConfig | None = None,
) -> EvaluationSnapshot:
    cfg = config or HarnessConfig()
    cap = compute_system_capability_state(
        capability_library,
        skill_library,
        previous_score=previous_score,
        dt=cfg.default_dt,
    )
    composed = any(
        (s.metadata or {}).get("composed_from") for s in skill_library.list_skills()
    )
    intel = compute_system_intelligence_state(
        capability_library,
        skill_library,
        previous_ig=previous_ig,
        previous_capability_score=previous_score,
        experiences=experiences,
        dt=cfg.default_dt,
        cp=0.3 if composed else 0.0,
        ad=0.2 if composed else 0.0,
        new_families=1 if composed else 0,
    )
    xfer = evaluate_transfer_layer(skill_library, cfg)
    skill = evaluate_skill_layer(skill_library, cfg)
    return EvaluationSnapshot(
        step=step,
        capability_score=cap.capability_score,
        cgr=cap.cgr,
        ig=intel.ig,
        igr=intel.igr,
        coverage=float(cap.portfolio.total_coverage if cap.portfolio else 0.0),
        mean_su=float(skill.metrics.get("mean_su", 0.0)),
        mean_ts=float(xfer.metrics.get("mean_ts", 0.0)),
        ntr=float(xfer.metrics.get("ntr", 0.0)),
    )
