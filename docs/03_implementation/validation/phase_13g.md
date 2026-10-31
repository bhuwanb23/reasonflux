Phase 13G: ARC Validation Experiments

This is the phase that determines whether ASFT remains:

An interesting synthetic framework


or becomes:

An ARC-relevant research contribution


This phase is extremely important because your current implementation report already identifies the largest limitation:

Synthetic Tasks Only


Everything before this phase validates:

Internal Validity


Phase 13G validates:

External Validity


In simple terms:

Does ASFT survive contact with ARC?

Important Mindset

Do NOT approach ARC validation as:

Can ASFT beat ARC?


That is the wrong experiment.

Remember our strongest reviewer defense from Phase 9F:

We are NOT claiming:

ASFT solves ARC.


We ARE claiming:

ASFT studies skill formation,
transfer,
and capability growth.


ARC is simply the environment used to validate those claims.

Phase 13G Objective

Validate:

IDT on ARC

SCT on ARC

Transfer on ARC

Capability Growth on ARC


without changing the core theory.

Success Definition

Success is NOT:

High ARC Accuracy


Success IS:

ARC traces produce invariants

ARC invariants produce skills

ARC skills transfer

ARC capabilities grow

Phase 13G Structure
13G-1
ARC Validation Philosophy

13G-2
ARC Dataset Preparation

13G-3
ARC Trace Validation

13G-4
ARC Invariant Discovery

13G-5
ARC Skill Formation

13G-6
ARC Transfer Experiments

13G-7
ARC Capability Growth Experiments

13G-8
ARC Baseline Comparisons

13G-9
ARC Failure Analysis

13G-10
ARC Evidence Package

13G-1 ARC Validation Philosophy

This section is critical.

Wrong Question
Did ASFT solve ARC task #123?

Right Question
What capabilities emerged
while solving ARC tasks?


This distinction should drive every ARC experiment.

What ARC Should Validate

ARC should test:

IDT
Can invariants emerge?

SCT
Can skills emerge?

Transfer
Do skills help future ARC tasks?

CGM
Does capability grow?

13G-2 ARC Dataset Preparation

Before experiments.

ARC Task Taxonomy

Classify ARC tasks.

Create families:

Reflection

Rotation

Translation

Counting

Grouping

Object Detection

Pattern Completion

Symmetry

Why?

ASFT operates on:

Task Families


not isolated tasks.

Dataset Split

Very important.

Discovery Set

Used for:

Invariant Discovery

Transfer Set

Used for:

Transfer Validation

Holdout Set

Used for:

Final Evaluation


Never mix them.

ARC Family Coverage

Measure:

How many ARC families
ASFT touches.


This becomes part of Phase 14.

13G-3 ARC Trace Validation

Before any claims.

EXP-ARC-01
Trace Quality

Question:

Do ARC tasks generate
meaningful traces?


Procedure:

Sample:

20 ARC Tasks


Inspect:

Reasoning Steps

Operation Sequences


Expected:

Structured Traces


not:

Noise


Metrics:

Trace Quality Score

Trace Consistency

EXP-ARC-02
Trace Stability

Question:

Do similar ARC tasks
produce similar traces?


Expected:

Positive clustering.

This is a prerequisite for IDT.

13G-4 ARC Invariant Discovery

Validates IDT.

EXP-ARC-03
Reflection Invariants

Question:

Can reflection invariants
be discovered from ARC?


Expected:

ReflectionInvariant


appears.

EXP-ARC-04
Rotation Invariants

Expected:

RotationInvariant


appears.

EXP-ARC-05
Counting Invariants

Expected:

CountInvariant


appears.

EXP-ARC-06
Invariant Precision

Measure:

IP=ValidInvariantsDetectedInvariantsIP = \frac {ValidInvariants} {DetectedInvariants}

Expected:

Similar to synthetic tasks.

EXP-ARC-07
IS vs Transfer

Question:

Do strong ARC invariants
transfer better?


Expected:

Positive correlation.

This is a key experiment.

13G-5 ARC Skill Formation

Validates SCT.

EXP-ARC-08
Skill Emergence

Question:

Do ARC invariants
create skills?


Expected:

Skills emerge naturally.

EXP-ARC-09
Skill Utility

Measure:

SU


on ARC tasks.

Expected:

Positive utility.

EXP-ARC-10
Skill Reuse

Question:

Can a skill created
from ARC Task A
help ARC Task B?


Expected:

Positive reuse.

EXP-ARC-11
SCV Validation

Question:

Does SCV still predict
future usefulness?


Expected:

Positive correlation.

13G-6 ARC Transfer Experiments

Most important ARC experiments.

EXP-ARC-12
Near Transfer

Train:

Reflection ARC Tasks


Test:

New Reflection ARC Tasks


Expected:

Positive TS.

EXP-ARC-13
Cross-Family Transfer

Train:

Reflection


Test:

Reflection + Counting


Expected:

Positive transfer.

EXP-ARC-14
Structural Transfer

Train:

Several ARC Families


Test:

Novel ARC Family


Expected:

Partial transfer.

EXP-ARC-15
Reasoning Cost Reduction

Measure:

RCR=RCbefore−RCafterRCR = RC_{before} - RC_{after}

Expected:

Positive.

One of the strongest validations.

13G-7 ARC Capability Growth

Validates CGM.

EXP-ARC-16
Capability Emergence

Question:

Do capabilities emerge
from ARC experience?


Expected:

Capability clusters appear.

EXP-ARC-17
Capability Growth

Measure:

CGRCGR

across ARC tasks.

Expected:

Positive.

EXP-ARC-18
Coverage Growth

Question:

Does ARC family coverage increase?


Expected:

Positive.

EXP-ARC-19
Intelligence Growth

Measure:

IGIGRIG IGR

Expected:

Positive trend.

13G-8 ARC Baseline Comparisons

Repeat major baselines.

Baseline B1

No Learning

Expected:

Minimal transfer.

Baseline B2

Skill Storage

Expected:

Some reuse.

Baseline B3

Random Skills

Expected:

Poor utility.

Baseline B4

DreamCoder-like

Expected:

Compression benefits.

Question:

Does ASFT still outperform?

13G-9 ARC Failure Analysis

Extremely important.

Reviewers will ask this.

Failure 1

No Invariants Found

Meaning:

Trace Representation Wrong

Failure 2

Skills Never Reused

Meaning:

SCT Weak

Failure 3

Transfer Near Zero

Meaning:

Synthetic Success
did not generalize

Failure 4

Capability Growth Flat

Meaning:

CGM unsupported


Document everything honestly.

13G-10 ARC Evidence Package

This becomes one of the most important sections of the paper.

Figure 1

ARC Task Family Map

Figure 2

ARC Invariants

Figure 3

ARC Skill Emergence

Figure 4

ARC Transfer Results

Figure 5

ARC Capability Growth

Figure 6

ASFT vs Baselines on ARC

Table 1

ARC Dataset Summary

Table 2

Discovered ARC Invariants

Table 3

ARC Skills

Table 4

Transfer Results

Table 5

Capability Growth Results

Table 6

Failure Analysis

ARC-Specific Success Criteria

Phase 13G succeeds if:

✅ ARC tasks generate meaningful traces

✅ ARC invariants emerge

✅ ARC skills emerge

✅ Positive transfer exists

✅ Positive reasoning cost reduction exists

✅ Positive CGR exists

✅ Positive IG exists

✅ ASFT beats major baselines

✅ Results align with synthetic experiments

ARC-Specific Failure Criteria

Phase 13G fails if:

❌ ARC traces unusable

❌ No invariants discovered

❌ Skills not reused

❌ Transfer absent

❌ CGR flat

❌ Synthetic findings fail to replicate

Most Important ARC Experiments

If I were submitting to an ARC-related venue and could only show five experiments:

EXP-ARC-07
IS ↔ Transfer Correlation

EXP-ARC-10
Skill Reuse

EXP-ARC-13
Cross-Family Transfer

EXP-ARC-15
Reasoning Cost Reduction

EXP-ARC-17
Capability Growth


These five experiments directly validate the complete ASFT chain on ARC data:

ARC Tasks
↓
Reasoning Traces
↓
Invariant Discovery
↓
Skill Formation
↓
Transfer
↓
Capability Growth


and provide the strongest evidence that ASFT is not merely a synthetic-task framework, but a capability-growth framework that remains meaningful in an ARC environment.