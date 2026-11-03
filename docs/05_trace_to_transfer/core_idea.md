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

## Core contribution candidate

The proposed differentiator is **counterexample-guided learning of the applicability boundary of an invariant-derived skill**, tested against strong replay/parameterized-script baselines. Claim N explicitly asks whether the invariant representation contributes information beyond replay. Claims B–D test whether counterexamples improve scope, reduce harmful transfer, and improve efficiency. The novelty wedge remains unverified pending the prior-art package.

## Preserve from original ASFT

- IDT: discover stable structure across varied experience.
- SCT: decide whether to promote a candidate, using only evidence available at the decision time.
- Transfer and negative transfer: count both useful application and harm.
- CGM / intelligence-growth language: defer. Use official task outcomes and action efficiency; do not introduce an unvalidated intelligence composite.
- Concept formation and skill composition: defer from the first study to avoid multiplying claims.

The existing `SCV = Reuse × AG × TS − CreationCost` remains an unvalidated intuition. Its terms require operational units, a source-only estimator, and missing-value rules before it may control promotion.

## Explicitly out of scope for this idea package

No new AGI-3 agent implementation, ARC run, hidden evaluation, score claim, Phase 2I run, Phase 3B/3D work, confirmatory split assignment, or new readiness phase. These documents prepare the question and plan only.
