"""End-to-end library robustness audit."""

from core import Skill, SkillState
from skills import SkillLibrary, SkillRobustnessConfig, audit_library


def test_audit_keeps_core_retires_harmful_and_bounds_library():
    cfg = SkillRobustnessConfig(
        library_capacity=3,
        ntr_retire=0.5,
        ntr_restrict=0.3,
        ntr_warn=0.2,
        min_evidence_promote=2,
        min_confidence_promote=0.4,
        audit_max_actions=5,
        collapse_periods=2,
        cgr_collapse=-0.05,
    )
    lib = SkillLibrary()
    core = Skill(
        skill_id="core",
        state=SkillState.CORE,
        utility=1.0,
        reuse_count=9,
        trigger_conditions=["reflect"],
        transfer_score=0.9,
        metadata={
            "confidence": 0.95,
            "evidence": {"discovery": [{}, {}, {}], "utility": [], "transfer": []},
            "lifecycle": {"age_tasks": 10},
        },
    )
    harmful = Skill(
        skill_id="harmful",
        state=SkillState.ACTIVE,
        utility=0.1,
        trigger_conditions=["count"],
        transfer_history=[{"success": False}] * 4 + [{"success": True}],
        metadata={"confidence": 0.5, "evidence": {"discovery": [{}, {}], "utility": [], "transfer": []}},
    )
    weak1 = Skill(
        skill_id="weak1",
        state=SkillState.ACTIVE,
        utility=0.0,
        trigger_conditions=["rotate"],
        metadata={"confidence": 0.1, "evidence": {"discovery": []}},
    )
    weak2 = Skill(
        skill_id="weak2",
        state=SkillState.ACTIVE,
        utility=0.0,
        trigger_conditions=["group"],
        metadata={"confidence": 0.1, "evidence": {"discovery": []}},
    )
    for s in (core, harmful, weak1, weak2):
        lib.add(s)

    report = audit_library(
        lib,
        config=cfg,
        asu_series=[1.0, 0.8, 0.5],
        validated_invariants=2,
        apply=True,
    )

    assert report.metrics["ser"] == 2.0
    assert report.collapsed is True
    assert core.state is SkillState.CORE  # useful skill survives
    assert harmful.state in (SkillState.DORMANT, SkillState.RETIRED)
    assert weak1.state in (SkillState.CANDIDATE, SkillState.RETIRED)
    assert report.actions
    assert len(report.retired) >= 1
    assert len(lib) == 4  # no deletion
    assert lib.get("core") is core


def test_audit_dry_run_does_not_mutate():
    cfg = SkillRobustnessConfig(min_evidence_promote=3)
    lib = SkillLibrary()
    weak = Skill(
        skill_id="weak",
        state=SkillState.ACTIVE,
        metadata={"confidence": 0.0, "evidence": {"discovery": []}},
    )
    lib.add(weak)
    report = audit_library(lib, config=cfg, apply=False)
    assert weak.state is SkillState.ACTIVE
    assert report.skill_findings
    assert report.actions == []
