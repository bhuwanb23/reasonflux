# EXP-IDT-14 Protocol — Confounded-Frequency Stress Test

**Status:** exploratory, post-Phase-13B design. Both per-family-six and per-family-twelve prototypes were inspected on seeds 5–9 during development; they are pilot-only and excluded from the reported final run. The configuration below is frozen before evaluating seeds 10–14, which were not used in the original Phase 13B run or these prototypes. This preserves the original `synthetic-v1` null result and is not a retrospective pass of the Phase 13B closure gate.

## Question

Can transfer-aware ranking select a transferable pattern over a more frequent, non-transfer-bearing pattern when both appear in the same validated candidate pool?

## Intervention

For each run seed, generate 48 traces (12 per synthetic family) using the existing low-difficulty synthetic solver. Add a zero-cost, no-op trace marker named `normalize_grid` to every generated trace in exactly three predeclared families: reflection, rotation and counting. Do not add it to grouping traces. The marker does not change the task input/output or solver execution. Since mining is success-trace-biased, the observed marker frequency is expected to be about 30 (some rotation traces fail), while its family generality stays at 0.75. It should be frequent but not universal-noise filtered by the 0.95 rule.

This is a **controlled trace confound**, not natural task data. It tests a specific failure mode (high frequency without transfer). It must be described as such.

## Split and ranking

- Run seeds: **10–14**, held out from both the original Phase 13B run (0–4) and the per-family-six pilot (5–9).
- Calibrate candidate transfer utility on generated tasks using task seeds `1000 + run_seed`.
- Evaluate rankings on disjoint generated task seeds `2000 + run_seed`.
- Use one shared, validated, semantically deduplicated candidate pool for all methods.
- Methods: transfer-aware (calibration TU), frequency-only, IS-only/no-transfer, and random (16 seeded permutations).
- Primary outcome: held-out mean transfer utility of the **top-1** candidate.
- Secondary outcomes: top-2 utility and the full mean-utility-at-k curve.
- Stress-test pass rule: transfer-aware top-1 must strictly exceed frequency-only, no-transfer and random for every run seed. This is a supplemental stress-test rule, not the original Phase 13B gate.

## Reporting and interpretation

Save the exact task/seed/config, candidate pool, per-candidate calibration and evaluation utility, method rankings, per-seed differences and 95% descriptive intervals. Retain zero-transfer candidates; do not drop the confounder because it is inconvenient. A pass means the ranking mechanism can reject this specified frequent no-op in this simulator. It does not establish general IDT validity, solve the original baseline tie, or validate the method on ARC. A confirmatory follow-up requires a new frozen protocol and untouched task seeds before results are inspected.

The machine-readable config is `configs/idt_confounded_benchmark.yaml`; the runner is `experiments/exp14_confounded_idt.py`.
