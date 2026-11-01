# Hypothesis Register (Pre-registration Draft)

**Status:** Draft; all `REQUIRED_BEFORE_RUN` items must be completed and frozen before confirmatory data are inspected. H1/H2/H3 are not established findings.

## Shared terms

- **Experience/source set:** REQUIRED_BEFORE_RUN; exact training tasks, demonstrations, trajectories, and labels.
- **Held-out target set:** REQUIRED_BEFORE_RUN; task/game IDs and family-level split.
- **Skill candidate:** a versioned executable program, action macro, or subpolicy with explicit preconditions, expected effects, and failure/rollback behavior. Track-specific schema must be specified.
- **Transfer:** improvement on held-out target tasks attributable to access to a learned invariant/skill, compared with matched-control exposure and compute. Specify primary outcome separately by track.
- **Budget:** fixed per-run limits on compute/time/tokens/actions/search/memory. Exact limits: REQUIRED_BEFORE_RUN.

## H1 — Invariant Discovery Theory (IDT)

**Claim:** A learned reusable structure extracted from source experience improves held-out target performance or efficiency compared with the same base solver without that learned structure.

**Treatment:** invariant discovery enabled; candidate representation, extraction algorithm, and selection threshold frozen in config.  
**Controls:** B0 no learned skills and B1 static/frequency-based library; same source experience and budget.  
**Primary outcome:** choose exactly one per track before running: (A) official score/pass rate at fixed budget, or (B) resource cost to a fixed success criterion. Track choice: REQUIRED_BEFORE_RUN.  
**Secondary outcomes:** the other primary candidate, transfer delta, candidate precision/coverage if independent ground truth exists, invalid-program rate, negative transfer, runtime.  
**Analysis unit:** paired held-out task/game ID; task-family split.  
**Support rule:** primary treatment-control effect exceeds the frozen `delta_min`, the preregistered CI excludes zero in the beneficial direction, and performance regression stays within `regression_margin`. Values: REQUIRED_BEFORE_RUN.  
**Falsification/weakening:** no held-out benefit; effect disappears versus a simple library baseline; extracted structures only work on source-family lookalikes; invalid/negative transfer overwhelms gains.  
**Risks to report:** hand-coded semantics in traces; hidden overlap; false invariants; selection using held-out labels; additional search budget.

## H2 — Skill Creation Trigger Theory (SCT)

**Claim:** A trigger estimating net future value creates/promotes skills more effectively than never-store and always-store policies under matched conditions.

**Decision-time rule:** an estimated benefit must use only evidence available before target outcomes. The existing `Reuse × AG × TS − CreationCost` is not accepted as an implementation until every term has operational units, scales, training-only estimator, and missing-value behavior. Canonical estimator: REQUIRED_BEFORE_RUN.  
**Treatments:** (1) never-store; (2) always-store every candidate meeting a frozen validity test; (3) SCT promotion threshold using only source/validation experience.  
**Primary outcome:** preselect a net result, preferably report (a) official held-out score/success and (b) resource cost separately, plus a predeclared practical-value criterion. Do not use a post-hoc composite.  
**Secondary outcomes:** skills created/reused, cost of creation/maintenance, invalid skill rate, negative transfer, duplicate rate, library size and retention.  
**Support rule:** SCT exceeds both controls on its preregistered primary outcome, meets `delta_min`, and respects negative-transfer and memory/runtime guardrails. Values: REQUIRED_BEFORE_RUN.  
**Falsification/weakening:** trigger performs no better than always/never; estimates use future outcomes; savings are offset by creation/maintenance or retrieval; performance degrades because useful skills are withheld.  
**Leakage rule:** no target/test outcome may be used to decide whether that target's skill should have been created.

## H3 — Capability Growth Metrics (CGM)

**Claim:** A predeclared growth measure based on a fixed held-out probe suite predicts later held-out task performance or efficiency beyond the current-score baseline.

**Do not claim:** “we measured intelligence” or “the system became more intelligent” based only on a custom weighted skill count.

**Candidate operational measure:** at predefined checkpoints, evaluate the same fixed probe set under the same budget. `ProbeScore_k` is the track-native mean score over that probe set at checkpoint k. Candidate growth over interval k is `G_k = ProbeScore_k - ProbeScore_(k-1)`; also report resource cost separately. Do not alter the probe set during the run. Track-specific scoring/aggregation: REQUIRED_BEFORE_RUN.

**Predictive test:** use independent experience sequences/seeds as units. Test whether early `G` predicts the next checkpoint's held-out probe score or cost better than a baseline predictor using current probe score alone. Choose one target, model, metric (e.g., held-out predictive error or incremental predictive association), and sample count before running. Details: REQUIRED_BEFORE_RUN.

**Support rule:** incremental predictive value beats the frozen baseline by `delta_min` on an untouched sequence/seed split, with uncertainty interval and no leakage.  
**Falsification/weakening:** growth does not predict future held-out outcomes; association disappears after controlling for current score/task difficulty/budget; apparent growth is caused by changing probe composition or weights.

**Status:** exploratory by default; do not make CGM a gate controlling the competition solver until predictive validity is shown.

## Track-specific operational definitions (must complete)

| Item | ARC-AGI-2 | ARC-AGI-3 |
|---|---|---|
| Source experience / training corpus | REQUIRED_BEFORE_RUN | REQUIRED_BEFORE_RUN |
| Held-out task/game families | REQUIRED_BEFORE_RUN | REQUIRED_BEFORE_RUN |
| Trace/event schema | REQUIRED_BEFORE_RUN | REQUIRED_BEFORE_RUN |
| Invariant representation | REQUIRED_BEFORE_RUN | REQUIRED_BEFORE_RUN |
| Skill representation / preconditions | REQUIRED_BEFORE_RUN | REQUIRED_BEFORE_RUN |
| Official evaluator version | REQUIRED_BEFORE_RUN | REQUIRED_BEFORE_RUN |
| Primary metric | REQUIRED_BEFORE_RUN | REQUIRED_BEFORE_RUN |
| Budget and matching rule | REQUIRED_BEFORE_RUN | REQUIRED_BEFORE_RUN |
| Minimum meaningful effect / guardrail | REQUIRED_BEFORE_RUN | REQUIRED_BEFORE_RUN |
| Seeds, sample size, uncertainty method | REQUIRED_BEFORE_RUN | REQUIRED_BEFORE_RUN |
| Data/license/competition-rule review | REQUIRED_BEFORE_RUN | REQUIRED_BEFORE_RUN |
