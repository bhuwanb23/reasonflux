# ASFT v1.1 Phase 2A — Representation Audit

**Phase ID:** `ASFT-V1.1-PHASE-2A`  
**Package:** `ASFT-V1.1-PHASE-2A-REPRESENTATION-AUDIT-V1`  
**Scope:** read-only audit of the Phase 13G ARC representation and specification of falsifiable alternatives. No ARC tasks were rerun.

## Start here

- [`phase2A_readiness_review.md`](phase2A_readiness_review.md) — Phase 2A decision and Phase 2 overall gates.
- [`historical_representation_audit.md`](historical_representation_audit.md) — exact Phase 13G representation, coverage, trace, budget, and failure findings.
- [`representation_bottleneck_assessment.md`](representation_bottleneck_assessment.md) — B1–B4 evidence rating, with causal limits.
- [`search_representation_interaction.md`](search_representation_interaction.md) — search vs representation decomposition and required future dataflow.
- [`representation_requirements_v2.md`](representation_requirements_v2.md) — R0/R1/HCC alternative-condition requirements for Phase 2B–2F.
- [`missing_concepts_audit.md`](missing_concepts_audit.md) — source-evidenced missing/partial concepts; no guessed ARC prevalence.

## Machine-readable audits

- [`primitive_inventory.csv`](primitive_inventory.csv) — all ten Phase 13G candidate programs plus input, auxiliary, helper, and trace layers.
- [`expressivity_matrix.csv`](expressivity_matrix.csv) — what each primitive can/cannot express and its bounded evidence.
- [`arc_coverage_audit.csv`](arc_coverage_audit.csv) — split-specific fit counts and explicitly unknown/non-operationalized categories.

## Provenance

- [`source_manifest.json`](source_manifest.json) and [`source_hashes.csv`](source_hashes.csv) — fingerprints for audited historical sources and Phase 2A deliverables.
- [`provenance_validation.md`](provenance_validation.md) — QA status.

## Evidence boundary

The saved full-inventory rates (3/600 discovery, 5/200 transfer, 2/200 holdout) are exact fits to demonstrations under a bounded ten-program implementation, not test accuracy or ARC semantic family prevalence. `unsupported_v1` means no fit found within that implementation, not proof of unrepresentability. The historical discovery path used ten candidates despite a configured budget of three. This package does not fix, rerun, or validate that system and does not authorize confirmatory ARC testing.