# ASFT v1.1 Phase 3A — IDT Implementation Readiness

Package: `ASFT-V1.1-PHASE-3A-IDT-IMPLEMENTATION-READINESS-V1`

## Decision

**BLOCKED** for Phase 3B calibration/freeze and Phase 3D confirmation. Implementation/package QA passes; actual-candidate pressure, independent FNTU evaluation, calibrated cost/λ, and production outcome-store sealing are not evidenced. No IDT efficacy claim is made.

## Required reports

1. [Historical IDT audit](historical_idt_audit.md)
2. [Ranker validation](ranker_validation_report.md)
3. [Candidate pool validation](candidate_pool_validation.md)
4. [Ranking pressure validation](ranking_pressure_validation.md)
5. [Endpoint validation](endpoint_validation_report.md)
6. [Leakage and isolation audit](leakage_audit.md)
7. [Fairness audit](fairness_audit.md)
8. [26-contract revalidation](contract_revalidation_report.md)
9. [Readiness review](phase3A_readiness_review.md)
10. [Mentor review and unlock-gate disposition](mentor_review.md)

The mentor review accepts Phase 3A as implementation plumbing, concurs with **BLOCKED / not authorized** for Phase 3B and Phase 3D, and records six remaining unlock gates. No Phase 3B calibration or freeze has been performed.

## Executable development artifacts

- Engine: `experiments/phase3a/benchmark_engine.py`
- Contract runner: `experiments/phase3a/run_contracts.py`
- Machine-readable re-run: `experiments/phase3a/contract_results.json`

Re-run from the repository root: `PYTHONPATH=src python experiments/phase3a/run_contracts.py`. The runner intentionally uses synthetic development fixtures; its PASS status is plumbing evidence only.
