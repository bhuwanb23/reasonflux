"""Stage 7 — post-creation monitoring hooks (Phase 11D-1 / 11D-2).

Records reuse / transfer / negative events and refreshes Skill Utility.
Retirement decisions are 11D-3.
"""

from __future__ import annotations

import time
from typing import Any

from core.skill import Skill
from skills.config import SkillConfig
from skills.evidence import SkillEvidence, compute_skill_confidence
from skills.utility import refresh_skill_utility


def _evidence_of(skill: Skill) -> SkillEvidence:
    meta = skill.metadata or {}
    return SkillEvidence.from_dict(meta.get("evidence"))


def _write_evidence(skill: Skill, evidence: SkillEvidence) -> None:
    skill.metadata = dict(skill.metadata or {})
    skill.metadata["evidence"] = evidence.to_dict()
    skill.metadata["confidence"] = compute_skill_confidence(evidence)


def _refresh(skill: Skill, config: SkillConfig | None = None) -> None:
    refresh_skill_utility(skill, config)


def record_reuse(
    skill: Skill,
    *,
    task_id: str = "",
    detail: dict[str, Any] | None = None,
    config: SkillConfig | None = None,
) -> None:
    """Append a reuse event, bump reuse_count, refresh SU."""
    event = {"task_id": task_id, "timestamp": time.time(), **(detail or {})}
    skill.reuse_history = list(skill.reuse_history or [])
    skill.reuse_history.append(event)
    skill.reuse_count = int(skill.reuse_count) + 1
    evidence = _evidence_of(skill)
    evidence.utility = list(evidence.utility)
    evidence.utility.append({"kind": "reuse", **event})
    _write_evidence(skill, evidence)
    _refresh(skill, config)


def record_transfer(
    skill: Skill,
    *,
    source_family: str = "",
    target_family: str = "",
    success: bool = True,
    benefit: float = 0.0,
    config: SkillConfig | None = None,
) -> None:
    """Append a transfer outcome and refresh SU."""
    event = {
        "source_family": source_family,
        "target_family": target_family,
        "success": success,
        "benefit": benefit,
        "timestamp": time.time(),
    }
    skill.transfer_history = list(skill.transfer_history or [])
    skill.transfer_history.append(event)
    evidence = _evidence_of(skill)
    if success:
        evidence.transfer = list(evidence.transfer)
        evidence.transfer.append({"kind": "transfer", **event})
    else:
        evidence.negative = list(evidence.negative)
        evidence.negative.append({"kind": "negative_transfer", **event})
    _write_evidence(skill, evidence)
    _refresh(skill, config)


def record_negative(
    skill: Skill,
    *,
    reason: str = "",
    detail: dict[str, Any] | None = None,
    config: SkillConfig | None = None,
) -> None:
    """Record negative evidence and refresh SU."""
    event = {"reason": reason, "timestamp": time.time(), **(detail or {})}
    evidence = _evidence_of(skill)
    evidence.negative = list(evidence.negative)
    evidence.negative.append({"kind": "negative", **event})
    _write_evidence(skill, evidence)
    _refresh(skill, config)
