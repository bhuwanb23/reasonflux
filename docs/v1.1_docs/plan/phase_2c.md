Excellent. Phase 2C is where we audit one of the biggest technical credibility problems from Phase 13G:

Declared budget

≠

Executed budget


The infamous example being:

Config:
3 candidates

Runtime:
10 candidates


Even though Phase 14 correctly concluded this did not explain the entire ARC failure, it created uncertainty about what was actually evaluated.

So Phase 2C exists to answer:

"Can we trust that the search process being evaluated is the search process that was specified?"

ASFT v1.1 Phase 2C
Search & Budget Audit

Phase ID

ASFT-V1.1-PHASE-2C


Package

ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1

Objective

Create a complete audit framework for:

Search

Runtime budgets

Candidate generation

Trace generation

Evaluation integrity


and ensure:

Declared budget

=

Executed budget

=

Logged budget

Core Research Questions
R2C-1
Can search behavior be reproduced exactly?

R2C-2
Are declared and executed budgets identical?

R2C-3
How much ARC coverage loss is due to search?

R2C-4
Can search limitations be separated
from representation limitations?

Phase Structure
2C.1 Historical Search Audit

2C.2 Search Inventory

2C.3 Budget Registry

2C.4 Runtime Integrity Framework

2C.5 Search Trace Benchmark

2C.6 Budget Sensitivity Benchmark

2C.7 Search vs Representation Audit

2C.8 Search Reporting Standard

2C.9 Readiness Review

2C.1 Historical Search Audit
Purpose

Audit exactly what happened in Phase 13G.

Required Findings

Examples:

Declared budget

Runtime budget

Candidate count

Search depth

Trace count

Questions
What was configured?

What actually executed?

What was logged?

Deliverable
historical_search_audit.md

2C.2 Search Inventory
Purpose

Document all search mechanisms.

Inventory:

Candidate generation

Trace expansion

Ranking

Pruning

Selection

Termination


For every mechanism:

Input

Output

Budget consumption


must be documented.

Deliverable
search_inventory.csv

2C.3 Budget Registry

This is the most important section.

Purpose

Create one source of truth.

For every run:

B1
Candidate budget

B2
Search depth

B3
Trace budget

B4
Runtime budget

B5
Memory budget

B6
Evaluation budget

Rule

Each budget must exist in:

Config

Runtime

Logs


and match.

Deliverable
budget_registry.yaml

2C.4 Runtime Integrity Framework
Purpose

Prevent hidden divergence.

Required checks:

R1
Config hash

R2
Runtime hash

R3
Search log hash

R4
Budget audit record

Rule

Mismatch automatically triggers:

Protocol violation.

Deliverable
runtime_integrity_framework.md

2C.5 Search Trace Benchmark
Purpose

Measure search itself.

Metrics:

Candidates generated

Candidates evaluated

Valid traces

Successful traces

Pruned traces


Questions:

Was coverage limited by search?

Or by representation?

Deliverable
search_trace_report.md

2C.6 Budget Sensitivity Benchmark
Purpose

Measure response to increased search.

Conditions:

S1
Production budget

S2
2× budget

S3
5× budget

S4
Diagnostic unrestricted


Questions:

Coverage improves?

Trace count improves?

Invariant count improves?

Interpretation

If:

Coverage rises dramatically


then:

Search bottleneck plausible.


If:

Coverage remains flat


then:

Representation bottleneck strengthened.

Deliverable
budget_sensitivity_report.md

2C.7 Search vs Representation Audit
Purpose

Separate competing hypotheses.

H1
Representation bottleneck

H2
Search bottleneck

H3
Mixed bottleneck

H4
Unresolved

Rule

No automatic attribution.

Deliverable
search_representation_assessment.md

2C.8 Search Reporting Standard

Every future ARC run must report:

Configured budget

Executed budget

Logged budget

Trace count

Coverage

Successful traces

Invariant candidates


And separately:

Accuracy

Rule

Search metrics cannot be hidden.

Deliverable
search_reporting_standard.md

2C.9 Readiness Review
Questions
Q1
Search inventory complete?

Q2
Budget registry frozen?

Q3
Runtime integrity enforceable?

Q4
Search measurable?

Q5
Budget sensitivity measurable?

Q6
Search vs representation separable?

Phase 2C Readiness Gates
Gate S1
Search inventory complete.

Gate S2
Budget registry frozen.

Gate S3
Runtime integrity framework active.

Gate S4
Search trace benchmark defined.

Gate S5
Budget sensitivity benchmark defined.

Gate S6
Search vs representation audit defined.

Gate S7
Reporting standard frozen.

Deliverables
historical_search_audit.md

search_inventory.csv

budget_registry.yaml

runtime_integrity_framework.md

search_trace_report.md

budget_sensitivity_report.md

search_representation_assessment.md

search_reporting_standard.md

phase2C_readiness_review.md

Phase 2C Exit Decision
PASS

Only if:

Search fully documented

Budgets frozen

Runtime integrity enforceable

Sensitivity measurable

Search vs representation separable

FAIL

If:

Budget mismatch possible

Search behavior opaque

Sensitivity unknown

Representation and search conflated

Most Important Outcome

The most important result of Phase 2C is not:

More search.


It is:

Knowing whether more search
would actually matter.


Because one of the biggest unresolved ARC questions after Phase 13G is:

Did ARC fail because
we searched too little?

or

because the representation
could not express the solution?


Phase 2C should make that question experimentally answerable.