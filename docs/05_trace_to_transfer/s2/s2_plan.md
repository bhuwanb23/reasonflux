# T2T-S2 Plan — Synthetic Mechanism Prototype

**Plan ID:** `T2T-S2-SyntheticMechanism-v1.0.0-draft`  
**Authorization:** user explicitly authorized a tiny synthetic-only prototype and first empirical test of Claims N and B.  
**Status:** prototype/pilot work complete, 2026-11-04. An initial weak-baseline pilot was followed by a strengthened R1-Max run; because the same N holdout was reused after the baseline/model revision, the decision-grade N result is **BLOCKED**. B showed the predeclared finite-fixture improvement.  
**Date:** 2026-11-04.

## 1. Purpose

Make the two mechanisms run in one small, fully specified synthetic world and record their first result:

- **N:** does a predeclared invariant predictor exceed a competent, source-trace-derived parameterized replay baseline on S1's all-context exact one-step effect-prediction accuracy?
- **B:** does a counterexample-updated applicability boundary reduce false activation on fresh contexts, without losing applicable-context coverage, relative to the same invariant with its boundary frozen?

This is a finite mechanism check, not ARC/AGI-3 evaluation, a benchmark, a full skill system, or a paper.

## 2. Hard boundaries

### In scope

- One deterministic key/door toy world and one predeclared color-match invariant family.
- One `R1-Max` source-only parameterized replay baseline, built before the invariant comparison.
- One minimal I0 predictor and one fixed-vocabulary counterexample boundary update (I1).
- Small enumerated source, counterexample, N-holdout, and B-holdout fixtures.
- A reproducible local run, focused tests, and a result record with denominators.

### Explicitly out of scope

- ARC, AGI-3, Mini-ARC, competition data, task IDs, splits, leaderboard metrics, evaluator, network, model, live environment, or restricted outcomes.
- General skill ecosystem, skill promotion, lifecycle manager, SCT, CGM, composition, agent loop, broad policy learning, cost-benefit composite, or paper work.
- Full P2/P4/P6 implementation or production event-journal changes.
- Claims about generalization beyond this finite toy set, statistical significance, real-world harm reduction, or production readiness.

No repository-wide tests or unrelated experiments are authorized by this plan.

## 3. Frozen mechanism and fixture definition

World state has observable booleans `adjacent`, `door_closed`, `has_key`, `corridor_clear`, and categorical `key_color`, `door_color`. The action is `USE_KEY_AND_ENTER`.

The known world transition succeeds exactly when:

`adjacent AND door_closed AND has_key AND corridor_clear AND (key_color == door_color)`

A successful effect is `{door_open: true, agent_advanced: true}`; all other complete states yield `{door_open: false, agent_advanced: false}`. The invariant family is the same color-match relation. No second rule or world is included.

### N source and holdout

- The shared synthetic source corpus contains two successful traces with distinct matched colors (blue→blue, green→green), two color-mismatch negatives, and one negative trace for each failed base predicate. Both arms receive the same source examples.
- N holdout: eight fixed, unseen contexts—four valid matched-color transitions and four non-success contexts (mismatched colors and failed base preconditions). These are not used to fit or tune either arm.
- **R1-Max:** first compresses the source action traces; then searches a frozen finite grammar of directly observable boolean predicates (adjacent, door closed, key present, path clear, and key-color-equals-door-color) for the shortest conjunction exactly consistent with source effects. It instantiates a deterministic conditional macro, allows new color literals through typed fields, predicts no-effect when the fitted macro guard is false, and receives no target labels or boundary updates. The predicate grammar and tie rule are fixed before evaluation.
- **I0:** fits the single predeclared color-equality invariant family from the same source corpus and predicts the exact one-step effect on complete observable states; its skill applicability boundary stays frozen for N.
- This is deliberately a demanding **bounded trace-to-script replay compiler**: it can compile the same simple condition into a macro without a P2 invariant object. If it matches I0, that is N-FAIL for this fixture, not a defective baseline. It is still not an unrestricted program synthesizer; the result is bounded to the frozen grammar.

### B training and holdout

- The frozen no-boundary guard is `G0 = adjacent AND door_closed AND has_key AND corridor_clear`.
- One source mismatch trace has a red key at a blue locked door under all base predicates. The candidate skill predicts success when G0 admits it, but the observed effect is no-op, so it is a scope-admission counterexample. R1 receives the trace as an exact source record; only I1 uses it to update the guard.
- One fixed update rule may add the sole predeclared observable predicate `key_color == door_color`, yielding `G1`.
- Six fresh B-holdout contexts are frozen independently of the counterexample and measured under G0 and G1. The counterexample is not included in B scoring.

## 4. Predeclared outcome rules

### N

Use S1's all-context exact effect-prediction accuracy: correct exact effect = 1; incorrect, abstain, invalid, or missing prediction = 0; denominator is all eight N-holdout contexts.

- **N-PASS:** `Acc_I0 > Acc_R1-Max`.
- **N-FAIL:** `Acc_I0 <= Acc_R1-Max` on this finite fixture (tie or lower).
- **N-BLOCKED:** any source/target leakage, invalid comparator, missing required observation, mismatched arm inputs, baseline implementation failure, or outcome-informed change to the baseline/model/source corpus followed by reuse of exposed N holdouts makes the comparison non-decision-grade.

This is a finite-fixture result only. No confidence interval or population claim is implied.

### B

On the six fresh B-holdout contexts report separately: false activations / truly non-applicable cases, applicable cases admitted / applicable cases, false rejections, and total coverage. `B-PASS` requires fewer false activations for G1 than G0 **and** no loss of applicable-context coverage on this frozen fixture. Otherwise `B-FAIL`; invalid/leaking or incomplete comparisons are `B-BLOCKED`.

A B pass establishes only that this fixed update changes this boundary correctly in the toy world; it does not establish harm reduction or learning quality in other worlds.

## 5. Milestones

1. **S2.0 Scope and outcomes frozen** — metric, denominators, and B decision rule were documented before the pilot; however, R1-Max's exact construction was under-specified and changed after the first N output. This deviation blocks decision-grade N interpretation.
2. **S2.1 Minimal world** — **complete**; deterministic transition function and state fixtures implemented.
3. **S2.2 R1-Max first** — **complete**; source-only trace compilation selects the shortest consistent conjunction in the frozen predicate grammar.
4. **S2.3 I0 and boundary** — **complete**; one-family relation fit, G0, append-only synthetic CE record, and immutable G1 successor implemented.
5. **S2.4 N run** — **exploratory only; decision-grade status N-BLOCKED**. The first baseline scored 4/8 against I0's 8/8; after strengthening R1-Max and revising I0, the reused holdout yielded 8/8 vs 8/8. The v0 output is preserved in `results/keydoor_pilot_v0.md`; neither run is an independent confirmation.
6. **S2.5 B run** — **complete; B-PASS on this fixture**; false activations fell 2/4→0/4 with applicable coverage 2/2 retained on six fresh contexts.
7. **S2.6 Verification/report** — **complete**; the focused S2 test module passed 8 tests; v0 pilot and revised exploratory output are documented, with the reused-holdout limitation recorded.

## 6. In-scope files

- `docs/05_trace_to_transfer/s2/s2_plan.md`
- `docs/05_trace_to_transfer/s2/README.md`
- `docs/05_trace_to_transfer/s2/results/keydoor_run_v1.json`
- `docs/05_trace_to_transfer/s2/results_v1.md`
- `docs/05_trace_to_transfer/s2/results/keydoor_pilot_v0.md`
- `src/t2t_s2/__init__.py`
- `src/t2t_s2/world.py`
- `src/t2t_s2/replay.py`
- `src/t2t_s2/invariant.py`
- `src/t2t_s2/evaluation.py`
- `src/t2t_s2/run.py`
- `tests/t2t/test_t2t_s2_mechanism.py`
- `docs/05_trace_to_transfer/README.md`, `master_plan.md`, and `current_evidence.md` only for the S2 status/index/evidence-ceiling update.
- `docs/05_trace_to_transfer/s1/README.md`, `s1/s1_plan.md`, and `s1/minimum_claim_package.md` only to record the user's S1/S1.1 approval and the completed S2 follow-on status.

These cross-index/status files were added to S2's documentation scope after the user's approval and S2 outcome so the project entry points remain accurate. No P4/P5/P6 design contracts were changed. No dependencies should be added unless an essential need is identified and documented. Tests and run use only synthetic in-memory fixtures; generated run output is the designated in-scope JSON result artifact.

## 7. Stop and interpretation rules

If R1-Max matches/beats I0, report N-FAIL for this test, not baseline incompetence. If I1 does not reduce false activation without losing positive coverage, report B-FAIL. A failure in this toy fixture is a valid negative result for this setup; it does not establish impossibility in all domains. A pass is equally bounded and does not authorize any broader claim. Do not change the world, holdout, metric, baseline, or predicate after viewing results.

## 8. Change log and validity deviation

The first exploratory implementation used a positive-trace shared-slot R1 that abstained outside its macro and a directly encoded I0 rule. It yielded I0 8/8 versus R1 4/8. After seeing that apparent advantage, R1 was strengthened to fit the shortest conjunction consistent with positive and negative source traces; I0 was also changed to fit-check against the same source corpus. The same N holdout was then reused and yielded 8/8 versus 8/8. The initial output is retained in `results/keydoor_pilot_v0.md`; the revised raw output is in `results/keydoor_run_v1.json`. A final reproducibility execution after input-validation hardening returned the same revised scores; it used no new contexts and is not an independent replicate.

This is a baseline/model revision after exposure to the N result, so neither the initial N pass nor revised tie is a confirmatory N result. The correct S2 N status is `N-BLOCKED`. The B rule, CE, G0/G1 update, and B holdout stayed fixed across the revision; the finite B comparison is recorded with its strict toy-only interpretation.

## 9. Completion log

**S2 prototype and exploratory mechanism check complete, 2026-11-04; no confirmatory Claim N result.**

- Implemented `src/t2t_s2/` using the standard library only: deterministic world, R1-Max trace-to-script compiler, one-family I0 relation fit, fixed I1 counterexample boundary update, finite scoring, and run entry point.
- Added focused tests at `tests/t2t/test_t2t_s2_mechanism.py`.
- Focused command `python -m pytest -q tests/t2t/test_t2t_s2_mechanism.py` — **PASS: 8 passed**; `python -m compileall -q src/t2t_s2 tests/t2t/test_t2t_s2_mechanism.py` — **PASS**.
- Documentation link QA — **PASS: 78 Markdown files, no missing relative targets**; S2 package network scan — **PASS: no network imports/calls/URLs**.
- The initial v0 exploratory run showed I0 8/8 vs a weaker positive-trace replay 4/8. After seeing this, R1-Max was strengthened to fit a shortest source-consistent conjunction and I0 was revised to fit-check against the same source corpus. The same exposed N holdout was reused. This sequence is recorded in `results/keydoor_pilot_v0.md` and means N is **BLOCKED for decision-grade interpretation** under the S2 rule; do not report v0 as an N pass.
- Revised-run raw metric: I0 = 8/8, R1-Max = 8/8; difference 0. This exploratory tie shows the bounded replay script can reproduce the invariant on this toy but is not an independent confirmation after the v0-driven revision.
- B result is unchanged: G0 false activations 2/4; CE-updated G1 0/4; both admitted 2/2 applicable contexts. Total activation was 4/6 for G0 and 2/6 for G1. Treat this as a deterministic finite-fixture mechanism demonstration only.
- Human-readable result: `results_v1.md`; revised-run machine-readable result: `results/keydoor_run_v1.json`; v0 audit: `results/keydoor_pilot_v0.md`.
- No ARC/AGI-3, Mini-ARC, competition data, evaluator, model, network, restricted outcome, repository-wide test suite, or unrelated experiment was used.

**Interpretation:** raw revised run corresponds to O3 (N tie, B succeeds), but valid program-level outcome remains **N-BLOCKED, B finite-fixture pass** because of the post-pilot baseline/model revision and reused N holdout. A fresh, prospectively frozen N test would be required before deciding the claim. The B result does not show harm reduction, population generalization, cost-effectiveness, novelty, or ARC value. P1's novelty no-go remains. Any boundary-only continuation requires separate novelty/research-question review. No further program or ARC work is authorized by this result.
