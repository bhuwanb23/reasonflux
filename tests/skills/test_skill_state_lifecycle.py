"""Extended SkillState enum and transition table (Phase 11D-3)."""

from core.states import (
    SKILL_TRANSITIONS,
    SkillState,
    assert_transition,
    can_transition,
)
from skills import SkillConfig, reactivate_skill
from core.skill import Skill


def test_new_states_present():
    assert SkillState.GROWING.value == "growing"
    assert SkillState.CORE.value == "core"
    assert SkillState.ARCHIVED.value == "archived"


def test_active_tier_transitions():
    assert can_transition(SkillState.ACTIVE, SkillState.GROWING, SKILL_TRANSITIONS)
    assert can_transition(SkillState.GROWING, SkillState.CORE, SKILL_TRANSITIONS)
    assert can_transition(SkillState.CORE, SkillState.DORMANT, SKILL_TRANSITIONS)
    assert can_transition(SkillState.GROWING, SkillState.ACTIVE, SKILL_TRANSITIONS)


def test_fsm_allows_retired_and_archived_reactivation():
    assert can_transition(SkillState.RETIRED, SkillState.ACTIVE, SKILL_TRANSITIONS)
    assert can_transition(SkillState.ARCHIVED, SkillState.ACTIVE, SKILL_TRANSITIONS)
    assert can_transition(SkillState.RETIRED, SkillState.ARCHIVED, SKILL_TRANSITIONS)
    assert_transition(
        SkillState.ARCHIVED, SkillState.ACTIVE, SKILL_TRANSITIONS, "skill"
    )


def test_reactivate_skill_still_enforces_evidence_gates():
    skill = Skill(skill_id="r1", state=SkillState.RETIRED)
    cfg = SkillConfig(reactivate_min_evidence=2, reactivate_min_expected_su=0.0)
    blocked = reactivate_skill(
        skill, evidence_count=0, expected_su=1.0, config=cfg
    )
    assert not blocked.success
    assert "insufficient_evidence" in blocked.reasons
    assert skill.state is SkillState.RETIRED
