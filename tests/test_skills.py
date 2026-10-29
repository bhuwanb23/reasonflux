"""Smoke / package export tests for skills (Phase 11D-1)."""

from skills import (
    SkillConfig,
    SkillCreationTrigger,
    SkillLibrary,
    create_skills_from_invariants,
    promote_skill,
    retrieve_skills,
)


def test_skills_package_exports():
    assert SkillConfig is not None
    assert SkillCreationTrigger is not None
    assert SkillLibrary is not None
    assert callable(create_skills_from_invariants)
    assert callable(promote_skill)
    assert callable(retrieve_skills)
