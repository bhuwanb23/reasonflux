Excellent. Phase 1F is arguably the highest-risk phase in all of ASFT v1.1.

Why?

Because Phase 14E and 14I concluded:

IG exists
✅

IG is computable
✅

IG measures intelligence
❌ Not established


In fact, v1.0's strongest criticism was:

"IG may simply be a mathematical composite of internal metrics."

So Phase 1F is not about improving IG.

Phase 1F is about answering:

"Does IG measure anything real at all?"

And importantly:

If it doesn't, are we willing to retire the intelligence-growth claim?

That makes this one of the most scientifically important phases in the entire v1.1 roadmap.

ASFT v1.1
Phase 1F – Intelligence Validation Benchmark Specification

Phase ID

ASFT-V1.1-PHASE-1F


Package

ASFT-V1.1-PHASE-1F-INTELLIGENCE-VALIDATION-SPEC-V1

Primary Research Question
RQ5

Do IG and IGR predict independently
measured future learning, adaptation,
or competence acquisition beyond
simpler baseline explanations?

Why This Phase Exists
v1.0 Findings

Phase 13E:

IG positive

IGR positive


Phase 14E:

IG
=
weighted composite


Phase 14I:

Construct validity
=
high risk


Current state:

IG may be useful

OR

IG may be bookkeeping.


Unknown.

Phase Goal

Build an evaluation framework that can determine:

Does IG correspond to
real future learning?

Core Principle

Intelligence must be validated externally.

Forbidden:

IG predicts IG

IG predicts CGR

IG predicts C_t


Required:

IG predicts something
outside its own formula.

Phase Structure
1F.1 Intelligence Audit

1F.2 Intelligence Definition

1F.3 Intelligence Taxonomy

1F.4 Independent Intelligence Battery

1F.5 Adaptation Framework

1F.6 Learning Framework

1F.7 Comparator Framework

1F.8 Evaluation Metrics

1F.9 Dataset & Split Design

1F.10 Preregistration Framework

1F.11 Retirement Criteria

1F.12 Readiness Review

1F.1 Intelligence Audit
Purpose

Understand why intelligence claims failed.

Inputs
Phase 13E

Phase 14E

Phase 14H

Phase 14I

Phase 14J

Questions
What does IG measure?

What evidence was missing?

What construct-validity problems exist?

Why was intelligence growth rejected?

Deliverable
intelligence_audit.md

1F.2 Intelligence Definition
Purpose

Define intelligence before measuring it.

Working Rule

Intelligence is NOT:

Metric growth

Score growth

Formula growth


alone.

A candidate intelligence measure must show:

Adaptation

Learning

Generalization

Future competence acquisition

Deliverable
intelligence_definition.md

Exit Criteria
Definition frozen.

1F.3 Intelligence Taxonomy
Purpose

Break intelligence into measurable categories.

I1
Learning Speed

I2
Adaptation Ability

I3
Transfer Ability

I4
Compositional Learning

I5
Generalization Ability

I6
Knowledge Efficiency

Goal

Avoid treating intelligence as one number.

1F.4 Independent Intelligence Battery

This is the heart of the benchmark.

Purpose

Create external targets.

Required Tests
Test A
Future Learning Rate


Can the system learn new tasks faster?

Test B
Adaptation Speed


Can the system adjust to changes?

Test C
Novel Environment Success

Test D
Few-Shot Acquisition

Test E
Cross-Domain Learning

Test F
Generalization Retention

Rule

No test may directly use:

IG

IGR

IE

CGR

Deliverable
intelligence_battery_spec.md

1F.5 Adaptation Framework
Purpose

Measure adaptation independently.

Examples:

Rule changes

Distribution shifts

Task-family shifts

Vocabulary shifts


Question:

Does higher IG predict adaptation?

Deliverable
adaptation_framework.md

1F.6 Learning Framework
Purpose

Measure future learning.

Possible outcomes:

Tasks learned

Learning speed

Sample efficiency

Retention


Question:

Does IG predict future learning?

Deliverable
learning_framework.md

1F.7 Comparator Framework
Purpose

Determine whether IG adds information.

Required Comparators
B1
Past Performance

B2
Experience Count

B3
Capability Score

B4
Memory Strength

B5
Transfer Metrics

B6
IG

Key Question

Can IG predict outcomes beyond:

Past performance

Experience

Capability

Memory


?

1F.8 Evaluation Metrics
Primary Endpoint

Must be frozen.

Examples:

Future Learning Success

Adaptation Success

Generalization Gain

Secondary Endpoints
Learning Speed

Sample Efficiency

Retention

Cross-Domain Success

Diagnostics
IG Stability

IG Variance

Metric Drift

1F.9 Dataset & Split Design
Required Splits
Development

Confirmatory

Replication

Rule

Future learning tasks remain unseen.

Rule

Adaptation tests remain unseen.

Deliverable
intelligence_dataset_protocol.md

1F.10 Preregistration Framework

Freeze:

Intelligence definition

Primary endpoint

Comparator set

Independent unit

SOI

Decision rules

Replication plan

Outcomes
Supported

Contradicted

Inconclusive

Unavailable

1F.11 Retirement Criteria

This is unique to Phase 1F.

Purpose

Define when the construct fails.

Intelligence Claim Survives

If:

IG predicts independent outcomes


and replicates.

Intelligence Claim Weakens

If:

IG only predicts internally-derived outcomes.

Intelligence Claim Retired

If:

IG provides no predictive value
beyond simpler variables.


Then:

Rename metric

Stop calling it intelligence.

Deliverable
intelligence_retirement_rules.md

1F.12 Readiness Review
Checklist
Intelligence Audit

✅

Intelligence Definition

✅

Taxonomy

✅

Intelligence Battery

✅

Adaptation Framework

✅

Learning Framework

✅

Comparators

✅

Metrics

✅

Splits

✅

Preregistration

✅

Retirement Rules

✅

Deliverables
intelligence_audit.md

intelligence_definition.md

intelligence_taxonomy.md

intelligence_battery_spec.md

adaptation_framework.md

learning_framework.md

intelligence_comparator_spec.md

intelligence_metrics.md

intelligence_dataset_protocol.md

intelligence_preregistration_template.md

intelligence_retirement_rules.md

phase1F_readiness_report.md

Phase 1F Exit Decision

PASS only if:

Intelligence is externally defined

External intelligence targets exist

Adaptation is measurable

Learning is measurable

IG is tested against alternatives

Retirement criteria are frozen

Replication is planned

Primary endpoint is frozen

Most Important Outcome

Phase 1F is designed to answer the question that v1.0 never could:

"If IG goes up, does the system actually become better at learning, adapting, or acquiring new competence in ways that simpler variables cannot explain?"

And unlike v1.0, Phase 1F explicitly allows the possibility that the answer is:

No.


If that happens, the benchmark doesn't fail.

The intelligence-growth claim fails.

That distinction is exactly what makes Phase 1F scientifically valuable.