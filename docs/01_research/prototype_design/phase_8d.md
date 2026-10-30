Phase 8D: Experimental Design

This is where ASFT becomes a real research project.

Up to now we have:

Theory ✅
Architecture ✅
Mathematics ✅
Novelty ✅
Prototype Design ✅


But none of that matters unless we can answer:

How do we prove ASFT is correct?

A strong ARC paper is ultimately judged by evidence.

Phase 8D Goal

We are not trying to prove:

ASFT solves ARC.


We are trying to prove:

ASFT's hypotheses are true.


Specifically:

H1

Invariant Discovery Theory is useful.

H2

Skill Creation Trigger Theory creates beneficial skills.

H3

Capability Growth Metrics capture genuine capability growth.

Experimental Philosophy

Current ARC research usually evaluates:

Task Accuracy


ASFT evaluates:

Capability Growth


Therefore our experiments must measure:

Transfer
Reuse
Skill Emergence
Reasoning Cost Reduction


not only accuracy.

Experimental Roadmap

I recommend 4 core experiments and 3 ablation studies.

Experiment 1
Invariant Discovery

Experiment 2
Skill Formation

Experiment 3
Transfer Learning

Experiment 4
Capability Growth

Ablation A
No Invariants

Ablation B
No Skill Creation

Ablation C
No Skill Library

Experiment 1
Invariant Discovery Validation
Purpose

Validate:

Contribution 1
Invariant Discovery Theory

Research Question

Can the system identify reusable invariants across tasks?

Setup

Reflection Family:

Reflect Shape A

Reflect Shape B

Reflect Shape C


Rotation Family:

Rotate Shape A

Rotate Shape B

Rotate Shape C


Counting Family:

Count Objects A

Count Objects B

Count Objects C

Procedure

For every solved task:

Store reasoning trace.

Example:

DetectObjects
FindSymmetry
ApplyReflection
Verify


Run Invariant Detector.

Expected invariant:

Reflection

Metrics
Precision

How many discovered invariants are correct?

Recall

How many true invariants are found?

Invariant Strength
IS=Frequency×Consistency×GeneralityIS = Frequency \times Consistency \times Generality
Success Condition

Invariant detector consistently identifies:

Reflection
Rotation
Counting


without being manually labeled.

Experiment 2
Skill Formation Validation
Purpose

Validate:

Contribution 2
Skill Creation Trigger Theory

Research Question

Can ASFT correctly decide when a skill should emerge?

Setup

Provide repeated tasks:

Reflection Task 1

Reflection Task 2

Reflection Task 3

Reflection Task 4

Procedure

Track:

Reuse

Abstraction Gain

Transfer Score

Creation Cost


Compute:

SCV


Expected outcome:

ReflectionSkill


created automatically.

Metrics
Skill Creation Accuracy

Was skill creation beneficial?

False Skill Rate

Skills created but never reused.

Skill Utility
SU=AccuracyGain×CostReduction×TransferabilitySU = AccuracyGain \times CostReduction \times Transferability
Success Condition

Created skills reduce future reasoning cost.

Experiment 3
Transfer Learning Validation

This is probably the most important experiment.

Purpose

Test the central ASFT claim.

Research Question

Does solving Task A make Task B easier?

Setup

Training Tasks:

Reflection


Transfer Tasks:

Reflection + Counting

Reflection + Rotation

Reflection + Grouping

Procedure

Compare:

Baseline

No skill formation.

ASFT

Skill formation enabled.

Metrics
Transfer Score
TS=PerformanceAfter−PerformanceBeforeTS = PerformanceAfter - PerformanceBefore
Reasoning Cost Reduction
RCbefore−RCafterRC_{before} - RC_{after}
Success Condition

ASFT performs transfer tasks using fewer reasoning operations.

Experiment 4
Capability Growth Validation
Purpose

Validate:

Contribution 3
Capability Growth Metrics

Research Question

Does capability increase over time?

Setup

Sequence:

Task 1
Task 2
Task 3
...
Task N

Procedure

Track:

Skills

Concepts

Transfer

Reasoning Cost


after every task.

Metrics
Capability Growth Rate
CGR=Capabilityt−Capabilityt−1ΔtCGR = \frac {Capability_t-Capability_{t-1}} {\Delta t}
Intelligence Growth
IG=f(AG,SU,TS,CGR)IG = f(AG,SU,TS,CGR)
Success Condition

Capability grows monotonically.

Baseline Systems

This is crucial.

Without baselines:

No paper.

Baseline A
No Learning
Task
↓
Solve
↓
Forget


Purpose:

Measure zero growth.

Baseline B
Skill Library Only
Store Skills


but no invariant discovery.

Purpose:

Show skill storage alone is insufficient.

Baseline C
DreamCoder-Like
Compression
↓
Primitive Creation


Purpose:

Most important comparison.

Ablation Studies

These are mandatory.

Ablation A

Remove Invariant Detector.

Question:

Do skills still emerge?


Expected:

Much weaker transfer.

Ablation B

Remove Skill Creation Trigger.

Question:

Can invariants alone help?


Expected:

Limited benefit.

Ablation C

Remove Skill Library.

Question:

Can transfer happen without memory?


Expected:

Transfer collapses.

Statistical Validation

For every experiment collect:

Mean

Variance

Confidence Interval


for:

TS
SU
CGR
AG
Failure Conditions

We must define them honestly.

ASFT is weakened if:

Failure 1

Invariants cannot be discovered reliably.

Failure 2

Created skills are rarely reused.

Failure 3

Transfer score remains near zero.

Failure 4

Capability growth is indistinguishable from baseline.

Expected Paper Results Section

If experiments succeed:

Experiment	Expected ResultInvariant Discovery	High IS for recurring reasoning structures
Skill Formation	Automatic emergence of reusable skills
Transfer	Positive TS on related tasks
Capability Growth	Positive CGR over task sequence
Phase 8D Deliverables Completed

✅ Experiment 1: Invariant Discovery Validation

✅ Experiment 2: Skill Formation Validation

✅ Experiment 3: Transfer Learning Validation

✅ Experiment 4: Capability Growth Validation

✅ Baseline definitions

✅ DreamCoder-style comparison

✅ Ablation studies

✅ Success criteria

✅ Failure criteria

✅ Statistical evaluation framework

Next Phase

We should move to Phase 8E: Success Metrics & MVP Definition, where we answer:

What exactly counts as a successful prototype?
What is the smallest implementation we can build?
What can be deferred to v0.2/v1.0?
What results would be strong enough for an ARC Paper Track submission?

This phase will prevent us from overbuilding and keep the project focused on validating the three research contributions.