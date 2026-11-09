# Claim N v1 Archive

**Status: CLOSED — FAILED (decision-grade predictive endpoint)**  
**Closure decision:** owner selected D1-B on 2026-11-05.  
**Rerun / N-v2:** not authorized; Claim N v1 is permanently closed as the current claim track.

## Original hypothesis

Claim N asked whether an explicit invariant-derived representation provides predictive value beyond the strongest fair source-derived replay/compiler under matched information and resources. The S3 operational estimand was all-context exact one-step effect prediction by I0 versus R4 in one finite deterministic synthetic relational-unlock world. The S3 endpoint did not measure a separate behavioral increment.

## Frozen protocol

- Frozen implementation package: `T2T-S3-RA-v0.2.0`.
- Independent comparator fairness review: PASS, reference `S3-RB-IND-2026-11-05-001`.
- Source: exactly 7 contexts, one for each required six-predicate contrast; no extra source contexts.
- Primary held-out suite: 35 surface × semantic cells, 3 contexts per cell, 105 contexts total.
- Diagnostics: 10 unknown-required-state contexts, excluded from the primary endpoint.
- Primary arms: I0 versus R4; R0–R3 were the frozen replay ladder diagnostics.
- R4: minimum-node source-derived decision tree over the six frozen predicates, capable of expressing every Boolean function in that grammar.
- Scoring: correct=1; wrong, abstain, invalid, or missing=0; all primary contexts remain in the denominator.
- Decision rule: `Delta_N = Accuracy(I0) - Accuracy(R4)`; `Delta_N > 0` → N-PASS; `Delta_N <= 0` → N-FAIL; protocol/integrity failure → N-BLOCKED.
- Full package, manifests, hashes, and run protocol: `docs/05_trace_to_transfer/s3/s3e_run_package_v1.md` and adjacent S3-E artifacts.

## Execution record

- Run ID: `T2T-S3-EXEC-2026-11-05-001`.
- One explicitly authorized execution; no reruns.
- No protocol deviations.
- Prediction events were committed before held-out outcomes were accessed.
- Execution record: `reports/experiments/T2T-S3-EXEC-2026-11-05-001/s3_execution_record.json`.
- Prediction artifact: `reports/experiments/T2T-S3-EXEC-2026-11-05-001/prediction_events.jsonl`.

## Result

- I0: **105/105**, accuracy **1.000**.
- R4: **105/105**, accuracy **1.000**.
- Per-cell result: I0 and R4 each scored **3/3** in all 35 cells.
- `Delta_N = 0.0`.
- Frozen decision: **N-FAIL**.
- Decision report: `reports/experiments/T2T-S3-EXEC-2026-11-05-001/claim_n_decision.md`.

## Lessons learned

1. The frozen source-derived Boolean compiler reproduced the relational rule as well as I0 within the declared six-predicate grammar and finite suite.
2. The protocol and comparator worked as intended; the result is an interpretable tie, not a blocked test.
3. Invariant-specific predictive value beyond R4 was not demonstrated for this estimand.
4. The result closes this Claim N v1 track. It does not justify weakening R4, selecting a favorable subset, changing the suite, or creating N-v2 as a rescue attempt.

## Limitations

- This was a finite synthetic one-step prediction test, not an ARC-AGI-3 evaluation or population-level study.
- The separate behavioral increment was not tested.
- N-FAIL does not prove that every invariant representation is impossible or that R4 dominates outside this suite.
- Claim A remains partial synthetic support; Claim B remains a toy-fixture observation only; Claims C, D, and E remain untested.
- No general intelligence, ARC transfer, or broad skill-formation conclusion follows.

## Closure

**CLAIM N v1: CLOSED — N-FAIL.** No S3 rerun, R4 modification, post-hoc subset, reinterpretation as N-BLOCKED, or N-v2 rescue is permitted under this decision. The separate boundary-learning question is preserved in `boundary_learning_question.md`; it is not a validated claim, implementation authorization, or new phase.
