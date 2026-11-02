# Phase 2G.7 — Phase 2 Exit Decision

## Decision: **PARTIAL — diagnostic foundation improved; ARC mechanism testing remains blocked**

### Phase 2 gate assessment

| Exit condition | Status | Rationale |
|---|---|---|
| Representation documented | **PASS** | Phase 2A inventories the bounded language and limits; Phase 2F registry specifies alternatives. |
| Coverage measurable | **PASS** | Phase 2B/2C test-blind found-fit coverage runs and reporting exist. |
| Search auditable | **PASS for current R1 diagnostics** | Phase 2C parity/replay pass; historical 13G mismatch is explicitly preserved. |
| Traces measurable | **PASS as diagnostic** | Phase 2D reports generation, validity, success, diversity/support; successful substrate remains sparse. |
| Invariant discovery measurable | **PASS as pipeline audit; PARTIAL as empirical test** | Phase 2E localizes support attrition and candidate stages, but no meaningful production candidate or independent validation exists. |
| Protocol integrity acceptable | **PARTIAL** | Current diagnostics are auditable/test-blind; historical holdout reuse remains and no fresh alternative comparison set is ready. |
| Failure localization possible | **PARTIAL** | Attrition is localized within the existing R1 pipeline, but primary representation/search/downstream attribution remains unresolved. |
| Alternative representation comparison possible | **PARTIAL / NOT EXECUTION-READY** | Phase 2F framework is complete; alternatives and HCC are not implemented, no fresh split, independent family annotations or adapters frozen. |
| ARC mechanism-level testing ready | **BLOCKED** | No adequate invariant candidate pool, skills, transfer-eligible skills, or capability units. |

## Why not PASS?

The stated Phase 2 success claim—being able to determine whether ARC failure arises from representation, search, trace generation, invariant discovery, or downstream activation—would overstate the evidence. The current R1 pipeline is much more diagnosable, but the key representation contrast has not run, meaningful invariant validation is unavailable, and downstream mechanism denominators remain zero. A future experiment may still localize these causes, but only after the Phase 2F implementation and data gates are satisfied.

## Authorization

**Do not proceed to confirmatory Phase 3/SCT or ARC mechanism testing.** Phase 2 can be considered complete only as a diagnostic/specification program with a **PARTIAL** exit, not as ARC Foundation Ready. Any later unlock requires a new review after the remaining prerequisites are executed and QA-passed.