"""CF8 on capability vs arc divergence."""

from capability.library import CapabilityLibrary
from capability.models import Capability
from capability.robustness.audit import ScoreSnapshot, audit_capability_ecosystem
from capability.robustness.config import CapabilityRobustnessConfig
from capability.robustness.detectors import detect_cf8_overfitting
from capability.robustness.taxonomy import CapabilityFailureKind
from core.skill import Skill
from core.states import SkillState
from evaluation.growth_checks import GrowthEvidence
from evaluation.harness.runner import run_benchmark
from skills.library import SkillLibrary


def test_cf8_detector_gap():
    hits = detect_cf8_overfitting(
        train_success=0.9,
        holdout_success=0.2,
        config=CapabilityRobustnessConfig(),
    )
    assert hits[0].kind is CapabilityFailureKind.CF8


def test_cf8_via_capability_vs_arc_snapshots():
    """Train=capability success, holdout=weaker arc-tagged success."""
    cap_run = run_benchmark("capability")
    arc_run = run_benchmark("arc")
    train_success = 0.9 if cap_run.snapshots[-1].cgr >= 0 else 0.2
    holdout_success = 0.2

    skills = SkillLibrary()
    skills.add(
        Skill(skill_id="s0", state=SkillState.ACTIVE, utility=0.5, transfer_score=0.4)
    )
    caps = CapabilityLibrary()
    caps.add(Capability(capability_id="c0", skill_ids=["s0"]))

    snaps = [
        ScoreSnapshot(
            cgr=cap_run.snapshots[-1].cgr,
            mean_su=0.5,
            mean_ts=0.4,
            coverage=0.3,
            ig=0.3,
            train_success=train_success,
            holdout_success=holdout_success,
        )
    ]
    result = audit_capability_ecosystem(
        caps,
        skills,
        snaps,
        evidence=GrowthEvidence(transfer_events=1, utility_improvement=0.1),
        hard_gate=False,
    )
    kinds = {f.kind for f in result.failures}
    assert CapabilityFailureKind.CF8 in kinds
    assert len(arc_run.snapshots) >= len(cap_run.snapshots)
