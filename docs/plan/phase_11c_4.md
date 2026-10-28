Phase 11C-4: Transfer-Aware Invariant Discovery

This is arguably the most important specification in the entire ASFT framework.

Why?

Because many systems can discover patterns.

Many systems can compress programs.

Many systems can store skills.

But ARC's fundamental question is:

How does solving Task A make Task B easier?

Everything in ASFT ultimately lives or dies on that question.

Position Within ASFT

Until now:

Task
↓
Trace
↓
Pattern
↓
Invariant


A normal system stops here.

ASFT continues:

Task
↓
Trace
↓
Invariant
↓
Transfer
↓
Skill
↓
Capability Growth


Transfer is not an evaluation metric.

Transfer is part of the learning mechanism itself.

Core ASFT Principle

Traditional view:

Pattern
↓
Invariant


ASFT view:

Pattern
↓
Invariant
↓
Transfer Validation
↓
True Invariant


Meaning:

An invariant is not fully accepted until it demonstrates usefulness beyond its original task family.

Formal Definition
Transfer-Aware Invariant

An invariant II is transfer-aware if:

It improves performance,
reduces reasoning cost,
or increases reuse
on tasks that were not used
to discover the invariant.

Why This Matters

Consider:

Tasks:

Reflect Red Shape

Reflect Blue Shape

Reflect Green Shape


System discovers:

Reflection


Question:

Is Reflection
actually useful?


Only one way to know:

Apply it to:

Reflect + Count

Reflect + Group

Reflect + Rotate


If performance improves:

Reflection
=
Transferable Invariant


Otherwise:

Reflection
=
Local Pattern

Transfer-Centric Learning Loop

Traditional Learning:

Task
↓
Solve
↓
Store


ASFT:

Task
↓
Solve
↓
Extract Invariant
↓
Test Transfer
↓
Promote


This extra stage is one of the main differentiators from simple memory systems.

Transfer Taxonomy

Not all transfer is equal.

We should formally classify it.

Type 1
Near Transfer

Small task variations.

Example:

Task A

Reflect Triangle


Task B

Reflect Square


Differences:

Shape changes


Underlying structure:

Same


Expected transfer:

Very High

Type 2
Moderate Transfer

Different task context.

Example:

Task A

Reflect Shape


Task B

Reflect Group


Expected transfer:

Medium

Type 3
Compositional Transfer

Most important for ARC.

Example:

Task A

Reflection


Task B

Reflection + Counting


Expected transfer:

Medium to High


Requires composition.

Type 4
Structural Transfer

Highest-value transfer.

Example:

Task A

Reflection


Task B

Rotation + Reflection + Grouping


Invariant becomes one component of a larger reasoning process.

Transfer Memory

A major new concept.

Every invariant should maintain:

Transfer History


not just:

Occurrence History


Example

ReflectionInvariant

Observed:
20 times

Transferred:
12 times

Successful Transfers:
10

Failed Transfers:
2


This information becomes crucial later for skill promotion.

Transfer Evidence Model

Each invariant accumulates evidence.

Discovery Evidence

How often observed.

Validation Evidence

How stable it is.

Transfer Evidence

How often it helped future tasks.

Total evidence:

Invariant Confidence

Transfer Score (Invariant-Level)

Until now TS was system-level.

We now define:

Invariant Transfer Score (ITS)

Measures:

How much transfer
is attributable
to one invariant.


Formula:

ITS(I)=∑TransferBenefits∑TransferAttemptsITS(I) = \frac {\sum TransferBenefits} {\sum TransferAttempts}

Interpretation:

0
=
No Transfer

1
=
Perfect Transfer

Example

ReflectionInvariant

Transfer Attempts:

20


Successful Transfer Events:

16

ITS=1620=0.8ITS = \frac{16}{20}=0.8

Very strong invariant.

Transfer Utility Function

Not every transfer event is equally useful.

We need weighting.

Define:

TU(I)=TransferSuccess×ReasoningReduction×TaskCoverageTU(I) = TransferSuccess \times ReasoningReduction \times TaskCoverage

Where:

TransferSuccess

How often transfer works.

ReasoningReduction

How much reasoning cost decreases.

TaskCoverage

How many task families benefit.

Example

ReflectionInvariant

Success = 0.8

Reduction = 0.7

Coverage = 0.6

TU=0.336TU=0.336

Higher:

Better Invariant

Transfer Graph

One of the most powerful future ideas.

Represent:

Task Family


as nodes.

Example

Reflection
     │
     ├──────── Count
     │
     ├──────── Grouping
     │
     └──────── Rotation


Edges represent:

Observed Transfer


This graph allows us to discover:

Where invariants travel


across tasks.

Transfer-Aware Ranking

Phase 11C-3 introduced:

InvariantScore=F×C×G×T×RInvariantScore = F \times C \times G \times T \times R

We now refine it.

Where:

T=ITS×TUT = ITS \times TU

meaning:

Transfer becomes an explicit ranking factor.

Result:

Frequent but non-transferable patterns are penalized.

Example

Candidate A

Reflection

Frequency High

Transfer High


Rank:

High


Candidate B

VerifyOutput

Frequency High

Transfer Low


Rank:

Low


Exactly what we want.

Transfer Validation Protocol

Every invariant must pass:

Stage 1

Discovery

Observed

Stage 2

Validation

Stable

Stage 3

Transfer Test

Applied to future tasks.

Stage 4

Transfer Confirmation

Positive ITS.

Stage 5

Promotion Eligibility

Can enter SCT.

Pipeline:

Observed
↓
Validated
↓
Transfer Tested
↓
Transfer Confirmed
↓
Promotable

Negative Transfer

Extremely important.

Most systems ignore this.

Example

ReflectionInvariant applied to:

Pure Counting Task


Performance worsens.

This is:

Negative Transfer


Define:

NTR=FailedTransferAttempts/TotalTransferAttemptsNTR = FailedTransferAttempts / TotalTransferAttempts

High NTR:

Penalty


This prevents harmful skills.

Transfer Confidence

Separate from Transfer Score.

Question:

How sure are we?


Depends on:

Number Of Transfer Events

Consistency

Success Rate


A new invariant may have:

High TS

Low Confidence


because evidence is limited.

Promotion Gate

Before an invariant enters SCT:

Must satisfy:

✅ Frequency Threshold

✅ Consistency Threshold

✅ Generality Threshold

✅ ITS Threshold

✅ NTR Below Limit

Only then:

Invariant
↓
Skill Candidate

Success Criteria

Transfer-Aware Discovery succeeds if:

✅ Strong invariants transfer

✅ Weak invariants do not

✅ Transfer predicts skill usefulness

✅ Transfer predicts future reasoning reduction

✅ Negative transfer is filtered

Failure Criteria

Fails if:

❌ Transfer unrelated to invariant quality

❌ Frequent patterns dominate

❌ Harmful invariants promoted

❌ Transfer graphs contain mostly noise

Deliverables of Phase 11C-4

✅ Transfer-aware invariant definition

✅ Transfer taxonomy

✅ Transfer memory model

✅ Invariant Transfer Score (ITS)

✅ Transfer Utility (TU)

✅ Transfer graph model

✅ Transfer-aware ranking

✅ Negative transfer handling

✅ Transfer confidence model

✅ Promotion gate specification

✅ Success/failure criteria

Most Important Outcome

The single most important decision of Phase 11C-4 is:

ASFT does not define an invariant by recurrence alone. An invariant becomes valuable only when it demonstrates measurable transfer to future tasks.

That is the direct implementation of the ARC principle:

Task A
↓
Learn Something
↓
Task B Easier


and it is the strongest conceptual bridge between Invariant Discovery Theory (IDT) and Skill Creation Trigger Theory (SCT).

Next Recommended Subphase

Phase 11C-5: Failure Modes & Edge Cases

This will be the final hardening phase for IDT, covering:

spurious invariants,
invariant explosion,
transfer leakage,
catastrophic promotion,
sparse-task regimes,
conflicting invariants,
noisy traces,
adversarial task sequences,
and safeguards needed before implementation.