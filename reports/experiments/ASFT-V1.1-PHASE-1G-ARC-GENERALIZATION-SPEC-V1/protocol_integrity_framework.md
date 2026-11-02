# Phase 1G.10 — Protocol Integrity Framework

## C1 — Config/code/budget consistency

One versioned config is the source of candidate limits, seeds, search rules, compute/time budgets, and stopping criteria. Runtime must receive those values explicitly; no hidden defaults. Automated preflight compares config, call arguments, runtime counters, and reported denominators. Any mismatch blocks confirmatory interpretation. An exhaustive coverage scan above the scored budget is allowed only if preregistered as a separate diagnostic, separately logged, and excluded from scored-arm accuracy/transfer estimates.

## C2 — Holdout integrity

Create discovery, transfer, and holdout manifests before model execution, hash them, and restrict gold labels. Holdout outputs/gold are accessed once after all code/config/predictor decisions are frozen. No debugging, posthoc rerun, candidate tuning, or metric adjustment on the same holdout. Multiple arms can be scored in the same authorized one-time evaluation, but outputs stay sealed until lock; any rerun/reuse must be disclosed and loses pristine-confirmatory status. Replication requires disjoint tasks/seeds/templates.

## C3 — Evaluation isolation

Policy/task-generation process cannot access test gold, official evaluation/private files, annotation labels, or evaluator outputs. Evaluator is separate and blind to arm/ASFT metrics. The target scorer must run with CGR/C_t/IG disabled. Log file access, API calls, task queries, memory state, and predictor join time. Do not claim official ARC performance absent a public, authorized submission and score.

## C4 — Coverage transparency

Every rate includes task IDs, denominator, representation version, search budget, and discovery stage. Budgeted and full-inventory demo-fit coverage are separate. Coverage, trace schema validity, successful traces, invariant yield, skill formation, transfer, capability, and accuracy receive distinct columns/statuses. Never turn `unsupported` into evidence of zero skill utility without denominator.

## C5 — Failure logging

Persist no-fit, budget exhausted, timeout, parse error, invalid candidate, demo mismatch, test mismatch, unsupported category, invariant rejection, skill rejection, ineligible transfer, negative transfer, missing gold, and unavailable metrics with explicit reason codes. Do not drop failures or replace them with zero/NaN silently.

## Integrity gate

All C1–C5 controls must be verified before confirmatory outcome access. If C1/C2/C3 fails, primary confirmatory results are unavailable/invalid; no selective repair or same-holdout rerun. Any correction requires new disjoint confirmatory tasks or a clearly labeled development rerun.