# ASFT v1.1 Phase 2C — Readiness Review

**Phase ID:** `ASFT-V1.1-PHASE-2C`  
**Package:** `ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1`  
**Scope:** historical Phase 13G search/budget audit plus frozen, test-output-blind Phase 2C budget sensitivity and runtime-integrity benchmark.  
**Accuracy:** `NOT_MEASURED_BY_DESIGN`.

## Executive decision

- **Phase 2C: PASS for search inventory, prospective budget registry, enforceable runtime integrity, test-blind search trace measurement, and budget sensitivity.**
- **Phase 2 overall remains BLOCKED.** Phase 2C does not clear representation alternatives, confirmatory/evaluation authorization, or downstream ASFT mechanism gates.
- **Historical audit:** declared Phase13G candidate cap 3 differed from discovery execution (10). Stability added ten more searches/task, each cap10. Historical B4 runtime and B5 memory limits were not configured or logged.
- **New Phase 2C run:** budget parity, config/runtime/log hashes, memory/runtime ceilings, and deterministic replay all PASS.
- **Sensitivity:** found-fit coverage was 2/1,000 (0.20%) at cap3; 5/1,000 (0.50%) at cap6; 10/1,000 (1.00%) at cap15/all-ten. Invariants remained zero in all conditions. More search helps coverage within this finite DSL; it does not establish the cause of ARC failure or accuracy.

## R2C research questions

| Question | Answer | Boundary |
|---|---|---|
| R2C-1 — Can search behavior be reproduced exactly? | **Yes for the instrumented Phase 2C runner:** all 4,000 primary task-condition searches matched deterministic replay; S3=S4 task fingerprints. Historical 600 discovery choices and saved stability values also reproduce exactly. | A replay validates determinism, not independent evidence. Phase13G's original per-permutation logs were incomplete. |
| R2C-2 — Are declared and executed budgets identical? | **Yes for Phase 2C B1–B6. No for Phase 13G discovery B1.** | S3's cap15 is logged as 15, while the finite unique DSL contains only ten candidates; that is pool exhaustion, not a hidden budget change. |
| R2C-3 — How much coverage loss is due to search? | The fixed-representation cap contrast recovers 8 additional demo fits when moving from 3 to all 10 candidates (2→10/1,000). | Specific to found-demo-fit coverage under R0; not accuracy or a general causal claim. |
| R2C-4 — Can search be separated from representation? | The candidate-cap effect on C1 is paired and separated within the unchanged representation. | Representation vs search as root causes remains unresolved until a matched R0×R1 design. |

## Readiness gates

| Gate | Status | Evidence |
|---|---|---|
| S1 — Search inventory complete | **PASS** | `search_inventory.csv` covers generation, inference, evaluation, ranking, pruning, selection, termination, trace expansion, stability, mining, arm routing, and coverage scans. |
| S2 — Budget registry frozen | **PASS** | `budget_registry.yaml` is the runtime source of truth; config/registry parity is checked before execution. Historical mismatch is separately preserved. |
| S3 — Runtime integrity enforceable | **PASS** | R1–R4 hashes, OS memory cap, per-search wall limit, budget audit, fail-closed mismatch policy, and replay verification are active. |
| S4 — Search trace benchmark defined | **PASS** | 4,000 primary task-condition logs, ordered candidate trials, 4,000 valid traces, and replay log. |
| S5 — Budget sensitivity measurable | **PASS** | S1/S2/S3/S4 coverage measured under matched task IDs and unchanged representation. |
| S6 — Search vs representation audit defined | **PASS with causal limit** | Paired cap effect measured; representation cause and any richer DSL effect remain unresolved. |
| S7 — Reporting standard frozen | **PASS** | `search_reporting_standard.md` freezes required budgets, logs, metrics, statuses, and accuracy separation. |

## Integrity summary

Config, registry, runtime, search logs, candidate-level attempts, replay records, and budget audit have recorded SHA-256 fingerprints. **Runtime parity: PASS.** Candidate/replay fingerprints matched 4,000/4,000. S3 and S4 match because the DSL contains only ten unique candidate programs. Peak RSS was 97.6 MiB under a 2,048 MiB process address-space limit; maximum task-condition search was under 0.487 seconds under a 30-second cap. Each condition used 1,000 primary tasks and 1,000 replay searches; replay does not enter coverage denominators. The benchmark parsed only task training demonstrations; no test-output field or accuracy was accessed.

## Final decision

**Phase 2C PASS for audit and search-budget measurement readiness.** It establishes that more candidate search recovers some exact-demo fits under the bounded Phase13G representation and prevents future declared/executed/logged budget drift through machine checks. The all-ten ceiling remains only 1.0%; no invariant candidate appears. Thus search contributes to observed coverage attrition, but whether broader representation is the primary remaining bottleneck is not identified. Phase 2 remains BLOCKED; no confirmatory ARC performance test or ASFT efficacy claim is authorized.