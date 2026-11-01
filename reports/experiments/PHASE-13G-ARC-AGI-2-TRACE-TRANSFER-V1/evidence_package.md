# Phase 13G — ARC-AGI-2 Trace, Invariant, Skill, Transfer and Growth

**Experiment:** `PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1`  
**Status:** completed bounded public-training-set validation. **Claim boundary:** this is not an ARC-AGI-2 official evaluation score and does not claim that ASFT solves ARC.

## Executive result

- Dataset: 1,000 ARC-AGI-2 training task IDs partitioned into 600 discovery / 200 transfer / 200 holdout; official evaluation JSON was not extracted, parsed, scored, or used as feedback. A temporary source archive containing evaluation blobs was downloaded during reconnaissance, only its filenames were listed, and it was deleted; see the disclosed transport deviation in Table 1 and the preregistration.
- Run integrity: attempt 01 generated transfer and holdout predictions in memory, then failed during report serialization (`KeyError: 'task_id'`); no numeric outcome rows were persisted or inspected. Attempt 02 is a software-only serialization fix (plus an explicit unavailable value for unsupported-task stability) on the same frozen split and is **not** an independent replication or pristine holdout confirmation. See the preserved attempt-01 folder.
- Trace mining input: 3 discovery traces, 3 exact-demo-fit, 0 accepted invariant candidates; 0 skill candidates measured and 0 promoted under existing gates.
- Transfer precision among exact-demo-fit candidate-skill attempts: None; denominator: 0 applicable task IDs. This is internal transfer evidence, not final holdout precision.
- Holdout exact task accuracy ASFT: 0.005; candidate trials/task: 2.995. These are for the preregistered bounded DSL only.
- Growth/IG: see Table 6. Missing capability groups or components remain unavailable; no ARC-specific IG replacement was invented.

## Protocol and dataset boundaries

The fixed DSL includes identity, reflections, rotations, transpose/anti-transpose, constant translation and bijective recoloring. Exact fit to all demonstrations is mandatory. The task ID is the independent unit; exact task success requires all test outputs in the task to match. Main arms use a maximum of three program trials. Unsupported tasks remain failures for this bounded system.

ARC-AGI-2 does not publish authoritative semantic family labels. Reflection, rotation and translation are directly labeled when the DSL fit supports them. Symmetry is an input/output property only; counting, grouping, object detection and pattern completion are not operationalized as transformations in v1 and are not assigned invented labels. Color remapping is not counted as grouping.

## EXP-ARC-07 — Trace fidelity and stability

The traces are bounded program-search traces, not claims about private human cognition. They record grid-schema validation, fixed candidate enumeration, the selected operation, and exact demonstration verification. Figure 2 and Table 3 report schema, replay fidelity and 10 seeded demonstration-order perturbations/task. Unsupported attempts are retained in the task-level trace file.

## EXP-ARC-10 — Invariants and IS–transfer

Invariants were mined from successful discovery traces using the existing TraceMiner. IS retains the repository formula (frequency × consistency × generality); generality is only relative to task-family labels observed by this limited program inventory. Figure 3 is descriptive, not causal. Table 4 retains accepted and rejected candidates and reasons.

## EXP-ARC-13 — Skills, SCV, utility and reuse

Skill proposals originate from accepted invariant candidates. Transfer evidence comes only from the internal 200-task transfer split. SCV and skill utility retain the repository APIs and frozen default skill thresholds; promotion requires at least three applicable transfer tasks plus `qualify_candidate`. Figure 4/Table 4 report null and rejected candidates as well as promoted skills.

## EXP-ARC-15 — Transfer and reasoning cost

Figure 5 compares exact task accuracy on transfer and holdout. Table 5 reports paired task-ID bootstrap contrasts of ASFT versus each B1–B4 baseline on final holdout (10,000 resamples, fixed seed 1307), including both accuracy and candidate-trial cost. Cross-semantic-family transfer cannot be identified without authoritative ARC labels; measured structural-bucket outcomes are descriptive. Candidate trials are not human time or FLOPs.

## EXP-ARC-17 — Capability growth and IG

Figure 6 combines candidate-trial cost with cumulative-discovery-prefix capability/IG diagnostics. Prefix curves reuse the same internal transfer split for validation and are descriptive, not independent estimates. Only repository-produced capabilities with evidence are counted. If no valid multi-skill capability group exists, IG is `unavailable`, not zero or replaced with a new formula.

## Failures, nulls, and limits

Table 6 and task-level CSV retain unsupported-v1 tasks, demo-fit/test-mismatch failures, budget misses, candidate rejection reasons, and unavailable growth values. This study tests a compact symbolic subset of ARC operations and cannot establish broad ARC generalization, capability growth outside this DSL, or general intelligence. The public ARC-AGI-2 evaluation and private tiers remain unscored.

## Evidence package

### Figures

1. [Figure 1 — Taxonomy and DSL coverage](figures/figure_1_taxonomy_coverage.svg)
2. [Figure 2 — Trace stability](figures/figure_2_trace_stability.svg)
3. [Figure 3 — Invariant strength and transfer](figures/figure_3_invariant_transfer.svg)
4. [Figure 4 — Skill utility](figures/figure_4_skill_utility.svg)
5. [Figure 5 — Transfer accuracy](figures/figure_5_transfer_accuracy.svg)
6. [Figure 6 — Cost and capability growth](figures/figure_6_cost_growth.svg)

### Tables

1. [Split integrity and data hashes](tables/table_1_split_integrity.csv)
2. [Taxonomy and operator coverage](tables/table_2_taxonomy_coverage.csv)
3. [Trace quality and stability](tables/table_3_trace_quality_stability.csv)
4. [Invariant/skill lifecycle](tables/table_4_invariant_skill_lifecycle.csv)
5. [Holdout B1–B4 contrasts](tables/table_5_holdout_B1_B4_contrasts.csv)
6. [Capability growth, failures and unavailable metrics](tables/table_6_capability_growth_failures.csv)

Additional records: `task_outcomes.csv`, `discovery_trace_quality.csv`, `invariants.csv`, `skills.csv`, `growth.csv`, `summary.json`, `pre_holdout_lock.json`, and `run_manifest.json`.

## Source and license

ARC Prize Foundation, [official ARC-AGI-2 repository](https://github.com/arcprize/ARC-AGI-2), pinned commit `f3283f727488ad98fe575ea6a5ac981e4a188e49`, Apache-2.0. Upstream attribution and license are retained under `datasets/arc/arc-agi-2/`.
