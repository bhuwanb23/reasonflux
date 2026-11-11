"""Skill failure taxonomy ids, levels, diagnosis shape."""

from core import Skill, SkillState
from skills import SkillFailure, SkillRobustnessConfig, diagnose_skill
from skills.robustness.taxonomy import FailureDiagnosis


def test_failure_enum_members():
    values = {f.value for f in SkillFailure}
    assert "sf1_premature" in values
    assert "sf8_adversarial" in values
    assert "ec3_zombie" in values
    assert len(values) == 12


def test_diagnose_returns_typed_diagnoses():
    skill = Skill(skill_id="t1", state=SkillState.ACTIVE)
    diags = diagnose_skill(
        skill,
        config=SkillRobustnessConfig(),
        ser=0.9,
        ntr=0.6,
        is_premature=True,
    )
    assert all(isinstance(d, FailureDiagnosis) for d in diags)
    failures = {d.failure for d in diags}
    assert SkillFailure.SF1 in failures
    assert SkillFailure.SF2 in failures
    assert SkillFailure.SF4 in failures
    payload = diags[0].to_dict()
    assert payload["skill_id"] == "t1"
    assert "level" in payload
