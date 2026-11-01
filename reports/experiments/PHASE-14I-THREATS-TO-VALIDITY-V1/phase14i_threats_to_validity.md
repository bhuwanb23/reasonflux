# Phase 14I — Threats to Validity

**Review ID:** `PHASE-14I-THREATS-TO-VALIDITY-V1`  
**Scope:** Internal, construct, external, statistical, implementation, and interpretation validity across Phases 13B–13G and the analyses in Phases 14A–14H.  
**Method:** read-only audit of saved evidence, frozen protocol/source definitions, and prior critical analyses. No experiments rerun; no Phase 13 outputs changed.  
**Status:** complete.

## Deliverable index

- [Internal Validity Analysis](internal_validity.md)
- [Construct Validity Analysis](construct_validity.md)
- [External Validity Analysis](external_validity.md)
- [Statistical Validity Analysis](statistical_validity.md)
- [Implementation Validity Analysis](implementation_validity.md)
- [Interpretation Validity Analysis](interpretation_validity.md)
- [Master Threat Register](master_threat_register.csv)
- [Safe vs. Unsafe Conclusions](safe_vs_unsafe_conclusions.csv)
- [Threats-to-Validity Scorecard](validity_scorecard.csv)
- [Source/hash manifest](source_manifest.json) and [hash list](source_hashes.csv)

## Executive verdict

The evidence base is **credible for bounded descriptive claims about what the saved synthetic pipelines did**, with explicit denominators and several documented repairs/caveats. It does not warrant broad claims about general invariant discovery, ASFT superiority, capability-growth theory, intelligence growth, or ARC generalization.

The largest risks are **construct validity, external validity, and interpretation**. Many positive results are internal to a known synthetic generator and a small set of represented operations. Metrics named invariant strength, capability growth, and intelligence growth are not all independently validated against the corresponding broad constructs. ARC results come from a very narrow adapter with low coverage; a frozen config/code budget mismatch further limits interpretation. Statistical claims also require care because seed clusters and candidate/task rows are not interchangeable, some analyses have low candidate counts or near-zero variance, and many endpoints/comparisons are available.

The central danger is not evidence that the entire project was run incorrectly. It is that **internally consistent synthetic behavior and formula-derived metric movement could be narrated as general capability or intelligence growth**, while the current evidence does not justify that extension. There are specific implementation and reporting defects—especially the ARC discovery budget mismatch and same-holdout retry—which must remain visible.

## 14I-1 — Risk classification and overall scorecard

| Validity class | Overall risk | Highest-risk claim | Why the rating is claim-specific |
|---|---|---|---|
| **Internal** | 🟡 Moderate for descriptive outcomes; 🔴 High for causal/superiority claims | SCT/IDT superiority and transfer→growth causation | Some primary contrasts are properly compared, but rank/selection decisions often do not diverge; generator alignment, unmatched memory opportunities, and phase-specific interventions limit attribution. |
| **Construct** | 🔴 High; **critical** for “intelligence growth” | IG/IGR/IE represent intelligence; CGR represents capability growth | These are repository-defined scores, and key constructs lack independent validation. The same inputs may participate in both score and outcome. |
| **External** | 🔴 Very high | General ASFT or ARC-relevant learning | Strongest positive results are synthetic and narrow; the ARC adapter has very low fit coverage and no downstream mechanism activation. |
| **Statistical** | 🟡 Moderate–High | Stable, generalizable associations/superiority | Some uncertainty estimates and paired gates are available, but small seed clusters, sparse candidates, metric multiplicity, clustered rows, and degenerate variance constrain precision. |
| **Implementation** | 🔴 High overall; **critical** for ARC adapter claims | Results faithfully instantiate frozen config and broad target capability | Most implementation behavior is inspectable, but the ARC discovery budget differs from config, growth output mislabels prefix size, and the same exposed holdout was rerun. |
| **Interpretation** | 🔴 High; **critical** for intelligence/general-theory claims | Mechanism result proves the full theory or broad intelligence growth | Operational success, metric movement, and theoretical construct validity are repeatedly at risk of being conflated. |

**How to read this table:** a “moderate” internal-validity rating does not imply that the full causal theory has moderate support. A descriptive result can be trustworthy for its frozen setting while the causal or general claim remains high-risk.

## 14I-2 — Internal validity

### Main threats

- **Shared generator–solver–trace vocabulary (high):** synthetic task operations, solver primitives, trace labels, and expected invariant signatures share an ecosystem. This makes operation-signature recovery interpretable and repeatable, but weakens the claim that the system independently discovers general reasoning structures.
- **Benchmark alignment (high):** positive discovery and skill outcomes center on operation families represented in the synthetic generator and implementation. Phase 13C produced reflection and rotation skills, not all intended families. This leaves coverage and task-family alignment as alternatives to general learning.
- **Low SCT selection pressure (critical for selection superiority):** the Phase 13C confirmation cutoff selects all 44/44 candidates; the frozen random-create probability is 1.0; SCT, ALWAYS_CREATE, and RANDOM_CREATE tie at net value 0.345. The observed result is a valid tie in that pool, but the policy contrast contains no meaningful selection divergence from which to identify SCT's incremental benefit.
- **Low IDT ranking pressure (critical for ranking superiority):** corrected Phase 13B transfer-aware, frequency-only, and no-transfer rankers have the same primary top-k outcome and semantic order across five seeds. This is evidence of no observed advantage in that benchmark, but low discrimination among rankers limits what the tie says about other candidate pools.
- **Competing retrieval mechanism (high):** Phase 13C MEMORY_ONLY has higher net value than SCT (1.325 vs. 0.345) and many more applications. Since opportunities are not matched, the result does not isolate per-attempt quality; nevertheless raw retrieval is a credible competing explanation for reuse benefit.
- **Cross-phase causal stitching (high):** the proposed full chain is reconstructed across distinct phases, candidate pools, metrics, and protocols. Adjacent phase-level positives are not a single mediation analysis and cannot be concatenated into a causal chain.
- **Ablation interpretation (moderate–high):** some ablations change a score pathway without changing behavior (e.g., no-capability-layer CGR changes with task utility unchanged); a tie means no observed effect under that intervention/pool, not universal irrelevance.
- **Post-result correction lineage (moderate):** Phase 13B's disclosed accounting correction changes the absolute TU values, though the informed rankers still tie and the strict gate still fails. Corrected Phase 13D analyses repair reporting/lookup defects using saved outcomes; these are corrected views, not independent reruns.
- **Holdout exposure (high for Phase 13G holdout independence):** attempt 01 generated predictions in memory before report serialization failed; the same frozen holdout was used in attempt 02. This is not independent replication or pristine holdout confirmation.

### Internal-validity verdict

For **what a specific saved arm did on its frozen synthetic tasks**, internal validity is generally moderate and often adequate for descriptive reporting. For **causal necessity, selection/ranking superiority, or transfer causing capability growth**, risk is high because the decisive decisions may not differ, alternative pathways remain, and the full chain is not tested in one design.

## 14I-3 — Construct validity

### Metrics and labels

- **Invariant Strength (IS):** operationally combines frequency, consistency, and generality within the observed program/task buckets. It may capture recurrence or compatibility with the bounded ontology, not invariant usefulness. Phase 13B's high IS–TS relationship rests on a small promoted-candidate population (about 4.4 candidates per seed); corrected Phase 13D has a near-zero/non-positive IS–TS relation. IS is not validated as a general quality construct.
- **SCV:** associated with future value in one Phase 13C synthetic sample (`ρ=0.700`), but frequency (`ρ=0.748`) and `p_reuse` (`ρ=0.884`) are numerically as strong or stronger. No incremental predictor/policy advantage is demonstrated; all candidates are selected in the primary confirmation pool.
- **Transfer and cost:** 13C/13D transfer is measured in simulator tasks with a reasoning-step reduction proxy. It is not wall-clock time, FLOPs, solver-search reduction, or general real-world transfer. The 91/91 cross-family attempts use a reflection/rotation skill pool, not independent semantic domains.
- **Capability Growth Rate (CGR):** in 13E, the score increases while one capability object persists; its membership and score change. Positive CGR therefore does not imply growth in the number or breadth of capabilities. Phase 13D mean CGR is negative, and transfer–CGR findings are inconsistent.
- **IG / IGR / IE:** these are repository-defined composites/derivatives using internal CGR, transfer, utility, coverage, and composition quantities. Their positive values demonstrate that the formula produces positive outputs in a cohort; they do not independently measure intelligence. IE is IG divided by cumulative experience and has a negative trend in 13E.
- **ARC categories and accuracy:** bounded DSL operation labels are not semantic ARC task families. Full-inventory demonstration-fit coverage is not exact test-task accuracy. “Unsupported-v1” is not a semantic diagnosis of what an ARC task requires.
- **Skill “emergence”:** 44 stored skill instances are created from validated synthetic candidates. This supports construction and reuse of skill objects, but not unprompted or broad skill emergence, nor SCT selection superiority.

### Construct-validity verdict

High risk overall, and **critical** for interpreting IG/IGR as intelligence growth. The direct operational counts (skill instances, successful reuse attempts, task exactness) are clearer constructs than the broad labels attached to internal scores. The paper should report operational definitions before theoretical names and avoid reifying a score as an ontology.

## 14I-4 — External validity

- **Synthetic-only concentration:** the positive invariant, skill, transfer, and cost results mainly arise in controlled synthetic environments with a narrow known vocabulary. They support bounded synthetic mechanisms, not general learning.
- **Limited skill diversity:** major skill evidence is reflection/rotation. A 91/91 cross-family result is conditional on the tested generated cases and available skill pool; it is not transfer across arbitrary domains.
- **ARC adapter coverage:** full ten-program demo-fit counts are discovery 3/600, transfer 5/200, holdout 2/200. These are not task accuracy. Zero invariants/skills/capabilities follow; downstream ASFT mechanisms did not activate. The failed adapter is not a representative test of unrestricted ASFT.
- **ARC budget mismatch:** frozen config says three candidates per task, while `discover()` defaults to ten; the saved 3/600 discovery yield is from the larger scan. Among those three observed fit programs, only the reflection fit is within the first three fixed candidates. This is a source-audited implementation discrepancy, not a rerun or revised Phase 13 metric.
- **Dataset scope:** Phase 13G used disjoint subsets of the public training split. Official ARC evaluation tasks were not scored. The user-facing result is not an ARC-AGI-2 benchmark score.
- **Holdout caveat:** same frozen holdout was processed again after attempt 01 generated predictions in memory. It is not pristine independent confirmation.
- **Temporary archive disclosure:** an upstream archive containing evaluation blobs was downloaded during reconnaissance; only filenames were listed; no evaluation JSON was extracted, parsed, or scored, and the archive was deleted. Do not claim that no evaluation bytes were ever downloaded.

### External-validity verdict

Very high risk for claims of general ASFT, broad transfer, or ARC generalization. The safe external claim is limited to synthetic tasks and the tested bounded ARC implementation. ARC is a diagnostic failure for that adapter; it cannot establish or falsify the theories in general.

## 14I-5 — Statistical validity

### Main threats

1. **Small independent-seed counts:** Phase 13B uses five seeds; several later phases use ten. A candidate count of 44 or 114 rows does not create 44 or 114 independent replications when rows are clustered within 10 seeds.
2. **Sparse IDT candidate population:** Phase 13B IS–TS results use roughly 4.4 promoted candidates per seed. Correlations from such a small set are unstable and sensitive to single candidates. Phase 13D's 114 observations are clustered in ten seeds and provide a near-zero/non-positive corrected relationship.
3. **Dependence and effective sample size:** Phase 13C has 44 candidate rows in 10 seed clusters; Phase 13D growth associations use rows in 9 or 10 clusters; Phase 13E's 30 within-seed round pairs arise from ten seeds. Cluster-aware intervals help, but do not create large numbers of independent units.
4. **Near-zero variance and exact ties:** 13B informed rankers tie; Phase 13F B3 paired differences can be exactly zero with SD 0. Standardized effects are undefined or unstable when variance vanishes. A zero CI width is not evidence of broad certainty.
5. **Many endpoints/comparisons:** the project reports many phases, baselines, metrics, correlations, robustness probes, and ablations. Primary gates are distinguishable from exploratory or posthoc findings; the latter carry greater false-positive and researcher-degrees-of-freedom risk. Do not elevate selected positive correlations or stress tests above failed frozen gates.
6. **Phase-specific endpoints:** net value, transfer utility, task utility, CGR, C_t, IG, and step-cost proxies are different outcomes. They must not be pooled as if they were one performance metric.
7. **Selected corrections and reanalyses:** Phase 13B's accounting correction changes effect magnitude; Phase 13D's corrected posthoc view and Phase 13E association analysis should be labeled according to their status. A corrected analysis can improve validity but is not an independent replication.
8. **Outcome denominator discipline:** ARC full-DSL demo-fit rates, arm exact-task accuracy, schema-valid traces, invariant-miner inputs, and skill-transfer precision have different denominators. Null/unavailable values are not zeros.

### Statistical-validity verdict

Moderate-to-high, depending on the claim. Saved denominators, paired comparisons, uncertainty intervals, cluster-aware summaries, and preregistered gates make the results useful. Precision/generalization remain limited by independent seed counts, sparse candidate pools, near-zero variance, multiplicity, and phase-specific metrics. Report independent units first and treat candidate/task rows as nested where appropriate.

## 14I-6 — Implementation validity

- **Bounded ARC adapter (critical):** ten fixed operations; very low demo-fit coverage; important concepts not operationalized. The adapter may explain the observed ARC failure but does not represent the full theory.
- **Budget discrepancy (critical for discovery-rate interpretation):** config/preregistration declares three candidates per task, but `discover()` defaults to ten. Coverage scans also intentionally search ten; scored arms search three. Keep these stages and denominators distinct.
- **Growth-field semantic bug (moderate):** Phase 13G labels prefix length (`100`–`600`) as `n_successful_traces`; source code stores `len(traces)`. The actual successful discovery count is three under the ten-candidate scan.
- **Attempt 01 reporting failure (moderate):** Phase 13G report serialization failed after predictions were generated in memory. Attempt 02 reused the same holdout. Preserve as a reproducibility/exposure caveat.
- **Phase 13C CLI seed display (low–moderate):** completion output once displayed calibration seeds during confirmation; saved `record.json` and evidence package identify the actual confirmation seeds as 20–29. The defect is reporting-only in the saved record.
- **Phase 13B accounting version (moderate):** post-result output-cost accounting changed absolute TU values; the ranker tie and failed strict gate remain in both recorded versions.
- **Phase 13D correction lineage (moderate):** corrected posthoc analysis repaired reporting/lookup defects and source coverage using saved outcomes. It is not a rerun; report the corrected analysis and its provenance.
- **Cost-model sensitivity (moderate):** Phase 13C net value depends on frozen creation-cost assumption `MC=0.06`; sensitivity values change the net outcome. Simulator net value should not be treated as a context-free economic value.
- **Trace provenance (high for general reasoning claims):** synthetic traces are generated by known solver logic; successful operation labels therefore do not independently establish free-form reasoning traces.

### Implementation-validity verdict

High overall, with an especially serious, specifically localized ARC budget/config discrepancy. These issues do not imply every synthetic output is invalid; they constrain which estimand each result represents. The phase reports and source manifests disclose the corrections, and this analysis preserves them.

## 14I-7 — Interpretation validity

### Common inferential errors to avoid

- **Metric inflation:** positive `C_t`, CGR, IG, or IGR is not automatically more capabilities or more intelligence. In 13E one capability object persists; capability count does not grow after round 1, and IE declines.
- **Mechanism-to-theory leap:** repeated operation patterns, constructed skill objects, or successful reuse do not validate the complete causal theory. The transfer-to-growth bridge is unestablished; capability-to-intelligence is unvalidated.
- **Tie-to-universal-null leap:** SCT/SCV and transfer-aware rankers tie in low-pressure pools. This means no advantage was demonstrated there, not that those mechanisms can never help.
- **ARC failure-to-theory-failure leap:** Phase 13G does not falsify unrestricted ASFT. Equally, “representation failure” is a proximate explanation for the tested adapter, not proof that the underlying theory would work with a richer representation.
- **Operation label-to-semantic family leap:** fixed DSL categories do not establish ARC semantic taxonomy or correct test outputs.
- **Cost-proxy-to-compute leap:** simulator reasoning-step savings are not wall-clock, FLOPs, or search-computation reductions.
- **Cross-phase concatenation:** phase-specific positives do not collectively prove one continuous end-to-end causal chain.
- **Memory alternative suppression:** Phase 13C MEMORY_ONLY is stronger on its primary net-value endpoint than SCT, but unmatched application opportunities and distinct later B2 systems prevent universal memory-superiority claims.

### Interpretation-validity verdict

High overall and critical for general intelligence or broad theoretical claims. The paper should use claim-specific verbs: “observed,” “constructed,” “associated,” “not established,” and “unavailable.” Reserve “caused,” “emerged,” “generalized,” “capability growth,” and “intelligence growth” for claims with independent evidence supporting those meanings.

## 14I-8 — Safe vs. unsafe conclusions

| Safe, with stated scope | Unsafe or not established |
|---|---|
| Phase 13B repeatedly detected operation-level signatures aligned with the known synthetic generator. | ASFT discovers general/open-ended invariants. |
| Phase 13C constructed and stored reflection/rotation skill objects; successful reuses and simulator step reductions were recorded. | SCT/SCV selection is superior to always-create, random-create, or retrieval. |
| Synthetic transfer occurred in tested generated tasks, including 91/91 attempted cross-family applications within the available skill pool. | Transfer generalizes broadly or causes capability growth. |
| The frozen 13E growth formulas computed positive cohort means; one weak same-cohort C_t→next-utility association passed its preregistered directional criterion. | CGR/IG/IGR are validated measures of capability or intelligence growth. |
| Phase 13G bounded adapter did not demonstrate ARC invariant/skill/capability learning and had very low full-DSL fit coverage. | ARC falsifies ASFT—or proves that representation is the only cause of failure. |
| Memory/retrieval is a strong, surviving alternative in the Phase 13C protocol. | Memory explains all ASFT results or universally beats learned skills. |
| A narrow synthetic subchain from recurring patterns through skill reuse is supported operationally. | The complete ASFT architecture works end to end or the full causal theory is validated. |

## 14I-9 — Final scientific judgment

The evidence is useful and sufficiently documented for **bounded synthetic mechanism claims and implementation diagnostics**. The most consequential validity limits are construct validity for CGR/IG, external validity beyond the synthetic generator, the ARC adapter's restricted coverage and budget discrepancy, and interpretation of metric movement as theory-level growth.

The dominant risk is **overgeneralization**, not a blanket finding that experiments were improperly run. The scientifically credible conclusion is that narrow synthetic pattern detection, skill construction, reuse, and step-cost effects are observed; superiority and the transfer-to-capability/intelligence chain remain unproven; and ARC generalization was not demonstrated by the tested bounded adapter.

**Exit decision: Phase 14I COMPLETE.**

## Evidence sources

- Phase 14A–14H review reports, scorecards, and validity registers are listed in [`source_manifest.json`](source_manifest.json).
- Consolidated Phase 13 records and key Phase 13B–13G outputs are hash-identified in [`source_hashes.csv`](source_hashes.csv). For detailed phase results, see [Phase 14H cross-contribution analysis](../PHASE-14H-CROSS-CONTRIBUTION-ANALYSIS-V1/phase14h_cross_contribution_analysis.md) and [Phase 13H evidence consolidation](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/master_evidence_package.md).
