# ASFT v1.1 Phase 2E — Invariant Discovery Audit Protocol

**Phase:** `ASFT-V1.1-PHASE-2E`  
**Package:** `ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1`  
**Status:** Frozen before Phase 2E analysis. This is a retrospective diagnostic audit, not confirmatory evaluation.

## Scope and data boundaries

Audit only: (1) the 600 saved Phase 13G discovery traces and original mining summary; and (2) successful discovery traces reconstructed from the saved Phase 2C task-condition logs for S1–S4, whose 1,000 task IDs per condition overlap. Do not run ARC search, parse/use test outputs, alter historical outcomes, or combine discovery traces with transfer/holdout traces for mining. No transfer, accuracy, capability, or causal efficacy endpoint is evaluated.

## Stage definitions

1. **Observed recurrence:** exact contiguous operation n-grams after the frozen normalizer/segmenter, counted by distinct successful discovery trace/task IDs before miner support filtering. Report fragments/occurrences separately from distinct-trace support. These are trace-operation patterns, not presumed semantic ARC rules.
2. **Miner patterns:** exact signatures surviving both `MiningConfig.min_frequency` and `min_cross_trace` in Stage 4.
3. **Structures:** output of frozen connected-component aggregation (`min_core_length=1`).
4. **Candidate proposals:** structures mapped to `Invariant` objects before the generator's rejection criteria. Report separately from candidates accepted by the ordinary generation filters and their rejection reasons.
5. **Validation:** candidate-to-validation state counts and the frozen validator scores. No candidate may be treated as a validated ASFT mechanism without independent evidence. If false-discovery truth labels are absent, FDR is `NOT_ESTIMABLE`.

## Support sensitivity

- **Relaxed S2:** support floor 2 distinct successful traces. This is the minimum threshold that can evidence recurrence across independent task IDs.
- **Current S1:** support floor 5, matching Phase 13G `MIN_SUPPORT=5` in extraction and candidate policy.
- **Strict S3:** support floor 6, a minimal stricter stress condition.

For each setting, apply the floor consistently to miner `min_frequency`, `min_cross_trace`, and candidate-policy `min_frequency`. Hold all other settings constant: max fragment length 4; min core length 1; successful-trace bias on; policy consistency 1.0, minimum task families 2, minimum generality 0.0, transfer evidence not required, transfer event floor 0, universal-noise generality 0.95, and the code's remaining default rejection criteria. These are predeclared diagnostic settings, not threshold recommendations. Also run a clearly separated validator plumbing diagnostic at S2 with only generation rejection bypassed; it is not an actual production candidate path and does not authorize promotion.

## Frozen analysis constraints

- Recurrence is computed before validation and independently of invariant/skill scores.
- Family labels present in traces are reported as stored but are not treated as independent ARC semantic family labels; Phase 13G labels are tied to solved-program families.
- No fit/unsuccessful trace is fabricated into a partial trace or pattern-bearing successful trace.
- No support threshold is selected based on post hoc performance. No FDR estimate without independently labeled true/false discoveries.
- `zero`, `not measured`, `not estimable`, `blocked upstream`, and `rejected at a named stage` remain distinct.

## Frozen questions

R2E-1 candidate generation; R2E-2 pre-validation recurrence; R2E-3 support-filter attrition; R2E-4 miner versus upstream scarcity; R2E-5 candidate validation survival. Findings will be limited to observed trace operations and frozen software behavior.