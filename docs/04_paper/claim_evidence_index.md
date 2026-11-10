# Claim–Evidence Index

**Purpose:** map each claim in the submission-facing manuscript to the exact archived evidence file that supports, qualifies, or fails it, together with its final disposition and claim ceiling.

**Applies to:** [`submission_package/paper_source_v4.md`](../../submission_package/paper_source_v4.md) (the v4 submission-facing manuscript). This index adds no experiments, metrics, or interpretations. It is a navigation layer over the frozen Phase 13/14 records and the Research Cycle 1 closure.

**Canonical sources for dispositions:**

- [`PHASE-13H claim evidence matrix`](../../reports/experiments/PHASE-13H-EVIDENCE-CONSOLIDATION-V1/claim_evidence_matrix.csv) — claim IDs, status, scope, defensible wording.
- [`PHASE-14J final claim classification`](../../reports/experiments/PHASE-14J-FINAL-SCIENTIFIC-CONCLUSIONS-V1/final_claim_classification.csv) — final status and boundary for each claim.
- [`PHASE-14J publication claim ceiling`](../../reports/experiments/PHASE-14J-FINAL-SCIENTIFIC-CONCLUSIONS-V1/publication_claim_ceiling.md) — the strongest defensible program-level claim.

---

## Status legend

| Mark | Disposition | Meaning |
|---|---|---|
| ✅ | **Supported (scoped)** | Observed in the tested synthetic setting; scope is named in the ceiling |
| 🟡 | **Partial / mixed** | Signal exists, but robustness, superiority, or construct validity is not established |
| ❌ | **Failed / not established** | A predeclared gate failed, or the claim exceeds the evidence |
| ⚪ | **Unavailable** | Required component, label, or run was absent — **not** a null effect |
| 🟣 | **Method / framing** | A procedural or interpretive claim, not an empirical result |
| ⛔ | **Terminated at P0** | Stopped on prior-art/novelty grounds before any experiment |
| 🔒 | **Excluded** | Archived but deliberately outside the paper's evidence |

---

## 1. The paper's five retained claims (Table 1)

| Paper claim | Paper location | Disposition | Primary evidence file | Claim ceiling |
|---|---|---|---|---|
| **Pattern discovery** — recurring operation signatures observed | §3.1, §3.5, Table 1 | ✅ **PARTIAL SUPPORT** | [`idt_evidence/summary.md`](../../reports/experiments/idt_evidence/summary.md) | Generator-bounded; no external validation |
| **Skill formation and reuse** — reflection/rotation skills, step savings; policy gates tied or failed | §3.1, §3.5, Table 1 | 🟡 **MIXED** | [`PHASE-13C evidence_package.md`](../../reports/experiments/PHASE-13C-SCT-V1/evidence_package.md) | Local utility ≠ policy superiority ≠ ARC transfer |
| **Capability growth** — mixed metrics; no validated ARC capability group | §3.2, §3.5, Table 1 | 🟡 **UNVALIDATED CONSTRUCT** | [`PHASE-13E evidence_package.md`](../../reports/experiments/PHASE-13E-CAP-GROWTH-V1/evidence_package.md) | Positive metric values do not establish robust growth or intelligence |
| **ARC transfer** — low coverage, no accepted downstream objects | §3.3, §3.5, Table 1 | ❌ **NOT DEMONSTRATED** | [`PHASE-13G evidence_package.md`](../../reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/evidence_package.md) | Coverage-limited non-activation, not broad ARC falsification |
| **BL1 boundary learning** — prior-art stop, no implementation | §3.4, §3.5, Table 1 | ⛔ **TERMINATED AT P0** | [`bl1/boundary_prior_art_review.md`](../05_trace_to_transfer/bl1/boundary_prior_art_review.md) | Novelty/program decision only; no efficacy conclusion |

---

## 2. Claim-ID index

These IDs are the frozen labels used by Phase 13H and Phase 14J. Every empirical statement in the paper resolves to one of them. The index is a **superset** of the paper's printed statements: a few IDs (notably `BASE-4` and parts of `TR-5`/`SCT-5`/`SCT-6`) are retained for completeness because they bound what the paper can claim, even where the paper does not print the comparator by name.

### IDT — Invariant Discovery Theory

| ID | Claim | Paper location | Disposition | Exact evidence file | Boundary |
|---|---|---|---|---|---|
| **IDT-1** | Useful invariants emerge from experience | §3.1, §4.1, §3.5 | ✅ **Supported narrowly** | [`idt_evidence/summary.md`](../../reports/experiments/idt_evidence/summary.md) | Recurring **operation-level** signatures in a known generator; not open-ended concept discovery; ARC 0 candidates |
| **IDT-1 (strong)** | ASFT discovers general/open-ended invariants | §4.1 ("occurrence is not contribution") | ❌ **Not supported** | [`phase_14b.md`](../03_implementation/results_analysis/phase_14b.md) | Generator, solver, traces, and labels share one vocabulary |
| **IDT-2** | Invariant strength predicts future transfer | §3.1, §4.1, §3.5 | ❌ **Not established** | [`PHASE-13D posthoc_analysis.md`](../../reports/experiments/PHASE-13D-TRANSFER-V1/posthoc_analysis.md) | 13B r≈1.0 on ~4.4 candidates/seed; corrected 13D **r = −0.042**, CI touches zero |
| **IDT-3** | Transfer-aware ranking beats frequency-only ranking | §3.1, §4.2, §3.5 | ❌ **Primary gate failed** | [`idt_evidence/table_3_baselines_by_seed.json`](../../reports/experiments/idt_evidence/table_3_baselines_by_seed.json) | 13B top-k2 TU **0.095809** for ASFT, frequency, and no-transfer; paired difference **0.000000** |
| **IDT-3b** | Transfer-aware ranking responds to a designed confound | §3.1 ("exploratory stress test") | 🟣 **Exploratory only** | [`EXP-IDT-14/report.md`](../../reports/experiments/EXP-IDT-14/report.md) | Test created after the original tie; does not repair the primary gate |

### SCT — Skill Creation Trigger Theory

| ID | Claim | Paper location | Disposition | Exact evidence file | Boundary |
|---|---|---|---|---|---|
| **SCT-1** | Skills emerge from validated invariants | §3.1, §4.1, §3.5 | ✅ **Supported narrowly** | [`PHASE-13C evidence_package.md`](../../reports/experiments/PHASE-13C-SCT-V1/evidence_package.md) | 44 candidate rows; births limited to reflection/rotation; no counting/grouping skills |
| **SCT-1 (strong)** | ASFT generates skills broadly | §4.1 | ❌ **Not supported** | [`phase_14c.md`](../03_implementation/results_analysis/phase_14c.md) | Only 2 of 4 skill families emerged; ARC 0 skills |
| **SCT-2** | SCV predicts future skill value | §3.1, §4.2, §3.5 | 🟡 **Partial association** | [`PHASE-13C correlations.json`](../../reports/experiments/PHASE-13C-SCT-V1/correlations.json) | SCV10 ρ **0.700** [0.545, 0.931]; frequency ρ **0.748**; `p_reuse` ρ **0.884** |
| **SCT-3** | SCT outperforms naive skill creation | §3.1, §4.2, §3.5 | ❌ **Not supported** | [`PHASE-13C evidence_package.md`](../../reports/experiments/PHASE-13C-SCT-V1/evidence_package.md) | SCT = always-create = random-create at **0.345**; memory-only **1.325** |
| **SCT-3b** | SCT beats a memory-only policy | §3.1, §4.2 | ❌ **Not supported** | [`PHASE-13C evidence_package.md`](../../reports/experiments/PHASE-13C-SCT-V1/evidence_package.md) | Memory-only 1.325 vs SCT 0.345; opportunity-matching caveat disclosed |
| **SCT-4** | SCV is necessary for the observed outcome | §4.2 (ablation context) | ❌ **Not supported** | [`PHASE-13F evidence_package.md`](../../reports/experiments/PHASE-13F-BASELINE-ABLATION-V1/evidence_package.md) | No-SCV and random-SCV contrasts were exactly zero |
| **SCT-5** | Lifecycle management is necessary | §4.2 | ❌ **Not established** | [`PHASE-13F evidence_package.md`](../../reports/experiments/PHASE-13F-BASELINE-ABLATION-V1/evidence_package.md) | Lifecycle off ≈ lifecycle on |
| **SCT-6** | Composition creates new capabilities | §3.1, §3.2 | 🟡 **Promising but limited / ❌ for capability** | [`PHASE-13E evidence_package.md`](../../reports/experiments/PHASE-13E-CAP-GROWTH-V1/evidence_package.md) | 13E composition value **−0.1429**, 0/10 capability gains; only one evaluable pair in 13C (rotation→reflection, 0% → 100%) |

### TR — Transfer

| ID | Claim | Paper location | Disposition | Exact evidence file | Boundary |
|---|---|---|---|---|---|
| **TR-1** | Skills transfer across tasks and families | §3.1, §4.3 | ✅ **Supported (synthetic)** | [`PHASE-13D phase13d_results.md`](../../reports/experiments/PHASE-13D-TRANSFER-V1/phase13d_results.md) | Near, moderate, and cross-family cells positive; full structural composition unavailable |
| **TR-2** | Transfer reduces reasoning cost | §3.1, §4.2 | ✅ **Strongly supported (proxy)** | [`PHASE-13C evidence_package.md`](../../reports/experiments/PHASE-13C-SCT-V1/evidence_package.md) | Mean normalized reduction ≈ **0.227**; simulator step proxy only; cost correction retained |
| **TR-3** | Transfer drives capability growth | §3.2, §4.3, §4.4 | ❌ **Not established** | [`PHASE-13E evidence_package.md`](../../reports/experiments/PHASE-13E-CAP-GROWTH-V1/evidence_package.md) | TS→CGR **r = −0.503**; 13D mean CGR **−0.060**; first major break in the chain |
| **TR-4** | Transfer beats all non-transfer baselines | §3.1, §4.2 | 🟡 **Partially supported / ❌ for B4** | [`PHASE-13D posthoc_pairwise_baselines.csv`](../../reports/experiments/PHASE-13D-TRANSFER-V1/posthoc_pairwise_baselines.csv) | Beat B1/B2/B3; **lost to B4 compression proxy**; mandatory criterion failed |
| **TR-5** | Structural and multi-skill transfer | §4.3, §4.6 | ⚪ **Unavailable** | [`PHASE-13D table_structural.csv`](../../reports/experiments/PHASE-13D-TRANSFER-V1/table_structural.csv) | CountSkill and GroupingSkill never formed; no component coverage |
| **TR-6** | Negative transfer is detectable | Not printed; supports §2.5 comparison discipline | ✅ **Supported** | [`PHASE-13D posthoc_analysis.md`](../../reports/experiments/PHASE-13D-TRANSFER-V1/posthoc_analysis.md) | Incorrect replays earned zero benefit and no utility |

### CGM — Capability Growth Metrics

| ID | Claim | Paper location | Disposition | Exact evidence file | Boundary |
|---|---|---|---|---|---|
| **CGM-1** | Capabilities emerge and grow over time | §3.2, §3.5 | 🟡 **Partial, metric scope only** | [`PHASE-13E evidence_package.md`](../../reports/experiments/PHASE-13E-CAP-GROWTH-V1/evidence_package.md) | CGR **0.2946** [0.2857, 0.3036], persistence 10/10 seeds; 13D mean CGR **−0.060**; generator-specific |
| **CGM-2** | Capability growth predicts future performance | §3.2 | 🟡 **Weak within-cohort association** | [`PHASE-13E evidence_package.md`](../../reports/experiments/PHASE-13E-CAP-GROWTH-V1/evidence_package.md) | Preregistered C_t→next-utility **r = 0.0498** (CI [0.0163, 0.0922]); small, same-generator, noncausal; not a robust prediction claim |
| **CGM-3** | IG/IGR measure intelligence growth | §3.2, §4.4 | ❌ **Not established** | [`PHASE-13E evidence_package.md`](../../reports/experiments/PHASE-13E-CAP-GROWTH-V1/evidence_package.md) | IG **0.2294**, IGR **0.00904**, but IE slope **−0.00394**; no external criterion; IG unavailable on ARC |
| **CGM-4** | Higher-order capabilities emerge | §3.2 | ❌ **Not observed** | [`PHASE-13E capability_formation.csv`](../../reports/experiments/PHASE-13E-CAP-GROWTH-V1/capability_formation.csv) | Zero accepted higher-order capabilities; 0/10 post-composition gains |
| **CGM-5** | Capability metrics are robust across phases | §3.2, §4.6 | ❌ **Not supported** | [`phase_14e.md`](../03_implementation/results_analysis/phase_14e.md) | 13E positive vs 13D negative CGR; 13F joint baseline outcome mixed |
| **CGM-6** | Composition has positive value | §3.2 | ❌ **Not supported** | [`PHASE-13E evidence_package.md`](../../reports/experiments/PHASE-13E-CAP-GROWTH-V1/evidence_package.md) | Composition value **−0.1429** |

### CHAIN — End-to-end causal chain

| ID | Claim | Paper location | Disposition | Exact evidence file | Boundary |
|---|---|---|---|---|---|
| **CHAIN-1** | Experience → invariants → skills → transfer | §3.1, §4.1–§4.3, §5 | ✅ **Supported (synthetic)** | [`PHASE-13H master_evidence_package.md`](../../reports/experiments/PHASE-13H-EVIDENCE-CONSOLIDATION-V1/master_evidence_package.md) | First three links hold in controlled synthetic tasks only |
| **CHAIN-2** | Transfer causes capability growth | §3.2, §4.4, §5 | ❌ **Not established** | [`phase_14h.md`](../03_implementation/results_analysis/phase_14h.md) | First major evidential break; C4 of the original chain fails |
| **CHAIN-3** | Capability growth causes intelligence growth | §3.2, §4.4, §5 | ❌ **Not established** | [`phase_14e.md`](../03_implementation/results_analysis/phase_14e.md) | C5 unproven; IG/IGR are internal composites |
| **CHAIN-4** | Full ASFT causal chain validated | §5, Table 1 | ❌ **Not validated** | [`PHASE-14J phase14j_final_scientific_conclusions.md`](../../reports/experiments/PHASE-14J-FINAL-SCIENTIFIC-CONCLUSIONS-V1/phase14j_final_scientific_conclusions.md) | Cross-phase positives are not one end-to-end mediation study |

### BASE — Baselines and ablations

| ID | Claim | Paper location | Disposition | Exact evidence file | Boundary |
|---|---|---|---|---|---|
| **BASE-1** | ASFT beats all mandatory baselines | §3.1, §3.2, §4.2 | ❌ **Not supported** | [`PHASE-13H baseline_master_table.csv`](../../reports/experiments/PHASE-13H-EVIDENCE-CONSOLIDATION-V1/baseline_master_table.csv) | 13B gate fail; 13C below memory-only; 13D B4 fail; 13E B1 fail; 13F B1/B3 fail; 13G all arms tie |
| **BASE-2** | ASFT beats no-learning (B1) | §3.2, §4.2 | 🟡 **Mixed** | [`PHASE-13H baseline_master_table.csv`](../../reports/experiments/PHASE-13H-EVIDENCE-CONSOLIDATION-V1/baseline_master_table.csv) | Positive on 13D transfer utility; 13E task utility **−0.0361**; 13F joint utility fails |
| **BASE-3** | Memory/retrieval explains the observed behavior | §4.2, §4.6 | 🟡 **Alternative survives** | [`PHASE-13C evidence_package.md`](../../reports/experiments/PHASE-13C-SCT-V1/evidence_package.md) | MEMORY_ONLY 1.325 vs 0.345; unmatched opportunities disclosed |
| **BASE-4** | Compression explains the observed behavior | §4.2, §4.6 | 🟡 **Alternative survives** | [`PHASE-13D posthoc_corrected_criteria.json`](../../reports/experiments/PHASE-13D-TRANSFER-V1/posthoc_corrected_criteria.json) | ASFT < B4 on the mandatory comparison |
| **BASE-5** | Component ablations degrade performance | §4.2 | 🟡 **Partial / null** | [`PHASE-13H ablation_master_table.csv`](../../reports/experiments/PHASE-13H-EVIDENCE-CONSOLIDATION-V1/ablation_master_table.csv) | IDT ablation partial; SCT, SCV, and lifecycle often exactly neutral |

### ARC — External validity

| ID | Claim | Paper location | Disposition | Exact evidence file | Boundary |
|---|---|---|---|---|---|
| **ARC-1** | ASFT mechanisms replicate on ARC | §3.3, §3.5, §4.3 | ❌ **Not demonstrated** | [`PHASE-13G evidence_package.md`](../../reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/evidence_package.md) | 0 invariants, 0 skills, 0 capabilities; IG unavailable |
| **ARC-2** | The adapter covers the ARC task space | §3.3, §4.6 | ❌ **No** | [`PHASE-13G discovery_trace_quality.csv`](../../reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/discovery_trace_quality.csv) | Exact fit **3/600** discovery, **5/200** transfer, **2/200** holdout |
| **ARC-3** | ASFT differs from baselines on ARC holdout | §3.3 | ❌ **No** | [`PHASE-13G task_outcomes.csv`](../../reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/task_outcomes.csv) | ASFT 1/200 vs baselines 1/200 (0.5%) |
| **ARC-4** | ARC failure falsifies IDT/SCT/CGM | §3.3, §4.3 | ❌ **Not supported** | [`phase_14g.md`](../03_implementation/results_analysis/phase_14g.md) | Chain broke at representation; downstream mechanisms never activated |
| **ARC-5** | The ARC adapter run is caveat-free | §3.3, §4.6 | ❌ **No** | [`PHASE-13G attempt_note.md`](../../reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1-ATTEMPT-01-REPORT-WRITE-FAILED/attempt_note.md) | Candidate-budget config/code mismatch; holdout reused after an earlier prediction-write failure |

---

## 3. Secondary empirical statements and supporting numbers

These narrower statements appear in §3.1–§3.4 and §4.1–§4.4, or directly support a printed sentence, but are not separate claim IDs. Where a number is only in the archive and not printed in the paper, the location says so.

| Paper statement | Paper location | Disposition | Exact evidence file | Note |
|---|---|---|---|---|
| 44 candidate rows across confirmation seeds; births limited to reflection/rotation | §3.1 | ✅ Scoped | [`PHASE-13C skill_births.json`](../../reports/experiments/PHASE-13C-SCT-V1/skill_births.json) | Confirmation seeds only; count/grouping births zero |
| Some reuse and simulator-step savings observed | §3.1, §4.2 | ✅ Scoped | [`PHASE-13C reuse_statistics.csv`](../../reports/experiments/PHASE-13C-SCT-V1/reuse_statistics.csv) | Simulator step proxy, not wall-clock compute |
| 201 positive-credit reuses (223 applied, 22 failed, 217 no-match) | Not printed; supports §3.1 reuse claim | ✅ Scoped | [`PHASE-13H package_B_SCT.md`](../../reports/experiments/PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_B_SCT.md) | Synthetic tasks only; recount ledger in the 13C record |
| Transfer-aware ranking tied on the original primary comparison | §3.1, §4.2 | ❌ Gate failed | [`idt_evidence/closure.json`](../../reports/experiments/idt_evidence/closure.json) | Strict closure gate remains `success: false` |
| SCT tied ALWAYS_CREATE and RANDOM_CREATE; below MEMORY_ONLY | §3.1, §4.2 | ❌ Not supported | [`PHASE-13C evidence_package.md`](../../reports/experiments/PHASE-13C-SCT-V1/evidence_package.md) | All eligible candidates had SCV > 0 |
| SCV associated with shadow future value but no incremental policy benefit | §3.1 | 🟡 Partial | [`PHASE-13C correlations.json`](../../reports/experiments/PHASE-13C-SCT-V1/correlations.json) | Frequency and `p_reuse` perform similarly or better |
| Positive CGR/IG/IGR and persistent low-order capabilities | §3.2 | 🟡 Scoped | [`PHASE-13E evidence_package.md`](../../reports/experiments/PHASE-13E-CAP-GROWTH-V1/evidence_package.md) | One synthetic cohort; not broad growth |
| Negative IE trend | §3.2 | ❌ Adverse | [`PHASE-13E evidence_package.md`](../../reports/experiments/PHASE-13E-CAP-GROWTH-V1/evidence_package.md) | IE slope **−0.00394** |
| Zero accepted higher-order capabilities | §3.2 | ⚪ Not observed | [`PHASE-13E capability_formation.csv`](../../reports/experiments/PHASE-13E-CAP-GROWTH-V1/capability_formation.csv) | Not a null effect; the object never formed |
| Non-positive composition-value result | §3.2 | ❌ Failed/null | [`PHASE-13E evidence_package.md`](../../reports/experiments/PHASE-13E-CAP-GROWTH-V1/evidence_package.md) | Mean **−0.1429** |
| Adverse ASFT-minus-B1 all-task utility | §3.2 | ❌ Failed baseline | [`PHASE-13F evidence_package.md`](../../reports/experiments/PHASE-13F-BASELINE-ABLATION-V1/evidence_package.md) | **−0.0361** on task utility |
| Corrected 13D negative mean CGR | §3.2 | ❌ Adverse | [`PHASE-13D posthoc_analysis.md`](../../reports/experiments/PHASE-13D-TRANSFER-V1/posthoc_analysis.md) | **−0.060** across 9 evaluable seeds |
| 13F joint baseline outcome mixed | §3.2 | 🟡 Mixed | [`PHASE-13F evidence_package.md`](../../reports/experiments/PHASE-13F-BASELINE-ABLATION-V1/evidence_package.md) | Fails B1 and B3; passes B2 and B4 |
| CGR/IG unavailable on the ARC adapter | §3.2, §3.3 | ⚪ Unavailable | [`PHASE-13G growth.csv`](../../reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/growth.csv) | No validated capability group |
| BL1 prior art includes learned option initiation sets | §3.4 | ⛔ P0 termination | [`bl1/boundary_prior_art_review.md`](../05_trace_to_transfer/bl1/boundary_prior_art_review.md) | Bounded review, not systematic; no absence claim |
| S2 toy observation (false activations 2/4→0/4, coverage 2/2) | §3.4 | ⚠ Toy fixture only | [`s2/results_v1.md`](../05_trace_to_transfer/s2/results_v1.md) | Not decision-grade; no general boundary-learning claim |

---

## 4. Methodological and framing claims

These are not empirical results. They are claims about how the audit was conducted and what it can support.

| Claim | Paper location | Disposition | Exact evidence file | Boundary |
|---|---|---|---|---|
| The four-level claim ladder is an organizing lens, not a validated scale | §2.2 | 🟣 Method | [`paper_source_v4.md`](../../submission_package/paper_source_v4.md) §2.2 | Do not treat ladder position as a psychometric score |
| Evidence categories separate synthetic support, comparative failure, mixed, unavailable, and prior-art stop | §2.3 | 🟣 Method | [`PHASE-13H negative_evidence_register.csv`](../../reports/experiments/PHASE-13H-EVIDENCE-CONSOLIDATION-V1/negative_evidence_register.csv) | Categories are descriptive, not pooled |
| Outcomes are not pooled across generators, endpoints, or seed structures | §2.3 | 🟣 Method | [`PHASE-13H master_evidence_package.md`](../../reports/experiments/PHASE-13H-EVIDENCE-CONSOLIDATION-V1/master_evidence_package.md) | No new effect estimate is calculated |
| A primary tie is not equivalence beyond the frozen test | §2.5, §3.1 | 🟣 Method | [`idt_evidence/closure.json`](../../reports/experiments/idt_evidence/closure.json) | Tie is reported as a tie |
| An unavailable endpoint is not zero effect | §2.5, §3.2 | 🟣 Method | [`PHASE-13H negative_evidence_register.csv`](../../reports/experiments/PHASE-13H-EVIDENCE-CONSOLIDATION-V1/negative_evidence_register.csv) | Applies to structural transfer, capability groups, and IG |
| A prior-art stop is not an experimental failure | §2.5, §3.4 | 🟣 Method | [`bl1/boundary_prior_art_review.md`](../05_trace_to_transfer/bl1/boundary_prior_art_review.md) | BL1 has no efficacy result in either direction |
| Failed gates and adverse results were preserved, not relabeled | §4.4, Data and audit trail | 🟣 Method / audit | [`phase_14a.md`](../03_implementation/results_analysis/phase_14a.md) | Phase 14A evidence-integrity audit: PASS with provenance gaps |
| The literature screen is purposive, not systematic | §1, §4.5, §4.6 | 🟣 Method | [`arc_evaluation_methodology_review.md`](../research_notes/arc_evaluation_methodology_review.md) | No priority or field-prevalence claim |
| ARC evaluation context: ConceptARC, Ouellette, ARC Prize reports, method ablations | §1, §4.5, References | 🟣 Positioning | [`arc_research_landscape_review.md`](../research_notes/arc_research_landscape_review.md) | Cited sources, not re-analyzed data |
| T2T/S3 is excluded due to an unreconciled timestamp | §2.1, §2.4 | 🔒 Procedural exclusion | [`s3_provenance_date_reconciliation.md`](../research_notes/s3_provenance_date_reconciliation.md) | Execution record `completed_at` 2026-11-05 vs manuscript 2026-10-28 |
| v1.1 candidate-production work is readiness/plumbing only | §2.1 | 🔒 Context only | [`phase_14j.md`](../03_implementation/results_analysis/phase_14j.md) | No real ARC candidate-production run; not efficacy evidence |

---

## 5. Excluded but archived (not paper claims)

Listed here so the repository's full evidence state is traceable without implying that the paper uses it.

| Archived claim | Final status | Exact evidence file | Why it is outside the paper |
|---|---|---|---|
| **T2T Claim N** — invariant representation adds predictive value beyond the strongest fair replay/compiler | ❌ **N-FAIL**, `Delta_N = 0` (I0 105/105, R4 105/105) | [`claim_n_decision.md`](../../reports/experiments/T2T-S3-EXEC-2026-11-05-001/claim_n_decision.md) | Provenance timestamp unresolved; excluded from v4 by decision |
| **T2T Claim A** — invariant skills help in a known generator | 🟡 Partial synthetic support | [`current_evidence.md`](../05_trace_to_transfer/current_evidence.md) | Subsumed by the ASFT synthetic scope; no ARC-AGI-3 evidence |
| **T2T Claim B** — counterexample evidence improves applicability boundaries | ⚠ Toy-fixture pass only | [`s2/results_v1.md`](../05_trace_to_transfer/s2/results_v1.md) | Not decision-grade; no general boundary-learning claim |
| **T2T Claims C/D/E** | ⚪ Untested | [`t2t_post_d1_program_closure_review.md`](../05_trace_to_transfer/t2t_post_d1_program_closure_review.md) | No experiment was authorized or run |
| **BL1** — counterexample-guided applicability-boundary learning | ⛔ Terminated at P0 | [`boundary_prior_art_review.md`](../05_trace_to_transfer/bl1/boundary_prior_art_review.md) | Substantial prior-art overlap; no implementation |
| **Successor program** (ASFT v3, T2T v2, BL2, Harness/Adapter/Human-Process P0) | ❌ No evidence-validated successor | [`research_cycle_1_closure.md`](../research_notes/research_cycle_1_closure.md) | No phenomenon cleared interest, novelty, clarity, and feasibility together |

---

## 6. Source-file guide

| File | Role |
|---|---|
| [`../../reports/experiments/PHASE-13H-EVIDENCE-CONSOLIDATION-V1/claim_evidence_matrix.csv`](../../reports/experiments/PHASE-13H-EVIDENCE-CONSOLIDATION-V1/claim_evidence_matrix.csv) | Canonical claim IDs, statuses, scope, defensible wording |
| [`../../reports/experiments/PHASE-13H-EVIDENCE-CONSOLIDATION-V1/negative_evidence_register.csv`](../../reports/experiments/PHASE-13H-EVIDENCE-CONSOLIDATION-V1/negative_evidence_register.csv) | All 20 preserved negative/adverse findings (NEG-01–NEG-20) |
| [`../../reports/experiments/PHASE-13H-EVIDENCE-CONSOLIDATION-V1/master_evidence_package.md`](../../reports/experiments/PHASE-13H-EVIDENCE-CONSOLIDATION-V1/master_evidence_package.md) | Cross-phase synthesis and no-pooling rationale |
| [`../../reports/experiments/PHASE-14J-FINAL-SCIENTIFIC-CONCLUSIONS-V1/final_claim_classification.csv`](../../reports/experiments/PHASE-14J-FINAL-SCIENTIFIC-CONCLUSIONS-V1/final_claim_classification.csv) | Final claim status and boundary |
| [`../../reports/experiments/PHASE-14J-FINAL-SCIENTIFIC-CONCLUSIONS-V1/final_scientific_scorecard.csv`](../../reports/experiments/PHASE-14J-FINAL-SCIENTIFIC-CONCLUSIONS-V1/final_scientific_scorecard.csv) | Program-level area verdicts |
| [`../../reports/experiments/PHASE-14J-FINAL-SCIENTIFIC-CONCLUSIONS-V1/publication_claim_ceiling.md`](../../reports/experiments/PHASE-14J-FINAL-SCIENTIFIC-CONCLUSIONS-V1/publication_claim_ceiling.md) | Maximum defensible program claim |
| [`../03_implementation/results_analysis/phase_14b.md`](../03_implementation/results_analysis/phase_14b.md)–[`phase_14j.md`](../03_implementation/results_analysis/phase_14j.md) | Contribution-level critical analyses and final verdict |
| [`../../reports/experiments/PHASE-13C-SCT-V1/evidence_package.md`](../../reports/experiments/PHASE-13C-SCT-V1/evidence_package.md) | Skill formation, SCV, policy ties, memory comparison, composition |
| [`../../reports/experiments/PHASE-13D-TRANSFER-V1/phase13d_results.md`](../../reports/experiments/PHASE-13D-TRANSFER-V1/phase13d_results.md) and [`posthoc_analysis.md`](../../reports/experiments/PHASE-13D-TRANSFER-V1/posthoc_analysis.md) | Transfer, corrected cost accounting, IS–TS, CGR, baselines |
| [`../../reports/experiments/PHASE-13E-CAP-GROWTH-V1/evidence_package.md`](../../reports/experiments/PHASE-13E-CAP-GROWTH-V1/evidence_package.md) | CGR/IG/IGR/IE, persistence, higher-order capability, composition value |
| [`../../reports/experiments/PHASE-13F-BASELINE-ABLATION-V1/evidence_package.md`](../../reports/experiments/PHASE-13F-BASELINE-ABLATION-V1/evidence_package.md) | Memory/compression comparators, SCV/lifecycle ablations |
| [`../../reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/evidence_package.md`](../../reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/evidence_package.md) | ARC coverage, downstream non-activation, holdout caveats |
| [`../../reports/experiments/idt_evidence/summary.md`](../../reports/experiments/idt_evidence/summary.md) | 13B discovery, IS–TS correlation, ranking tie, robustness |
| [`../../reports/experiments/EXP-IDT-14/report.md`](../../reports/experiments/EXP-IDT-14/report.md) | Exploratory confound stress test |
| [`../05_trace_to_transfer/bl1/boundary_prior_art_review.md`](../05_trace_to_transfer/bl1/boundary_prior_art_review.md) | BL1 P0 prior-art decision |
| [`../05_trace_to_transfer/claim_n_archive.md`](../05_trace_to_transfer/claim_n_archive.md) | T2T Claim N closure and N-FAIL record |
| [`../research_notes/research_cycle_1_closure.md`](../research_notes/research_cycle_1_closure.md) | Final program dispositions and observation-mode boundary |
| [`../../validation/HYPOTHESES.md`](../../validation/HYPOTHESES.md) | Pre-registration draft for H1/H2/H3; explicitly not established findings |

---

## 7. Editing rules

1. **Do not upgrade a disposition in this index.** A claim moves only when a new, separately authorized experiment passes a predeclared criterion; an index edit is not evidence.
2. **Do not add a paper claim without a claim ID and a primary evidence file.** If a statement cannot be resolved, it does not belong in the manuscript.
3. **Keep unavailable distinct from failed.** Missing components and absent capability groups are not null effects.
4. **Keep the S3 exclusion intact.** No S3 result, disposition, or 105/105 figure enters the v4 empirical narrative while the provenance timestamp remains unreconciled.
5. **Link, never paraphrase, the frozen numbers.** If a number changes, the underlying record changed; that requires a separate correction note, not a silent README/index edit.

---

**Last reconciled against:** `submission_package/paper_source_v4.md`, Phase 13H evidence consolidation, and Phase 14J final conclusions (Research Cycle 1 closure, 2026-11-05).
