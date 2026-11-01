# Phase 13D Transfer v1 — preregistration

**Status:** design frozen before any Phase 13D execution. No Phase 13D benchmark has run. See `phase_13d_preflight.md` for the repository audit and known limitations. Machine-readable companion: `configs/phase13d_transfer_v1.yaml`.

## 1. Scope and honest-claim boundary

Phase 13D tests whether experience-derived invariants/skills help on held-out synthetic grid programs. The dataset is new (`synthetic-transfer-v1`); historical `synthetic-v1`, EXP-03, Phase 13B, Phase 13C, and EXP-IDT-14 are not modified or pooled. Results do not establish ARC or natural-task external validity. No empirical success is promised: each success/failure criterion will be computed from the frozen outcomes, with nulls retained.

The repository has no canonical DreamCoder implementation. B4 is a **DreamCoder-like trace-compression proxy**, not DreamCoder: it mines recurring canonical operation subsequences from training traces, stores the most frequent eligible chunks under the same slot budget, and reuses a matching chunk without invariant scores or SCT.

## 2. Run split and candidate formation

- Ten independent confirmation run seeds: `[50,51,52,53,54,55,56,57,58,59]`. Contract-test fixtures previously instantiated isolated one-task programs under test labels 40 and 42; those labels are explicitly excluded from confirmation. The frozen set is distinct from Phase 13C calibration/confirmation seeds and the legacy EXP-03 one-run record.
- Per seed `s`, training traces use `s+1000`; near, moderate, composition, structural, negative, and randomization test streams use `s+2000`, `s+3000`, `s+4000`, `s+5000`, `s+6000`, and `s+7000`. Within each task-family stream, cell slots use disjoint blocks of 100 task seeds. Training uses 12 task seeds per family, fixed `variant=0` (including quarter-turn rotation), the existing `GridSolver`, `TraceLogger`, and invariant pipeline. Each experiment cell receives 10 held-out tasks with distinct recorded IDs. The task-ID auditor asserts that train/test and cross-cell streams do not collide.
- Train 12 examples per existing family, using the existing trace and invariant pipelines. Promote through the existing qualification path with provisional-prior evidence allowed only for trials. Use Phase 13C's frozen SCV10 mapping and `SCV10 > 0` rule for the SCT arm; the always-create arm uses the same common non-SCV candidate pool. Do not weaken qualification or insert hand-written skills. If a required source skill does not emerge, the affected cell is **not evaluable** and stays in the denominator/report.
- Candidate invariants and skills are linked by IDs. Candidate `IS` is the repository's frozen invariant strength; skill `SU` is the existing utility score. Each transfer task is paired across policies and scored from the same input grid and expected program.

## 3. Phase-13D synthetic task program and cost model

Each task has a deterministic input grid and a predeclared ordered program made from `apply_reflection`, `apply_rotation`, `count_objects`, `group_by_color`, and the experiment-local reducer `count_groups = len(group_by_color(current_grid))`. Training traces use the existing solver for its existing four operations; `count_groups` is a derived held-out evaluator operation, not a learned source skill. Evaluation recipes include the stated single-operation, two-operation, three-operation, and unseen-order tasks. Output is computed by the reference interpreter: transform operations change the grid; reducers produce their stated output; a composite task returns the final grid when it contains a transform plus all requested reducer outputs. Thus a transform-plus-count/group program has a verifiable ordered output, not an assumed composition label.

The experiment-local reference interpreter is tested against hand-calculated grids and does not change `src/solver/` or global operation costs. A task baseline executes each operation from scratch: 3 reasoning steps for each transform (two search/inference steps plus execution), 2 for each reducer (one search/inference step plus execution), plus 1 final verification step. A matched single-skill application costs 2 steps (one retrieval/replay step plus execution) in place of the operation's search/inference; an ordered composition costs 1 sequence-retrieval step plus 1 execution step per required operation, plus final verification. A forced random/wrong skill costs 2 steps per applied skill in addition to the task's baseline. Exact costs and output correctness are logged per task. Memory and compression arms use their separately defined replay rules below.

For each matched task, performance is frozen as:

`P = exact_correctness_indicator − 0.02 × reasoning_step_count`

`TS = mean(P_after − P_before)` on the same tasks, using `compute_ts` only as the subtraction helper. The coefficient 0.02 is fixed before running. It ensures a wrong answer is worse than the maximum plausible step saving. Report accuracy and raw/normalized reasoning-cost changes separately; do not use TS to conceal a correctness loss.

- `RCR_steps = baseline_steps − transfer_steps`; also report normalized RCR and success-gated fractional savings.
- `TU` uses the repository's `compute_tu(success_rate, mean_success_gated_fractional_RCR, target_family_coverage)`.
- `ITS` uses the repository's `compute_its(attempts, success-gated benefits)`.
- One assigned transfer application is one policy-arm decision on one held-out task program (one task-level row), even when that program replays multiple ordered component skills. `NTR_accuracy = incorrect assigned task episodes / assigned task episodes` (same failure-rate interpretation as the repository metric). Also report `NTR_harm = assigned episodes where P_after < P_before / assigned episodes`; this catches correct-but-wasteful transfer. `reuse_rate` is task episodes with at least one retrieved/forced learned representation divided by eligible held-out task episodes. Per-task skill IDs and operation counts remain separate. No-match is separate from an assigned application.
- Report reuse attempts, correct/incorrect applications, no-match opportunities, unique skills reused/created, family coverage, operations/steps, and available candidate-evaluation counts separately.

## 4. Frozen arms

1. **ASFT/SCT:** invariant-derived eligible skills, create iff frozen SCV10 > 0, persistent library, composition available only where the repository composition proposer emits a candidate.
2. **B1 no learning:** same task stream and reference solver, no invariant/skill/exemplar reuse.
3. **B2 memory-only:** nearest exact-family successful raw trace exemplar; replay without a Skill object or persistent SkillLibrary.
4. **B3 random skills:** uniform selection from the same learned skill pool using the independent seed stream; forced diagnostic applications are retained even when wrong/harmful.
5. **B4 compression proxy:** extract each successful single-operation training trace's canonical program after search/admin steps are removed; enumerate recurring subsequences of length 1–4 appearing in at least two traces; store at most one chunk per common eligible skill-candidate slot and replay a matched chunk without invariant or SCT metadata. Since v1 training recipes contain one family operation each, length-2–4 chunks are structurally unavailable and remain null/not present. Label only as a compression proxy.
6. **A1 no invariants:** literal raw-trace programs only, no recurrence/generalization score; retain at most one training exemplar per common eligible skill-candidate slot, so its slot budget equals B4 and ASFT's candidate-slot count.
7. **A2 no SCT:** create every candidate passing the common non-SCV qualification gate.
8. **A3 no persistent SkillLibrary:** a trained skill can be used once on a matching held-out opportunity and is then removed.
9. **A4 no composition:** use eligible individual skills only; do not apply an ordered composition.
10. **Safe negative-control retrieval:** ordinary `ReuseEngine` retrieval is run for invalid combinations and should reject non-applicable skills. Separate forced-application diagnostics (EXP-TR-15/16/17) intentionally bypass retrieval only inside the Phase-13D harness to measure counterfactual harm; they are never described as normal safe-policy behavior.

All policy arms receive the same eligible tasks, training traces, candidate pool, and cost units. Random selection has a separately recorded RNG seed `run_seed + 7000 + cell_number × 101 + policy_index`; selected skill IDs are retained in task-level rows. Policy effects are paired by task and summarized by run seed.

## 5. Experiment map (all cells run over the ten seeds)

| Experiment | Taxonomy | Frozen task/contrast |
|---|---|---|
| EXP-TR-01 | Near | Reflection skill → held-out reflection grids with changed size/variant |
| EXP-TR-02 | Near | Rotation skill → held-out rotation grids with changed size/variant |
| EXP-TR-03 | Near | Counting skill → held-out counting grids |
| EXP-TR-04 | Moderate | Reflection skill → ordered reflection+grouping program |
| EXP-TR-05 | Moderate | Rotation skill → ordered rotation+counting program |
| EXP-TR-06 | Moderate | Grouping skill → ordered grouping+counting program |
| EXP-TR-07 | Compositional | Reflection and counting learned separately; ordered composition vs best single vs B1 |
| EXP-TR-08 | Compositional | Reflection and grouping learned separately; ordered composition vs best single vs B1 |
| EXP-TR-09 | Compositional | Rotation and counting learned separately; ordered composition vs best single vs B1 |
| EXP-TR-10 | Structural | Reflection, rotation, grouping source skills cooperate in one ordered three-op program |
| EXP-TR-11 | Structural/novel order | Known component skills applied in a held-out order not present in training |
| EXP-TR-12 | Cost | Matched raw and normalized reasoning-cost reduction for every transfer cell |
| EXP-TR-13 | Search | Compare operations/steps and actual candidate-evaluation counters; report unavailable counters as null, not zero |
| EXP-TR-14 | Reuse efficiency | Compare exact raw-trace retrieval, compressed-chunk reuse, skill replay, and rediscovery baseline on matched tasks |
| EXP-TR-15 | Negative | Force reflection on pure counting; measure correctness and added reasoning cost separately |
| EXP-TR-16 | Negative | Uniform random-skill application across held-out task types; report accuracy NTR and harm NTR |
| EXP-TR-17 | Negative | Wrong ordered composition vs correct program and B1 |

## 6. Capability growth and correlations

After each predeclared test block, derive capabilities using the existing capability proposal/validation path from the currently verified skill library; do not hand-create capability records. Compute `C_t` and `CGR=(C_t-C_(t-1))/Δt` with repository APIs. If no capability is valid/eligible for a block, retain `C_t/CGR` as unavailable and do not substitute a custom score. Correlations are seed-clustered and descriptive: `IS↔TS`, `SU↔TS`, and `TS↔CGR`. Report candidate/skill/seed sample sizes and all zero-variance/undefined correlations.

## 7. Statistics and decisions

- Independent unit: run seed; 10 seeds; 95% intervals by seed-cluster bootstrap, with mean, SD, paired per-seed values, and standardized paired effect where defined.
- A direction is called **positive/stable** only when its mean is positive, its seed-bootstrap 95% lower bound is above zero, and at least 8/10 seed means have the same positive sign. Define `TS≈0` as a point estimate in `[-0.01,+0.01]`; retain the exact estimate and interval.
- The primary positive-cost-reduction gate uses success-gated fractional RCR; raw step and normalized RCR remain reported separately. Composition adds value only if paired composition-minus-best-single TS and success-gated fractional RCR are both stable-positive under the seed rule, and the paired mean exact-accuracy difference is nonnegative. Negative transfer is detected when forced application causes an exact failure or `P_after < P_before`; both rates are reported.
- ASFT beats a baseline only if its paired TS 95% seed-bootstrap lower bound is above zero against that baseline. Ablation degradation is assessed by paired full-minus-ablation TS; do not hide an equal or superior ablation.
- Correlation signs are predeclared hypotheses, not magnitude gates: report each coefficient and sample size; a positive estimate is directional support, a zero/negative estimate is flagged as a failure-condition signal that transfer may be unrelated to invariants/skills, and an undefined estimate is unavailable. Do not tune or drop skills to alter the correlation.
- The final criterion dashboard labels every requested gate passed, failed, or unavailable. No seed, task recipe, cost coefficient, metric, filter, or baseline is changed after outcomes are observed. Any implementation change that can affect outcomes requires versioning and a fresh untouched seed set.

## 8. Stop/report rules and required artifacts

Before execution, contract tests must pass for exact output semantics, operation ordering, task-ID disjointness, pairing, TS/RCR/NTR formulas, missing-skill/null behavior, random draws, compression extraction, and report aggregation. Contract tests may use stubs but may not call full benchmark entry points.

The result package will contain: transfer taxonomy figure; score by family/type; reasoning-cost figure; transfer/CGR timeline; positive-vs-negative figure; tables for near, moderate, compositional, structural transfer, matched baselines, and matched ablations; candidate/task-level CSV/JSON; seed-level stats; code/config/protocol hashes; and an explicit synthetic-only validity statement. Missing candidate skills, unavailable metrics, failed transfer, and baseline wins remain visible.

**Success is not guaranteed by code.** Passing software contracts is distinct from empirical transfer, scientific validity, and ARC external validity. The Phase 13D claim will be marked pass/fail/unavailable by dimension under these rules.