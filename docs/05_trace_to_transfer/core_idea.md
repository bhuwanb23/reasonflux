# Core Idea — From Trace to Transfer

## Working title

**From Trace to Transfer: Counterexample-Guided Invariant Skills for ARC-AGI-3**

## Research question

Can an interactive agent infer a reusable state/action/effect invariant from varied experience, learn its applicability boundary from counterexamples, and use the resulting skill to improve later action efficiency beyond raw or compressed trace replay?

## Main hypothesis

A skill formed from cross-context state/action/effect invariants, with its scope refined by counterexamples, will improve held-out ARC-AGI-3 performance/action efficiency over no-skill, raw replay, strong parameterized/compressed replay, and simple recurrence-based skill creation at matched budgets, without unacceptable negative transfer.

This is a hypothesis, not a result or novelty claim.

## Mechanism in one line

`varied interaction traces → candidate invariant/effect → positive + counterexample evidence → applicability boundary → executable conditional skill → verified transfer`

A skill is not a copied trajectory. It is a versioned conditional procedure that says what relation it represents, what must be true before use, what it predicts, how it terminates, how it fails safely, and which experiences support it.

## Core contribution candidate — P1 revised status

The original proposed differentiator was **counterexample-guided learning of the applicability boundary of an invariant-derived skill**, tested against strong replay/parameterized-script baselines. The completed first-pass P1 review finds that this mechanism-level novelty claim is **not supportable as written**: SkillApt learns evidence-conditioned activation boundaries from matched outcomes; BASM uses explicit skill boundaries; and public issue #6645 proposes counterexample-qualified refinement of reusable skill guards. ARC world-model systems also cover mismatch-driven repair. See [`P1 decision`](p1/novelty_decision.md).

A narrower comparative question may remain: whether cross-context structural state/action/effect invariants add held-out value beyond outcome-based activation, boundary-aware skill records, guard-refinement analogues, per-environment model repair, and strong replay. The owner selected this comparative reframe as the best direction on 2026-11-03. It is not novelty-cleared or empirically tested. Keep Claims N and B–E untested; do not present the original mechanism as novel, and do not infer authorization for implementation or experiments from the reframe decision.

## Preserve from original ASFT

- IDT: discover stable structure across varied experience.
- SCT: decide whether to promote a candidate, using only evidence available at the decision time.
- Transfer and negative transfer: count both useful application and harm.
- CGM / intelligence-growth language: defer. Use official task outcomes and action efficiency; do not introduce an unvalidated intelligence composite.
- Concept formation and skill composition: defer from the first study to avoid multiplying claims.

The existing `SCV = Reuse × AG × TS − CreationCost` remains an unvalidated intuition. Its terms require operational units, a source-only estimator, and missing-value rules before it may control promotion.

## Explicitly out of scope for this idea package

No new AGI-3 agent implementation, ARC run, hidden evaluation, score claim, Phase 2I run, Phase 3B/3D work, confirmatory split assignment, or new readiness phase. These documents prepare the question and plan only.
