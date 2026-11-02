# ASFT v1.1 Phase 1H — Readiness Report

**Phase ID:** `ASFT-V1.1-PHASE-1H`  
**Package:** `ASFT-V1.1-PHASE-1H-BASELINE-ABLATION-SPEC-V1`  
**Scope:** cross-phase baseline, ablation, comparison, and research-governance framework  
**RQ:** Not applicable — governance/specification phase.

## Executive decision

- **PASS for specification layer.**
- **PASS for contract layer — 50/50 checks.**
- **BLOCKED for empirical execution.**
- **RQ not applicable.** No Phase 1B–1G experiment was run or unlocked by this package.

## Historical baseline audit

Phase 14F's read-only synthesis finds comparator-specific evidence, not a global winner. Memory/retrieval survives as a strong alternative in Phase 13C: raw MEMORY_ONLY net value `1.325` vs SCT `.345`, but applications were `440/440` vs `223/440`; the gap combines attempt frequency and correctness, and this MEMORY_ONLY variant is not the same as later skill-store or ARC memory baselines. Frequency-only ties informed/no-transfer ranking in corrected 13B, and a frequency-only policy ties ASFT on 13F outcomes. B4 compression proxy narrowly defeats the corrected 13D transfer-utility gate; 13E/13F favor ASFT on their distinct joint endpoints. No-learning/never-create are useful controls but not sufficient alone; ASFT loses to B1 on task utility in 13E/13F. Random controls sometimes tie when selection degenerates. Hybrid memory+frequency remains an untested mandatory comparator. Oracle is analysis-only.

Degenerate comparisons are explicit: 13B ranked identically across ASFT/frequency/no-transfer; 13C selected `44/44` candidates and RANDOM_CREATE probability was `1.0`; 13F selectors each constructed four of four candidates; 13G arms all scored `1/200` holdout accuracy while coverage prevented mechanism activation, with a budget mismatch and same-holdout reuse caveats. These findings motivate a non-informative-comparison label, not a posthoc win.

## Frozen framework

The package defines baseline families B1–B7 and mandatory BL1–BL7; maps nine ablations A1–A9 to major claims; freezes fairness dimensions (tasks, candidate pool, budget, storage, compute, horizon, exposure, evaluator, config/runtime parity); measures eligible/offered/selected/attempted/completed opportunities; and requires comparator activation/divergence reporting. The framework allows ASFT to win, tie, lose, be unavailable, or have a non-informative/invalid comparison. Ablations may show positive, no measurable, negative, inconclusive, or unavailable contribution.

## Attribution and interpretation

A positive score difference is not attributable to a component unless the comparison is fair, the component is manipulated and activated, candidate/decision divergence is measured, the endpoint is frozen, and relevant surviving alternatives are included. Identical decisions are non-informative for a selection claim. A tie is no demonstrated advantage (equivalence only inside SOI); unavailable is not zero; metric growth is not theory validation; ablation contribution is local, not universal necessity; synthetic success is not external validity.

## Readiness gates

| Gate | Status | Evidence / outstanding work |
|---|---|---|
| Gate 1 — Baseline taxonomy/registry | **PASS specification** | Seven families, mandatory BL1–BL7, subtypes and source qualifications. |
| Gate 2 — Ablation taxonomy | **PASS specification** | A1–A9 and claim mapping, including separate SCT and SCV removals. |
| Gate 3 — Fairness checks | **PASS contract/interface** | 9 parity dimensions; known mismatch fails; missing audit evidence unavailable. |
| Gate 4 — Comparator activation | **PASS contract/interface** | Identical choices, divergent choices, unmatched pool/opportunities, and no denominator distinguished. |
| Gate 5 — Interpretation rules | **PASS specification** | Frozen tie/unavailable/metric/theory/external-validity and local-ablation rules. |
| Gate 6 — Governance | **PASS specification/contract** | Preregistration and no post-outcome changes; governance preflight paths tested. |
| Gate 7 — Frozen registry | **SPECIFIED; NOT EXPERIMENT-POPULATED** | Global registry exists; each 1B–1G preregistration must populate/version its own concrete implementations. |
| Gate 8 — Replication | **PENDING PER EXPERIMENT** | Replication must use disjoint confirmatory/replication manifests and frozen versions; Phase 1H performed no empirical replication. |
| Empirical execution | **BLOCKED** | No new baseline, ablation, or task outcomes generated. Each experiment still needs implementation readiness and separate authorization. |

## Final decision

> Phase 1H has a frozen governance framework and 50/50 passing contracts. It demonstrates that the comparison system can represent ASFT wins, ties, losses, unavailable results, ablation nulls, and non-informative identical decisions. It does not demonstrate that IDT/SCT works, that memory loses, that capability/intelligence is valid, or that any baseline is empirically superior across phases. A future positive claim must name its comparator and prove fairness and activation.