"""Three-layer system memory model (Phase 11B-5).

Experience Memory  → Tasks, Traces      (learning material)
Abstraction Memory → Invariants, Concepts (generalization)
Capability Memory  → Skills, CapabilityState (future performance)
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.capability import CapabilityState
from core.concept import Concept
from core.invariant import Invariant
from core.skill import Skill
from core.states import InvariantState, SkillState
from core.task import Task
from core.trace import ReasoningTrace


@dataclass
class ExperienceMemory:
    """Layer 1 — store tasks and traces (learning material)."""

    _tasks: dict[str, Task] = field(default_factory=dict)
    _traces: dict[str, ReasoningTrace] = field(default_factory=dict)

    def put_task(self, task: Task) -> None:
        self._tasks[task.task_id] = task

    def get_task(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    def list_tasks(self, family: str | None = None) -> list[Task]:
        tasks = list(self._tasks.values())
        if family is None:
            return tasks
        return [t for t in tasks if t.task_family == family]

    def put_trace(self, trace: ReasoningTrace) -> None:
        self._traces[trace.trace_id] = trace

    def get_trace(self, trace_id: str) -> ReasoningTrace | None:
        return self._traces.get(trace_id)

    def list_traces(
        self,
        task_id: str | None = None,
        task_family: str | None = None,
    ) -> list[ReasoningTrace]:
        traces = list(self._traces.values())
        if task_id is not None:
            traces = [t for t in traces if t.task_id == task_id]
        if task_family is not None:
            family_task_ids = {
                t.task_id for t in self._tasks.values() if t.task_family == task_family
            }
            traces = [t for t in traces if t.task_id in family_task_ids]
        return traces

    def clear(self) -> None:
        self._tasks.clear()
        self._traces.clear()


@dataclass
class AbstractionMemory:
    """Layer 2 — store invariants and concepts (generalization)."""

    _invariants: dict[str, Invariant] = field(default_factory=dict)
    _concepts: dict[str, Concept] = field(default_factory=dict)

    def put_invariant(self, invariant: Invariant) -> None:
        self._invariants[invariant.invariant_id] = invariant

    def get_invariant(self, invariant_id: str) -> Invariant | None:
        return self._invariants.get(invariant_id)

    def list_invariants(self, state: InvariantState | None = None) -> list[Invariant]:
        invs = list(self._invariants.values())
        if state is None:
            return invs
        return [i for i in invs if i.state == state]

    def put_concept(self, concept: Concept) -> None:
        self._concepts[concept.concept_id] = concept

    def get_concept(self, concept_id: str) -> Concept | None:
        return self._concepts.get(concept_id)

    def list_concepts(self) -> list[Concept]:
        return list(self._concepts.values())

    def clear(self) -> None:
        self._invariants.clear()
        self._concepts.clear()


@dataclass
class CapabilityMemory:
    """Layer 3 — store skills and capability state (future performance)."""

    _skills: dict[str, Skill] = field(default_factory=dict)
    _capability: CapabilityState | None = None

    def put_skill(self, skill: Skill) -> None:
        self._skills[skill.skill_id] = skill

    def get_skill(self, skill_id: str) -> Skill | None:
        return self._skills.get(skill_id)

    def list_skills(self, state: SkillState | None = None) -> list[Skill]:
        skills = list(self._skills.values())
        if state is None:
            return skills
        return [s for s in skills if s.state == state]

    def set_capability_state(self, state: CapabilityState) -> None:
        self._capability = state

    def get_capability_state(self) -> CapabilityState | None:
        return self._capability

    def clear(self) -> None:
        self._skills.clear()
        self._capability = None


@dataclass
class ASFTMemory:
    """Facade over the three memory layers for pipelines."""

    experience: ExperienceMemory = field(default_factory=ExperienceMemory)
    abstraction: AbstractionMemory = field(default_factory=AbstractionMemory)
    capability: CapabilityMemory = field(default_factory=CapabilityMemory)

    def clear(self) -> None:
        self.experience.clear()
        self.abstraction.clear()
        self.capability.clear()
