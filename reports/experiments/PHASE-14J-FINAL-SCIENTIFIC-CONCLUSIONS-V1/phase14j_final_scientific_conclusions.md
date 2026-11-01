# Phase 14J — Final Scientific Conclusions

**Review ID:** `PHASE-14J-FINAL-SCIENTIFIC-CONCLUSIONS-V1`  
**Scope:** Final synthesis of the ASFT v0.1 research program, including Phase 11–12 implementation records, Phase 13 experiments/evidence consolidation, and Phase 14A–14I audits.  
**Method:** evidence synthesis only. No experiments, metrics, or analyses were added; no Phase 13 outputs were modified.  
**Status:** complete.

## Deliverable index

- [Final Claim Classification](final_claim_classification.csv)
- [Final Scientific Scorecard](final_scientific_scorecard.csv)
- [Publication Claim Ceiling](publication_claim_ceiling.md)
- [Future Research Priorities](future_research_priorities.md)
- [Source/hash manifest](source_manifest.json) and [hash list](source_hashes.csv)

## 14J-1 — Research program and evidence boundary

ASFT v0.1 proposed three contributions—Invariant Discovery Theory (IDT), Skill Creation Trigger Theory (SCT), and Capability Growth Metrics (CGM)—within a broader chain:

`Experience → Invariant Discovery → Skill Formation → Transfer → Capability Growth → Intelligence Growth`

The program has produced both **implementation evidence** and **scientific evidence**, and these must not be conflated:

- The saved Phase 11 completion note reports all 24 modules implemented, six MVP gates demonstrated, and 501 tests passing. It also records substantial implementation corrections and states that tasks were synthetic, with one capability cluster and a single seed/four rounds at that stage. This supports a working research prototype and software test coverage; it is not proof of the scientific theory.
- The repository's Phase 12 file is an implementation plan/checklist discussion, not a separate confirmatory experiment. Its planned gates and closure language are useful for tracing design intent, but should not be treated as independent evidence that every scientific acceptance criterion passed.
- Phases 13B–13G supply empirical evidence with different tasks, endpoints, comparators, and limitations. Phase 13H consolidates that record. Phases 14A–14I audit integrity, individual contributions, transfer, baselines, ARC, cross-contribution claims, and validity threats.

The result is not a single experiment that tests the full causal chain. Evidence for adjacent links is drawn from distinct, bounded synthetic studies; later links show important inconsistencies or construct-validity limits.

## 14J-2 — Final claim classification

### Contribution 1: IDT

| Claim | Final verdict | Defensible reading |
|---|---|---|
| **IDT-1: useful invariants emerge from experience** | 🟡 Supported narrowly in synthetic scope | Phase 13B repeatedly recovers operation-level signatures aligned with the known generator vocabulary. This is not open-ended or blinded invariant discovery. |
| **IDT-2: IS predicts future transfer** | ❌ Not established | A small early association is not robustly reproduced; corrected 13D is near-zero/non-positive, and ARC has no estimable IS–TS relationship. |
| **IDT-3: transfer-aware ranking beats frequency-only/no-transfer** | ❌ Primary gate failed | Corrected 13B policies tie on the primary top-k endpoint and semantic ordering. EXP-IDT-14 shows sensitivity to a deliberately injected frequent no-op, but is exploratory and cannot repair the failed primary gate. |

### Contribution 2: SCT

| Claim | Final verdict | Defensible reading |
|---|---|---|
| **SCT-1: skills form from validated synthetic candidates** | 🟡 Supported narrowly as pipeline behavior | Phase 13C constructs 44 reflection/rotation skill instances and records reuse. This does not prove that invariant triggering is necessary or uniquely responsible for value. |
| **SCT-2: SCV predicts future skill value** | 🟡 Partial association; incremental validity unestablished | SCV is associated with future value in one sample, but frequency and `p_reuse` are at least as strongly associated; selection does not discriminate in the primary pool. |
| **SCT-3: SCT outperforms naive creation** | ❌ Not supported on the primary superiority criterion | SCT ties ALWAYS_CREATE and RANDOM_CREATE in 13C; memory-only is stronger on that protocol's net-value endpoint. Later baselines differ, so this is not a universal memory verdict. |

### Contribution 3: CGM

| Claim | Final verdict | Defensible reading |
|---|---|---|
| **CGM-1: capabilities emerge and grow** | 🟡 Partially supported as metric behavior | Phase 13E has positive C_t/CGR in its cohort, but one capability object persists and its score/membership changes; corrected 13D mean CGR is negative. This is not robust ontological capability growth. |
| **CGM-2: capability growth predicts future performance** | 🟡 Weak, within-cohort predictive evidence only | The preregistered 13E C_t→next-round task-utility association is positive and small (`r=0.0498`, cluster CI `[0.0163,0.0922]`). It is not causal or external. This result is distinct from transfer→CGR, which is inconsistent across phases. |
| **CGM-3: IG measures intelligence growth** | ❌ Not established | Positive IG/IGR are outputs of internal formulas; IE trends downward; no independent intelligence criterion validates these constructs. |

## 14J-3 — End-to-end causal chain

### What survives

> **Controlled synthetic experience → recurring operation-level trace patterns → construction of reflection/rotation skill objects → some successful skill reuse and reduced simulator reasoning-step cost.**

This is a **narrow operational subchain**, assembled across controlled synthetic evidence. It is not open-ended invariant discovery, selection-policy superiority, broad transfer, or one end-to-end mediation test.

### Where the chain first becomes unestablished

**Transfer → Capability Growth** is the first major missing causal bridge. Transfer events and step-cost proxy reductions are observed, but corrected 13D/13E/13F evidence does not establish that transfer causes or reliably predicts capability growth. Positive capability scores in one cohort do not fill this gap.

**Capability Growth → Intelligence Growth** is also unvalidated. `C_t`, CGR, IG, IGR, and IE are repository-defined internal metrics; no independent measure establishes that they capture broad capability or intelligence growth.

### Final chain verdict

| Original chain link | Final status |
|---|---|
| Experience → Invariant | Narrow synthetic operation-pattern support |
| Invariant → Skill | Narrow operational construction support; necessity/selection value not established |
| Skill → Transfer | Narrow synthetic reuse and step-cost proxy support |
| Transfer → Capability | Not established; first major evidential break |
| Capability → Intelligence | Not established; construct validity absent |
| **Entire chain** | **Not validated** |

## 14J-4 — ARC verdict

Phase 13G is the strongest external-validity attempt in this program, but it is a test of a bounded adapter, not an official ARC-AGI-2 evaluation score or an unrestricted ASFT theory test.

- Full ten-program exact demonstration fits: discovery `3/600`, transfer `5/200`, holdout `2/200`. These are demo-fit coverage counts, not task accuracy or semantic ARC-family rates.
- All 600 discovery records are schema-valid, but only three successful exact-fit traces enter mining; invariant candidates, skills, and capabilities are zero.
- **IG is unavailable, not a measured zero**, because no validated capability group exists.
- A source audit found a material budget mismatch: frozen config declares three candidates per task, while `discover()` defaults to ten. The `3/600` discovery count is therefore a full-inventory yield; only the reflection fit among the three saved discovery programs is among the first three fixed candidates.
- Scored ASFT exact transfer accuracy is `0/200`; learned-skill precision is unavailable because there are no applicable skills. B2's one transfer success is episodic memory. All five arms have `1/200` holdout accuracy; the same frozen holdout was reused after attempt 01 generated predictions in memory.

**Final ARC verdict:** ASFT external validity on ARC is **not demonstrated**. Low task/program coverage and sparse successful traces are the dominant proximate failures of this implementation, but the experiment does not isolate representation from other causes or falsify IDT/SCT/transfer/CGM in general.

## 14J-5 — Strongest positive findings

1. **Synthetic operation-pattern recurrence:** repeatable detection of generator-aligned operation signatures under a known vocabulary.
2. **Synthetic skill-object construction:** reflection and rotation skill objects form from validated candidates and are stored.
3. **Synthetic reuse:** successful positive-credit skill applications are recorded, including attempted cross-family cases within the reflection/rotation pool.
4. **Simulator step-cost reductions:** positive reasoning-step proxy savings are measured in 13C/13D; not wall-clock, FLOPs, or solver-search savings.
5. **Implemented research infrastructure:** Phase 11 records module implementation, six MVP gates, and 501 passing tests. End-to-end synthetic pipeline execution is demonstrated at the implementation level, but the complete theory chain is not scientifically validated.

## 14J-6 — Strongest negative or limiting findings

1. **Transfer-aware ranking superiority:** primary 13B gate failed; exploratory stress-test evidence remains exploratory.
2. **SCT selection superiority:** no advantage over always/random creation in the 13C primary pool; candidate decisions degenerate to selecting all.
3. **Memory alternative:** survives as a serious comparator, especially in 13C; it is not proven universally superior because opportunity counts and later implementations differ.
4. **Capability-growth theory:** internal metric values rise in 13E, but cross-phase CGR/transfer evidence is mixed and capability object count does not broadly grow.
5. **Intelligence-growth theory:** not established; positive composite indices lack external construct validation and IE trends negatively.
6. **ARC mechanism replication:** not demonstrated by the bounded, low-coverage adapter; downstream mechanisms were unavailable after the upstream bottleneck.
7. **Complete causal chain:** not established; the first three links have narrow operational evidence, while C4/C5 remain unresolved.

## 14J-7 — What was actually learned?

### Lesson 1: mechanism operation is not theory validation

A module can detect patterns, create skill objects, or execute reuse without establishing that the named theory is uniquely responsible, superior to simpler baselines, or general beyond the designed task population.

### Lesson 2: candidate and decision pressure determine what a comparison can identify

The 13B rankers and 13C skill-creation policies often make identical decisions. Their ties are meaningful within the frozen pools, but offer little leverage for estimating an advantage of transfer-aware ranking or SCV-based selection. Memory and compression remain comparator-specific alternatives.

### Lesson 3: internal metrics need independent construct validation

Positive CGR/IG does not equal broader competence or intelligence. Metric behavior, capability object count, task performance, and external construct validity must remain separate.

### Lesson 4: external representation is a prerequisite to testing downstream mechanisms

The ARC adapter's low coverage and budget inconsistency prevent a meaningful test of downstream ASFT mechanisms. This is an implementation/external-validity result, not proof of an exclusive representation cause or a general theory failure.

## 14J-8 — Final research contribution

The strongest defensible contribution of ASFT v0.1 is **an implemented, inspectable synthetic research framework and a bounded proof of concept**: in controlled grid-task environments, it can detect recurring operation-level patterns, construct reflection/rotation skill objects, and record successful reuse with lower simulator reasoning-step cost. It also produces capability-oriented internal metrics and supports baselines/ablations that expose where proposed mechanisms do not add measurable value.

The work does **not** yet establish a unified learning theory. It does not demonstrate transfer-aware ranking superiority, SCT selection superiority, a causal transfer-to-capability-growth mechanism, validated intelligence growth, or ARC generalization. The honest contribution includes both the positive synthetic behaviors and the well-documented limits, nulls, competing explanations, and implementation failures.

## 14J-9 — Publication claim ceiling

> **“In controlled synthetic grid-task environments, the implemented ASFT pipeline repeatedly detects operation-level structures aligned with the generator, constructs reflection/rotation skill objects, and records successful reuse with reductions in a simulator reasoning-step cost proxy. The evidence does not demonstrate transfer-aware ranking or SCT selection superiority, a causal transfer-to-capability-growth effect, validated intelligence growth, or ARC generalization. Repository-defined capability and intelligence metrics rise in one synthetic cohort but lack independent construct validation. The bounded ARC adapter has very low task/program coverage and does not instantiate the downstream mechanism chain.”**

Anything stronger—especially claims of general invariant discovery, intelligence growth, or ARC replication—would exceed the evidence. See [publication claim ceiling](publication_claim_ceiling.md) for a standalone version.

## 14J-10 — Future research priorities

These are priorities for future work, not new analyses or changes to the present evidence:

1. **Representation and protocol alignment:** expand ARC-compatible representations and traces under a separately preregistered, internally consistent search budget.
2. **Selection pressure and competing mechanisms:** construct candidate pools with real positive/negative choices; test rank/selection policies against frequency, memory/retrieval, and compression comparators without conflating implementations.
3. **Capability validation:** evaluate capability claims against independent behavioral breadth, persistence, and transfer outcomes rather than only internal composite movement.
4. **External evaluation:** test out-of-generator tasks and independent datasets; treat ARC as a fresh confirmatory evaluation only after an adapter's representation and protocol are specified and validated.

## 14J-11 — Final scientific scorecard

| Area | Verdict |
|---|---|
| Architecture / research framework | 🟡 Implemented prototype; useful testbed, not a validated full theory |
| Implementation | 🟡 Core synthetic pipeline and tests reported; localized defects and ARC budget mismatch remain |
| Reproducibility / audit trail | 🟡 Substantial saved records and hashes; corrections, phase-specific methods, and holdout exposure qualify replication claims |
| Synthetic invariant-pattern detection | 🟡 Supported narrowly within known generator vocabulary |
| Synthetic skill construction and reuse | 🟡 Supported narrowly for reflection/rotation operations |
| Synthetic transfer / step-cost proxy | 🟡 Supported narrowly in generated tasks |
| Transfer-aware ranking superiority | ❌ Primary gate failed |
| SCT / SCV policy superiority | ❌ Not demonstrated in primary pools |
| Memory/retrieval alternative | 🟡 Survives; comparator-specific, not universal |
| Capability-growth interpretation | ❌ Not established as robust capability growth |
| Intelligence-growth interpretation | ❌ Not established |
| ARC validation | ❌ Not demonstrated by bounded adapter |
| External validity | ❌ Not demonstrated beyond tested synthetic scope |
| Full ASFT causal chain | ❌ Not validated end to end |

**Phase 14 exit decision: COMPLETE.** The evidence is sufficient for a carefully scoped paper on an implemented synthetic proof of concept and its limitations. It is not sufficient for the original broad theory claims. The next phase can focus on manuscript strategy while preserving the claim ceiling above.

## Evidence sources

- **Phase 11–12 implementation record:** [Phase 11 completion notes](../../../docs/03_implementation/notes/phase_11_completion.md), [Phase 12 implementation plan](../../../docs/03_implementation/validation/phase_12.md), and [Phase 12 closure checklist](../../../docs/03_implementation/validation/phase_12_closure_checklist.md). The latter two are design/checklist records, not independent experimental results.
- **Phase 13:** [13H master evidence package](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/master_evidence_package.md), [13H IDT package](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_A_IDT.md), [SCT](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_B_SCT.md), [CGM](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_C_CGM.md), [ARC](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_F_ARC.md).
- **Phase 14:** [14A integrity review](../PHASE-14A-EVIDENCE-INTEGRITY-REVIEW-V1/evidence_integrity_report.md), [14H cross-contribution analysis](../PHASE-14H-CROSS-CONTRIBUTION-ANALYSIS-V1/phase14h_cross_contribution_analysis.md), and [14I validity analysis](../PHASE-14I-THREATS-TO-VALIDITY-V1/phase14i_threats_to_validity.md), plus individual contribution reviews listed in the source manifest.
