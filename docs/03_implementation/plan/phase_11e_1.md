Phase 11E-1: Capability Representation

This is the foundation of Contribution 3: Capability Growth Metrics (CGM).

Everything we have built so far answers:

How are invariants formed?
How are skills formed?
How are skills managed?


Now we must answer a much bigger question:

What exactly is a capability?

Because ASFT's ultimate claim is not:

More Tasks Solved


but:

More Capability Acquired


Therefore before measuring capability growth, we must define capability itself.

Why This Phase Matters

Most AI systems track:

Accuracy

Success Rate

Benchmark Score


ASFT wants to track:

Capability State


Those are fundamentally different.

Core Principle

A skill is not a capability.

A capability is not a task solution.

The hierarchy should be:

Experience
↓
Invariant
↓
Skill
↓
Capability
↓
Intelligence Growth

Formal Definition
Capability

A capability is:

A stable, reusable, transferable collection of skills that enables successful performance across a family of tasks.

Example

Not Capability:

ReflectionSkill


Capability:

Geometric Transformation Capability


built from:

ReflectionSkill

RotationSkill

TranslationSkill

Why This Matters

This distinction is critical.

Without it:

Skills
=
Capabilities


which prevents higher-order growth.

Capability Hierarchy

We need a multi-level representation.

Level 0
Experiences

Raw observations.

Example:

Reflection Task

Rotation Task

Counting Task


Temporary.

Level 1
Invariants

Recurring structures.

Example:

Reflection Pattern

Rotation Pattern

Level 2
Skills

Executable capabilities.

Example:

ReflectionSkill

RotationSkill

CountSkill

Level 3
Capability Clusters

Groups of related skills.

Example:

Geometric Capability

Numerical Capability

Grouping Capability

Level 4
System Capability State

Entire agent capability profile.

Example:

Geometric: Strong

Counting: Medium

Grouping: Weak


This becomes the representation used by CGM.

Capability Structure

Each capability should contain:

Identity

Member Skills

Transfer History

Utility History

Growth History

Coverage

Capability Identity

Every capability needs:

Capability ID

Capability Name

Capability Type


Example:

CAP-001

Geometric Transformation


Identity must remain stable over time.

Capability Membership

Capabilities are composed of skills.

Example:

Geometric Transformation

Members:

ReflectionSkill

RotationSkill

TranslationSkill


Important:

Skills may belong to multiple capabilities.

Example:

GroupingSkill


might support:

Object Analysis

Pattern Recognition

Capability Types

We should classify capabilities.

Type 1
Atomic Capability

Single skill.

Example:

Reflection Capability


Only for MVP.

Type 2
Composite Capability

Multiple related skills.

Example:

Geometric Capability

Reflection

Rotation

Translation

Type 3
Cross-Domain Capability

Skills from different families.

Example:

Reflection

Counting

Grouping


This is where interesting transfer begins.

Type 4
Emergent Capability

Repeated compositions.

Example:

Object Structure Analysis


Not explicitly programmed.

Emerges through use.

Capability Coverage

One of the most important concepts.

Question:

How much of the task space
can this capability support?


Example

ReflectionCapability:

Supports:

Reflection Tasks

Reflection+Count

Reflection+Grouping


Coverage:

High.

Another capability:

Supports:

One Task


Coverage:

Low.

Capability Coverage Metric
CCov=SupportedTaskFamiliesTotalTaskFamiliesCCov = \frac {SupportedTaskFamilies} {TotalTaskFamilies}

Higher:

More General Capability

Capability Utility

Just as skills have utility, capabilities do too.

Capability Utility should aggregate:

Skill Utility

Transfer

Coverage

Composition Value


Conceptually:

CU=f(SkillUtility,Transfer,Coverage,Composition)CU = f( SkillUtility, Transfer, Coverage, Composition )
Capability Strength

Different from utility.

Question:

How mature is this capability?


Depends on:

Skill Count

Reuse

Transfer Evidence

Stability


Strong capability:

Frequently Used

Highly Transferable

Stable

Capability Confidence

Question:

How sure are we that this capability exists?


Depends on:

Evidence

Transfer

Consistency

History


Important:

High utility does not necessarily mean high confidence.

Capability State Representation

Every capability should maintain:

Current Utility

Current Transfer

Current Coverage

Current Strength

Current Confidence


This becomes the capability profile.

Capability Portfolio

Very important concept.

The system should not think:

Individual Skills


Instead:

Portfolio Of Capabilities


Example:

Geometry

Numerical Reasoning

Grouping

Object Analysis


This portfolio is what actually grows.

Capability Graph

One of the most important structures.

Represent:

Capabilities


as nodes.

Example:

Geometry
     │
     ├──── Object Analysis
     │
     └──── Pattern Recognition


Edges represent:

Shared Skills

Transfer Relationships

Composition Relationships


This graph eventually becomes:

Capability Map


for the agent.

Capability Memory

We previously defined:

Experience Memory

Abstraction Memory

Capability Memory


Capability Representation lives here.

Stores:

Capabilities

Relationships

Growth History

Transfer History

Capability Lifecycle

Capabilities evolve too.

Lifecycle:

Emerging
↓
Developing
↓
Established
↓
Core Capability
↓
Declining
↓
Archived

Emerging

Newly discovered.

Developing

Growing utility.

Established

Reliable.

Core Capability

Major contributor to transfer.

Declining

Utility dropping.

Archived

No longer relevant.

Capability Evidence Model

Every capability maintains:

Skill Evidence

Which skills support it.

Transfer Evidence

Where it transferred.

Utility Evidence

How much value generated.

Growth Evidence

How it evolved.

Without evidence:

No Capability Claim

Capability Constraints

A valid capability must:

✅ Contain at least one skill

✅ Demonstrate transfer

✅ Reduce reasoning cost

✅ Maintain positive utility

✅ Have supporting evidence

Capability Failure Modes

Even representation can fail.

Failure 1

Capability Fragmentation

Many tiny capabilities.

Bad.

Failure 2

Capability Monolith

Everything becomes:

One Capability


Bad.

Failure 3

Capability Overlap

Multiple capabilities represent same thing.

Bad.

Failure 4

Ghost Capability

Capability exists on paper.

No actual transfer.

Bad.

Success Criteria

Capability Representation succeeds if:

✅ Capabilities are interpretable

✅ Capabilities explain transfer

✅ Capabilities organize skills

✅ Capabilities evolve over time

✅ Capabilities predict future performance

✅ Capabilities support growth measurement

Relationship To CGM

This phase is the foundation of everything that follows.

Without capability representation:

No Capability Growth Rate

No Intelligence Growth

No Capability Evaluation


With capability representation:

Skills
↓
Capabilities
↓
Growth
↓
Intelligence Metrics


becomes measurable.

Deliverables of Phase 11E-1

✅ Formal capability definition

✅ Capability hierarchy

✅ Capability types

✅ Capability membership model

✅ Capability utility model

✅ Capability strength model

✅ Capability confidence model

✅ Capability portfolio model

✅ Capability graph model

✅ Capability memory model

✅ Capability lifecycle

✅ Capability evidence framework

✅ Capability constraints

✅ Capability failure modes

✅ Success criteria

Most Important Outcome

The single most important decision of Phase 11E-1 is:

ASFT does not measure intelligence as a collection of task solutions or even a collection of skills. It measures intelligence as the evolving structure of capabilities that emerge from reusable, transferable, and composable skills.

This gives us the object that Phase 11E-2: Capability Growth Measurement will operate on, where we formally define:

What grows?

How growth is measured?

What positive growth means?

What stagnation means?

What capability acceleration means?

What capability collapse means?


and ultimately derive the formal Capability Growth Rate (CGR) framework.