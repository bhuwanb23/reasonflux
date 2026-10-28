Phase 11D-4: Skill Composition

This is where ASFT begins to move from:

Skill Formation


to

Capability Formation


Honestly, this may be one of the most important phases after SCT.

Why?

Because creating isolated skills is not enough.

A system with:

ReflectionSkill

RotationSkill

CountSkill


is not necessarily intelligent.

The real question is:

Can the system combine skills to solve problems it has never seen before?

That is much closer to ARC's underlying philosophy.

Position Within ASFT

Before Skill Composition:

Task
↓
Invariant
↓
Skill


After Skill Composition:

Task
↓
Skill A

Skill B

Skill C
↓
Composed Capability
↓
Novel Problem Solving

Core Principle

A skill is useful.

A composition of skills is powerful.

Example:

System knows:

ReflectionSkill


and

CountSkill


New task:

Reflect objects
then count them


Without composition:

Failure


With composition:

ReflectionSkill
+
CountSkill
=
Success

Formal Definition
Skill Composition

A skill composition is:

A structured combination of two or more skills that together solve a task that no individual skill can solve alone.

Important Distinction

Not:

Many Skills Exist


But:

Many Skills Cooperate

Why Composition Matters

Without composition:

Skill Count ↑

Capability ↑ very slowly


With composition:

Skill Count ↑

Capability ↑ exponentially


Example:

3 skills:

Reflection

Rotation

Counting


Possible compositions:

Reflection + Rotation

Reflection + Counting

Rotation + Counting

Reflection + Rotation + Counting


Notice:

3 Skills
↓
7 Possible Capabilities


This is extremely important.

Composition Hierarchy

We need levels.

Level 0
Atomic Skill

Single skill.

Example:

ReflectionSkill

Level 1
Pair Composition

Two skills.

Example:

ReflectionSkill
+
CountSkill

Level 2
Multi-Skill Composition

Three or more skills.

Example:

Reflection
+
Rotation
+
Counting

Level 3
Capability Composition

Repeatedly successful compositions.

Example:

Reflection
+
Grouping
+
Counting


becomes:

ObjectAnalysisCapability


Future work, not MVP.

Composition Trigger

Critical question.

When should skills be composed?

Not:

Always


That creates combinatorial explosion.

ASFT principle:

Compose only when:

No Individual Skill
Can Solve Task


Formula:

Let:

Task Requirement = TR

Skill Coverage = SC


If:

SC<TRSC < TR

for all individual skills

then:

Try Composition

Composition Candidate

Before composition:

Create temporary object.

Contains:

Skill Set

Expected Utility

Expected Transfer

Composition Cost


Example:

ReflectionSkill

CountSkill


↓

ReflectionCountCandidate


Not permanent yet.

Composition Evaluation

Every composition must be evaluated.

Questions:

Does it solve the task?
Does it reduce reasoning cost?
Does it transfer?
Is it reusable?

Only then should it be remembered.

Composition Utility

Similar to skill utility.

Define:

CU=TransferGain+ReasoningReduction+ReusePotential−CompositionCostCU = TransferGain + ReasoningReduction + ReusePotential - CompositionCost

Where:

CU
=
Composition Utility


High CU:

Keep Composition


Low CU:

Discard Composition

Composition Types

This is important.

Type 1
Sequential Composition

Most important for MVP.

Example:

Reflection
↓
Counting


Execution order matters.

Type 2
Parallel Composition

Future version.

Example:

Count Objects

Detect Groups


simultaneously.

Not MVP.

Type 3
Conditional Composition

Future version.

Example:

If Symmetry
Use Reflection

Else
Use Rotation


Not MVP.

Type 4
Recursive Composition

Future AGI work.

Skill creates composition of compositions.

Not MVP.

MVP Scope

Only:

Sequential Composition


Everything else later.

Composition Memory

Should compositions be stored?

Answer:

Not immediately.

Example:

Reflection + Count


works once.

Do NOT store.

Need repeated evidence.

Composition Lifecycle
Composition Candidate
↓
Validated Composition
↓
Reusable Composition
↓
Capability Candidate


Similar to skills.

Composition Evidence

Every composition tracks:

Uses

Successes

Failures

Transfer Events

Cost Reduction


Without evidence:

No Promotion

Composition Confidence

Question:

How confident are we
that this composition works?


Depends on:

Successful Executions

Transfer Events

Task Diversity

Composition Graph

Very important future structure.

Represent:

Skill


as node.

Example:

Reflection
     │
     ├──── Count
     │
     ├──── Group
     │
     └──── Rotate


Edges represent:

Successful Composition


This graph becomes:

Capability Graph


later.

Composition Reuse

A key metric.

Example:

Reflection + Count


used:

25 times


High value.

Used:

1 time


Low value.

Composition Promotion

A repeated composition may eventually become:

Higher-Level Skill


Example:

Reflection
+
Counting


↓

ReflectionCountSkill


This is extremely important.

This is how capability hierarchies emerge.

Capability Emergence

One of the strongest ideas in ASFT.

Example:

Atomic skills:

Reflection

Rotation

Grouping

Counting


Repeated compositions:

Reflection+Grouping

Grouping+Counting

Reflection+Counting


Eventually:

ObjectStructureAnalysis


capability emerges.

Not manually programmed.

Discovered.

Composition Failure Modes

We must define them.

Failure 1

Composition Explosion

Example:

10 skills.

Possible combinations:

Huge.

Solution:

Only compose when necessary.

Failure 2

Redundant Composition

Example:

Reflection + Reflection


Provides no value.

Reject.

Failure 3

Negative Composition

Example:

Reflection
+
Wrong Skill


↓

Performance drops.

Track:

Negative Composition Rate

Failure 4

Over-Specialization

Example:

ReflectionCountBlueTriangleSkill


Too specific.

Reject.

Composition Metrics

ASFT should track:

Composition Utility
CUCU
Composition Reuse
CRCR
Composition Transfer
CTCT
Composition Confidence
CCCC
Negative Composition Rate
NCRNCR
Success Criteria

Skill Composition succeeds if:

✅ Skills combine successfully

✅ Transfer increases

✅ New capabilities emerge

✅ Reuse increases

✅ Reasoning cost decreases

✅ Composition remains manageable

Failure Criteria

Skill Composition fails if:

❌ Combinatorial explosion

❌ Most compositions useless

❌ No transfer improvement

❌ No capability emergence

❌ Retrieval complexity explodes

Relationship To Capability Growth

This is the most important section.

Without composition:

Capability Growth
=
Linear


With composition:

Capability Growth
=
Combinatorial


because a small set of skills can generate a much larger set of capabilities.

Deliverables of Phase 11D-4

✅ Formal skill composition definition

✅ Composition hierarchy

✅ Composition trigger rules

✅ Composition candidate model

✅ Composition utility model

✅ Composition lifecycle

✅ Composition confidence model

✅ Composition graph model

✅ Capability emergence mechanism

✅ Composition failure modes

✅ Composition metrics

✅ Success/failure criteria

Most Important Outcome

The single most important decision of Phase 11D-4 is:

Skills are not the final unit of intelligence in ASFT. Skills become building blocks that can be composed into larger capabilities, allowing Task A knowledge to contribute to Task B, Task C, and entirely new task families.

This is the first place in ASFT where we get a plausible mechanism for moving from:

Skill Acquisition


to

Capability Growth


which is the central thesis of the entire framework.

Next Recommended Subphase

Phase 11D-5: Skill Failure Modes & Robustness

This should complete SCT by defining:

skill creation failures,
skill utility failures,
skill lifecycle failures,
composition failures,
catastrophic transfer,
capability collapse,
memory overload,
retrieval failures,
adversarial skill formation,
and all safeguards needed before implementation.