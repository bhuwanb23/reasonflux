"""SkillLibrary add/get/list/similar."""

from core import Skill, SkillState
from skills import SkillLibrary


def test_library_crud_and_similar():
    lib = SkillLibrary()
    s = Skill(
        skill_id="sk1",
        trigger_conditions=["apply_reflection", "find_symmetry"],
        state=SkillState.ACTIVE,
    )
    lib.add(s)
    assert lib.get("sk1") is s
    assert len(lib.list_skills(SkillState.ACTIVE)) == 1
    hits = lib.find_similar(["apply_reflection", "find_symmetry"], threshold=0.8)
    assert hits and hits[0][0].skill_id == "sk1"
    assert lib.remove("sk1")
    assert lib.get("sk1") is None
