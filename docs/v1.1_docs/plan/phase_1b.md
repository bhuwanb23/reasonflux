Excellent. If Phase 1A identified why the old benchmarks failed, then Phase 1B is the first benchmark we actually redesign.

This phase directly attacks the single biggest SCT criticism from v1.0:

No selection pressure existed.

↓

SCT could not demonstrate value.


Phase 1B must ensure that can never happen again.

ASFT v1.1
Phase 1B — Selection Pressure Benchmark Specification

Phase ID

ASFT-V1.1-PHASE-1B


Package

ASFT-V1.1-PHASE-1B-SELECTION-PRESSURE-SPEC-V1


Primary Research Question

RQ2

Does SCV select candidates with higher future value
than simpler selection methods when genuine choice
pressure exists?

Phase Goal

Create a benchmark where:

Good candidates exist

Bad candidates exist

Neutral candidates exist


and where:

Selection decisions differ.

Why This Phase Exists

v1.0 result:

44/44 selected

↓

SCT
=
Always Create
=
Random Create


This means:

No meaningful selection test occurred.


Phase 1B exists specifically to prevent this.

Success Condition

At the end of Phase 1B we should have:

A benchmark where different selectors
make measurably different decisions.

Phase Structure
1B.1 Selection Failure Audit

1B.2 Candidate Taxonomy

1B.3 Value Definition

1B.4 Pressure Design

1B.5 Selector Competition Design

1B.6 Baseline Design

1B.7 Evaluation Metrics

1B.8 Dataset & Split Design

1B.9 Preregistration Framework

1B.10 Readiness Review

1B.1 Selection Failure Audit
Purpose

Understand exactly why v1.0 failed.

Inputs
Phase 13C

Phase 13F

Phase 14C

Phase 14F

Questions
Why were all candidates selected?

Why did SCV not matter?

Why did random tie SCT?

What pressure was missing?

Deliverable
selection_failure_audit.md

Exit Criteria
Every v1.0 selection failure mapped.

1B.2 Candidate Taxonomy
Purpose

Define candidate types.

Every candidate must belong to:

Type A
Positive Value


Expected future benefit exceeds cost.

Type B
Neutral Value


Approximately break-even.

Type C
Negative Value


Future value less than maintenance cost.

Type D
Deceptive Value


Looks useful initially.

Becomes harmful later.

Type E
Rare High-Impact


Low frequency.

High future value.

Goal

Create candidate diversity.

Exit Criteria
Taxonomy frozen.

1B.3 Value Definition
Purpose

Define what "good" means.

Must define:

Creation cost

Maintenance cost

Reuse value

Transfer value

Future utility

Rule

Value cannot be defined using:

SCV itself.


Otherwise:

Circular evaluation.

Deliverable
candidate_value_definition.md

1B.4 Pressure Design
Purpose

Guarantee real decisions.

Mandatory Rule

Every evaluation batch must contain:

Positive candidates

Neutral candidates

Negative candidates

Mandatory Rule

Selection rate must not be:

100%

or

0%

Mandatory Rule

Selectors must disagree.

Required Pressure Score

Define:

Selection Divergence Rate


Example:

SCV selects

Frequency rejects


counts as divergence.

Exit Criteria
Meaningful divergence guaranteed.

1B.5 Selector Competition Design
Purpose

Define competitors.

Required Selectors
S1
SCV

S2
Frequency

S3
Reuse Probability

S4
Random

S5
Always Create

S6
Never Create

S7
Oracle


Used only for analysis.

Not a production baseline.

Exit Criteria
Selectors frozen.

1B.6 Baseline Design
Purpose

Ensure fair comparison.

Rules

All selectors receive:

Same candidates

Same information

Same budget

Same evaluation horizon

Forbidden
Different candidate pools

Different opportunities

Deliverable
baseline_fairness_protocol.md

1B.7 Evaluation Metrics
Primary Endpoint

Must be frozen before experiments.

Candidate examples:

Future Net Value

Future Utility

Future Transfer Benefit

Secondary Endpoints
Precision

Recall

False Positive Rate

False Negative Rate

Maintenance Cost

Skill Survival

Diagnostic Metrics
Selection Rate

Divergence Rate

Value Distribution

Exit Criteria
Endpoints frozen.

1B.8 Dataset & Split Design
Purpose

Prevent leakage.

Required Splits
Calibration

Development

Confirmatory

Replication

Rule

Confirmatory split remains untouched.

Rule

Replication split remains untouched.

Deliverable
selection_dataset_protocol.md

1B.9 Preregistration Framework
Purpose

Prevent v1.0-style ambiguity.

Must freeze:

Primary endpoint

Comparator set

Independent unit

Sample size rationale

SOI

Decision rules

Missing-data policy

Required Outcomes
Supported

Contradicted

Inconclusive

Unavailable

Exit Criteria
Preregistration template frozen.

1B.10 Readiness Review
Checklist
Candidate Taxonomy
✅

Value Definition
✅

Pressure Design
✅

Selectors
✅

Baselines
✅

Metrics
✅

Dataset Design
✅

Preregistration
✅

Deliverables
selection_failure_audit.md

candidate_taxonomy.md

candidate_value_definition.md

selection_pressure_design.md

selector_competition_spec.md

baseline_fairness_protocol.md

selection_metrics.md

selection_dataset_protocol.md

selection_preregistration_template.md

phase1B_readiness_report.md

Phase 1B Exit Decision

PASS only if:

Selectors are forced to disagree

Good and bad candidates exist

Selection pressure is measurable

Evaluation is non-circular

Baselines are fair

Replication is planned

Primary endpoint is frozen

Most Important Output

If Phase 1B succeeds, then for the first time in ASFT history we can answer a meaningful scientific question:

"When presented with both good and bad skill candidates, does SCV actually make better creation decisions than simpler alternatives?"

That question was never truly tested in v1.0. Phase 1B exists to make sure v1.1 can answer it decisively.