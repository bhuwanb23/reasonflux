# ASFT v1.1 Phase 2B — Readiness Review

**Phase ID:** `ASFT-V1.1-PHASE-2B`  
**Package:** `ASFT-V1.1-PHASE-2B-ARC-COVERAGE-BENCHMARK-V1`  
**Method:** frozen, test-output-blind descriptive coverage benchmark of the unchanged Phase 13G representation.  
**Scope boundary:** no accuracy computation, no confirmatory ARC efficacy test, and no changes to Phase 13G historical outputs.

## Executive decision

- **Phase 2B: PASS for coverage definition, coverage-only execution, stage measurement, trace audit, and reporting readiness.**
- **Phase 2 overall ARC Foundation Readiness: BLOCKED.** Phase 2B does not clear holdout, alternative-representation, causal-attribution, empirical mechanism, or confirmatory evaluation gates.
- **Headline:** 2/1,000 task demonstrations (0.20%) fit within the declared three-candidate budget; 10/1,000 (1.00%) fit in the ten-program diagnostic fullscan. All 1,000 tasks received independently validated trace records; successful traces were exactly 2 and 10 respectively. The actual invariant miner emitted zero candidates in both modes. Skill, transfer eligibility, and capability stages were not run because no invariant candidate was available.
- **Localization:** observed pattern F5 (mixed); causal/root-cause attribution F6 (unresolved).
- **Accuracy:** `NOT_MEASURED_BY_DESIGN`.

## Research-question answers

| Question | Phase 2B result | Boundary |
|---|---|---|
| R2B-1 — How much ARC is representable under current representation? | 10/1,000 (1.00%) found a demo-fit in the all-ten bounded scan. | Operational finite-scan fit only; not semantic representability. |
| R2B-2 — How much is discoverable under current search budget? | 2/1,000 (0.20%) fit within three candidates. | Uses declared production budget and fixed Phase 13G order; no test outputs. |
| R2B-3 — What reaches each stage? | C2/C3: 1,000/1,000 trace emitted/valid; successful C3: 2 budgeted, 10 fullscan; C4: 0; C5–C7: 0 reached / blocked. | Downstream conditional rates are not estimable because their upstream pool is empty. |
| R2B-4 — Where does pipeline fail? | Sparse C1/C3, loss under three-candidate search, and no repeated signatures at C4. | Mixed observed losses; primary cause unresolved absent alternative representation and matched factorial test. |

## Readiness questions and gates

| Gate | Status | Evidence |
|---|---|---|
| C1 — Coverage definition frozen | **PASS** | `coverage_definition.md` freezes finite representation+search-budget exact demo-fit; accuracy is explicitly excluded. |
| C2 — Coverage stages measurable | **PASS with blocked-stage labels** | 1,000 task rows include C1–C7 for budgeted/fullscan, including unavailable/blocked statuses and denominators. |
| C3 — Budgeted benchmark defined/executed | **PASS** | Frozen budget of three; 2/1,000 (0.20%) exact demo fits. |
| C4 — Fullscan benchmark defined/executed | **PASS (diagnostic only)** | All ten programs; 10/1,000 (1.00%) exact demo fits; no accuracy claims. |
| C5 — Trace yield measurable | **PASS** | 100% emitted and independently validated; successful trace rate 0.20% budgeted / 1.00% fullscan. |
| C6 — Failure localization operational | **PASS for stage localization; attribution unresolved** | F5 mixed observed attrition; F6 causal/root-cause state retained. |
| C7 — Coverage separated from accuracy | **PASS** | Runner parses training demonstrations only; accuracy not measured; separate report field says `NOT_MEASURED_BY_DESIGN`. |

## Integrity and limitations

The Phase 2B runner reads the frozen split manifest and uses a fail-closed streaming parser that stops after each task's training demonstrations. It independently checks training-grid schema, exact demo fit, trace structure, and trace outcome. The 1,000 task files matched the supplied ARC source manifest hashes. The run manifest records code/config/protocol/dataset-manifest hashes and confirms test-output fields were not parsed or used. The historical holdout reuse remains a limitation: these descriptive coverage counts do not restore pristine confirmatory status.

The fullscan reproduced Phase 13G's saved demo-fit totals (3/600, 5/200, 2/200). Relative to it, the budgeted mode found two of ten task IDs with any fullscan fit; eight additional fits needed candidates beyond the first three. This is a within-implementation search-budget contrast, not evidence that a larger budget resolves general ARC coverage.

## Exit decision

**Phase 2B PASS for its coverage-measurement objective.** Coverage is operationally defined, measured separately from accuracy, stratified by budget/fullscan and split, traced, and localized through the first empty invariant stage. The benchmark documents rather than repairs the low-coverage bottleneck. Phase 2 overall remains **BLOCKED**; this phase does not authorize confirmatory tests or establish representation as the primary cause.