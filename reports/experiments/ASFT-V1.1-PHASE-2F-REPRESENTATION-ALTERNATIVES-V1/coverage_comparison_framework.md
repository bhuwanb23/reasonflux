# Phase 2F.4 — Coverage Comparison Framework

## Primary endpoint

For each task ID and representation, **found-fit coverage** is 1 iff the registered search finds at least one candidate that exactly reproduces every training demonstration within the shared candidate/resource budget. It is an operational bounded-search outcome, not semantic representability, held-out generalization, or accuracy.

## Paired design

- Same prospectively frozen task IDs, demonstrations, split membership, and input validation across all representations. All 1,000 Phase 2C IDs have already been inspected in coverage/trace/invariant audits; reruns on them are diagnostic only. Confirmatory attribution requires a new authorized untouched common split.
- Coverage runner reads training demonstrations only and terminates before test fields. A separate evaluator is sealed and not invoked by the coverage runner.
- Primary comparator: R1 vs R3. Secondary predeclared comparisons are in `comparison_matrix.csv`; R0 is historical context only.
- For each task log: representation/parser version; candidate IDs and order; candidates available, generated, evaluated, fit, skipped, and remaining at cap; fit ambiguity if known; parameter inference state; elapsed time; memory; and terminal status.
- Allowed no-fit statuses include `NOT_FOUND_WITHIN_LANGUAGE_AND_BUDGET`, `SEARCH_BUDGET_EXHAUSTED`, `PARAMETER_SEARCH_INCOMPLETE`, `PARSER_FAILURE`, `INVALID_INPUT`, and `AMBIGUOUS_DEMO_FIT`. Do not label a capped no-fit “not representable.”

## Matched resources

Use the Phase 2C frozen S4 ceiling for the primary comparison: B1 max 10 complete candidate trials/task; B2 one flat search level; B3 one primary trace/task/condition and at most four high-level steps; B4 30 seconds/search; B5 2,048 MiB process limit; B6 1,000 primary task IDs/condition plus one 1,000-task deterministic replay. A composed AST is one complete candidate, not iterative deepening. All candidate expansions count as trials. Log actual consumption separately from caps.

R0 historical budget mismatch (declared3/discovery10) is not corrected retrospectively. Its results cannot enter the paired primary estimate. A future primary run must verify config=runtime=log parity for every representation. If alternative grammars cannot be meaningfully sampled under the same cap, report the resulting fixed-budget comparison and add a separately preregistered language-ceiling diagnostic; never silently give an arm extra search.

## Estimate and limits

Report covered/uncovered counts and paired task-level risk difference `coverage_alt - coverage_R1`, win/loss/tie (discordant/equal) counts, and predeclared 95% paired bootstrap intervals over task IDs. Freeze seed and resample count in the run preregistration. Freeze a practical effect threshold `δ_coverage` before outcomes; this framework does not choose it. Report split-specific results and no-fit categories. Do not treat a demo-fit increase as transfer or test-accuracy gain.