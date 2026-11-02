Perfect. If Phase 1B fixes SCT's selection problem, then Phase 1C fixes IDT's ranking problem.

This phase exists because the single most important finding from v1.0 IDT was:

Transfer-aware Ranking
=
Frequency Ranking
=
No-Transfer Ranking


Not because IDT was proven wrong.

But because the benchmark never forced them to disagree.

Phase 1C must ensure:

If transfer-aware ranking has value, it gets a chance to show it.

If it doesn't, it fails fairly.

ASFT v1.1
Phase 1C – Ranking Pressure Benchmark Specification

Phase ID

ASFT-V1.1-PHASE-1C


Package

ASFT-V1.1-PHASE-1C-RANKING-PRESSURE-SPEC-V1

Primary Research Question
RQ1

Does transfer-aware ranking improve
future utility relative to frequency-only,
reuse-only, compression-oriented,
and random ranking methods when
meaningful ranking disagreement exists?

Why This Phase Exists
v1.0 Failure

Phase 13B demonstrated:

Transfer-Aware
=
Frequency
=
No-Transfer


on the primary benchmark.

Phase 14 showed:

No ranking pressure existed.


Meaning:

The benchmark could not identify
whether transfer-aware ranking
was useful.

Phase Goal

Construct a benchmark where:

Multiple candidate structures exist

Different rankers disagree

Ranking choices matter

Future value differs

Success Condition

At completion:

Different rankers produce
meaningfully different rankings.

Phase Structure
1C.1 Ranking Failure Audit

1C.2 Ranking Candidate Taxonomy

1C.3 Future Value Definition

1C.4 Ranking Pressure Design

1C.5 Ranker Competition Framework

1C.6 Transfer Ground Truth Design

1C.7 Evaluation Metrics

1C.8 Dataset & Split Design

1C.9 Preregistration Framework

1C.10 Readiness Review

1C.1 Ranking Failure Audit
Purpose

Understand exactly why Phase 13B failed.

Inputs
Phase 13B

Phase 14B

Phase 14F

Phase 14H

Questions
Why did rankers tie?

Why did transfer information
not change rankings?

Was pressure absent?

Was ranking value absent?

Were candidates too similar?

Deliverable
ranking_failure_audit.md

Exit Criteria
Every tie explained.

1C.2 Ranking Candidate Taxonomy
Purpose

Create candidate diversity.

Every candidate must belong to one category.

Type A
Frequent + Useful


Common and genuinely valuable.

Type B
Frequent + Useless


Common but misleading.

Type C
Rare + Useful


Important but uncommon.

Type D
Rare + Useless


Low value.

Type E
Transfer-Rich


Useful across many future tasks.

Type F
Transfer-Poor


Useful locally only.

Type G
Compression-Rich


Reduces representation size.

Type H
Deceptive


Looks valuable initially.

Poor future value.

Goal

Prevent:

All candidates looking identical.

1C.3 Future Value Definition
Purpose

Define ranking success.

Future value must be measured independently.

Allowed:

Future utility

Future reuse

Future transfer

Future task benefit


Forbidden:

Ranking score itself


because:

Circular evaluation.

Deliverable
future_value_definition.md

1C.4 Ranking Pressure Design
Purpose

Guarantee disagreement.

Mandatory Rule

At least:

20% Frequent + Useless

20% Rare + Useful


must exist.

Without this:

Frequency and transfer-aware
will often agree.

Required Property

Different rankers must produce:

Different Top-K selections.

Pressure Metric

Define:

Ranking Divergence Rate (RDR)


Example:

Top-K overlap < 100%

Exit Criteria
Rankers demonstrably disagree.

1C.5 Ranker Competition Framework
Purpose

Freeze competitors.

Required Rankers
R1
Transfer-Aware


(IDT)

R2
Frequency

R3
Reuse Probability

R4
Compression-Oriented

R5
Random

R6
Oracle


Upper bound only.

Rule

Every ranker sees:

Same candidate pool
Same information
Same budget

1C.6 Transfer Ground Truth Design
Purpose

Avoid subjective judgments.

Need a frozen definition of:

Future transfer value.


Must specify:

Transfer horizon

Transfer opportunities

Transfer scoring

Rule

Ground truth cannot be derived from:

IDT ranking score.

Deliverable
transfer_ground_truth_protocol.md

1C.7 Evaluation Metrics
Primary Endpoint

Frozen before experiments.

Candidate examples:

Future Transfer Utility

Held-Out Future Value

Future Net Benefit

Secondary Endpoints
Precision@K

Recall@K

Transfer Recall

Utility Gain

Diagnostics
Ranking Divergence Rate

Top-K Overlap

Candidate Distribution

1C.8 Dataset & Split Design
Required Splits
Calibration

Development

Confirmatory

Replication

Rules

Confirmatory set:

Never used for tuning.


Replication set:

Never used for tuning.

Deliverable
ranking_dataset_protocol.md

1C.9 Preregistration Framework

Must freeze:

Primary endpoint

Comparator set

Top-K

Independent unit

SOI

Decision rules

Missing-data handling

Outcomes
Supported

Contradicted

Inconclusive

Unavailable

1C.10 Readiness Review
Checklist
Failure Audit

✅

Candidate Taxonomy

✅

Future Value Definition

✅

Ranking Pressure

✅

Rankers

✅

Ground Truth

✅

Metrics

✅

Splits

✅

Preregistration

✅

Deliverables
ranking_failure_audit.md

candidate_taxonomy.md

future_value_definition.md

ranking_pressure_design.md

ranker_competition_spec.md

transfer_ground_truth_protocol.md

ranking_metrics.md

ranking_dataset_protocol.md

ranking_preregistration_template.md

phase1C_readiness_report.md

Phase 1C Exit Decision

PASS only if:

Rankers disagree

Useful and misleading candidates exist

Future value is independently defined

Evaluation is non-circular

Baselines are frozen

Replication is planned

Primary endpoint is frozen

Most Important Outcome

At the end of Phase 1C, ASFT should finally be able to answer the question that v1.0 never truly tested:

"When frequency, reuse, compression, and transfer information point to different candidates, does transfer-aware ranking actually identify the candidates with the highest future value?"

That is the core scientific question behind IDT, and Phase 1C is designed specifically to make that question answerable.