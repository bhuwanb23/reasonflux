Phase 9C: Experiment Matrix

This is the phase that converts everything into an execution-ready research plan.

After this phase, every future coding task should map to:

Contribution
↓
Hypothesis
↓
Experiment
↓
Metric
↓
Expected Result
↓
Paper Figure


If a coding task cannot be mapped into this chain, we should not build it.

Master Experiment Matrix

We have 3 contributions:

Invariant Discovery Theory (IDT)
Skill Creation Trigger Theory (SCT)
Capability Growth Metrics (CGM)

And 1 grand hypothesis:

Invariant Discovery
↓
Skill Formation
↓
Transfer
↓
Capability Growth

Experiment E1
Invariant Discovery Validation
Purpose

Validate:

Contribution 1
Invariant Discovery Theory

Research Question

Can ASFT identify stable invariants across related reasoning traces?

Dataset

Reflection Family

Reflection Task A
Reflection Task B
Reflection Task C
Reflection Task D


Rotation Family

Rotation Task A
Rotation Task B
Rotation Task C
Rotation Task D


Counting Family

Counting Task A
Counting Task B
Counting Task C
Counting Task D

Inputs
Reasoning Traces

Output
Discovered Invariants

Metrics
Primary

Invariant Strength

IS

Secondary

Invariant Precision

Correct Invariants
/
Detected Invariants

Secondary

Invariant Recall

Detected True Invariants
/
Total True Invariants

Expected Result

Reflection tasks:

Reflection Invariant


Rotation tasks:

Rotation Invariant


Counting tasks:

Counting Invariant

Paper Figure

Figure 1

Task Family
↓
Trace Clustering
↓
Invariant Discovery

Success Threshold
Invariant Precision > 70%

Experiment E2
Skill Formation Validation
Purpose

Validate:

Contribution 2
Skill Creation Trigger Theory

Research Question

Can ASFT determine when a reusable skill should emerge?

Dataset

Repeated Reflection Tasks

Reflection 1
Reflection 2
Reflection 3
Reflection 4
Reflection 5

Inputs
Invariant
Reuse Count
Reasoning Cost
Transfer Potential

Output
Skill Created?

Metrics
Primary

Skill Creation Value

SCV

Secondary

Skill Utility

SU

Secondary

Reuse Count

RCount

Expected Result

Reflection skill emerges automatically.

Paper Figure

Figure 2

Repeated Trace
↓
Invariant
↓
SCV Calculation
↓
Skill Creation

Success Threshold
Most Created Skills
must be reused.

Experiment E3
Reasoning Cost Reduction
Purpose

Validate core ASFT claim.

Research Question

Do created skills reduce reasoning cost?

Dataset

Reflection Tasks

Before Skill Creation

After Skill Creation

Inputs
Skill Library State

Metrics
Primary

Reasoning Cost

RC

Primary

Abstraction Gain

AG
=
RC_before
-
RC_after

Expected Result
RC_after
<
RC_before

Paper Figure

Figure 3

Reasoning Cost
vs
Number of Skills

Success Threshold

Positive AG.

Experiment E4
Transfer Learning Validation

This is probably the most important experiment.

Purpose

Test:

Task A
↓
Task B Easier

Research Question

Do learned skills transfer to related tasks?

Training Tasks
Reflection Family

Evaluation Tasks
Reflection + Counting

Reflection + Rotation

Reflection + Grouping

Metrics
Primary

Transfer Score

TS

Secondary

Accuracy

Secondary

Reasoning Cost Reduction

Expected Result
TS > 0

Paper Figure

Figure 4

Transfer Score
Across Task Families

Success Threshold

Transfer significantly exceeds baseline.

Experiment E5
Capability Growth Validation
Purpose

Validate:

Contribution 3
Capability Growth Metrics

Research Question

Does the system become more capable over time?

Dataset

Sequential Tasks

Task1
Task2
Task3
...
TaskN

Metrics
Primary

Capability Growth Rate

CGR

Secondary

Intelligence Growth

IG

Secondary

Transfer Score

TS

Expected Result
Positive Growth Curve

Paper Figure

Figure 5

Capability
vs
Tasks Solved

Success Threshold

CGR remains positive.

Experiment E6
End-to-End ASFT Validation

This is the paper's centerpiece.

Purpose

Validate Grand Hypothesis.

Research Question

Does ASFT produce:

Invariant Discovery
↓
Skill Creation
↓
Transfer
↓
Capability Growth

Pipeline
Task A
↓
Invariant

Invariant
↓
Skill

Skill
↓
Transfer

Transfer
↓
Capability Growth

Metrics
IS
SCV
SU
TS
CGR
IG

Expected Result

All links remain positive.

Paper Figure

Figure 6

The complete ASFT pipeline.

Baseline Matrix

Every experiment must compare against:

Baseline A

No Learning

Solve
Forget

Baseline B

Skill Storage Only

Store Skills
No Invariant Discovery

Baseline C

DreamCoder-like

Compression
Primitive Creation

Baseline D

Random Skill Creation

Create Skills Randomly

Experimental Group

ASFT

Invariant Discovery
+
SCT
+
Skill Library

Ablation Matrix
Ablation	RemovedA1	Invariant Detector
A2	Skill Trigger
A3	Skill Library
A4	Transfer Module
A5	Capability Metrics
Claims → Experiments Matrix
Contribution	ExperimentIDT	E1
SCT	E2
SCT	E3
SCT	E4
CGM	E5
Grand Hypothesis	E6
Paper Artifact Matrix
Figure	PurposeFig 1	Invariant Discovery
Fig 2	Skill Formation
Fig 3	Cost Reduction
Fig 4	Transfer Learning
Fig 5	Capability Growth
Fig 6	End-to-End ASFT
Deliverables Completed for Phase 9C

✅ Full experiment matrix

✅ Dataset mapping

✅ Metric mapping

✅ Expected results

✅ Baseline matrix

✅ Ablation matrix

✅ Paper figure plan

✅ Claims-to-experiments mapping

✅ End-to-end validation strategy

Next Step

Proceed to Phase 9D: Baseline & Ablation Strategy Deep Dive.

Although we already identified baselines and ablations, Phase 9D should rigorously define:

exactly how each baseline works,
why each baseline is fair,
what results would demonstrate superiority,
and how to defend the comparisons against reviewer criticism.

This is often where strong research papers differentiate themselves from interesting ideas.