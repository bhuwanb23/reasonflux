# Phase 2I — Data and Annotation Plan

## Permitted diagnostic data

The only presently auditable candidate-production set is the 600-task historical ARC `discovery` split. Every ID has Phase 2B/2C exposure; use is **development/diagnostic only**, never confirmatory or a pristine estimate. The other 400 historical transfer/holdout IDs are excluded from Phase 2I candidate generation. The Phase 13G holdout reuse caveat remains attached to the historical split.

Read each task's training demonstrations only. The test outputs in public ARC training files are sealed from Phase 2I code by the runner contract; do not parse them for candidate construction, features, trace labels, family annotation, or stopping decisions.

## Family annotation requirement

The current data manifest has no independent semantic family labels. Phase 2D/2E reports program-derived trace family labels; Phase 2F explicitly prohibits using those as independent task-family labels. Before a Phase 2I run:

1. define an outcome-blind family taxonomy usable across both R1 and R3;
2. annotate from permitted task training demonstrations without seeing representation-specific search outputs or candidate yield;
3. use at least two independent annotators plus adjudication, retaining agreement and uncertainty; or provide an independently justified machine annotation protocol with human audit;
4. hash the annotation rubric and task-to-family map before candidate generation; and
5. preserve `UNKNOWN/AMBIGUOUS` rather than force a family label.

If qualifying candidates cannot be shown to span two independently annotated families, mark family/generalization qualification unavailable; do not infer family from the operator/program that solved a task.

## Split and exposure rules

- Phase 2I: historical discovery IDs only, development designation, explicitly exposed.
- No new C1/C2/C3/C4 split is assigned by this program; do not claim confirmatory readiness.
- Candidate-production outputs from this exposed set cannot supply pristine confirmatory or replication labels.
- A later Phase 3 attempt requires a new authorized, disjoint panel/task/family split and the Phase 3A-R gates; nonzero yield here is necessary, not sufficient.
