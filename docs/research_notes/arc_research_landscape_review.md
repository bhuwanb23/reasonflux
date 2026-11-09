# ARC Research Landscape Review

**Review cutoff:** 2026-11-05  
**Purpose:** Map major ARC research themes and identify whether a major, scientifically interesting phenomenon remains both unexplained and not already substantially covered.  
**Scope:** Static ARC-AGI-1/-2, the interactive ARC-AGI-3 transition, solver and harness families, human-process evidence, and benchmark/evaluation status. This is a bounded landscape review, not a systematic review. It does not define a protocol, propose an implementation, or authorize experiments.

## Executive read

The field's main performance phenomena are now extensively studied: program induction and search, neural/test-time adaptation, refinement loops, compositional generalization, interactive exploration, executable world models, memory/context handling, task-family generation, and human–agent process comparison all have direct ARC work. A broad framing such as “improve ARC reasoning,” “learn reusable skills,” “use counterexamples,” “build a world model,” or “explore more efficiently” is not a clean novelty claim.

The landscape has also changed sharply in 2026. ARC-AGI-3 was below 1% for frontier systems at launch, but ARC Prize's verified results now report GPT-6 Astra at 99.9% on the Semi-Private set with a Provider Adapter and 62.7% with the Standard harness. The adapter preserves provider-side reasoning state and compacts long context. These are system/interface-conditioned results, not a weights-only comparison; ARC Prize itself describes them separately. ARC-AGI-3's public demonstration games are expressly not a valid progress measure, and community harness scores on that set should not be compared as though they were independently verified hidden-set results.

**Landscape conclusion:** I do not find a broad ARC phenomenon that can now be confidently called both wholly unexplained and untouched by prior art. The strongest remaining candidate is narrower: **why harness and retained-state choices produce such large differences in interactive ARC performance, and when those gains represent transferable adaptation rather than system-specific scaffolding or development-set fit.** This is promising but not a cleared novelty claim: direct ARC evidence and related harness-optimization literature already exist, and an October 2026 controlled study directly examines autonomous harness revision. The unresolved piece is explanatory attribution and generalization, not the existence of harness effects.

## 1. Field map: what is already covered

| Research area | Established lines of work | Landscape status |
|---|---|---|
| **Static ARC rule induction and program search** | DSL-based program synthesis, constraint/search methods, neuro-symbolic solvers, object-centric representations, ensembles and multi-hypothesis selection. | Mature and crowded. “Infer the rule from few examples” and “improve search” alone are not novel. |
| **Neural solving and test-time adaptation** | Test-time training, synthetic ARC-like data, zero-pretraining/small-network approaches, recursive refinement, direct grid prediction, and hybrid solvers. | Broad coverage; results depend heavily on training exposure, search/computation, data split, and evaluation budget. |
| **Compositional generalization / version gap** | ARC-AGI-2 deliberately emphasizes interacting rules, sequential transformations, contextual symbol definitions, and greater task difficulty. Surveys compare cross-version degradation and solver families. | Widely recognized and directly measured. A generic “models struggle with composition” question is saturated at the framing level. |
| **Iterative refinement and feedback** | ARC Prize 2025 identifies refinement loops across program evolution, verifier feedback, and weight-space adaptation as a central method family. | Established. Counterexample/refinement loops are not new as a general mechanism. |
| **Interactive ARC-AGI-3 exploration, dynamics, and goals** | Graph-based exploration, active probing, executable world models, model repair, program induction, planning, and game-specific/harness orchestration. | Fast-moving and already directly studied. “Build a world model and plan” is not an uncovered direction. |
| **Human reasoning processes** | Human action/replay datasets and, most recently, synchronized ARC-AGI-3 think-aloud reports paired with environment actions, feedback, mechanism annotations, and LLM trajectories. | A new evidence base exists. Initial differences are descriptive and selection-limited; the broad human-vs-agent process question is no longer untouched. |
| **Harness / agent design and self-improvement** | General ADAS/meta-agent search, workflow optimization, evolutionary harness modification, and direct ARC-AGI-3 harness studies. | The general idea is mature outside ARC; ARC-specific controlled evidence is emerging. The unsolved issue is when revisions transfer and why they regress, not whether harnesses matter. |
| **Task generation and benchmark integrity** | ARC-TGI and other task-family generators support resampling, controlled variation, reasoning templates, and human validation; benchmark papers explicitly address private splits and contamination. | Strong prior art for generated/resampled tasks and leakage-resistant evaluation. New work must distinguish task-family generalization from fixed-set tuning. |

A 2026 living survey reports a broad cross-generation review of 82 approaches through early 2026, but its cutoff predates several important ARC-AGI-3 papers and verified results from later in 2026. It is useful for the static-ARC map, not a complete account of the current interactive frontier. [Vahdati et al., *The ARC of Progress towards AGI: A Living Survey*](https://arxiv.org/abs/2603.13372)

## 2. The current ARC-AGI-3 signal: do not confuse score, model, harness, and generalization

ARC-AGI-3 shifts from static input-output tasks to interactive, turn-based environments in which agents must explore, infer mechanics and goals, and plan under an action-efficiency score. Its technical report states that the public demonstration set is intentionally easier and is not a valid progress measure; the private sets are the intended generalization test. [ARC-AGI-3 Technical Report](https://arxiv.org/abs/2603.24621)

By the review cutoff, ARC Prize's official results page showed results far beyond the March launch baseline. The clearest diagnostic is its paired GPT-6 Astra report: on the Semi-Private set, Astra scored 62.7% with the Standard harness and up to 99.9% with the Provider Adapter. The Foundation describes the adapter as preserving opaque reasoning state between requests and compacting long conversations; it also reports substantial API costs. Thus the high score is evidence about a configured model-plus-interface system, not evidence that the model weights alone acquired the same performance. The task/action score also does not fully price inference cost. [ARC Prize verified results](https://arcprize.org/results); [Astra evaluation and harness details](https://arcprize.org/blog/astra)

Three consequences for interpreting the literature:

- Public-set saturation and hidden-set generalization are different questions. Self-reported public scores from custom harnesses are not equivalent to ARC-verified Semi-Private results.
- “Model capability” is not a stable unit unless the harness, retained state, reasoning settings, tools, retries, and costs are specified. Harness choice can change results dramatically.
- Near-ceiling action efficiency does not by itself explain what knowledge is retained, which components transfer to unseen mechanics, or how much computation was used to obtain it.

## 3. Closest prior work on the remaining candidate

### 3.1 ARC-specific harness and world-model work

- **Executable world models:** *Executable World Models for ARC-AGI-3 in the Era of Coding Agents* reports verifier-driven executable models on the 25 public games and explicitly notes that private evaluation is needed for generalization. [Paper](https://arxiv.org/abs/2605.05138)
- **Tycho:** *Active Abstraction with Programmatic World Models for ARC-AGI-3* compares orchestration policies on the public games and distinguishes model fit from effective use: accurate transition replay does not guarantee correct goal inference or a better next action. It directly studies when to construct, repair, use, or bypass an executable model. [Paper](https://arxiv.org/abs/2607.28287)
- **Schema:** *Discovering Unknown Environments via Agentic Program Induction* uses a persistent code workspace, tests program hypotheses against interaction histories, and plans within them. Its reported high public-set performance is self-reported; the authors disclose that status. [Paper](https://arxiv.org/abs/2609.39140); [project/results disclosure](https://schema-harness.github.io/)
- **Exploration critiques:** *Explore Before You Solve* examines action-selection and exploration claims on the public games, including trivial-action and benchmark-validity concerns. It is a recent preprint and its strongest claims should not be treated as independently replicated; it nevertheless makes “more exploration” an already-claimed ARC topic. [Paper](https://arxiv.org/abs/2605.25931)

### 3.2 Human-process and autonomous-revision evidence

- **Human think-aloud data:** *How Humans Learn Unfamiliar Worlds* (25 October 2026) aligns 144 successful human trajectories from 64 people with speech and gameplay across 25 public games, and compares them with 250 LLM trajectories. It reports more qualitative mechanism descriptions in successful human trajectories than in selected successful harness trajectories (50.0% vs 14.3%) and differences in hypothesis-free exploration. These are descriptive comparisons, not causal estimates of why a strategy works; the systems and successful-trajectory selections are not a fully matched intervention. [Paper](https://arxiv.org/abs/2610.34523)
- **Autonomous harness revision:** *Can LLMs Improve Their Own Harness? A Controlled Study on ARC-AGI-3* (21 October 2026) evaluates 27 lineages, 81 frozen snapshots, and held-out games after two rounds of revision. Mean held-out change is small and uncertain (+2.80 RHAE; 95% interval [-1.44, 7.35]); development-set gains overstate held-out gains, and cost reductions may trade off with performance. It is direct prior art for asking whether an agent can improve the scaffold through which it acts. The authors' result is bounded to their bootstrap, five development games, two revisions, model/effort conditions, and holdout; it does not explain what edits or game properties determine transfer. [Paper](https://arxiv.org/abs/2610.30499)
- **General automated agent design:** ADAS/meta-agent search and later workflow/harness evolution research cover automated construction and optimization of agent scaffolds beyond ARC. Therefore “automated harness design” or “self-improving agent” alone cannot be positioned as new. [ADAS, ICLR 2025](https://arxiv.org/abs/2408.08435)

## 4. Candidate phenomenon and novelty judgment

### Candidate, stated narrowly

> **Interactive-ARC harness adaptation is highly configuration-sensitive, yet agent-authored revisions do not reliably convert development-game experience into held-out gains. What properties of the learned state, edits, and environment change explain when an adaptation transfers versus regresses?**

This candidate is independent of the closed ASFT/T2T/BL1 line: it arises from ARC-AGI-3 results and current ARC literature. The phenomenon has a real empirical anchor: the same model has sharply different verified results under Standard and Provider Adapter interfaces, and a controlled harness-revision study finds weak/uncertain average held-out improvement despite development progress. A contemporaneous human-process dataset provides potential descriptive evidence about how beliefs, actions, and revisions unfold.

### Prior-art overlap and what is not yet settled

- **Already covered:** executable world models, programmatic hypothesis checking, persistent state, exploration/planning loops, and automated harness search/revision.
- **Directly tested:** ARC harness sensitivity and one bounded self-revision protocol; human and agent behavior have newly been annotated in an ARC-AGI-3 think-aloud dataset.
- **Not resolved by the sources reviewed:** component-level explanation of the Standard-vs-Provider-Adapter gap; why some harness revisions transfer while others regress; whether those effects persist on mechanics not used for development; and how to attribute gains among model, retained state, search, tool use, and compute.
- **Novelty risk:** high. These unresolved details sit next to an active body of work in agent/workflow optimization and several very recent ARC papers. A contribution framed as “a better harness,” “world-model induction,” “human-like exploration,” or “self-improving agents” would overlap substantially. A narrower explanatory question might remain worthwhile, but this bounded review does not establish priority or clear a paper claim.

## 5. Bottom line

The **closest potentially unsaturated phenomenon** is the transfer and failure behavior of harness-level adaptation on interactive ARC: why strong configured systems can approach benchmark ceilings while autonomous harness revisions show uncertain held-out gains, and which components or environment properties account for that mismatch.

This is a **provisional landscape lead, not a recommendation, protocol, or novelty clearance**. The broad phenomenon of harness effects is already studied. The question is plausibly paper-scale only if future bibliographic review shows that the specific attribution/generalization gap is not already covered outside ARC and if the public/private evaluation distinction is respected. The present review does not propose a program or authorize subsequent work.

## Sources reviewed

1. [ARC Prize 2025 Technical Report](https://arxiv.org/abs/2601.10904) — current static ARC methods, competition outcomes, refinement loops, and contamination concerns.
2. [The ARC of Progress towards AGI: A Living Survey](https://arxiv.org/abs/2603.13372) — cross-generation survey through early 2026; preprint and not current through this review's cutoff.
3. [ARC-AGI-3 Technical Report](https://arxiv.org/abs/2603.24621) — benchmark purpose, public/private split, human calibration, scoring, and harness policy.
4. [ARC Prize Results](https://arcprize.org/results) and [GPT-6 Astra analysis](https://arcprize.org/blog/astra) — official verified scores, interface conditions, and costs as of the review cutoff.
5. [Executable World Models for ARC-AGI-3](https://arxiv.org/abs/2605.05138) — early public-set executable-model results and explicit generalization caveats.
6. [Explore Before You Solve](https://arxiv.org/abs/2605.25931) — exploration strategy and public benchmark critique; recent preprint, not independently adjudicated here.
7. [Tycho](https://arxiv.org/abs/2607.28287) — matched public-set orchestration comparison and active-abstraction framing.
8. [Schema](https://arxiv.org/abs/2609.39140) — program induction and persistent-workspace harness for interactive worlds; self-reported public-set results are not treated as verified hidden-set evidence.
9. [Can LLMs Improve Their Own Harness?](https://arxiv.org/abs/2610.30499) — direct controlled ARC-AGI-3 harness-revision study, submitted October 2026.
10. [How Humans Learn Unfamiliar Worlds](https://arxiv.org/abs/2610.34523) — October 2026 human think-aloud/action dataset and descriptive human–agent comparison.
11. [Automated Design of Agentic Systems](https://arxiv.org/abs/2408.08435) — broader prior art on automated agent/harness design outside ARC.
12. [ARC-TGI](https://arxiv.org/abs/2603.05099) — task-family generation, human validation, and resampleable ARC evaluation.