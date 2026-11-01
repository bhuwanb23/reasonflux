# ARC Prize 2026 Paper Track — ASFT v0.1 Readiness Assessment

**Assessment date:** 1 November 2026 (Asia/Kolkata)  
**Basis:** saved ASFT Phase 11–14 project records; official ARC Prize 2026 Paper Track requirements; no new ASFT experiments or rescoring.

## Bottom line

**Could ASFT submit a paper? Yes, if the competition-entry requirements are met. Is it currently a plausible top-three contender based on the evidence available here? Unlikely.**

The project has a serious strength as a transparent synthetic-systems and negative-results study. It does not yet have the evidence profile of a strong ARC paper-track submission: no Kaggle prediction-track submission ID or leaderboard score is present in the project records, and Phase 13G is a low-coverage evaluation on a split of ARC-AGI-2 public training tasks—not a Kaggle leaderboard result. The paper track requires a linked Kaggle code submission for ARC-AGI-2 or ARC-AGI-3; its score is used for the Accuracy criterion. A high score is not required for eligibility, but it still matters to the rubric. [Paper Prize rules](https://arcprize.org/competitions/2026/paper)

The Kaggle Paper Track also requires a final writeup (maximum 1,500 words), a public notebook, and a media gallery with a cover image. The listed deadline is **9 November 2026, 23:59 UTC**—**10 November, 05:29 IST**. A draft writeup is not a final submission. [Kaggle competition page](https://www.kaggle.com/competitions/arc-prize-2026-paper-track)

**Eligibility status from the available artifacts: unconfirmed / currently not evidenced.** If there is no Kaggle submission ID outside this workspace, the immediate issue is not paper quality: the qualifying entry has not been demonstrated.

## What in the supplied assessment is fair—and what needs correction

### Directionally fair

- The project shows unusual breadth: implementation, multiple synthetic experiments, baselines, ablations, ARC testing, integrity review, and unusually candid claim reduction.
- Narrow synthetic pattern detection, construction of reflection/rotation skill objects, reuse, and simulator reasoning-step savings survive the audits.
- Transfer-aware ranking did not beat frequency/no-transfer on the primary corrected Phase 13B endpoint; SCT tied always-create/random-create in its primary Phase 13C pool; memory retrieval remains a live alternative.
- Capability/intelligence interpretations and ARC external validity are not established.

### Overstated or too absolute

1. **“ARC demonstrated the representation bottleneck.”** Low coverage is the strongest *proximate* diagnosis for the tested adapter, but it is not proven to be the sole cause. Phase 13G also has a config/code budget mismatch: config says three candidates per task, while `discover()` defaults to ten. The test does not isolate representation from task difficulty or other implementation choices.
2. **“0 IG.”** Phase 13G IG/CGR are **unavailable**, not measured zeros, because no validated capability group formed.
3. **“The entire software pipeline functions end-to-end.”** Phase 11 reports an end-to-end prototype and passing tests; the synthetic trace→skill→reuse subchain is observed. The complete capability→intelligence theory chain is not validated.
4. **“Capability growth predicts performance: not supported.”** This needs qualification: Phase 13E’s preregistered `C_t`→next-round task-utility association was positive but very small (`r=0.0498`, cluster CI `[0.0163,0.0922]`). It is within-cohort and noncausal; it does not establish transfer→growth or intelligence growth.
5. **“Novelty 7/10” and “publishability 6.5–8/10.”** These are not validated by the experiment record. Novelty needs explicit prior-art comparison, and the Kaggle rubric is different from general publication readiness.

## Rubric-based outlook

The organizers score Accuracy, Universality, Progress, Theory, Completeness, and Novelty equally. This is a directional assessment—not a judge score or win-probability model.

| Criterion | ASFT v0.1 outlook today | Reason |
|---|---|---|
| **Accuracy** | **Unscored / likely weak until a leaderboard entry exists** | Phase 13G’s `1/200` holdout result is from public training tasks and is not a leaderboard score. The Kaggle rubric uses the linked submission’s score. |
| **Universality** | **Weak** | Positive evidence is concentrated in synthetic tasks; ARC mechanisms did not activate under the bounded adapter. |
| **Progress** | **Weak-to-moderate at best** | The architecture and negative findings may be useful, but current results do not demonstrate an improvement likely to move ARC toward the competition’s high-score target. |
| **Theory** | **Moderate potential, weak validation** | Careful causal decomposition is a strength; the first three links are narrow, while transfer→capability and capability→intelligence remain unestablished. |
| **Completeness** | **Strong research archive; incomplete competition artifact until linked** | The Phase 11–14 record is extensive. A public notebook, valid code submission ID, writeup within 1,500 words, and cover/media still need confirmation. |
| **Novelty** | **Uncertain / potentially moderate** | Trace-driven invariant/skill integration may be distinctive, but overlap with program synthesis, memory/retrieval, and prior ARC learning systems needs a concise related-work analysis. |

I would **not** confidently attach a numeric prize score. If forced to estimate under the assumption that a valid notebook is submitted but its leaderboard performance is poor, I would expect the paper to be more competitive on Completeness and possibly Theory/Novelty than on Accuracy, Universality, or Progress. That profile makes a top-three award **low probability**, not impossible. The 2025 ARC Prize included 90 paper submissions and selected technically substantial conceptual contributions; this is a competitive field, not a reward for documentation quality alone. [2025 results](https://arcprize.org/blog/arc-prize-2025-results-analysis)

## Recommendation

Treat the project as a **credible negative-results/synthetic-mechanisms paper**, not as an ARC-solving entry or validated theory of intelligence. Do not present the internal `1/200` ARC holdout as a Kaggle leaderboard result.

Before deciding to submit, verify all of the following:

1. A qualifying ARC-AGI-2 or ARC-AGI-3 Kaggle code submission exists and has a submission ID that can be linked to the paper.
2. The public notebook actually runs the submitted method and corresponds to the submitted code; report the actual leaderboard score, even if low.
3. The Kaggle writeup is at most 1,500 words, selects the required track, includes a cover image in the media gallery, and is finally submitted—not left as a draft.
4. The writeup states clearly that Phase 13G used public training tasks, that ARC mechanisms did not activate, that the official evaluation was not scored in Phase 13G, and that the discovery-budget discrepancy and holdout caveat exist.
5. The novelty section compares the approach with relevant ARC, program-synthesis, test-time adaptation, and episodic-memory work; avoid asserting novelty from architecture labels alone.

### Final judgment

**As a research project:** strong engineering/research-process effort with valuable synthetic results and negative findings, but incomplete theoretical validation.  
**As an ARC paper-track contender today:** **not yet competition-ready on the evidence available; top-three win is unlikely without a valid linked Kaggle entry and a compelling, clearly novel contribution.** Eligibility is still possible even with a low score, but a low score would hurt the Accuracy criterion.

If a Kaggle submission ID and score already exist outside the saved project records, they would materially change the eligibility and Accuracy assessment.
