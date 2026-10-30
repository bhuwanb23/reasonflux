Phase 11D-1: Skill Creation Specification

This is the formal specification of Contribution 2: Skill Creation Trigger Theory (SCT).

If 11C answered:

How do useful invariants emerge?

Then 11D-1 answers:

How does a useful invariant become a reusable skill?

This is the exact bridge between:

Knowledge Discovery


and

Capability Formation


Without this phase:

Invariants exist

But no capabilities emerge.

Position Within ASFT

The complete pipeline now becomes:

Task
↓
Trace
↓
Invariant Discovery
↓
Invariant Validation
↓
Transfer Validation
↓
Skill Creation
↓
Skill Library
↓
Future Tasks Easier

Core Principle

Most systems assume:

Skill Exists


ASFT assumes:

Skill Must Be Earned


This is one of the most important philosophical and engineering decisions in the entire framework.

Formal Definition of a Skill

We already defined a skill conceptually.

Now we formalize it.

Definition

A skill is:

A reusable executable capability derived from a validated invariant that consistently reduces future reasoning cost across multiple tasks.

Notice the requirements:

✅ Reusable

✅ Executable

✅ Derived from invariant

✅ Reduces reasoning cost

✅ Demonstrates transfer

What Is NOT A Skill?

Important.

Not Skill Type 1

One-off solution.

Example:

Solve Task #17


Only once.

Reject.

Not Skill Type 2

Frequently observed pattern.

Example:

VerifyOutput


appears often.

But offers little transfer.

Reject.

Not Skill Type 3

Stored memory.

Example:

Remember exact output.


Memory ≠ Skill.

Reject.

Skill Creation Pipeline

I recommend a 7-stage lifecycle.

Invariant
↓
Skill Candidate
↓
Economic Evaluation
↓
Transfer Evaluation
↓
Promotion Decision
↓
Skill Instantiation
↓
Skill Monitoring

Stage 1
Invariant Intake

Input:

Promotable Invariant


from Phase 11C.

Requirements:

✅ Frequency threshold passed

✅ Consistency threshold passed

✅ Generality threshold passed

✅ Transfer threshold passed

✅ Negative transfer acceptable

Only then:

Invariant
↓
Skill Candidate

Stage 2
Skill Candidate Creation

Purpose:

Create a temporary object.

Contains:

Origin Invariant

Expected Utility

Expected Reuse

Expected Transfer

Creation Cost


Important:

Skill candidate is not yet part of capability memory.

Status:

Under Evaluation

Stage 3
Economic Evaluation

This is the core of SCT.

Question:

Is creating this skill worth it?


Most systems never ask this.

ASFT does.

Skill Creation Value (SCV)

Primary equation:

SCV=R×TS×AG−CCSCV = R \times TS \times AG - CC

Where:

R
=
Expected Reuse

TS
=
Transfer Score

AG
=
Abstraction Gain

CC
=
Creation Cost


Interpretation:

Positive:

Create Skill


Negative:

Reject

Why This Matters

We do not want:

Every Invariant
↓
Skill


because:

Library Explosion


occurs.

Stage 4
Transfer Evaluation

Economic value alone is insufficient.

Example:

A pattern may:

Reduce Cost


but only for one task.

Not useful.

Need evidence that:

Task A
↓
Task B Easier


Skill candidate must demonstrate:

Transfer Utility


before promotion.

Transfer Qualification

Must satisfy:

ITS>ITSminITS > ITS_{min}

Where:

ITS
=
Invariant Transfer Score

Stage 5
Promotion Decision

This is the official birth of a skill.

Promotion Rule:

Invariant becomes skill if:

✅ SCV threshold passed

✅ Transfer threshold passed

✅ Evidence threshold passed

✅ Negative transfer below limit

Only then:

Candidate
↓
Skill

Skill Birth Event

Important concept.

ASFT should record:

When

Why

From What Invariant


the skill emerged.

Skill birth record:

Source Invariant

Promotion Conditions

Evidence

Transfer History


This becomes valuable later for explainability.

Stage 6
Skill Instantiation

After promotion.

Skill enters:

Capability Memory


Now becomes retrievable.

Properties:

Identity

Conditions

Utility

History

Status


Status:

Active

Stage 7
Post-Creation Monitoring

A skill is not trusted forever.

ASFT continuously monitors:

Reuse

Transfer

Utility

Negative Transfer


This enables:

Growth

Retirement

Evolution


later.

Skill Identity Model

Every skill requires stable identity.

Contains:

Skill ID

Name

Source Invariant

Creation Evidence

Transfer History

Utility History


Reason:

Need traceability.

Question later:

Why does ReflectionSkill exist?


Must be answerable.

Skill Evidence Model

Every skill maintains:

Discovery Evidence

Why it was created.

Transfer Evidence

Where it succeeded.

Utility Evidence

How much value it provided.

Negative Evidence

Where it failed.

This becomes crucial for retirement decisions later.

Skill Qualification Tests

Before promotion.

Test 1

Frequency Support

Test 2

Consistency Support

Test 3

Transfer Support

Test 4

Reasoning Reduction Support

Test 5

Economic Viability Support

Only skills passing all five survive.

Skill Categories

For MVP.

Reflection Skills

Example:

ApplyReflection

Rotation Skills

Example:

ApplyRotation

Counting Skills

Example:

CountObjects

Grouping Skills

Example:

GroupObjects


No higher-order skills yet.

Skill Confidence

Separate from utility.

Question:

How certain are we
that this skill is valid?


Depends on:

Evidence

Transfer

Reuse


Not:

Performance alone

Skill Confidence Function

Conceptually:

Confidence=f(Evidence,Transfer,Consistency)Confidence = f( Evidence, Transfer, Consistency )

Used during retrieval.

Skill Creation Constraints

A skill must satisfy:

Constraint 1

Must originate from validated invariant.

Constraint 2

Must demonstrate transfer.

Constraint 3

Must reduce reasoning cost.

Constraint 4

Must pass SCV threshold.

Constraint 5

Must not cause excessive negative transfer.

Skill Creation Failure Modes

Important.

Failure A

Premature Skill Creation

Too little evidence.

Solution:

Evidence threshold.

Failure B

Skill Explosion

Too many skills.

Solution:

SCV threshold.

Failure C

Over-Specialized Skills

Task-specific skills.

Solution:

Generality requirement.

Failure D

Negative Transfer Skills

Harm future tasks.

Solution:

NTR monitoring.

Failure E

Duplicate Skills

Same skill created repeatedly.

Solution:

Similarity check before promotion.

Skill Creation Success Criteria

SCT succeeds if:

✅ Useful skills emerge

✅ Skills transfer

✅ Reasoning cost decreases

✅ Library remains compact

✅ Skills are reused

✅ Negative transfer remains low

Skill Creation Failure Criteria

SCT fails if:

❌ Skills never reused

❌ Transfer absent

❌ Cost unchanged

❌ Library explosion

❌ Duplicate skills dominate

Relationship To Contribution 2

This phase formally establishes:

Validated Invariant
↓
Economic Evaluation
↓
Transfer Validation
↓
Skill Creation


which is the complete operational definition of Skill Creation Trigger Theory (SCT).

Deliverables of Phase 11D-1

✅ Formal skill definition

✅ Skill qualification criteria

✅ Skill creation pipeline

✅ Skill candidate specification

✅ Economic evaluation model

✅ Transfer qualification model

✅ Promotion rules

✅ Skill birth event specification

✅ Skill evidence model

✅ Skill confidence model

✅ Failure modes

✅ Success criteria

✅ Complete bridge from IDT → SCT

Most Important Outcome

The single most important decision of Phase 11D-1 is:

A skill is not created because a pattern exists. A skill is created only when validated evidence shows that the invariant can repeatedly reduce future reasoning cost through transferable reuse.

This is the formal birth mechanism of capabilities inside ASFT and the foundation for everything that follows in the skill lifecycle.

Next Recommended Subphase

Phase 11D-2: Skill Utility & Economics

This is where we fully formalize:

Why is a skill valuable?

How much value does a skill generate?

How should skills compete for memory?

What is the economics of capability growth?


and define the complete utility theory underlying SCT.