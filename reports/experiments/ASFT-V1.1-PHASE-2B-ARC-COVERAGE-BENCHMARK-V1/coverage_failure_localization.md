# Phase 2B.7 — Coverage Failure Localization

## Observed stage cascade

| Stage | Budgeted | Fullscan | Localized observation |
|---|---:|---:|---|
| C1: exact demo fit within condition | 2/1,000 | 10/1,000 | Sparse found-fit coverage even under all ten programs; eight additional fits appear only when budget expands from three to ten. |
| C2: trace record generated | 1,000/1,000 | 1,000/1,000 | A search attempt/no-fit record was generated for every task; this is not a successful-trace claim. |
| C3: independently successful trace | 2/1,000 | 10/1,000 | Success equals exact demo fit under each mode; no separate trace-success loss after fit. |
| C4: invariant candidate available | 0/1,000 | 0/1,000 | Actual TraceMiner emitted none; discovery support is one per signature (budgeted) or three signatures at one each (fullscan), below support 5. |
| C5: skill candidate | 0 reached | 0 reached | Not run; no C4 candidate. |
| C6: transfer eligible | 0 reached | 0 reached | Not run; no skill pool. Conditional rate has zero denominator. |
| C7: capability eligible | 0 reached | 0 reached | Not run; no validated reusable skills/transfer pool. Conditional rate has zero denominator. |

## Classification

**Observed pattern: F5 — mixed. Causal/root-cause attribution: F6 — unresolved.**

The observed pipeline contains (a) very low bounded demo-fit yield, (b) eight additional fits exposed by diagnostic expansion from three to ten candidates, and (c) no repeated discovery signature sufficient for the frozen invariant support gate. These are multiple measured attrition points. The matched budget contrast supports a search-budget effect on found demo fits under this representation. Sparse fullscan coverage is consistent with a representation/parameterization limitation, but without an alternative representation it does not isolate a representation cause. The support gate is the immediate reason C4 remains empty; whether that threshold is appropriate is not tested here.

## What cannot be concluded

- No evidence establishes that representation is the unique or primary cause of low ARC performance.
- No downstream skill, transfer, capability, or intelligence mechanism was tested because the upstream pool was empty.
- A zero C5–C7 reached count is not a negative efficacy result; these stages were blocked/not run. Conditional downstream rates are `not_estimable`.
- No test accuracy, hidden-label result, leaderboard evidence, or confirmatory theory conclusion is reported.

The next informative step is a preregistered matched representation × search study with an independent high-coverage plumbing control and a sealed, test-label-blind coverage runner. It must preserve the threshold or vary it as an explicit factor rather than tuning it after seeing these outcomes.