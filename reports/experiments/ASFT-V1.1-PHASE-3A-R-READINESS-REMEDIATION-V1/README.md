# ASFT v1.1 Phase 3A-R — Readiness Remediation

**Package:** `ASFT-V1.1-PHASE-3A-R-READINESS-REMEDIATION-V1`  
**Disposition:** **BLOCKED**; all six authorization gates are not closed. Phase 3B and Phase 3D remain unauthorized.

This is a source-audited remediation assessment, not a benchmark run. It distinguishes verified workspace artifacts from missing RQ1 candidate/task data, and calls out the feature-definition conflict that prevents silently freezing a changed R1 score.

## Reports

1. [Candidate pool qualification](candidate_pool_qualification.md)
2. [Task pool qualification](task_pool_qualification.md)
3. [Feature lineage freeze audit](feature_lineage_freeze.md)
4. [Actual-pool pressure report](actual_pool_pressure_report.md)
5. [FNTU evaluator validation](fntu_evaluator_validation.md)
6. [Sealed outcome store audit](sealed_outcome_store_audit.md)
7. [Power and precision plan](power_precision_plan.md)
8. [Phase 3A-R readiness review](phase3A-R_readiness_review.md)

## Machine-readable audit artifacts

- `candidate_registry_template.csv` — required schema, intentionally no fabricated candidate rows.
- `task_registry_inventory.csv` — hash-verified inventory of historical ARC task files, explicitly unassigned and ineligible for new confirmation.
- `split_assignment_template.csv` — no C1–C4 assignments are made.
- `feature_lineage_matrix.csv` — Phase 1C vs Phase 3A-R feature semantics and blockers.
- `inventory_audit.json` — counts, hashes, and source reconciliation.
- `package_manifest.json` / `provenance.json` — package QA and source hashes.

Read-only inventory command: `PYTHONPATH=src python experiments/phase3ar/audit_inventory.py`. It reads source/split manifests and the Phase 2B test-blind audit ledger; it does not parse task payload outputs or run the solver.