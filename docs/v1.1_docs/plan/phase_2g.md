Excellent. Phase 2G should not create new science.

Its purpose is to answer one brutally important question:

"After Phases 2A–2F, are we actually ready to run meaningful ARC experiments?"

Phase 13G failed partly because the foundation was weak. Phase 2G is the final gate designed to prevent repeating that mistake.

ASFT v1.1 Phase 2G
ARC Foundation Readiness Review

Phase ID

ASFT-V1.1-PHASE-2G


Package

ASFT-V1.1-PHASE-2G-ARC-FOUNDATION-READINESS-V1

Phase Objective

Integrate findings from:

2A Representation Audit

2B Coverage Benchmark

2C Search & Budget Audit

2D Trace Generation Audit

2E Invariant Discovery Audit

2F Representation Alternatives


and determine whether:

ARC mechanism testing

should proceed

or

remain blocked.

Core Research Questions
R2G-1
Can ARC coverage be measured reliably?

R2G-2
Can search and representation
be separated?

R2G-3
Can trace generation be measured?

R2G-4
Can invariant discovery be measured?

R2G-5
Can ARC failures now be localized?

R2G-6
Is ARC ready for mechanism-level testing?

Phase Structure
2G.1 Foundation Evidence Review

2G.2 Readiness Matrix

2G.3 Risk Assessment

2G.4 Protocol Integrity Review

2G.5 ARC Mechanism Test Readiness

2G.6 Representation Hypothesis Assessment

2G.7 Phase 2 Exit Decision

2G.8 Readiness Report

2G.1 Foundation Evidence Review
Purpose

Summarize all findings from 2A–2F.

Required sections:

Representation
Documented?

Coverage mapped?

Missing concepts known?

Coverage
Measurable?

Separated from accuracy?

Search
Budget integrity?

Runtime integrity?

Traces
Yield measurable?

Diversity measurable?

Invariants
Candidate generation measurable?

Validation measurable?

Alternatives
Representation comparison possible?

Deliverable
foundation_evidence_review.md

2G.2 Readiness Matrix
Purpose

Create a single readiness dashboard.

Example:

Area	StatusRepresentation Audit	PASS
Coverage Benchmark	PASS
Search Audit	PASS
Trace Audit	PASS
Invariant Audit	PASS
Alternative Representation	PASS/PENDING

Possible statuses:

PASS

PARTIAL

BLOCKED

UNAVAILABLE

Deliverable
arc_readiness_matrix.csv

2G.3 Risk Assessment
Purpose

Identify remaining risks.

Categories:

R1
Representation Risk

R2
Search Risk

R3
Coverage Risk

R4
Trace Risk

R5
Invariant Risk

R6
Protocol Risk

R7
Interpretation Risk


For each:

Low

Moderate

High

Critical

Deliverable
arc_risk_assessment.md

2G.4 Protocol Integrity Review
Purpose

Verify all known Phase 13G problems are addressed.

Checklist:

P1
Config/runtime parity

P2
Budget logging

P3
Holdout protection

P4
Outcome isolation

P5
Coverage reporting

P6
Failure reporting

P7
Version control

Deliverable
protocol_integrity_review.md

2G.5 ARC Mechanism Test Readiness

This is the most important section.

Purpose

Determine readiness for:

Invariant testing

Skill testing

Transfer testing

Capability testing


Questions:

Q1
Can invariants exist?

Q2
Can skills form?

Q3
Can transfer be measured?

Q4
Can capability eligibility be measured?


Possible outcomes:

READY

PARTIAL

BLOCKED

Deliverable
mechanism_test_readiness.md

2G.6 Representation Hypothesis Assessment
Purpose

Assess current evidence.

Possible outcomes:

H1
Representation Dominant

H2
Representation Contributing

H3
Representation Weak

H4
Unresolved

Rule

No causal claim allowed.

Only evidence assessment.

Deliverable
representation_hypothesis_status.md

2G.7 Phase 2 Exit Decision
PASS

Only if:

Representation documented

Coverage measurable

Search auditable

Traces measurable

Invariant discovery measurable

Protocol integrity acceptable

Failure localization possible

PARTIAL

If:

Some diagnostics operational

but mechanism testing still blocked

FAIL

If:

Coverage unknown

Search unverified

Traces unmeasurable

Failure localization impossible

2G.8 Readiness Report
Required Final Statement
What Phase 2 Demonstrates

Examples:

✅

ARC diagnostics exist.


✅

Coverage measurable.


✅

Trace generation measurable.


✅

Invariant discovery measurable.


✅

Representation hypothesis testable.

What Phase 2 Does NOT Demonstrate

❌

ASFT works on ARC.


❌

Representation is the bottleneck.


❌

Skills emerge on ARC.


❌

Transfer emerges on ARC.


❌

Capability emerges on ARC.

Phase 2 Deliverables
foundation_evidence_review.md

arc_readiness_matrix.csv

arc_risk_assessment.md

protocol_integrity_review.md

mechanism_test_readiness.md

representation_hypothesis_status.md

phase2_exit_decision.md

phase2_readiness_report.md

Phase 2 Exit Criteria

A successful Phase 2 should allow the following statement:

"We now have sufficient diagnostic infrastructure to determine whether ARC failures arise from representation, search, trace generation, invariant discovery, or downstream mechanism activation, and future ARC experiments can be interpreted without conflating those stages."

Most Important Outcome

The most important outcome of Phase 2 is not:

Better ARC accuracy.


It is:

ARC failures become diagnosable.


Because Phase 13G produced a negative result that was scientifically difficult to localize.

If Phase 2 succeeds, then whether Phase 3 ARC experiments succeed or fail, you'll know where and why they succeeded or failed. That is the real foundation Phase 2 is supposed to build.