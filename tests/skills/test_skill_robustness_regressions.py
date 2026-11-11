"""Regression tests for 11D-5 review findings."""

from core import Skill, SkillState
from skills import SkillLibrary, SkillRobustnessConfig, audit_library, demote_skill
from skills.robustness.edge_cases import enforce_zombie_archive
from skills.robustness.gates import evaluate_skill_promotion_gate
from skills.robustness.metrics import skill_ntr
from skills.robustness.sf_creation import detect_duplicates, merge_skills


def test_ntr_does_not_double_count_overlapping_negative_evidence():
    """record_transfer writes both transfer_history and evidence.negative."""
    skill = Skill(
        skill_id="n1",
        state=SkillState.ACTIVE,
        transfer_history=[{"success": False}] + [{"success": True}] * 5,
        metadata={
            "evidence": {
                "negative": [{"kind": "negative_transfer", "success": False}],
                "transfer": [],
                "discovery": [],
                "utility": [],
            }
        },
    )
    assert skill_ntr(skill) == 1 / 6


def test_zombie_archive_from_active_reaches_archived():
    cfg = SkillRobustnessConfig(zombie_permanent_archive_attempts=2)
    skill = Skill(
        skill_id="z1",
        state=SkillState.ACTIVE,
        metadata={"reactivations": 2, "last_reactivation": {"raised_utility": False}},
    )
    assert enforce_zombie_archive(skill, cfg)
    assert skill.state is SkillState.ARCHIVED


def test_zombie_archive_noop_returns_false_no_metadata():
    cfg = SkillRobustnessConfig(zombie_permanent_archive_attempts=2)
    skill = Skill(
        skill_id="z2",
        state=SkillState.RETIRED,
        metadata={"reactivations": 2, "last_reactivation": {"raised_utility": True}},
    )
    assert not enforce_zombie_archive(skill, cfg)
    assert skill.state is SkillState.RETIRED
    assert "permanent_archive" not in (skill.metadata or {})


def test_duplicates_ignore_retired_corpses_and_empty_signatures():
    cfg = SkillRobustnessConfig(duplicate_similarity=0.8)
    lib = SkillLibrary()
    live = Skill(
        skill_id="live", state=SkillState.ACTIVE, trigger_conditions=["reflect"]
    )
    dead = Skill(
        skill_id="dead", state=SkillState.RETIRED, trigger_conditions=["reflect"]
    )
    empty_a = Skill(skill_id="ea", state=SkillState.ACTIVE, trigger_conditions=[])
    empty_b = Skill(skill_id="eb", state=SkillState.ACTIVE, trigger_conditions=[])
    for s in (live, dead, empty_a, empty_b):
        lib.add(s)

    assert detect_duplicates(live, lib, cfg) == []
    assert detect_duplicates(empty_a, lib, cfg) == []


def test_merge_winner_stays_promotable():
    cfg = SkillRobustnessConfig(duplicate_similarity=0.8)
    lib = SkillLibrary()
    keep = Skill(
        skill_id="keep",
        state=SkillState.ACTIVE,
        trigger_conditions=["reflect"],
        transfer_score=0.8,
        utility=0.5,
        metadata={
            "confidence": 0.9,
            "evidence": {"discovery": [{}, {}, {}], "utility": [], "transfer": []},
        },
    )
    drop = Skill(
        skill_id="drop", state=SkillState.ACTIVE, trigger_conditions=["reflect"]
    )
    lib.add(keep)
    lib.add(drop)
    merge_skills(keep, drop, lib)
    assert detect_duplicates(keep, lib, cfg) == []
    gate = evaluate_skill_promotion_gate(keep, library=lib, config=cfg, ser=0.1)
    assert "duplicate" not in gate.reasons


def test_ec1_override_does_not_bypass_utility_floor():
    cfg = SkillRobustnessConfig(transfer_override_min=0.7, min_utility_promote=0.4)
    poor = Skill(
        skill_id="poor",
        state=SkillState.ACTIVE,
        transfer_score=0.9,
        utility=-5.0,
        metadata={"confidence": 0.9, "evidence": {"discovery": [{}, {}, {}]}},
    )
    gate = evaluate_skill_promotion_gate(poor, library=SkillLibrary(), config=cfg)
    assert not gate.promotable
    assert "utility" in gate.reasons


def test_demote_does_not_strip_core():
    core = Skill(skill_id="core", state=SkillState.CORE)
    demote_skill(core)
    assert core.state is SkillState.CORE


def test_audit_does_not_retire_core_and_enforces_ser():
    cfg = SkillRobustnessConfig(
        ser_restrict=0.5,
        library_capacity=10,
        min_evidence_promote=2,
        ntr_warn=0.9,
        ntr_restrict=0.95,
        ntr_retire=1.0,
    )
    lib = SkillLibrary()
    core = Skill(
        skill_id="core",
        state=SkillState.CORE,
        utility=1.0,
        reuse_count=9,
        trigger_conditions=["reflect"],
        metadata={
            "confidence": 0.95,
            "evidence": {"discovery": [{}, {}, {}], "utility": [], "transfer": []},
        },
    )
    lib.add(core)
    for i in range(4):
        lib.add(
            Skill(
                skill_id=f"w{i}",
                state=SkillState.ACTIVE,
                utility=0.0,
                trigger_conditions=[f"t{i}"],
                metadata={"confidence": 0.1, "evidence": {"discovery": [{}, {}]}},
            )
        )
    report = audit_library(lib, config=cfg, validated_invariants=2, apply=True)
    assert core.state is SkillState.CORE
    live = [
        s
        for s in lib.list_skills()
        if s.state not in (SkillState.RETIRED, SkillState.ARCHIVED)
    ]
    assert len(live) <= 1  # ser_restrict 0.5 * 2 invariants
    assert report.metrics["ser_target"] == 1
    assert len(lib) == 5  # nothing deleted
