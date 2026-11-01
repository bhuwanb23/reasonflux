# Phase 13C preregistration v1 — Skill Creation Trigger Theory

**Status:** protocol v1 was frozen before execution; implementation/contract tests passed; calibration seeds 15–19 and confirmation seeds 20–29 are complete. The pre-confirmation copy is archived at `reports/experiments/PHASE-13C-SCT-V1/preregistration_v1_frozen_preconfirmation.md`; all stage artifacts are saved in the report directory.  
**Scope:** controlled synthetic validation of skill-creation economics and downstream use, conditional on the current invariant/task generator. It does not validate natural invariant discovery, overturn Phase 13B, or establish ARC validity.  
**Prior observations:** legacy EXP-02 is exploratory only. Its one-run admissions and birth-time utility are not pooled with v1 confirmation. EXP-IDT-14 is separate and unchanged.

## Frozen design decisions

- **Creation rule:** include maintenance cost in the Phase-13C birth decision, per the user's selection. Implement this as a Phase-13C-specific score; leave the existing global SCV function and all past records untouched.
- **Evaluation horizon:** 10 eligible future task opportunities per candidate/skill.
- **Cost units:** normalized, success-gated fractional reasoning-cost reduction per eligible opportunity. This is simulator utility, not wall-clock compute.
- **Creation cost:** charge once at birth; use the candidate/config value (default `0.10`).
- **Maintenance cost:** charge per eligible opportunity. Use the predeclared per-opportunity value `MC = base_maintenance + 0.01 = 0.06` under the default `SkillConfig`; record overrides. This operationalizes the current flat storage-maintenance term as a per-opportunity simulator charge. It is an explicit modeling assumption, not an empirical compute-cost estimate.
- **Primary birth score:**

  `SCV10 = 10 × p_reuse × AG × TS − CC − 10 × MC`

  Map candidate fields exactly as follows: `p_reuse = clip01(reuse if reuse != 0 else expected_reuse)`; `AG = clip01(abstraction_gain)`; `TS = clip01(transfer_score if transfer_score != 0 else expected_transfer)`; `CC = max(0, creation_cost)`. `clip01(x)=min(1,max(0,x))`. For each component, save the raw value, mapped value, and source (measured/prior/default); clipping is explicit and must never be hidden. Log `CC` defaults/overrides. `MC` is the approved fixed simulator assumption `0.06` per eligible opportunity under the default config. Create iff `SCV10 > 0`; equality means do not create. No threshold is adjusted after calibration or confirmation.

  `p_reuse` is interpreted as probability of skill use per eligible opportunity, not count of total uses; multiplying by 10 yields expected uses in the fixed horizon. `AG` is normalized fractional reasoning reduction per successful use; `TS` is expected success probability. The empirical held-out value is measured separately. If the runner cannot preserve these fields and transformations, stop before running and repair the schema/tests; do not silently change the equation.
- **Realized future value:** on the separate evaluation tasks, sum success-gated fractional reasoning reductions over the 10 eligible opportunities, then subtract `CC` once and `10 × MC`. A failed skill application contributes zero benefit and remains in the record. Report transfer success and accuracy separately, not only inside this scalar.
- **Calibration/confirmation seed split:** calibration seeds `[15,16,17,18,19]`; confirmation seeds `[20,21,22,23,24,25,26,27,28,29]`. These IDs are not present in the current saved experiment JSON seed lists. Record the split in config before execution. No result from calibration seeds is confirmation evidence.
- **Discovery quantity:** use 6 discovery traces per family, matching the existing EXP-02 default. Do not increase this to force count/grouping births; report any missing families.
- **Task split:** for every calibration and confirmatory run seed `s`, generate discovery/candidate traces with task seed `s + 1000` and held-out evaluation tasks with task seed `s + 2000`. Give the 10 held-out eligible opportunities per candidate distinct task IDs; persist the generated task IDs and assert no discovery/evaluation overlap. Composition training, validation, and reuse streams use `s + 3000`, `s + 4000`, and `s + 5000`; lifecycle shadow probes use `s + 6000` to prevent task-ID overlap with composition training. The random policy uses a separate recorded RNG stream keyed by run seed. Configuration and contract tests must enforce these offsets before any run.
- **No code path may launch the full benchmark from an aggregation unit test.** Aggregation tests use stubbed per-seed records; experiment execution is an explicit command.

## Calibration-only rules (seeds 15–19)

1. Use the same candidate eligibility gate and SCV10 equation planned for confirmation.
2. Freeze the random-creation probability to the pooled SCT birth proportion among eligible candidates on these calibration seeds. In confirmation, randomly assign eligible candidates using this fixed probability and a recorded RNG seed; do not match the realized SCT count per confirmatory seed.
3. For EXP-SCT-06 only, derive low/medium/high decision cutoffs as the 25th/50th/75th percentiles of calibration-candidate SCV10. Freeze those numeric cutoffs before opening confirmation records. Keep the primary SCT cutoff at zero regardless of this sensitivity analysis.
4. Calibration runs may reveal implementation faults. Any protocol, score, or task-generator change after inspecting calibration outcomes must be versioned, disclosed, and followed by a fresh untouched confirmation split. Do not use confirmation outcomes to repair the design.

## Confirmatory arms and matched controls (seeds 20–29)

All arms receive the same per-seed discovery traces, eligible invariant/candidate pool, held-out task opportunities, solver, task order, library capacity, and cost accounting. Candidate eligibility is fixed before the SCT decision. Record unsuccessful outcomes, no-matches, and candidates rejected by each gate.

| Arm | Frozen policy |
|---|---|
| SCT | Create iff `SCV10 > 0` |
| Never-create | Keep the same discovery/invariant memory, but create no executable skills |
| Always-create | Create every candidate passing the common non-SCV eligibility gate |
| Random-create | Bernoulli-create from the common eligible pool using calibration-frozen probability |
| Memory-only | Store/retrieve trace or invariant exemplars but do not create executable skills; implement and test this separately, not by relabeling `skill_storage` |

The existing `skill_storage` and `random_skill_creation` baselines may be reported as contextual only; their current candidate pools/budgets are not matched sufficiently to serve as the primary SCT controls.

## Primary and secondary outcomes

### Primary confirmatory outcome

Per seed and policy, compute mean 10-opportunity realized net value per initially eligible candidate. The primary policy contrasts are paired SCT-minus-control differences versus never-create, always-create, random-create, and memory-only. Report mean, SD, 95% CI, effect size, and all ten per-seed differences. Strong SCT superiority requires the predeclared paired 95% CI lower bound to exceed zero against **each** primary control; otherwise report the relevant comparison as inconclusive or failed, not as a pass. Report skill count/library size and total creation/maintenance cost beside net value so a zero/negative result cannot be hidden by averaging.

### Required secondary outcomes

- **Emergence:** automatic births by family and unique semantic skill; distinguish candidate, provisional, validated/active, and duplicate signature. No manual skill insertion in the SCT arm.
- **SCV predictiveness (EXP-SCT-05):** compare pre-birth SCV10 with held-out 10-opportunity realized net value for every eligible candidate using isolated shadow evaluations that do not affect the policy arm. Report Spearman correlation and seed-clustered 95% CI; compare with frequency/IS, `p_reuse`, AG-only, and TS-only predictors. SCV–SU correlation is descriptive only because formulas share terms.
- **Utility:** record birth and fixed checkpoint RCG/TV/CP/RV/CC/MC/NR/SU breakdowns. SU is secondary accounting; realized net value above is the prediction target.
- **Reuse:** report eligible opportunities, applied attempts, successes/failures, no-match, unique skills ever reused / skills with an eligible opportunity, successful applications / eligible opportunities, and the requested reused-skills/created-skills ratio.
- **Reasoning reduction:** paired baseline vs skill-enabled costs on the same held-out task; report raw step difference and normalized fractional reduction, with correctness preserved as a separate metric.
- **Transfer:** report task-level success, TS, and family coverage; no positive transfer credit for incorrect replay.
- **Threshold study:** report all three calibration-frozen cutoffs and their confirmatory skill counts/net values; do not select a winner based on the confirmatory results.
- **MC sensitivity:** repeat the confirmatory net-value calculations at per-opportunity MC `{0.00, 0.03, 0.06, 0.12}` (zero, half, nominal, double). The primary assumption remains 0.06; do not select a favorable value after seeing confirmation results.

## Focused lifecycle and composition studies

These are secondary, separately reported modules, not mixed into the primary baseline comparison unless their behavior is explicitly enabled in every relevant arm.

- **Lifecycle:** use a predeclared task schedule to expose skills to eligible use, then 10 unused task-clock ticks to test dormancy, then at least `reactivate_min_evidence` relevant opportunities to test reactivation. Record state transitions, utility, success, and negative cases. Do not confuse an imposed idle schedule with organic natural-language task frequencies.
- **Composition (EXP-SCT-15/16/17):** use actual solver/task outcomes for reflection→counting and multi-skill tasks; compare no skill, best single skill, and ordered composition on paired held-out tasks. Never pass a constant `ComposeOutcome` as if it were learned performance. Report correctness, composition utility/cost, transfer, reasoning savings, and reuse of the same composition on new tasks.
- **Ablations:** no-SCV bypasses only SCV; no-lifecycle disables lifecycle updates but preserves birth and reuse; no-composition disables only composition. Match all other candidates, task streams, random seeds, and accounting.

## Reporting and stop rules

- Minimum confirmatory sample: 10 independent run seeds (20–29); retain seed-level and paired per-task rows.
- Report n, mean, SD, 95% CI and effect size for each major outcome. Bootstrap/resample by run seed, not by treating tasks from the same seed as independent.
- Report all four expected families, including absent or rejected skills, without changing minimum generality/quality filters to force emergence.
- Stop before confirmation if task split, cost units, candidate field mapping, memory-only arm, or composition outcome plumbing fails its contract tests.
- A Phase 13C success claim must be dimension-specific. Failure of SCV prediction, reuse, reasoning savings, transfer, lifecycle, or composition remains visible even if another dimension passes. This is synthetic evidence only.

## Required evidence package (user-requested seven items)

1. Skill emergence/birth table (EXP-SCT-01–04).
2. SCV distribution, threshold sensitivity, and held-out predictiveness (EXP-SCT-05/06).
3. Utility trajectories and future realized net value (EXP-SCT-07–09).
4. Reuse opportunity and success statistics plus paired reasoning-cost reduction (EXP-SCT-10/11).
5. Task-grounded composition and composition-reuse outcomes (EXP-SCT-15–17).
6. Matched SCT vs never/always/random/memory-only baseline table.
7. Matched no-SCV/no-lifecycle/no-composition ablation table.

**Phase 13C confirmation is complete.** Calibration-derived values were frozen before opening confirmation seeds; the pre-confirmation digests remain in `pre_confirmation_freeze.json`. Results and implementation/reporting limitations are recorded in `evidence_package.md` and `execution_note.md`.
