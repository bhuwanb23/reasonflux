# ARC evaluation methodology and evidence-quality literature: targeted review

**Prepared:** 2026-10-28  
**Purpose:** identify prior work that addresses evaluation failures, benchmark interpretation, generalization, or evidence quality relevant to the proposed case study.  
**Status:** targeted narrative review; not systematic, exhaustive, or independently double-coded.

## Bottom line

The ARC literature already contains meaningful work on evaluation methodology. In particular, ConceptARC measures concept-level understanding/generalization rather than relying only on standard ARC accuracy; ARC Prize technical reports openly discuss benchmark limitations, score interpretation, compute, hidden-set exposure, and split comparability; controlled compositional-generalization studies test methods against alternatives; and a 2026 living survey explicitly analyzes evaluation practices. Thus a claim that evaluation quality is absent from ARC research is false or at least much too broad.

A narrower opportunity remains: **a cross-claim retrospective audit of one research program**, showing how operational mechanism evidence, utility evidence, comparator evidence, external validity, and prior-art decisions lead to distinct dispositions. The present archive can illustrate that process. It cannot establish that the process is novel, that it is common or rare across ARC papers, or that ARC research generally fails because claims are not isolated.

## Relevant literature

### 1. Benchmark construct and interpretation

- **Chollet (2019), “On the Measure of Intelligence.”** Establishes the intended construct—skill-acquisition efficiency on novel tasks—and motivates ARC as a benchmark. It is a foundation for distinguishing a task score from a broader intelligence claim. [arXiv](https://arxiv.org/abs/1911.01547)
- **Pfister & Jud (2025), “Understanding and Benchmarking Artificial Intelligence: OpenAI’s o3 Is Not AGI.”** An arXiv critique that argues high ARC scores under massive trialling do not establish broad AGI; it emphasizes the gap between benchmark performance and a general intelligence inference. This is conceptual/benchmark critique, not a controlled ARC mechanism experiment. [arXiv](https://arxiv.org/abs/2501.07458)
- **ARC Prize 2024 Technical Report (Chollet et al.).** The report discusses the ARC-AGI-1 private set's small size and repeated leaderboard feedback, differing split difficulty, and the dependence of scores on compute. This is direct precedent for benchmark-validity and score-interpretation discussion from benchmark authors. [arXiv](https://arxiv.org/abs/2412.04604)
- **ARC Prize 2025 Technical Report (Chollet et al.).** Reviews competition systems and the refinement-loop theme, and discusses knowledge coverage, contamination, and benchmark evolution. It is a field/competition synthesis, not an independent meta-analysis of every paper's comparator strength. [arXiv](https://arxiv.org/abs/2601.10904)
- **ARC-AGI-3 Technical Report (ARC Prize Foundation, 2026).** Establishes an interactive benchmark and explicitly separates public demonstration environments from private generalization evaluation. It illustrates evaluation design as a first-order research object, though it concerns an interactive benchmark rather than static ARC solver mechanisms. [arXiv](https://arxiv.org/abs/2603.24621)

### 2. Concept-level evaluation and generalization

- **Moskvichev, Odouard & Mitchell (2023), ConceptARC.** Builds concept-grouped ARC-style tasks specifically to probe abstraction and generalization and compares humans with multiple solvers. This directly anticipates the idea that standard task success alone may not establish concept understanding. [TMLR/arXiv](https://arxiv.org/abs/2305.07141)
- **Ouellette (2025), controlled compositional-generalization comparison.** Compares execution-guided neural program synthesis, non-execution-guided synthesis, and test-time fine-tuning on a designed ARC-domain compositional-generalization experiment. This is a strong counterexample to the generalization “ARC work only reports headline scores,” though conclusions are bounded by the constructed task family and program language. [arXiv](https://arxiv.org/abs/2507.15877)

### 3. Component attribution, ablation, and comparator examples

- **Franzen, Disselhoff & Hartmann (ICML 2025), Product of Experts with LLMs.** Presents a stepwise internal comparison of test-time training, augmentations, product-of-experts scoring, and search. Its internal component ladder is evidence that ARC work can test component contributions. Cross-paper leaderboard tables remain contextual because methods differ in data, architecture, split, and compute. [arXiv](https://arxiv.org/abs/2505.07859)
- **Moghe & Chin (2026), cost-effective agent harnesses.** Uses same-model, same-task comparisons and ablations, and reports cost; it identifies different bottlenecks in its pipeline. Its main results use ARC-AGI-1 public evaluation, so they should not be confused with independent distributional transfer. [arXiv](https://arxiv.org/abs/2607.06764)
- **Liao & Gu (2025), CompressARC / “ARC-AGI Without Pretraining.”** Compares against a U-Net baseline under the paper's no-pretraining, per-task adaptation constraint and reports other systems as context. This is an example of making the baseline relevant to a specific constraint, while external score tables still require protocol caveats. [arXiv](https://arxiv.org/abs/2512.06104)

### 4. Surveys and field-level evidence

- **Vahdati et al. (2026), “The ARC of Progress towards AGI: A Living Survey of Abstraction and Reasoning.”** An arXiv preprint submitted to ACM Computing Surveys that says it surveys 82 approaches and has a section on evaluation practice and public/semi-private comparisons. Its existence is direct prior art for field-level evaluation analysis. Its numerical claims and coding should be checked against the underlying paper list before being quoted; the abstract/HTML contains signs that some extracted figures or text may need verification. [arXiv](https://arxiv.org/abs/2603.13372)

## What is already established

- ARC papers and benchmark reports have distinguished benchmark score from broader claims about intelligence, understanding, or transfer.
- There are concept-level and compositional-generalization evaluations, not just leaderboard ranking.
- Some methods papers use matched within-paper baselines and ablations; others rely more heavily on contextual cross-paper comparisons.
- Benchmark and competition reports themselves discuss hidden-set feedback, split differences, compute, exposure, and evaluation validity.
- A broader ML venue now explicitly treats evaluation claim construction and interpretation as a scientific topic. The NeurIPS 2026 E&D call included auditing, methodology, and critical analysis—but its submission deadline has passed. [Call](https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets)

## What remains unproven for this manuscript

The literature found in this targeted screen does not establish that:

1. claim-level auditing is absent from ARC research;
2. most ARC papers use weak comparators;
3. a four-stage ladder is a novel or validated methodology;
4. the ASFT/T2T/BL1 case generalizes to other ARC laboratories; or
5. a long archive, by itself, constitutes a contribution.

The potentially defensible contribution is therefore a **case study with a reusable analytical presentation**, not a field-wide diagnosis. The manuscript should cite the precedents above, explicitly state how its lens differs, and use wording such as “in this archived research cycle” rather than “ARC research repeatedly.”

## Recommended manuscript wording

> “ARC evaluation is not an empty methodological space: prior work includes concept-centered benchmarks, controlled compositional-generalization tests, component ablations, and explicit critiques of benchmark validity. We therefore do not argue that ARC research has ignored evaluation. Instead, we present a retrospective case study that traces multiple claims in one ARC-motivated research cycle from mechanism occurrence through utility, comparative increment, and external validity, while keeping empirical negatives, unavailable endpoints, and prior-art decisions distinct.”

## References

1. Chollet, F. (2019). *On the Measure of Intelligence*. https://arxiv.org/abs/1911.01547
2. Pfister, R., & Jud, H. (2025). *Understanding and Benchmarking Artificial Intelligence: OpenAI’s o3 Is Not AGI*. https://arxiv.org/abs/2501.07458
3. Chollet, F., Knoop, M., Kamradt, G., & Landers, B. (2025). *ARC Prize 2024: Technical Report*. https://arxiv.org/abs/2412.04604
4. Chollet, F., Knoop, M., Kamradt, G., & Landers, B. (2026). *ARC Prize 2025: Technical Report*. https://arxiv.org/abs/2601.10904
5. ARC Prize Foundation (2026). *ARC-AGI-3: A New Challenge for Frontier Agentic Intelligence*. https://arxiv.org/abs/2603.24621
6. Moskvichev, A., Odouard, V. V., & Mitchell, M. (2023). *The ConceptARC Benchmark: Evaluating Understanding and Generalization in the ARC Domain*. https://arxiv.org/abs/2305.07141
7. Ouellette, S. (2025). *Out-of-Distribution Generalization in the ARC-AGI Domain: Comparing Execution-Guided Neural Program Synthesis and Test-Time Fine-Tuning*. https://arxiv.org/abs/2507.15877
8. Franzen, D., Disselhoff, J., & Hartmann, D. (2025). *Product of Experts with LLMs: Boosting Performance on ARC Is a Matter of Perspective*. https://arxiv.org/abs/2505.07859
9. Moghe, K., & Chin, P. (2026). *Cost-Effective Agent Harnesses for Abstract Reasoning and Generalization on ARC-AGI-1*. https://arxiv.org/abs/2607.06764
10. Liao, I., & Gu, A. (2025). *ARC-AGI Without Pretraining*. https://arxiv.org/abs/2512.06104
11. Vahdati, S., Aioanei, A., Suresh, H., & Lehmann, J. (2026). *The ARC of Progress towards AGI: A Living Survey of Abstraction and Reasoning*. https://arxiv.org/abs/2603.13372
