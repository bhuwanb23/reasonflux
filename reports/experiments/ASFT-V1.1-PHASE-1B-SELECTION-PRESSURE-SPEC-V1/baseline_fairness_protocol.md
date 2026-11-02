# 1B.6 — Baseline Fairness Protocol

## Required parity

| Dimension | Frozen rule |
|---|---|
| Candidate pool | Exactly same 20 candidate IDs and technical eligibility result for every selector in a batch. |
| Information | Same selector-visible feature card and observation timestamp; all future/outcome/latent-label fields sealed. Each method may use only its declared signal. |
| Creation capacity | Eight slots for S1–S5 and S7; S6 is the required no-create anchor. No policy can buy extra candidates. |
| Candidate opportunities | Ten fixed future task opportunities per candidate lane for every selector. Task IDs, order, difficulty, and no-skill paired scores match across arms. |
| Cost horizon | Same once-only creation cost and same ten-opportunity maintenance window for each selected candidate. Unselected candidates incur no deployment cost; their counterfactual task lane remains logged. |
| Compute | Same feature extraction, decision-time ceiling, solver, environment, operation/time accounting, and evaluation runtime cap. Report selector decision compute separately. |
| Randomization | Common immutable batch manifest; S4 uses independent recorded RNG. Reproducible seeds; no matched-to-SCV sample count learned from outcomes. |
| Ties/missing inputs | Fixed ID-hash tie break; no outcome-aware tie resolution. Feature missingness handled by predeclared imputation/source tags; no policy-specific missingness rule. |
| Software | Versioned arms, source/config hashes, contract tests, isolated state/library per selector, same task runner. |
| Reporting | Report every selector, selected IDs, selection rate, outcomes, costs, failures, missingness, and pressure status. No arm deletion or label pooling. |

## Allowed comparator differences

A fair comparison does not require identical scoring equations. It requires the same information availability and candidate/budget/opportunity conditions, with each policy restricted to its declared signal. S2's frequency-only and S3's reuse-probability-only rules are intentionally simpler; they are not deprived of the shared candidate record or technical data. Oracle S7 has latent truth by definition and is therefore an analysis-only ceiling.

## Special baselines

- **S5 always-create:** capacity-limited to eight of twenty using an outcome-independent order; not “create all 20” under a common eight-slot budget.
- **S6 never-create:** zero selected by definition. Report its zero-value anchor; do not represent its 0% rate as pressure failure.
- **S7 oracle:** inaccessible truth-based ceiling, excluded from production comparisons and selection-pressure calculation.
- **Memory-only:** not part of this RQ2 selector contest. The 13C raw trace memory and 13F B2 memory/skill-store are not interchangeable. Memory/abstraction budget matching belongs to the Phase 1D/5 benchmark, not a silently altered Phase 1B comparator.

Any parity deviation makes the affected comparison unavailable until resolved before confirmation. If it is discovered after outcomes are accessed, preserve the run and report the deviation; do not repair by selectively rerunning favorable arms.