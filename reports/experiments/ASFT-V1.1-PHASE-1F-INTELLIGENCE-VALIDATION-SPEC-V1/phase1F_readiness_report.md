# ASFT v1.1 Phase 1F — Readiness Report

**Phase ID:** `ASFT-V1.1-PHASE-1F`  
**Package:** `ASFT-V1.1-PHASE-1F-INTELLIGENCE-VALIDATION-SPEC-V1`  
**RQ5:** Do IG and IGR predict independently measured future learning, adaptation, or competence acquisition beyond simpler baseline explanations?

## Executive decision

- **PASS for specification layer.**
- **PASS for contract layer — 44/44 checks.**
- **BLOCKED for empirical execution.**
- **RQ5 untested.**

No Phase 1F learning/adaptation battery, task generator, or confirmatory/replication outcome has been run. Any win/tie/loss inputs in the contract artifacts are constructed code-path fixtures, not task evidence.

## Historical intelligence audit

Phase 13E computed the frozen internal composite `IG=.35*CGR+.25*TG+.20*UG+.15*CCG+.05*CompG`; IGR is its round difference; IE is IG divided by cumulative experiences. In ten synthetic seeds, mean IG was `0.2294` (95% CI `[0.2245,0.2343]`), mean IGR `0.00904` (`[0.00903,0.00906]`), and mean IE `0.0043` (`[0.0041,0.0044]`). The IE OLS slope was negative: `−0.00394` (95% CI `[−0.00421,−0.00367]`). Round trajectories were non-monotone and include an initial zero-state jump.

Phase 14E concluded that the formula is computable, but no independent intelligence criterion validated the construct. Phase 14H marked Capability Growth→Intelligence Growth unvalidated. Phase 14I rated construct validity high-risk and critical for intelligence-growth claims. Phase 14J classified “IG measures intelligence growth” as not established. These sources support the concern that IG may be an internal composite; they do not show that any independent learning/adaptation outcome is predicted.

## Definition and target independence

The frozen benchmark definition is external capacity to acquire future competence efficiently, adapt to shifts, generalize/transfer to unseen tasks/domains, and retain or reacquire learning under fixed budgets. It is not a definition in terms of IG. The A–F battery measures learning rate, adaptation speed, novel-environment success, few-shot acquisition, cross-domain learning, and generalization retention.

**Can intelligence be measured without IG? YES, by design.** Task outputs are scored against independent gold/rubrics; the AULC, adaptation, transfer, and retention outcomes use behavior and exposure/resource logs only. The target schema rejects IG, IGR, IE, CGR, C_t, capability scores, and internal transfer scores. Current contracts check APIs/schemas; production-level removal of IG and sealed-gold verification remain gates.

## Comparator and decision framework

Primary predictor is frozen `IG_t`; `IGR_t` is a separately preregistered key-secondary predictor with Holm adjustment, and IE remains exploratory. M0 contains past performance, experience count, capability score (legacy C_t and behavior-based prior capability kept separate), memory strength, and transfer metrics. M1 adds IG. A fixed chance/random baseline and within-split IG permutations are also specified. The primary endpoint is Test A future-learning normalized AULC at exposures `[0,1,3,5]`; the primary comparison is held-out `MAE(M0)−MAE(M1)` with SOI `+0.02` and a positive IG slope. The result logic permits IG win, equivalent tie, loss/inverse direction, inconclusive, or unavailable.

## Retirement commitment

IG survives only with replicated positive incremental prediction on primary future learning plus at least one independent transfer/generalization/adaptation outcome. If adequately powered confirmatory and replication cohorts show equivalent ties or losses across A–F, with no replicated external win, retire the intelligence/intelligence-growth label and rename the formula as an internal growth composite. Underpowered or integrity-failed nulls are inconclusive/unavailable, not evidence of retirement.

## Readiness gates

| Gate | Status | Evidence / outstanding work |
|---|---|---|
| Gate 1 — Contracts | **PASS, interface scope** | 44/44 interface, schema, AULC, outcome-response, and retirement-path contracts; no battery outcomes. |
| Gate 2 — Independent battery | **SPECIFIED; NOT IMPLEMENTED** | A–F behavior-only tests; no task runner/evaluator yet. |
| Gate 3 — Task generators and controls | **PENDING** | Need independent future tasks, rule/distribution shifts, novel domains, and matched random/no-learning controls. |
| Gate 4 — Sample size | **PENDING** | Cluster-level precision/power simulation; exact N must be frozen before confirmation. |
| Gate 5 — Frozen analysis | **PENDING** | Freeze feature derivations, M0/M1, SOIs, multiplicity, missingness, and intervals. |
| Gate 6 — Replication | **SPECIFIED; NOT GENERATED** | Disjoint task-family/template/seeds and preferably domains. |
| Gate 7 — Construct validation | **PENDING** | Prove target scoring and task selection work with IG module absent; production leakage/sealed-gold audit. |
| Gate 8 — Retirement review | **SPECIFIED; NOT EXECUTED** | Precommitted survival, weakening, and retirement rules; no empirical IG status yet. |
| Confirmatory authorization | **BLOCKED** | Readiness gates and separate authorization required; this package does not unlock Phase 3/IDT or SCT. |

## Final decision

> Phase 1F is a behavior-first intelligence-validation specification with an explicit path to reject IG as an intelligence measure. It does not validate IG. RQ5 remains untested until independent outcomes, adequate sample size, locked analysis, system-level construct separation, and replication are completed.