"""Baselines A–D and ablations A1–A5 (Phase 11E-4)."""

from __future__ import annotations

from copy import deepcopy
from typing import Literal

from capability.library import CapabilityLibrary
from capability.models import Capability
from core.skill import Skill
from evaluation.harness.scenarios import ScenarioStep
from skills.library import SkillLibrary

BaselineId = Literal["A", "B", "C", "D", "none"]
AblationId = Literal["A1", "A2", "A3", "A4", "A5", "none"]


def _clone_skill(skill: Skill) -> Skill:
    return Skill.from_dict(skill.to_dict())


def _clone_cap(cap: Capability) -> Capability:
    return Capability.from_dict(cap.to_dict())


def _clone_step(step: ScenarioStep) -> ScenarioStep:
    skills = SkillLibrary()
    for s in step.skills.list_skills():
        skills.add(_clone_skill(s))
    caps = CapabilityLibrary()
    for c in step.capabilities.list_capabilities():
        caps.add(_clone_cap(c))
    return ScenarioStep(skills=skills, capabilities=caps)


def apply_baseline(steps: list[ScenarioStep], baseline: str | None) -> list[ScenarioStep]:
    """Transform scenario steps for baselines A–D."""
    if not baseline or baseline in ("none", "None"):
        return steps
    b = baseline.upper()
    out = [_clone_step(s) for s in steps]

    if b == "A":
        # No learning: freeze first step for all times.
        first = out[0]
        return [first for _ in out]

    if b == "B":
        # Skill storage only: keep skills, zero transfer history / scores.
        for step in out:
            for sk in step.skills.list_skills():
                sk.transfer_score = 0.0
                sk.transfer_history = []
        return out

    if b == "C":
        # Random skill creation: inflate count with low utility, no reuse.
        for step in out:
            for i in range(5):
                sid = f"rand-{i}"
                if step.skills.get(sid) is None:
                    from evaluation.harness.scenarios import _skill

                    step.skills.add(
                        _skill(
                            sid,
                            category="general",
                            utility=0.05,
                            ts=0.0,
                            families=[],
                            reuse=0,
                        )
                    )
                    step.skills.get(sid).transfer_history = []
        return out

    if b == "D":
        # DreamCoder-like: strong compression (high reuse) but flat transfer growth.
        for step in out:
            for sk in step.skills.list_skills():
                sk.reuse_count = max(5, int(sk.reuse_count or 0))
                sk.utility = max(float(sk.utility or 0.0), 0.5)
                # Cap transfer so economics look weaker than ASFT growth path.
                sk.transfer_score = min(0.3, float(sk.transfer_score or 0.0))
        return out

    return out


def apply_ablation(steps: list[ScenarioStep], ablation: str | None) -> list[ScenarioStep]:
    """Apply ablation flags A1–A5."""
    if not ablation or ablation in ("none", "None"):
        return steps
    a = ablation.upper()
    out = [_clone_step(s) for s in steps]

    if a == "A1":
        # Remove IDT: strip categories / invariant-like metadata.
        for step in out:
            for sk in step.skills.list_skills():
                meta = dict(sk.metadata or {})
                meta["mvp_category"] = "general"
                sk.metadata = meta
        return out

    if a == "A2":
        # Remove SCT: zero utility / no reuse growth.
        for step in out:
            for sk in step.skills.list_skills():
                sk.utility = 0.0
                sk.reuse_count = 0
                meta = dict(sk.metadata or {})
                meta["utility_breakdown"] = {"su": 0.0}
                sk.metadata = meta
        return out

    if a == "A3":
        # Remove skill library: empty skills/caps after first step.
        if not out:
            return out
        empty_s = SkillLibrary()
        empty_c = CapabilityLibrary()
        return [out[0]] + [ScenarioStep(empty_s, empty_c) for _ in out[1:]]

    if a == "A4":
        # Remove transfer.
        for step in out:
            for sk in step.skills.list_skills():
                sk.transfer_score = 0.0
                sk.transfer_history = []
        return out

    if a == "A5":
        # Remove CGM: flatten capability utilities / scores across steps.
        for step in out:
            for cap in step.capabilities.list_capabilities():
                cap.utility = 0.1
                cap.coverage = 0.0
            for sk in step.skills.list_skills():
                sk.utility = min(float(sk.utility or 0.0), 0.15)
                meta = dict(sk.metadata or {})
                meta["utility_breakdown"] = {"su": float(sk.utility)}
                sk.metadata = meta
        return out

    return out
