# Phase 2G.4 — Protocol Integrity Review

| Check | Status | Evidence and remaining limitation |
|---|---|---|
| **P1 Config/runtime parity** | **PASS for Phase 2C; historical mismatch preserved** | Phase 2C B1–B6 config/registry/runtime/log parity passed. Phase 13G declared cap3 but discovery defaulted to 10; this historical mismatch is not retroactively fixed. New representation runs have not occurred. |
| **P2 Budget logging** | **PASS for Phase 2C diagnostics** | Configured caps, available inventory, actual trials, first-fit skips, replay, runtime, and memory are separated. Historical runtime/memory were not configured/logged. Alternative grammar candidate budgets remain to implement and verify. |
| **P3 Holdout protection** | **BLOCKED for confirmatory evidence** | Phase 13G attempt02 reused the same holdout after attempt01 generated predictions in memory; it is not pristine. All Phase2C task IDs have been seen in earlier test-blind coverage/trace/invariant audits. No new authorized untouched common split is available in Phase2F. |
| **P4 Outcome isolation** | **PASS for Phase 2B–2F diagnostic runners** | 2B/2C use training demonstrations only; 2D/2E reconstruct saved logs/traces; 2F is specification only. Historical Phase 13G scored task test outputs and combined coverage/test paths. Do not claim official ARC evaluation data were scored; do not claim no evaluation bytes were ever downloaded. |
| **P5 Coverage reporting** | **PASS with bounded-language label** | Exact training-demo fit is separately reported from accuracy in 2B/2C. Report as found-fit coverage within a named language, search budget, and parameter implementation—not semantic representability. |
| **P6 Failure reporting** | **PARTIAL** | Current pipeline records no-fit, valid/successful trace, recurrence, support, and empty downstream stages. Root representation attribution, independent semantic family labels, candidate truth/FDR, and alternative-stage failures remain unresolved. |
| **P7 Version control/provenance** | **PASS for completed audit packages; pending for alternatives** | Phases 2A–2F package manifests/hashes exist; Phase2C run parity and replay passed. R2–R7/HCC have no implementation hashes because they are not built. |

## Integrity decision

Phase 2B–2E descriptive diagnostics are interpretable within their frozen scopes. Phase 13G historical results remain useful only with the documented budget, holdout, first-fit, and logging caveats. Phase 2F does not yet provide an executable representation contrast. Therefore protocol integrity is **acceptable for retrospective diagnostics but insufficient for confirmatory ARC mechanism testing**.