"""Each CF fires on synthetic libs / series."""

from capability.library import CapabilityLibrary
from capability.models import Capability
from capability.robustness.config import CapabilityRobustnessConfig
from capability.robustness.detectors import (
    detect_cf1_growth_illusion,
    detect_cf2_fragmentation,
    detect_cf3_inflation,
    detect_cf4_transfer_collapse,
    detect_cf5_saturation,
    detect_cf6_regression,
    detect_cf7_metric_gaming,
    detect_cf8_overfitting,
    detect_cf9_intelligence_illusion,
    detect_cf10_collapse,
)
from capability.robustness.taxonomy import CapabilityFailureKind
from core.skill import Skill
from core.states import SkillState
from evaluation.growth_checks import GrowthEvidence
from skills.library import SkillLibrary


CFG = CapabilityRobustnessConfig()


def _skills(n: int, *, ts: float = 0.1, util: float = 0.1) -> SkillLibrary:
    lib = SkillLibrary()
    for i in range(n):
        lib.add(
            Skill(
                skill_id=f"s{i}",
                state=SkillState.ACTIVE,
                utility=util,
                transfer_score=ts,
                transfer_history=[{"success": True}],
            )
        )
    return lib


def test_cf1_skill_count_without_utility():
    hits = detect_cf1_growth_illusion(
        cgr=0.1,
        tg=0.0,
        ug=0.0,
        ccg=0.0,
        skill_delta=3,
        transfer_delta=0.0,
        evidence=GrowthEvidence(new_skills=3),
        config=CFG,
    )
    assert any(h.kind is CapabilityFailureKind.CF1 for h in hits)


def test_cf2_fragmentation():
    skills = _skills(3)
    caps = CapabilityLibrary()
    for i in range(3):
        caps.add(Capability(capability_id=f"c{i}", skill_ids=[f"s{i}"]))
    # FR = 3/3 = 1.0 > 0.8
    hits = detect_cf2_fragmentation(caps, skills, CFG)
    assert any(h.kind is CapabilityFailureKind.CF2 for h in hits)


def test_cf3_inflation_gap():
    skills = _skills(2)
    caps = CapabilityLibrary()
    caps.add(Capability(capability_id="c0", skill_ids=["s0", "s1"]))
    hits = detect_cf3_inflation(
        caps,
        skills,
        claimed_coverage=0.9,
        observed_coverage=0.1,
        config=CFG,
    )
    assert any(h.kind is CapabilityFailureKind.CF3 for h in hits)


def test_cf4_transfer_collapse():
    skills = _skills(2, ts=0.1)
    hits = detect_cf4_transfer_collapse(skills, prev_ts=0.8, config=CFG)
    assert any(h.kind is CapabilityFailureKind.CF4 for h in hits)


def test_cf5_saturation():
    hits = detect_cf5_saturation(new_cap=0.01, existing_cap=1.0, config=CFG)
    assert any(h.kind is CapabilityFailureKind.CF5 for h in hits)


def test_cf6_regression():
    hits = detect_cf6_regression([-0.1, -0.2], CFG)
    assert any(h.kind is CapabilityFailureKind.CF6 for h in hits)


def test_cf7_metric_gaming():
    hits = detect_cf7_metric_gaming(
        evidence=GrowthEvidence(),
        cgr=0.1,
        ug=0.0,
        tg=0.0,
        config=CFG,
    )
    assert any(h.kind is CapabilityFailureKind.CF7 for h in hits)


def test_cf8_overfitting():
    hits = detect_cf8_overfitting(
        train_success=0.95, holdout_success=0.2, config=CFG
    )
    assert any(h.kind is CapabilityFailureKind.CF8 for h in hits)


def test_cf9_stagnation():
    hits = detect_cf9_intelligence_illusion(
        ig=0.5,
        ig_delta=0.0,
        evidence=None,
        config=CFG,
    )
    assert any(h.kind is CapabilityFailureKind.CF9 for h in hits)


def test_cf10_collapse():
    hits = detect_cf10_collapse([-0.1, -0.2], CFG)
    assert any(h.kind is CapabilityFailureKind.CF10 for h in hits)
