# Phase 1G.3 — Coverage Benchmark Specification

## Definitions

- **Task ingestion rate:** task files passing schema/grid parsing ÷ task IDs attempted.
- **Budgeted demo-fit coverage:** tasks with at least one exact-fit candidate found within the frozen candidate/compute budget ÷ all tasks attempted. This is the main representation coverage output.
- **Full-inventory demo-fit coverage:** same measure under an explicitly diagnostic exhaustive scan. Report separately; never substitute it for the scored-arm budget.
- **Trace generation rate:** attempted tasks with a serialized, schema-valid trace ÷ attempted tasks.
- **Successful trace rate:** tasks with a candidate exactly matching all allowed demonstrations and passing deterministic replay ÷ attempted tasks. Report separately from schema-valid failures.
- **Candidate yield:** unique invariant/structure candidates proposed ÷ successful traces, with unique candidate count, diversity, rejection reasons, and repeated proposals shown.
- **Skill yield:** promoted skills ÷ independently validated invariant candidates; also report counts and survival.
- **Transfer rate:** successful eligible skill applications ÷ eligible skill-task attempts, paired with transfer utility and negative-transfer rate. If eligible denominator is zero, transfer is **unavailable**, not zero.
- **Capability formation:** externally validated capability units under Phase 1E behavioral criteria; report counts, persistence, utility, and eligible denominators. Internal C_t/CGR is not a capability label.
- **Accuracy:** exact task success, partial pixel accuracy, and family/annotation-category accuracy on held-out test outputs. This is never coverage or transfer evidence.

## Required breakdowns

Report all stages by split, representation version, candidate budget, task ID, family/reference annotation (including unknown/ambiguous), and arm. Show counts and denominators as well as rates. Use task-ID as the independent unit; family/seed and repeated program candidates are nested. Preserve no-fit, timeout, invalid trace, candidate rejection, insufficient support, no eligible skill, negative transfer, and missing-gold statuses separately.

## Independent annotation and invariant reference

ARC has no authoritative semantic-family labels for this purpose. Before candidate review, two independent domain annotators may label task phenomenon/operation hypotheses from allowed demonstration pairs only; blind to model candidates, arm, and held-out test outputs. Preserve ambiguous/unknown and report agreement/adjudication. These labels are a benchmark reference—not ground truth for latent reasoning. Primary invariant validity must also use behavioral evidence: recurrence across disjoint task IDs, survival on withheld demonstration pairs or preregistered counterexample probes, and downstream held-out utility. Report annotation agreement and behavioral validation separately.

## Data-sufficiency/zero rule

A count of zero is reportable as observed zero when the stage denominator is available. It does not itself prove theory failure. If the previous stage supplied too few examples to evaluate a stage's frozen criterion, label the stage `inconclusive` or `unavailable` with its support shortfall; do not treat failure to have an eligible denominator as a negative transfer result. Stage activation thresholds and minimum N are calibrated only on development data and frozen before confirmation.