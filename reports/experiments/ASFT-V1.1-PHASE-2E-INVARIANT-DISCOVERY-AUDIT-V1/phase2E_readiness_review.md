# ASFT v1.1 Phase 2E — Readiness Review

**Phase ID:** `ASFT-V1.1-PHASE-2E`  
**Package:** `ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1`  
**Scope:** Retrospective Phase 13G invariant-pipeline reconstruction and support-sensitivity replay on saved Phase 2C discovery traces. No new ARC search, test-output parsing, scoring, or historical outcome modification.

## Executive decision

- **Phase 2E: PASS as an invariant-discovery audit and stage-observability exercise.** All seven audit gates are operationalized and machine-readable.
- **Empirical invariant readiness: NOT ESTABLISHED.** No production candidate or final semantic ARC invariant is observed. Phase 2 overall remains **BLOCKED**.
- The key historical failure is measurable: 3 successful traces entered Phase 13G mining; four exact operation signatures recur before thresholding, but their maximum support is 3. The current 5/5 extraction thresholds therefore force zero raw patterns, structures, candidates, and final invariants.
- Relaxed support 2 yields four patterns and two structures on the historical/S3/S4 traces (also S2), but those are control-flow/verification fragments; both candidate proposals are rejected by `universal_noise`. No accepted production candidate results.
- A separate validator diagnostic with generation filters bypassed confirms stage instrumentation: 2 proposals enter validation on the historical/S3/S4 sources, of which 2 reach the structural F-C-G `VALIDATED` tier; none is transfer-verified or promotable. This uses the same traces, is not a production path, and does not establish semantic truth. False-discovery rate is not estimable.
- **Failure classification: F6 mixed; F7 primary causal attribution unresolved.** The data cannot say whether meaningful ARC invariants do not exist. It shows the observed trace pool is too small to satisfy current support rules and that relaxed mining extracts generic trace scaffolding rather than demonstrated domain rules.

## Core research questions

| Question | Finding | Claim ceiling |
|---|---|---|
| R2E-1 Can invariant candidates be generated? | At support 2, two proposals per source (except S1) are mapped from structures; both are rejected before production validation. | These are generic procedure fragments, not meaningful ARC invariant candidates. |
| R2E-2 Are recurring structures present? | Yes, exact operation n-grams recur at support 2–3 before filtering. | Recurrence is of trace-control operations; semantic ARC recurrence is not established. |
| R2E-3 Are support thresholds eliminating candidates? | Yes. Support 5 exceeds max observed support 1–3 and yields zero patterns. | Threshold 5 is incompatible with this trace supply, not proven globally unreasonable. |
| R2E-4 Miner or upstream scarcity? | Mixed: input is sparse; support blocks Stage 4; lowering support lets extraction/aggregation run. | Miner efficacy on a sufficient, semantically grounded corpus remains untested. |
| R2E-5 If candidates exist, do they survive validation? | Production: no candidates reach validation. Diagnostic bypass: F-C-G structural states appear in some conditions; no transfer verification or promotion. | Same-corpus diagnostic, outcome-derived family labels, and no independent truth mean no validation of semantic correctness or FDR. |

## Readiness gates

| Gate | Status | Evidence |
|---|---|---|
| I1 — Invariant taxonomy frozen | **PASS** | I1–I6 definitions and evidence requirements in `invariant_taxonomy.md`. |
| I2 — Recurrence measurable | **PASS with semantic boundary** | Signature-level pre-filter recurrence and support distributions reported. |
| I3 — Candidate generation measurable | **PASS** | Fragments→patterns→structures→proposals→rejections logged by condition. |
| I4 — Support thresholds auditable | **PASS** | Current 5, relaxed 2, strict 6 swept with other settings frozen. |
| I5 — Validation measurable | **PASS for stage observability; quality unavailable** | Diagnostic candidate states/scores recorded; production denominator zero; FDR and independent generality unavailable. |
| I6 — Discovery yield measurable | **PASS** | Trace/pattern/candidate/validation denominators and per-stage yields reported. |
| I7 — Failure localization operational | **PASS for observed stages; primary cause unresolved** | Support attrition and downstream rejection localized without automatic blame. |

## Final decision and next evidence needed

Phase 2E **passes as an audit** because recurrence, threshold effects, candidate generation, rejection, validation states, yield, and zero denominators are separable and observable. It does **not** pass as evidence that ASFT discovered meaningful invariants. Before any mechanism claim, a separately authorized diagnostic should provide substantially more successful, diverse discovery traces; independently label semantic task families; audit the `universal_noise` and support policies without outcome-derived family labels; and evaluate candidate consistency, generality, and false discovery on an independent predeclared set. No confirmatory evaluation is authorized by this report.