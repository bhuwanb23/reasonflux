# ASFT v1.1 Phase 1E — Full Audit and Specification Report

**Phase:** `ASFT-V1.1-PHASE-1E-CAPABILITY-VALIDATION-SPEC-V1`  
**Research question RQ4:** Does a capability measure predict future performance on independently measured tasks beyond simpler explanations?  
**Report status:** specification and contract review; not an empirical benchmark report.

## 1. Decision

- **Specification layer: PASS.** Required behavioral construct, battery, comparator, endpoint, split, and preregistration rules are documented.
- **Contract layer: PASS, 31/31 checks.** Function/schema boundaries and outcome-response logic pass the implemented contract tests.
- **Empirical execution: BLOCKED.** Task/evaluator implementation, sample-size freeze, confirmatory locks, independent gold store, and run authorization/readiness are not complete.
- **RQ4: UNTESTED.** No Phase 1E task battery or predictive model outcomes exist.

## 2. Historical audit and interpretive boundary

Phase 13E's ten-seed synthetic cohort showed C_t monotonicity in 10/10 seeds, mean C_t `1.0227`, mean CGR `0.2946` (95% CI `[0.2857,0.3036]`), and one persistent `cap-cross-domain` object. The object count remained one at every measured round after formation; subsequent new capability count was zero. Thus the score increased while capability count did not. No accepted higher-order capability emergence was observed.

Phase 13E's preregistered C_t-at-round-t to next-round task utility association was positive but very small (`r=.0498`, seed-cluster bootstrap CI `[.0163,.0922]`, 10 clusters/30 round pairs). It is a same-generator internal-cohort association, not external behavioral validation or a causal estimate. Keep it distinct from TS→CGR (`r=−.5027`, CI `[−.8601,.1857]`), which did not establish that transfer drove growth. Phase 13D corrected mean CGR was `−.060` over nine evaluable seeds; do not pool the two synthetic contexts.

Phase 14E's critical review treats CGM computation as available but robust capability growth, transfer-driven growth, higher-order emergence, and intelligence construct validity as unestablished. Phase 14H locates the first major causal evidence break at transfer→capability growth and notes capability→intelligence is also unsupported. Phase 14J concludes the full ASFT causal chain is not validated. Phase 13F's task-utility contrasts were comparator/endpoint-specific: ASFT failed B1 and B3 but passed B2 and B4 under that protocol. This is narrow synthetic evidence, not an external capability test.

**Historical conclusion:** positive internal metric movement is real within Phase 13E's frozen cohort, but it does not show external breadth, durable transfer, task capability growth, or intelligence growth. Phase 1E is designed to measure those behavioral outcomes independently.

## 3. Phase 1E construct and target

Capability is a persistent, generalizable behavioral competence with measurable positive utility on unseen tasks. It must be externally scored, persist after delay, generalize over held-out variants, and transfer when the subtype claim requires it. C1–C6 are independently tested: single-skill, multi-skill, transfer, compositional, adaptive, and cross-domain behavior.

The battery's six outcomes are A novel task success, B transfer success, C task breadth, D retention, E composition, and F adaptation. The target External Behavioral Capability Score (EBCS) is their equal-weight macro-average; raw components and denominators remain visible. The evaluator uses task outputs and gold/rubric only. If the target cannot be computed with the CGM module absent, the benchmark fails construct separation.

The growth endpoint is `ΔEBCS = EBCS_future − EBCS_disjoint_baseline`, complemented by the change in validated task-family breadth. C_t/CGR/IG, capability-object count, and internal skill utility do not enter that target, capability labels, or success rules.

## 4. RQ4 comparator and analysis plan

Primary candidate predictor is CGR_t, frozen at time t. Simple baselines are B1 past performance on disjoint prior tasks; B2 experience count; B3 independently probed memory retrieval precision/coverage; B4 training-only frequency/reuse statistics; and B5 recency of the last related success. Primary model M0 combines B1–B5; M1 adds CGR_t. The endpoint is future EBCS and the primary estimand is out-of-sample `ΔMAE = MAE(M0) − MAE(M1)`. The planned SOI is `+0.02` EBCS MAE reduction. A positive slope is required for the interpretation that higher CGR predicts more future behavioral capability.

The result can be a meaningful metric win, an equivalence tie, a loss/inverse direction, inconclusive, or unavailable. A tie supports no practically meaningful incremental value for CGR within the defined target/population/range, not a universal claim that CGR is useless. M0 versus M1 directly permits simpler variables to account for or outperform CGR. C_t and IG/IGR comparisons remain secondary unless separately preregistered with multiplicity control.

## 5. Data integrity and test design

Development, confirmatory, and replication splits are separated by task families/templates, seeds, and where possible domains. Future tasks and gold labels are unseen at time t and absent from the memory store. Predictor features use prior data only. Test outputs and EBCS are computed, hashed, and locked before joining predictor snapshots. All arms receive the same tasks and fixed query/context/compute budgets. The independent unit is the agent-run/task-family-seed panel; task items and repeated rounds are nested.

The preregistration template requires exact N from calibration-only power/precision simulation, feature/model definitions, SOI, interval method, split hashes, task/evaluator versions, outcome lock, missingness, budgets, and replication rules. Those run-specific fields are intentionally blank pending implementation and calibration.

## 6. Contract scope and outcome-response check

`experiments/phase1e/run_contracts.py` returned **31/31 PASS**. It verifies six declared behavioral tests, six taxonomy labels, presence of required baseline variables, behavior-only scorer signatures, rejection of CGR/C_t/IG-family fields in outcome payloads, behavior-derived capability gate cases, and all decision statuses.

The outcome-response CSV uses five constructed intervals to exercise win, tie, loss, inconclusive, and unavailable code paths. These are code fixtures only. They contain no task outcomes, no estimated predictor values, and no scientific evidence about the metric.

The contract scope is limited: no production task generator, sealed gold store, full leak-proof process, predictive model, or capability battery is implemented. Interface checks do not guarantee a downstream production pipeline cannot bypass them. That needs a separate system-level test before empirical execution.

## 7. Outstanding gates and authorization

1. Implement and independently review the behavior-only task generator, A–F evaluation, task rubrics, and same-budget runner.
2. Prove target scoring works with CGM dependencies removed; establish sealed independent gold storage and access logging.
3. Run development-only calibration; freeze thresholds, costs, predictor definitions, models, SOI, missingness, and exact panel N.
4. Freeze and hash confirmatory and replication manifests; verify no future-task exposure or near-duplicate leakage.
5. Complete sample-size/precision analysis, model validation, budget audit, and independent preregistration review before outcome access.
6. Obtain explicit authorization for any empirical phase. This package does not authorize Phase 3/IDT or SCT experiments.

## 8. Bottom line

> Phase 1E now has a behavior-only capability definition, independent A–F battery specification, comparator framework, primary endpoint/decision rule, split and preregistration protocols, and 30 passing interface/decision contracts. The design can conclude that CGR wins, ties, loses, or is unavailable. No external behavior outcomes have been collected, so capability growth and RQ4 remain untested.