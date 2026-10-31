# Phase 13 Experiment Registry

This registry is the source of truth for experiment governance. Every run must
record its experiment ID, seed, configuration, dataset policy, metrics, and
success criteria.

## Registered experiments

| ID | Experiment | Claim | Primary metrics | Status |
| --- | --- | --- | --- | --- |
| EXP-01 | Invariant discovery | IDT discovers transferable invariants | IS, precision, recall, confidence | Implemented |
| EXP-02 | Skill formation | SCT promotes useful skills when SCV justifies creation | SCV, SU, reuse, health | Implemented |
| EXP-03 | Transfer | Skills learned on one task help another task | TS, TU, NTR | Implemented |
| EXP-04 | Capability growth | Repeated experience increases capability and intelligence | CGR, IG, IGR, coverage | Implemented |
| EXP-05 | End-to-end ASFT | The complete ASFT loop produces measurable growth | CGR, IG, reuse | Implemented |
| EXP-06 | Baselines | ASFT can be compared with non-ASFT learning strategies | CGR, IG, capability score | Harness available |
| EXP-07 | Ablations | Removing a contribution weakens the corresponding outcome | Layer-specific metrics | Harness available |
| EXP-08 | ARC validation | The mechanism generalizes beyond synthetic tasks | transfer, reuse, reasoning reduction | Planned |

## Governance fields

Each experiment runner exposes `EXPERIMENT_META` with:

- `experiment_id`: stable registry identifier.
- `hypothesis`: falsifiable statement.
- `claim`: contribution being tested.
- `primary_metrics`: metrics used for the main conclusion.
- `success_thresholds`: thresholds fixed before execution.
- `failure_thresholds`: explicit failure conditions.

## Dataset policy

- **Tier 1 — synthetic mechanism tasks:** reflection, rotation, counting, and
  grouping. These validate individual mechanisms.
- **Tier 2 — transfer tasks:** composed or held-out family combinations such as
  reflection+count and rotation+grouping. Discovery and validation task IDs must
  be disjoint.
- **Tier 3 — ARC tasks:** external-validation data. ARC integration is tracked
  by EXP-08 and is not silently substituted with Tier 1 data.

Discovery tasks are used to mine invariants and form candidate skills. Transfer
tasks are generated with a separate seed and task batch and are only used after
discovery has completed.

## Standard report structure

Every report contains:

1. Configuration
2. Dataset
3. Metrics
4. Results
5. Failure cases
6. Observations

Raw per-seed records and aggregate summaries are stored under
`reports/experiments/<experiment_id>/`.

## Phase 13A gate

Phase 13B may begin only after the registry, seed policy, metric definitions,
statistical summaries, reproducibility records, and smoke-test gate report are
present. Thresholds are configuration inputs and must not be changed after
observing results.

## Phase 13B IDT experiment map

| ID | Experiment | Runner | Primary metrics |
| --- | --- | --- | --- |
| EXP-IDT-01 | Reflection discovery | `experiments/idt_experiments.py` | IS, discovery |
| EXP-IDT-02 | Rotation discovery | `experiments/idt_experiments.py` | IS, discovery |
| EXP-IDT-03 | Counting discovery | `experiments/idt_experiments.py` | IS, discovery |
| EXP-IDT-04 | Grouping discovery | `experiments/idt_experiments.py` | IS, discovery |
| EXP-IDT-05 | Invariant precision | `experiments/idt_experiments.py` | IP |
| EXP-IDT-06 | Invariant recall | `experiments/idt_experiments.py` | IR |
| EXP-IDT-07 | Invariant confidence | `experiments/idt_experiments.py` | confidence, IS |
| EXP-IDT-08 | IS versus TS correlation | `experiments/idt_experiments.py` | Pearson, Spearman |
| EXP-IDT-09 | Cross-family transfer | `experiments/idt_experiments.py` | TS, TU, reuse |
| EXP-IDT-10 | Transfer utility ranking | `experiments/idt_experiments.py` | TU |
| EXP-IDT-11 | Variation survival | `experiments/idt_experiments.py` | VST |
| EXP-IDT-12 | Noise resistance | `experiments/idt_experiments.py` | rank stability |
| EXP-IDT-13 | Sparse data | `experiments/idt_experiments.py` | IS, confidence |

The runner uses the Phase 13A seed policy and writes the consolidated evidence
package to `reports/experiments/idt_evidence/`.
