# Phase 14G — ARC Failure Analysis

**Review ID:** `PHASE-14G-ARC-FAILURE-ANALYSIS-V1`  
**Evidence:** saved Phase 13G ARC-AGI-2 public-training split, bounded solver and trace artifacts; Phase 13H ARC synthesis; Phase 13G frozen config/source; disclosed attempt history.  
**Method:** read-only posthoc diagnosis. No reruns, no DSL changes, no threshold changes, and no Phase 13 outputs modified.  
**Status:** complete.

## Deliverable index

- [ARC Root-Cause Analysis](arc_root_cause_analysis.md)
- [Failure Cascade Analysis](failure_cascade_analysis.md)
- [DSL Coverage Analysis](dsl_coverage_analysis.md)
- [Representation Analysis](representation_analysis.md)
- [Theory-vs-Implementation Assessment](theory_vs_implementation.md)
- [ARC Threats-to-Validity Assessment](arc_threats_to_validity.md) and [risk register](arc_threats_to_validity.csv)
- [Revised ARC Claim](revised_arc_claim.md)
- [ARC Failure Scorecard](arc_failure_scorecard.csv)
- [Coverage summary](arc_coverage_summary.csv), [failure cascade table](failure_cascade.csv), and [arm outcomes](arc_arm_outcomes.csv)
- [Source/hash manifest](source_manifest.json) and [hash list](source_hashes.csv)

## Executive verdict

Phase 13G **failed as an attempt to demonstrate ARC learning with the deployed bounded implementation**. It did not validate invariant discovery, ASFT skill formation, learned transfer, capability growth, or IG on ARC. The dominant *proximate* failure is the mismatch between the ARC task distribution and the fixed ten-program symbolic inventory, compounded by support thresholds and the per-arm candidate budget. The invariant-to-skill-to-capability chain did not activate.

That is not the same as proving the broad ASFT theories false. The ARC run did not supply enough qualifying, recurrent task-derived programs to test IDT/SCT/learned transfer/CGM meaningfully. Conversely, it is also too strong to say “only representation failed” or “ARC was not actually analyzed”: 600 discovery tasks were loaded, scanned, and given schema-valid trace records; all 200 transfer and 200 holdout task IDs were scored by the bounded arms; some tasks fit the full DSL; and exact task accuracy remained very low. The **implemented bounded system** has a negative result; the **general theories** remain untested by this pipeline.

### Coverage figures—three different quantities, not one rate

The full-inventory coverage scan tests the complete 10-program DSL and asks whether a program fits the training demonstrations. It finds:

| Split | Full-DSL exact demonstration fits | Rate | Meaning |
|---|---:|---:|---|
| Discovery | `3/600` | `0.5%` | Three tasks yield exact-fit programs; one reflection, one rotation, one recoloring. |
| Transfer | `5/200` | `2.5%` | Five tasks fit some program in the full inventory: one rotation, two transpose/anti-transpose, one translation, one recoloring. |
| Holdout | `2/200` | `1.0%` | Two tasks fit a full-inventory program: one reflection, one rotation. |

**Correction:** `0.5% or lower` is not accurate across all three full-inventory scans; transfer is `2.5%`. These counts are **demo-fit coverage**, not solved-task accuracy and not ARC-wide semantic coverage. The main arms had a three-candidate budget, whereas the coverage scan tested all ten programs, so a task can be in the full-DSL fit count yet remain outside an arm's tested candidate order/budget.

**Budget implementation discrepancy:** frozen `config.json` declares `per_task_candidate_budget=3`, and the preregistration says three distinct program trials per task for arms. But `runner.py`'s `discover()` defaults to budget 10 and is called without an override; the saved discovery fits therefore come from a ten-program discovery scan, not a three-program discovery pass. The coverage table intentionally scans all ten. The scored transfer/holdout arms use three. This stage-specific discrepancy was not presented as an independently verified deviation at run time and is flagged here as a config/protocol-to-code mismatch. It makes `3/600` a full-inventory discovery yield, not the discovery yield under the declared three-candidate limit. From the saved fixed program order and fitted program IDs, only the `reflect_vertical` fit is among the first three programs; thus at most one of the three observed discovery fits would be retained under that declared first-three limit. This is a source-based implication, not a rerun or replacement metric.

### What the scored arms did

- ASFT transfer exact accuracy: `0/200`; B1: `0/200`; B2 episodic memory: `1/200`; B3: `0/200`; B4: `0/200`.
- Holdout exact accuracy: `1/200` for **each** of ASFT, B1, B2, B3, and B4. The single successful holdout task is a reflection solvable by the fixed program inventory; it is not evidence that an ASFT invariant or learned skill was formed.
- Accepted invariants: `0`; ASFT skill candidates/promotions: `0`; validated capabilities: `0`; transfer-precision denominator for learned skills: `0`; IG/CGR: **unavailable**, not zero-valued growth measurements.

The B2 transfer success came from its nearest-episode/raw-discovery-memory route; it does not contradict the zero ASFT invariant/skill inventory. It shows that one memory-style operation can act even when the abstraction pipeline has failed.

## 14G-1 — Locate the first broken link

| Pipeline stage | Saved evidence | Diagnosis |
|---|---|---|
| Task loading and trace-record construction | 600 discovery trace-quality rows; schema-valid rate `100%`; unsupported tasks have recorded failed bounded-search traces | Generic trace serialization/task ingestion ran. This does not mean the traces contain useful solved operations. |
| DSL fit / useful discovery trace | `3/600` full-inventory discovery fits; each successful trace is a different program family, each stable under 10 demonstration-order permutations | First dominant bottleneck: almost all tasks cannot be represented by this program inventory; successful examples are too sparse and heterogeneous. |
| Invariant mining | Miner receives 3 successful traces; `raw_patterns=0`, `structures=0`, `candidates=0`, `rejected=0` | No pattern population existed to qualify. This is not a test that IDT rejects a representative ARC invariant set. |
| Skill formation | `support`: recolor `1`, reflection `1`, rotation `1`; preregistered minimum support is `5`; eligible program pool is empty; zero skills | Skill creation is mechanically downstream-blocked by absent invariant/support. |
| Transfer | Learned-skill applicability denominator `0`; weighted invariant precision `null`; ASFT exact accuracy `0/200`; B2 `1/200` | Learned transfer is unavailable as a mechanism measure; bounded arm-level solving still produced mostly failures. |
| Capability formation | Zero learned skills and zero valid capability groups | Capability proposal cannot activate; zero is an outcome count, but CGM scores are unavailable. |
| IG/CGM | `IG_status=unavailable_no_validated_capability_group`; C_t/CGR/IG blank | No evidence for or against CGM growth on ARC. |

### Reporting-field correction

The saved Phase 13G `growth.csv`/summary rows label a prefix field `n_successful_traces` and show 100, 200, …, 600. Inspection of `experiments/phase13g/runner.py` shows the value is assigned `len(traces)` for the prefix, not the number of successful traces. It must not be cited as 100–600 successful traces. The actual discovery record has **three successful exact-fit traces** among 600 tasks. This is a field-label/reporting defect; the saved underlying trace and task rows make the correct count recoverable.

## 14G-2 — Root-cause assessment

1. **Bounded DSL / task-representation coverage — strongly supported as proximate cause.** The ten-program inventory covers a narrow set of identity, reflection, rotation, transpose, constant translation, and bijective recoloring operations. Full-DSL exact-demo fit is only 0.5% on discovery, 2.5% on transfer, and 1.0% on holdout. Counting, grouping, object detection, and pattern completion are explicitly not operationalized; `unsupported_v1` is an operational category, not a semantic label for what the task “really is.”
2. **Trace representation/schema failure — not supported in the generic serialization sense.** All 600 discovery records are schema-valid, and the three exact-fit traces have recorded stability 1.0 across ten demonstration-order permutations each. However, the operation-level trace representation is limited to the selected primitive program. There is insufficient diversity/repetition for abstraction. Thus “representation bottleneck” is accurate for the **program/task language**, not a claim that the trace schema itself failed.
3. **Invariant support-gate interaction — strongly supported as an immediate downstream blocker.** The miner is configured with `min_frequency=5` and `min_cross_trace=5`; skill support is also `MIN_SUPPORT=5`. The observed successful discovery support is one per program across only three different operations. The threshold and observed pool therefore cannot yield an invariant/eligible skill. Phase 13G does not distinguish whether a broader ARC representation would reveal regularities or whether the invariant formulation itself would fail on those traces.
4. **Candidate ordering/budget — additional implementation limitation and audit discrepancy.** The full-DSL coverage table uses all ten programs; scored transfer/holdout arms are limited to three candidates. The saved discovery code also uses ten candidates despite the frozen config's three-candidate setting, so the discovery fit yield is not budget-conformant with the declared limit. The three successful discovery programs are reflection (third in fixed order), rotation (sixth), and recoloring (tenth); only the reflection case lies within the first three. With empty ASFT skill order and empty qualified B3/B4 operator pools, scored arms fall back to fixed order. Thus the 5/200 and 2/200 full-inventory counts are not arm-level reachable coverage rates, and the 3/600 discovery yield is not the yield at the declared budget.
5. **ARC task difficulty — not isolated.** The results do not support “ARC is intrinsically too hard” as the root cause, but they also cannot rule difficulty out. The proximate observed failure is that the bounded solver often cannot fit the demonstrations with its program inventory; no matched DSL-expansion or difficulty manipulation isolates representation from task complexity.

## 14G-3 — Why synthetic success did not transfer automatically

Synthetic tasks were generated from known operations and shared vocabulary aligned with trace extraction, invariant signatures, skill mapping, and evaluation. In Phase 13G, the inventory contains only ten fixed transforms; the discovery split yields three exact fits, each a different operation. The Phase 13G invariant miner requires at least five occurrences across traces, and skill construction requires support plus at least three applicable transfer tasks. The synthetic-to-ARC gap is therefore not merely “ARC is harder”: the ARC adapter presents a much narrower and differently aligned operational representation, and its fixed support rules then prevent downstream formation.

This comparison supports a **representation-alignment explanation** for why the tested pipeline had no ASFT learning chain. It does not prove that synthetic gains were entirely artifacts, nor establish that richer ARC traces would validate the theory.

## 14G-4 — Theory versus implementation

- **What ARC directly shows:** the 13G bounded adapter had extremely low program coverage, generated only three successful discovery traces, formed no invariant/skill/capability chain, and achieved `1/200` holdout accuracy equally across five arms.
- **What it does not show:** that IDT, SCT, transfer, or CGM are false in general. Their learned ARC pathways were not instantiated. The no-invariant result is constrained by low coverage and a minimum support threshold that the observed data cannot meet.
- **What remains negative evidence:** the deployed 13G implementation did not demonstrate ARC learning or transfer; the bounded system's task accuracy is poor; and baseline arms showed no holdout separation. This is a genuine implementation/external-validity failure, not a success to explain away.
- **What remains undecided:** whether a substantially broader but still pre-registered representation and trace grammar could provide enough independent examples for invariant discovery; whether the current invariant learner can generalize over such structured ARC traces; whether downstream skill transfer then helps task accuracy.

## 14G-5 — Protocol and holdout caveats

Phase 13G uses 600/200/200 disjoint task IDs sampled from the public ARC-AGI-2 training set; this is not an official ARC-AGI-2 evaluation score. Attempt 01 generated predictions in memory before a report-serialization error; no numeric outcome table was persisted or inspected during repair. Attempt 02 fixed serialization on the **same frozen holdout**, so it is not independent replication or pristine holdout confirmation. The user-facing result remains useful as a bounded software/system diagnostic with this exposure caveat.

The disclosed temporary upstream archive contained evaluation blobs; only filenames were listed, no evaluation JSON was extracted, parsed, scored, or used as feedback, and the archive was deleted. Do not claim that no evaluation bytes were ever downloaded.

## 14G-6 — Revised ARC claim

> **“Phase 13G did not demonstrate ASFT invariant discovery, skill-based transfer, capability growth, or intelligence growth on ARC-AGI-2. The dominant proximate failure was extremely low coverage of the fixed ten-program symbolic DSL, compounded by support thresholds and budget inconsistency: although the frozen config declares three candidates per task, the discovery function searches ten. Only three discovery tasks yielded successful exact-fit traces under the full inventory (only the reflection case is within the first three fixed candidates), leaving the invariant-to-skill chain unable to activate. This is a failure of the tested ARC implementation and an external-validity non-result for the higher-level mechanisms—not a direct falsification of IDT, SCT, transfer, or CGM in general.”**

## 14G-7 — Final scorecard

| Question | Status | Evidence |
|---|---|---|
| Did tasks load and produce trace records? | ✅ Yes, bounded-record scope | 600/600 discovery rows schema-valid; all tasks processed by bounded search. |
| Did useful exact-fit discovery traces emerge? | ❌ Nearly absent | 3/600 full-DSL fits found with discovery budget 10; one each reflection, rotation, recoloring. Only reflection is among first three fixed candidates. |
| Was the trace schema itself invalid? | ❌ No | Saved schema-valid rate 100%; useful-operation coverage is a separate failure. |
| Was ARC DSL coverage adequate? | ❌ No | 3/600 discovery, 5/200 transfer, 2/200 holdout full-inventory demo fits. |
| Did ARC invariant discovery succeed? | ❌ No | 3 successful traces enter mining; zero raw patterns/candidates. |
| Did ASFT skills form? | ❌ No | Support 1/program vs minimum 5; zero skills. |
| Did ASFT learned transfer get measured? | ⚪ Unavailable | Learned-skill precision denominator 0; ASFT transfer task accuracy 0/200. |
| Did episodic memory do anything? | 🟡 Narrow event | B2 memory has 1/200 transfer exact task; distinct from learned ASFT skill transfer. |
| Did capabilities/IG form? | ⚪ Unavailable | Zero capabilities; CGM scores blank by design when no valid group. |
| Did holdout performance validate ASFT? | ❌ No | All five arms 1/200 exact accuracy; same-holdout rerun caveat. |
| Does ARC falsify IDT/SCT/transfer/CGM theory? | ❌ No | Upstream coverage/support block means higher-level theories were not meaningfully instantiated. |
| Is the representation bottleneck identified? | ✅ Strongly, for bounded implementation | Low full-DSL coverage plus no support-qualified traces; not a proof of a unique causal root. |

**Exit decision: Phase 14G COMPLETE.** The first decisive failure in the tested pipeline is the task/program representation and coverage layer; sparse valid traces plus fixed gates then make zero invariants a predictable downstream consequence. The result is a serious ARC implementation failure and a non-test of the broader learning theories, not a broad theoretical exoneration.

## Evidence sources

- Phase 13G: [`evidence_package.md`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/evidence_package.md), [`summary.json`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/summary.json), [`discovery_trace_quality.csv`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/discovery_trace_quality.csv), [`discovery_traces.jsonl`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/discovery_traces.jsonl), [`task_outcomes.csv`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/task_outcomes.csv), [`invariants.csv`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/invariants.csv), [`skills.csv`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/skills.csv), [`growth.csv`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/growth.csv), [`pre_holdout_lock.json`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/pre_holdout_lock.json), [`tables`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/tables/table_2_taxonomy_coverage.csv).
- Phase 13G frozen implementation: [`config.json`](../../../experiments/phase13g/config.json), [`preregistration.md`](../../../experiments/phase13g/preregistration.md), [`runner.py`](../../../experiments/phase13g/runner.py), [`common.py`](../../../experiments/phase13g/common.py), [`reporting.py`](../../../experiments/phase13g/reporting.py).
- Data provenance: [`ARC split manifest`](../../../datasets/arc/arc-agi-2/split_manifest.json), [`Phase 13G run manifest`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/run_manifest.json), [`attempt 01 note`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1-ATTEMPT-01-REPORT-WRITE-FAILED/attempt_note.md).
- Phase 13H: [`Package F — ARC`](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_F_ARC.md); Phase 14A integrity caveats: [`evidence_integrity_report.md`](../PHASE-14A-EVIDENCE-INTEGRITY-REVIEW-V1/evidence_integrity_report.md).
