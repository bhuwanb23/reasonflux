# Phase 13C — SCT Evidence Preflight

**Status:** PRE-FLIGHT; no new Phase 13C validation run has been made for this audit  
**Purpose:** map the proposed Skill Creation Trigger Theory (SCT) claims to the current code and saved evidence, define the seven requested evidence deliverables, and identify what must be frozen before a confirmatory run.  
**Scope boundary:** this phase evaluates skills conditional on the current synthetic invariant/task pipeline. It does not repair or overturn the failed original Phase 13B IDT gate, and it is not ARC validation.

## Decision summary

The repository has working skill-creation, utility, reuse, lifecycle, reactivation, and composition components, plus tests and some baseline runners. It does **not** yet contain a Phase 13C evidence package that supports the SCT claims. The legacy EXP-02 artifact is an initial software/demo result, not confirmatory evidence: it is one run, reports four reflection/rotation-pattern skills (including duplicate concepts), uses prior-enabled admission in the runner, gives no future held-out utility/reuse/transfer outcomes, and has no matched SCT baseline comparison.

No thresholds or metrics are changed here. No Phase 13C benchmark is run in this preflight. The raw proposal remains in `phase_13c.md`; this document is the code/evidence audit and a proposed protocol freeze checklist.

## 1. Skill emergence results

### Existing artifact

`reports/metrics/exp02_skills.json` reports:

- 4 promoted candidates from 4 promotable invariants.
- The listed signatures are two reflection-related patterns and two rotation-related patterns; no counting or grouping skill appears in this saved sample.
- Reported SCV values are 0.0500, 0.0667, 0.0667, and 0.0500.
- The reported utility is 0.5622 for each candidate.
- A comparison with a deliberately prohibitive threshold admitted 0 candidates.

The runner `experiments/exp02_skills/run.py` defaults to seed 0, but the saved JSON omits a seed field. It calls `run_skill_pipeline(..., allow_prior_evidence=True)`. The skill pipeline documents these as provisional trials when transfer evidence is absent; therefore the saved promotion count is not evidence that all four became active, validated, useful skills. The legacy artifact does not retain a provisional flag per row, so this property cannot be audited from that JSON alone.

### Interpretation and required evidence

This supports only that a pipeline can map some mined synthetic patterns into skill candidates under its bootstrap path. It does not establish natural semantic emergence, all-four-family emergence, or useful skill birth. `classify_mvp_category` assigns categories using operation-name token heuristics; report this as automatic pipeline formation from known synthetic operation traces, not blind semantic discovery.

A future birth table should contain one row per unique skill birth, with run seed, task/trace split, skill and source-invariant IDs, signature, mapped concept, SCV components, threshold, decision, provisional/active state, birth time, and later held-out outcomes. Count unique semantic skills separately from duplicate signatures and candidate rows.

## 2. SCV statistics

The implementation defines:

`SCV = reuse × abstraction_gain × transfer_score − creation_cost`

(`src/core/skill.py`, `src/skills/trigger.py`). The saved EXP-02 values are all positive but clustered between 0.05 and 0.0667 in one run; the runner also has a 0.0 default threshold and tests a 100.0 rejection threshold. That establishes neither a calibrated threshold nor SCV predictiveness. In particular, the saved strict comparison is a floor/prohibitive control, not the proposed low/medium/high threshold study.

Candidate formation currently estimates reuse partly from frequency and can admit prior transfer/abstraction values. Freeze and record the source of every component as measured, prior, or default. Keep the candidate universe and SCV formula fixed across policy arms. Do not choose a threshold after inspecting confirmatory outcomes.

For EXP-SCT-05, SCV must be recorded at the decision/birth time and tested against outcomes on a later, disjoint task block. Compare it with frequency/IS, expected reuse, abstraction gain, and transfer-prior baselines. Report rank and calibration metrics with uncertainty clustered at the run-seed level. Do not treat correlation with the repository's contemporaneous SU alone as prediction: SCV and SU share components by construction.

## 3. Skill utility results

The legacy EXP-02 artifact reports SU=0.5622 per candidate at admission, but it has no time series or independent post-birth validation. `src/skills/utility_components.py` defines:

`SU = (RCG + TV + CP + RV) − (CC + MC + NR)`

Several terms have birth-time fallbacks: RCG can use abstraction gain, TV can use half the birth transfer score when there is no transfer history, and CP can use the default/category heuristic. RV is derived from observed reuse count. Thus a nonzero birth SU is not equivalent to realized future net value.

For the evidence package, report the full component breakdown at birth and at fixed follow-up checkpoints. Keep a separate held-out realized-value endpoint (e.g. total success-gated reasoning-cost savings and transfer benefit minus the same predeclared creation/maintenance costs). Treat the existing SU as a tracked accounting measure, not as an independent truth label for SCV prediction.

## 4. Reuse statistics

The EXP-02 artifact does not report reuse attempts, eligible opportunities, successful reuses, transfer counts, or reuse-rate denominators. `ReuseEngine.apply` can compare a skill-enabled solve with the same task's baseline and only gives positive reuse/transfer credit when replay succeeds; this is a suitable basis for a paired task-level evaluation, subject to keeping the Phase 13B cost-accounting correction in place.

Report at least:

1. Number of skills born and number with at least one eligible held-out opportunity.
2. Skills used at least once / skills with an eligible opportunity.
3. Successful reuse events / eligible application opportunities.
4. Failed applications, negative transfer, and no-match opportunities.
5. Per-task paired baseline and skill-enabled cost and accuracy.

Also show the requested simple `reused skills / created skills` ratio, but do not use it alone: a skill with no opportunity must not be conflated with an eligible skill that was never selected. Define eligibility from task requirements before observing whether retrieval applies the skill.

## 5. Composition results

There is no Phase 13C composition result package. Composition models, triggers, candidate evaluation, utility, and lifecycle exist in `src/skills/composition/`, with unit/e2e tests. Those demonstrate software paths, not empirically learned composition utility.

Important validity condition: `ComposeOutcome` in `src/skills/composition/compose.py` can supply a prefilled success, transfer gain, and reasoning reduction. A confirmatory composition run must derive these from actual task execution against a paired baseline; it must not pass a constant synthetic success outcome and then report it as learned capability. For reflection-plus-counting, construct held-out tasks that require both operations, compare no-skill, either single skill, and the ordered two-skill composition, and measure exact correctness, cost, transfer, and composition cost. Use analogous blinded task splits for multi-skill composition and composition reuse.

## 6. SCT baseline comparisons

Relevant baseline code exists, but it is not yet a fair Phase 13C comparison package:

- `baselines/skill_storage/run.py` creates skills from every mined candidate and skips SCV; this can inform an always-store/always-create arm if its candidate pool and task stream are matched.
- `baselines/random_skill_creation/run.py` creates arbitrary random triggers and utility values; it does **not** randomize the same eligible candidates under a matched creation budget, so it is not by itself a fair primary SCT comparator.
- A no-learning/no-skill arm exists in the broader experiment suite, but it needs to retain the same discovery/memory pipeline if the comparison is intended to isolate skill creation.
- No current arm cleanly implements the requested memory-only condition as trace/example retrieval without executable skill creation.

Before running, freeze a common candidate universe, task stream, library capacity, and cost accounting. Proposed arms:

| Arm | Skill creation policy | Required control |
|---|---|---|
| SCT | Create iff the frozen SCV rule passes | Primary treatment |
| Never-create | Discover/store the same invariants, but create no executable skills | Isolates skill creation from discovery/memory |
| Always-create | Create every candidate that passed the same non-SCV eligibility/validation gate | Bypasses only the economic decision, not candidate quality |
| Random-create | Randomly select from that same eligible pool | Match SCT's creation budget using calibration data, then freeze the rule/seeded policy |
| Memory-only | Retain/retrieve traces or invariant exemplars, but create no executable skills | Must be a genuine non-skill memory baseline; do not relabel skill storage |

The main outcome should be paired held-out net benefit per run/task block and the SCT-minus-each-control contrast. Report skill count/library size and creation/maintenance cost as well as utility; “skill explosion” is a measured outcome, not an assumed one.

## 7. SCT ablation results

There are no Phase 13C ablation results yet. Freeze ablations as matched counterfactuals on the same candidate/task streams:

- **No-SCV:** bypass the SCV decision while preserving other candidate filters and execution.
- **No-lifecycle:** keep birth/retrieval fixed, disable dormancy/retirement/reactivation updates, and report accumulated library size and maintenance cost.
- **No-composition:** preserve individual skill creation/reuse, but disable composition proposals and composition bonuses.

Do not interpret an ablation unless the disabled component is the only intervention and all other random seeds, candidates, task exposures, and costs remain paired. Include composition ablation only for outcomes where composition is available to the treatment.

## Design choices resolved for protocol v1

The user selected (1) to include expected maintenance in the birth gate, (2) to charge maintenance per eligible opportunity over a ten-opportunity horizon, and (3) to freeze 0.06 per opportunity as the primary simulator-cost assumption with sensitivity reporting. Protocol v1 uses a Phase-13C-specific score while leaving the global SCV function and EXP-02/Phase 13B/EXP-IDT-14 records untouched. The 0.06 value is a code-derived modeling assumption, not an empirical compute-cost estimate. The full formula, thresholds, arms, endpoints, and seed split are in `phase_13c_preregistration_v1.md`; machine-readable choices are mirrored in `configs/phase13c_sct_v1.yaml`.

**Before running:** implement the Phase-13C-only score and seed-split config, then contract-test the explicit `[0,1]` mapping for p-reuse, AG, and TS and the 10-opportunity cost accounting. If the runner cannot preserve these definitions, stop and version the protocol before opening confirmatory seeds. Legacy EXP-02 numbers remain preliminary for their earlier score definition and must not be pooled with v1.

## Preregistration controls

The proposed split is calibration seeds `[15,16,17,18,19]` and confirmatory seeds `[20,21,22,23,24,25,26,27,28,29]`; current saved experiment JSON records list seeds 0–4 and 10–14. Use calibration only for the predeclared calibration procedures, and keep the confirmation block unopened until all calibration-derived values/configuration are saved. Do not recycle Phase 13B/EXP-IDT-14 outcomes as Phase 13C confirmation.
2. Freeze the candidate eligibility gate and the source/units of SCV inputs; preserve provisional vs validated/active distinctions.
3. Freeze the held-out opportunity definition, task order, output-cost accounting, success criterion, utility horizon, maintenance-cost schedule, and all control arms.
4. Predeclare one primary endpoint and smallest effect of interest before observing confirmation results. Keep the user-proposed SCV, SU, reuse, TS, AG, CU, lifecycle, and composition measures as separately named secondary outcomes.
5. Use paired per-task outcomes and seed-level aggregation; report n, mean, SD, 95% CI, effect sizes, and failures. Keep unsuccessful skills and null results in the package.
6. Validate that the confirmation runner cannot accidentally execute during unit tests; use stubs for aggregation tests, as done for the corrected EXP-IDT-14 aggregation test.
7. Produce the requested seven deliverables as distinct evidence sections: emergence table; SCV statistics/predictiveness; utility trajectory and realized value; reuse/opportunity statistics; composition outcomes; matched SCT baselines; matched ablations.

## Current disposition of the seven requested deliverables

| Requested item | Current status | What can be defended now |
|---|---|---|
| Skill emergence results | Preliminary only | Four candidate promotions are in one legacy run; the runner uses prior-enabled admission; no all-four-family or validated active-skill claim |
| SCV statistics | One-run descriptive values | Four reported SCVs, no threshold calibration and no held-out prediction test |
| Skill utility results | Birth-time report only | Four SU values reported; no realized future utility trajectory |
| Reuse statistics | Not available in EXP-02 artifact | Code can record success-gated reuse; no Phase 13C opportunity denominator/results |
| Composition results | No experiment results | Implementation and tests exist; task-grounded outcome measurement remains required |
| SCT baseline comparisons | Not available as a matched Phase 13C package | Existing baselines need matched candidate pools, discovery, exposure, and budget |
| SCT ablation results | Not available | Matched SCT/no-SCV, lifecycle, and composition ablations remain to be run |

**Gate:** Phase 13C is in preflight, not validated. The seven evidence items are requirements for the future evidence package; this audit does not claim them as results. Phase 13B remains a separate failed gate. No thresholds, metric definitions, original `synthetic-v1` evidence, or EXP-IDT-14 results were modified by this preflight.
