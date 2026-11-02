Excellent. After Phase 2A (Representation Audit), the next logical step is:

ASFT v1.1 Phase 2B
ARC Coverage Benchmark

Phase ID

ASFT-V1.1-PHASE-2B


Package

ASFT-V1.1-PHASE-2B-ARC-COVERAGE-BENCHMARK-V1

Why Phase 2B Exists

Phase 13G and Phase 14G taught us:

Coverage

≠

Accuracy


and

No coverage

↓

No traces

↓

No invariants

↓

No skills

↓

No transfer


The biggest mistake we could make is jumping directly to:

Can ASFT solve ARC?


before answering:

Can ASFT even represent enough ARC
to activate the mechanism chain?


Phase 2B exists to answer that question.

Core Research Questions
R2B-1
How much ARC is representable
under the current representation?

R2B-2
How much ARC is discoverable
under the current search budget?

R2B-3
What percentage of ARC tasks
reach each stage of the chain?

R2B-4
Where does the activation pipeline fail?

Phase Structure
2B.1 Historical Coverage Audit

2B.2 Coverage Definition

2B.3 Coverage Measurement Framework

2B.4 Budgeted Coverage Benchmark

2B.5 Full-Scan Coverage Benchmark

2B.6 Trace Yield Benchmark

2B.7 Coverage Failure Localization

2B.8 Coverage Reporting Framework

2B.9 Readiness Review

2B.1 Historical Coverage Audit
Purpose

Audit exactly what happened in 13G.

Required Findings

Examples:

Tasks evaluated

Successful traces

Coverage %

DSL fit rates

Search budgets

Questions
What was measured?

What was not measured?

Which denominators were used?

Deliverable
historical_coverage_audit.md

2B.2 Coverage Definition

This is the most important conceptual section.

Purpose

Freeze what coverage means.

Coverage

Must mean:

Task representable under
representation + search budget.

Not Coverage
Correct test answer

Transfer success

Capability formation

Task accuracy

Rule

Coverage must remain independent from:

Accuracy

Deliverable
coverage_definition.md

2B.3 Coverage Measurement Framework
Purpose

Define measurable coverage stages.

For every ARC task record:

C1
Representable

C2
Trace Generated

C3
Successful Trace

C4
Invariant Candidate Available

C5
Skill Candidate Available

C6
Transfer Eligible

C7
Capability Eligible

Rule

Each stage measured separately.

Deliverable
coverage_stage_framework.csv

2B.4 Budgeted Coverage Benchmark
Purpose

Measure realistic coverage.

Uses:

Frozen search budget

Frozen representation

Frozen runtime limits


Outputs:

Coverage %

Trace Rate

Successful Trace Rate

Rule

Must use production budget.

Deliverable
budgeted_coverage_report.md

2B.5 Full-Scan Coverage Benchmark
Purpose

Measure theoretical coverage ceiling.

Allows:

Expanded search

Expanded runtime

Diagnostic mode


Not used for:

Performance claims.


Used for:

Coverage diagnosis.

Deliverable
fullscan_coverage_report.md

2B.6 Trace Yield Benchmark
Purpose

Measure trace generation independently.

Metrics:

Valid traces

Successful traces

Trace diversity

Trace density


Questions:

Representation issue?

Or search issue?

Deliverable
trace_yield_report.md

2B.7 Coverage Failure Localization
Purpose

Identify failure location.

Possible outcomes:

F1
Representation bottleneck

F2
Search bottleneck

F3
Support-threshold bottleneck

F4
Invariant bottleneck

F5
Mixed

F6
Unresolved

Rule

No automatic attribution.

Deliverable
coverage_failure_localization.md

2B.8 Coverage Reporting Framework
Purpose

Standardize outputs.

Every run must report:

Tasks

Coverage %

Trace %

Successful Trace %

Invariant %

Skill %

Transfer Eligibility %

Capability Eligibility %


And separately:

Accuracy

Rule

Coverage and accuracy may never be merged.

Deliverable
coverage_reporting_standard.md

2B.9 Readiness Review
Questions
Q1
Coverage definition frozen?

Q2
Coverage measurable independently?

Q3
Budgeted coverage benchmark defined?

Q4
Full-scan benchmark defined?

Q5
Failure localization possible?

Q6
Coverage separated from accuracy?

Phase 2B Readiness Gates
Gate C1
Coverage definition frozen.

Gate C2
Coverage stages measurable.

Gate C3
Budgeted benchmark defined.

Gate C4
Full-scan benchmark defined.

Gate C5
Trace yield measurable.

Gate C6
Failure localization operational.

Gate C7
Coverage and accuracy separated.

Deliverables
historical_coverage_audit.md

coverage_definition.md

coverage_stage_framework.csv

budgeted_coverage_report.md

fullscan_coverage_report.md

trace_yield_report.md

coverage_failure_localization.md

coverage_reporting_standard.md

phase2B_readiness_review.md

Phase 2B Exit Decision
PASS

Only if:

Coverage measurable

Coverage stages measurable

Budgeted coverage defined

Full-scan coverage defined

Trace yield measurable

Failure localization possible

Coverage separated from accuracy

FAIL

If:

Coverage still inferred from accuracy

Trace generation not measured

Failure localization impossible

Coverage stages collapsed together

Most Important Outcome

The most important result of Phase 2B is not:

Higher coverage.


It is:

Knowing exactly how much ARC
reaches each stage of the ASFT chain.


Because after Phase 13G, the key unresolved question is not:

Can ASFT solve ARC?


It is:

How far into the pipeline does ARC
actually get before failing?


Phase 2B should make that answer measurable.