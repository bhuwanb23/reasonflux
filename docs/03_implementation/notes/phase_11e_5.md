# Phase 11E-5 notes — Capability Failure Modes & Robustness

## Delivered

- Package `src/capability/robustness/` with CF1–CF10, CHS/CS, hard gate,
  recovery, and `audit_capability_ecosystem`.
- YAML `capability_robustness:` + `load_capability_robustness_config`.
- Harness `gate_run` uses `validate_growth_claim` when `hard_validation=True`
  (default). Multi-signal hard gate decides acceptance; adjacent-step growth/intel
  audit kinds are still reported in metadata but do not veto a passing claim.
- Docs: `docs/02_design/capability_failure_modes.md`.

## Design choices

- Representation wrappers stay thin; series CF6/CF10/CF5 live in detectors +
  metrics helpers.
- Recovery archives tiny / harmful caps and restores declining → developing;
  archived caps get `restore_requested` metadata (no illegal reverse transition).
- CF8 compares train vs holdout success on snapshots (`train_success` /
  `holdout_success`), typically capability vs ARC-tagged runs.

## Tests

`tests/test_cap_robustness_*.py` — taxonomy, detectors, gates, health, recovery,
audit, overfitting, e2e.

## Next (after 11E-5)

Paper / experiments checklist beyond CGM measurement (explicitly out of scope
for this phase).
