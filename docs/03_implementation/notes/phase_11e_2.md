# Phase 11E-2 notes — Capability Growth Measurement

## Assumptions

- Per-capability \(C_t\) reuses CapU components (SU, TS, CCov, composition)
  with weights from `GrowthConfig` (`growth:` in `thresholds.yaml`).
- System \(C_t\) is the mean of non-archived capability scores.
- CGR / CA are finite differences with default \(\Delta t = 1\).
- IG is a weighted sum of CGR + component growths (TG, UG, CCG, CompG).
- Positive growth claims must pass evidence / robustness checks.

## Success criteria (implementation)

- CGR sign matches capability trajectory (positive / zero / negative).
- IG moves with CGR and component deltas under default weights.
- All five failure modes are detectable via `audit_growth`.
- Portfolio sync can opt in to writing `cgr` / `capability_score` without
  mutating history when `write_growth=False` (default).

## Non-goals (later phases)

- Formal intelligence ontology / prediction (11E-3).
- Evaluation harness dashboards (11E-4).
- Extended capability failure suite beyond growth measurement guards (11E-5).
