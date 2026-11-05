# T2T-S1 Plan — Mechanism Feasibility

**Plan ID:** `T2T-S1-MechanismFeasibility-v1.0.0-draft`  
**Status:** S1.1–S1.5 design/analytic deliverables completed and approved on 2026-11-04. T2T-S2 was separately authorized and run afterward; see `../s2/`.  
**Authority:** documentation and hand-worked synthetic analysis only. No code, benchmark, ARC access, experiment, or S2 approval.

## Objective

Determine whether Claim N (invariant representation adds predictive value beyond strong replay) and Claim B (counterexamples improve applicability boundaries) have observable, non-goalpost-shifting operational tests. This is a mechanism-feasibility program, not ARC-AGI-3 evaluation, a paper, or a method implementation.

## Milestones and status

| Milestone | Deliverable / acceptance | Status |
|---|---|---|
| **S1.0 — Scope freeze** | Keep Claims N/B central; exclude ARC/data/run, S2, paper drafting, and broad implementation. Preserve the existing P1 novelty no-go and all data/run controls. | **Complete** |
| **S1.1 — Minimum-publishable outcome review** | Define outcomes O1–O4 and a policy for continue/narrow/stop before mechanism results. Mark publication choices as recommendations requiring owner sign-off. | **Draft complete; owner sign-off pending** |
| **S1.2 — Claim N operationalization** | Select one primary endpoint; define arms, timing, denominator, scoring, and exact finite S1 decision rule; keep statistical fields unset rather than guess. | **Complete for operational definition** |
| **S1.3 — Boundary measurability** | Specify a deterministic toy world, separate source/refinement/held-out roles, and hand-compute independent boundary measures. State exactly what this demonstrates and what it does not. | **Analytic check complete; no code or empirical learner test** |
| **S1.4 — Strong replay stress specification** | Define the strongest fair replay envelope, primary comparator selection/freeze, competence review, expressivity stress check, and equal-opportunity accounting. | **Design complete; no baseline built** |
| **S1.5 — Kill criteria** | Separate claim-level falsification from blocked/inconclusive/invalid states; establish stop/hold gates before S2. | **Design complete** |

## S1 completion conclusion

S1 has established **operational measurability in principle**, not mechanism success: (a) Claim N has one all-context effect-prediction accuracy endpoint and a deterministic finite-domain rule; (b) the toy world shows how an observable scope counterexample can alter a versioned guard and how the successor can be assessed on fresh cases; and (c) a strong replay stress envelope and explicit stop conditions are specified.

No learner, baseline, statistical study, or real environment was run. Claim N and Claim B remain **empirically untested**. Do not describe S1 as evidence that either claim succeeds.

## S2 authorization and follow-up status

The user approved S1, including the S1.1 outcome framework, and separately authorized S2. The S2 prototype/run is recorded in [`../s2/README.md`](../s2/README.md). Its current status is: raw revised N scores tied, but the decision-grade N result is blocked because the baseline/model changed after the initial pilot and the same N holdout was reused; B passed only on the finite toy fixture.

Any fresh N test must freeze the replay baseline, invariant fitting rule, source corpus, and contexts before outcomes; address the previous holdout exposure; and record an explicit analysis plan. A stochastic or population-level test must additionally resolve `alpha`, meaningful-effect threshold, uncertainty method, and sample-size/power prospectively. These remain unset; none is inferred from S2. Any further code or evaluation requires its own scope decision/authorization. Nothing in S1/S2 authorizes ARC-AGI-3 data, tasks, evaluator, competition, or paper work.
