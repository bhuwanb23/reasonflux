"""SF4 negative transfer ladder."""

from core import Skill, SkillState
from skills import SkillRobustnessConfig
from skills.robustness.sf_transfer import (
    apply_transfer_health,
    assess_negative_transfer,
)


def _skill(sid: str, failures: int, successes: int = 0) -> Skill:
    history = [{"success": False}] * failures + [{"success": True}] * successes
    return Skill(
        skill_id=sid, state=SkillState.ACTIVE, transfer_history=history
    )


def test_ntr_ladder_warn_restrict_retire():
    cfg = SkillRobustnessConfig(ntr_warn=0.2, ntr_restrict=0.3, ntr_retire=0.5)

    clean = _skill("clean", 0, 5)
    assert assess_negative_transfer(clean, cfg).action == "none"

    warn = _skill("warn", 1, 3)  # ntr = 0.25
    health = assess_negative_transfer(warn, cfg)
    assert health.action == "demote_retrieval"
    apply_transfer_health(warn, health)
    assert warn.state is SkillState.ACTIVE
    assert warn.metadata["retrieval_boost"] < 0

    restrict = _skill("restrict", 2, 3)  # ntr = 0.4
    health = assess_negative_transfer(restrict, cfg)
    assert health.action == "dormant"
    apply_transfer_health(restrict, health)
    assert restrict.state is SkillState.DORMANT

    retire = _skill("retire", 4, 1)  # ntr = 0.8
    health = assess_negative_transfer(retire, cfg)
    assert health.action == "retire"
    apply_transfer_health(retire, health)
    assert retire.state is SkillState.RETIRED
