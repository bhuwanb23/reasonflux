# ARC Prize 2026 Paper Track — Strategy and Project Fit

**Research checked:** 2026-11-03 (Asia/Kolkata)  
**Scope:** Official ARC Prize/Kaggle rules, prior paper-award outcomes, and the current ReasonFlux/ASFT evidence state. This is a strategy assessment, not a promise of eligibility or a prediction of winning.

## Executive decision

**Current owner status:** the user confirms that no ARC code submission or Paper Track entry has yet been made; their team is on ARC-AGI-3, has joined that track, and can make a late submission. Proceed on the ARC-AGI-3 route to prepare matching paper materials, but distinguish technical acceptance/scoring from prize eligibility. The Paper Track is not standalone: it requires a real code submission to ARC-AGI-2 or ARC-AGI-3 and uses the linked submission's score for Accuracy. [S1][S2]

The ordinary ARC-AGI-2/3 entry deadline (Oct 26 UTC) and final-submission deadline (Nov 2 UTC) have passed. The owner reports the team joined ARC-AGI-3 and the late-submission route is available. Kaggle’s rules require registration before the Entry Deadline and say late submissions are not prize-eligible in the code competition. The Paper Track requires a matching team making an ARC code submission, and ARC Prize says the linked code submission need not score highly, but neither public text explicitly states whether the linked code entry must itself be on-time/prize-eligible. Late linkage is plausible but not guaranteed. **Do not claim eligibility until confirmed.** Capture a platform-generated ID/score and seek sponsor confirmation. [S1][S2][S3][S4][S9]

The paper deadline is inconsistent across official pages: Kaggle says **Nov 9, 2026, 23:59 UTC**; ARC Prize's 2026 overview says papers are due **Nov 8**. Use **Nov 8, 23:59 UTC (Nov 9, 05:29 IST)** as the internal deadline. Paper-track rules also require the paper team to match the team that made the code submission. [S1][S5][S9]

**Current project fit:** no linked submission ID/score is present in the workspace. The local ARC-AGI-3 validation document is a design draft with no runs/results; Phase 2I candidate production remains unauthorized, and WP3 remains incomplete. Existing Phase 13G evidence is a bounded ARC-AGI-2 diagnostic, not an ARC-AGI-3 result. The AGI-3 paper must match the exact interactive agent in the late submission; none of the existing results can be represented as its score. Thus, the project is **not yet evidenced as a 2026 Paper Track contender**. Do not write around those gaps as though they were results.

## What this event is—and why it exists

Kaggle is the competition and notebook platform; the listed host for the ARC competitions is the Abstraction and Reasoning Corpus/ARC Prize organization. Google announced its acquisition of Kaggle in 2017. [S1][S6]

ARC Prize is using the competition to encourage open, reproducible progress on systems that adapt to unfamiliar tasks. The Paper Prize specifically rewards **conceptual progress**, not merely a high score: the paper must explain a working ARC-AGI-2 or ARC-AGI-3 entry, why its approach works, and what others can reuse. The official pages require an associated Kaggle code submission and say its score is used for Accuracy. [S2][S5]

The 2026 Paper Track advertises a $75,000 top-paper pool ($50,000/$20,000/$5,000) and a separate $375,000 pool for papers scoring above 4.5/5, at host discretion. The paper rubric has six equally weighted 0–5 categories: **Accuracy, Universality, Progress, Theory, Completeness, Novelty**. Kaggle also says a tie goes to the paper submitted first. [S1][S2]

## What prior winners suggest

In 2025, 1,455 teams filed 15,154 competition entries and **90 papers** were submitted, up from 47 the prior year. The paper field is therefore substantial; polished prose alone is not a differentiator. [S7]

The first-place paper, **“Less is More: Recursive Reasoning with Tiny Networks,”** presented a concrete recursive-refinement mechanism in a roughly 7M-parameter model and reported about 45% on ARC-AGI-1 and 8% on ARC-AGI-2. Second place focused on self-improving evolutionary program synthesis; third place, **“ARC-AGI Without Pretraining,”** emphasized a distinct no-pretraining route. The important lesson is not to copy these methods: winning papers make one legible technical contribution, connect the mechanism to evidence, expose limitations, and provide usable artifacts. [S7][S8]

The 2025 high-score winner NVARC scored 24.03% on the ARC-AGI-2 private evaluation; its approach was a separate solution track from the paper-award winner. This illustrates that code leaderboard performance and paper-award recognition overlap but are not identical. [S7]

## Fit of ReasonFlux/ASFT to the six criteria

| Criterion | What judges need to see | Current evidence and gap |
|---|---|---|
| **Accuracy** | Actual score from the linked Kaggle submission ID. | No ID/score is present in the workspace. Local train/holdout or synthetic results must not be presented as a Kaggle score. |
| **Universality** | Evidence the method transfers beyond one narrow fixture or representation. | Synthetic controls and prior ARC experiments are informative, but current Phase 2I candidate generation has not run; broad transfer is not established. |
| **Progress** | A concrete increase in the field's ability to solve ARC or a reusable discovery that changes what others can do. | Candidate production is the strategic bottleneck, but the current Phase 2I objective is unfinished. No nonzero qualified invariant-candidate population is established here. |
| **Theory** | A causal/mechanistic account—why a method works or fails, tested against alternatives. | The project has useful decomposition and falsification discipline. It must connect that theory to a real submitted method and evidence, not just architecture or phase descriptions. |
| **Completeness** | Paper, exact public notebook, submission ID, results, ablations, costs, limitations, and reproducibility. | Engineering documentation is extensive, but the matching competition artifact and leaderboard receipt are not in the project records. |
| **Novelty** | A fair comparison with prior ARC work: program synthesis, test-time adaptation, recursive refinement, memory/retrieval, and synthetic-data methods. | “Invariant candidate production” could be a distinctive angle, but novelty and value remain hypotheses until the candidate-generation experiment runs and is compared fairly. |

## Recommendation for this project

### If a qualifying Kaggle submission already exists

1. Provide its **competition track, submission ID, public notebook URL/version, score, and team identity**. Confirm it was submitted under the team that will enter the Paper Track.
2. Audit whether the submitted notebook actually contains the ReasonFlux/ASFT method. The writeup must describe the submitted code, not a later unsubmitted design.
3. The owner confirms ARC-AGI-3. The current leading research direction is **“From Trace to Transfer: Counterexample-Guided Invariant Skills”**—learn a reusable skill from state/action/effect regularities, infer scope from counterexamples, and test held-out action-efficiency benefit against trace-replay/simple-recurrence controls. The full synthesis is in [`Project Idea V3`](arc_prize_2026_project_idea_v3.md), with claims and required evidence in [`Claim–Evidence Map V1`](arc_prize_2026_claim_evidence_map_v1.md). Recent literature covers skill induction, transfer, verification, lifecycle, and cost amortization, so the novelty wedge is provisional and needs a focused prior-art matrix. Current Phase 13B/13C/13G results are separate synthetic/ARC-AGI-2 studies; they motivate but cannot validate an AGI-3 result. The local AGI-3 validation plan has no runs/results, and Phase 2I remains unauthorized.
4. Show the exact pipeline, frozen thresholds, search budget, controls, failure/attrition states, public leaderboard score, and honest limitations. Include ablations only when supported by actual runs. Do not elevate synthetic HCC or training-task results into scientific ARC evidence.
5. Write to the Kaggle 1,500-word maximum. Map every section to the six rubric items; attach the required cover image/media and public notebook; submit the final writeup (not a draft) by the conservative Nov 8 UTC deadline. [S1][S2]

### If no qualifying Kaggle submission exists (current status)

The user says the ARC-AGI-3 team is joined and can make a late submission. Prepare only the exact interactive-agent notebook the team intends to submit; do **not** manufacture an ID, attach an unrelated notebook, or retrofit the paper to a method the notebook does not implement. Obtain an official ruling on whether a late, non-prize-eligible code-track submission satisfies the separate Paper Track linked-submission condition. If it does not, the 2026 paper may not qualify even if Kaggle accepts a late score. Continue the evidence-bounded research work regardless, and do not represent Paper Prize eligibility as settled.

For the next cycle: finish the independent WP3 gate; obtain run-specific authorization; execute the frozen outcome-blind Phase 2I pipeline; test whether a nonzero population is produced; compare it with relevant baselines; and only then decide whether the results support a competition submission and a paper claim. A positive yield is necessary, not sufficient. Any later Phase 3 readiness gates remain required.

## Paper strategy if eligibility is confirmed

Given the owner’s ARC-AGI-3 track choice, the current paper direction is a **controlled study of whether reusable skills cause useful cross-level transfer**, not “we solved ARC” or “we built AGI.” The concept is still being refined; before settling it, the team should establish:

- What is a skill versus a copied script or level-specific macro, and what evidence qualifies its preconditions?
- Does the linked agent make the skill available on a later level, activate it, change behavior because of it, and improve the action-efficiency objective?
- How will a matched no-skill or raw-replay baseline isolate the role of the skill, under equal action/time/model budgets?
- How will harmful/stale transfer, unused skills, no-support cases, and fallbacks be reported?
- How is this distinct from prior ARC-AGI-3 script-tracing/negative-transfer work and general causal skill-evaluation frameworks?
- What finding would falsify the claim that validated skill transfer improves later play?

Only state what a future linked notebook actually implements and what its authorized results support. Existing ASFT synthetic/ARC-AGI-2 evidence can motivate the question but cannot answer these AGI-3 questions. The current paper concept is a research direction, not a winning-level contribution claim.

## Immediate owner checklist (Nov 3)

- [ ] Build/submit the exact late ARC-AGI-3 interactive-agent notebook the user intends to use; capture the platform submission ID, score, notebook version, and team identity (no credentials in chat).
- [ ] Ask Kaggle/ARC Prize whether a late code submission can satisfy the Paper Track's linked-code requirement, and keep the answer/receipt.
- [ ] Confirm the Paper Track team matches the late code-submission team.
- [ ] Select only the method that the linked notebook actually runs.
- [ ] Decide whether current evidence supports any original claim; do not claim Phase 2I results before authorized execution.
- [ ] Target **Nov 8 UTC** for the final writeup because official deadline pages disagree.
- [ ] Check 1,500-word count, required cover image/media, public notebook accessibility, submission ID, license/open-source obligations, and final “Submit” status.

## Sources

- **[S1]** Kaggle, [ARC Prize 2026 — Paper Track](https://www.kaggle.com/competitions/arc-prize-2026-paper-track) — deadline, format, notebook/media requirements, rubric, tie rule.
- **[S2]** ARC Prize, [2026 Paper Prize](https://arcprize.org/competitions/2026/paper) — conceptual-progress goal, linked-code requirement, rubric, awards, paper contents.
- **[S3]** Kaggle, [ARC Prize 2026 — ARC-AGI-2](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2) — entry/final submission dates and notebook constraints.
- **[S4]** Kaggle, [ARC Prize 2026 — ARC-AGI-3](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3) — track distinction and entry/final submission dates.
- **[S5]** ARC Prize, [ARC Prize 2026 overview](https://arcprize.org/competitions/2026) — mission, open-source expectation, and Nov 8 paper date.
- **[S6]** Google, [Google Cloud Next ’17 announcements](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/100-announcements-google-cloud-next-17/) — Kaggle acquisition announcement.
- **[S7]** ARC Prize, [2025 Results and Analysis](https://arcprize.org/blog/arc-prize-2025-results-analysis) — participation, score results, paper winners, and prior-year field size.
- **[S8]** ARC Prize, [2025 Competition Details](https://arcprize.org/competitions/2025) and the TRM paper, [“Less is More”](https://arxiv.org/abs/2510.04871) — award list and winner’s method.
- **[S9]** Kaggle, [ARC Prize 2026 Paper Track Rules](https://www.kaggle.com/competitions/arc-prize-2026-paper-track/rules) — sponsor, team-match requirement, entry terms, and award/license rules.
