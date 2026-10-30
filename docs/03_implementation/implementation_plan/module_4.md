Phase 10D: Skill Library Design

This is where ASFT finally becomes a capability accumulation system.

Up to now we have:

Trace Logger
↓
Invariant Detector
↓
Skill Creation Trigger


But a critical question remains:

What happens after a skill is created?

If the answer is:

Store it somewhere


then we have just built memory.

If the answer is:

Store it, retrieve it, compose it, reuse it, and measure its impact on future reasoning


then we have built the foundation for capability growth.

Phase 10D Goal

Answer:

How does a skill created from Task A become useful for Task B and Task C?

This is the entire ARC philosophy in engineering form.

Core Design Principle

The library is NOT:

Skill Storage


The library is:

Capability Infrastructure


Meaning:

Store
↓
Retrieve
↓
Compose
↓
Transfer
↓
Measure Growth

High-Level Architecture
                 Skill Creation
                        ↓

               ┌─────────────────┐
               │  Skill Library  │
               └────────┬────────┘
                        │

      ┌─────────────────┼─────────────────┐
      │                 │                 │

      ▼                 ▼                 ▼

 Retrieval Engine   Composition Engine   Analytics Engine

      │                 │                 │

      ▼                 ▼                 ▼

 Future Tasks      New Skills        Growth Metrics

First Design Decision
What Is Stored?

Not traces.

Not raw tasks.

Not outputs.

Store:

Skills


and

their history

Skill Object

Final MVP structure:

Skill
{
    skill_id,

    name,

    source_invariant,

    trigger_conditions,

    execution_policy,

    utility,

    transfer_score,

    reuse_count,

    creation_task,

    status
}

Example
{
    skill_id: "S001",

    name: "ReflectionSkill",

    source_invariant:
        "ReflectionInvariant",

    trigger_conditions:
        ["SymmetryDetected"],

    execution_policy:
        "ApplyReflection",

    utility: 0.81,

    transfer_score: 0.63,

    reuse_count: 19,

    status: "Active"
}

Skill Library Structure

I strongly recommend a hierarchical structure.

Not flat.

Bad Design
Skill1
Skill2
Skill3
Skill4
Skill5


Impossible to scale.

Better Design
Geometry

 ├─ ReflectionSkill

 ├─ RotationSkill

 └─ TranslationSkill

Counting

 ├─ CountObjects

 └─ CompareCounts

Grouping

 ├─ GroupObjects

 └─ ClusterObjects

Why Hierarchical?

Later:

Reflection
+
Rotation
+
Translation


may form:

Transformation


This gives a path toward future concept formation.

Component 1
Retrieval Engine

Most important library function.

Question

Given a new task:

Which skills should be used?

MVP Retrieval

Rule-based retrieval.

Example:

Task contains:

Symmetry


Retrieve:

ReflectionSkill

Retrieval Object
RetrievalResult
{
    skill_id,

    confidence,

    applicability_score
}


Example

{
    skill_id:"ReflectionSkill",

    confidence:0.87,

    applicability_score:0.91
}

Retrieval Score

Simple MVP:

Applicability
×
Utility
×
Transfer Score


High score:

Use Skill

Component 2
Skill Composition Engine

This is where Task B and Task C become possible.

Example

Task:

Rotate
Then Reflect


Library contains:

RotationSkill

ReflectionSkill


Composition Engine creates:

RotationSkill
+
ReflectionSkill


New execution chain.

MVP Composition Rule

Simple sequential composition.

Example

Skill A

then

Skill B


No graph search.

No planning.

Keep simple.

Why Important?

Without composition:

Task A
helps
Task A-like tasks


With composition:

Task A
helps
Task B
helps
Task C


This is closer to ARC-style transfer.

Component 3
Skill Analytics Engine

Contribution 3 begins here.

Purpose:

Track:

Skill Use

Transfer

Growth

Analytics Object
SkillStatistics
{
    skill_id,

    reuse_count,

    transfer_score,

    utility,

    avg_cost_reduction
}


Example

{
    skill_id:"ReflectionSkill",

    reuse_count:25,

    transfer_score:0.71,

    utility:0.82,

    avg_cost_reduction:4.1
}

Why Needed?

Because:

Capability Growth


requires evidence.

Component 4
Skill Promotion

After SCT creates a skill:

Candidate
↓
Active


Promotion criteria:

SCV > Threshold


and

Invariant Strength > Minimum


This prevents noisy skills.

Component 5
Skill Retirement

A surprisingly important feature.

Question:

Should every skill live forever?


No.

Retirement Conditions
Reuse Count Low

Transfer Score Low

Utility Low


for long periods.

Then:

Active
↓
Dormant
↓
Retired

Why Retire?

Otherwise:

Library Size
→ Infinity


And retrieval becomes noisy.

Component 6
Skill Evolution

Not MVP.

But we should design for it.

Future:

ReflectionSkill

+

RotationSkill

↓

TransformationSkill


This is future work.

Not v0.1.

Transfer Mechanism

This is the most important section.

How Task A Helps Task B

Task A:

Reflect Shape


Creates:

ReflectionSkill


Task B:

Reflect Object Group


System retrieves:

ReflectionSkill


Reasoning cost decreases.

Task C:

Reflect
+
Count


System retrieves:

ReflectionSkill

CountSkill


Transfer occurs.

Capability State

The library should maintain:

CapabilityState
{
    skill_count,

    active_skills,

    avg_transfer,

    avg_utility,

    capability_score
}


This directly feeds:

CGR

IG

MVP Interfaces
Skill Creation Trigger

Output:

SkillCandidate

Skill Library

Input:

SkillCandidate


Output:

Skill

Retrieval Engine

Input:

Task Context


Output:

Relevant Skills

MVP Scope

Included:

✅ Skill storage

✅ Retrieval

✅ Composition

✅ Analytics

✅ Promotion

✅ Retirement

Excluded:

❌ Concept graphs

❌ Neural retrieval

❌ Meta-reasoning

❌ Dynamic ontology growth

❌ Self-modifying skills

Deliverables of Phase 10D

✅ Skill object

✅ Library architecture

✅ Retrieval engine

✅ Composition engine

✅ Analytics engine

✅ Promotion policy

✅ Retirement policy

✅ Capability state

✅ Transfer mechanism

✅ MVP interfaces

Most Important Outcome

The critical engineering decision is:

The Skill Library is not a memory system. It is the mechanism by which experience becomes future capability.

That distinction is what allows ASFT to claim:

Task A
↓
Creates Skill
↓
Task B Easier
↓
Task C Easier


instead of simply:

Task A
↓
Stored

Next Phase

Phase 10E: Evaluation Engine Design

This will implement the actual measurement layer for:

Invariant Strength (IS)
Abstraction Gain (AG)
Skill Utility (SU)
Transfer Score (TS)
Capability Growth Rate (CGR)
Intelligence Growth (IG)

This phase is critical because it determines whether ASFT can scientifically validate its three contributions.