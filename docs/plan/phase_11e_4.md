Phase 11E-4: Evaluation & Benchmarking Framework

This is the phase where ASFT becomes a scientifically testable framework.

Up to now, we have defined:

11E-1
Capability Representation

11E-2
Capability Growth Measurement

11E-3
Intelligence Growth Model


However, none of those matter unless we can answer:

How do we evaluate whether ASFT actually works?

This phase defines the complete benchmarking, validation, evaluation, comparison, reporting, and scientific evidence framework for ASFT.

Why This Phase Matters

Most systems are evaluated using:

Accuracy

Success Rate

Benchmark Score


ASFT cannot rely on those alone.

Why?

Because ASFT's primary claim is:

Capability Growth


not:

Single Task Success


Therefore we need a new evaluation hierarchy.

Goal of Phase 11E-4

Define:

What is evaluated?

How is it evaluated?

Against what?

Under which conditions?

What counts as success?

What counts as failure?

Evaluation Hierarchy

The evaluation hierarchy should mirror the ASFT hierarchy.

Invariant Evaluation
↓
Skill Evaluation
↓
Transfer Evaluation
↓
Capability Evaluation
↓
Intelligence Evaluation


Each layer supports the next.

Level 1: Invariant Evaluation

Supports:

Contribution 1
(IDT)

Core Question
Are meaningful invariants being discovered?

Metrics
Invariant Strength (IS)
IS=Frequency×Consistency×Generality×Transfer×ReasoningValueIS = Frequency \times Consistency \times Generality \times Transfer \times ReasoningValue
Invariant Precision
IP=UsefulInvariantsDetectedInvariantsIP = \frac {UsefulInvariants} {DetectedInvariants}
Invariant Recall
IR=DetectedTrueInvariantsTrueInvariantsIR = \frac {DetectedTrueInvariants} {TrueInvariants}
Invariant Confidence

Measures certainty.

Success Conditions

✅ Reflection invariant discovered

✅ Rotation invariant discovered

✅ Counting invariant discovered

✅ Transfer-relevant invariants rank highly

Failure Conditions

❌ Noise dominates

❌ Random patterns dominate

❌ Useful invariants missed

Level 2: Skill Evaluation

Supports:

Contribution 2
(SCT)

Core Question
Do useful skills emerge?

Metrics
Skill Utility (SU)
SU=Benefit−CostSU = Benefit - Cost
Reuse Frequency (RF)
RF=SkillUsesRF = SkillUses
Transfer Contribution (STC)

Measures:

How much transfer
a skill generates.

Skill Health Score (SHS)

Depends on:

Utility

Transfer

Reuse

Confidence

Success Conditions

✅ Skills reused

✅ Utility positive

✅ Transfer positive

✅ Core skills emerge

Failure Conditions

❌ Skill explosion

❌ No reuse

❌ Negative utility

Level 3: Transfer Evaluation

This is one of the most important layers.

Core Question
Does Task A help Task B?

Transfer Taxonomy

We already defined:

Near Transfer

Moderate Transfer

Compositional Transfer

Structural Transfer

Metrics
Transfer Score (TS)
TS=PerformanceAfter−PerformanceBeforeTS = PerformanceAfter - PerformanceBefore
Transfer Utility (TU)
TU=TransferSuccess×Coverage×ReasoningReductionTU = TransferSuccess \times Coverage \times ReasoningReduction
Transfer Diversity (TD)

Measures:

How many task families benefit.

Negative Transfer Rate (NTR)
NTR=NegativeTransfersTransferAttemptsNTR = \frac {NegativeTransfers} {TransferAttempts}
Success Conditions

✅ Positive TS

✅ Positive TU

✅ Cross-family transfer

✅ Low NTR

Failure Conditions

❌ Transfer collapse

❌ Transfer illusion

❌ High NTR

Level 4: Capability Evaluation

Supports:

CGM

Core Question
Are capabilities growing?

Metrics
Capability Growth Rate
CGR=Ct−Ct−1ΔtCGR = \frac {C_t-C_{t-1}} {\Delta t}
Capability Coverage
CCov=SupportedFamiliesTotalFamiliesCCov = \frac {SupportedFamilies} {TotalFamilies}
Capability Utility

Aggregated capability value.

Capability Acceleration
CA=CGRt−CGRt−1ΔtCA = \frac {CGR_t-CGR_{t-1}} {\Delta t}
Success Conditions

✅ Positive CGR

✅ Growing coverage

✅ Increasing utility

✅ Emerging capabilities

Failure Conditions

❌ Capability stagnation

❌ Coverage stagnation

❌ Capability collapse

Level 5: Intelligence Evaluation

Highest layer.

Core Question
Is the system becoming more intelligent?

Metrics
Intelligence Growth (IG)
IG=f(AG,SU,TS,CGR,CP,AD)IG = f( AG, SU, TS, CGR, CP, AD )
Intelligence Growth Rate (IGR)
IGR=IGt−IGt−1ΔtIGR = \frac {IG_t-IG_{t-1}} {\Delta t}
Intelligence Efficiency (IE)
IE=IGExperienceIE = \frac {IG} {Experience}
Intelligence Elasticity

Measures adaptation speed.

Success Conditions

✅ Positive IGR

✅ Positive IE

✅ Positive adaptation

✅ Positive composition growth

Failure Conditions

❌ Growth illusion

❌ Intelligence collapse

❌ No capability expansion

Benchmarking Framework

Now define benchmark levels.

Benchmark Level 1
Synthetic Skill Formation Benchmark

Purpose:

Validate theory.

Task Families:

Reflection

Rotation

Counting

Grouping


Measures:

IDT

SCT

CGM

Benchmark Level 2
Transfer Benchmark

Purpose:

Validate transfer.

Examples:

Reflection + Count

Reflection + Group

Rotation + Count


Measures:

TS

TU

NTR

Benchmark Level 3
Capability Benchmark

Purpose:

Validate growth.

Long task sequences.

Measures:

CGR

IGR

Coverage

Benchmark Level 4
ARC Validation Benchmark

Purpose:

Show relevance.

Selected ARC task families:

Reflection

Rotation

Object Grouping

Counting


Not leaderboard chasing.

Theory validation.

Baseline Framework

Every experiment must compare against:

Baseline A

No Learning

Solve

Forget


Expected:

CGR ≈ 0

Baseline B

Skill Storage Only

Memory

No Invariant Discovery


Expected:

Moderate transfer.

Baseline C

Random Skill Creation

No SCT


Expected:

Poor utility.

Baseline D

DreamCoder-like

Compression

Primitive Creation


Expected:

Strong compression.

Weaker skill economics.

Experimental Group

ASFT

IDT

SCT

CGM

Ablation Framework

We already defined:

A1

Remove IDT

A2

Remove SCT

A3

Remove Skill Library

A4

Remove Transfer

A5

Remove CGM

Each contribution must be independently testable.

Evidence Framework

A critical section.

Every claim must map to:

Claim
↓
Evidence
↓
Metric
↓
Experiment


Example:

Claim:

Skills reduce reasoning cost.


Evidence:

RC_before > RC_after


Metric:

AG


Experiment:

Transfer Benchmark

Reporting Framework

Every evaluation run should produce:

Report 1

Invariant Report

Contains:

IS

Precision

Recall

Report 2

Skill Report

Contains:

SU

Reuse

Health

Report 3

Transfer Report

Contains:

TS

TU

NTR

Report 4

Capability Report

Contains:

CGR

Coverage

Capability Utility

Report 5

Intelligence Report

Contains:

IG

IGR

IE

Statistical Framework

Important for paper quality.

Track:

Mean

Median

Variance

Confidence Intervals


for all major metrics.

Avoid:

Single Run Results

Benchmark Success Criteria

ASFT benchmarking succeeds if:

✅ Invariants emerge

✅ Skills emerge

✅ Transfer improves

✅ Capability grows

✅ Intelligence metrics improve

✅ Baselines are outperformed

✅ Ablations show meaningful degradation

Benchmark Failure Criteria

ASFT benchmarking fails if:

❌ Transfer absent

❌ Skills not reused

❌ Capability growth flat

❌ Intelligence metrics meaningless

❌ Baselines perform equally well

Evaluation Maturity Levels

Useful future framework.

Level 1

Pattern Discovery

Level 2

Skill Formation

Level 3

Transfer Learning

Level 4

Capability Growth

Level 5

Intelligence Growth

ASFT should progress through these levels.

Relationship To Entire Framework

This phase connects:

Theory
↓
Metrics
↓
Experiments
↓
Evidence
↓
Paper


Without this phase:

ASFT remains a theory.


With this phase:

ASFT becomes scientifically testable.

Deliverables of Phase 11E-4

✅ Evaluation hierarchy

✅ Invariant evaluation framework

✅ Skill evaluation framework

✅ Transfer evaluation framework

✅ Capability evaluation framework

✅ Intelligence evaluation framework

✅ Benchmark hierarchy

✅ Baseline framework

✅ Ablation framework

✅ Evidence framework

✅ Reporting framework

✅ Statistical framework

✅ Success criteria

✅ Failure criteria

✅ Evaluation maturity model

Most Important Outcome

The single most important decision of Phase 11E-4 is:

ASFT is evaluated not by how many tasks it solves, but by how effectively it converts experience into transferable capabilities and measurable intelligence growth.

This fully operationalizes Contribution 3 (CGM) and prepares us for the final CGM phase:

Phase 11E-5: Capability Failure Modes & Robustness

where we stress-test the entire capability and intelligence growth framework against:

growth illusions,
metric gaming,
capability collapse,
transfer collapse,
intelligence stagnation,
benchmark overfitting,
misleading growth signals,
and long-term system stability.