"""SF3 duplicate skills and merge."""

from core import Skill, SkillState
from skills import SkillLibrary, SkillRobustnessConfig, merge_skills
from skills.robustness.sf_creation import detect_duplicates


def _skill(sid: str, **kw) -> Skill:
    base = dict(
        skill_id=sid,
        state=SkillState.ACTIVE,
        trigger_conditions=["reflect", "symmetry"],
    )
    base.update(kw)
    return Skill(**base)


def test_detect_duplicates_excludes_self():
    cfg = SkillRobustnessConfig(duplicate_similarity=0.8)
    lib = SkillLibrary()
    a = _skill("a")
    b = _skill("b")
    lib.add(a)
    lib.add(b)
    hits = detect_duplicates(a, lib, cfg)
    assert [h[0].skill_id for h in hits] == ["b"]


def test_merge_preserves_histories_and_retires_drop():
    lib = SkillLibrary()
    keep = _skill(
        "keep",
        reuse_count=2,
        reuse_history=[{"task_index": 1}, {"task_index": 2}],
        transfer_history=[{"success": True, "target_family": "f1"}],
    )
    drop = _skill(
        "drop",
        reuse_count=3,
        reuse_history=[{"task_index": 3}],
        transfer_history=[{"success": True, "target_family": "f2"}],
    )
    lib.add(keep)
    lib.add(drop)

    merged = merge_skills(keep, drop, lib)
    assert merged is keep
    assert keep.reuse_count == 5
    assert len(keep.reuse_history) == 3
    assert len(keep.transfer_history) == 2
    assert keep.metadata["merged_from"] == ["drop"]
    assert drop.state is SkillState.RETIRED
    assert lib.get("drop") is drop
