# Phase 1H.7 — Comparator Activation and Divergence Audit

## Required measurements

Before interpreting a ranking/selection or ablation result, record:

- common candidate-pool ID/hash and candidates eligible per arm;
- complete rank orders, selected sets, action/decision vectors, tie rules, and decision horizons;
- eligible, offered, selected, attempted, completed, and successful opportunity counts;
- selection/activation rate per arm and candidate/task overlap;
- pairwise rank correlation, top-k/set overlap, and **decision divergence rate** on common opportunities;
- budget, storage, compute, and evaluator parity; and
- whether the ablated component was actually exercised and disabled.

## Decision-divergence rule

If two or more comparators make **identical decisions on every common eligible opportunity**, the selection comparison is `non_informative_identical_decisions`. Report the performance data descriptively, but do not claim a ranking/selection mechanism win. If rank orders differ but the selected set is identical for the frozen top-k policy, the top-k comparison remains non-informative for the selected-set claim; report rank-order differences as secondary only.

If pools or opportunity counts differ, classify the direct contrast `unmatched_candidate_pool` or `unmatched_opportunities`; it cannot establish clean decision attribution. If no eligible opportunity exists, activation is `unavailable`, not zero success. For ablations, a manipulation that never fires is unavailable/non-informative rather than “no contribution.”

## Historical degeneracy checks

- **13B:** transfer-aware, frequency-only, and no-transfer rank orders were the same across saved seeds; random pattern differed. The primary transfer-aware ranking advantage is not demonstrated.
- **13C:** 44/44 candidates were selected; SCT, ALWAYS_CREATE, and RANDOM_CREATE made the same choices because random-create probability was 1.0. Selection superiority was not tested by differentiated actions.
- **13F:** ASFT, no-SCV, and random-SCV each construct four items from a common four-item pool; primary outcomes tie exactly. This is a non-informative SCV selection comparison in that pool, not evidence for SCV.
- **13G:** all five arms have identical 1/200 holdout accuracy, but low coverage prevented the mechanism chain from activating; a budget mismatch and reused holdout further limit interpretation. This is not evidence that all ARC mechanisms are equivalent.

## Contract statuses

The framework distinguishes `informative_decision_divergence`, `non_informative_identical_decisions`, `unmatched_candidate_pool`, `unmatched_opportunities`, `unmatched_decision_horizon`, and `unavailable`. Only a fair, active, divergent comparison may enter the ordinary win/tie/loss decision rule for mechanism attribution.