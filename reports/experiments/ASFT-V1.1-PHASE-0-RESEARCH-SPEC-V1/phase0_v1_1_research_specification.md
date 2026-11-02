# ASFT v1.1 — Phase 0 Research Specification

**Phase ID:** `ASFT-V1.1-PHASE-0`  
**Package:** `ASFT-V1.1-PHASE-0-RESEARCH-SPEC-V1`  
**Status:** complete; required foundation before v1.1 design or experiments  
**Method:** retrospective synthesis of saved Phases 11–14 only. No experiments were run; no new metric was evaluated; no prior result was changed.

## Deliverable index

- [Claim Survival Matrix](claim_survival_matrix.csv)
- [Failure Root-Cause Matrix](failure_root_cause_matrix.csv)
- [Alternative Explanation Matrix](alternative_explanation_matrix.csv)
- [v1.1 Research Questions](research_questions.csv)
- [Frozen Success Criteria](success_criteria.csv)
- [Risk Register](risk_register.csv)
- [Master Roadmap](master_roadmap.csv)
- [Phase 0H Readiness Checklist](readiness_checklist.csv)
- [Machine-readable v1.1 Charter](v1_1_research_charter.json)
- [Source/hash manifest](source_manifest.json) and [hash list](source_hashes.csv)

## 0. Executive decision

**Phase 0 PASS — ASFT v1.1 is specified and ready to begin Phase 1 benchmark design.** This is a readiness decision, not evidence that any v1.1 hypothesis is true or that v1.1 experiments are ready to run. Confirmatory data collection may begin only after each benchmark, baseline, split, endpoint, sample-size plan, effect threshold, and analysis has been frozen in its own preregistration.

Phase 0 sets the research questions, dependency order, non-negotiable interpretation rules, validation gates, and success tiers. It does **not** pre-judge the outcome of future experiments. It also does not silently revise v1.0 metrics or thresholds.

### Overall v1.0 synthesis

- **Survives narrowly:** operation-level recurrence detection in the known synthetic generator; construction and reuse of reflection/rotation skill objects; successful synthetic reuse with a simulator reasoning-step cost reduction; implementation of a useful experimental framework.
- **Failed as primary superiority claims:** transfer-aware ranking over frequency/no-transfer in the corrected Phase 13B gate; SCT over always/random creation in the Phase 13C primary pool.
- **Remains a live alternative:** memory/retrieval, frequency heuristics, and compression, with comparator-specific results rather than a universal winner.
- **Not established:** reliable IS or SCV incremental prediction, transfer causing capability growth, capability metrics representing broad capability, IG measuring intelligence, full ASFT end-to-end causal theory.
- **ARC:** the bounded adapter did not activate the invariant→skill→capability chain. Low DSL coverage is the strongest proximate diagnosis, but not an isolated or exclusive cause. The config/code search-budget discrepancy is part of the failure map.

## 0A. Claim survival matrix

The complete row-level classification is in [`claim_survival_matrix.csv`](claim_survival_matrix.csv). Statuses use the following meanings:

- **Supported narrowly:** operational behavior observed in the named scope; no general claim implied.
- **Partial:** some supporting evidence, but mixed outcomes, limited coverage, or unresolved alternatives.
- **Not established:** evidence is insufficient or non-replicating; not proof of impossibility.
- **Failed primary gate:** the frozen superiority criterion was not met; the failure remains recorded.
- **Unavailable / not demonstrated:** no valid denominator or mechanism activation; never substitute zero.

Key classifications:

| v1.0 claim | Phase 0 status | Boundary |
|---|---|---|
| Synthetic operation-pattern recurrence | Supported narrowly | Known synthetic generator and vocabulary; not open-ended discovery. |
| Skill-object construction and reuse | Supported narrowly | Reflection/rotation pool; skill construction does not prove SCT necessity. |
| Synthetic transfer / step-cost proxy | Supported narrowly | Generated tasks and simulator step metric; not wall-clock or broad transfer. |
| IS predicts transfer | Not established | Early sparse association not sustained by corrected 13D; ARC unavailable. |
| Transfer-aware ranking superiority | Failed primary gate | Corrected 13B tie with frequency/no-transfer. |
| SCV predicts future value | Partial association | Frequency and p_reuse comparable or stronger; selection choices often did not diverge. |
| SCT selection superiority | Not supported on primary pool | SCT ties always/random; MEMORY_ONLY stronger in 13C under unmatched opportunities. |
| Capability-score growth | Partial metric-scope evidence | 13E positive; 13D negative mean; persistent single capability object. |
| Transfer → capability growth | Not established | Phase-specific associations/outcomes inconsistent; no causal bridge. |
| IG/IGR as intelligence growth | Not established | Internally defined metrics without independent construct validation; IE trend negative. |
| ARC mechanism chain | Not demonstrated | Low bounded DSL coverage; no invariants/skills/capabilities; IG unavailable. |
| Full ASFT chain | Not validated | First three links have narrow synthetic operational evidence; C4/C5 remain open. |

## 0B. Failure root-cause map

The detailed map is [`failure_root_cause_matrix.csv`](failure_root_cause_matrix.csv). Each row distinguishes **observed proximate bottleneck** from **causal explanation not isolated**.

| Failure / unresolved claim | Best-supported proximate explanation | What remains unresolved | v1.1 response |
|---|---|---|---|
| IDT ranking superiority | Candidate/ranker pool produced identical policy order and no differential primary outcome | Whether transfer information helps when rankings genuinely disagree | Phase 1 pressure audit; Phase 3 ranking competition |
| SCT selection superiority | All 44/44 eligible confirmation candidates selected; random-create probability 1.0 | Whether SCV can choose better candidates when good/bad/neutral options compete | Phase 1 selection benchmark; Phase 4 controlled comparison |
| Memory vs abstraction | Raw memory applies more often and performs strongly in 13C; opportunity counts are unmatched | Whether abstraction helps on novel recombinations/context beyond exact replay | Phase 5 matched-budget memory challenge |
| ARC mechanism failure | Extremely low coverage of fixed DSL; sparse successful traces; support gates cannot activate | Representation vs task difficulty vs learner insufficiency; budget inconsistency | Phase 2 representation/coverage audit, then Phase 10 clean ARC test |
| Transfer → growth | Cross-phase TS/CGR findings vary; no causal manipulation or consistent effect | Whether transfer causes externally meaningful capacity changes | Phase 6 and Phase 7 preregistered bridge tests |
| Intelligence interpretation | IG/IGR are internally constructed composites; no external criterion | Whether any index forecasts independent future learning | Phase 8 external criterion validation |
| External validity | Positive mechanisms concentrated in one synthetic ecosystem and narrow operation set | Whether the behavior survives generator, vocabulary, and trace shifts | Phase 9 independent replication |

No entry in the matrix claims that a proximate explanation has been causally proven when the v1.0 design did not isolate it.

## 0C. Alternative explanation map

The full matrix is [`alternative_explanation_matrix.csv`](alternative_explanation_matrix.csv). These alternatives remain active research competitors, not nuisances to be dismissed:

- **Memory / episodic retrieval:** survives; strongest in 13C MEMORY_ONLY net value, with unequal application opportunities.
- **Frequency / reuse heuristics:** survive; tie informed rankers in 13B and correlate at least as well as SCV in the 13C sample.
- **Compression / program reuse:** survives; results differ across phase-specific endpoints and B4 is a proxy, not canonical DreamCoder.
- **Generator and vocabulary alignment:** survives as an explanation of synthetic operation-pattern results.
- **Metric construction / score coupling:** survives for CGR/IG interpretation; a score can rise by construction without broader capability or intelligence gains.
- **Representation / DSL coverage:** strongly implicated in the tested ARC adapter, but not shown to be the only cause.
- **Cost assumptions and selection degeneracy:** affect net-value comparisons and the value of skill creation; MC sensitivity is preserved.
- **Task difficulty and hidden confounds:** not isolated by v1.0; remain possible explanations, not conclusions.

## 0D. v1.1 research questions

The frozen research questions are in [`research_questions.csv`](research_questions.csv):

1. **RQ1 — IDT:** Does transfer-aware ranking improve held-out utility over frequency-only and no-transfer when the candidate pool creates real ranking disagreement?
2. **RQ2 — SCT/SCV:** Does SCV select candidates with higher future value than frequency-only, always-create, and randomized selection under genuine choice pressure?
3. **RQ3 — Memory vs abstraction:** Does an abstract reusable skill outperform episodic retrieval on unseen combinations or contexts under matched data, storage, and compute budgets? When does a hybrid help?
4. **RQ4 — Capability:** Does an independently measured capability score predict future performance on novel tasks beyond prior performance, exposure count, and simpler baselines?
5. **RQ5 — Intelligence metric:** Do IG/IGR predict an independent future-learning or adaptation target beyond baseline capability and experience? If not, retire or relabel the construct.
6. **RQ6 — ARC:** With a broader, frozen, protocol-conformant representation, can the invariant→skill→transfer→capability chain activate on a clean ARC evaluation, and does it improve held-out exact task performance over baselines?
7. **RQ7 — Replication:** Do the supported mechanisms survive independent generators, operation vocabularies, and trace implementations?

## 0E. Frozen success criteria

The detailed gates appear in [`success_criteria.csv`](success_criteria.csv). They separate benchmark readiness from scientific success.

### Confirmatory decision rules (frozen)

- Every primary hypothesis must identify one primary endpoint, independent unit, comparator set, split, missing-data rule, sample-size/power rationale, and smallest effect of interest **before confirmatory outcomes are accessed**.
- Use paired/task- or seed-cluster-level inference appropriate to the randomized unit; report denominators and uncertainty. Rows nested in a seed are not independent replications.
- **Supported for a confirmatory claim:** the preregistered primary contrast is in the predicted direction, its interval clears the predeclared smallest effect of interest, and the result survives the planned independent replication for any generalization claim.
- **Inconclusive:** uncertainty spans both the null and the predeclared useful-effect region, or the required pressure/coverage prerequisite is absent. Do not call this a pass or a refutation.
- **Contradicted / primary gate failed:** the comparator is favored or the effect is nonpositive under the frozen decision rule. Do not rescue it through post-hoc endpoints, thresholds, or subgroup selection.
- **Unavailable:** a mechanism prerequisite or denominator does not exist. Report unavailable, not zero.
- No confirmatory threshold, split, candidate, metric, baseline, or exclusion may be altered after outcomes are inspected. Any exploratory follow-up is labeled exploratory and requires a new holdout.

### Bronze → Silver → Gold → Platinum

- **Bronze — infrastructure/design readiness:** benchmark suite v2, selection/ranking pressure audit, matched-budget memory challenge, independent capability criterion, and ARC coverage audit are implemented and frozen; v1.0 baselines are evaluated on the same development/locked test partitions; representation coverage improvement is measured separately from task accuracy. Bronze is not a theory pass.
- **Silver — mechanism and construct evidence:** RQ1 and RQ2 each pass their primary head-to-head test and independent replication; RQ4 validates a capability measure against a preregistered external task criterion. RQ5 remains separately judged—do not award Silver merely because the metric is computable.
- **Gold — ARC mechanism activation:** a preregistered ARC evaluation produces valid invariants and skills, measurable held-out skill transfer, a validated capability group, and positive held-out task benefit over the frozen no-learning baseline. If stages activate but task benefit or capability validity does not, report partial activation, not Gold.
- **Platinum — external validation / strong competition evidence:** key results replicate on independent generator(s) and an external benchmark; a public Kaggle code submission documents the actual method and its leaderboard score; the paper claim remains within validated scope. This tier is an evidence target, not a guarantee of a prize or judge score.

Exact sample sizes and numeric smallest-effect thresholds are **phase-specific preregistration gates** to be calculated from the chosen endpoint and frozen before confirmatory data. This rule is itself frozen here; no v1.1 confirmatory result may be judged with a threshold selected after seeing it.

## 0F. Risk register

The full register is [`risk_register.csv`](risk_register.csv). Highest-priority risks:

- R1 Memory still matches or beats abstraction under fair tests.
- R2 SCV adds no value after frequency/reuse signals are controlled.
- R3 Transfer-aware ranking continues to tie simpler rankers.
- R4 Expanded ARC representation remains insufficient or exceeds feasible search budget.
- R5 Capability measures fail independent behavioral validation.
- R6 IG remains an internal score without construct validity.
- R7 Candidate pools again fail to create decision pressure.
- R8 Synthetic gains fail under generator/vocabulary/trace shift.
- R9 Benchmark design leaks held-out labels or overfits development tasks.
- R10 v1.1 is rushed to fit the 2026 Paper Track deadline, compromising protocol or claim quality.

## 0G. Frozen v1.1 master roadmap

The phase-by-phase inputs, outputs, dependencies, and exit gates are in [`master_roadmap.csv`](master_roadmap.csv).

`Phase 0 → Phase 1 → Phase 2 → (Phases 3–6) → Phase 7 → Phase 8`, with Phase 9 testing cross-domain survival, Phase 10 testing ARC only after representation/protocol gates, Phase 11 synthesizing the results, and Phase 12 preparing publication. The roadmap preserves the supplied 0–12 numbering.

### Dependency rules

- Phase 1 must establish pressure and independent validation criteria before mechanism outcomes are collected.
- Phase 2 must report ARC demo-fit coverage and task accuracy separately; its taxonomy cannot be treated as ground truth without annotation/provenance.
- Phases 3–6 may run only with frozen candidate pools, baselines, budgets, and locked evaluation sets.
- Phase 7 precedes any CGR construct claim; Phase 8 precedes any intelligence interpretation.
- Phase 9 is an independent replication, not a tuning set.
- Phase 10 consumes the frozen adapter and locked benchmark; no test feedback may repair the same evaluation.
- Phase 11 preserves all null, negative, unavailable, and exploratory outcomes. Phase 12 is claim-bounded publication, not a new analysis phase.

## 0H. Final readiness review

[`readiness_checklist.csv`](readiness_checklist.csv) records all required Phase 0 checks as passed. The claim set, failures, alternatives, research questions, success gates, risks, roadmap, and source lineage are documented and frozen at the research-specification level.

**Phase 0 exit: PASS to begin Phase 1 design.** It is **not** a pass to start confirmatory experiments before Phase 1/2 preregistration and representation gates are met.

### Competition timing note

As of 1 November 2026, the [ARC Prize 2026 Paper Track](https://www.kaggle.com/competitions/arc-prize-2026-paper-track) deadline is listed as 9 November 2026. This multi-phase v1.1 research program cannot be honestly completed before that deadline. A possible v1.0 writeup/entry is a separate decision; it must not be mislabeled as v1.1 evidence or imply the future roadmap has been executed.

## Evidence provenance

Phase 0 synthesizes the saved Phase 11 completion notes, Phase 12 planning/closure records, Phase 13A–13H artifacts, and Phase 14A–14J reviews. The Phase 12 documents are treated as design records rather than independent experiment results. Source paths and SHA-256 digests are in [`source_manifest.json`](source_manifest.json) and [`source_hashes.csv`](source_hashes.csv).
