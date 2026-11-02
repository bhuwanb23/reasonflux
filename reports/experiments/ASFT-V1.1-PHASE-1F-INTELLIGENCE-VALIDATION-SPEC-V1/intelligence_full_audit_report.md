# ASFT v1.1 Phase 1F — Full Audit and Specification Report

**Phase:** `ASFT-V1.1-PHASE-1F-INTELLIGENCE-VALIDATION-SPEC-V1`  
**Primary question RQ5:** Do IG and IGR predict independently measured future learning, adaptation, or competence acquisition beyond simpler baseline explanations?  
**Report type:** historical audit + specification + contract-layer readiness. This is not an empirical result.

## 1. Executive decision

- **Specification layer: PASS.** The intelligence construct, independent A–F battery, comparator set, primary endpoint, decision rules, splits, preregistration, and retirement path are specified.
- **Contract layer: PASS, 44/44 checks.** Final count matches `phase1F_contract_test_results.csv`.
- **Empirical execution: BLOCKED.** No Phase 1F task battery, task generator, evaluator, confirmatory outcomes, or replication outcomes have been run.
- **RQ5: UNTESTED.** Nothing in the contract fixtures establishes that IG predicts an external outcome.

## 2. Historical audit: what IG did and did not measure

Phase 13E's frozen formula is `IG=.35*CGR+.25*TG+.20*UG+.15*CCG+.05*CompG`; IGR is round-to-round IG difference; IE is IG divided by experience count (32 discovery traces plus cumulative held-out tasks). Across ten synthetic seeds, mean IG was `0.2294` (95% CI `[0.2245,0.2343]`), mean IGR `0.00904` (`[0.00903,0.00906]`), and mean IE `0.0043` (`[0.0041,0.0044]`). The mean IE OLS slope was negative at `−0.00394` (95% CI `[−0.00421,−0.00367]`). Round-average IG/IGR trajectories were non-monotone, and the initial zero-state transition is influential.

These are formula outputs: the components are internal CGR, transfer, utility, capability coverage, and composition quantities. They show that the pipeline computes the score and that it moved positively on average in this cohort. They do not independently measure learning speed, adaptation, generalization, knowledge efficiency, or future competence acquisition.

Phase 14E says computability is supported but intelligence construct validity is not. Phase 14H says the capability-to-intelligence link is unvalidated. Phase 14I identifies construct validity as high risk and critical for intelligence-growth claims. Phase 14J concludes that IG/IGR/IE do not establish intelligence growth. The v1.0 composite criticism therefore remains a live validity threat. Phase 1F responds by defining and scoring task behavior first.

## 3. Frozen construct and independent targets

Intelligence is operationalized here as externally observable acquisition of future competence, adaptation to task shifts, generalization/transfer to unseen instances/domains, and persistence/relearning under fixed budgets. The I1–I6 taxonomy is reported dimension-by-dimension, not collapsed into IG or another newly invented intelligence scalar.

The battery has six independent targets: A future learning rate, B adaptation speed, C novel-environment success, D few-shot/compositional acquisition, E cross-domain learning, and F generalization retention/relearning. Test A normalized learning-curve AULC at examples `[0,1,3,5]` is the sole primary endpoint. The target is computed from outputs, independent gold/rubrics, exposure and resource logs only. If it cannot be computed with IG disabled, the benchmark fails.

**Q1: Can intelligence be measured without IG? Yes, by specification.** The API contracts reject IG/IGR/IE/CGR/C_t/capability/internal transfer fields from outcome payloads. This is not production security evidence: task generation, a sealed gold store, production solver, and the full metric-disabled execution pipeline remain unimplemented.

## 4. Comparator and RQ5 analysis

Primary predictor is frozen `IG_t`; `IGR_t` is a preregistered key-secondary predictor with Holm adjustment, while IE remains exploratory. IGR cannot replace or rescue a failed IG primary claim. The required comparator set includes past performance, experience count, capability score (legacy C_t separated from behavior-based prior competence), memory strength, and transfer metrics (legacy TS separated from external prior transfer). A chance/random policy baseline and within-split IG permutation baseline are also specified.

Primary M0 contains B1–B5; M1 adds IG_t. Primary estimand is out-of-sample `ΔMAE=MAE(M0)−MAE(M1)` for Test A AULC. The design SOI is `+0.02` on the normalized endpoint, with a positive IG slope required. A result may be a win, equivalent tie, loss/inverse direction, inconclusive, or unavailable. The intelligence label survives only with primary and additional independent endpoint replication; equivalence/loss across the external battery can trigger retirement.

## 5. Retirement commitment

The benchmark is expressly designed to allow rejection. If adequately powered confirmatory and independent replication cohorts show equivalent ties or losses across A–F, with no replicated external win, retire “IG measures intelligence/intelligence growth” for the tested scope and rename IG as an **Internal Growth Composite** (or equivalent non-construct label). Preserve the formula only as bookkeeping/diagnostic. Underpowered nulls or integrity failures are inconclusive/unavailable, not retirement evidence.

> The benchmark is designed to allow IG to be rejected as an intelligence measure if it provides no predictive value beyond capability, experience, memory, transfer, or prior performance.

## 6. Contract scope and outcome-response audit

The contract runner returned **44/44 PASS** for behavior-only function signatures, rejection of internal metric fields, normalized AULC arithmetic, required baseline presence, result branches, and claim survival/retirement status logic. Constructed intervals are code-path fixtures only; they were not derived from predictor ranks, task outcomes, or model fits. They demonstrate that logic can label IG win/tie/loss/inconclusive/unavailable and that the retirement branch is reachable; they provide zero evidence about IG's actual performance.

The contract layer does not build tasks, score live solver outputs, seal gold, fit M0/M1, select sample size, or run replication. These remain separate empirical-readiness gates.

## 7. Readiness gates and authorization

1. Implement A–F generators, rubrics, evaluators, fixed-example learning curves, shifts, and random/no-learning controls.
2. Demonstrate scoring with IG code absent and audit the production pipeline for shared-state, task-selection, budget, and gold leakage.
3. Run development-only calibration; freeze B1–B5, M0/M1, endpoint/SOIs, multiplicity, missingness, resource budgets, and exact independent N.
4. Hash disjoint confirmatory/replication manifests; test future-task and near-duplicate exclusion.
5. Lock preregistration, sealed gold, outcome scoring, and predictor-join order before confirmatory data access.
6. Obtain explicit empirical authorization/readiness. This package does not authorize Phase 3/IDT or SCT experiments.

## 8. Bottom line

> Phase 1F can test IG against independent future learning and adaptation behavior, challenge it against prior performance, exposure, capability, memory, and transfer, and retire the intelligence label if replicated equivalence/loss is found. It cannot currently tell us whether IG is intelligence. No external task outcomes exist; RQ5 remains untested.