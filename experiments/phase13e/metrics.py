"""Frozen Phase 13E portfolio, CGR, intelligence, and robustness measures."""
from __future__ import annotations

from typing import Any

from capability import compute_capability_portfolio, compute_system_capability_state
from capability.failures import audit_representation
from evaluation.growth_metrics import compute_ig, compute_saturation_ratio
from evaluation.intelligence import compute_ie, compute_igr

from .common import capability_config_from_json, growth_config_from_json


def _system_family_coverage(runtime: Any, families: tuple[str, ...]) -> float:
    supported: set[str] = set()
    if not runtime.enable_capabilities:
        return 0.0
    for cap in runtime.capabilities.list_capabilities():
        if cap.state.value == "archived":
            continue
        for sid in cap.skill_ids:
            skill = runtime.library.get(sid)
            if skill is None:
                continue
            for event in skill.transfer_history or []:
                if event.get("success"):
                    family = str(event.get("target_family", ""))
                    if family in families:
                        supported.add(family)
    return len(supported) / max(1, len(families))


def summarize_round(
    runtime: Any,
    *,
    round_index: int,
    previous: dict[str, float] | None,
    experiences: int,
    task_utility_mean: float,
    new_capabilities: int,
    config: dict[str, Any],
) -> dict[str, Any]:
    """Compute round measures using existing global APIs; optionally mask A5."""
    if runtime.mask_growth:
        measured_skills = [s for s in runtime.library.list_skills() if not (s.metadata or {}).get("provisional")]
        return {
            "arm": runtime.arm,
            "round": int(round_index) + 1,
            "n_skills_total": len(runtime.library),
            "n_skills_measured": len(measured_skills),
            "n_capabilities": None,
            "new_capabilities": None,
            "fragmentation_ratio": None,
            "saturation_ratio": None,
            "growth_state": "unavailable_by_design_no_CGM",
            "ct": None, "cgr": None, "capu": None,
            "portfolio_coverage": None, "supported_family_coverage": None,
            "mean_skill_utility_su": None, "mean_transfer_score_ts": None,
            "tg": None, "ug": None, "ccg": None,
            "composition_skill_count": None, "compg": None,
            "ig": None, "igr": None, "ie": None,
            "task_utility": float(task_utility_mean),
            "experiences": int(experiences),
            "capability_ids": None, "capability_states": None,
            "representation_failures": None,
            "measurement_status": "unavailable_by_design_no_CGM",
            "_next_state": {"ct": 0.0, "tg": 0.0, "ug": 0.0, "supported_coverage": 0.0, "comp": 0.0, "ig": 0.0},
        }
    prev = previous or {"ct": 0.0, "tg": 0.0, "ug": 0.0, "supported_coverage": 0.0, "comp": 0.0, "ig": 0.0}
    families = tuple(config["task_families"])
    gc = growth_config_from_json(config)
    cap_config = capability_config_from_json(config)
    if runtime.enable_capabilities:
        snap = compute_system_capability_state(
            runtime.capabilities,
            runtime.library,
            config=cap_config,
            growth_config=gc,
            previous_score=float(prev["ct"]),
            new_capability=float(new_capabilities),
            dt=float(config["growth_config"]["dt_per_round"]),
        )
        portfolio = compute_capability_portfolio(runtime.capabilities, runtime.library, cap_config, refresh=True)
        ct = float(snap.capability_score)
        cgr = float(snap.cgr)
        coverage = float(portfolio.total_coverage)
        cap_count = len([c for c in runtime.capabilities.list_capabilities() if c.state.value != "archived"])
        capu = float(portfolio.mean_capu)
    else:
        ct = cgr = coverage = capu = 0.0
        cap_count = 0
    skills = [s for s in runtime.library.list_skills() if not (s.metadata or {}).get("provisional")]
    ts = sum(float(s.transfer_score or 0.0) for s in skills) / len(skills) if skills else 0.0
    su = sum(float(s.utility or 0.0) for s in skills) / len(skills) if skills else 0.0
    comp_count = sum(1 for s in skills if (s.metadata or {}).get("composed_from"))
    family_coverage = _system_family_coverage(runtime, families)
    tg = ts - float(prev["tg"])
    ug = capu - float(prev["ug"])
    ccg = family_coverage - float(prev["supported_coverage"])
    compg = float(comp_count) - float(prev["comp"])
    ig = compute_ig(cgr, tg=tg, ug=ug, ccg=ccg, compg=compg, growth_config=gc)
    igr = compute_igr(ig, float(prev["ig"]), dt=float(config["growth_config"]["dt_per_round"]))
    ie = compute_ie(ig, experiences)
    representation = audit_representation(runtime.capabilities, runtime.library, cap_config) if runtime.enable_capabilities else []
    row = {
        "arm": runtime.arm,
        "round": int(round_index) + 1,
        "n_skills_total": len(runtime.library),
        "n_skills_measured": len(skills),
        "n_capabilities": cap_count,
        "new_capabilities": int(new_capabilities),
        "fragmentation_ratio": cap_count / max(1, len(runtime.library)),
        "saturation_ratio": compute_saturation_ratio(float(new_capabilities), float(cap_count - new_capabilities)),
        "growth_state": snap.growth_state if runtime.enable_capabilities else "unavailable_no_CGM",
        "ct": ct,
        "cgr": cgr,
        "capu": capu,
        "portfolio_coverage": coverage,
        "supported_family_coverage": family_coverage,
        "mean_skill_utility_su": su,
        "mean_transfer_score_ts": ts,
        "tg": tg,
        "ug": ug,
        "ccg": ccg,
        "composition_skill_count": comp_count,
        "compg": compg,
        "ig": ig,
        "igr": igr,
        "ie": ie,
        "task_utility": float(task_utility_mean),
        "experiences": int(experiences),
        "capability_ids": [c.capability_id for c in runtime.capabilities.list_capabilities() if c.state.value != "archived"],
        "capability_states": {c.capability_id: c.state.value for c in runtime.capabilities.list_capabilities()},
        "representation_failures": [f.to_dict() for f in representation],
        "measurement_status": "available",
    }
    row["_next_state"] = {"ct": ct, "tg": ts, "ug": capu, "supported_coverage": family_coverage, "comp": float(comp_count), "ig": ig}
    return row
