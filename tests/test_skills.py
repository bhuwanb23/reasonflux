"""Smoke / package export tests for skills (Phase 11D-1)."""

from skills import (
    SkillConfig,
    SkillCreationTrigger,
    SkillLibrary,
    apply_lifecycle,
    compute_cu,
    compute_health,
    compute_portfolio_metrics,
    compute_su,
    create_skills_from_invariants,
    evaluate_lifecycle,
    promote_skill,
    rank_by_utility,
    reactivate_skill,
    retire_skills,
    retrieve_skills,
    should_compose,
    try_compose,
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
    assert callable(evaluate_lifecycle)
    assert callable(apply_lifecycle)
    assert callable(retire_skills)
    assert callable(reactivate_skill)
    assert callable(compute_health)
    assert callable(try_compose)
    assert callable(should_compose)
    assert callable(compute_cu)
