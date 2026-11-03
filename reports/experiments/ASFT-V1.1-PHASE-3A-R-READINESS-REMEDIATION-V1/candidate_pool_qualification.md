# Phase 3A-R — Candidate Pool Qualification

**Gate 1 status: BLOCKED.** The audited workspace has no qualified real RQ1 invariant-candidate registry. The available actual ARC task files do not substitute for a candidate pool.

## Inventory evidence

- The Phase 1C `N=40` A–H population is a deliberately engineered synthetic contract fixture. It is excluded from this qualification.
- The Phase 2E candidate-generation audit is the relevant real-ARC R1-path evidence. Under historical/current/relaxed/strict and S1–S4 audited conditions, accepted invariant candidate count is **0**. Relaxed-support proposals are rejected as `universal_noise`; no candidate reaches independent validation. Phase 2B likewise records zero C4 invariant candidates across all 1,000 ARC tasks in both budgeted and fullscan modes.
- Phase 2C's 3.36 MB `candidate_trial_log.csv` records attempts over bounded programs (`identity`, etc.), demo-fit results and trial fingerprints. These are program-search trials, not invariant candidate cards, and cannot be relabeled as an RQ1 candidate registry.
- Historical Phase 13B/EXP-IDT-14 candidate pools are synthetic. They cannot replace the missing real pool or establish natural pressure.

A header-only `candidate_registry_template.csv` is provided with the requested candidate ID, source, creation date, eligibility, deduplication, family, version, canonical hash, exposure and feature-hash fields. It intentionally contains **zero invented candidate rows**.

## G1.1–G1.4 checks

| Requirement | Evidence | Status |
|---|---|---|
| G1.1 Candidate registry | No accepted candidates in audited ARC R1 path; no source/creation/eligibility/dedup/family/version registry | **FAIL / missing** |
| G1.2 Task registry | 1,000 task metadata rows hash-verified in `task_registry_inventory.csv`; not a qualified FNTU pool | **PARTIAL** |
| G1.3 Opaque-ID audit | ARC task IDs are source IDs; no candidate IDs or ranker payload exists to audit | **NOT TESTABLE for candidates** |
| G1.4 Diversity | Candidate family/source/coverage/difficulty distributions cannot be measured with zero accepted candidates; task family and difficulty annotations are absent | **NOT ESTABLISHED** |
| Lineage | Source commit/hash exists for ARC files and historical Phase 2 reports; candidate-to-trace lineage is absent | **FAIL / missing** |

## Decision

Gate 1 does not pass. No real candidate pool exists to pressure-test. The 40 synthetic cards are explicitly excluded; there is no outcome-blind basis to generate or curate a substitute pool from the inspected outputs. Remediation requires an authorized candidate-generation pathway that produces eligible actual candidate records, a frozen deduplication/eligibility rule, and complete trace/source lineage. If the invariant pipeline still returns zero candidates, report that result and keep the gate blocked—do not lower support thresholds after seeing outcomes.