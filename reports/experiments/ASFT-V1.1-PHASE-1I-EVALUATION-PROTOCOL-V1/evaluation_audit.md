# Phase 1I.1 — Historical Evaluation Audit

**Scope:** documentary audit of Phase 14A–14J and the historical evaluation weaknesses carried forward from v1.0 Phase 13. No benchmark was rerun, no Phase 13 outcome was recalculated, and no definition or threshold was changed.

## Executive conclusion

Phase 14's strongest contribution is methodological candor: it distinguishes operation of the saved implementation from theory validation; preserves failed/null results and posthoc corrections; separates a bounded ARC implementation failure from a general theory verdict; and identifies the missing transfer→capability and capability→intelligence links. Phase 14 did **not** establish a globally valid evaluation protocol or certify every historical run as a perfect replay. The audit identified weak decision pressure, uncertain constructs, different denominators/endpoints, posthoc interpretation risks, incomplete environment/Git provenance, Phase 13B accounting-version drift, Phase 13G code/config budget mismatch, and same-holdout reuse.

## Phase 14A–14J: key evaluation lessons

| Review | Strongest methodological contribution | Weakness/risk carried forward |
|---|---|---|
| **14A — Evidence integrity** | Failed gates, negative results, posthoc corrections, and ARC holdout exposure are disclosed; saved evidence has useful but uneven provenance. | Phase 13B has weaker run-bound hashes and two accounting versions; later phases lack uniform Git/environment locks; stale preflight snapshots; 13G holdout reuse means no pristine confirmation. Integrity PASS was qualified, not universal replay certification. |
| **14B — IDT** | Narrow repeatable operation-signature detection in a known synthetic vocabulary; a failed primary ranking gate remains failed. | Transfer-aware, frequency-only, and no-transfer ranks/outcomes tie; small candidate pool makes IS–TS association fragile; 13D correction does not reproduce positive predictive validity; ARC IS estimate unavailable. |
| **14C — SCT** | Reflection/rotation skill objects, reuse, and simulator step-cost changes are recorded. | All `44/44` candidates selected; random-create probability `1.0`; SCT/always/random decisions collapse. SCV association is not incremental policy benefit. Memory-only has higher 13C net value with unmatched applications. |
| **14D — Transfer** | Covered synthetic reuse and success-gated reasoning-step cost reduction are measurable; coverage is separated from structural transfer. | Step cost is not compute time/FLOPs; transfer→growth is inconsistent/noncausal; missing source skills make some composition/structure endpoints unavailable; superiority is comparator-specific. |
| **14E — Capability/growth metrics** | Internal scores and trajectories are inspectable; a preregistered `C_t`→next-round utility association is preserved as a small within-cohort result. | One persistent capability object changes score/membership; formulas share internal ingredients; CGR differs across phases; IG/IGR/IE lack independent intelligence criterion; construct labels overreach if treated as validated. |
| **14F — Baselines/ablations** | Memory, frequency, compression, and null/negative ablations remain live; local contribution is distinguished from universal necessity. | Baseline implementations/endpoints differ across phases; 13B/13C/13F have degenerate decisions; 13C opportunities differ; several ablations do not activate or change behavior. |
| **14G — ARC** | Failure is localized by stage; bounded adapter did not demonstrate ARC learning; no result is converted into success. | Low DSL coverage; config declares three candidates while discovery defaults to ten; same holdout reused after predictions generated in memory; representation is a proximate diagnosis, not proven sole root cause. |
| **14H — Cross-contribution** | Identifies the first major causal break at transfer→capability growth and rejects cross-phase causal stitching. | Adjacent positives come from different tasks, endpoints, and protocols; no unified randomized mediation/factorial test; component synergy is not identified. |
| **14I — Validity threats** | Separates internal, construct, external, statistical, implementation, and interpretation validity; warns against score reification. | Clustered rows are not independent replications; small seed counts, multiple endpoints, and phase-specific denominators limit precision/generalization; high construct and external validity risk. |
| **14J — Final claims** | Sets a bounded publication claim ceiling and states what is not demonstrated. | Final synthesis names ASFT v0.1; it does not itself establish a run-specific v1.1 protocol, preregistration, independent replication, or an empirical result. Phase 1I must now operationalize the rules for future v1.1 studies. |

## What conclusions are relatively strong?

1. **Implementation-level observations:** saved synthetic pipelines detect known-generator operation patterns, construct reflection/rotation skill objects, and record reuse/step-proxy outcomes. These are operational facts within their task/generator and metric definitions.
2. **Comparator-specific negative results:** the 13B informed rankers tie on their primary outcome; the 13C creation policies select all candidates and tie; 13F no-SCV/random-SCV choices/results tie in the common pool. These results block superiority claims for those tested settings.
3. **Integrity/validity caveats:** 13B accounting-version change, 13D posthoc saved-record correction, 13G budget mismatch and holdout history are explicitly disclosed and must remain attached to the corresponding claims.
4. **Missing theoretical links:** transfer→capability growth and capability→intelligence growth are not established; broad ARC validation was not demonstrated by the bounded adapter.

These are not all claims about ASFT efficacy. Some are strong conclusions about the *limits of what the data can establish*.

## Which conclusions remain ambiguous?

- **IDT construct:** repeated operation signatures might reflect useful recurrence extraction, generator/solver vocabulary overlap, or both. The saved evidence does not establish open-ended abstraction.
- **IS/SCV predictive validity:** correlations from small, clustered candidate sets do not show incremental prediction over frequency, reuse, or a task-derived baseline; the frozen policy outcomes did not show selection superiority.
- **Memory explanation:** 13C raw MEMORY_ONLY is stronger on its net-value endpoint, but more applications occurred; later B2s are different implementations. This is a serious alternative, not a universal memory verdict.
- **Capability growth:** a score rises in one synthetic cohort while one capability object persists; the score is internally constructed. Metric change is observed; ontological breadth/independent capability is not thereby established.
- **ARC root cause:** low coverage and a budget mismatch explain the tested implementation's non-activation; no experiment isolates representation as the only cause. ARC failure is not theory failure, and it is not success.
- **Correlation/causality:** cross-phase associations are not randomized component effects; posthoc corrections improve saved-record interpretation but are not new confirmation.

## Evaluation pathologies converted to protocol rules

| Historical problem | Future control in Phase 1I |
|---|---|
| Low pressure / no decision divergence | Require pre-outcome activation and informative-comparison audit; identical choices yield `non_informative`, not a mechanism win. |
| Construct ambiguity | One decision-driving primary endpoint; secondary evidence and diagnostics are separate; independent behavioral target for capability/intelligence claims. |
| Metric interpretation drift | Freeze operational definition, units, direction, SOI, and claim mapping; no relabeling after outcomes. |
| Different denominators | Declare independent unit and analysis denominator; report rows and clusters separately; show eligible/attempted/completed/missing counts. |
| Unavailable confused with zero | Five-state outcome model; undefined denominator or absent measure is `unavailable`, never imputed zero by default. |
| Post-hoc explanations | Register competing hypotheses, failure-localization plan, and limits in advance; label all after-access changes as posthoc/new version. |
| Exact ties/zero variance | Report tie and variance status; distinguish identical decisions (`non_informative`) from an informative equivalence result. |
| Exploratory result promoted to confirmation | E1/E2 prohibited from primary claims; E3/E4 require preregistration and separate data lineage. |
| Replication conflated with repeated analysis | Define R1–R4; repeat code on the same exposed holdout is not independent replication. |
| Selective reporting | Mandatory report fields include negative, null, inconclusive, non-informative, and unavailable results. |
| Provenance gaps | Hash protocol, code, config, environment, evaluator, data splits, and analysis; preserve append-only correction lineage and access logs. |

## Historical outcome boundaries (must remain unchanged)

- **13B:** corrected transfer-aware, frequency-only, and no-transfer top-k mean TU all `0.0958085`; identical rankings; strict superiority gate failed. The pre-correction mean `0.143130` remains a separate version. No later stress test repairs this result.
- **13C:** net value SCT `.345`, ALWAYS_CREATE `.345`, RANDOM_CREATE `.345`, MEMORY_ONLY `1.325`; all 44 confirmation candidates were selected; memory applied 440 opportunities vs SCT 223. Selection comparison is non-informative; net value gap does not isolate per-attempt quality.
- **13E:** C_t/CGR/IG computed and positive in one cohort, but the same capability object persisted; the small preregistered C_t-to-next-utility association is not external or causal; IG is not validated intelligence.
- **13G:** three full-DSL discovery fits/600, five/200 transfer, two/200 holdout; config/code search-budget discrepancy; no ASFT invariants/skills/capabilities; 1/200 holdout accuracy across arms; reused holdout after predictions were generated in memory. Official ARC evaluation JSON was not scored; evaluation archive bytes had been downloaded during reconnaissance, filenames listed, archive deleted.

These are source-audit facts, not new analyses. The Phase 1I framework does not repair or reclassify historical results; it specifies how new results must be governed.

## Audit verdict

> **Historical evaluation audit complete.** Phase 14 provides a useful claim ceiling and a map of recurring failure modes, but not a substitute for experiment-specific preregistration, one-primary-endpoint discipline, independent-unit inference, explicit missingness, independent replication, or complete data-access lineage. Phase 1I converts those lessons into pre-outcome rules. No scientific claim is upgraded by this audit.