# Phase 1H.6 — Fairness Framework

## Equality requirements

For a direct policy/mechanism contrast, competitors must share:

1. **Tasks and splits:** same task IDs, order/randomization plan, train/test labels, family strata, and evaluator.
2. **Candidate pool:** common eligible candidates for ranking/selection tests. If candidate generation differs by design, run a common-pool policy test and a separate natural-system test; never describe different pools as a clean ranking comparison.
3. **Budget:** identical candidate/query/attempt caps, wall time, token/compute limits, and stopping rules; runtime counters must match the preregistered config. Report actual use as well as caps.
4. **Storage/memory:** same capacity, access window, persistence horizon, retrieval-query cap, and data visibility. The memory mechanism itself may differ, but the opportunity/capacity boundary does not.
5. **Compute:** same hardware/model/tool access and compute cap; disclose if actual consumption differs.
6. **Horizon/exposure:** same number and schedule of training episodes, demonstrations, updates, eligible test opportunities, and rounds. BL1 receives the same task/input stream but cannot update its learned state.
7. **Evaluation:** same held-out queries, gold, partial-credit rubric, success/cost conversion, and blinding.
8. **Integrity:** config and code hashes locked before outcomes; no test-label leakage, holdout reuse, outcome-driven exclusions, or silent defaults.

## Opportunity denominators

Report, per arm: eligible candidates/tasks, offered opportunities, queried, selected, attempted, completed, correct, failed, no-match/abstained, and resource use. Show intention-to-treat per eligible opportunity and conditional per-attempt performance separately. Unequal attempts may be a policy effect, but a net-value gap alone cannot isolate application quality from application frequency. Do not delete no-match or failed opportunities from the primary denominator unless preregistered.

## Non-identical mechanisms

Some comparators cannot have identical internal state (e.g. memory versus no-memory). Equality means same **caps, task information, opportunities, and access rules**, not identical state. For a selection claim, the candidate pool must match. For a system-level claim, report both matched-component contrast and full-system contrast when feasible.

## Integrity gate

A known mismatch in tasks, candidate pool, budgets, storage/compute caps, horizon, exposure, evaluator, or config/runtime parity yields `comparison_invalid` or `unavailable` before considering favorable effect estimates. A beautiful score difference cannot repair an unfair comparison.