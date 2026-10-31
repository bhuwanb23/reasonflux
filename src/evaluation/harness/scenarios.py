"""Synthetic benchmark scenarios L1–L4 (Phase 11E-4)."""

from __future__ import annotations

from dataclasses import dataclass
import random

from capability.library import CapabilityLibrary
from capability.models import Capability, CapabilityType
from core.skill import Skill
from core.states import SkillState
from skills.library import SkillLibrary

FAMILIES = ("reflection", "rotation", "counting", "grouping")


@dataclass(slots=True)
class ScenarioStep:
    skills: SkillLibrary
    capabilities: CapabilityLibrary


def _skill(
    sid: str,
    *,
    category: str,
    utility: float,
    ts: float,
    families: list[str],
    reuse: int = 1,
    composed: bool = False,
    arc: bool = False,
) -> Skill:
    meta = {
        "mvp_category": category,
        "utility_breakdown": {"su": utility},
    }
    if composed:
        meta["composed_from"] = ["a", "b"]
    if arc:
        meta["arc_family"] = category
    return Skill(
        skill_id=sid,
        state=SkillState.ACTIVE,
        utility=utility,
        transfer_score=ts,
        reuse_count=reuse,
        transfer_history=[
            {"target_family": f, "success": True} for f in families
        ],
        metadata=meta,
    )


def _cap(cid: str, skill_ids: list[str], *, utility: float = 0.0) -> Capability:
    return Capability(
        capability_id=cid,
        skill_ids=list(skill_ids),
        utility=utility,
        capability_type=CapabilityType.COMPOSITE,
    )


def scenario_skill_formation() -> list[ScenarioStep]:
    """L1: synthetic skill formation over 2 steps."""
    s0 = SkillLibrary()
    s0.add(_skill("reflect", category="reflection", utility=0.3, ts=0.2, families=["geo"], reuse=1))
    c0 = CapabilityLibrary()
    c0.add(_cap("geo", ["reflect"], utility=0.3))

    s1 = SkillLibrary()
    s1.add(_skill("reflect", category="reflection", utility=0.6, ts=0.5, families=["geo", "algebra"], reuse=3))
    s1.add(_skill("rotate", category="rotation", utility=0.5, ts=0.4, families=["geo"], reuse=2))
    c1 = CapabilityLibrary()
    c1.add(_cap("geo", ["reflect", "rotate"], utility=0.55))
    return [ScenarioStep(s0, c0), ScenarioStep(s1, c1)]


def scenario_transfer() -> list[ScenarioStep]:
    """L2: transfer across families."""
    steps = scenario_skill_formation()
    s2 = SkillLibrary()
    for sk in steps[-1].skills.list_skills():
        s2.add(
            _skill(
                sk.skill_id,
                category=str((sk.metadata or {}).get("mvp_category") or "geo"),
                utility=float(sk.utility) + 0.1,
                ts=min(1.0, float(sk.transfer_score) + 0.2),
                families=["geo", "algebra", "objects"],
                reuse=max(2, int(sk.reuse_count)),
                composed=True,
            )
        )
    c2 = CapabilityLibrary()
    c2.add(_cap("geo", [s.skill_id for s in s2.list_skills()], utility=0.7))
    return list(steps) + [ScenarioStep(s2, c2)]


def scenario_capability_growth() -> list[ScenarioStep]:
    """L3: long sequence with rising CapU / coverage."""
    steps = scenario_transfer()
    # Continue from last transfer step — strictly stronger utilities/TS.
    prev = steps[-1]
    s3 = SkillLibrary()
    for sk in prev.skills.list_skills():
        cat = str((sk.metadata or {}).get("mvp_category") or "reflection")
        s3.add(
            _skill(
                sk.skill_id,
                category=cat,
                utility=min(0.98, float(sk.utility) + 0.25),
                ts=min(0.98, float(sk.transfer_score) + 0.25),
                families=["geo", "algebra", "objects", cat],
                reuse=max(4, int(sk.reuse_count) + 2),
                composed=True,
            )
        )
    for i, fam in enumerate(("counting", "grouping")):
        sid = f"sk-{fam}"
        if s3.get(sid) is None:
            s3.add(
                _skill(
                    sid,
                    category=fam,
                    utility=0.8 + 0.05 * i,
                    ts=0.75 + 0.05 * i,
                    families=[fam, "geo", "algebra"],
                    reuse=5 + i,
                    composed=True,
                )
            )
    c3 = CapabilityLibrary()
    ids = [s.skill_id for s in s3.list_skills()]
    c3.add(_cap("multi", ids, utility=0.95))
    c3.add(
        Capability(
            capability_id="emergent",
            skill_ids=ids[:2],
            utility=0.9,
            capability_type=CapabilityType.EMERGENT,
        )
    )
    return list(steps) + [ScenarioStep(s3, c3)]


def scenario_arc_validation() -> list[ScenarioStep]:
    """L4: ARC-tagged synthetic families (no dataset download)."""
    base = scenario_capability_growth()
    s = SkillLibrary()
    for fam in FAMILIES:
        s.add(
            _skill(
                f"arc-{fam}",
                category=fam,
                utility=0.7,
                ts=0.65,
                families=[fam, "arc"],
                reuse=4,
                composed=True,
                arc=True,
            )
        )
    caps = CapabilityLibrary()
    caps.add(_cap("arc-portfolio", [sk.skill_id for sk in s.list_skills()], utility=0.8))
    return list(base) + [ScenarioStep(s, caps)]


def scenario_flat_no_learning() -> list[ScenarioStep]:
    """Baseline A style: static weak skills, no growth."""
    s = SkillLibrary()
    s.add(_skill("lonely", category="reflection", utility=0.1, ts=0.0, families=[], reuse=0))
    # empty transfer history intentionally
    s.get("lonely").transfer_history = []
    c = CapabilityLibrary()
    c.add(_cap("static", ["lonely"], utility=0.1))
    return [ScenarioStep(s, c), ScenarioStep(s, c)]


SCENARIO_BUILDERS = {
    "skill": scenario_skill_formation,
    "transfer": scenario_transfer,
    "capability": scenario_capability_growth,
    "intelligence": scenario_capability_growth,
    "arc": scenario_arc_validation,
    "flat": scenario_flat_no_learning,
}


def build_scenario(level: str, *, seed: int = 0) -> list[ScenarioStep]:
    key = str(level or "capability").lower()
    builder = SCENARIO_BUILDERS.get(key) or SCENARIO_BUILDERS["capability"]
    steps = builder()
    # Keep the mechanism fixed while making each governed seed an independent
    # draw from the synthetic benchmark. The small perturbation preserves all
    # gate thresholds and prevents false precision from identical seed runs.
    rng = random.Random(int(seed))
    if seed:
        for step in steps:
            for skill in step.skills.list_skills():
                skill.utility = max(0.0, min(1.0, float(skill.utility) + rng.uniform(-0.01, 0.01)))
                skill.transfer_score = max(
                    0.0, min(1.0, float(skill.transfer_score) + rng.uniform(-0.01, 0.01))
                )
    return steps
