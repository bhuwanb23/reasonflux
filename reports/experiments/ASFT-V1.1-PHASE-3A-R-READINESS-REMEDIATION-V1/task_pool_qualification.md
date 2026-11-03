# Phase 3A-R — Task Pool Qualification

**Task inventory exists; qualified Phase 3A-R task pool and split assignment do not. Gate 1 remains blocked.**

## Read-only inventory result

A read-only manifest reconciliation produced `task_registry_inventory.csv` from the ARC-AGI-2 source/split manifests and the Phase 2B test-blind schema ledger:

- Source: ARC-AGI-2 repository commit `f3283f727488ad98fe575ea6a5ac981e4a188e49`.
- Manifest count: 1,000; all 1,000 source task files match their manifest SHA-256; all 1,000 have a Phase 2B `schema_valid=True` record.
- Historical split: 600 discovery / 200 transfer / 200 holdout.
- Target Phase 3A-R eligibility: not established for every row; new calibration/development/confirmatory/replication assignments: **0**.
- Task-family annotations: 0; difficulty-tier annotations: 0.

This inventory did not parse ARC task payloads or test outputs, run solvers, or calculate task outcomes. “Schema valid” is the prior Phase 2B structural audit status, not evidence of future-task endpoint suitability.

## Exposure and split integrity

All 1,000 task IDs have prior Phase 2B/2C audit exposure. The historical holdout block also appears in Phase 13G, whose attempt-02 report documents reuse after attempt 01 had generated predictions in memory. These tasks may be considered for **development/debugging only** subject to the existing exposure caveats; they are not a pristine C3 confirmatory or C4 replication set. Existing ARC files are public training tasks with target outputs in the source data, not a sealed future-outcome collection.

No Phase 3A-R split has been assigned. The historical `discovery/transfer/holdout` labels are not silently reinterpreted as C1–C4. Existing Phase 13C calibration/confirmation seeds and Phase 13D synthetic-transfer task rows belong to different protocols and are not substitutes for RQ1 split blocks.

## G1.2 qualification matrix

| Required field | Current evidence | Status |
|---|---|---|
| Task ID / source / version hash | Present for all 1,000 source tasks | PASS as historical inventory |
| Family assignment | Not in manifest / independently annotated | OPEN |
| Difficulty tier | Not frozen or audited | OPEN |
| Eligibility for candidate-level transfer / common FNTU horizon | Not evaluated | OPEN |
| Split assignment C1/C2/C3/C4 | None; no disjoint assignment | OPEN |
| Prior exposure | Phase 2B/2C known; Phase 13G exposure for old holdout recorded | PASS as disclosure; disqualifies pristine confirmation |
| Paired evaluator / task horizon | Not available for Phase 1C RQ1 | OPEN |

## Decision

The task files are real and hash-verified, but this does not create a qualified benchmark population. Before use, define family/difficulty labels independently, eligibility, task-instance/family disjointness, a new C1–C4 assignment, and an independently evaluated FNTU horizon. Do not call the historical holdout “locked” or “sealed”; it is exposed in files and prior reports.