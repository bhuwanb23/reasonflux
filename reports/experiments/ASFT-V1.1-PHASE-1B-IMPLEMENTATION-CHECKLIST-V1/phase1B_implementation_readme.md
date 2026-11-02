# Phase 1B implementation contract package

This package supplements the benchmark specification at `ASFT-V1.1-PHASE-1B-SELECTION-PRESSURE-SPEC-V1` with an executable selector/pressure contract harness.

## Main file

- [`phase1B_readiness_report.md`](phase1B_readiness_report.md) — readiness decision, contract summary, pressure results, pairwise matrix, and remaining unlock gates.
- [`phase1B_full_audit_report.md`](phase1B_full_audit_report.md) — full forensic audit, correction log, detailed CT table, outcome-response audit, and current readiness boundary.

## Requested audit outputs

- [`contract_test_results.csv`](contract_test_results.csv) — 26/26 contract results.
- [`pairwise_divergence_matrix.csv`](pairwise_divergence_matrix.csv) — pairwise decision-set divergence for the development fixture.
- [`pressure_validation_report.md`](pressure_validation_report.md) — standalone validation report with thresholds, results, divergence matrix, limitations, and confirmatory boundary.
- [`outcome_response_sanity_report.md`](outcome_response_sanity_report.md) — demonstrates the fixture metric can report a win, tie, or SCV loss; not study evidence.
- [`outcome_response_sanity.csv`](outcome_response_sanity.csv) — per-policy fixture values/type counts supporting the report.
- [`pressure_validation.json`](pressure_validation.json) — 100-fixture pressure check summary and selector sets.
- [`phase1B_contract_checklist.csv`](phase1B_contract_checklist.csv) — contract and final unlock gate status.
- [`source_manifest.json`](source_manifest.json) and [`source_hashes.csv`](source_hashes.csv) — refreshed provenance inventory and SHA-256 hashes for source/evidence files.

## Code

- `experiments/phase1b/selection_benchmark.py` — selector interfaces, separate truth record, score, and pressure gate.
- `experiments/phase1b/run_contracts.py` — reproducible contract runner; invoke from repository root:

```bash
python experiments/phase1b/run_contracts.py reports/experiments/ASFT-V1.1-PHASE-1B-IMPLEMENTATION-CHECKLIST-V1
```

## Scope warning

These are synthetic contract fixtures, not calibration or confirmatory SCT outcomes. The development pressure fixtures use one deterministic candidate-feature/type recipe and vary the random-policy seed. They verify implementation behavior under the specified interface, not population validity, cost calibration, statistical power, or whether SCV wins. The future Phase 4 evaluation remains blocked until the run-specific N, data/config/code hashes, analysis code, and sealed confirmatory store are frozen.
