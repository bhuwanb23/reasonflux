"""Ecosystem audit aggregates failures."""

from capability.library import CapabilityLibrary
from capability.models import Capability
from capability.robustness.audit import (
    ScoreSnapshot,
    audit_capability_ecosystem,
)
from capability.robustness.config import CapabilityRobustnessConfig
from capability.robustness.taxonomy import CapabilityFailureKind
from core.skill import Skill
from core.states import SkillState
from evaluation.growth_checks import GrowthEvidence
from skills.library import SkillLibrary


def test_audit_aggregates_fragmentation_and_gate():
    skills = SkillLibrary()
    for i in range(4):
        skills.add(
            Skill(
                skill_id=f"s{i}",
                state=SkillState.ACTIVE,
                utility=0.1,
                transfer_score=0.1,
            )
        )
    caps = CapabilityLibrary()
    for i in range(4):
        caps.add(Capability(capability_id=f"c{i}", skill_ids=[f"s{i}"]))

    snaps = [
        ScoreSnapshot(cgr=0.0, mean_su=0.1, mean_ts=0.1, coverage=0.1, ig=0.1),
        ScoreSnapshot(cgr=0.05, mean_su=0.1, mean_ts=0.1, coverage=0.1, ig=0.1),
    ]
    result = audit_capability_ecosystem(
        caps,
        skills,
        snaps,
        config=CapabilityRobustnessConfig(),
        evidence=GrowthEvidence(new_skills=4),
        skill_delta=4,
        hard_gate=True,
    )
    kinds = {f.kind for f in result.failures}
    assert CapabilityFailureKind.CF2 in kinds or not result.ok
    assert result.growth_claim is not None
    assert result.growth_claim.accepted is False
    assert result.health is not None


def test_audit_ok_on_supported_growth():
    skills = SkillLibrary()
    skills.add(
        Skill(
            skill_id="s0",
            state=SkillState.ACTIVE,
            utility=0.8,
            transfer_score=0.7,
            transfer_history=[{"success": True}],
        )
    )
    skills.add(
        Skill(
            skill_id="s1",
            state=SkillState.ACTIVE,
            utility=0.7,
            transfer_score=0.6,
            transfer_history=[{"success": True}],
        )
    )
    caps = CapabilityLibrary()
    caps.add(Capability(capability_id="c0", skill_ids=["s0", "s1"], utility=0.75))

    snaps = [
        ScoreSnapshot(cgr=0.0, mean_su=0.4, mean_ts=0.3, coverage=0.2, ig=0.2),
        ScoreSnapshot(cgr=0.05, mean_su=0.6, mean_ts=0.5, coverage=0.4, ig=0.35),
    ]
    ev = GrowthEvidence(
        new_skills=1,
        transfer_events=2,
        coverage_expansion=0.2,
        utility_improvement=0.2,
        composition_growth=0.15,
    )
    result = audit_capability_ecosystem(
        caps,
        skills,
        snaps,
        evidence=ev,
        skill_delta=0,
        new_cap=0.2,
        existing_cap=1.0,
        hard_gate=True,
    )
    assert result.growth_claim is not None
    assert result.growth_claim.accepted is True
    assert result.ok is True
