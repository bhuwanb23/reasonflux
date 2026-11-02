Excellent. Phase 2D answers:

Can we generate traces?


Phase 2E asks the much harder question:

Can those traces actually produce invariants?


This is where the original ASFT mechanism chain truly begins.

Remember the Phase 13G failure cascade:

Coverage low

↓

3 successful traces

↓

0 invariant candidates

↓

0 skills

↓

0 transfer

↓

0 capabilities


Phase 2D separates trace-generation failure from downstream failure.

Phase 2E now asks:

If traces exist, can invariant discovery work at all?

ASFT v1.1 Phase 2E
Invariant Discovery Audit

Phase ID

ASFT-V1.1-PHASE-2E


Package

ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1

Phase Objective

Audit the complete invariant-discovery pipeline.

Determine:

Whether recurring structures exist

Whether invariant candidates can be generated

Whether support thresholds are reasonable

Whether invariant discovery fails because:

No traces

No recurrence

Poor miner

Support rules

Representation limits

Core Research Questions
R2E-1
Can invariant candidates be generated?

R2E-2
Are recurring structures present?

R2E-3
Are support thresholds eliminating candidates?

R2E-4
Does invariant discovery fail because
of the miner or because of upstream scarcity?

R2E-5
If candidates exist, do they survive validation?

Phase Structure
2E.1 Historical Invariant Audit

2E.2 Invariant Taxonomy

2E.3 Recurrence Benchmark

2E.4 Candidate Generation Audit

2E.5 Support Threshold Audit

2E.6 Invariant Validation Audit

2E.7 Discovery Yield Benchmark

2E.8 Failure Localization

2E.9 Reporting Framework

2E.10 Readiness Review

2E.1 Historical Invariant Audit
Purpose

Reconstruct what happened in 13G.

Required Findings

Examples:

Successful traces

Raw patterns

Candidate invariants

Support-qualified invariants

Final invariants

Questions
How many candidates existed?

Where were they lost?

Which thresholds mattered?

Deliverable
historical_invariant_audit.md

2E.2 Invariant Taxonomy
Purpose

Define invariant categories.

I1
Exact Structural Invariant

I2
Transform Invariant

I3
Object Invariant

I4
Relational Invariant

I5
Compositional Invariant

I6
Cross-Task Invariant

Goal

Avoid treating all discovered patterns equally.

Deliverable
invariant_taxonomy.md

2E.3 Recurrence Benchmark
Purpose

Measure recurrence independently.

Metrics:

R1
Pattern Frequency

R2
Task Coverage

R3
Cross-Task Occurrence

R4
Support Distribution

Rule

Recurrence measured before validation.

Deliverable
recurrence_benchmark.md

2E.4 Candidate Generation Audit
Purpose

Audit invariant proposal generation.

Pipeline:

Successful Traces

↓

Patterns

↓

Candidates

↓

Validated Invariants


Metrics:

Patterns Generated

Candidates Generated

Candidate Yield

Yield Per Trace

Questions
Can the miner generate candidates?

Or is candidate count near zero?

Deliverable
candidate_generation_audit.md

2E.5 Support Threshold Audit

This is likely the most important section.

Purpose

Determine whether support rules kill discovery.

Audit:

S1
Current Threshold

S2
Relaxed Threshold

S3
Strict Threshold


Metrics:

Candidates Surviving

Invariant Count

Discovery Yield

Questions
Zero invariants because:

No recurrence?

or

Threshold too high?

Deliverable
support_threshold_audit.md

2E.6 Invariant Validation Audit
Purpose

Evaluate candidate quality.

Metrics:

V1
Consistency

V2
Generality

V3
Survival Rate

V4
False Discovery Rate

Rule

Validation separate from recurrence.

Deliverable
invariant_validation_audit.md

2E.7 Discovery Yield Benchmark
Purpose

Measure overall productivity.

Metrics:

Trace → Candidate Yield

Candidate → Invariant Yield

Invariant Yield Per Task

Invariant Yield Per Trace

Goal

Locate bottlenecks quantitatively.

Deliverable
discovery_yield_report.md

2E.8 Failure Localization
Purpose

Identify root causes.

Possible outcomes:

F1
Trace Scarcity Bottleneck

F2
Recurrence Bottleneck

F3
Candidate Generation Bottleneck

F4
Support Threshold Bottleneck

F5
Validation Bottleneck

F6
Mixed

F7
Unresolved

Rule

No automatic blame assignment.

Deliverable
invariant_failure_localization.md

2E.9 Reporting Framework

Every ARC run must report:

Successful Traces

Patterns Generated

Candidates Generated

Candidate Yield

Support Distribution

Validated Invariants

Invariant Survival Rate


Separately from:

Coverage

Transfer

Capabilities

Accuracy

Deliverable
invariant_reporting_standard.md

2E.10 Readiness Review
Questions
Q1
Invariant taxonomy frozen?

Q2
Recurrence measurable?

Q3
Candidate generation measurable?

Q4
Support thresholds auditable?

Q5
Validation measurable?

Q6
Discovery yield measurable?

Q7
Failure localization possible?

Phase 2E Readiness Gates
Gate I1
Invariant taxonomy frozen.

Gate I2
Recurrence benchmark defined.

Gate I3
Candidate-generation audit defined.

Gate I4
Support-threshold audit defined.

Gate I5
Validation audit defined.

Gate I6
Discovery-yield benchmark defined.

Gate I7
Failure localization operational.

Deliverables
historical_invariant_audit.md

invariant_taxonomy.md

recurrence_benchmark.md

candidate_generation_audit.md

support_threshold_audit.md

invariant_validation_audit.md

discovery_yield_report.md

invariant_failure_localization.md

invariant_reporting_standard.md

phase2E_readiness_review.md

Phase 2E Exit Decision
PASS

Only if:

Recurrence measurable

Candidates measurable

Support thresholds auditable

Validation measurable

Yield measurable

Failure localization possible

FAIL

If:

Invariant discovery remains a black box

Support effects unknown

Validation undefined

Failure source unclear

Most Important Outcome

The single most important question Phase 2E should answer is:

"When ARC produces zero invariants, is that because meaningful invariants do not exist, because the trace supply is too weak, because support thresholds are too strict, or because the invariant-discovery mechanism itself is ineffective?"

Phase 13G could not distinguish those explanations.

Phase 2E should make them separable and measurable.