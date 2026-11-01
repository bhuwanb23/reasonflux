# Package B — Skill Creation and Transfer (SCT)

**Question:** Do validated invariants form reusable skills; does SCV improve creation decisions; do skill reuse and composition add value?

## Phase 13C primary results

- Ten confirmation seeds (20–29); 44 candidate rows and six unique signatures. All observed births were reflection/rotation. There were zero counting/grouping births.
- SCT selected all eligible candidates; selection did not discriminate among candidates. Mean primary net value was `0.345` (SD `0.063`, 95% CI `[0.306,0.384]`). It tied ALWAYS_CREATE and RANDOM_CREATE and was below MEMORY_ONLY at `1.325` (zero between-seed variance in that experiment). The strict superiority criterion failed.
- SCV10 versus shadow future net value: Spearman `ρ=0.700`, 95% seed-cluster bootstrap CI `[0.545,0.931]`, 44 candidate rows/10 seed clusters. Frequency was `ρ=0.748`; p_reuse was `ρ=0.884`; AG was `ρ=-0.074`. These are candidate associations, not independent seed-level treatment effects. All 44 confirmation candidate rows had primary cutoff 0 and were selected; calibration had 22/22 positive scores, so random-create probability froze at 1.0, limiting policy discrimination. Sensitivity was cutoff-dependent: q25 `0.675` selected 28/44 for net value `0.418`; median/high q75 `0.966667` selected 4/44 for `0.018`; MC values `0.00/0.03/0.06/0.12` yielded net values `0.945/0.645/0.345/-0.255`.
- SU rose from mean `0.678` after the first eligible opportunity to `1.459` after the tenth (secondary accounting; no pre-task birth snapshot was serialized, so the first value must not be relabeled as birth utility). SU was strongly associated with reuse and future net value in this synthetic sample; that is correlational and shares the same task generator and shadow-value construction.
- Reuse ledger: 440 eligible SCT opportunities; 223 applied, 201 correct/positive-credit, 22 failed, 217 no-match; 201 positive-credit reuses across 44 created candidate instances. Mean raw step saving among applied rows was 1.000; mean normalized reduction among correct applications was 0.227. MEMORY_ONLY had 440 applied, 418 correct, and 0.950 correct/eligible, so the cost result does not imply ASFT policy superiority. Simulator step reduction is not wall-clock compute savings.
- Composition was evaluable only for rotation→reflection: over 100 paired tasks, the no-skill composition-capable solver succeeded on 100%, best single component 0%, ordered rotation→reflection 100%; success-gated normalized reasoning reduction was 0.429, and all 10/10 separately seeded composition-reuse tasks succeeded. Counting/grouping composition and broader component coverage were unavailable. The one synthetic pair result cannot establish general composition.
- Lifecycle dormancy/reactivation evidence was mixed; the frozen no-lifecycle ablation matched the primary mean net value (`0.345`), so no lifecycle contribution was demonstrated.

## Cross-phase evidence

- Phase 13D: observed synthetic skill reuse and positive success-gated reasoning-step cost reduction; however, only reflection/rotation skills were born, required component coverage was absent, no composition applications occurred, and the full composition/structural-transfer criterion was unavailable. Memory-only performed better on some primary comparisons.
- Phase 13E/13F: no-SCT/no-SCV/random-SCV/lifecycle conditions include null contrasts; these do not prove universal irrelevance, but do not support incremental SCT benefit in the frozen cases.
- Phase 13G: zero skills were formed; no ARC skill reuse inference is available.

## Judgment

**Synthetic skill storage, reuse, and a single composition case are observed. SCT's incremental policy value and generalized composition are not established.** SCV's 13C correlation is hypothesis-generating; it did not demonstrate advantage over frequency/no-SCV controls. No unsupported grouping/counting or ARC claims should be made.

## Defensible claim

> “Reflection and rotation skills can be extracted and reused in the controlled synthetic tasks, with measured step-cost savings in some cases. The tested skill-creation policy did not outperform its primary alternatives, and broad composition/ARC transfer remains unavailable or unproven.”

Sources: [Phase 13C evidence package](../PHASE-13C-SCT-V1/evidence_package.md), [Phase 13D corrected analysis](../PHASE-13D-TRANSFER-V1/posthoc_analysis.md), [Phase 13E evidence](../PHASE-13E-CAP-GROWTH-V1/evidence_package.md), [Phase 13F evidence](../PHASE-13F-BASELINE-ABLATION-V1/evidence_package.md), and [Phase 13G evidence](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/evidence_package.md).
