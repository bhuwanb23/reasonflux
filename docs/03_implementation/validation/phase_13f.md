Phase 13F: Baseline & Ablation Experiments

This is the most important experimental phase for publication.

Many researchers think:

Best Result
=
Best Paper


That is wrong.

A reviewer is far more interested in:

WHY did it work?


than:

How much did it improve?


Phase 13F exists to answer exactly that question.

Why Phase 13F Matters

Without baselines:

ASFT improved.


Reviewer:

Maybe memory explains everything.


Without ablations:

ASFT improved.


Reviewer:

Maybe SCT doesn't matter.


Without Phase 13F:

Interesting system.
Weak scientific evidence.


With Phase 13F:

Strong causal evidence.

Phase 13F Objective

Answer:

What causes ASFT to work?

Which contribution matters most?

What happens when components are removed?

How much improvement comes from each component?

Phase 13F Structure
13F-1
Research Questions

13F-2
Baseline Philosophy

13F-3
Baseline Experiments

13F-4
Ablation Philosophy

13F-5
IDT Ablations

13F-6
SCT Ablations

13F-7
CGM Ablations

13F-8
Cross-Component Ablations

13F-9
Sensitivity Analysis

13F-10
Statistical Validation

13F-11
Evidence Package

13F-1 Research Questions

Everything in this phase should answer:

Q1

Does ASFT outperform no learning?

Q2

Does ASFT outperform memory-only systems?

Q3

Does SCT matter?

Q4

Does IDT matter?

Q5

Does transfer matter?

Q6

Does composition matter?

Q7

What contribution is most important?

Q8

What causes capability growth?

13F-2 Baseline Philosophy

A baseline should represent:

A plausible alternative explanation.


Not:

A weak competitor.

Golden Rule

Every baseline must be:

Reasonable

Competitive

Scientifically meaningful

Baseline Categories

We need four baseline families.

Family 1
No Learning

Tests:

Does learning matter?

Family 2
Memory-Based

Tests:

Does memory explain gains?

Family 3
Random Skill Systems

Tests:

Does SCT matter?

Family 4
DreamCoder-like

Tests:

Is ASFT merely compression?

13F-3 Baseline Experiments

These are mandatory.

Baseline B1
No Learning

Architecture:

Task
↓
Solve
↓
Forget


Purpose:

Establish zero-growth reference.

Expected:

TS ≈ 0

CGR ≈ 0

IG ≈ 0


Metrics:

IS

SU

TS

CGR

IG


Expected Table

Metric	ExpectedTS	Near zero
CGR	Near zero
IG	Near zero
Baseline B2
Skill Storage Only

Architecture:

Store Skills

No Invariant Discovery

No SCT


Purpose:

Test:

Does memory alone explain growth?


Expected:

Better than B1.

Worse than ASFT.

Critical Comparison

ASFT

vs

Skill Storage


This directly validates:

IDT

SCT

Baseline B3
Random Skill Creation

Architecture:

Randomly Promote Skills


Purpose:

Test SCT.

Question:

Does any skill help?

Or only well-selected skills?


Expected:

Higher skill count.

Lower utility.

Higher NTR.

Critical Metrics:

SU

TS

CGR

Baseline B4
DreamCoder-like

Most important baseline.

Architecture:

Task
↓
Compression
↓
Primitive
↓
Library


Purpose:

Novelty defense.

Question:

Is ASFT
just compression?


Expected:

DreamCoder-like:

Strong Compression

Moderate Transfer


ASFT:

Stronger Capability Growth


This baseline will appear prominently in the paper.

13F-4 Ablation Philosophy

Ablations answer:

What happens if we remove a contribution?


Unlike baselines:

Baseline
=
Alternative System

Ablation
=
Broken ASFT

General Ablation Rule

Remove:

One Component


while keeping everything else unchanged.

13F-5 IDT Ablations

Contribution 1.

Ablation A1
Remove Invariant Discovery

Architecture:

Trace
↓
No Invariants
↓
Skills


Question:

Do invariants matter?


Expected:

Transfer decreases.

Skill quality decreases.

Metrics:

TS

SU

CGR


Critical Result

If performance remains unchanged:

IDT weakened.

Ablation A1.1
Frequency-Only Invariants

Replace:

Transfer-Aware Discovery


with:

Frequency Counting


Question:

Does transfer-awareness matter?


Expected:

More spurious invariants.

13F-6 SCT Ablations

Contribution 2.

Ablation A2
Remove SCV

Architecture:

Invariant
↓
Always Create Skill


Question:

Does skill economics matter?


Expected:

Skill explosion.

Utility reduction.

Ablation A2.1
Random SCV

Replace:

SCV


with:

Random Promotion


Expected:

Lower utility.

Lower transfer.

Ablation A2.2
Remove Lifecycle

Disable:

Dormancy

Retirement

Reactivation


Expected:

Library bloat.

Ablation A2.3
Remove Composition

Disable:

Skill Composition


Question:

Does composition contribute to growth?


Expected:

Lower CGR.

Lower IG.

13F-7 CGM Ablations

Contribution 3.

Ablation A3
Remove Capability Layer

Architecture:

Skills Exist

Capabilities Do Not


Question:

Do capabilities matter?


Expected:

Growth becomes difficult to measure.

Ablation A3.1
Remove Growth Tracking

Disable:

CGR

IGR


Purpose:

Validate measurement contribution.

Expected:

System functions.

Growth becomes invisible.

Ablation A3.2
Remove Capability Portfolio

Treat capabilities independently.

Expected:

Reduced intelligence interpretation.

13F-8 Cross-Component Ablations

Most powerful experiments.

EXP-ABL-01
No Transfer

Disable:

Skill Reuse


Question:

Can capability growth occur
without transfer?


Expected:

Growth collapses.

EXP-ABL-02
No Skill Library

Skills created.

Never stored.

Expected:

Transfer disappears.

EXP-ABL-03
No Experience Memory

Disable trace history.

Expected:

No invariant discovery.

EXP-ABL-04
No Capability Formation

Skills exist.

Capabilities never emerge.

Expected:

IG drops significantly.

13F-9 Sensitivity Analysis

Often overlooked.

Reviewers love it.

Threshold Sensitivity

Vary:

SCV Threshold


Observe:

Skill Count

Transfer

CGR

IS Sensitivity

Vary:

Invariant Strength Threshold


Observe:

Precision

Recall

Composition Sensitivity

Vary:

Composition Requirements


Observe:

IG

Capability Emergence

Goal

Show:

Results are stable.

13F-10 Statistical Validation

Run:

Seed 0-9


recommended.

Report:

Mean

Std Dev

95% CI


for:

TS

SU

CGR

IG


For every:

Baseline

Ablation

ASFT

Effect Size Analysis

Very important.

Report:

ASFT vs DreamCoder

ASFT vs Storage

ASFT vs Random


Not just:

Difference


but:

Magnitude of Difference

13F-11 Evidence Package

This becomes one of the strongest sections of the paper.

Figure 1

ASFT vs Baselines.

Figure 2

Ablation comparison.

Figure 3

Contribution impact chart.

Figure 4

Sensitivity curves.

Table 1

Baseline results.

Table 2

Ablation results.

Table 3

Effect sizes.

Table 4

Sensitivity analysis.

Master Result Matrix
System	IS	SU	TS	CGR	IGASFT	?	?	?	?	?
No Learning	?	?	?	?	?
Skill Storage	?	?	?	?	?
Random Skills	?	?	?	?	?
DreamCoder-like	?	?	?	?	?
A1	?	?	?	?	?
A2	?	?	?	?	?
A3	?	?	?	?	?

This table alone may become one of the most important tables in the paper.

Success Criteria

Phase 13F succeeds if:

✅ ASFT beats all baselines

✅ Removing IDT hurts performance

✅ Removing SCT hurts performance

✅ Removing Transfer hurts performance

✅ Removing Composition hurts performance

✅ Removing Capability Layer hurts interpretation

✅ Results stable across seeds

✅ Effect sizes meaningful

Failure Criteria

Phase 13F fails if:

❌ Baselines match ASFT

❌ Ablations cause little degradation

❌ Random skills perform equally well

❌ Memory-only explains all gains

❌ DreamCoder-like matches capability growth

❌ Results highly sensitive to thresholds

Most Important Experiments in Entire Project

If reviewers only looked at 4 results:

ASFT vs DreamCoder-like

ASFT vs Skill Storage

No IDT Ablation

No SCT Ablation


those four experiments would probably determine whether the paper is accepted or rejected.

Final Outcome of Phase 13F

If Phase 13F succeeds, you will be able to make the strongest scientific claim in ASFT:

Capability growth is not explained by memory alone, random skill creation, or compression alone. It emerges from the interaction of invariant discovery, economically justified skill formation, transfer, and capability organization.

And that is essentially the complete experimental validation of:

Contribution 1
IDT

Contribution 2
SCT

Contribution 3
CGM


which is the entire ASFT thesis.