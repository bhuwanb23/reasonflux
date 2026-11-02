# ASFT v1.1 Phase 1G — Full Audit and Specification Report

**Phase:** `ASFT-V1.1-PHASE-1G-ARC-GENERALIZATION-SPEC-V1`  
**Primary question RQ6:** Can the invariant→skill→transfer→capability chain activate on ARC under a protocol-conformant representation with measurable downstream benefit?  
**Status:** specification and contract report; no new empirical ARC evaluation.

## 1. Executive decision

- **Specification layer: PASS.** All requested independent stage specifications, representation/protocol controls, preregistration, and readiness rules are documented.
- **Contract layer: PASS, 42/42 checks.** Stage/accuracy separation, zero vs unavailable, config/runtime budgets, holdout reuse, and chain response paths pass the contract runner.
- **Empirical execution: BLOCKED.** No new ARC search, task evaluation, or confirmatory/replication outcomes were produced.
- **RQ6: UNTESTED.** Phase 13G remains historical evidence, not a Phase 1G benchmark result.

## 2. Historical ARC audit and cascade

Phase 13G used 1,000 public ARC-AGI-2 training task IDs split 600 discovery/200 transfer/200 holdout. The fixed DSL contained ten primitive programs. Full-inventory demo-fit counts were 3/600, 5/200, and 2/200; these are representation/fit coverage, not accuracy. There is a material source/config discrepancy: frozen config says three candidates per task, but `discover()` defaults to ten. A separate reporting defect labels prefix sizes 100–600 as `n_successful_traces`; the actual successful exact-fit count is three. All 600 discovery trace rows were schema-valid; only three were successful exact-demo-fit traces. The invariant miner saw three examples with support one each against a threshold of five and emitted zero raw patterns/candidates. No eligible program or skill passed; learned-skill transfer denominator was zero; capability groups were zero and C_t/CGR/IG unavailable. ASFT bounded transfer accuracy was 0/200. Holdout accuracy was 1/200 across all five arms, but attempt 01 generated predictions in memory and attempt 02 reused the same holdout after a serialization fix. It is not independent replication. B2 nearest-episode retrieval solved one transfer task and is not invariant-derived skill transfer.

Phase 14G concludes the tested implementation has very low representation coverage and a downstream support bottleneck, but representation is not proven as the sole cause. Phase 14I/14J classify ARC validity as unestablished for ASFT; Phase 14H finds no external validation of the complete causal chain. The official evaluation JSON was not extracted or scored, but a temporary archive containing evaluation blobs was downloaded for reconnaissance; only filenames were listed before deletion.

The stage map in `arc_failure_cascade.csv` distinguishes (a) observed successful ingestion/schema, (b) low coverage, (c) zero invariant candidates with insufficient support, (d) blocked skill formation, (e) unavailable learned-skill transfer/capability metrics, (f) separately observed poor task accuracy, and (g) unrun official evaluation. It does not convert the cascade into a theory verdict.

## 3. Benchmark design

Representation variants are versioned and semantically auditable; additional primitives are not presumed beneficial. A direct representation-bottleneck test compares the historical adapter to a justified alternate/reference condition under matched task IDs and budgets, or demonstrates a sufficiently high-coverage regime. Budgeted demo-fit coverage and any exhaustive diagnostic scan remain separate.

Each stage has a distinct measure and denominator: task ingestion, representation coverage, trace schema/success, discovery candidates/diversity, invariant validation/survival, skill formation/promotion, eligible skill transfer/utility/negative transfer, Phase 1E behavioral capability, and exact/partial/family accuracy. Unknown/ambiguous ARC semantic families stay explicit. Independent blind annotations are reference data, not unquestionable ground truth. Zero invariant counts are reported as zero; if successful traces/support are insufficient, the test is inconclusive rather than theory failure. Transfer with no eligible skill denominator is unavailable, not zero.

## 4. Protocol-integrity design

C1–C5 explicitly address Phase 13G: one-source configuration/runtime budget parity; separate diagnostic full scans; prelocked and single-use holdout with no debugging/reuse; isolated evaluator/test gold and no CGM target inputs; transparent coverage/accuracy denominators; and complete failure logging. Automated preflight checks config/call/runtime counters. A failed integrity gate blocks confirmatory interpretation; rerunning on the same holdout cannot repair it.

The current contracts are API/design checks only. They do not implement a sealed gold store, file access control, full ARC solver, new representation, human annotation workflow, or production audit.

## 5. Outcome-response and construct separation

Contracts demonstrate that the benchmark can express coverage high/accuracy low, coverage low/accuracy low, chain activated, a stage break, unavailable transfer, and inconclusive support. These are constructed code-path cases only, not ARC outcome fixtures or evidence. The benchmark can conclude that an adequate-coverage representation still fails at invariant, skill, transfer, capability, or accuracy. It can also conclude representation remains unresolved when no adequate coverage regime is reached.

Coverage scoring uses demonstration fit and search logs; accuracy scoring uses held-out test outputs and independent gold. They are computed by separate interfaces. The outcome schema rejects IG/IGR/IE/CGR/C_t and internal capability/transfer fields. Capability follows Phase 1E external behavior criteria, not internal C_t/CGR.

## 6. Remaining gates

Implement the frozen task parser/search/evaluator; select and justify representation variants; establish double-blind annotation with unknown labels allowed; complete development-only threshold and precision calibration; freeze budgets, candidate limits, splits, baseline definitions and sample size; seal held-out gold; confirm access isolation and one-time holdout handling; then obtain separate authorization before any confirmatory or replication run. Phase 1G completion does not authorize Phase 3/IDT or SCT experiments.

## 7. Bottom line

> The framework is designed to identify whether failure occurs at coverage, trace generation, invariant discovery, skill formation, transfer, capability formation, or task accuracy, and does not assume representation is the sole bottleneck. The specification and contract layer pass. Whether the chain activates on ARC remains entirely untested in Phase 1G.