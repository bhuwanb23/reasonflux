# Phase 13H — Master Evidence Package

**Experiment:** `PHASE-13H-EVIDENCE-CONSOLIDATION-V1`  
**Purpose:** posthoc evidence consolidation for Phase 14; no benchmark reruns, no pooled cross-phase inference, and no edits to earlier-phase result artifacts.  
**Status:** consolidation deliverables complete. **Scientific status:** the evidence does not support the full IDT→SCT→transfer→CGM→IG→ARC claim chain. Several claims are supported only inside controlled synthetic generators; key superiority gates fail or are unavailable; ARC transfer was not demonstrated by the bounded Phase 13G system.

## Executive decision

Phase 13H turns saved Phase 13A–13G results into explicit claim statuses and Phase 14 guidance. It does **not** convert readiness smoke tests, a tie, a controlled stress test, or a proxy metric into confirmatory evidence. The correct overall conclusion is mixed and bounded:

1. **Synthetic mechanisms can produce repeatable traces, invariant candidates, skills, transfer events, and capability metrics.** This is evidence of software behavior inside the tested synthetic generators.
2. **The central incremental claims remain unproven.** Transfer-aware ranking tied frequency/no-transfer on the original Phase 13B benchmark; EXP-IDT-14 was a later, deliberately confounded stress test. SCT's Phase 13C policy was tied to always-create/random-create and below memory-only. Phase 13D's corrected mandatory-baseline gate failed on B4; Phase 13E/13F superiority was mixed, and no-SCV/random-SCV often tied ASFT.
3. **The synthetic evidence does not establish ARC external validity.** Phase 13G's 10-program ARC adapter exactly fit only 3/600 discovery, 5/200 transfer, and 2/200 holdout tasks. It mined zero invariants, formed zero skills/capabilities, and scored 1/200 exact holdout tasks (0.5%) for every main arm. This diagnoses severe DSL coverage limits; it neither validates the full theory on ARC nor proves the theory cannot work with a broader, independently preregistered ARC system.
4. **Capability-growth and IG numbers are simulator metrics, not general intelligence measurements.** Positive 13E synthetic CGR/IG coexist with negative IE trend, negative/uncertain TS→CGR association, no accepted higher-order capability, and mixed baseline/ablation findings.

**Phase 14 readiness:** ready only for critical results analysis, claim narrowing, and limitation analysis using the preserved evidence. **Not ready** to assert that ASFT beats alternatives in general, that invariant strength reliably predicts transfer, that capabilities or intelligence grow generally, or that ASFT mechanisms replicate on ARC.

## 13H-1 — Evidence philosophy

A metric is not a claim. Each claim in this package is linked to its experiment, operational metric, saved evidence, scope, and a defensible wording. `Pass` within a phase means only that phase's frozen criterion was met on that phase's task generator and analysis unit. It does not transfer automatically to a different phase or domain. CIs with different units, denominators, metrics, or task generators are not pooled.

Evidence status labels used here:

- **Supported—synthetic scope:** observed under a controlled ReasonFlux generator, with the generator/solver/task labels known.
- **Mixed / partial:** one or more measures support the claim, while a primary contrast, required component, or another phase contradicts or fails it.
- **Not supported / gate failed:** the frozen criterion failed or the observed contrast was zero/adverse.
- **Unavailable:** required events, components, baselines, variance, or labels were absent; not imputed as zero or turned into a pass.
- **Exploratory only:** designed after prior results, adversarial by construction, or otherwise not confirmatory.
- **ARC external validity not demonstrated:** no mechanism chain was observed on the ARC task split.

## 13H-2 — Claim–evidence mapping

| Claim ID | Claim under review | Main evidence | Status | Defensible wording |
|---|---|---|---|---|
| IDT-1 | Useful invariants emerge from experience | 13B synthetic discovery/IP/IR; 13C–13D reflection/rotation-only births; 13G 0 candidates after only 3 exact-fit ARC discovery traces | **Partial; generator-bound** | The implemented pipeline detects recurring operation signatures in the synthetic task generator. It has not established broad or ARC-level invariant discovery. |
| IDT-2 | IS predicts future transfer | 13B perfect correlation on a small constructed population; 13D corrected IS–TS `r=-0.042` (cluster-bootstrap 95% CI `[-0.132, ~0]`, 114 rows/10 seed clusters); 13G unavailable | **Not established** | The synthetic evidence is inconsistent and too dependent on small, constructed populations to support a general predictive claim. |
| IDT-3 | Transfer-aware discovery beats frequency-only/no-transfer | Original 13B strict gate failed: ASFT top-k=2 tied frequency-only and no-transfer; EXP-IDT-14 top-1 stress test passed on a deliberately injected no-op confound but is explicitly exploratory | **Gate failed; stress test exploratory** | Transfer-aware ranking can reject the specifically inserted frequent no-op in that stress test; superiority on the original or natural task distribution is not shown. |
| SCT-1 | Skills emerge from validated invariants | 13C formed 44 candidate instances/10 seeds, only reflection/rotation; 13D likewise only reflection/rotation; 13G 0 skills | **Partial; synthetic only** | Reflection/rotation skills form in controlled synthetic settings; counting/grouping and ARC skill emergence are not established. |
| SCT-2 | SCV selects skills with greater future value | 13C SCV10 vs shadow net-value Spearman `ρ=0.700`, cluster-bootstrap CI `[0.545,0.931]`, n=44 candidates/10 seed clusters; frequency `ρ=0.748`, p_reuse `ρ=0.884`; all calibration candidates SCV>0 and random-create probability froze at 1.0; 13F no-SCV/random-SCV tied ASFT | **Associational, not validated as a policy advantage** | SCV was associated with shadow value in one synthetic sample, but it did not demonstrate a selective benefit over frequency or no-SCV policy in the confirmatory contrasts. |
| SCT-3 | Skills are reused and reduce reasoning cost | 13C/13D positive success-gated step reductions in synthetic tasks; 13D observed reuse, but memory-only often outperformed; 13G had no promoted skill | **Supported in simulator; not externally validated** | Reuse can reduce the repository's measured step-cost proxy in the tested synthetic tasks; this is not wall-clock/compute savings or ARC transfer. |
| TR-1 | Skills transfer to new tasks/families | 13D positive near/moderate/structural TS across its synthetic cells; full compositional/structural claims unavailable because required component skills absent; 13G transfer outcomes near zero and no skills | **Synthetic transfer observed; structural chain incomplete** | Some synthetic skills transfer across generated tasks. Full multi-skill composition and transfer to ARC remain unproven. |
| CGM-1 | Capability portfolios grow over experience | 13E positive mean CGR `0.2946` and persistent capability in 10/10 seeds; 13D mean CGR `-0.060` over 9 evaluable seeds; 13F baseline deltas mixed; 13G no capabilities | **Mixed, generator-specific** | The frozen CGM pathway registers positive capability growth in one synthetic cohort, but growth is not consistent across phases and is absent on the Phase 13G ARC adapter. |
| CGM-2 | IG/IGR indicate intelligence growth | 13E mean IG `0.2294`, IGR `0.0090`, but IE slope `-0.00394` (95% CI `[-0.00421,-0.00367]`); no higher-order capability cluster; 13G IG unavailable | **Metric-pathway result only; broad claim unsupported** | Repository IG/IGR rose in the Phase 13E synthetic setup; this does not establish general intelligence growth. IE trend and other diagnostics are adverse or unavailable. |
| BASE-1 | ASFT beats all reasonable alternatives | 13B gate fails; 13C SCT below memory-only and tied always/random; corrected 13D fails B4; 13E fails B1; 13F fails B1 and B3; 13G all arms tie at 0.5% | **Not supported** | ASFT's superiority is not established; results depend on task generator and comparator, with several mandatory contrasts null or adverse. |
| ARC-1 | IDT/SCT/transfer/CGM mechanisms replicate on ARC | 13G bounded DSL fit 3/600 discovery, 5/200 transfer, 2/200 holdout; 0 invariants/skills/capabilities; all arms 1/200 holdout exact task | **Not demonstrated** | Phase 13G is a low-coverage bounded-DSL test and does not provide evidence that the mechanism chain replicates on ARC. |

Machine-readable version: [`claim_evidence_matrix.csv`](claim_evidence_matrix.csv). The source artifact for each decision is cited in the package files and source manifest.

## 13H-3 — IDT consolidation

The synthetic trace pipeline does produce recurring operation-level candidates. Phase 13B reported perfect IP/IR and perfect IS–TS correlations, but the correlation population was small (about 4.4 promoted candidates per seed) and shared a controlled generator with the solver. The same original benchmark failed the mandatory baseline gate because transfer-aware ranking tied frequency-only and no-transfer at top-k=2. EXP-IDT-14 later passed top-1 against a deliberately injected, frequent, non-transfer-bearing `normalize_grid` marker, but its preregistration and report correctly classify it as an exploratory stress test that does not replace the original gate.

Corrected Phase 13D reports `IS_vs_TS` `r=-0.042` with the 95% seed-cluster bootstrap interval reaching zero; Phase 13G has no invariant candidates from which to estimate the relation. **Conclusion:** recurrence is demonstrated in the synthetic mechanism; general IS predictive validity and transfer-aware superiority are not established.

See [Package A — IDT](package_A_IDT.md), original [Phase 13B results](../../../docs/03_implementation/validation/phase_13b_results.md), [EXP-IDT-14](../EXP-IDT-14/report.md), and the corrected [Phase 13D posthoc analysis](../PHASE-13D-TRANSFER-V1/posthoc_analysis.md).

## 13H-4 — SCT consolidation

Phase 13C recorded 44 eligible candidate rows across 10 confirmation seeds (six unique signatures), all births reflection/rotation; counting/grouping had zero births. The frozen SCT policy selected all eligible candidates. Its mean net value was `0.345` (SD `0.063`, 95% CI `[0.306,0.384]`), equal to always-create and the calibration-frozen random-create arm; memory-only was `1.325` with zero between-seed variance in that setup. The strict superiority gate failed. SCV10 correlated with shadow realized net value (`ρ=0.700`, 44 candidate rows/10 seed clusters), but p_reuse and frequency were at least as strongly associated and the random-create probability degenerated to 1.0. In Phase 13F, removing SCV/randomizing SCV/turning off lifecycle produced zero paired change under the frozen scenario; this is null contribution evidence, not proof those components never matter.

Synthetic skill reuse can reduce measured step count and composition was demonstrated only for the available rotation→reflection pair. No counting/grouping composition was evaluable. Phase 13G produced no skills. **Conclusion:** synthetic skill construction/reuse is demonstrated; SCT's incremental value and ARC skill emergence are not.

See [Package B — SCT](package_B_SCT.md), [Phase 13C evidence](../PHASE-13C-SCT-V1/evidence_package.md), and [Phase 13F evidence](../PHASE-13F-BASELINE-ABLATION-V1/evidence_package.md).

## 13H-5 — CGM consolidation

Phase 13E reported, across 10 seeds, mean `C_t=1.0227` (SD `0.0667`, 95% CI `[0.9750,1.0705]`), CGR `0.2946` (`0.0125`, `[0.2857,0.3036]`), IG `0.2294` (`0.0069`, `[0.2245,0.2343]`), IGR `0.00904` (`0.00002`, `[0.00903,0.00906]`), CCG `0.2500` (`0`, `[0.2500,0.2500]`), and UG `0.2946` (`0.0125`, `[0.2857,0.3036]`). The summary table also records supported-family coverage and other saved metrics. A capability persisted across consecutive rounds in 10/10 seeds. These positive results coexist with a negative IE slope (`-0.00394`, CI `[-0.00421,-0.00367]`), negative/non-positive TS→CGR association (`r=-0.503`, CI `[-0.860,0.186]`), no accepted higher-order emergent capability, 0/10 post-composition capability-count gains meeting the descriptive criterion, and an adverse composition-value result (`-0.1429`). ASFT failed the Phase 13E B1 comparison on task utility despite the growth-score delta.

Phase 13D's corrected posthoc analysis found mean CGR `-0.060` over nine evaluable seeds. Phase 13F found very large positive CGR deltas in some arms, but the decision requires both task utility and CGR: ASFT failed B1 and B3 and passed B2/B4. Phase 13G has no validated capability group, so CGR/IG remain unavailable. **Conclusion:** the repository growth metrics can increase in this synthetic pathway; their interpretation as robust capability or intelligence growth is not supported across phases or on ARC.

See [Package C — CGM](package_C_CGM.md), [Phase 13E evidence](../PHASE-13E-CAP-GROWTH-V1/evidence_package.md), [Phase 13D corrected analysis](../PHASE-13D-TRANSFER-V1/posthoc_analysis.md), and [Phase 13F evidence](../PHASE-13F-BASELINE-ABLATION-V1/evidence_package.md).

## 13H-6 — Cross-contribution chain

The chain `experience → invariant → skill → transfer → capability → IG` is **not established end-to-end**. Phase 13C/13D synthetic runs connect some trace patterns to reflection/rotation skills and synthetic reuse; Phase 13D cannot validate the full composition cells because counting/grouping component skills are absent; Phase 13E forms synthetic capabilities but shows inconsistent relationships between transfer and growth; Phase 13G produces none of these downstream objects on ARC.

The flagship diagram [`figure_1_evidence_chain.svg`](figures/figure_1_evidence_chain.svg) marks each link with its evidence scope and the first point of failure. It is intentionally not a success chain graphic.

## 13H-7 — Baseline consolidation

No phase establishes that ASFT beats every mandatory baseline across the full evidence program:

- **13B:** ASFT top-k=2 TU `0.095809` equals frequency-only and no-transfer; random is lower (`0.063113`). Strict gate fails. EXP-IDT-14 is a separate adversarial stress test.
- **13C:** SCT mean net value `0.345` ties always-create/random-create and is below memory-only `1.325`.
- **13D corrected:** ASFT transfer-utility difference is positive versus B1 (`+0.0189`, CI `[0.0167,0.0200]`), B2 (`+0.0153`, `[0.0131,0.0164]`) and B3 (`+0.7289`, `[0.7064,0.7613]`), but negative versus B4 compression proxy (`-0.00109`, `[-0.00327,0]`). Mandatory all-baseline criterion fails. B4 is not canonical DreamCoder.
- **13E:** ASFT beats B2/B3/B4 on the preregistered combination of final `C_t` and task utility, but fails B1 because task-utility difference is `-0.0361` (lower CI `-0.0363`).
- **13F:** ASFT task utility is lower than B1 (`-0.0363`) and ties B3 (`0.0000`); it passes the joint utility/CGR rule versus B2 (`+0.0749` utility) and B4 (`+0.0749` utility), without a universal win.
- **13G:** all five arms have holdout exact accuracy `0.005`; paired accuracy deltas are zero. The repeated holdout caveat further limits inference.

See [Package D — Baselines](package_D_Baselines.md), [`baseline_master_table.csv`](baseline_master_table.csv), and [`baseline_metric_summary.csv`](baseline_metric_summary.csv). The latter reports IS/SU/TS/CGR/IG arm-level descriptive summaries only for Phase 13E/13F where saved seed summaries contain those metrics; unavailable measurements remain blank/status-coded. Metrics from different phases are named as reported; they are not treated as a common scale.

## 13H-8 — Ablation consolidation

Ablations do not tell one uniform component-importance story. No-SCT is null in Phase 13C and Phase 13D; Phase 13F's no-SCV/random-SCV/lifecycle conditions also tie. Phase 13D's corrected no-invariants comparison is positive (`+0.0189`) on its synthetic transfer metric, while Phase 13E/13F report some growth reductions from removing IDT/capability components. Composition is not validated as a general mechanism: Phase 13D has zero active composition applications and missing source skills; Phase 13E's composition-value criterion is adverse; Phase 13C has one evaluable synthetic pair; Phase 13F contains a positive composition-specific contrast in its frozen composition stream. These are scope- and metric-dependent results, not a single causal verdict.

See [Package E — Ablations](package_E_Ablations.md) and [`ablation_master_table.csv`](ablation_master_table.csv). Structural removal effects on CGR/IG are not task-performance gains.

## 13H-9 — ARC evidence

Phase 13G uses ARC-AGI-2 public training task IDs, split 600/200/200, with a fixed 10-program symbolic adapter. Full-DSL exact demonstration-fit coverage was 3/600 discovery, 5/200 transfer, and 2/200 holdout. The main three-trial systems all scored 1/200 exact tasks (0.5%) on holdout, with no accuracy difference across ASFT/B1–B4. Only three discovery traces fit; the preregistered five-task recurrence threshold yielded zero invariant candidates, zero skills, zero capabilities, and unavailable IG. Counting/grouping/object detection/pattern completion were not operationalized; semantic cross-family transfer is unidentifiable without labels. The 120-task official evaluation set was not scored.

**Conclusion:** ARC external validity is not demonstrated. The result is chiefly a low-coverage DSL null, not a fair broad evaluation of ASFT's full theory. Attempt 01 generated holdout predictions in memory before a report-write failure; attempt 02 reused the same holdout after a software-only fix. This is disclosed and is not an independent or pristine holdout estimate. The upstream archive transport and pre-run training-grid schema audit deviations are also disclosed in the Phase 13G package.

See [Package F — ARC](package_F_ARC.md) and [Phase 13G evidence](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/evidence_package.md).

## 13H-10 — Statistical evidence

The dedicated [`statistical_summary.csv`](statistical_summary.csv) records reported means, SDs, intervals, independent units, and source files. [`baseline_metric_summary.csv`](baseline_metric_summary.csv) adds phase-specific 13E/13F descriptive mean/SD/95% t intervals for IS, SU, TS, CGR, and IG by ASFT/B1–B4 arm where those metrics were actually recorded; empty cells are explicitly not reported/not defined. These extra summaries are computed only from the saved seed-summary rows, do not change frozen criteria, and are not cross-phase inferential tests. The statistical unit differs by design: phase-level seed aggregates (n=5 or 10), candidate-level observations clustered by seed, or ARC task IDs. Intervals include normal/t-based seed CIs, cluster bootstrap intervals, and task-paired bootstrap intervals. They must not be compared as though they were generated from one pooled sample.

Recurring limitations: small number of independent seed clusters; deterministic synthetic task streams; zero or near-zero paired variance yielding undefined or enormous standardized effects; per-contrast CIs without global multiplicity correction; posthoc reporting corrections for 13D/13E/13F; and the repeated Phase 13G holdout exposure. Phase 13B's perfect correlation is especially fragile at roughly 4.4 candidates per seed. No new meta-analysis or cross-phase p-value was created.

See [Package G — Statistics](package_G_Statistics.md).

## 13H-11 — Negative evidence and failures

Null and adverse findings are first-class evidence, not discarded exceptions: original 13B baseline tie; failed Phase 13B strict gate; EXP-IDT-14's exploratory status; 13C SCT no superiority and memory-only advantage; 13D failed all-baseline/ablation/association criteria, incomplete composition, and negative mean CGR; 13E negative IE slope and TS→CGR association plus adverse composition value; 13F failure versus B1/B3 and multiple null ablations; and 13G near-zero ARC coverage/no mechanism chain. Reporting defects, incomplete attempts, proxy-baseline limits, and unavailable outcomes are indexed in [Package H — Failure Analysis](package_H_Failure_Analysis.md) and [`negative_evidence_register.csv`](negative_evidence_register.csv).

## 13H-12 — Master package contents

| Package | File | Contents |
|---|---|---|
| A | [IDT](package_A_IDT.md) | discovery, IS, precision/recall, rank comparison, robustness, claim ceiling |
| B | [SCT](package_B_SCT.md) | skill births, SCV, utility, reuse, lifecycle, composition |
| C | [CGM](package_C_CGM.md) | Cₜ, CGR, coverage, utility, IG/IGR/IE and limits |
| D | [Baselines](package_D_Baselines.md) | consolidated B1–B4 comparisons, definitions, outcomes |
| E | [Ablations](package_E_Ablations.md) | contribution removals, nulls, unavailability, scope |
| F | [ARC](package_F_ARC.md) | Phase 13G ARC protocol, data limits, coverage and negative result |
| G | [Statistics](package_G_Statistics.md) | metric-specific means/SD/CIs, units, uncertainty limitations |
| H | [Failure analysis](package_H_Failure_Analysis.md) | adverse/null evidence, reporting defects, interrupted attempts, caveats |

Also included: [`claim_evidence_matrix.csv`](claim_evidence_matrix.csv), [`baseline_master_table.csv`](baseline_master_table.csv), [`baseline_metric_summary.csv`](baseline_metric_summary.csv), [`ablation_master_table.csv`](ablation_master_table.csv), [`statistical_summary.csv`](statistical_summary.csv), [`negative_evidence_register.csv`](negative_evidence_register.csv), [`phase_inventory.csv`](phase_inventory.csv), source hashes, the flagship evidence-chain SVG, and [Phase 14 readiness](phase14_readiness.md).

## 13H-13 — Phase 14 readiness review

| Question | Decision | Reason |
|---|---|---|
| Can we defend that recurring traces/invariants occur in synthetic tasks? | **Yes, narrowly** | Controlled synthetic discovery and high precision/recall; same-generator labels and tiny candidate populations limit external interpretation. |
| Can we defend that IS predicts transfer? | **No** | Original perfect correlation is fragile; corrected 13D relation is near zero/non-positive; 13G unavailable. |
| Can we defend transfer-aware ranking superiority? | **No** | Original 13B gate failed; EXP-IDT-14 is exploratory; later baseline outcomes are mixed. |
| Can we defend SCT policy superiority? | **No** | 13C tied no-SCV/random and lost to memory-only; subsequent contrasts are mixed. |
| Can we defend synthetic task-to-task transfer? | **Yes, with scope limits** | Positive synthetic reuse and cost reduction exist; full composition/structural cells were unavailable and baselines/ablation outcomes vary. |
| Can we defend capability/IG growth as general capability/intelligence growth? | **No** | Positive 13E pathway result only; adverse IE/TS-CGR/composition findings, 13D negative CGR, mixed baselines, no ARC group. |
| Can we defend mechanism replication on ARC? | **No** | 13G DSL coverage is extremely low and no invariant/skill/capability chain emerged. |
| Are results ready for a strong confirmatory paper claim? | **No** | Mandatory baseline gate failure, mixed/negative component evidence, small and incompatible synthetic studies, and non-pristine repeated ARC holdout. |
| Is Phase 14 critical results/limitations analysis appropriate? | **Yes** | Saved records, corrected posthoc views, claim map, and negative evidence are consolidated; no reruns are needed for analysis. |

### Phase 14 guardrails

1. Analyze these saved artifacts; do not rerun or overwrite Phases 13C–13G as part of consolidation.
2. Keep the original `synthetic-v1` Phase 13B `baseline_comparison` gate failed. EXP-IDT-14 remains supplemental/exploratory; never promote it retrospectively to a 13B pass.
3. Use Phase 13D's corrected saved-record analysis for pairwise baselines/composition; preserve the original faulty dashboard files for audit.
4. Keep Phase 13F seeds 70–79 as the confirmation block; the interrupted seed-0 attempt remains excluded and preserved.
5. Describe Phase 13G as bounded low-coverage ARC evidence with a disclosed archive-transport deviation and repeated holdout exposure—not as an official ARC score or a clean confirmation.
6. Report metric definitions, seed/task units, uncertainty method, comparator, missingness, and scope for every number. Do not pool incompatible experiments or use effect sizes with near-zero variance as proof of huge practical effects.
7. Recommended paper claim ceiling: **“ASFT's mechanisms have been prototyped and tested in controlled synthetic grid tasks; some synthetic trace reuse/transfer and capability-metric trajectories were observed, but baseline superiority, general invariant predictive validity, robust capability growth, and ARC external validity remain unestablished.”**

## Phase 13H deliverable exit checklist

| Deliverable | Status |
|---|---|
| Multi-seed evidence collected and inventoried | Complete from saved 13B–13F runs and 13G task split; no new run opened. |
| IDT / SCT / CGM evidence packages | Complete (Packages A–C). |
| Consolidated baselines / ablations | Complete (Packages D–E and machine-readable tables). |
| ARC evidence and limitations | Complete (Package F). |
| Statistical summary with means/SD/95% CIs, effect-size and sensitivity cautions | Complete (Package G and CSVs); new 13E/13F descriptive intervals derive only from saved seed summaries. |
| Negative evidence / failure analysis | Complete (Package H and register). |
| Claim-evidence mapping | Complete. |
| Master package / Phase 14 readiness review | Complete. |
| Scientific success of all Phase 13 hypotheses | **Not achieved / not claimed.** Multiple frozen gates failed and key mechanisms remain unavailable or not demonstrated. |

## Reproducibility and immutability

This is a saved-record consolidation. No Phase 13A–13G benchmark was rerun. Earlier reports, frozen configs, source snapshots, interrupted attempts, and posthoc audits remain in their original locations. `source_manifest.json` records SHA-256 hashes of the exact source artifacts used here. The consolidation contains no new inferential statistic derived by pooling seeds/tasks across phases.
