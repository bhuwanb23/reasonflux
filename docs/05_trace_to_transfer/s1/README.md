# T2T-S1 — Mechanism Feasibility Program

**Program:** `T2T-S1-MechanismFeasibility-v1.0.0-draft`  
**Purpose:** determine whether Claims N and B are operationally observable and measurable before building the T2T mechanism or attempting an ARC-AGI-3 evaluation.  
**Status:** S1.1–S1.5 decision package drafted; S1.3 includes an analytically worked synthetic toy world. No code, experiment, benchmark, ARC data, or empirical result is part of this package.

## Scope boundary

S1 is not ARC-AGI-3 evaluation, a benchmark phase, a paper, or an implementation phase. It does not reopen P4/P5/P6 implementation, authorize T2T-S2, or change any data/run restrictions. Existing P2–P7 documents remain design contracts; this packet operationalizes feasibility questions for a possible later step without rewriting those contracts.

The toy world in S1.3 is a hand-computable fixture. Its truth labels are defined by a known deterministic transition rule, and the table shows that boundary changes and their effects can be measured. It is not a run of an implemented learner and does not show that the proposed algorithm can discover the rule or that it transfers to ARC.

## S1 deliverables

1. [`minimum_claim_package.md`](minimum_claim_package.md) — recommended minimum-publishable-outcome decisions for O1–O4, with a strict no-go if both central mechanisms fail.
2. [`claim_N_decision_rule.md`](claim_N_decision_rule.md) — one primary endpoint and exact all-context decision rule for invariant prediction versus strong replay.
3. [`boundary_measurability_report.md`](boundary_measurability_report.md) — toy key/door world, held-out truth table, and non-composite boundary metrics.
4. [`strong_replay_spec.md`](strong_replay_spec.md) — a defensible replay baseline envelope and an adversarial expressivity stress test.
5. [`research_stop_conditions.md`](research_stop_conditions.md) — claim-level kill criteria, program-level stop/hold distinctions, and gate for any later S2 proposal.

## Recommended immediate conclusion

At S1 completion, the questions were **measurable in principle** under explicit observability and holdout assumptions. The separately authorized S2 prototype has since run: its revised raw N scores tied, but N is blocked for decision-grade interpretation because the baseline/model changed after the pilot and the N holdout was reused; B passed only on the finite toy fixture. See [`S2 results`](../s2/results_v1.md). This does not establish a population effect or ARC relevance.

## Decision items that remain open

- The user reviewed and approved the S1.1 O1–O4 framework on 2026-11-04. This is approval of the outcome policy, not a personal commitment to write a paper for any particular result.
- For a future stochastic study, the confidence level, minimum meaningful difference, sample size/power, resource caps, and cost trade-offs remain unset. S1 deliberately does not invent them.
- P1's no-go on generic counterexample-guided guard refinement remains controlling. A positive B result alone does not establish novelty.

## Sequence

`P0–P7 design packets` → **S1 approved** → **S2 separately authorized and run** (see `../s2/README.md`; N decision-grade status blocked, B finite-fixture pass) → owner decision to retest, narrow, or stop → only later consider ARC-AGI-3, subject to all existing approvals and controls.
