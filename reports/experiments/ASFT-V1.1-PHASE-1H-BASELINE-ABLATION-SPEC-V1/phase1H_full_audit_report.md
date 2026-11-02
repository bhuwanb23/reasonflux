# ASFT v1.1 Phase 1H — Full Audit and Governance Specification

**Phase:** `ASFT-V1.1-PHASE-1H-BASELINE-ABLATION-SPEC-V1`  
**Purpose:** freeze who ASFT must beat, which components must be ablatable, what constitutes a fair/active comparison, and how outcomes may be interpreted.  
**RQ:** Not applicable — cross-phase governance phase.

## 1. Executive decision

- **Specification layer: PASS.** Baseline registry, ablation map, fairness, comparator activation, attribution, outcome response, and governance rules are documented.
- **Contract layer: PASS, 50/50 checks.** The outcome logic supports ASFT win/tie/loss, unavailable, fairness failure, identical-decision non-informativeness, and positive/no-measurable/negative/unavailable ablation results.
- **Empirical execution: BLOCKED.** This phase generated no task, baseline, ablation, or confirmatory outcomes.
- **RQ: not applicable.** Phase 1H governs other phases; it does not test whether ASFT or any component works.

## 2. Historical audit

Phase 14F's synthesis is the baseline evidence source. Corrected 13B informed ranking ties frequency-only and no-transfer at mean top-k transfer utility `.0958085`; random-pattern is lower at `.0631134`. The pre-correction informed-arm value `.143130` is kept separate; the tie and failed strict all-control gate remain. Phase 13C net value is SCT `.345`, ALWAYS_CREATE `.345`, RANDOM_CREATE `.345`, NEVER_CREATE `0`, MEMORY_ONLY `1.325`; all 44 candidates were selected and random-create probability was 1.0. MEMORY_ONLY attempted 440 opportunities versus SCT 223, so net value combines opportunity frequency and correctness. It is raw trace-exemplar/macro-operation reuse, not exact full-solution replay or a skill store.

Corrected 13D ASFT is ahead of B1/B2/B3 transfer utility but `−.001091` versus B4 compression proxy, so its all-baseline gate fails. In 13E, ASFT passes B2/B3/B4 under a joint internal C_t/task-utility rule but loses task utility to B1; C_t is not independent capability. In 13F, the joint task-utility/CGR gate passes B2/B4, fails B1, and ties B3; ASFT/no-SCV/random-SCV share the same four-candidate set. In 13G all five arms tie at 1/200 holdout exact accuracy, but no invariant/skill/capability chain activated; budget mismatch and same-holdout reuse undermine a clean mechanism contrast.

**Cross-phase boundary:** comparator names, implementations, opportunities, pools, and outcomes differ. Never pool 13C MEMORY_ONLY, 13D memory, 13E skill storage, 13F B2, and 13G nearest-episode retrieval; never average non-equivalent endpoints into an overall “ASFT wins.” The detailed audit is `baseline_audit.md`.

## 3. Frozen comparator and ablation registry

Baseline taxonomy B1–B7 covers no-learning, memory/retrieval, random, frequency, compression, heuristic/hybrid, and oracle analysis. Mandatory BL1–BL7 instantiate no-learning, memory, random, frequency, compression, hybrid memory+frequency, and oracle. Oracle is analysis-only. Baselines are versioned at the implementation-subtype level; a label alone is not a comparable method.

A1–A9 cover no IDT, no SCT, no SCV, no transfer, no capability layer, no lifecycle, no composition, no memory, and no ARC extension. Claim mapping, manipulation checks, controls, and local interpretation boundaries are specified. The framework permits an ablation to change nothing; it also permits the ablation to improve outcomes or be unavailable.

## 4. Fairness and attribution

A direct comparison checks same tasks/splits, common candidates where ranking is tested, same candidate/query budgets, storage/compute caps, horizon/exposure, evaluator, and config/runtime parity. Actual eligible/offered/selected/attempted/completed/failed counts are recorded; per-eligible and per-attempt outcomes are shown separately. If candidate pools or opportunities differ, the direct comparison is invalid/unmatched or requires separate common-support and natural-system analyses.

A mechanism attribution requires a frozen claim/endpoint, fair comparator, verified manipulation, actual activation/decision divergence, paired/randomized contrast at the independent unit, relevant surviving alternatives, and appropriate uncertainty/replication. If all comparators make identical decisions, a ranking/selection comparison is explicitly **non-informative**, even if a performance number is available. If an ablated component never activates, the removal test is not a null contribution result.

## 5. Decision and interpretation rules

Positive effect is defined as ASFT minus comparator. A win requires the lower confidence bound to exceed the frozen SOI; baseline win is the reverse; equivalence tie requires the interval wholly within the SOI region; otherwise inconclusive. Fairness failure or no activation blocks attribution. For ablations, positive `full − ablated` supports local contribution only; equivalence is no measurable contribution only if removal is verified, the component is exercised, and precision is adequate; a negative effect means ablation is better under tested conditions.

Frozen interpretation rules include: tie is not validation; unavailable is not zero; a metric increase is not theory validation; synthetic success is not external validity; an ablation is not universal necessity; an oracle is not a deployable competitor; phase-specific metrics are not pooled; and a proximate cause is not a proven root cause.

## 6. Outcome-response and contract scope

The 50 contracts verify taxonomy completeness, required baselines/ablations, fairness pass/fail/unavailable, activation divergence/degeneracy, win/tie/loss/inconclusive/unavailable paths, positive/no-measurable/negative ablation effects, and governance failures. The fixture values are constructed unit-test inputs, not outcome evidence. They were not chosen from predictor rankings and do not encode an empirical winner.

The contracts do not implement baselines, ablations, task runners, candidate assignment, randomized interventions, or future experiment-specific registries. Those must be populated and validated in each phase's preregistration before outcome access.

## 7. Governance and readiness

Every experiment freezes baseline IDs/versions, ablations, budgets, candidate pools, splits, endpoints, SOIs, decision rules, activation metrics, and interpretation rules before outcomes. Any post-outcome change is a new version requiring disjoint confirmatory evidence; it cannot rescue the original result. Amendments before outcome access must be dated, justified, and versioned.

## 8. Bottom line

> The framework permits ASFT components to show positive contribution, no measurable contribution, negative contribution, or unavailable contribution under specified conditions, and does not interpret component existence as evidence of component necessity. Baseline/ablation governance is specified and contract-tested; scientific mechanism superiority remains untested by Phase 1H.