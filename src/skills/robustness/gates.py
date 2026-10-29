"""Robust skill promotion and retirement gates (Phase 11D-5)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.skill import Skill, SkillCandidate
from core.states import SkillState
from invariants.robustness.escalation import FailureLevel
from skills.library import SkillLibrary
from skills.robustness.config import SkillRobustnessConfig
from skills.robustness.edge_cases import is_ancient_core, rare_high_value_override
from skills.robustness.metrics import skill_ntr
from skills.robustness.sf_capability import detect_adversarial_formation
from skills.robustness.sf_creation import (
    detect_duplicates,
    detect_premature_skill,
    should_restrict_skill_promotion,
)


@dataclass(slots=True)
class SkillGateResult:
    """Outcome of a robust skill gate evaluation."""

    promotable: bool
    level: FailureLevel
    reasons: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "promotable": self.promotable,
            "level": self.level.value,
            "reasons": list(self.reasons),
            "metrics": dict(self.metrics),
        }


def evaluate_skill_promotion_gate(
    skill_or_candidate: Skill | SkillCandidate,
    *,
    library: SkillLibrary | None = None,
    config: SkillRobustnessConfig | None = None,
    ser: float | None = None,
    families: list[str] | None = None,
    tasks: int | None = None,
    ntr: float | None = None,
) -> SkillGateResult:
    """Evidence + transfer + utility + NTR + similarity + diversity + SER."""
    config = config or SkillRobustnessConfig()
    library = library or SkillLibrary()
    reasons: list[str] = []
    metrics: dict[str, Any] = {}

    if isinstance(skill_or_candidate, SkillCandidate):
        # Build a temporary Skill view for checks.
        skill = Skill.from_candidate(skill_or_candidate)
        skill.utility = float(skill_or_candidate.scv or 0.0)
        skill.metadata = dict(skill_or_candidate.metadata or {})
    else:
        skill = skill_or_candidate

    conf = float((skill.metadata or {}).get("confidence", 0.0) or 0.0)
    metrics["confidence"] = conf
    evidence = 0
    ev = (skill.metadata or {}).get("evidence") or {}
    if isinstance(ev, dict):
        evidence = max(
            len(ev.get("discovery") or []),
            len(ev.get("utility") or []),
            len(ev.get("transfer") or []),
        )
    metrics["evidence"] = evidence

    override = rare_high_value_override(skill, config)
    metrics["transfer_override"] = override
    premature = detect_premature_skill(skill, config)
    if premature and not override:
        reasons.append("evidence")
        if conf < config.min_confidence_promote:
            reasons.append("confidence")

    if float(skill.utility or 0.0) < float(config.min_utility_promote) and not override:
        reasons.append("utility")

    ntr_val = float(ntr) if ntr is not None else skill_ntr(skill)
    metrics["ntr"] = ntr_val
    if ntr_val > config.ntr_restrict:
        reasons.append("ntr")

    dups = detect_duplicates(skill, library, config)
    metrics["duplicates"] = len(dups)
    if dups:
        reasons.append("duplicate")

    if ser is not None:
        metrics["ser"] = ser
        if should_restrict_skill_promotion(ser, config):
            reasons.append("ser_restrict")

    if families is not None:
        adv = detect_adversarial_formation(families, tasks, config)
        metrics["tfd"] = adv.tfd
        if adv.blocked:
            reasons.append("low_tfd")

    level = FailureLevel.OK
    if reasons:
        level = FailureLevel.REJECTED
        if "ser_restrict" in reasons or "ntr" in reasons:
            level = FailureLevel.RESTRICTED
    promotable = not reasons
    return SkillGateResult(promotable, level, sorted(set(reasons)), metrics)


def confirm_skill_promotion(
    skill_or_candidate: Skill | SkillCandidate,
    *,
    library: SkillLibrary | None = None,
    config: SkillRobustnessConfig | None = None,
    ser: float | None = None,
    families: list[str] | None = None,
    tasks: int | None = None,
    ntr: float | None = None,
) -> SkillGateResult:
    """Evaluate promotion gate; does not create the skill (caller does)."""
    return evaluate_skill_promotion_gate(
        skill_or_candidate,
        library=library,
        config=config,
        ser=ser,
        families=families,
        tasks=tasks,
        ntr=ntr,
    )


def evaluate_skill_retirement_gate(
    skill: Skill,
    *,
    config: SkillRobustnessConfig | None = None,
) -> SkillGateResult:
    """Allow retirement only when low utility/transfer/reuse and no reactivation."""
    config = config or SkillRobustnessConfig()
    reasons: list[str] = []
    metrics: dict[str, Any] = {}

    if is_ancient_core(skill, config):
        return SkillGateResult(
            promotable=False,
            level=FailureLevel.OK,
            reasons=["ancient_core"],
            metrics={"protected": True},
        )

    util = float(skill.utility or 0.0)
    ts = float(skill.transfer_score or 0.0)
    reuse = int(skill.reuse_count or 0)
    metrics.update({"utility": util, "ts": ts, "reuse": reuse})

    low_u = util <= float(config.su_min)
    low_ts = ts <= float(config.retire_max_ts)
    low_reuse = reuse <= int(config.retire_max_reuse)
    reactivation = int((skill.metadata or {}).get("reactivations", 0) or 0) > 0
    last = dict((skill.metadata or {}).get("last_reactivation") or {})
    reactivation_signal = reactivation and bool(last.get("raised_utility", False))

    if not low_u:
        reasons.append("utility_not_low")
    if not low_ts:
        reasons.append("transfer_not_low")
    if not low_reuse:
        reasons.append("reuse_not_low")
    if reactivation_signal:
        reasons.append("reactivation_signal")

    # promotable here means "eligible to retire"
    eligible = not reasons
    level = FailureLevel.OK if eligible else FailureLevel.WARNING
    return SkillGateResult(eligible, level, reasons, metrics)
