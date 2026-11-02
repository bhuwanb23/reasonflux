# ASFT v1.1 Phase 1D — Full Memory-Challenge Audit

**Phase ID:** `ASFT-V1.1-PHASE-1D`  
**Package:** `ASFT-V1.1-PHASE-1D-MEMORY-CHALLENGE-SPEC-V1`  
**Scope:** retrospective memory audit, benchmark specification, and design/schema contracts.  
**Decision:** **PASS for specification/contract layer; scientific benchmark NOT READY; RQ3 UNTESTED.**  
**New experiments/outcomes:** none.

## 1. Why Phase 1D is needed

Phase 13C's memory-only result is a serious alternative explanation for skill abstraction: mean net value **1.325** for `MEMORY_ONLY` versus **0.345** for SCT, paired SCT-minus-memory **−0.980** (seed-bootstrap 95% CI **[−1.020, −0.940]**). Memory applied 440/440 eligible opportunities and was correct on 418; SCT applied 223/440 and was correct on 201, with 22 failures and 217 no-matches. Correct/eligible was 0.950 vs 0.457. This is a strong Phase-13C result, not universal memory superiority.

## 2. Source-level correction to the “exact replay” description

A direct read of the saved Phase 13C implementation (`source_snapshot/phase13c_sct_frozen/part_02.txt`) shows `_evaluate_memory_only`:

1. selects the first source trace whose operations include the target invariant pattern;
2. extracts a single macro operation from that trace (an `apply_*` op, `count_objects`, or `group_by_color`); and
3. applies that macro to ten eligible task opportunities.

It does not simply retrieve and replay a full solution keyed to each repeated test task. Phase 14C's interpretation calls this exact retrieval, but the operative saved path is more accurately **raw-trace-exemplar / partial-macro memory**. The Phase 1D taxonomy preserves M1 exact episodic as a distinct new arm rather than retroactively assigning the Phase 13C arm to M1.

## 3. What explains the historical advantage?

The observed denominator is 440 eligible opportunities; this was not a larger eligible-task denominator for memory. The realized **application coverage** differed: memory applied on all 440, SCT only on 223 and had 217 no-matches. Memory's correct count was 418 vs SCT 201. That is direct evidence of better coverage/correctness in that setting. It does not identify whether the cause was retrieval, broad macro applicability, repeated task structure, operation-level alignment, or selection policy.

The primary net-value cost terms are simulator-normalized creation/maintenance proxies. They are not byte-matched storage, measured FLOPs, or wall-clock compute. Historical protocols also do not supply a common instrumented budget ledger across exact memory, raw exemplar macro, and abstract skills. Therefore the numerical win cannot be interpreted as a clean resource-matched causal estimate of “memory vs abstraction.”

Phase 13F's `B2_MEMORY_SKILL_STORE` is a distinct arm and protocol: Phase 14C reports task utility 0.715 and CGR 0 vs ASFT 0.789906 and 0.287172. This is not an exact replication and should not be pooled with Phase 13C net value. Phase 14H keeps memory as a live, incompletely controlled alternative.

Source records: [Phase 13C summary](../PHASE-13C-SCT-V1/summary.md), [Phase 13C evidence](../PHASE-13C-SCT-V1/evidence_package.md), [Phase 13C implementation snapshot](../PHASE-13C-SCT-V1/source_snapshot/phase13c_sct_frozen/part_02.txt), [Phase 14C memory interpretation](../PHASE-14C-SCT-CRITICAL-ANALYSIS-V1/memory_interpretation.md), [Phase 14F baseline analysis](../PHASE-14F-BASELINE-ABLATION-CRITICAL-ANALYSIS-V1/phase14f_baselines_ablations_analysis.md), and [Phase 14H cross-contribution analysis](../PHASE-14H-CROSS-CONTRIBUTION-ANALYSIS-V1/phase14h_cross_contribution_analysis.md).

## 4. Benchmark design created

- **Five distinct memory/abstraction representations:** M1 exact episodic, M2 partial episodic, M3 pattern memory, M4 skill abstraction, M5 hybrid.
- **Six challenge families:** A exact replay; B context shift; C composition shift with a case-specific parameter; D structural analogy; E far transfer; F adversarial retrieval.
- **All required arms:** memory-only suite B1a–c; abstraction B2; hybrid B3; random retrieval B4; no learning B5; Oracle B6 post-lock only.
- **Common ceilings:** same training exposure, byte storage, item slots, construction/query compute, retrieval inspections, and future task horizon. Actual use and costs must be instrumented.
- **Primary endpoint:** HNU macro-average over B–F, with Family A as a separate memory-positive control. Compare M4 against each of M1/M2/M3; do not select a favorable memory variant after confirmation.
- **Leakage exception made explicit:** Family A uses a planned training demonstration whose task is deliberately repeated in a future query. This is the exact-replay treatment, not accidental exposure. B–F may not have future task keys, answers, or traces in memory.
- **Splits/replication:** development, confirmatory, and replication; all families occur in confirmatory and replication blocks.

## 5. Contract suite and evidence boundary

The contract runner reports **26/26 PASS** for schema and design assertions: family definitions, separate memory types, family A exposure, B–F abstraction challenges, composition/hybrid condition, common resource caps, budget-overrun handling, comparator presence, hidden-label API checks, split-family coverage, and leakage exception declarations.

**No task solver ran. No arm won a Phase 1D task.** The contracts do not show that M1 beats M4 on A, that M4 beats M1–M3 on B–F, or that M5 beats both in C. Those are challenge hypotheses, not results. The development-stage task-derived generator and policy implementations are still to be built and tested. The current contract runner does not provide fake outcome tables or claim the challenge families' anticipated winners have been observed.

## 6. Remaining gates

1. Implement a task generator/base solver with task-derived gold values, disjoint future tasks, and all six challenge families.
2. Implement and instrument B1a–c, B2, B3, B4, B5, and post-lock B6; demonstrate common caps and measured resource use.
3. Validate the family constructions on development data without using confirmatory/replication outcomes.
4. Calibrate utility/cost coefficients, partial-credit rules, missingness, and SOI on allowed calibration/development data.
5. Freeze exact N using a cluster-level power/precision simulation; freeze code/data/config hashes and analysis.
6. Implement storage/retrieval/exposure audits and a sealed outcome store; independently verify Family A allowlist and no B–F leakage.
7. Freeze the preregistration and obtain independent review before confirmatory access; replicate on disjoint seed/template blocks.

## 7. Final decision

> **Phase 1D specification and design/schema contracts: PASS. Scientific benchmark execution: BLOCKED. RQ3 evidence: NONE.**

Phase 1D now specifies how to test when memory is sufficient, abstraction is useful, and a hybrid may complement both. It has not yet answered those scientific questions. No confirmatory testing, Phase 3 IDT evaluation, or SCT experiment is authorized by this package.