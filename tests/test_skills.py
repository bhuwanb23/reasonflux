"""Smoke / package export tests for skills (Phase 11D-1)."""

from skills import (
    SkillConfig,
    SkillCreationTrigger,
    SkillLibrary,
    compute_portfolio_metrics,
    compute_su,
    create_skills_from_invariants,
    promote_skill,
    rank_by_utility,
    retrieve_skills,
)


def test_skills_package_exports():
    assert SkillConfig is not None
    assert SkillCreationTrigger is not None
    assert SkillLibrary is not None
    assert callable(create_skills_from_invariants)
    assert callable(promote_skill)
    assert callable(retrieve_skills)
    assert callable(compute_su)
    assert callable(rank_by_utility)
    assert callable(compute_portfolio_metrics)
