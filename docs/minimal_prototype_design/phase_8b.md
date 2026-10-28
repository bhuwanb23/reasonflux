Phase 8B: Data & Task Design

This is actually one of the most critical phases.

A lot of research projects fail because they pick the wrong evaluation environment.

If we choose the wrong tasks:

Good Theory
+
Bad Tasks
=
Unconvincing Results


If we choose the right tasks:

Simple Prototype
+
Good Tasks
=
Strong Paper

Phase 8B Objective

We are NOT trying to prove:

ASFT solves ARC


We are trying to prove:

ASFT creates reusable skills


Those are very different goals.

The Biggest Design Decision

We have three options.

Option A

Directly use ARC-AGI tasks.

Pros
Most realistic
Direct relevance
Cons
Extremely noisy
Hard to isolate skill formation
Difficult to debug
Option B

Synthetic Toy Environment

Pros
Easy to control
Easy to measure
Cons
Reviewers may say:
Nice toy
but not ARC

Option C (Recommended)

Two-layer evaluation.

Layer 1

Synthetic Skill Formation Environment

Layer 2

ARC Validation Environment

This gives us:

Controlled Science
+
ARC Relevance

Design Principle

The prototype should answer:

Does solving Task A create something that helps solve Task B?

Not:

Can we solve ARC?

Layer 1: Synthetic Skill Formation Benchmark

This is our scientific benchmark.

Task Family 1
Reflection Tasks

Task A1

Reflect Red Shape


Task A2

Reflect Blue Shape


Task A3

Reflect Multi-Object Shape


Expected Invariant

Reflection


Expected Skill

ApplyReflection()

Task Family 2
Rotation Tasks

Task B1

Rotate Triangle


Task B2

Rotate Square


Task B3

Rotate Object Group


Expected Invariant

Rotation


Expected Skill

ApplyRotation()

Task Family 3
Counting Tasks

Task C1

Count Red Objects


Task C2

Count Blue Objects


Task C3

Count Object Clusters


Expected Invariant

Numerosity


Expected Skill

CountObjects()

Why These Three Families?

They exist repeatedly throughout ARC-like reasoning.

More importantly:

Reflection
Rotation
Counting


are understandable abstractions.

We can verify whether ASFT discovers them.

Layer 2: Transfer Tasks

This is where ASFT either succeeds or fails.

Transfer Family 1
Reflection + Counting

Task D1

Reflect Shape
Then Count Reflected Objects


Required Skills

Reflection
+
Counting

Transfer Family 2
Rotation + Reflection

Task D2

Rotate
Then Reflect


Required Skills

Rotation
+
Reflection

Transfer Family 3
Counting + Grouping

Task D3

Count Groups


Requires composition.

Why Transfer Tasks Matter

The whole ASFT hypothesis depends on:

Task A
↓
Creates Skill
↓
Task B Easier


Transfer tasks directly test that.

Reasoning Trace Design

This is extremely important.

Without reasoning traces:

No Invariants

Trace Structure

Every solution generates:

[
 DetectObjects,
 FindSymmetry,
 ApplyReflection,
 VerifyResult
]


or

[
 DetectObjects,
 ComputeRotation,
 ApplyRotation,
 VerifyResult
]


ASFT operates on traces.

Not outputs.

Skill Discovery Dataset

The actual learning dataset should be:

Task
+
Reasoning Trace
+
Outcome


Example:

{
  "task":"ReflectionTask",
  "trace":[
    "DetectObject",
    "FindSymmetry",
    "ApplyReflection",
    "Verify"
  ],
  "success":true
}

Skill Emergence Scenario

This is the heart of the experiment.

Task 1

Reflection


No skill.

Task 2

Reflection


Still no skill.

Task 3

Reflection


Repeated reasoning appears.

SCT calculates:

SCV > threshold


System creates:

ReflectionSkill


Task 4

Uses:

ReflectionSkill


instead of:

Full Search


Measure:

Reasoning Cost Reduction

ARC Mapping Dataset

Now we connect to ARC.

We should not start with:

All ARC Tasks


Instead:

Select approximately:

20-30 ARC tasks


containing:

reflection
rotation
counting
grouping

families

Reason:

We need interpretable skill emergence.

Not benchmark chasing.

Dataset Structure

I recommend:

Synthetic Training Layer

Reflection Tasks
Rotation Tasks
Counting Tasks

↓

Transfer Layer

Mixed Tasks

↓

ARC Validation Layer

20-30 ARC Tasks

Experimental Groups

We need three systems.

Group A

Baseline

No Skill Creation

Group B

DreamCoder-like

Program Compression

Group C

ASFT

Invariant Discovery
+
Skill Creation Trigger


This comparison is crucial.

Phase 8B Deliverables
Dataset Design

✅ Reflection family

✅ Rotation family

✅ Counting family

✅ Transfer tasks

✅ ARC validation tasks

Trace Design

✅ Reasoning traces

✅ Skill emergence traces

Experimental Structure

✅ Baseline

✅ DreamCoder-style comparison

✅ ASFT

Most Important Outcome of Phase 8B

We discovered that the first prototype should not be evaluated on raw ARC accuracy.

The first prototype should be evaluated on:

Can it discover a reusable invariant?

Can it create a reusable skill?

Does that skill reduce future reasoning cost?

Does it improve transfer?


Only after proving those should we care about leaderboard performance.

Recommended Next Step

Proceed to Phase 8C: Minimal System Architecture & Internal Data Structures, where we formally define:

What exactly is a reasoning trace?
How invariants are represented
How concepts are represented
How skills are stored
What data structures the prototype uses
The end-to-end execution pipeline for ASFT v0.1

This is the step that will convert the research thesis into something implementable.