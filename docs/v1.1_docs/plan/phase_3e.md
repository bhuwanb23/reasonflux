Excellent. Phase 3E is where IDT either survives or fails.

Not Phase 3D.

Phase 3D can produce:

Positive result

Negative result

Tie


but a single confirmatory benchmark is still only one benchmark.

Phase 3E asks:

Does the Phase 3D result replicate under independently generated conditions?

Under the Phase 1I governance framework:

Generalization

≠

Single positive result


Therefore Phase 3E is mandatory before any strong claim about IDT.

ASFT v1.1 Phase 3E
IDT Replication Benchmark

Phase ID

ASFT-V1.1-PHASE-3E


Package

ASFT-V1.1-PHASE-3E-IDT-REPLICATION-BENCHMARK-V1


Classification

E4 Replication

Primary Objective

Determine whether the Phase 3D outcome:

Replicates

Partially Replicates

Fails to Replicate


under independent conditions.

Primary Research Question
RQ1-R:

Does the Phase 3D IDT result
recur in an independent benchmark population?

Fundamental Rule

Phase 3E is not:

Run Phase 3D again.


Instead:

New population

New candidate pools

New seeds

New family clusters


while preserving:

Same preregistered methodology.

Phase Structure
3E.1 Replication Activation

3E.2 Independence Verification

3E.3 Comparator Execution

3E.4 Replication Endpoint Evaluation

3E.5 Heterogeneity Analysis

3E.6 Replication Classification

3E.7 Generalization Assessment

3E.8 Final Replication Report

3E.1 Replication Activation
Purpose

Activate the frozen replication benchmark.

Required Checks
RA1
Replication split hash

RA2
Replication preregistration hash

RA3
Comparator version hashes

RA4
Analysis hash

RA5
Outcome store seal

Failure

Any mismatch:

Unavailable

Deliverable
replication_activation_report.md

3E.2 Independence Verification

This is the most important section.

Purpose

Demonstrate genuine independence from Phase 3D.

Required Independence
I1
Disjoint candidate pools

I2
Disjoint family clusters

I3
Disjoint seeds

I4
Disjoint outcome population

I5
No tuning using replication data

Failure

Any overlap beyond preregistered limits:

Replication invalid.

Deliverable
independence_verification.md

3E.3 Comparator Execution
Purpose

Run the same frozen comparators.

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


Analysis only.

Rule

No comparator changes.

No feature changes.

No parameter changes.

Deliverable
replication_execution_report.md

3E.4 Replication Endpoint Evaluation
Purpose

Evaluate the frozen primary endpoint.

Primary Endpoint
FNTU@K

Primary Comparison
R1 vs R2

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
replication_endpoint_report.md

3E.5 Heterogeneity Analysis
Purpose

Determine whether results vary materially.

Questions
H1
Effect direction stable?

H2
Magnitude stable?

H3
Family-specific variation?

H4
Candidate-pool variation?

Rule

Heterogeneity is descriptive.

Not a rescue mechanism.

Deliverable
heterogeneity_report.md

3E.6 Replication Classification
Purpose

Classify replication status.

R-REP-1
Replicated

Requirements:

Same direction

Same practical interpretation

Independent confirmation

R-REP-2
Partially Replicated

Requirements:

Direction consistent

Magnitude weaker

or

Precision lower

R-REP-3
Failed Replication

Requirements:

Direction reversed

or

No practical effect

R-REP-4
Inconclusive Replication

Requirements:

Precision insufficient

R-REP-5
Unavailable

Requirements:

Protocol failure

Deliverable
replication_classification.md

3E.7 Generalization Assessment
Purpose

Assess scope of inference.

Possible Conclusions
G1
Within-Population Generalization

G2
Cross-Population Generalization

G3
Cross-Generator Generalization

G4
Not Established

Rule

Generalization must be earned.

Never assumed.

Deliverable
generalization_assessment.md

3E.8 Final Replication Report
Required Sections
Phase 3D Summary

Frozen historical result.

Replication Result

Independent outcome.

Replication Classification

Replicated / Partial / Failed / Inconclusive / Unavailable.

Generalization Status

Explicitly bounded.

Limitations

Mandatory.

Interpretation

Frozen rules only.

Deliverable
phase3E_replication_report.md

Phase 3E Readiness Gates
Gate 3E-1
Replication split active.

Gate 3E-2
Independence verified.

Gate 3E-3
Comparators frozen.

Gate 3E-4
Primary endpoint evaluated.

Gate 3E-5
Heterogeneity analyzed.

Gate 3E-6
Replication classified.

Gate 3E-7
Generalization assessed.

Possible Outcomes
V1
Successful Replication

V2
Partial Replication

V3
Failed Replication

V4
Inconclusive Replication

V5
Unavailable

What Phase 3E Must NOT Do

It must NOT:

Change SOI

Change N

Change endpoint

Change comparator

Change analysis


after seeing Phase 3D.

It must NOT:

Explain away failed replication


using exploratory subgroup analyses.

It must NOT:

Use heterogeneity
to rescue failure.

Relationship To Phase 3F

Phase 3D answers:

What happened?


Phase 3E answers:

Did it happen again?


Phase 3F answers:

What is the final scientific verdict?

Success Criteria

A successful Phase 3E is not:

Replication succeeds.


A successful Phase 3E is:

Replication outcome is trustworthy.


Possible trustworthy outcomes:

Replicated

Partially Replicated

Failed Replication

Inconclusive

Unavailable


All are scientifically acceptable.

Most Important Question

The single most important question of Phase 3E is:

"If Phase 3D suggests that transfer-aware ranking is beneficial, does that conclusion survive exposure to a genuinely independent benchmark population?"

If the answer is:

Yes


then IDT becomes scientifically credible.

If the answer is:

No


then Phase 3F must report that honestly, regardless of how positive the original Phase 3D result was.