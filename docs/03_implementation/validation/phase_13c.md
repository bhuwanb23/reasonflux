# Phase 13C: Skill Formation Experiments (SCT Validation)

> **Current status (2026-10-31):** Phase 13C-SCT-V1 completed: calibration seeds 15–19 and confirmation seeds 20–29. The primary SCT superiority gate **failed**: SCT tied always-create and random-create, and memory-only trace retrieval had higher mean net value. See `reports/experiments/PHASE-13C-SCT-V1/evidence_package.md` and the saved raw record. Results are conditional synthetic evidence only. Legacy EXP-02 is preliminary only; Phase 13B and EXP-IDT-14 evidence remain unchanged.

This phase is dedicated to validating the strongest and most novel contribution of ASFT:

Skill Creation Trigger Theory (SCT)

If Phase 13B answered:

Can useful invariants be discovered?


Phase 13C answers:

Can useful skills emerge from those invariants?


and more importantly:

Can ASFT decide WHEN a skill should be created?


This phase is not about proving skills exist.

Almost every learning system has some notion of reusable knowledge.

This phase is about proving:

ASFT Skill Creation
>
Never Create Skills

ASFT Skill Creation
>
Always Create Skills

ASFT Skill Creation
>
Random Skill Creation

Phase 13C Objective

Validate the core SCT claim:

Skills should be created only when expected future value exceeds creation and maintenance cost.

At the end of Phase 13C, you should have evidence for:

✅ Skills emerge

✅ Skills are reused

✅ Skills reduce reasoning cost

✅ Skills transfer

✅ SCT decisions outperform naive alternatives

✅ Skill utility predicts future value

Phase 13C Structure

I recommend:

13C-1
Research Questions

13C-2
Skill Emergence Experiments

13C-3
SCV Validation Experiments

13C-4
Skill Utility Experiments

13C-5
Skill Reuse Experiments

13C-6
Skill Lifecycle Experiments

13C-7
Skill Composition Experiments

13C-8
Baseline & Ablation Experiments

13C-9
Statistical Validation

13C-10
SCT Evidence Package

13C-1 Research Questions

Everything in this phase should answer one of these.

Q1

Do useful skills emerge?

Q2

Does SCT create better skills than random creation?

Q3

Do skills reduce reasoning cost?

Q4

Do skills improve transfer?

Q5

Can skill utility predict future usefulness?

Q6

Can skills evolve through their lifecycle?

Q7

Can composed skills create new capabilities?

13C-2 Skill Emergence Experiments

These are the foundational experiments.

EXP-SCT-01
Reflection Skill Emergence
Goal

Verify:

ReflectionInvariant
↓
ReflectionSkill

Procedure

Run repeated reflection tasks.

Allow invariant accumulation.

Allow SCT decisions.

Observe

Does:

ReflectionSkill


emerge naturally?

Metrics
SCV

Evidence

Confidence

Reuse

Success

Skill promoted automatically.

No manual creation.

EXP-SCT-02
Rotation Skill Emergence

Same process.

Expected output:

RotationSkill

EXP-SCT-03
Counting Skill Emergence

Expected output:

CountSkill

EXP-SCT-04
Grouping Skill Emergence

Expected output:

GroupingSkill

Output

Create:

Skill Birth Table


Example:

Skill	Source Invariant	SCV	PromotedReflection	ReflectionInvariant	3.4	Yes
Rotation	RotationInvariant	2.8	Yes
13C-3 SCV Validation Experiments

This is probably the most important experiment block.

EXP-SCT-05
SCV Predictiveness

Research Question:

Does SCV predict future usefulness?

Procedure

For each skill:

Record:

SCV at creation


Track:

Future Utility

Future Reuse

Future Transfer

Expected

Higher SCV →

Higher future usefulness.

Metrics

Correlation:

SCV ↔ SU

SCV ↔ Reuse

SCV ↔ TS

EXP-SCT-06
SCV Threshold Study

Research Question:

Is the threshold reasonable?


Run:

Low Threshold

Medium Threshold

High Threshold


Observe:

Skills Created

Utility

Transfer


Expected:

Very low threshold:

Skill Explosion


Very high threshold:

Few Skills


Middle threshold:

Best Performance

13C-4 Skill Utility Experiments

Validates the economics framework.

EXP-SCT-07
Utility Tracking

For every skill measure:

SU=Benefit−CostSU = Benefit - Cost

Track over time.

Research Question:

Do useful skills remain useful?


Expected:

Core skills maintain positive utility.

EXP-SCT-08
Utility vs Reuse

Research Question:

Do useful skills get reused?


Measure:

SU

Reuse Count


Expected:

Positive correlation.

EXP-SCT-09
Utility vs Transfer

Research Question:

Do useful skills transfer better?


Measure:

SU

TS


Expected:

Positive correlation.

13C-5 Skill Reuse Experiments

One of the strongest proofs.

EXP-SCT-10
Reuse Validation

Question:

Are skills actually used?


Track:

Created Skills

Reused Skills


Metric:

ReuseRate=ReusedSkillsCreatedSkillsReuseRate = \frac {ReusedSkills} {CreatedSkills}

Expected:

High reuse rate.

EXP-SCT-11
Reasoning Cost Reduction

Question:

Do skills save reasoning?


Measure:

Before skill:

RC_before


After skill:

RC_after


Formula:

AG=RCbefore−RCafterAG = RC_{before} - RC_{after}

Expected:

Positive AG.

This is one of the strongest SCT validations.

13C-6 Skill Lifecycle Experiments

Validates 11D-3.

EXP-SCT-12
Growth Experiment

Question:

Do skills become more useful?


Track:

SU over time


Expected:

Core skills grow.

EXP-SCT-13
Dormancy Experiment

Question:

Can skills become dormant?


Stop exposing tasks.

Observe lifecycle transitions.

Expected:

Active
↓
Dormant

EXP-SCT-14
Reactivation Experiment

Question:

Can dormant skills return?


Reintroduce relevant tasks.

Expected:

Dormant
↓
Active

13C-7 Skill Composition Experiments

Supports 11D-4.

EXP-SCT-15
Reflection + Counting

Goal:

Verify composition.

Task:

Reflect Then Count


Expected:

ReflectionSkill
+
CountSkill

Metrics
Composition Utility

Transfer

Reasoning Reduction

EXP-SCT-16
Multi-Skill Composition

Task:

Reflection
+
Grouping
+
Counting


Expected:

Successful composition.

EXP-SCT-17
Composition Reuse

Question:

Do successful compositions reappear?


Expected:

Reusable compositions emerge.

13C-8 Baseline & Ablation Experiments

Mandatory.

Baseline B1

Never Create Skills

Expected:

Poor transfer.

Poor CGR.

Baseline B2

Always Create Skills

Expected:

Skill explosion.

Baseline B3

Random Skill Creation

Expected:

Low utility.

Baseline B4

Memory Only

Expected:

Reuse without SCT.

Ablation A1

Remove SCV

Question:

Does skill economics matter?


Expected:

Lower utility.

Ablation A2

Remove Lifecycle

Expected:

Skill explosion.

Ablation A3

Remove Composition

Expected:

Lower capability growth.

13C-9 Statistical Validation

Run:

Seed 0-4 minimum


Prefer:

10 seeds


For every major metric:

Report:

Mean

Std Dev

95% CI


Metrics:

SCV

SU

Reuse

TS

AG

CU

Example

Instead of:

Reuse Rate = 0.84


Report:

Reuse Rate = 0.84 ± 0.05

13C-10 SCT Evidence Package

At the end of Phase 13C produce:

Figure 1

Skill emergence timeline.

Figure 2

SCV vs Future Utility.

Figure 3

Utility growth over time.

Figure 4

Reasoning cost reduction.

Figure 5

Skill lifecycle transitions.

Figure 6

Composition success rates.

Table 1

Created skills.

Table 2

SCV statistics.

Table 3

Reuse statistics.

Table 4

Baseline comparison.

Table 5

Ablation comparison.

Success Criteria

Phase 13C succeeds if:

✅ ReflectionSkill emerges

✅ RotationSkill emerges

✅ CountSkill emerges

✅ GroupingSkill emerges

✅ SCV predicts usefulness

✅ Skills reused frequently

✅ Positive AG

✅ Positive TS

✅ Useful compositions emerge

✅ SCT beats random creation

✅ SCT beats always-create baseline

✅ Results stable across seeds

Failure Criteria

Phase 13C fails if:

❌ Skills rarely reused

❌ SCV unrelated to future utility

❌ No reasoning cost reduction

❌ No transfer improvement

❌ Random skill creation performs equally well

❌ Composition provides no benefit

❌ Utility does not predict future value

Most Important Experiments

If I had to pick only 4 experiments for the paper:

EXP-SCT-05
SCV Predictiveness

EXP-SCT-11
Reasoning Cost Reduction

EXP-SCT-10
Reuse Validation

EXP-SCT-15
Skill Composition


Because together they validate the full SCT chain:

Invariant
↓
SCV
↓
Skill Creation
↓
Reuse
↓
Reasoning Reduction
↓
Transfer
↓
Capability Growth


And that is the strongest scientific evidence for Contribution 2.