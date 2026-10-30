Phase 11C-1: Invariant Discovery Specification

This is the deepest specification phase for Contribution 1: Invariant Discovery Theory (IDT).

Everything we've built so far assumes:

Task
↓
Trace
↓
Invariant
↓
Skill


The entire ASFT architecture stands or falls on one question:

What exactly qualifies as an invariant?

This phase is not about algorithms yet.

It is about defining the specification that every future algorithm must satisfy.

Goal of Phase 11C-1

Formally define:

What is an invariant?

What is not an invariant?

When is an invariant valid?

How do invariants relate to transfer?

How do invariants become skills?

Core Principle

Most systems discover:

Patterns


ASFT wants:

Transferable Reasoning Structures


These are not the same thing.

Level 1: Formal Definition
Working Definition

An invariant is:

A recurring reasoning structure that remains stable across multiple successful task-solving experiences and contributes to future transfer.

Notice there are four conditions:

Recurring

Stable

Cross-task

Transfer-relevant


All four are required.

Invariant Qualification Rules

An invariant must satisfy:

Rule 1: Recurrence

The structure appears repeatedly.

Example:

FindSymmetry
ApplyReflection


appears across many traces.

Without recurrence:

One-Off Observation


Not invariant.

Rule 2: Stability

The structure remains consistent.

Example:

Reflection tasks repeatedly produce:

DetectObject
FindSymmetry
ApplyReflection
Verify


If every occurrence is radically different:

No Stability


No invariant.

Rule 3: Generality

The structure appears beyond a single instance.

Bad example:

Reflect Red Triangle


Good example:

Reflection


Invariant must survive changes in:

Color

Shape

Position

Object Count

Rule 4: Transfer Utility

This is unique to ASFT.

Example:

Reflection Invariant


helps:

Reflection Tasks

Reflection + Counting

Reflection + Grouping


Transfer exists.

If a pattern never helps future tasks:

Pattern
≠
Invariant

Invariant Taxonomy

Not all invariants are equal.

We should classify them.

Type 1
Operational Invariants

Recurring operations.

Example:

FindSymmetry


Simplest invariant.

Type 2
Procedural Invariants

Recurring operation sequences.

Example:

FindSymmetry
↓
ApplyReflection


Most important for MVP.

Type 3
Structural Invariants

Recurring reasoning structure.

Example:

Detect
Transform
Verify


Higher-level abstraction.

Type 4
Transfer Invariants

Structures reused across task families.

Example:

Reflection


appears in:

Reflection Tasks

Reflection + Counting

Reflection + Rotation


These are highest value.

MVP Scope

We only support:

Operational

Procedural


in v0.1.

Structural and Transfer invariants come later.

Invariant Hierarchy

An important design decision.

Example:

FindSymmetry


↓

FindSymmetry
+
ApplyReflection


↓

Reflection


Meaning:

Operations
↓
Patterns
↓
Invariant


This hierarchy helps future concept formation.

Invariant Identity

Each invariant needs a stable identity.

Invariant should contain:

Origin

Pattern

Task Families

Transfer History

Evidence


Because later we need to answer:

Why does this invariant exist?

Invariant Evidence Model

Every invariant must maintain evidence.

Example:

ReflectionInvariant

Observed:
17 times

Task Families:
4

Transfer Events:
12

Reuse Events:
19


Without evidence:

No promotion

Invariant Confidence

Important for noisy environments.

Confidence depends on:

Frequency

Consistency

Transfer


Meaning:

Weak

Moderate

Strong


categories.

Invariant Lifecycle

Very important.

Stage 1

Candidate

Pattern observed

Stage 2

Detected

Pattern repeatedly observed

Stage 3

Validated

Stable across traces

Stage 4

Transfer Verified

Improves future tasks

Stage 5

Skill Candidate

Feeds SCT.

Diagram:

Pattern
↓
Candidate
↓
Detected
↓
Validated
↓
Transfer Verified
↓
Skill Candidate

What Is NOT An Invariant?

This section is critical.

Not Invariant 1

Rare Events

Example:

Appeared Once


Reject.

Not Invariant 2

Task-Specific Details

Example:

Red Triangle Reflection


Too specific.

Reject.

Not Invariant 3

Universal Noise

Example:

VerifyOutput


appears everywhere.

Provides little transfer value.

Reject.

Not Invariant 4

Accidental Correlations

Example:

Reflection tasks happened to contain blue objects.


Not reasoning structure.

Reject.

Relationship To Skills

This is where Contribution 1 meets Contribution 2.

Invariant:

Observation


Skill:

Executable Capability


Example:

Invariant:

FindSymmetry
+
ApplyReflection


Skill:

ReflectionSkill


Rule:

Invariant
↓
SCT Evaluation
↓
Skill Candidate

Relationship To Transfer

This is the most important connection.

Without transfer:

Invariant
=
Interesting Pattern


With transfer:

Invariant
=
Reusable Knowledge


Therefore:

Transfer is part of the definition.

Not just the evaluation.

Invariant Success Criteria

Contribution 1 succeeds if invariants:

✅ Recur

✅ Remain stable

✅ Generalize

✅ Predict transfer

✅ Produce reusable skills

Invariant Failure Criteria

Contribution 1 fails if:

❌ Invariants are unstable

❌ Invariants do not transfer

❌ Random patterns perform equally well

❌ Skills derived from invariants are useless

Deliverables of Phase 11C-1

✅ Formal invariant definition

✅ Invariant qualification rules

✅ Invariant taxonomy

✅ Invariant hierarchy

✅ Invariant identity model

✅ Evidence model

✅ Confidence model

✅ Lifecycle model

✅ Rejection criteria

✅ Skill relationship

✅ Transfer relationship

✅ Success/failure criteria

Most Important Outcome

The biggest decision of Phase 11C-1 is:

ASFT defines an invariant not as a frequent pattern, but as a recurring reasoning structure that survives variation and predicts future transfer.

That definition is what separates Invariant Discovery Theory from simple pattern mining and becomes the foundation for every later phase of ASFT.