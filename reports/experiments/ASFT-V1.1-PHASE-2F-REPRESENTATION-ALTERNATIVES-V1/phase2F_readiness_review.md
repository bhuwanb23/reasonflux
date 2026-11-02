# ASFT v1.1 Phase 2F — Readiness Review

**Phase ID:** `ASFT-V1.1-PHASE-2F`  
**Package:** `ASFT-V1.1-PHASE-2F-REPRESENTATION-ALTERNATIVES-V1`  
**Scope:** specification of representation alternatives and fair comparison/attribution methods. **No alternative was implemented or benchmarked.** No ARC search, test-output parsing, test scoring, or accuracy measurement occurred in Phase 2F.

## Executive decision

- **Phase 2F: PASS as a representation-alternatives framework.** The registry, taxonomy, endpoints, common budgets, downstream activation states, comparison matrix, and attribution rules are specified.
- **Empirical comparison readiness: NOT YET READY.** R2–R7 and HCC are design specifications only. Their code, grammar hashes, adapters, shared independent family annotations, a prospective untouched task set, and numerical practical margins still need pre-run freeze/QA.
- **No result on the representation hypothesis:** historical evidence strongly shows low coverage under the deployed bounded ten-program implementation. It does not show that representation is the sole/primary cause, nor that a richer alternative will activate invariants or skills.
- The primary proposed contrast is **R1 (current bounded representation) vs R3 (object-centric)** under the common Phase 2C S4 cap and unchanged downstream pipeline. R2, R4–R6 are component contrasts; R7 is a multi-factor hybrid and is later-only. HCC is a plumbing positive control, not ARC evidence.
- **Phase 2 overall remains BLOCKED.** This specification does not authorize confirmatory evaluation or accuracy testing.

## Research questions

| Question | Phase 2F answer | Boundary |
|---|---|---|
| R2F-1 Does representation affect coverage? | Framework specifies paired found-fit coverage and matched-task estimates. | Effect not measured. |
| R2F-2 Does it affect trace generation? | Valid/successful trace endpoints and schema contract are specified. | Alternatives not implemented. |
| R2F-3 Does it affect invariant discovery? | Frozen support/miner pipeline and candidate-yield endpoints are specified. | Family labels/adapters require independent freeze; no comparison run. |
| R2F-4 Can downstream failures persist despite coverage gains? | Yes; activation table reports every stage and permits coverage-gain/downstream-blocked outcomes. | Not empirically tested. |
| R2F-5 Is representation primary, contributing, weak, mixed, or unresolved? | Attribution rule set is frozen, with B1–B5 outcomes. | Current evidence leaves primary attribution unresolved. |

## Readiness gates

| Gate | Status | Evidence / remaining work |
|---|---|---|
| RA1 — Registry complete | **PASS (specification)** | R0, R1, R2–R7, HCC recorded with primitives, object/relation/composition model, search interface, status, and limits. |
| RA2 — Alternatives specified | **PASS (design only)** | Finite proposed alternatives and parameter/segmentation assumptions are specified; implementation hashes pending. |
| RA3 — Coverage comparison possible | **PASS (framework)** | Test-output-blind paired exact-demo-fit endpoint, common task requirement, budgets, statuses, and paired analysis specified. |
| RA4 — Trace comparison possible | **PASS (framework)** | One trace/task-condition, max-four-step contract, independent validator, success/diversity/support metrics specified. |
| RA5 — Invariant comparison possible | **PASS (framework, annotation dependency)** | Same Phase 2E miner/thresholds and stage counts specified; shared independent family labels/adapter need pre-run freeze. |
| RA6 — Activation comparison possible | **PASS (framework)** | Coverage→trace→invariant→skill→transfer→capability eligibility and separate accuracy states defined. |
| RA7 — Bottleneck attribution possible | **PASS (framework)** | B1–B5 criteria frozen; margins and task set must be preregistered before execution. |

## Evidence and next authorization gates

The 2B–2C search sensitivity results weaken a representation-only story: within the unchanged representation, demo fits increase from 2 to 5 to 10 per 1,000 as the candidate cap expands, although the ten-program fullscan remains at 1%. Phases 2D–2E show that successful trace supply and recurrence are independently weak and that support5 is unreachable; these are additional barriers between coverage and mechanism activation.

Before any comparison run: implement/hash the registered alternatives and HCC; freeze one common prospective task set disjoint from representation development. All 1,000 Phase 2C task IDs have already been inspected in earlier coverage/trace/invariant audits, so reruns on them are diagnostic only; the historical Phase 13G holdout is also not pristine confirmation. A confirmatory comparison requires a new authorized untouched common split. Resolve the legacy R0/R1 naming crosswalk; preflight equal search/resource budgets and independent trace validation; freeze common semantic family annotations, trace/invariant/skill adapters, `δ_coverage` and activation margins, bootstrap seed/multiplicity; verify coverage code cannot access test outputs; authorize sealed accuracy separately.

**Final decision:** Phase 2F passes as the requested framework, not as an empirical representation test. The question “does a large coverage gain activate the ASFT chain?” is now operationally testable, but remains unanswered.