"""Isolated regression and metric-gaming probes on copied final portfolios."""
from __future__ import annotations

from typing import Any

from capability import Capability, CapabilityConfig, CapabilityLibrary
from core.skill import Skill
from core.states import SkillState
from evaluation.growth_config import GrowthConfig
from evaluation.growth_metrics import compute_cgr, compute_portfolio_capability
from skills.library import SkillLibrary


def _clone_portfolios(runtime: Any) -> tuple[SkillLibrary, CapabilityLibrary]:
    skills = SkillLibrary()
    for skill in runtime.library.list_skills():
        skills.add(Skill.from_dict(skill.to_dict()))
    caps = CapabilityLibrary()
    for cap in runtime.capabilities.list_capabilities():
        caps.add(Capability.from_dict(cap.to_dict()))
    return skills, caps


def run_isolated_robustness(runtime: Any, *, capability_config: CapabilityConfig | None = None, growth_config: GrowthConfig | None = None) -> dict[str, Any]:
    """Measure retirement regression and 20-skill gaming invariance, never mutate main run."""
    if not runtime.enable_capabilities:
        return {
            "status": "unavailable_no_capability_portfolio",
            "regression": {"status": "unavailable_no_capability_portfolio"},
            "growth_illusion": {"status": "unavailable_no_capability_portfolio"},
        }
    gc = growth_config or GrowthConfig()
    cap_config = capability_config or CapabilityConfig()
    base_skills, base_caps = _clone_portfolios(runtime)
    baseline = compute_portfolio_capability(base_caps, base_skills, config=cap_config, growth_config=gc)
    candidates = sorted(
        [
            s for s in base_skills.list_skills()
            if any(s.skill_id in c.skill_ids for c in base_caps.list_capabilities())
            and any(e.get("success") for e in (s.transfer_history or []))
        ],
        key=lambda s: s.skill_id,
    )
    retired_id = candidates[0].skill_id if candidates else ""
    if retired_id:
        for cap in base_caps.list_capabilities():
            cap.remove_skill(retired_id)
            if not cap.skill_ids:
                base_caps.archive(cap.capability_id)
        base_skills.remove(retired_id)
        after = compute_portfolio_capability(base_caps, base_skills, config=cap_config, growth_config=gc)
        decline = compute_cgr(current_c=after, previous_c=baseline)
        regression = {
            "status": "evaluated",
            "retired_skill_id": retired_id,
            "baseline_ct": baseline,
            "post_retirement_ct": after,
            "cgr": decline,
            "decrease_detected": decline < 0.0,
        }
    else:
        regression = {"status": "unavailable_no_measured_member_skill", "baseline_ct": baseline}

    dummy_skills, dummy_caps = _clone_portfolios(runtime)
    before = compute_portfolio_capability(dummy_caps, dummy_skills, config=cap_config, growth_config=gc)
    for i in range(20):
        dummy_skills.add(Skill(
            skill_id=f"adversarial-useless-{i:02d}",
            state=SkillState.ACTIVE,
            utility=0.0,
            transfer_score=0.0,
            metadata={"adversarial_dummy": True, "learned": False, "transfer_history": []},
        ))
    after_dummy = compute_portfolio_capability(dummy_caps, dummy_skills, config=cap_config, growth_config=gc)
    illusion = {
        "status": "evaluated",
        "baseline_empty": len(dummy_caps) == 0,
        "dummy_skills_added": 20,
        "ct_before": before,
        "ct_after": after_dummy,
        "delta": after_dummy - before,
        "unchanged_within_tolerance": abs(after_dummy - before) <= 1e-12,
        "dummy_skills_are_learned": False,
    }
    return {"status": "evaluated", "regression": regression, "growth_illusion": illusion}
