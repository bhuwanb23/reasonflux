"""SU competition ranking and soft capacity."""

from core import Skill, SkillState
from skills import rank_by_utility, refresh_skill_utility, select_dominant


def _sk(sid, utility_fields):
    s = Skill(skill_id=sid, state=SkillState.ACTIVE, **utility_fields)
    refresh_skill_utility(s)
    return s


def test_higher_su_ranks_first():
    strong = _sk(
        "strong",
        dict(
            abstraction_gain=0.9,
            transfer_score=0.8,
            creation_cost=0.05,
            reuse_count=8,
            reuse_history=[{"impact": 1.0}] * 8,
            transfer_history=[
                {"success": True, "target_family": f"f{i}"} for i in range(4)
            ],
            metadata={"composition_potential": 0.7, "mvp_category": "reflection"},
        ),
    )
    weak = _sk(
        "weak",
        dict(
            abstraction_gain=0.1,
            transfer_score=0.1,
            creation_cost=0.2,
            reuse_count=0,
            metadata={"composition_potential": 0.1},
        ),
    )
    ranked = rank_by_utility([weak, strong])
    assert ranked[0].skill_id == "strong"
    assert ranked[0].utility > ranked[1].utility


def test_select_dominant_capacity():
    skills = [
        _sk(f"s{i}", dict(abstraction_gain=0.1 * i, creation_cost=0.05, reuse_count=i))
        for i in range(5)
    ]
    top = select_dominant(skills, capacity=2)
    assert len(top) == 2
    assert top[0].utility >= top[1].utility
