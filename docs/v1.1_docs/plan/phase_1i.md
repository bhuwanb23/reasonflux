Perfect. Phase 1I is the final and most important governance phase of Phase 1.

Everything before Phase 1I creates:

Benchmarks

Baselines

Ablations

Validation criteria


Phase 1I answers:

"How do we ensure v1.1 experiments are scientifically trustworthy before a single confirmatory result is collected?"

In many ways, Phase 1I is the biggest methodological upgrade from v1.0.

ASFT v1.1
Phase 1I – Evaluation Protocol Specification

Phase ID

ASFT-V1.1-PHASE-1I


Package

ASFT-V1.1-PHASE-1I-EVALUATION-PROTOCOL-V1

Phase Objective

Create a frozen evaluation framework governing:

Experiment design

Preregistration

Data handling

Inference

Replication

Interpretation

Reporting


for every confirmatory v1.1 experiment.

Why This Phase Exists

Phase 14 identified recurring issues:

Low pressure benchmarks

Construct ambiguity

Metric interpretation drift

Different denominators

Unavailable vs zero confusion

Post-hoc explanations


Phase 1I exists to prevent those problems before they occur.

Core Principle

Every future result must be classifiable as:

Supported

Contradicted

Inconclusive

Unavailable


without changing rules after outcomes are observed.

Phase Structure
1I.1 Evaluation Audit

1I.2 Experiment Classification Framework

1I.3 Preregistration Standard

1I.4 Endpoint Framework

1I.5 Statistical Framework

1I.6 Replication Framework

1I.7 Interpretation Framework

1I.8 Reporting Framework

1I.9 Governance Rules

1I.10 Readiness Review

1I.1 Evaluation Audit
Purpose

Audit all evaluation problems found in v1.0.

Inputs
Phase 14A–14J

Questions
Which conclusions were strong?

Which were ambiguous?

Which depended on benchmark weaknesses?

Which suffered from construct issues?

Deliverable
evaluation_audit.md

Exit Criteria
All evaluation weaknesses documented.

1I.2 Experiment Classification Framework
Purpose

Classify every future experiment.

Every experiment must be labeled:

E1
Exploratory


Hypothesis generation.

E2
Development


Benchmark tuning.

E3
Confirmatory


Primary scientific test.

E4
Replication


Independent verification.

Rule

Only:

Confirmatory

Replication


may support primary claims.

1I.3 Preregistration Standard
Purpose

Freeze decisions before results.

Every confirmatory experiment must specify:

Research question

Primary hypothesis

Primary endpoint

Secondary endpoints

Comparators

Independent unit

Sample-size rationale

SOI

Missing-data policy

Decision rule

Forbidden
Changing endpoints

Changing thresholds

Changing splits

after outcome inspection

Deliverable
preregistration_template.md

1I.4 Endpoint Framework
Purpose

Standardize outcome definitions.

Each experiment must define:

Primary Endpoint

Single decision-driving metric.

Secondary Endpoints

Supporting evidence.

Diagnostic Metrics

Understanding mechanism behavior.

Rule

Only primary endpoint determines:

Pass

Fail

Inconclusive

Example

For SCT:

Primary:
Future Utility

Secondary:
Precision

Diagnostics:
Selection Rate

1I.5 Statistical Framework
Purpose

Prevent denominator confusion.

Independent Unit Rules

Must identify:

Seed

Task

Candidate

Capability

Agent


as applicable.

Rule

Rows nested within seeds:

≠ independent replications

Required Reporting
Effect estimate

Uncertainty interval

Independent unit count

Missing-data count

Rule

Exact ties and zero variance must be reported explicitly.

1I.6 Replication Framework
Purpose

Separate discovery from confirmation.

Replication Types
R1
Within-generator

R2
Cross-generator

R3
Cross-domain

R4
External benchmark

Rule

Generalization claims require replication.

Rule

Single positive result:

≠ generalized finding

1I.7 Interpretation Framework

This is one of the most important sections.

Frozen Interpretation Rules
Rule 1
Metric increase

≠

Theory validation

Rule 2
Tie

=

No demonstrated advantage

Rule 3
Unavailable

≠

Zero

Rule 4
Ablation effect

≠

Universal necessity

Rule 5
Synthetic success

≠

External validity

Rule 6
Correlation

≠

Causation

Rule 7
Capability score

≠

Capability growth


until Phase 7 validation.

Rule 8
IG

≠

Intelligence


until Phase 8 validation.

1I.8 Reporting Framework
Purpose

Standardize reporting.

Every experiment must report:

Research Question

Hypothesis

Primary Result

Secondary Results

Negative Results

Unavailable Results

Limitations

Interpretation

Mandatory

Null findings remain reported.

Forbidden

Selective reporting.

1I.9 Governance Rules
Purpose

Protect integrity.

G1
No changing frozen protocols.

G2
No relabeling failed gates.

G3
No hiding negative results.

G4
No converting exploratory findings
into confirmatory evidence.

G5
No treating unavailable as failure.

G6
All corrections tracked.

G7
Source lineage preserved.

1I.10 Readiness Review
Checklist
Evaluation Audit

✅

Experiment Classes

✅

Preregistration Standard

✅

Endpoint Framework

✅

Statistical Framework

✅

Replication Framework

✅

Interpretation Rules

✅

Reporting Rules

✅

Governance Rules

✅

Deliverables
evaluation_audit.md

experiment_classification_framework.md

preregistration_template.md

endpoint_framework.md

statistical_framework.md

replication_framework.md

interpretation_framework.md

reporting_framework.md

governance_rules.md

phase1I_readiness_report.md

Phase 1 Exit Package

At completion of:

1A
1B
1C
1D
1E
1F
1G
1H
1I


ASFT v1.1 will have:

Benchmark Suite v2

Selection Benchmark

Ranking Benchmark

Memory Challenge

Capability Validation

Intelligence Validation

ARC Generalization Benchmark

Baseline Framework

Ablation Framework

Evaluation Protocol


all frozen before any confirmatory v1.1 experiments begin.

Phase 1 Exit Decision
PASS


only if:

Benchmarks are frozen

Baselines are frozen

Ablations are frozen

Validation targets exist

Interpretation rules are frozen

Governance rules are frozen

Replication requirements are frozen

Most Important Outcome

The single most important deliverable of Phase 1I is:

A future ASFT v1.1 result should be interpretable without changing definitions, thresholds, benchmarks, baselines, or claims after the outcome is known.

That is the fundamental methodological lesson learned from the entire v1.0 → Phase 14 journey, and Phase 1I formally encodes it into the ASFT v1.1 research process.