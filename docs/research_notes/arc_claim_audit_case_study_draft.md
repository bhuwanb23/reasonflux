> **Superseded draft:** This earlier negative-results-oriented version is retained for reference. Use `arc_claim_evaluation_case_study_draft_v2.md` as the current, more cautious claim-evaluation case-study framing.

# From Plausible Mechanism to Bounded Evidence
## A Claim-Level Audit of an ARC-Motivated Research Program

**Manuscript status:** internal, venue-neutral draft based only on archived evidence; not submission-ready. No new benchmark run, experiment, or cross-phase statistical analysis is reported here.  
**Proposed article type:** transparent retrospective case study / negative-results report.  
**Evidence cutoff:** 2026-11-05.

### Abstract

Research on the Abstraction and Reasoning Corpus (ARC) often advances from a plausible mechanism to a system-level performance claim. We present a retrospective, claim-level audit of an ARC-motivated research cycle investigating recurring structures, skill formation, transfer, capability metrics, and whether an invariant representation improves prediction beyond replay. The audit distinguishes evidence of software behavior from comparative efficacy, finite-estimand results from general claims, and empirical outcomes from blocked or prior-art decisions. Across the ASFT research line, recurring operation-level patterns and reflection/rotation skill objects were observed in controlled synthetic tasks, but transfer-aware ranking and skill-creation superiority were not established, capability-growth interpretations were inconsistent across phases, and a bounded ARC-AGI-2 adapter did not activate the proposed downstream mechanism chain. A separate frozen synthetic comparison of an invariant representation with a strong replay/compiler comparator yielded identical exact prediction on all 105 held-out cases (105/105 each), meeting the frozen N-FAIL rule for that finite estimand. A proposed boundary-learning follow-up was terminated after prior-art review and was not experimentally tested. The cycle therefore supports no end-to-end ASFT claim, ARC generalization claim, or new boundary-learning efficacy claim. Its defensible contribution is narrower: an auditable account of how claim decomposition, comparator review, frozen execution, and evidence ceilings constrain interpretation of a complex research program. This case study does not establish those practices as a new methodology or as universally effective; it documents their application and the limits they exposed in one program.

**Keywords:** ARC-AGI; negative results; claim-evidence mapping; comparator design; synthetic benchmarks; research audit; generalization

## 1. Introduction

The Abstraction and Reasoning Corpus (ARC) was designed to probe flexible rule induction from sparse examples rather than recall of a fixed task-specific solution [1]. ARC-AGI-2 and ARC-AGI-3 extend this research agenda to harder abstract-reasoning tasks and interactive environments, respectively [2, 3]. Research systems now span symbolic program search, neural models, test-time adaptation, synthetic-task training, and hybrids. This methodological diversity makes headline performance difficult to interpret without explicit information about the claim, comparator, task population, data exposure, resources, and evidence scope. A system can execute a proposed mechanism without showing that the mechanism is necessary, superior to simpler alternatives, predictive beyond the training setup, or transferable outside the task generator.

This paper reports a retrospective audit of Research Cycle 1, which began with an ASFT research line linking experience, recurring structures, skill formation, transfer, and capability-growth metrics. A later T2T Claim N test asked a narrower question: whether an invariant representation added finite synthetic predictive value beyond a source-derived replay/compiler baseline. A proposed boundary-learning line (BL1) was then considered, but terminated at a planning/prior-art gate before implementation or experiment.

The cycle did not produce a validated end-to-end theory or an ARC-winning algorithm. It did produce a heterogeneous evidence record: bounded synthetic support for some operational behaviors; failed or tied comparative gates; mixed metric results; one decision-grade negative result for a frozen finite synthetic estimand; a low-coverage ARC adapter result; and a separate prior-art termination without an efficacy test. Treating these outcomes as interchangeable would overstate what was learned. In particular, BL1's termination is not a negative experimental result, and the T2T N-FAIL is not evidence that all invariant representations fail.

The paper asks:

> **What conclusions survive when the research program is audited claim by claim against its saved evidence, comparators, estimands, and scope limits?**

The paper makes three deliberately limited contributions:

1. It provides a traceable synthesis of the program's strongest surviving findings and its principal failed, unavailable, or blocked claims.
2. It records a frozen, one-execution comparison in which a strong replay/compiler baseline matched the invariant arm on a finite synthetic predictive estimand.
3. It illustrates why “mechanism present,” “mechanism useful,” “mechanism superior,” and “mechanism generalizes” are different claims requiring different evidence.

We do **not** claim a new ARC-solving method, a new benchmark, a new general theory of research methodology, or a systematic review of all ARC work. The contribution is a case study of one research cycle and its evidence boundaries.

## 2. Scope and evidence-audit method

### 2.1 Research lines included

The audit covers four linked records, without treating them as four equivalent experiments:

- **ASFT:** the saved Phase 13–14 synthesis of the synthetic prototype, comparator studies, capability metrics, and bounded ARC-AGI-2 adapter.
- **T2T Claim N:** one authorized, frozen S3 execution comparing invariant representation I0 against replay/compiler R4 on a finite synthetic predictive suite.
- **BL1:** a bounded P0 prior-art review of counterexample-guided applicability-boundary learning. No implementation or experiment occurred.
- **Research Cycle 1 closure:** a synthesis of the program dispositions and the decision not to authorize a descendant research program.

Later ASFT v1.1 candidate-production readiness work is reported only as readiness/plumbing context; it is not counted as an ARC experiment. The candidate-production run remained blocked by incomplete independent annotation, and no real ARC candidate-production run occurred.

### 2.2 Evidence categories

Each conclusion is classified by what kind of evidence supports it:

- **Narrow synthetic support:** an operational behavior occurred in a controlled, known generator. This does not imply external validity or superiority.
- **Comparative support or failure:** a frozen contrast met or failed its stated criterion on the specified benchmark and estimand.
- **Mixed / partial:** some measures support a bounded claim while a primary comparison, another phase, or a related construct does not.
- **Unavailable / blocked:** required candidates, labels, components, or runs were absent. This is not a zero effect and not a negative experiment.
- **Prior-art termination:** the proposed contribution was judged substantially covered before testing. This is a novelty/program decision, not an efficacy result.

The audit uses the saved Phase 13H and Phase 14J syntheses, the permanent S3 execution record, the T2T claim archive and claim-evidence map, and the BL1 P0 prior-art review. No earlier result artifact was changed; no experiment was rerun; no cross-phase estimates were pooled. The prior-art review was bounded, not systematic. The present manuscript is a secondary synthesis of those records, not an independent replication.

### 2.3 Comparison and claim discipline

Results from different task generators, endpoints, candidate pools, and seed structures are not treated as a common quantitative scale. In particular:

- A primary comparison tie is not “evidence of equivalence” outside its frozen test.
- A decision-grade negative is limited to its specified estimand and decision rule.
- A synthetic pass is not ARC evidence.
- An implementation/readiness pass is not scientific efficacy evidence.
- An unavailable endpoint is not a null effect.
- A prior-art stop is not an experimental failure.

## 3. Findings from the ASFT research line

### 3.1 What was observed in controlled synthetic tasks

The saved Phase 13–14 evidence supports a narrow operational statement: within the tested synthetic task generators, the implemented pipeline can detect recurring operation-level patterns, construct reflection/rotation skill objects, record some successful reuse, and measure reductions in a simulator reasoning-step proxy. Phase 13C recorded 44 eligible candidate rows across its seed runs, with births limited to reflection/rotation operations. These results show that the software pipeline can perform specified operations in controlled environments. They do not establish open-ended invariant discovery, a general skill-formation theory, or a full causal chain from invariant detection to broad capability growth.

The distinction between output production and incremental contribution was consequential. Transfer-aware ranking tied frequency-only and no-transfer variants on the original Phase 13B primary top-k comparison. A later injected-no-op stress test was explicitly exploratory and does not repair that failed primary gate. In Phase 13C, SCT, always-create, and random-create tied on the principal net-value endpoint; memory-only was stronger on that protocol's endpoint, subject to the report's opportunity-matching caveat. SCV was associated with shadow future value in one synthetic sample, but frequency and `p_reuse` were at least as strongly associated, and the confirmatory contrasts did not demonstrate an incremental SCV policy benefit.

**Interpretation:** synthetic pattern detection and skill-object creation occurred, but neither occurrence alone establishes that the proposed ranking or creation policy adds value over simpler baselines.

### 3.2 Capability metrics did not validate a general growth theory

Phase 13E reported positive repository-defined capability metrics in one synthetic cohort, including positive mean CGR and a small `C_t` to next-task-utility association. Those outcomes coexist with a negative IE trend, no accepted higher-order capability, an adverse composition-value result, and an inconsistent transfer-to-CGR relationship across phases. Corrected Phase 13D reported negative mean CGR over its evaluable seeds. Phase 13F's comparisons were mixed and dependent on the joint task-utility/CGR rule. In the bounded ARC adapter, no validated capability group existed, so CGR/IG were unavailable.

The defensible conclusion is that the internal metrics moved as designed in one synthetic pathway. The evidence does not validate them as robust capability growth or intelligence growth, and it does not establish the causal bridge from transfer to capability or from capability to intelligence.

### 3.3 ARC external validity was not demonstrated

The Phase 13G adapter used a bounded symbolic program language. Exact demonstration-fit coverage was 3/600 discovery, 5/200 transfer, and 2/200 holdout. The system produced no accepted invariant candidates, skills, or capabilities; IG was unavailable. The main arms had equal holdout exact-task accuracy of 1/200 (0.5%). The package also records a candidate-budget configuration/code mismatch, a low-coverage representation, and reuse of the same holdout after an earlier attempt generated predictions before a report-writing failure.

These limitations mean the result did not instantiate the intended downstream mechanism chain on ARC. It is evidence that this bounded adapter had very low coverage and did not demonstrate the proposed mechanisms on ARC; it is not a clean causal test showing that an invariant representation cannot work on ARC, nor is it evidence of ARC-AGI-3 performance [3].

### 3.4 ASFT claim summary

| Claim family | Audited status | Defensible reading |
|---|---|---|
| Recurring patterns / invariants | Partial synthetic support | Recurring generator-aligned operation signatures were detected in controlled tasks; broad discovery is not established. |
| Transfer-aware ranking | Primary gate failed | The original primary comparison tied frequency-only/no-transfer; an exploratory stress test does not overturn the result. |
| Skill formation / SCT / SCV | Partial operational evidence; superiority not established | Skill objects were formed; creation policies tied on the main 13C criterion, while the SCV correlation did not demonstrate incremental policy value. |
| Synthetic reuse / cost proxy | Narrow operational support | Some reuse and step-cost reductions were measured in the tested synthetic tasks; this is not general compute or wall-clock efficiency. |
| Capability / intelligence growth | Mixed or unvalidated | Positive internal metric movement in one cohort does not validate general capability or intelligence growth. |
| ARC transfer | Not demonstrated | Low candidate coverage and no downstream objects left the mechanism chain untested on the adapter. |
| End-to-end ASFT theory | Not validated | Adjacent links were studied in different bounded experiments; no full mediation chain was established. |

## 4. T2T Claim N: a decision-grade negative result with a strict ceiling

### 4.1 Frozen question and execution

Claim N asked whether an invariant representation added predictive value beyond a strong replay/compiler baseline on a frozen finite synthetic suite. The authorized S3 execution used seven source traces, 105 held-out primary cases in 35 cells, and 10 diagnostic-only checks. Predictions were committed before held-out outcomes were accessed. The execution record reports one completed run, no protocol deviations, no reruns, and an independent fairness PASS for R4. The frozen resource vector allowed one prediction per arm and context, with no adaptive refit or post-holdout updates.

### 4.2 Result

I0 and R4 each scored **105/105** exact one-step predictions. The difference was `Delta_N = 0.0`, and the frozen decision rule classified the result as **N-FAIL**.

### 4.3 Interpretation boundary

This is the strongest decision-grade negative result in the cycle, but its scope is finite and explicit. It means the invariant representation did not add predictive accuracy over the matched replay/compiler baseline on this frozen suite under the frozen decision rule. It does not establish that:

- all invariant representations are useless;
- the same result holds on another task generator, distribution, or ARC benchmark;
- replay is universally superior;
- the untested behavioral increment is absent; or
- broader intelligence or transfer claims are false.

The equality of scores is an interpretable outcome for the tested estimand, not a population-level proof of equivalence. Claim N v1 was closed rather than rescued by post-hoc subsets or a revised comparator.

## 5. BL1: a prior-art stop, not a negative experiment

BL1's proposed chain was counterexample evidence → better applicability-boundary precision → maintained useful coverage. The P0 review found substantial and direct prior art in counterexample-guided refinement [4, 5] and, more specifically, learning skill/option initiation sets from success/failure examples with explicit attention to classifier quality and useful coverage [6]. The program was terminated at P0 before implementation, data generation, or experiment.

This is a novelty/program decision. It does not show that counterexample updates do not improve boundaries, and the earlier S2 toy-fixture observation (false activations 2/4→0/4, coverage 2/2) remains only a toy observation. Treating BL1 as another empirical negative would misstate the record.

## 6. What the case study shows—and does not show

### 6.1 Narrow lessons supported by this record

1. **A mechanism can run without adding measurable value.** The pipeline produced patterns and skills, while ranking and creation superiority gates failed or tied.
2. **A strong comparator can erase the apparent increment.** Replay/compiler R4 matched I0 on the finite S3 predictive suite, so the representation-specific increment was not observed there.
3. **Constructs need independent interpretation.** Positive repository-defined capability metrics did not by themselves establish broader capability or intelligence growth.
4. **Readiness and implementation evidence are not efficacy evidence.** The ASFT v1.1 parser, runner, synthetic controls, and test suite do not constitute an ARC candidate-production result; the latter remained blocked.
5. **Null, unavailable, blocked, and prior-art outcomes are different.** S3 was a valid negative for a finite estimand; ARC downstream outcomes were unavailable because the candidate chain did not activate; BL1 stopped for prior-art overlap without an experiment.
6. **An end-to-end theory cannot be assembled by adding adjacent phase wins.** The phases used different generators, metrics, baselines, and units; some critical causal links remained unestablished.

### 6.2 What this paper does not establish

This single-cycle account does not establish that claim maps, evidence ceilings, frozen protocols, or comparator audits are new research methods or that using them generally prevents false claims. Automated agent-system design already has a broader literature [7], and a novelty claim about process or system design would require its own focused review. This paper does not estimate how often ARC research overclaims, compare laboratories, quantify the benefit of preregistration, or provide a systematic survey of ARC prior art. It also does not convert the program's documentation volume into a scientific contribution by itself.

## 7. Limitations

The evidence base is heterogeneous and largely generated within a bespoke synthetic research framework. Synthetic task generators and solver vocabularies were known to the researchers, limiting external validity. Several ASFT claims were assessed using small numbers of seeds, constructed candidate pools, or endpoints with phase-specific definitions. Positive findings, ties, and negative findings cannot be pooled into one effect estimate. The ARC adapter was severely coverage-limited and carried disclosed configuration and holdout caveats. T2T's decision-grade result applies to one finite suite and one frozen comparison. BL1's prior-art review was bounded rather than systematic. No independent laboratory replicated the cycle's results.

The retrospective synthesis is also vulnerable to selection and narrative bias: the cycle's documents were created for evolving research goals, and the present audit is performed by the same project lineage. We therefore present source paths and exact claim boundaries, avoid asserting that the process itself is validated, and preserve the distinction between original frozen outcomes and later audits.

## 8. Conclusion

Research Cycle 1 did not establish a paper-ready ARC algorithm or a validated end-to-end ASFT theory. It did produce a detailed evidence record with narrow synthetic positives, failed comparative gates, mixed capability-metric outcomes, a low-coverage ARC result, one decision-grade N-FAIL for a finite predictive estimand, and a BL1 termination based on prior-art overlap rather than experimental efficacy.

The scientifically defensible article is therefore not “ASFT works,” “invariants beat replay,” or “counterexample boundary learning is novel.” It is a bounded case study of claim-level evaluation in one ARC-motivated research program. Whether that case study is sufficiently novel and useful for a particular venue remains an external editorial question. The paper should not be represented as a new general methodology, and it should preserve the finite, synthetic, and non-generalizable ceilings stated throughout.

## Data, code, and audit trail

The manuscript draws on saved records; it reports no new experiment or analysis. Source-of-truth artifacts include:

- `reports/experiments/PHASE-14J-FINAL-SCIENTIFIC-CONCLUSIONS-V1/` — final ASFT scientific synthesis and claim ceiling.
- `reports/experiments/PHASE-13H-EVIDENCE-CONSOLIDATION-V1/` — phase-by-phase evidence packages and machine-readable tables.
- `reports/experiments/T2T-S3-EXEC-2026-11-05-001/` — permanent S3 execution artifacts, hashes, committed predictions, outcomes, and N-FAIL decision.
- `docs/05_trace_to_transfer/claim_n_archive.md` and `docs/05_trace_to_transfer/current_evidence.md` — Claim N archive and current T2T evidence ceiling.
- `docs/05_trace_to_transfer/bl1/boundary_prior_art_review.md` — BL1 P0 prior-art disposition.
- `research_asset_inventory.md`, `arc_research_landscape_review.md`, `candidate_phenomena_ranking.md`, and `research_cycle_1_closure.md` — Research Cycle 1 inventory, landscape, ranking, and closure.

The archived execution and synthesis artifacts are to remain unchanged.

## References

1. Chollet, F. (2019). “On the Measure of Intelligence.” *arXiv:1911.01547*. https://arxiv.org/abs/1911.01547
2. Chollet, F., Knoop, M., Kamradt, G., & Landers, B. (2026). “ARC Prize 2025: Technical Report.” *arXiv:2601.10904*. https://arxiv.org/abs/2601.10904
3. ARC Prize Foundation (2026). “ARC-AGI-3: A New Challenge for Frontier Agentic Intelligence.” *arXiv:2603.24621*. https://arxiv.org/abs/2603.24621
4. Solar-Lezama, A. (2009). “The Sketching Approach to Program Synthesis.” https://people.csail.mit.edu/asolar/papers/Solar-Lezama09.pdf
5. Clarke, E. M., et al. “Counterexample-Guided Abstraction Refinement.” https://web.stanford.edu/class/cs357/cegar.pdf
6. Bagaria, A., et al. (2023). “Effectively Learning Initiation Sets in Hierarchical Reinforcement Learning.” *NeurIPS 2023*. https://proceedings.neurips.cc/paper_files/paper/2023/file/e8da56eb93676e8f60ed2b696e44e7dc-Paper-Conference.pdf
7. Hu, S., Lu, C., & Clune, J. (2025). “Automated Design of Agentic Systems.” *ICLR 2025*. https://arxiv.org/abs/2408.08435

---

**Internal editorial note:** The primary contribution is a retrospective case study, not a new ARC method. Before submission, the intended venue and its expectations for negative results, research-process case studies, and artifact auditability should be checked. No extra empirical claim should be added to strengthen the framing.