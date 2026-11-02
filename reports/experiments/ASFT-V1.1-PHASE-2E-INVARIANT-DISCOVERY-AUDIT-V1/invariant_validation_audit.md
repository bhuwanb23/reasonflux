# Phase 2E.6 — Invariant Validation Audit

## Frozen production path

Under the current support floor, **zero candidates are generated**, so the production validator receives zero inputs. Validation survival is `NOT_ESTIMABLE_ZERO_CANDIDATES`, not 0%. At relaxed support 2, two candidate proposals per eligible source are rejected before validation by the candidate-generation `universal_noise` rule; they also do not enter the ordinary validator.

## Separate validator diagnostic (not a production result)

To audit validator observability, Phase 2E reran the default validator in memory on the relaxed-S2 structures with only candidate-generation rejection bypassed. These diagnostic candidates are derived and “validated” on the same three successful traces; they are not real production candidates and cannot demonstrate generality or truth.

| Source | Diagnostic proposals | Structural F-C-G `VALIDATED` | Transfer-verified | Promotable | Notes |
|---|---:|---:|---:|---:|---|
| Phase 13G historical | 2 | 2 | 0 | 0 | Both have C=1, code G=1, T=0, R=0; score 0. |
| S2 | 2 | 0 | 0 | 0 | Frequency score 0.2 is below default 0.3; T=R=0. |
| S3 | 2 | 2 | 0 | 0 | Both have C=1, code G=1, T=0, R=0; score 0. |
| S4 | 2 | 2 | 0 | 0 | Same three discovery successes as S3. |
| S1 | 0 | 0 | 0 | 0 | Only one trace; no recurring proposal. |

The validator's `VALIDATED` state is its structural **frequency/consistency/generality (F-C-G)** tier. In this diagnostic, its G input derives from program-family labels attached to the same traces; those labels are not independent semantic task families. A candidate can reach this structural tier while failing the separate transfer and reasoning-value gates. Here all diagnostic proposals have transfer score 0 and reasoning-value score 0; none are transfer-verified or promotable. This is an implementation-stage result, not a claim that the patterns are true invariants.

- **V1 Consistency:** Exact signature recurrence gives 1.0 on the same traces used to propose it; in-sample and not independent.
- **V2 Generality:** Code-level family score is available, but independent generality is `NOT_ESTIMABLE` because family labels are solver/program-derived and no independent validation split is authorized.
- **V3 Survival:** Production path has no validator denominator; relaxed candidates fail generation. Diagnostic F-C-G state survival is recorded above; promotion survival is 0/2 in each nonempty diagnostic source.
- **V4 False discovery rate:** `NOT_ESTIMABLE_NO_INDEPENDENT_TRUTH_LABELS`; no candidate truth labels or independent oracle exist.

The audit demonstrates that validation stages and zero denominators can be made observable, but **candidate quality and false-discovery performance remain unvalidated**. See `candidate_and_validation_details.csv` and `validation_diagnostic_summary.csv`.