"""Tests for three-layer ASFT memory model."""

from core import (
    ASFTMemory,
    CapabilityState,
    Concept,
    Invariant,
    InvariantState,
    ReasoningTrace,
    Skill,
    SkillState,
    Task,
)


def test_experience_memory_store_and_filter():
    mem = ASFTMemory()
    mem.experience.put_task(
        Task(task_id="t1", task_family="reflection", input_state=None)
    )
    mem.experience.put_task(
        Task(task_id="t2", task_family="rotation", input_state=None)
    )
    mem.experience.put_trace(
        ReasoningTrace(trace_id="tr1", task_id="t1", timestamp=1.0)
    )
    mem.experience.put_trace(
        ReasoningTrace(trace_id="tr2", task_id="t2", timestamp=2.0)
    )

    assert mem.experience.get_task("t1") is not None
    assert len(mem.experience.list_tasks(family="reflection")) == 1
    assert len(mem.experience.list_traces(task_id="t1")) == 1
    assert len(mem.experience.list_traces(task_family="rotation")) == 1


def test_abstraction_memory_filter_by_state():
    mem = ASFTMemory()
    inv = Invariant(
        invariant_id="INV-1",
        pattern_signature=["reflect"],
        state=InvariantState.DETECTED,
    )
    mem.abstraction.put_invariant(inv)
    inv.transition_to(InvariantState.VALIDATED)
    mem.abstraction.put_invariant(inv)
    mem.abstraction.put_concept(
        Concept(concept_id="C1", label="Reflection", invariant_ids=["INV-1"])
    )

    assert len(mem.abstraction.list_invariants(state=InvariantState.VALIDATED)) == 1
    assert mem.abstraction.get_concept("C1").label == "Reflection"


def test_capability_memory_and_facade_clear():
    mem = ASFTMemory()
    mem.capability.put_skill(Skill(skill_id="SK-1", state=SkillState.ACTIVE))
    mem.capability.set_capability_state(CapabilityState(state_id="cap-1"))
    assert mem.capability.get_skill("SK-1") is not None
    assert len(mem.capability.list_skills(state=SkillState.ACTIVE)) == 1
    assert mem.capability.get_capability_state().state_id == "cap-1"

    mem.clear()
    assert mem.experience.list_tasks() == []
    assert mem.abstraction.list_invariants() == []
    assert mem.capability.list_skills() == []
    assert mem.capability.get_capability_state() is None
