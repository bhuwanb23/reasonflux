Phase 13A: Experimental Validation Setup

This is arguably the most important phase before any serious experimentation.

Why?

Because a poorly designed experiment can invalidate even a correct system.

At this point, ASFT has:

✅ Theory
✅ Architecture
✅ Specification
✅ Implementation
✅ Initial Results


Now we must ensure:

Results
=
Scientific Evidence


rather than:

Interesting Prototype Outputs

Objective of Phase 13A

Establish a rigorous, reproducible, paper-grade experimental framework.

By the end of 13A, every experiment should answer:

What is being tested?

Why is it being tested?

How is it being measured?

Against what baseline?

What constitutes success?

What constitutes failure?

Phase 13A Structure

I would split this into:

13A-1
Experimental Philosophy

13A-2
Experiment Governance

13A-3
Dataset Governance

13A-4
Randomization & Seed Policy

13A-5
Metric Governance

13A-6
Statistical Validation

13A-7
Reproducibility Framework

13A-8
Reporting Framework

13A-9
Experiment Registry

13A-10
Go/No-Go Criteria

13A-1 Experimental Philosophy

This is the foundation.

ASFT is NOT trying to prove:

Best ARC Solver


ASFT IS trying to prove:

Invariant Discovery

↓

Skill Formation

↓

Transfer

↓

Capability Growth


Therefore experiments should prioritize:

Primary Metrics
IS

SU

TS

CGR

IGR


before:

Accuracy

13A-2 Experiment Governance

Every experiment must have:

Experiment ID

Example:

EXP-01
Invariant Discovery

Hypothesis

Example:

Higher IS predicts higher TS.

Research Claim

Maps directly to:

IDT

SCT

CGM

Metrics

Clearly defined.

Success Threshold

Predefined.

Never changed after execution.

Critical Rule

No metric threshold should be modified after seeing results.

13A-3 Dataset Governance

This is extremely important.

Dataset Tiers
Tier 1

Synthetic

Current status:

✅ Implemented

Families:

Reflection

Rotation

Counting

Grouping


Purpose:

Validate mechanism.

Tier 2

Transfer Datasets

Examples:

Reflection+Count

Reflection+Grouping

Rotation+Count


Purpose:

Validate transfer.

Tier 3

ARC Dataset

Future.

Purpose:

External validity.

Dataset Separation

Never allow:

Discovery Tasks


and

Transfer Validation Tasks


to be identical.

Otherwise:

Transfer Illusion


occurs.

13A-4 Randomization & Seed Policy

Your current results use:

Seed 0


This is insufficient for paper-grade evidence.

Required Seed Set

Minimum:

0
1
2
3
4


Preferred:

10 seeds


For every experiment:

Collect:

Mean

Std Dev

Variance

Confidence Interval

Why?

To ensure:

Result
≠
Lucky Seed

13A-5 Metric Governance

One of the most important sections.

Every metric needs:

Definition
Formula
Interpretation
Range
Failure Condition

Example

TS

Transfer Score

TS=PerformanceAfter−PerformanceBeforeTS = PerformanceAfter - PerformanceBefore

Interpretation:

TS > 0

Positive Transfer


Failure:

TS ≤ 0


Do this for:

IS

SCV

SU

TS

TU

NTR

CGR

IG

IGR

13A-6 Statistical Validation

Currently missing from most prototypes.

Every experiment should report:

Mean
μ\mu
Standard Deviation
σ\sigma
Confidence Interval

95%

Effect Size

Especially for:

ASFT vs Baselines

Example

Instead of:

TS = 0.42


report:

TS = 0.42 ± 0.07


This dramatically improves paper credibility.

13A-7 Reproducibility Framework

A reviewer should be able to reproduce results.

Every run should store:

Seed

Dataset Version

Configuration

Thresholds

Metrics

Timestamp

Reproducibility Object

Each experiment should produce:

Experiment Record


containing:

Inputs

Configuration

Outputs

Metrics

Critical Rule

Every reported number must be reproducible.

13A-8 Reporting Framework

All experiments should generate the same structure.

Report Structure
Section 1

Configuration

Section 2

Dataset

Section 3

Metrics

Section 4

Results

Section 5

Failure Cases

Section 6

Observations

Why?

This makes Phase 14 much easier.

13A-9 Experiment Registry

Create a master experiment registry.

EXP-01

Invariant Discovery

Supports:

IDT

EXP-02

Skill Formation

Supports:

SCT

EXP-03

Transfer

Supports:

IDT + SCT

EXP-04

Capability Growth

Supports:

CGM

EXP-05

End-to-End ASFT

Supports:

All Contributions

EXP-06

Baselines

EXP-07

Ablations

EXP-08

ARC Validation

This registry becomes the backbone of the paper.

13A-10 Go/No-Go Criteria

Before moving to Phase 13B.

IDT Readiness

Must have:

✅ Invariants discovered

✅ IS operational

✅ Ranking operational

SCT Readiness

Must have:

✅ Skill creation

✅ SCV operational

✅ Skill reuse

Transfer Readiness

Must have:

✅ Positive TS

✅ Positive TU

CGM Readiness

Must have:

✅ Positive CGR

✅ Positive IG

Baseline Readiness

Must have:

✅ No Learning

✅ Skill Storage

✅ Random Skill

✅ DreamCoder-like

Reporting Readiness

Must have:

✅ Logs

✅ Metrics

✅ Reports

✅ Reproducibility

Phase 13A Deliverables

At completion, you should possess:

✅ Experiment Registry

✅ Dataset Policy

✅ Seed Policy

✅ Metric Definitions

✅ Statistical Policy

✅ Reporting Template

✅ Reproducibility Framework

✅ Go/No-Go Criteria

✅ Success Thresholds

✅ Failure Thresholds

✅ Experiment Governance

Specific Recommendation Based on Your Current Status

From the assessment you shared, your immediate priorities inside Phase 13A are:

Priority 1

Multi-seed execution

Current weakness:

Only Seed 0

Priority 2

A1-A5 ablation table

Current weakness:

Implemented
Not Reported

Priority 3

ARC dataset integration

Current weakness:

Synthetic Only

Priority 4

Confidence intervals

Current weakness:

Point Estimates Only

Most Important Outcome

The single most important decision of Phase 13A is:

No result in ASFT becomes evidence until it is reproducible, statistically characterized, compared against baselines, and mapped to a specific research claim.

That principle will govern every experiment in Phases 13B through 13H and ultimately determine whether the paper is viewed as a prototype report or a credible research contribution.