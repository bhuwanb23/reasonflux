# ASFT v1.1 Phase 1I — Evaluation Protocol Report

**Phase ID:** `ASFT-V1.1-PHASE-1I`  
**Package:** `ASFT-V1.1-PHASE-1I-EVALUATION-PROTOCOL-V1`  
**RQ:** Not applicable — evaluation/governance phase.

## 1. Executive decision

- **PASS for specification layer.**
- **PASS for contract layer — 67/67 checks.**
- **BLOCKED for empirical execution/confirmatory launch.**
- **RQ not applicable.** No benchmark or statistical experiment ran in Phase 1I.

The required sentence is frozen: **“The protocol permits ASFT hypotheses to be supported, contradicted, inconclusive, unavailable, or non-informative, and prohibits reinterpretation of those states after outcome access.”**

## 2. Historical evaluation audit (14A–14J)

The detailed read-only audit is in `evaluation_audit.md`. Phase 14's strongest contribution is its evidence boundary: it retains failed gates and nulls, distinguishes implementations from mechanisms, and identifies the first unsupported causal links. Yet it does not certify perfect run replay or resolve every construct/denominator issue.

Specific lessons carried forward:

- **13B:** transfer-aware, frequency-only, and no-transfer top-k outcomes tie at corrected mean `0.0958085`, with identical rankings; strict superiority failed. Pre-correction `0.143130` is a separate measurement version.
- **13C:** all `44/44` eligible candidates selected; random-create probability `1.0`; SCT/always/random choices collapse. MEMORY_ONLY net value is `1.325` vs SCT `.345`, with 440 vs 223 applications, so the net value contrast does not isolate per-attempt quality.
- **13E:** internal C_t/CGR/IG score growth is observed, but one capability object persists and construct validity is unestablished. The small registered same-cohort C_t→next-utility association is not external or causal evidence for intelligence.
- **13G:** coverage, transfer, accuracy, and capability activation are separate. The bounded DSL fit only 3/600 discovery tasks under a ten-program scan while config declared three candidates; no invariant/skill/capability chain formed; same holdout reused after predictions generated in memory; official evaluation JSON was not scored, though a temporary archive with evaluation blobs was downloaded and deleted.
- **Phase 14:** posthoc corrections are disclosed, not independent confirmation; correlation does not show causality; internal metrics do not validate theory; different endpoints/denominators cannot be pooled; ARC failure is a failure of the tested implementation but not a general theory refutation—and never a success.

## 3. Classification framework

E1 exploratory and E2 development work can generate hypotheses or tune benchmarks but cannot support primary claims. E3 confirmatory and E4 independent replication can support primary claims only after all gates pass. Outcome-informed work cannot be promoted after the fact. Replication type is R1 within-generator, R2 cross-generator, R3 cross-domain, or R4 external benchmark; generalization requires relevant R2/R3/R4.

## 4. Preregistration framework

The template freezes the question, directional hypothesis, estimand, SOI, exactly one primary endpoint, secondaries/diagnostics, mandatory comparators and ablations, independent unit and sample-size rationale, randomization, splits, missingness policy, denominator, analysis/multiplicity, replication plan, source hashes, sealed outcome access, reporting, and interpretation rules. Threshold, endpoint, split, baseline, budget, or decision-rule changes after outcome access cannot rescue the original claim; they require a new version and independent data.

## 5. Endpoint framework

One primary endpoint is decision-driving. Secondary outcomes support; diagnostic metrics explain mechanism activation and failure. Neither can rescue/replace a primary result. Coverage, task accuracy, transfer, capability, and intelligence remain separate. Internal scores cannot act as external target labels absent independently validated and preregistered authorization.

## 6. Statistical framework

Every study defines the independent sampling/assignment unit and nesting. Seed/task/candidate rows are not automatically independent replicates. Reports include effect, interval, independent-unit N, nested row count, denominators, missingness, exact ties, and zero variance. Missing outcome is unavailable, never zero by default. Valid zero successes with a nonzero denominator remain a zero result. Clustered/pairing methods and SOI are frozen before outcomes.

## 7. Replication framework

R1 verifies within-generator reproducibility; R2 tests a new generator; R3 tests a new domain; R4 tests an external benchmark. One positive study is not a generalized finding. Reused/exposed holdouts and repeated analyses are not independent replication. Conflicting replication is inconclusive/heterogeneous, not a cherry-picked pass.

## 8. Interpretation and outcome states

The framework includes the frozen interpretations: metric increase ≠ theory validation; tie = no demonstrated advantage; unavailable ≠ zero; ablation effect ≠ universal necessity; synthetic success ≠ external validity; correlation ≠ causation; capability score ≠ capability growth until Phase 7 validation; IG ≠ intelligence until Phase 8 validation. The five-state model distinguishes supported, contradicted, inconclusive, unavailable, and non-informative. Identical decisions/no activation yield non-informative for mechanism attribution; missing denominator or failed integrity yields unavailable. These are not interchangeable.

## 9. Reporting and governance

All E3/E4 reports include research question, hypothesis, primary/secondary/diagnostic results, negative/null results, unavailable and non-informative states, limitations, interpretation, denominator/unit counts, deviations, replication, and source lineage. Rules G1–G13 freeze protocols, forbid gate relabeling and selective reporting, bar E1/E2 promotion, prohibit zero imputation for unavailable data, require versioned amendments, preserve hashes/access logs, and require append-only corrections.

## 10. Contract layer

67 constructed contracts cover class restrictions, prereg completeness, one-primary separation, statistical unit/missingness checks, all five outcome states, exact ties/zero variance, R1–R4 and generalization, governance failures, and report completeness. Fixtures are code-path checks, not empirical outcomes or tests of an ASFT hypothesis.

## 11. Phase 1 exit and launch decision

**Phase 1 design/specification exit: PASS.** The benchmark, baseline, ablation, validation-target, replication, interpretation, and governance specifications are present across Phases 1A–1I.

**Confirmatory launch: BLOCKED.** Phase-specific task/solver implementation, exact N and power/precision, hashes, sealed outcomes/access logs, run-specific registry completion, and separate authorization remain pending. A specification PASS is not an empirical readiness sign-off.

## 12. Final statement

> Phase 1I makes the evidence rules explicit and contract-checkable. It reduces the opportunity for post-outcome interpretation drift but cannot make future experiments trustworthy by itself: execution integrity, independent units, valid constructs, fair comparators, actual activation, sealed outcomes, and replication still have to be demonstrated in each experiment.