"""Skill failure taxonomy SF1–SF8 and EC1–EC4 (Phase 11D-5)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from core.skill import Skill
from invariants.robustness.escalation import FailureLevel
from skills.robustness.config import SkillRobustnessConfig


class SkillFailure(str, Enum):
    """Skill-side failure and edge-case identifiers."""

    SF1 = "sf1_premature"
    SF2 = "sf2_explosion"
    SF3 = "sf3_duplicate"
    SF4 = "sf4_negative_transfer"
    SF5 = "sf5_retrieval"
    SF6 = "sf6_composition"
    SF7 = "sf7_collapse"
    SF8 = "sf8_adversarial"
    EC1 = "ec1_rare_high_value"
    EC2 = "ec2_ancient_core"
    EC3 = "ec3_zombie"
    EC4 = "ec4_cannibalization"


@dataclass(slots=True)
class FailureDiagnosis:
    """One diagnosed skill failure with escalation level."""

    failure: SkillFailure
    level: FailureLevel
    reasons: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    skill_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "failure": self.failure.value,
            "level": self.level.value,
            "reasons": list(self.reasons),
            "metrics": dict(self.metrics),
            "skill_id": self.skill_id,
        }


def diagnose_skill(
    skill: Skill,
    *,
    config: SkillRobustnessConfig | None = None,
    ser: float | None = None,
    ntr: float | None = None,
    is_duplicate: bool = False,
    is_premature: bool = False,
    is_zombie: bool = False,
    is_ancient_core: bool = False,
) -> list[FailureDiagnosis]:
    """Collect applicable failure diagnoses for a skill (lightweight router)."""
    config = config or SkillRobustnessConfig()
    out: list[FailureDiagnosis] = []
    sid = skill.skill_id

    if is_premature:
        out.append(
            FailureDiagnosis(
                SkillFailure.SF1,
                FailureLevel.REJECTED,
                ["premature_creation"],
                {"confidence": float((skill.metadata or {}).get("confidence", 0.0))},
                sid,
            )
        )
    if ser is not None and ser >= config.ser_restrict:
        out.append(
            FailureDiagnosis(
                SkillFailure.SF2,
                FailureLevel.RESTRICTED,
                ["skill_explosion"],
                {"ser": ser},
                sid,
            )
        )
    elif ser is not None and ser >= config.ser_warn:
        out.append(
            FailureDiagnosis(
                SkillFailure.SF2,
                FailureLevel.WARNING,
                ["skill_explosion_warn"],
                {"ser": ser},
                sid,
            )
        )
    if is_duplicate:
        out.append(
            FailureDiagnosis(
                SkillFailure.SF3,
                FailureLevel.WARNING,
                ["duplicate"],
                {},
                sid,
            )
        )
    if ntr is not None:
        if ntr >= config.ntr_retire:
            level = FailureLevel.REJECTED
            reasons = ["ntr_retire"]
        elif ntr >= config.ntr_restrict:
            level = FailureLevel.RESTRICTED
            reasons = ["ntr_restrict"]
        elif ntr >= config.ntr_warn:
            level = FailureLevel.WARNING
            reasons = ["ntr_warn"]
        else:
            level = FailureLevel.OK
            reasons = []
        if reasons:
            out.append(
                FailureDiagnosis(
                    SkillFailure.SF4, level, reasons, {"ntr": ntr}, sid
                )
            )
    if is_zombie:
        out.append(
            FailureDiagnosis(
                SkillFailure.EC3,
                FailureLevel.BLACKLISTED,
                ["zombie"],
                {},
                sid,
            )
        )
    if is_ancient_core:
        out.append(
            FailureDiagnosis(
                SkillFailure.EC2,
                FailureLevel.OK,
                ["ancient_core_protect"],
                {},
                sid,
            )
        )
    return out
