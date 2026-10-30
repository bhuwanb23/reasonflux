Phase 9D: Baseline & Ablation Strategy

This phase is much more important than most researchers realize.

Many papers fail not because their idea is bad, but because reviewers say:

"Your comparison is unfair."

or

"You removed the wrong thing in the ablation."

or

"Your gains come from extra memory, not your proposed method."

Phase 9D exists to prevent exactly that.

Goal of Phase 9D

We need to answer:

If ASFT works,
what exactly caused it to work?


and

What would happen if pieces of ASFT were removed?


This is how we isolate the value of each contribution.

First Principle

A baseline should answer:

"What is the strongest reasonable alternative explanation?"

An ablation should answer:

"Which component of ASFT actually matters?"

Experimental Groups Overview

We will have:

4 Baselines

1 ASFT System

5 Ablations

Baseline B1
No-Learning Baseline
Architecture
Task
↓
Solve
↓
Forget


No memory.

No skills.

No transfer.

No accumulation.

Why This Baseline Exists

This establishes:

Zero Capability Growth

Reviewer Question

Maybe capability growth happens naturally.

Answer:

No-Learning Baseline


tests that.

Expected Behavior
TS ≈ 0

CGR ≈ 0

Fairness

Very fair.

Represents traditional task-independent solving.

Baseline B2
Skill Storage Only
Architecture
Task
↓
Store Skill
↓
Reuse Skill


But:

No Invariant Discovery
No SCT

Purpose

Tests whether:

Skill Storage Alone


explains gains.

Reviewer Question

Maybe all you need is memory.

This baseline directly addresses that.

Expected Result

Should perform better than B1.

But worse than ASFT.

Why?

Because ASFT decides:

What to store


rather than storing everything.

Baseline B3
DreamCoder-like Baseline

This is the most important comparison.

Architecture
Task
↓
Program
↓
Compression
↓
Primitive
↓
Library

Why This Baseline Matters

DreamCoder is the closest known prior art to our thesis.

Throughout our novelty validation:

Biggest Threat
=
DreamCoder

What It Tests

Whether:

Program Compression


is sufficient.

versus

Invariant Discovery
+
Skill Formation

Reviewer Question

Isn't ASFT just DreamCoder?

This baseline exists specifically to answer that.

Expected Result

DreamCoder-like system:

Creates Primitives


ASFT:

Creates Skills
via
Invariant Discovery

Baseline B4
Random Skill Creation

This baseline is extremely important.

Architecture
Task
↓
Randomly Create Skills
↓
Store Skills

Purpose

Test:

Does SCT actually matter?

Reviewer Question

Maybe creating any skill helps.

This baseline directly challenges SCT.

Expected Result

ASFT should dramatically outperform random skill creation.

Experimental System
ASFT

Architecture:

Reasoning Trace
↓
Invariant Discovery
↓
SCT
↓
Skill Creation
↓
Transfer
↓
Capability Growth


This is our full system.

Ablation A1
Remove Invariant Detector
Architecture
Trace
↓
No Invariants
↓
SCT
↓
Skill Library

Question

Do invariants matter?

Expected Result

Transfer decreases.

Skill quality decreases.

What It Proves

Contribution 1:

IDT


is important.

Ablation A2
Remove SCT
Architecture
Invariant
↓
Always Create Skill

Question

Does the trigger matter?

Expected Result

Too many skills.

Low utility.

Poor efficiency.

What It Proves

Contribution 2:

SCT


is important.

Ablation A3
Remove Skill Library
Architecture
Invariant
↓
Skill
↓
Forget

Question

Does memory matter?

Expected Result

Transfer collapses.

Capability growth collapses.

What It Proves

Skills must persist.

Ablation A4
Remove Transfer Mechanism
Architecture
Skills Exist
↓
Cannot Reuse

Question

Does transfer matter?

Expected Result

Capability growth becomes minimal.

What It Proves

Transfer is the bridge between:

Skill
↓
Growth

Ablation A5
Remove Capability Metrics
Architecture

Everything works.

But:

No CGR
No IG

Question

Do we actually need Contribution 3?

Expected Result

System still functions.

But growth becomes unmeasurable.

What It Proves

Contribution 3 is an evaluation innovation.

Master Comparison Matrix
System	Invariants	SCT	Skill Library	Transfer	Growth MetricsB1 No Learning	❌	❌	❌	❌	❌
B2 Skill Storage	❌	❌	✅	Partial	❌
B3 DreamCoder-like	Partial	❌	✅	Partial	❌
B4 Random Skills	❌	Random	✅	Partial	❌
ASFT	✅	✅	✅	✅	✅
A1	❌	✅	✅	✅	✅
A2	✅	❌	✅	✅	✅
A3	✅	✅	❌	❌	✅
A4	✅	✅	✅	❌	✅
A5	✅	✅	✅	✅	❌
Reviewer Defense Mapping
Reviewer Attack 1

Maybe memory alone explains everything.

Answer:

Compare ASFT
vs
Skill Storage Baseline

Reviewer Attack 2

Maybe random skill creation works.

Answer:

Random Skill Baseline

Reviewer Attack 3

This is DreamCoder.

Answer:

DreamCoder Baseline

Reviewer Attack 4

Invariants don't matter.

Answer:

Ablation A1

Reviewer Attack 5

SCT doesn't matter.

Answer:

Ablation A2

Most Important Expected Result

The single strongest result we want is:

ASFT
>
DreamCoder-like
>
Skill Storage
>
No Learning


for:

Transfer Score

Reasoning Cost Reduction

Capability Growth


If that ordering appears consistently, it becomes very strong evidence that:

Invariant Discovery
+
Skill Creation Trigger


are contributing something meaningful beyond simple memory or compression.

Phase 9D Deliverables

✅ Fair baseline strategy

✅ DreamCoder comparison strategy

✅ Reviewer defense strategy

✅ Ablation framework

✅ Component-isolation plan

✅ Expected ranking of systems

✅ Evidence for all three contributions

Status After Phase 9D

We now have:

Phase 9A
Claims & Hypotheses ✅

Phase 9B
Evidence Mapping ✅

Phase 9C
Experiment Matrix ✅

Phase 9D
Baselines & Ablations ✅


Next, we should move to Phase 9E: Paper Blueprint, where we design the actual paper structure, section-by-section, map each contribution to sections, figures, tables, and experiments, and effectively pre-write the paper before any implementation begins. This will make Phase 10 (engineering plan) much more focused.