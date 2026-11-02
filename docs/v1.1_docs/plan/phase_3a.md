Excellent. Phase 3A is the most important implementation phase in the entire IDT revalidation program.

If Phase 1C answered:

Can we design a valid ranking benchmark?


then Phase 3A answers:

Does the actual implementation faithfully execute
the benchmark we designed?


Historically, Phase 13B failed partly because:

Rankers did not meaningfully diverge.


Phase 3A must ensure we never accidentally recreate that situation.

ASFT v1.1 Phase 3A
IDT Implementation Readiness

Phase ID

ASFT-V1.1-PHASE-3A


Package

ASFT-V1.1-PHASE-3A-IDT-IMPLEMENTATION-READINESS-V1


Objective

Implement and validate the complete Phase 1C benchmark before any confirmatory outcomes are visible.

Phase 3A Structure
3A.1 Historical Benchmark Audit

3A.2 Ranker Implementation Validation

3A.3 Candidate Pool Validation

3A.4 Ranking Pressure Validation

3A.5 Endpoint Validation

3A.6 Leakage & Isolation Audit

3A.7 Fairness Audit

3A.8 Contract Revalidation

3A.9 Readiness Review

3A.1 Historical Benchmark Audit
Purpose

Freeze exactly what Phase 13B and Phase 1C taught us.

Required Findings
H1
13B ranking tie preserved

H2
No ranking superiority demonstrated

H3
Pressure absence identified

H4
Phase 1C benchmark requirements frozen

Deliverable
historical_idt_audit.md

3A.2 Ranker Implementation Validation
Purpose

Verify all rankers are implemented exactly as specified.

Required Rankers
R1
Transfer-Aware IDT


Current operational score.

R2
Frequency Only

R3
Reuse Probability

R4
Compression

R5
Random

R6
Oracle


Analysis only.

Validation Tests
RV1
Deterministic replay

RV2
Tie-break audit

RV3
Seed stability

RV4
Feature allowlist

RV5
No hidden fields

Deliverable
ranker_validation_report.md

3A.3 Candidate Pool Validation
Purpose

Validate benchmark inputs.

Required Properties
CP1
N = 40


(or frozen value)

CP2
Candidate diversity

CP3
Opaque IDs

CP4
Randomized arrival order

CP5
No label leakage

Deliverable
candidate_pool_validation.md

3A.4 Ranking Pressure Validation

This is the most important section.

Purpose

Demonstrate actual ranking disagreement.

Metrics
P1
TopK-RDR

P2
Normalized Kendall Divergence

P3
Pairwise Rank Divergence Matrix

P4
Top-K Overlap

Required Conditions

R1 must differ from:

Frequency

Reuse

Compression

Random

Failure Condition
Rankers converge


or

Pressure below threshold

Deliverable
ranking_pressure_validation.md

3A.5 Endpoint Validation
Purpose

Validate independent outcome measurement.

Primary Endpoint
FNTU@K


Future Net Transfer Utility.

Validation Tests
EV1
Independent of rank score

EV2
Independent of IDT formula

EV3
Frozen cost model

EV4
Paired baseline computation

Deliverable
endpoint_validation_report.md

3A.6 Leakage & Isolation Audit
Purpose

Prevent hidden outcome access.

Tests
L1
No future value fields

L2
No latent labels

L3
No task-family leakage

L4
No outcome access

L5
Oracle isolation

Deliverable
leakage_audit.md

3A.7 Fairness Audit
Purpose

Verify comparator fairness.

Requirements
F1
Same candidate pool

F2
Same budget

F3
Same horizon

F4
Same evaluator

F5
Same information visibility

Deliverable
fairness_audit.md

3A.8 Contract Revalidation
Purpose

Re-run the Phase 1C contract suite on the real implementation.

Required
26/26 contracts pass


(or updated count if expanded)

Categories
Rankers

Pressure

Leakage

Fairness

Endpoint

Outcome Logic

Deliverable
contract_revalidation_report.md

3A.9 Readiness Review
Required Questions
Q1
All rankers implemented?

Q2
Pressure present?

Q3
Endpoint independent?

Q4
Leakage absent?

Q5
Fairness verified?

Q6
Contracts pass?

Q7
Ready for calibration freeze?

Phase 3A Readiness Gates
Gate 3A-1
Rankers implemented.

Gate 3A-2
Candidate pool validated.

Gate 3A-3
Pressure validated.

Gate 3A-4
Endpoint validated.

Gate 3A-5
Leakage audit passed.

Gate 3A-6
Fairness audit passed.

Gate 3A-7
Contract suite passed.

Gate 3A-8
Outcome store sealed.

Outcome States

Phase 3A may conclude:

READY
All gates pass.

PARTIAL
Implementation exists
but critical gates remain open.

BLOCKED
Pressure absent

or

Leakage present

or

Endpoint invalid.

Deliverables
historical_idt_audit.md

ranker_validation_report.md

candidate_pool_validation.md

ranking_pressure_validation.md

endpoint_validation_report.md

leakage_audit.md

fairness_audit.md

contract_revalidation_report.md

phase3A_readiness_review.md

Most Important Question

The single most important question Phase 3A must answer is:

"If IDT wins or loses later, can we trust that the benchmark implementation actually created meaningful ranking pressure and measured future value independently?"

If the answer is not clearly yes, then Phase 3B and Phase 3D should remain blocked.

Under the brutal-honesty standard, Phase 3A succeeds even if IDT ultimately loses, because its purpose is not to help IDT win. Its purpose is to ensure that any future win, tie, or loss is scientifically interpretable.