# ASFT v1.1 Phase 1A — Benchmark Audit & Pressure Analysis

**Phase ID:** `ASFT-V1.1-PHASE-1A`  
**Package:** `ASFT-V1.1-PHASE-1A-BENCHMARK-AUDIT-V1`  
**Status:** complete  
**Scope:** Forensic audit of v1.0 benchmarks and their ability to test the stated claims. No theory was retested, no confirmatory data were collected, and no prior result was changed.

## Deliverable index

- [Benchmark Inventory](benchmark_inventory.csv)
- [Benchmark Classification](benchmark_classification.csv)
- [Pressure Audit](pressure_audit.csv)
- [Baseline Audit](baseline_audit.csv)
- [Construct Audit](construct_audit.csv)
- [External Validity Audit](external_validity_audit.csv)
- [Decision-Divergence Audit](decision_divergence_audit.csv)
- [Failure Attribution Audit](failure_attribution_audit.csv)
- [Benchmark Redesign Requirements](benchmark_redesign_requirements.csv)
- [Readiness checklist](phase1A_readiness_checklist.csv)
- [Source/hash manifest](source_manifest.json) and [hash list](source_hashes.csv)

## Executive finding

**Phase 1A PASS.** The v1.0 benchmark record is inventoried and classified; pressure and decision divergence are audited at the mechanism-appropriate level; baseline and construct limitations are explicit; each material weakness maps to at least one Phase 1B–1I design requirement.

The central finding is that v1.0 contained **different kinds of evidence, not one uniform benchmark failure**:

- **13B:** recurrence detection had repeatable positive observations in a known synthetic vocabulary, but the primary ranking benchmark gave the informed rankers identical orders and outcomes. Transfer-aware ranking superiority therefore failed its primary gate in a low-discrimination pool.
- **13C:** skill objects and successful reuse were observed, but the primary SCT policies selected all eligible candidates. The selection-superiority question had effectively zero decision divergence. MEMORY_ONLY was a strong comparator, but application opportunity was not matched.
- **13D:** transfer and reasoning-step-cost outcomes had moderate variation in covered synthetic cells and diagnostic negative-transfer probes. Structural/compositional cells were unavailable and the transfer→growth link was not causal or consistent. “13D has moderate pressure” is accurate only for some task-transfer outcomes, not for every hypothesis in that phase.
- **13E:** internal capability/growth scores moved and some arm outcomes differed, but the capability construct lacked an independent target. A weak positive C_t→next-task-utility association is distinct from the negative/uncertain transfer→CGR evidence.
- **13F:** the baseline/ablation suite had meaningful outcome differences for some comparators, but the SCV/frequency/random selection arms chose the same four candidates and tied. Thus a global claim that “13F decision divergence was zero” would be too broad: it is zero for the named selection-policy contrast, not for every baseline/task outcome.
- **13G:** the ARC adapter had very low coverage and no learned mechanism population. All holdout arms tied at 1/200; B2's one transfer solve is episodic memory. The results diagnose this bounded adapter, not general ASFT. Discovery additionally searched ten programs despite a three-candidate frozen config.

## 1A.1–1A.2 — Inventory and benchmark taxonomy

The inventory covers mechanism-specific experiments in 13B–13G and the Phase 11–12 implementation/readiness records. Phase 11/12 are included for completeness but classified as **engineering gates**, not scientific benchmark evidence. The extra Phase 14 IDT no-op experiment is included as an exploratory stress test, not folded into the confirmatory 13B result.

The benchmark classes are multi-label: discovery, selection, ranking, transfer, capability/metric, ablation, baseline, robustness, and external attempt. A phase name does not determine a single benchmark class; e.g., 13C contains skill creation, transfer/reuse, memory, lifecycle, and composition components.

## 1A.3 — Pressure audit

Pressure is specific to the decision being claimed. The audit uses:

- **None:** competing methods make the same relevant decision, e.g. all candidates are selected or rank orders coincide.
- **Weak:** outcome variation exists, but decisions, constructs, coverage, or independent validation are insufficient.
- **Moderate:** meaningful successes/failures or comparator contrasts exist in a defined covered domain, but scope or identification limits remain.
- **High:** repeated independent, decision-divergent, construct-valid pressure with adequate external task support. **No v1.0 benchmark reaches this level.**
- **N/A/unavailable:** the relevant downstream decision did not exist or could not be estimated.

### Headline pressure results

| Benchmark/question | Pressure verdict | Reason |
|---|---|---|
| 13B ranking superiority | **None** among informed rankers | Same semantic order across seeds; exact primary tie. |
| 13C SCT selection superiority | **None** | 44/44 selected; random-create probability 1.0; identical policy choices. |
| 13C skill reuse | **Moderate** | Successful and failed uses exist, but only narrow skills/tasks and memory applications are unmatched. |
| 13D covered transfer | **Moderate** | Positive/negative outcomes and baseline differences exist; source coverage and structure limit scope. |
| 13D transfer→growth | **Weak** | Descriptive associations, differing phase outcomes, no causal intervention. |
| 13E capability construct | **Weak** | Internal score movement; one capability object; no independent target. |
| 13F selection ablations | **None** for SCV/frequency/random choice | Same four candidates selected; exact outcome ties. Other arm outcomes do diverge. |
| 13G ARC mechanism chain | **Unavailable after upstream bottleneck** | No invariant/skill/capability pool; fit coverage low; scored arms largely at floor. |

The machine-readable row-level evidence is in [`pressure_audit.csv`](pressure_audit.csv).

## 1A.4 — Baseline audit

Baseline quality is scored from **1 (poor/informative only as a floor) to 5 (strong, matched, nondegenerate, claim-targeted)**. This is an audit rubric, not a performance score.

- **Strongest targeted competitors:** frequency-only and no-transfer for ranking; MEMORY_ONLY as a surviving retrieval alternative; always-create as the direct selection-policy comparator.
- **Important limitation:** strong baselines do not become informative if the benchmark forces identical decisions. Frequency/no-transfer are relevant competitors but tie the ASFT ranking because rank order does not diverge; always/random creation are direct controls but the candidate pool makes them identical.
- **Useful floors, not sufficient challenges:** NEVER_CREATE and no-learning.
- **Comparator identity risk:** B2, B3, and B4 differ across phases. B4 is a compression-inspired proxy, not canonical DreamCoder. They must not be pooled by label.
- **Memory audit:** MEMORY_ONLY is the strongest v1.0 counterexample to a skill-abstraction-only explanation in 13C, but its 440 applications vs SCT's 223 applications prevent a matched per-opportunity causal comparison.

Exact scores and rationales are in [`baseline_audit.csv`](baseline_audit.csv).

## 1A.5 — Construct audit

The construct audit identifies what each metric actually records. Main findings:

- **IS:** recurrence/consistency/generalization within a bounded ontology; high risk as a general invariant-quality measure.
- **SCV:** composite associated with future value once, but frequency and `p_reuse` are at least as associated; high risk for incremental selection validity.
- **TS/TU:** synthetic covered transfer and phase-specific utility, not broad generalization.
- **RCR:** simulator reasoning-step proxy, not compute time/FLOPs/search reduction.
- **C_t/CGR:** internal portfolio score and change; one persistent capability in 13E means score movement is not capability-count growth.
- **IG/IGR/IE:** formula-derived internal indices without independent intelligence criterion; very high/critical construct risk.
- **ARC labels:** bounded operator coverage, not semantic task taxonomy; full-inventory demo fit is not task accuracy.

The complete metric/label register is [`construct_audit.csv`](construct_audit.csv).

## 1A.6 — External-validity audit

Positive evidence from 13B–13F is predominantly synthetic, uses a narrow shared generator/operation vocabulary, and has no independent generator replication. Phase 13G is an external-data attempt using public ARC-AGI-2 training tasks, but adapter coverage is very low and the mechanism chain never activates. It cannot be treated as evidence that unrestricted ASFT fails on ARC, and the positive synthetic evidence cannot be treated as ARC generalization.

Additional boundary: the Phase 13G full-DSL coverage scan uses ten programs; the frozen config says three per task and the `discover()` implementation defaults to ten. Scored arms use three. These denominators and stages are distinct. Attempt 02 also reused the same frozen holdout after attempt 01 generated predictions in memory.

See [`external_validity_audit.csv`](external_validity_audit.csv).

## 1A.7 — Decision-divergence audit

This audit separates **decision divergence** from **outcome divergence**:

- 13B: `0` ranking-order divergence among ASFT/frequency/no-transfer in the five-seed primary comparison; random is a secondary distinct control.
- 13C: `0/44` candidate-selection divergence among SCT/always/random; no pressure for selection superiority.
- 13D: transfer outcomes and baseline contrasts diverge, but a common candidate-ranking divergence statistic is not established in the consolidated evidence. Negative-transfer probes show some guard decisions; they do not establish broad guard specificity.
- 13E: task/growth outcomes differ across some arms; the experiment does not supply a common rank/selection decision record for the CGM claim.
- 13F: selection-ablation divergence is `0/4` candidates for ASFT/no-SCV/random-SCV, while other baseline/task outcomes diverge. Global “13F=0” is incorrect.
- 13G: holdout accuracy divergence is zero across five arms; no learned skill decisions exist. B2 has one transfer memory event, separate from ASFT.

This distinction is central: a benchmark may have outcome variation yet still fail to identify the claimed decision rule, or may have identical decisions while the mechanism object itself is constructed.

## 1A.8 — Failure attribution

The failure matrix avoids the two invalid extremes:

1. **“The theory is false”** when a mechanism was not exposed to the necessary decision or data (e.g., 13C selection all-create; 13G no eligible skill pool).
2. **“The benchmark alone failed”** when the primary comparison did run and its frozen gate failed (e.g., 13B ranking superiority).

The supported attributions are scoped:

- **IDT superiority:** failed on the tested primary benchmark; ranking-pressure deficiency explains weak discrimination, not the universal theory.
- **SCT superiority:** not established because choices did not diverge; skill construction/reuse still occurred.
- **Memory:** survives as an alternative; not proven universal due unmatched applications and phase-specific baselines.
- **ARC:** low representation/fit coverage and support-gate interaction are proximate; exclusive root cause is not identified.
- **Transfer→growth:** no causal link; measure/phase inconsistency is a reason not to infer the chain.
- **CGM/IG:** primary problem is construct validation, not arithmetic computation.

## 1A.9 — Benchmark redesign requirements

[`benchmark_redesign_requirements.csv`](benchmark_redesign_requirements.csv) is the direct input for Phase 1B–1G. It requires, among other things:

- candidate-value distributions that force real selection without leaking test labels;
- ranking conflicts orthogonal to frequency and transfer signals, with development-set disagreement checks;
- fair memory/abstraction/hybrid budgets and unseen-combination/context cases;
- independent behavioral targets for capability and future-learning targets for IG;
- ARC coverage, successful traces, invariants, skills, capabilities, transfer denominators, and exact task accuracy as separate quantities;
- a single source of truth for the declared and executed search budget;
- frozen baselines/ablations, costs, splits, endpoints, and analysis before confirmation;
- separate pilot/development and confirmatory evaluation sets.

Pressure is a **precondition for interpreting a superiority test**, not a requirement that ASFT wins. A benchmark passes the design gate when it creates fair, measurable opportunities for methods to disagree and can reveal either success or failure.

## 1A.10 — Phase 1A exit review

All user-specified deliverables are present. The audit covers Phase 13A–13G mechanism and readiness benchmarks, the exploratory Phase 14 IDT stress test, plus Phase 11–12 implementation-only evidence. Every major v1.0 weakness has a corresponding redesign requirement; no new experiment, metric value, or causal interpretation was added.

**Phase 1A decision: PASS.** Ready to proceed to Phase 1B and 1C benchmark design. This is not a pass to collect confirmatory outcomes: first validate candidate labels, pressure, matching, budget parity, and leakage controls on development materials, then freeze the confirmatory protocol.

## Source map

Sources include v1.0 Phase 13B–13G evidence packages and raw result summaries, Phase 14B–14J critical analyses, Phase 0 v1.1 charter, and Phase 11/12 design/implementation records. See [`source_manifest.json`](source_manifest.json) for exact paths and hashes.
