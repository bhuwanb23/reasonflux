"""SF5 skill retrieval failure (Phase 11D-5)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from core.skill import Skill
from skills.library import SkillLibrary
from skills.robustness.config import SkillRobustnessConfig
from skills.robustness.metrics import retrieval_recall


def _norm(items: Sequence[str]) -> set[str]:
    return {str(x).lower().strip() for x in items if str(x).strip()}


def applicable_skills(
    library: SkillLibrary, requirements: Sequence[str]
) -> list[Skill]:
    """Skills whose triggers overlap requirements (any state except archived)."""
    req = _norm(requirements)
    hits: list[Skill] = []
    for skill in library.list_skills():
        if skill.state.value == "archived":
            continue
        triggers = _norm(skill.trigger_conditions or [])
        if req & triggers:
            hits.append(skill)
    return hits


@dataclass(slots=True)
class RetrievalDiagnosis:
    recall: float
    missed_ids: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)
    available_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "recall": self.recall,
            "missed_ids": list(self.missed_ids),
            "actions": list(self.actions),
            "available_ids": list(self.available_ids),
        }


def diagnose_retrieval_failure(
    requirements: Sequence[str],
    library: SkillLibrary,
    retrieved: Sequence[Skill] | Sequence[str],
    config: SkillRobustnessConfig | None = None,
) -> RetrievalDiagnosis:
    config = config or SkillRobustnessConfig()
    available = applicable_skills(library, requirements)
    avail_ids = [s.skill_id for s in available]
    if isinstance(retrieved, Sequence) and retrieved and isinstance(retrieved[0], Skill):
        ret_ids = [s.skill_id for s in retrieved]  # type: ignore[union-attr]
    else:
        ret_ids = [str(x) for x in retrieved]
    recall = retrieval_recall(ret_ids, avail_ids)
    missed = sorted(set(avail_ids) - set(ret_ids))
    actions: list[str] = []
    if recall < float(config.rr_min):
        actions.append("boost_missed")
        actions.append("update_retrieval_weights")
    return RetrievalDiagnosis(
        recall=recall,
        missed_ids=missed,
        actions=actions,
        available_ids=avail_ids,
    )


def boost_retrieval(skill: Skill, amount: float | None = None) -> float:
    """Increase metadata retrieval_boost; returns new value."""
    meta = dict(skill.metadata or {})
    delta = float(amount) if amount is not None else 0.2
    current = float(meta.get("retrieval_boost", 0.0) or 0.0)
    new_val = current + delta
    meta["retrieval_boost"] = new_val
    skill.metadata = meta
    return new_val
