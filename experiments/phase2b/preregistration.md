# ASFT v1.1 Phase 2B — Frozen Coverage-Only Protocol

**Phase:** `ASFT-V1.1-PHASE-2B`  
**Package:** `ASFT-V1.1-PHASE-2B-ARC-COVERAGE-BENCHMARK-V1`  
**Status:** frozen before the new coverage-only run.  
**Purpose:** measure how many ARC training tasks reach operational stages under the unchanged Phase 13G representation; do not assess ARC answer accuracy or confirm ASFT efficacy.

## Questions and estimands

- **R2B-1 — bounded operational representability:** fraction of tasks with an exact training-demonstration fit under all ten Phase 13G candidates and unchanged parameter inference. A no-fit result means only that this bounded scan found no fit; it does not prove semantic unrepresentability.
- **R2B-2 — budgeted discoverability:** fraction with an exact training-demonstration fit within the declared production candidate budget of three, in the frozen Phase 13G order.
- **R2B-3 — stage reach:** task-level C1–C7 outcomes, reported separately for budgeted and fullscan modes, with conditional denominators and upstream-blocked states explicit.
- **R2B-4 — failure localization:** identify the first observed pipeline stage with attrition; do not automatically assign causal responsibility to representation, search, threshold, or downstream mechanism.

## Dataset and isolation

Use the frozen Phase 13G split manifest: 600 discovery, 200 transfer, and 200 holdout task IDs. Task files are read through a fail-closed loader that parses only the first top-level `train` array and stops before the next field. The runner contains no test-output accessor, does not call `solve_task`, and does not calculate accuracy. It performs independent rectangular-grid/color-domain checks and exact replay on training demonstrations only. Whole task files may be hashed for provenance; hashes are not labels or scores. This diagnostic does not rehabilitate the previously reused holdout for confirmatory claims.

## Representation and search conditions

Keep the Phase 13G ten-program order, helper implementation, inference rules, exact-demo-fit criterion, and first-fit stopping semantics unchanged. Run two paired diagnostic modes on each task:

1. **Budgeted:** first three programs only, matching the declared per-task reasoning/search budget and scored-arm budget in Phase 13G.
2. **Fullscan:** all ten programs, diagnostic ceiling only.

The Phase 13G config did not specify a wall-clock timeout. The frozen resource control is deterministic candidate trials (3 and 10 respectively); no additional per-task timeout is introduced. Record aggregate runtime but do not tune on it.

## Frozen stage rules

- **C1 — representable within this mode:** at least one exact fit on every training demonstration within the mode's finite candidate set and trial budget.
- **C2 — trace generated:** one structured trace emitted per task/mode, including explicit no-fit traces.
- **C3 — successful trace:** independently validate trace structure and replay the selected program exactly on every training demonstration.
- **C4 — invariant candidate available:** run the Phase 13G TraceMiner on successful discovery traces only, using the existing minimum support 5 and consistency 1.0 policy; count only candidates mapped to a Phase 13G program.
- **C5 — skill candidate available:** report only if C4 provides an input pool. If C4 is empty, report zero tasks reached and `blocked_upstream_no_C4_candidate`; do not call the transfer-dependent skill builder.
- **C6 — transfer eligible:** requires a nonempty skill candidate and a separate authorized transfer protocol; never use test accuracy as a coverage proxy.
- **C7 — capability eligible:** requires at least two independently validated reusable skills and transfer evidence; not inferred from accuracy.

All rates use task ID as the unit. Report all-task rates and, where the prior-stage denominator is nonzero, conditional transition rates. When a conditional denominator is zero, report `not_estimable` rather than a numeric zero. Keep “0 reached” distinct from “not run/unavailable.”

## Trace metrics

Report trace emitted rate, independently validated trace rate, successful-trace rate, distinct successful first-fit signatures, Shannon entropy of successful program labels, and mechanical trace steps per task. Mechanical record density is not a measure of reasoning depth. Fullscan trace yield is diagnostic and cannot be presented as accuracy or system performance.

## Failure localization policy

Classify observed stage losses only. Possible labels: F1 representation/bounded-language concern; F2 search-budget concern; F3 support-threshold concern; F4 invariant-mining concern; F5 mixed observed failure pattern; F6 unresolved causal attribution. Assigning a label does not establish theory-level root cause. Any comparison changing representation, order, parameter inference, support threshold, or transfer rule requires a distinct preregistered experiment.

## Frozen output and stop rules

Write task-level stage outcomes, split-level summaries, trace-yield report, and an execution manifest. Abort on split/count mismatch, invalid training-grid schema, independent trace validation failure, or inability to stop before the `test` field. Preserve Phase 13G artifacts and outcomes unchanged. Do not compute or report accuracy, confidence intervals for accuracy, leaderboard results, or efficacy claims.