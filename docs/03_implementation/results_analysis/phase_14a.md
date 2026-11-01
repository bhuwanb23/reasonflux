Phase 14A: Evidence Integrity Review
Purpose

Before analyzing results, we must answer a fundamental question:

Can we trust the evidence?

Phase 14A is not about whether ASFT succeeded or failed.

It is about whether the Phase 13 evidence is:

reproducible,
auditable,
frozen,
correctly interpreted,
and free from posthoc manipulation.

Only after passing Phase 14A can we trust any later conclusions.

14A-1 Review Scope

Evidence sources under review:

Phase 13A
Experimental Validation Setup

Phase 13B
IDT Experiments

Phase 13C
SCT Experiments

Phase 13D
Transfer Experiments

Phase 13E
Capability Growth Experiments

Phase 13F
Baselines & Ablations

Phase 13G
ARC Validation

Phase 13H
Evidence Consolidation

14A-2 Integrity Principles

All evidence must satisfy:

Principle 1

Frozen Criteria

Success criteria must be defined
before confirmatory execution.

Principle 2

Failed Gates Remain Failed

A failed experiment
cannot later be relabeled
as successful.

Principle 3

Exploratory ≠ Confirmatory

Stress tests

Posthoc analyses

Follow-up investigations


must never replace:

Predefined confirmation tests.

Principle 4

Negative Evidence Preserved

Failures must remain visible.

Principle 5

Traceability

Every claim must map to:

Claim
↓
Experiment
↓
Metric
↓
Evidence

14A-3 Audit of Phase 13A
Experimental Governance

Review:

Experiment Registry
Seed Policy
Dataset Policy
Metrics Registry
Reporting


Assessment:

✅ Registry exists

✅ Seed policy documented

✅ Metrics governed

✅ Reporting standardized

✅ Records stored

Finding
PASS

Limitation

Provenance still incomplete:

Git SHA

Environment Hash

Dirty Tree State


not universally preserved.

Severity
Low


Paper-quality issue.

Not evidence-invalidating.

14A-4 Audit of Phase 13B
IDT Integrity

Key question:

Were failed outcomes preserved?


Findings:

Original benchmark:

Transfer-aware
=
Frequency
=
No-transfer


remains unchanged.

Strict gate:

Failed


remains:

Failed


EXP-IDT-14:

explicitly labeled:

Exploratory


and not promoted to confirmation.

Assessment

✅ Strong integrity

Reviewer View

This is exactly how a failed hypothesis should be handled.

14A-5 Audit of Phase 13C
SCT Integrity

Question:

Were null results preserved?


Findings:

SCT:

0.345


Always Create:

0.345


Random:

0.345


Strict superiority:

Failed


remains:

Failed


Memory-only:

1.325


still reported.

Assessment

✅ Strong integrity

Reviewer View

No evidence of threshold tuning or posthoc reinterpretation.

14A-6 Audit of Phase 13D–13F
Transfer / CGM / Baselines

Question:

Were adverse findings retained?


Findings:

Negative CGR

Negative IE trend

Negative TS→CGR

Failed baselines

Null ablations

all preserved.

Assessment

✅ Strong integrity

Important Observation

Many projects remove:

Negative Transfer

Negative Growth

Failed Ablations


from final reports.

ReasonFlux preserved them.

14A-7 Audit of Phase 13G
ARC Integrity

Question:

Was ARC oversold?


Findings:

ARC results:

0 invariants

0 skills

0 capabilities

0.5% exact holdout


reported directly.

No attempt to reinterpret:

0 invariants


as:

weak invariants


or similar.

Assessment

✅ Strong integrity

Limitation

Holdout exposure issue disclosed.

Severity:

Medium


because it affects future external-validity claims.

14A-8 Claim–Evidence Traceability Audit

Review:

claim_evidence_matrix.csv


structure.

Assessment:

Every major claim mapped to:

Evidence

Metric

Experiment


Examples:

IDT-3
↓
13B
↓
Baseline Comparison
↓
Failed

SCT-2
↓
13C
↓
SCV Correlation
↓
Partial

Assessment

✅ Pass

14A-9 Exploratory vs Confirmatory Separation

One of the most important audits.

Confirmatory

Examples:

13B synthetic-v1

13C SCT

13D Transfer

13E CGM

Exploratory

Examples:

EXP-IDT-14

Posthoc analyses

Corrective diagnostics


Assessment:

Separation maintained.

Result

✅ Pass

14A-10 Evidence Contamination Review

Question:

Were later results used
to redefine earlier claims?


Findings:

No evidence of:

Threshold changes

Metric redefinitions

Success criterion changes

Dataset replacement


after results.

Assessment

✅ Pass

14A-11 Reproducibility Review

Review:

Records

Seeds

Configs

Reports

Artifacts


Assessment:

✅ Strong

Missing:

Git Commit Capture

Environment Snapshot


Classification:

Reproducible
with minor provenance gaps

14A-12 Evidence Risk Register
Risk EIR-01

Small synthetic populations.

Severity:

Medium

Risk EIR-02

Shared generator and solver vocabulary.

Severity:

High

Risk EIR-03

Low ARC DSL coverage.

Severity:

High

Risk EIR-04

Repeated ARC holdout exposure.

Severity:

Medium

Risk EIR-05

Metric interpretation drift.

Severity:

Medium

14A-13 Integrity Scorecard
Category	StatusFrozen protocols	✅
Failed gates preserved	✅
Exploratory separated	✅
Negative evidence preserved	✅
Claim traceability	✅
Baseline transparency	✅
Ablation transparency	✅
ARC transparency	✅
Reproducibility	✅ (minor gaps)
Provenance completeness	⚠
14A Conclusion
Main Question

Can the Phase 13 evidence be trusted for analysis?

Answer
Yes.


With limitations.

Formal Verdict
Evidence Integrity
PASS

Strongest Finding

The strongest outcome of Phase 14A is:

There is no evidence that failed hypotheses, failed baselines, failed ARC results, or adverse findings were hidden, reclassified, or replaced by exploratory results.

Weakest Area

The weakest area is not integrity.

It is external validity:

Synthetic dependence

ARC coverage

Representation limits


Those belong to later analysis phases.

Deliverables of Phase 14A

✅ Evidence Integrity Report

✅ Frozen-protocol audit

✅ Claim traceability audit

✅ Exploratory/confirmatory audit

✅ Reproducibility review

✅ Risk register

✅ Integrity scorecard

✅ Formal pass/fail verdict

Exit Decision
Phase 14A
✅ PASSED


The evidence base is sufficiently trustworthy to proceed to:

Phase 14B: Contribution 1 (IDT) Critical Results Analysis

where we stop asking:

Can we trust the evidence?


and start asking:

What does the evidence actually tell us about IDT?