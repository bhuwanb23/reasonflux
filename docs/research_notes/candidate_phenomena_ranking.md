# Candidate Phenomena Ranking

**Purpose:** Rank candidate ARC phenomena after the landscape review. This is a screening document only—not a program decision, protocol, implementation plan, or experiment authorization.  
**Decision boundary:** No descendant of ASFT, T2T, or BL1 is proposed. The ranking uses ARC literature and benchmark evidence only.

## Rank 1 — Harness adaptation transferability

### Section A — Phenomenon

Human-steered harnesses can produce near-ceiling performance on ARC-AGI-3, while LLM-authored revisions do not reliably convert development-game improvement into held-out improvement. In a recent controlled ARC-AGI-3 study, 27 lineages and two revisions produced a mean held-out gain of 2.80 RHAE points with a 95% interval spanning zero (`[-1.44, 7.35]`); development gains exceeded held-out gains. [Lehmann & Vahdati, 2026](https://arxiv.org/abs/2610.30499)

### Section B — Why scientifically interesting

This may reveal a difference between **solving through an effective engineered scaffold** and **acquiring the ability to improve one's own adaptation process**. It is a direct, measurable form of the broader question of how systems turn experience into transferable changes.

### Section C — Strongest prior-art overlap

- Direct ARC-AGI-3 study of autonomous harness construction and revision: [Can LLMs Improve Their Own Harness?](https://arxiv.org/abs/2610.30499).
- General automated agent/workflow design and optimization: [ADAS](https://arxiv.org/abs/2408.08435), evolutionary harnesses, and automated workflow-search literature.
- ARC-specific executable-world-model and agent-harness systems: [Tycho](https://arxiv.org/abs/2607.28287), [Schema](https://arxiv.org/abs/2609.39140), and related work.

### Section D — Novelty risk

**HIGH.** The core question “can an agent improve its own harness and generalize?” has direct ARC prior art, while the broader mechanism is an active and crowded agent-optimization area. Any distinct contribution would have to explain *which* edits transfer, under *which* environment changes, and why—not simply rerun the headline comparison.

### Section E — Estimated path to a paper

Potentially paper-scale if a distinct explanatory regularity emerges linking harness changes and transfer across genuinely new environment mechanics, rather than reporting another aggregate score or harness recipe. Novelty and evidential separation from the October 2026 study are unresolved.

### Section F — Kill condition

Kill if the October 2026 study or follow-on work already explains the edit-level transfer/regression pattern; if observed differences are accounted for by score noise, model/effort or evaluation mismatch; or if the proposed contribution reduces to a new instance of existing ADAS/harness optimization.

---

## Rank 2 — Extreme harness/state sensitivity of interactive ARC performance

### Section A — Phenomenon

ARC Prize's verified GPT-6 Astra evaluation reports a large score difference between its Standard and Provider Adapter interfaces on the same Semi-Private benchmark: at maximum reasoning effort, 62.7% with Standard versus 98.6% with Provider Adapter; the adapter preserves provider-side reasoning state and compacts context. At high effort, the Provider Adapter score is 99.9%. These are configuration-conditioned system scores, not a weights-only result. [ARC Prize results](https://arcprize.org/results/openai-gpt-6-astra) · [ARC Prize analysis](https://arcprize.org/blog/astra)

### Section B — Why scientifically interesting

The size of the difference raises a basic measurement question: how much of “agent capability” is in the model, and how much depends on retained state, context handling, and the serving interface? It also makes replication and comparisons across providers difficult unless the whole system configuration is part of the claim.

### Section C — Strongest prior-art overlap

- ARC Prize's paired verified Standard/Provider Adapter comparison and analysis already document the phenomenon: [official results](https://arcprize.org/results/openai-gpt-6-astra), [official analysis](https://arcprize.org/blog/astra).
- Persistent memory, context management, reasoning-state retention, and harness effects are established topics in agent systems; [Schema](https://arxiv.org/abs/2609.39140) and other harness papers address related components.
- ARC-AGI-3's own design/reporting discusses human-relative action efficiency and public/private score interpretation: [technical report](https://arxiv.org/abs/2603.24621).

### Section D — Novelty risk

**HIGH.** The headline effect has already been measured and discussed by the benchmark owner. The unisolated contribution of individual adapter features is a narrower potential gap, but state retention and context engineering have substantial adjacent prior art.

### Section E — Estimated path to a paper

A publishable contribution would need to explain the performance shift at the component or generalization level and establish that the explanation is not specific to one provider interface or one benchmark split. A simple restatement of the score gap is not a paper contribution.

### Section F — Kill condition

Kill if existing or forthcoming controlled comparisons isolate the relevant components and explain the shift, or if the score gap is attributable to non-comparable effort, hidden provider behavior, or other configuration differences that cannot support a general scientific conclusion.

---

## Rank 3 — Human and agent differences in uncertainty and representation during first-contact learning

### Section A — Phenomenon

In an October 2026 ARC-AGI-3 think-aloud dataset, qualitative mechanism descriptions were observed in 50.0% of successful human trajectories versus 14.3% of selected successful LLM/harness trajectories. The paper also reports differences in hypothesis-free exploration, uncertainty expression, correction, and recovery. These are descriptive findings, not causal evidence that one style is more effective. [Liu et al., 2026](https://arxiv.org/abs/2610.34523)

### Section B — Why scientifically interesting

The patterns may help explain how humans learn unfamiliar mechanics without committing prematurely to a detailed but incorrect model—and whether representation granularity and expressed uncertainty affect efficient correction and planning.

### Section C — Strongest prior-art overlap

- Direct ARC-AGI-3 human/LLM trajectory and think-aloud dataset: [How Humans Learn Unfamiliar Worlds](https://arxiv.org/abs/2610.34523).
- Earlier human ARC-solving datasets, think-aloud research, cognitive models of hypothesis testing, and world-model learning.
- ARC-AGI-3 harness papers already analyze hypothesis formation, model revision, and recovery: [Tycho](https://arxiv.org/abs/2607.28287), [Schema](https://arxiv.org/abs/2609.39140).

### Section D — Novelty risk

**HIGH.** A direct, recent ARC-specific dataset and analysis now cover the headline phenomenon. Comparability limits and descriptive design leave explanatory questions, but the broad “humans reason differently from LLMs” framing is not novel.

### Section E — Estimated path to a paper

Only plausible if a distinctive, robust relation between a process feature (e.g., uncertainty calibration or representation granularity) and held-out learning/efficiency can be separated from verbalization style, success selection, model configuration, and harness differences.

### Section F — Kill condition

Kill if apparent differences disappear under matched trajectory visibility and coding, are explained by success-only selection or verbal reporting differences, or if the claimed process-to-outcome relation is already established in the new dataset or broader cognitive literature.

---

## Rank 4 — Action efficiency and inference cost can tell different stories

### Section A — Phenomenon

ARC-AGI-3 measures relative environment-action efficiency, while high-performing system runs can still incur substantial inference costs. For example, ARC Prize reports about $18,817 for GPT-6 Astra's high-effort Provider Adapter run, alongside a 99.9% RHAE result and fewer environment actions than the median human on most levels. The benchmark score and monetary/compute budget therefore describe different resource dimensions. [ARC Prize analysis](https://arcprize.org/blog/astra)

### Section B — Why scientifically interesting

A system can be highly efficient in its interaction with the world while consuming a large amount of compute to decide what to do. This matters for interpreting “skill-acquisition efficiency,” comparing human and machine performance, and distinguishing a short action plan from an efficient overall reasoning process.

### Section C — Strongest prior-art overlap

- ARC-AGI-2 and ARC Prize reports already treat cost per task as a performance axis; the ARC-AGI-3 technical report defines action-based scoring and reports system costs. [ARC Prize 2025 report](https://arxiv.org/abs/2601.10904) · [ARC-AGI-3 report](https://arxiv.org/abs/2603.24621)
- Test-time compute, inference-time search, and efficiency-vs-accuracy tradeoffs are heavily studied across reasoning systems.
- Astra's official analysis already presents both action performance and API cost. [Official analysis](https://arcprize.org/blog/astra)

### Section D — Novelty risk

**HIGH.** The existence of a cost/action tradeoff is known and reported. Novelty would require a non-obvious explanatory result or a construct-level finding, not simply adding another cost column to ARC scores.

### Section E — Estimated path to a paper

Potentially viable only if the relationship between internal inference expenditure, interaction actions, and generalization reveals a repeatable phenomenon that current cost-performance analyses do not explain. At present, that contribution is unclear.

### Section F — Kill condition

Kill if existing reporting already captures the effect, if cost comparisons cannot be standardized across proprietary providers, or if adding inference cost changes system rankings without yielding a distinct scientific explanation.

---

## Rank 5 — Public-game solvability may not measure exploration

### Section A — Phenomenon

The ARC-AGI-3 technical report says the public set is an easier demonstration surface and not a valid measure of progress. A recent preprint further claims that all 25 public games can be reached through simple or non-intelligent action strategies. The latter claim is not independently adjudicated here and should not be generalized to the Semi-Private or Private sets. [ARC-AGI-3 report](https://arxiv.org/abs/2603.24621) · [Explore Before You Solve](https://arxiv.org/abs/2605.25931)

### Section B — Why scientifically interesting

If high public-set scores can be achieved without the exploration or model-building the benchmark is meant to test, score interpretation and agent comparisons on that split may be misleading.

### Section C — Strongest prior-art overlap

- The benchmark owner explicitly limits the intended use of the public demonstration set and identifies hidden-set generalization as the evaluation target. [ARC-AGI-3 report](https://arxiv.org/abs/2603.24621)
- The recent *Explore Before You Solve* preprint directly analyzes public-game solvability and exploration claims. [Paper](https://arxiv.org/abs/2605.25931)
- General benchmark contamination, test-set reuse, and shortcut-solution concerns are longstanding.

### Section D — Novelty risk

**HIGH.** The validity concern is explicitly acknowledged by the benchmark design and directly examined in recent ARC-AGI-3 work. A broad claim that “public scores do not prove exploration” is already covered.

### Section E — Estimated path to a paper

Limited. A remaining contribution would need to identify a specific unaddressed validity failure on an intended evaluation split—not repeat the public-versus-private caveat.

### Section F — Kill condition

Kill if the claim rests only on public-set shortcuts, if the official evaluation already excludes the affected score from progress claims, or if the suspected shortcut does not generalize beyond the public games.

---

## Stop-condition outcome

**No justified new program.** Rank 1 is the strongest candidate, but it does not yet clearly survive the ranking exercise: direct ARC prior art already studies autonomous harness revision, and broader agent-design literature is substantial. The other candidates are either directly covered, too close to existing results, or dependent on a weak/public-only claim. Phenomenon interest is not enough to establish contribution clarity or novelty.

No P0, protocol, implementation, or experiment is created or authorized by this ranking.