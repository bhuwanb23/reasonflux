Excellent. Phase 3D is the first true scientific test of IDT in ASFT v1.1.

Everything before this point exists to ensure that whatever happens in Phase 3D:

Win

Tie

Loss

Unavailable


is interpretable.

Unlike Phase 3C:

Phase 3C
=
Does the benchmark work?


Phase 3D asks:

Does transfer-aware ranking produce
higher future value than simpler alternatives?


This is the first phase allowed to answer RQ1.

ASFT v1.1 Phase 3D
IDT Confirmatory Benchmark

Phase ID

ASFT-V1.1-PHASE-3D


Package

ASFT-V1.1-PHASE-3D-CONFIRMATORY-IDT-BENCHMARK-V1


Classification

E3 Confirmatory


Per Phase 1I:

This is the first phase allowed
to generate primary evidence.

Primary Research Question
RQ1:

Does transfer-aware ranking (IDT)
improve future value compared with
simpler ranking policies?

Scientific Objective

Determine whether:

Transfer-aware ranking

↓

Selects better candidates

↓

Produces higher future utility


than:

Frequency

Reuse

Compression

Random


under a pressure-valid benchmark.

Required Preconditions

Before execution:

Phase 3A
READY

Phase 3B
READY

Phase 3C
READY


must all be completed.

Phase Structure
3D.1 Confirmatory Activation

3D.2 Comparator Execution

3D.3 Pressure Verification

3D.4 Primary Endpoint Evaluation

3D.5 Secondary Endpoint Evaluation

3D.6 Robustness & Integrity Review

3D.7 Outcome Classification

3D.8 Confirmatory Report

3D.1 Confirmatory Activation
Purpose

Activate the frozen confirmatory benchmark.

Required Verification
A1
Confirmatory dataset hash

A2
Outcome store seal intact

A3
Frozen analysis hash

A4
Comparator versions match

A5
Preregistration unchanged

Failure

Any mismatch:

Unavailable

Deliverable
confirmatory_activation_report.md

3D.2 Comparator Execution
Purpose

Run all frozen comparators.

Required Comparators
R1
Transfer-Aware IDT

R2
Frequency

R3
Reuse

R4
Compression

R5
Random

R6
Oracle


Analysis-only.

Not eligible to win.

Deliverable
comparator_execution_report.md

3D.3 Pressure Verification

This must occur before interpretation.

Purpose

Confirm benchmark remained informative.

Metrics
P1
TopK-RDR

P2
Kendall Divergence

P3
Pairwise Divergence Matrix

Failure Condition
Pressure collapse


or:

Identical selections

Outcome
Non-Informative


if pressure fails.

Deliverable
pressure_verification_report.md

3D.4 Primary Endpoint Evaluation

This is the most important section.

Primary Endpoint
FNTU@K


(Future Net Transfer Utility)

Primary Comparison
IDT

vs

Frequency

Primary Estimator

Frozen in Phase 3B.

Required Reporting
E1
Effect estimate

E2
Confidence interval

E3
SOI comparison

E4
Independent-unit count

Deliverable
primary_endpoint_report.md

3D.5 Secondary Endpoint Evaluation
Purpose

Context only.

Cannot rescue failed primary.

Comparisons
S1
IDT vs Reuse

S2
IDT vs Compression

S3
IDT vs Random

Diagnostics

Examples:

Coverage

Selection overlap

Transfer utility

Deliverable
secondary_endpoint_report.md

3D.6 Robustness & Integrity Review
Purpose

Ensure result credibility.

Checks
R1
Missingness audit

R2
Leakage audit

R3
Comparator parity audit

R4
Outcome access audit

R5
Hash verification

Deliverable
integrity_review.md

3D.7 Outcome Classification

Per Phase 1I.

Supported

Requirements:

Primary endpoint exceeds SOI

and

Direction favorable

Contradicted

Requirements:

Comparator superior

or

Direction unfavorable

Tie

Requirements:

Equivalence region satisfied

Inconclusive

Requirements:

Precision insufficient

Unavailable

Requirements:

Protocol failure

Non-Informative

Requirements:

Pressure failure

Deliverable
outcome_classification.md

3D.8 Confirmatory Report
Required Sections
RQ
Frozen RQ1

Benchmark Status
Pressure

Fairness

Integrity

Primary Result
FNTU@K

Secondary Results

Frozen set only.

Outcome State
Supported

Contradicted

Tie

Inconclusive

Unavailable

Non-Informative

Limitations

Mandatory.

Interpretation

Frozen interpretation rules only.

Deliverable
phase3D_confirmatory_report.md

Phase 3D Readiness Gates
Gate 3D-1
Confirmatory split active.

Gate 3D-2
Outcome store unsealed correctly.

Gate 3D-3
Comparators executed.

Gate 3D-4
Pressure verified.

Gate 3D-5
Primary endpoint computed.

Gate 3D-6
Integrity audit passed.

Gate 3D-7
Outcome classified.

Possible Scientific Outcomes
V1
IDT Supported


Confirmatory benchmark positive.

V2
IDT Contradicted


Comparator superior.

V3
IDT Tie


No demonstrated advantage.

V4
IDT Inconclusive


Precision insufficient.

V5
IDT Unavailable


Protocol failure.

V6
IDT Non-Informative


Pressure failure.

What Phase 3D Must NOT Do

It must NOT conclude:

IDT validated forever.


because:

Replication still pending.


It must NOT conclude:

Transfer theory proven.


because:

This is one benchmark.


It must NOT use:

Secondary endpoints

or

Diagnostics


to rescue a failed primary endpoint.

Success Criteria For Phase 3D

A successful Phase 3D is not:

IDT wins.


A successful Phase 3D is:

The benchmark returns a trustworthy answer.


Possible trustworthy answers:

Supported

Contradicted

Tie

Inconclusive

Unavailable

Non-Informative


All six are scientifically acceptable outcomes.

Most Important Question

The single most important question Phase 3D must answer is:

"When evaluated under a pressure-valid, preregistered, independently scored benchmark, does transfer-aware ranking provide meaningful future utility beyond simpler ranking policies?"

That is the first real scientific test of IDT in ASFT v1.1. Phase 3E will then determine whether whatever answer Phase 3D produces can survive replication.