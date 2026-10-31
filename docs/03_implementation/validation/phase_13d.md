Phase 13D: Transfer Learning Experiments

This is arguably the most important experimental phase in the entire ASFT project.

Why?

Because:

IDT
without transfer
=
Pattern Mining

SCT
without transfer
=
Skill Storage

CGM
without transfer
=
Metric System


Transfer is the bridge that connects all three contributions.

If Phase 13B validated:

Can we discover invariants?


and Phase 13C validated:

Can we create useful skills?


then Phase 13D validates:

Do those skills actually make future tasks easier?


This is the direct experimental realization of the ASFT thesis.

Phase 13D Objective

Validate the central transfer hypothesis:

Knowledge extracted from previous experiences can reduce future reasoning cost and improve future problem-solving capability.

By the end of Phase 13D, you should have evidence that:

✅ Transfer exists

✅ Transfer is measurable

✅ Skills enable transfer

✅ Invariants predict transfer

✅ Transfer reduces reasoning cost

✅ Transfer contributes to capability growth

✅ Transfer is better than baseline approaches

Phase 13D Structure
13D-1
Research Questions

13D-2
Near Transfer Experiments

13D-3
Moderate Transfer Experiments

13D-4
Compositional Transfer Experiments

13D-5
Structural Transfer Experiments

13D-6
Transfer Cost Reduction Experiments

13D-7
Negative Transfer Experiments

13D-8
Baseline & Ablation Experiments

13D-9
Statistical Validation

13D-10
Transfer Evidence Package

13D-1 Research Questions

Everything in this phase should answer:

Q1

Does solving Task A help Task B?

Q2

Do skills enable transfer?

Q3

Do invariants predict transfer quality?

Q4

How much reasoning cost is saved?

Q5

Can transfer occur across task families?

Q6

When does transfer fail?

Q7

Can transfer explain capability growth?

Transfer Taxonomy

Before experiments, classify transfer.

This becomes very important later for the paper.

Type 1
Near Transfer

Small variations.

Example:

Training

Reflect Triangle


Testing

Reflect Square


Expected:

Very High Transfer.

Type 2
Moderate Transfer

Different context.

Training

Reflect Object


Testing

Reflect Object Group


Expected:

Medium Transfer.

Type 3
Compositional Transfer

Training

Reflection


Testing

Reflection + Counting


Expected:

Positive Transfer.

Type 4
Structural Transfer

Most difficult.

Training

Reflection


Testing

Reflection + Grouping + Counting


Expected:

Lower but measurable transfer.

13D-2 Near Transfer Experiments

These should be easiest.

EXP-TR-01
Reflection Family Transfer

Training:

Reflection Tasks


Testing:

Modified Reflection Tasks


Measure:

TS

Reasoning Cost Reduction

Reuse Rate


Expected:

Strong positive transfer.

EXP-TR-02
Rotation Family Transfer

Same design.

Expected:

RotationSkill reused.

EXP-TR-03
Counting Family Transfer

Expected:

CountSkill reused.

Goal

Establish that transfer exists under favorable conditions.

13D-3 Moderate Transfer Experiments

Harder.

EXP-TR-04
Reflection → Reflection Grouping

Training:

Reflection


Testing:

Reflection + Grouping


Question:

Can ReflectionSkill still help?

Expected:

Positive TS.

EXP-TR-05
Rotation → Rotation Count

Expected:

Positive transfer.

EXP-TR-06
Grouping → Counting Groups

Expected:

Partial transfer.

Goal

Validate cross-context transfer.

13D-4 Compositional Transfer Experiments

This directly validates Phase 11D-4.

EXP-TR-07
Reflection + Count

Training:

Reflection

Count


separately.

Testing:

Reflection + Count


Expected:

Skill composition occurs.

Metrics:

TS

Composition Utility

Reasoning Reduction

EXP-TR-08
Reflection + Grouping

Same setup.

EXP-TR-09
Rotation + Counting

Same setup.

Goal

Demonstrate capability emergence from skill composition.

13D-5 Structural Transfer Experiments

Most important scientifically.

EXP-TR-10
Multi-Skill Structural Transfer

Training:

Reflection

Rotation

Grouping


Testing:

Reflection
+
Rotation
+
Grouping


Question:

Can prior skills cooperate?

Expected:

Positive transfer.

EXP-TR-11
Novel Structure Transfer

Testing task contains:

Known Skills

Unknown Arrangement


Expected:

Partial transfer.

This is very close to ARC philosophy.

13D-6 Transfer Cost Reduction Experiments

One of the strongest validations.

EXP-TR-12
Reasoning Cost Reduction

Question:

Does transfer save reasoning?


Measure:

RCR=RCbefore−RCafterRCR = RC_{before} - RC_{after}

Expected:

Positive.

EXP-TR-13
Search Reduction

Question:

Does transfer reduce exploration?


Track:

Operations

Steps

Candidates Evaluated


Expected:

Lower search effort.

EXP-TR-14
Skill Reuse Efficiency

Question:

Does retrieval outperform rediscovery?


Expected:

Reuse cheaper than reconstruction.

13D-7 Negative Transfer Experiments

Critical for robustness.

EXP-TR-15
Reflection on Counting

Apply:

ReflectionSkill


to:

Pure Counting Task


Expected:

Negative transfer.

Why Important?

Validates NTR metric.

EXP-TR-16
Random Skill Application

Purpose:

Measure false transfer.

Expected:

Low utility.

High NTR.

EXP-TR-17
Wrong Composition

Example:

Reflection
+
Unrelated Skill


Expected:

Transfer decreases.

Goal

Show ASFT can distinguish:

Good Transfer

Bad Transfer

13D-8 Baseline & Ablation Experiments

Mandatory.

Baseline B1

No Learning

Expected:

TS≈0TS \approx 0
Baseline B2

Memory Only

Expected:

Some reuse.

Limited transfer.

Baseline B3

Random Skills

Expected:

High NTR.

Baseline B4

DreamCoder-like

Expected:

Transfer through compression.

Compare against:

ASFT

Ablation A1

Remove Invariants

Question:

Do invariants drive transfer?

Ablation A2

Remove SCT

Question:

Do skills drive transfer?

Ablation A3

Remove Skill Library

Question:

Can transfer occur without persistence?

Ablation A4

Disable Composition

Question:

Can structural transfer still occur?

Expected

Performance degrades.

13D-9 Statistical Validation

Run:

Seed 0-4 minimum


Prefer:

10 Seeds


Report:

Mean

Std Dev

95% CI


for:

TS

TU

NTR

RCR

Reuse


Example:

Instead of:

TS = 0.41


report:

TS = 0.41 ± 0.06

Correlation Studies

Very important.

Study:

IS vs TS

Supports IDT.

SU vs TS

Supports SCT.

TS vs CGR

Supports CGM.

Expected:

Positive relationships.

13D-10 Transfer Evidence Package

Produce paper-ready artifacts.

Figure 1

Transfer taxonomy.

Figure 2

Transfer score by task family.

Figure 3

Reasoning cost reduction.

Figure 4

Transfer growth over time.

Figure 5

Positive vs negative transfer.

Table 1

Near transfer results.

Table 2

Moderate transfer results.

Table 3

Compositional transfer results.

Table 4

Structural transfer results.

Table 5

Baseline comparison.

Table 6

Ablation comparison.

Success Criteria

Phase 13D succeeds if:

✅ Positive TS across task families

✅ Positive RCR

✅ Skills reused successfully

✅ Composition improves transfer

✅ Structural transfer exists

✅ Negative transfer detected correctly

✅ ASFT beats baselines

✅ Ablations reduce transfer

✅ Results stable across seeds

Failure Criteria

Phase 13D fails if:

❌ TS ≈ 0

❌ Skills not reused

❌ Composition adds no value

❌ Negative transfer undetected

❌ Baselines perform equally well

❌ Transfer unrelated to invariants

❌ Transfer unrelated to skills

Most Important Experiments

If I had to pick only 5 experiments for the paper:

EXP-TR-07
Reflection + Count

EXP-TR-10
Structural Transfer

EXP-TR-12
Reasoning Cost Reduction

EXP-TR-15
Negative Transfer

IS ↔ TS Correlation


Together they validate the central ASFT chain:

Invariant
↓
Skill
↓
Transfer
↓
Reduced Reasoning Cost
↓
Capability Growth


which is the core scientific argument of the entire framework.