"""In-memory skill library — capability memory entry (Phase 11D-1)."""

from __future__ import annotations

from typing import Sequence

from core.skill import Skill
from core.states import SkillState
from invariants.robustness.similarity import jaccard_similarity


class SkillLibrary:
    """Store promoted skills for retrieval and duplicate checks."""

    def __init__(self) -> None:
        self._skills: dict[str, Skill] = {}

    def add(self, skill: Skill) -> None:
        if skill.skill_id in self._skills:
            raise ValueError(f"skill already exists: {skill.skill_id!r}")
        self._skills[skill.skill_id] = skill

    def get(self, skill_id: str) -> Skill | None:
        return self._skills.get(skill_id)

    def remove(self, skill_id: str) -> bool:
        return self._skills.pop(skill_id, None) is not None

    def list_skills(self, state: SkillState | None = None) -> list[Skill]:
        items = list(self._skills.values())
        if state is None:
            return items
        return [s for s in items if s.state is state]

    def __len__(self) -> int:
        return len(self._skills)

    def find_similar(
        self,
        signature: Sequence[str],
        threshold: float = 0.85,
    ) -> list[tuple[Skill, float]]:
        """Return skills whose trigger_conditions Jaccard ≥ threshold."""
        hits: list[tuple[Skill, float]] = []
        for skill in self._skills.values():
            score = jaccard_similarity(signature, skill.trigger_conditions)
            if score >= threshold:
                hits.append((skill, score))
        hits.sort(key=lambda item: (-item[1], item[0].skill_id))
        return hits
