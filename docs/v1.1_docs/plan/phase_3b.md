Excellent. Phase 3B is the firewall between development and science.

If Phase 3A asks:

Did we build the benchmark correctly?


then Phase 3B asks:

Have we frozen enough of the benchmark
that future results can be trusted?


Historically, many of the Phase 14 criticisms ultimately reduce to:

Too much flexibility remained
after outcomes were known.


Phase 3B exists to eliminate that flexibility.

ASFT v1.1 Phase 3B
Calibration & Freeze

Phase ID

ASFT-V1.1-PHASE-3B


Package

ASFT-V1.1-PHASE-3B-CALIBRATION-AND-FREEZE-V1


Objective

Freeze all critical scientific decisions before confirmatory outcome access.

Phase 3B Structure
3B.1 Historical Calibration Audit

3B.2 Calibration Dataset Lock

3B.3 Sample Size Freeze

3B.4 Endpoint Freeze

3B.5 Comparator Freeze

3B.6 Analysis Freeze

3B.7 Replication Freeze

3B.8 Outcome-Seal Verification

3B.9 Final Preregistration Review

3B.1 Historical Calibration Audit
Purpose

Identify every place where post-hoc flexibility existed historically.

Audit Topics
H1
Ranking corrections

H2
Comparator interpretation drift

H3
Metric reinterpretation

H4
Construct-validity revisions

Deliverable
historical_calibration_audit.md

3B.2 Calibration Dataset Lock
Purpose

Separate:

Calibration

Development

Confirmatory

Replication


completely.

Required Splits
C1
Calibration


Allowed:

Variance estimation

Power estimation

Threshold tuning

C2
Development


Allowed:

Implementation debugging

C3
Confirmatory


Locked.

C4
Replication


Locked.

Rule
No overlap.

Deliverable
dataset_lock_report.md

3B.3 Sample Size Freeze
Purpose

Freeze N before outcomes.

Required
S1
Independent unit defined.


Example:

Panel

Family Seed

Cluster

S2
Power simulation.

S3
Precision target.

S4
Final N frozen.

Rule
N cannot change after outcomes.

Deliverable
sample_size_freeze.md

3B.4 Endpoint Freeze
Purpose

Freeze exactly what determines success.

Primary Endpoint
FNTU@K

Secondary Endpoints

Examples:

Coverage

Transfer utility

Candidate yield

Diagnostic Endpoints

Examples:

Pressure metrics

Rank divergence

Rule
Secondary endpoints
cannot rescue
a failed primary endpoint.

Deliverable
endpoint_freeze.md

3B.5 Comparator Freeze
Purpose

Prevent comparator switching.

Freeze
R1
Transfer-Aware

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

Required
Version hashes

Feature definitions

Tie-break rules

Deliverable
comparator_freeze.md

3B.6 Analysis Freeze

This is the most important section.

Purpose

Freeze the entire statistical analysis.

Freeze
A1
Primary estimator

A2
Uncertainty intervals

A3
Multiplicity corrections

A4
Missingness rules

A5
Equivalence rules

A6
SOI

Outcome States

Must remain:

Supported

Contradicted

Tie

Inconclusive

Unavailable

Non-Informative

Deliverable
analysis_freeze.md

3B.7 Replication Freeze
Purpose

Freeze replication before confirmation.

Required
R1
Replication population

R2
Replication criteria

R3
Success criteria

R4
Failure criteria

Deliverable
replication_freeze.md

3B.8 Outcome-Seal Verification
Purpose

Verify no confirmatory outcomes are visible.

Required
O1
Outcome store sealed

O2
Access log active

O3
Hash recorded

O4
No premature access

Failure

Any outcome access:

Confirmatory status invalid.

Deliverable
outcome_seal_verification.md

3B.9 Final Preregistration Review
Purpose

Produce the final frozen package.

Must Include
RQ

Hypotheses

Comparators

N

SOI

Endpoints

Analysis

Replication

Hashes

Outcome
READY
All freezes complete.

PARTIAL
Some freezes incomplete.

BLOCKED
Outcome access

or

major freeze missing.

Deliverable
phase3B_preregistration.md

Phase 3B Readiness Gates
Gate 3B-1
Calibration split locked.

Gate 3B-2
Development split locked.

Gate 3B-3
Confirmatory split locked.

Gate 3B-4
Replication split locked.

Gate 3B-5
Sample size frozen.

Gate 3B-6
Endpoints frozen.

Gate 3B-7
Comparators frozen.

Gate 3B-8
Analysis frozen.

Gate 3B-9
Outcome store sealed.

Gate 3B-10
Replication plan frozen.

Deliverables
historical_calibration_audit.md

dataset_lock_report.md

sample_size_freeze.md

endpoint_freeze.md

comparator_freeze.md

analysis_freeze.md

replication_freeze.md

outcome_seal_verification.md

phase3B_preregistration.md

phase3B_readiness_review.md

Exit Criteria
PASS

Only if:

Splits frozen

N frozen

Endpoints frozen

Comparators frozen

Analysis frozen

Replication frozen

Outcome store sealed

PARTIAL

If:

Implementation complete

but preregistration incomplete.

FAIL

If:

Outcome access occurred

or

critical freezes missing.

Most Important Question

The single most important question of Phase 3B is:

"If IDT wins, loses, or ties in Phase 3D, can anyone reasonably argue that the result depended on choices made after seeing the outcomes?"

If the answer is:

No


then Phase 3B succeeded.

Under the brutal-honesty standard, Phase 3B is successful even if it produces zero scientific findings, because its purpose is not discovery. Its purpose is to make the eventual discovery trustworthy.