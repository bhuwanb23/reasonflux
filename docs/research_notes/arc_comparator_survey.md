# ARC comparator practice: a bounded survey of illustrative papers

**Prepared:** 2026-10-28  
**Scope:** exploratory review for manuscript framing, not a systematic census.  
**Question:** Can we support the claim that ARC papers mostly compare against weak baselines?

## Short answer

**No—not from this review.** “Weak baseline” is not a stable category unless the target claim, model family, data exposure, task split, candidate budget, compute, adaptation access, and scoring protocol are specified. A deliberately selected group of ARC papers includes both careful within-study contrasts and comparisons that are contextual rather than matched. It does not support a prevalence claim about the field.

The stronger, supportable point is that comparator adequacy is **claim-relative**: a baseline can be adequate for demonstrating that a component operates, but inadequate for attributing a system-level gain or claiming transfer. Cross-paper leaderboard tables are not automatically matched experiments.

## Inclusion and coding

We inspected six primary ARC or ARC-related works selected for relevance to ablations, generalization, or evaluation. This was a purposive sample, not a random sample. We coded the comparison type, the claim it can support, and the main residual confound. We did **not** rank baseline quality on a single scale or count “weak-baseline papers” because that requires paper-specific budgets and claim targets.

## Screened comparisons

| Work | Comparison design | What it can support | Limits for claims beyond the design |
|---|---|---|---|
| ConceptARC (Moskvichev et al., 2023) | Human participants and three solvers on a concept-organized benchmark | Relative performance on concept-group tasks; a direct test beyond ordinary ARC headline accuracy | Not an ablation of a solver mechanism; concept-level task performance is not causal attribution to internal mechanisms. [Paper](https://arxiv.org/abs/2305.07141) |
| Ouellette (2025), execution-guided NPS vs. TTFT | Controlled compositional-generalization experiment comparing execution-guided NPS, non-execution-guided NPS, and test-time fine-tuning | Relative performance on the designed compositional setting; one can ask whether execution feedback helps that defined task family | Task-family and DSL scope bound transfer; the review should inspect resource and data matching before calling the comparator fully matched. [Paper](https://arxiv.org/abs/2507.15877) |
| Franzen et al. (ICML 2025), Product of Experts | Internal component ladder: baseline → TTT → 16× augmentation → PoE → DFS; also reports contextual systems | Incremental component effects within its own pipeline/configuration; ablations are more informative than the headline public score alone | Published external systems differ in model, data, split, compute and protocol; its table is context, not a controlled head-to-head. [Paper](https://arxiv.org/abs/2505.07859) |
| Moghe & Chin (2026), agent harnesses | Same-model/provider architectures and ablations on the same ARC-AGI-1 public task set, with reported cost and paired-task comparisons | Architecture/component increments under that fixed public evaluation setup | Public-set exposure, single-model dependence for main comparisons, and no independent ARC-AGI-2 distribution test constrain broad generalization. [Paper](https://arxiv.org/abs/2607.06764) |
| CompressARC (Liao & Gu, 2025) | Includes a U-Net baseline under a similar no-pretraining/per-task-training constraint; also gives cross-paper contextual comparisons | A baseline comparison designed around the method's key resource constraint | External table entries have differing training and evaluation regimes; contextual leaderboard results should not be treated as matched controls. [Paper](https://arxiv.org/abs/2512.06104) |
| ARC Prize 2024 Technical Report | Competition and leaderboard comparisons, plus explicit discussion of private-set reuse, compute, and split comparability | Competition-level progress and benchmark-design lessons | Entrants are not a single matched experimental study; score differences do not isolate component causes. [Report](https://arxiv.org/abs/2412.04604) |

## Interpretation

The evidence supports these distinctions:

1. **Within-paper ablations exist.** Product of Experts and the 2026 harness study give examples of component-level contrasts; it would be inaccurate to imply that ARC papers uniformly omit them.
2. **Controlled generalization studies exist.** Ouellette directly frames an ARC-domain comparison around compositional OOD performance; ConceptARC targets concept-group generalization.
3. **Leaderboard comparisons are not causal component comparisons.** Reports across systems are useful context but usually differ in model, data, compute, or protocol.
4. **A baseline's adequacy depends on the claim.** One-shot may be relevant to total scaffold lift, but not sufficient to isolate an invariant-representation increment if a strong replay/compiler arm is the actual alternative.
5. **Generalization remains its own axis.** A matched ablation on public ARC-AGI-1 can establish within-benchmark incremental value without demonstrating transfer to ARC-AGI-2, ARC-AGI-3, or a new task generator.

## Answer to the requested count

This review **cannot responsibly answer “how many published ARC papers compare only weak baselines?”** The sample is purposive, “weak” is not pre-defined independently of the claim, and several papers' baseline conditions require a full methods-level audit. A prevalence number would be misleading. The safe manuscript statement is:

> “ARC papers use heterogeneous comparator strategies. Some report controlled component ablations or explicit generalization contrasts; other tables compare systems under different data, compute, and evaluation conditions. Therefore, comparator strength must be judged against the particular claim, not inferred from the presence of a leaderboard table.”

## Relevance to the archived case study

The archive offers a concrete *within-program* comparator lesson, not proof of an ARC-wide weakness: T2T S3 compared I0 to a fairness-reviewed R4 replay/compiler baseline on one frozen synthetic predictive estimand, where both scored 105/105. That supports an N-FAIL for this finite estimand and illustrates claim-relative comparator design. It does not demonstrate that ARC literature generally uses weak baselines.

## References

- Moskvichev, A., Odouard, V. V., & Mitchell, M. (2023). *The ConceptARC Benchmark: Evaluating Understanding and Generalization in the ARC Domain*. TMLR. https://arxiv.org/abs/2305.07141
- Ouellette, S. (2025). *Out-of-Distribution Generalization in the ARC-AGI Domain: Comparing Execution-Guided Neural Program Synthesis and Test-Time Fine-Tuning*. arXiv:2507.15877. https://arxiv.org/abs/2507.15877
- Franzen, D., Disselhoff, J., & Hartmann, D. (2025). *Product of Experts with LLMs: Boosting Performance on ARC Is a Matter of Perspective*. ICML 2025. https://arxiv.org/abs/2505.07859
- Moghe, K., & Chin, P. (2026). *Cost-Effective Agent Harnesses for Abstract Reasoning and Generalization on ARC-AGI-1*. arXiv:2607.06764. https://arxiv.org/abs/2607.06764
- Liao, I., & Gu, A. (2025). *ARC-AGI Without Pretraining*. arXiv:2512.06104. https://arxiv.org/abs/2512.06104
- Chollet, F., Knoop, M., Kamradt, G., & Landers, B. (2025). *ARC Prize 2024: Technical Report*. https://arxiv.org/abs/2412.04604
