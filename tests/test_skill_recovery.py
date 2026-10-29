"""Recovery planning and application."""

from core import Skill, SkillState
from skills import SkillFailure, SkillRobustnessConfig
from skills.robustness.recovery import apply_recovery, plan_recovery
from skills.robustness.taxonomy import FailureDiagnosis
from invariants.robustness.escalation import FailureLevel


def test_plan_and_apply_demote():
    diag = FailureDiagnosis(
        SkillFailure.SF1, FailureLevel.REJECTED, ["premature_creation"], {}, "r1"
    )
    action = plan_recovery(diag)
    assert action.action == "demote"

    skill = Skill(skill_id="r1", state=SkillState.ACTIVE)
    apply_recovery(skill, action)
    assert skill.state is SkillState.CANDIDATE


def test_plan_and_apply_archive_is_terminal_not_delete():
    diag = FailureDiagnosis(
        SkillFailure.EC3, FailureLevel.BLACKLISTED, ["zombie"], {}, "r2"
    )
    action = plan_recovery(diag)
    assert action.action == "archive"
    skill = Skill(skill_id="r2", state=SkillState.RETIRED)
    apply_recovery(skill, action)
    assert skill.state is SkillState.ARCHIVED


def test_plan_ntr_warn_boosts_down_and_restrict_dormants():
    warn = FailureDiagnosis(
        SkillFailure.SF4, FailureLevel.WARNING, ["ntr_warn"], {}, "r3"
    )
    assert plan_recovery(warn).action == "demote_retrieval"
    restrict = FailureDiagnosis(
        SkillFailure.SF4, FailureLevel.RESTRICTED, ["ntr_restrict"], {}, "r4"
    )
    assert plan_recovery(restrict).action == "dormant"


def test_apply_recovery_boost_increases_metadata():
    diag = FailureDiagnosis(SkillFailure.SF5, FailureLevel.WARNING, ["low_rr"], {}, "r5")
    action = plan_recovery(diag)
    skill = Skill(skill_id="r5", state=SkillState.ACTIVE)
    apply_recovery(skill, action, config=SkillRobustnessConfig(retrieval_boost=0.3))
    assert skill.metadata["retrieval_boost"] == 0.3
