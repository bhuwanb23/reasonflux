Excellent. Phase 2D is where Phase 2 stops asking:

Can ARC be represented?


and starts asking:

Can ARC generate enough successful traces
to feed the entire ASFT mechanism chain?


This is a crucial distinction.

Phase 13G showed:

600 discovery tasks

↓

3 successful traces

↓

0 invariant candidates

↓

0 skills


At that point, the system never truly tested invariants, skills, transfer, or capability.

So Phase 2D exists to determine whether the problem is:

No traces

or

Bad traces

or

Too few traces

or

Trace-to-invariant failure

ASFT v1.1 Phase 2D
Trace Generation Audit

Phase ID

ASFT-V1.1-PHASE-2D


Package

ASFT-V1.1-PHASE-2D-TRACE-GENERATION-AUDIT-V1

Phase Objective

Audit the entire ARC trace-generation pipeline.

Determine:

How traces are generated

How often traces succeed

How trace diversity behaves

Whether traces are sufficient
for invariant discovery

Core Research Questions
R2D-1
How many traces are generated?

R2D-2
How many traces are valid?

R2D-3
How many traces are successful?

R2D-4
Are trace counts sufficient
for invariant discovery?

R2D-5
Are failures primarily caused by:

Representation

Search

Support thresholds

Trace quality

or downstream filtering?

Phase Structure
2D.1 Historical Trace Audit

2D.2 Trace Taxonomy

2D.3 Trace Lifecycle Audit

2D.4 Trace Yield Benchmark

2D.5 Trace Diversity Benchmark

2D.6 Trace Quality Benchmark

2D.7 Invariant Readiness Audit

2D.8 Failure Localization

2D.9 Reporting Framework

2D.10 Readiness Review

2D.1 Historical Trace Audit
Purpose

Reconstruct exactly what happened in Phase 13G.

Required Metrics
Tasks processed

Candidate programs generated

Valid traces

Successful traces

Trace success rate

Questions
How many traces existed?

How many solved demonstrations?

How many survived filtering?

Deliverable
historical_trace_audit.md

2D.2 Trace Taxonomy
Purpose

Define trace classes.

Every trace must be classified.

T1
Invalid Trace


Fails execution.

T2
Valid Trace


Executes successfully.

T3
Partial Trace


Explains part of behavior.

T4
Successful Trace


Matches demonstration.

T5
High-Support Trace


Appears repeatedly.

T6
Transfer-Relevant Trace


Potentially reusable.

Goal

Avoid treating all traces as identical.

Deliverable
trace_taxonomy.md

2D.3 Trace Lifecycle Audit
Purpose

Track trace attrition.

Trace flow:

Candidate

↓

Executable

↓

Valid

↓

Successful

↓

Invariant Candidate

↓

Skill Candidate

Required Metrics

At every stage:

Count

Drop Rate

Survival Rate

Deliverable
trace_lifecycle_report.md

2D.4 Trace Yield Benchmark
Purpose

Measure production rates.

Metrics:

Y1
Candidates Generated

Y2
Valid Traces

Y3
Successful Traces

Y4
Successful Trace Rate

Y5
Successful Traces per Task

Rule

Yield reported independently of:

Accuracy

Deliverable
trace_yield_report.md

2D.5 Trace Diversity Benchmark
Purpose

Measure variety.

Problem:

100 traces

≠

100 unique traces


Metrics:

D1
Unique Trace Count

D2
Structural Diversity

D3
Operation Diversity

D4
Template Diversity

Goal

Determine whether invariant discovery has enough variation.

Deliverable
trace_diversity_report.md

2D.6 Trace Quality Benchmark
Purpose

Evaluate usefulness.

Metrics:

Q1
Demonstration Fit

Q2
Consistency

Q3
Generality

Q4
Support

Q5
Reuse Potential

Rule

Quality metrics cannot use:

Invariant scores

Skill scores

Deliverable
trace_quality_report.md

2D.7 Invariant Readiness Audit

This is the most important section.

Purpose

Determine whether invariant discovery is even possible.

Questions:

Enough successful traces?

Enough diversity?

Enough support?

Enough recurrence?

Outcomes
I1
Ready

I2
Marginal

I3
Not Ready

Rule

Zero invariants can result from:

No traces


rather than:

Bad invariant miner.

Deliverable
invariant_readiness_audit.md

2D.8 Failure Localization
Purpose

Identify trace bottlenecks.

Possible outcomes:

F1
Representation Bottleneck

F2
Search Bottleneck

F3
Trace Yield Bottleneck

F4
Trace Diversity Bottleneck

F5
Support Threshold Bottleneck

F6
Mixed

F7
Unresolved

Rule

No automatic blame assignment.

Deliverable
trace_failure_localization.md

2D.9 Reporting Framework

Every ARC run must report:

Candidate Programs

Valid Traces

Successful Traces

Trace Success Rate

Trace Diversity

Trace Support

Invariant Readiness


Separately from:

Coverage

Transfer

Capability

Accuracy

Deliverable
trace_reporting_standard.md

2D.10 Readiness Review
Questions
Q1
Trace taxonomy complete?

Q2
Trace lifecycle measurable?

Q3
Yield measurable?

Q4
Diversity measurable?

Q5
Quality measurable?

Q6
Invariant readiness measurable?

Q7
Failure localization possible?

Phase 2D Readiness Gates
Gate T1
Trace taxonomy frozen.

Gate T2
Trace lifecycle measurable.

Gate T3
Yield benchmark defined.

Gate T4
Diversity benchmark defined.

Gate T5
Quality benchmark defined.

Gate T6
Invariant readiness defined.

Gate T7
Failure localization operational.

Deliverables
historical_trace_audit.md

trace_taxonomy.md

trace_lifecycle_report.md

trace_yield_report.md

trace_diversity_report.md

trace_quality_report.md

invariant_readiness_audit.md

trace_failure_localization.md

trace_reporting_standard.md

phase2D_readiness_review.md

Phase 2D Exit Decision
PASS

Only if:

Trace generation measurable

Trace quality measurable

Trace diversity measurable

Invariant readiness measurable

Failure localization possible

FAIL

If:

Trace counts unknown

Trace diversity unknown

Invariant readiness unknown

Failures cannot be localized

Most Important Outcome

The single most important question Phase 2D should answer is:

"If the invariant miner receives zero invariants, is that because the miner failed, or because the trace-generation system never supplied enough successful, diverse, high-support traces in the first place?"

Phase 13G could not answer that question.

Phase 2D should make it answerable.