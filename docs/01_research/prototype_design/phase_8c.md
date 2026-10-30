Phase 8C: Minimal System Architecture & Internal Data Structures

This is where ASFT becomes implementable.

Up until now, we've had:

Theory
↓
Mathematics
↓
Architecture


Now we define:

Data Structures
State
Memory
Execution Flow
Interfaces


This is essentially the "system design document" for ASFT v0.1.

Design Principles

Before defining structures, let's establish constraints.

ASFT v0.1 must:

✅ Validate the 3 contributions

✅ Be implementable by a small team

✅ Work on synthetic tasks first

✅ Be extendable to ARC

✅ Not require AGI

ASFT v0.1 Architecture
Task
 ↓

Reasoning Engine

 ↓

Reasoning Trace Logger

 ↓

Invariant Detector

 ↓

Concept Builder

 ↓

Skill Creation Trigger

 ↓

Skill Library

 ↓

Future Tasks

Component 1
Reasoning Trace

This is the most important object in the system.

Without traces:

No invariants
No concepts
No skills

Definition

A reasoning trace is:

A structured sequence of cognitive operations used to solve a task.

Trace Object
ReasoningTrace
{
    task_id

    steps[]

    outcome

    cost

    timestamp
}

Example
{
    task_id: "reflection_001",

    steps: [
        DetectObjects,
        FindSymmetry,
        ApplyReflection,
        VerifyOutput
    ],

    outcome: Success,

    cost: 12
}

Why Not Store Outputs?

Because:

Output = solution

Trace = reasoning


ASFT learns from reasoning.

Not answers.

Component 2
Reasoning Step

The atomic unit.

Definition

A reasoning step is the smallest explainable operation.

Structure
ReasoningStep
{
    operation

    inputs

    outputs

    cost
}

Example
{
    operation: "FindSymmetry",

    inputs:
        ObjectSet,

    outputs:
        SymmetryAxis,

    cost: 3
}

Component 3
Invariant Representation

Contribution #1 begins here.

Definition

Invariant:

Stable structure recurring across traces.

Data Structure
Invariant
{
    invariant_id

    pattern

    frequency

    consistency

    generality

    strength
}

Example
{
    invariant_id: INV_01,

    pattern:
        [FindSymmetry, ApplyReflection],

    frequency: 15,

    consistency: 0.92,

    generality: 0.78,

    strength: 10.8
}

Why Store Frequency?

Because repeated patterns matter.

Why Store Generality?

Because:

Useful across many tasks


is more valuable than:

Useful once

Component 4
Concept Representation

This is the most important distinction from DreamCoder.

Definition

A concept is a compressed explanation of one or more invariants.

Structure
Concept
{
    concept_id

    name

    source_invariants[]

    confidence

    abstraction_gain

    transfer_score
}

Example
{
    concept_id: C_01,

    name: Reflection,

    source_invariants:
    [
        INV_01,
        INV_03
    ],

    confidence: 0.91,

    abstraction_gain: 0.72,

    transfer_score: 0.63
}

Important

Concepts are:

Semantic Objects


not programs.

Component 5
Skill Representation

Contribution #2 begins here.

Definition

A skill is an executable concept.

Structure
Skill
{
    skill_id

    concept_id

    trigger_conditions

    execution_policy

    utility

    reuse_count
}

Example
{
    skill_id: S_01,

    concept_id: Reflection,

    trigger_conditions:
        SymmetryDetected,

    execution_policy:
        ApplyReflection,

    utility: 0.81,

    reuse_count: 19
}

Important Distinction

Concept:

Knows


Skill:

Acts

Component 6
Skill Library

Long-term memory.

Structure
SkillLibrary
{
    concepts[]

    skills[]

    relationships[]

    statistics
}


Example:

Reflection
    ↳ ReflectionSkill

Rotation
    ↳ RotationSkill

Counting
    ↳ CountingSkill

Why Relationships Matter?

Eventually:

Reflection
+
Rotation


may form:

Transformation


This enables future growth.

Component 7
Skill Creation Trigger

Contribution #2.

Structure
SkillCandidate
{
    concept_id

    reuse

    abstraction_gain

    transfer_score

    creation_cost

    scv
}

Example
{
    concept_id: Reflection,

    reuse: 15,

    abstraction_gain: 0.72,

    transfer_score: 0.63,

    creation_cost: 5,

    scv: 7.4
}

Decision Rule
If SCV > Threshold

Create Skill


Otherwise:

Keep Observing

Component 8
Capability State

Contribution #3.

Tracks agent growth.

Structure
CapabilityState
{
    num_concepts

    num_skills

    avg_transfer

    avg_reasoning_cost

    capability_score
}

Example
{
    num_concepts: 8,

    num_skills: 5,

    avg_transfer: 0.44,

    avg_reasoning_cost: 7.3,

    capability_score: 12.9
}

Why This Exists

Because we need to measure:

Agent Improvement


not just:

Task Success

Complete Execution Pipeline

Now let's put everything together.

Stage 1

Solve Task

Reflection Task

Stage 2

Generate Trace

DetectObject
FindSymmetry
ApplyReflection
Verify

Stage 3

Store Trace

Trace Database

Stage 4

Run Invariant Detector

Find recurring structures.

Stage 5

Create Concept Candidates

Example:

Reflection

Stage 6

Evaluate SCT

Compute:

SCV

Stage 7

Create Skill

ReflectionSkill

Stage 8

Store Skill

Skill Library

Stage 9

Future Task

Use:

ReflectionSkill


instead of:

Full Search

Stage 10

Measure Improvement

Transfer Score

Reasoning Cost

Capability Growth

ASFT v0.1 MVP Scope

To prevent scope creep:

Included

✅ Trace Logger

✅ Invariant Detector

✅ Concept Builder

✅ Skill Trigger

✅ Skill Library

✅ Metrics

Excluded

❌ Full Meta-Reasoner

❌ Autonomous Goal Creation

❌ LLM-based Planning

❌ ARC-3 Agent Framework

❌ Self-modifying Architecture

❌ Recursive Skill Evolution

Deliverables Completed for Phase 8C

✅ Formal reasoning trace definition

✅ Reasoning step structure

✅ Invariant representation

✅ Concept representation

✅ Skill representation

✅ Skill library design

✅ Skill creation trigger structure

✅ Capability state model

✅ End-to-end execution pipeline

✅ ASFT v0.1 MVP architecture

At this point, Phase 8 is roughly 70% complete. The next logical step is Phase 8D: Experimental Design, where we define the exact experiments, baselines, ablations, datasets, hypotheses, expected outcomes, and failure conditions needed to validate the three research contributions.