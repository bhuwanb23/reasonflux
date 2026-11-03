# Research Contribution Concept — ARC Prize 2026 Paper Track

**Status:** superseded as the lead idea by [`Project Idea V3 — From Trace to Transfer`](arc_prize_2026_project_idea_v3.md). Retain this file as an earlier candidate-support/skill-transfer evidence map; not a submitted Kaggle writeup, experiment, or claim of contest eligibility.  
**Project basis:** saved ASFT v0.1 Phases 13B–13G and audits 14H–14J, plus the Phase 2I-A engineering package. The owner confirms the intended competition track is **ARC-AGI-3**, the team joined that track, and a late submission can be made.  
**Track alignment warning:** most cited empirical evidence below is synthetic or ARC-AGI-2, not ARC-AGI-3. It can motivate an audit question but cannot stand in for results from the linked interactive agent. The exact AGI-3 submission code, ID, and score are not yet in this workspace.  
**Paper deadline risk:** Kaggle’s Paper Track page says Nov 9, 23:59 UTC; ARC Prize’s overview says Nov 8. Plan to the earlier Nov 8 UTC date unless the sponsor resolves this. A late ARC-AGI code submission may be technically accepted for scoring, but ordinary code-track rules state late submissions are not prize-eligible; the Paper Track’s treatment of a late-linked code submission needs sponsor confirmation.

## 1. The candidate idea

### Working title

**Does a Skill Actually Transfer? A Support-Conditioned Causal Test for Interactive ARC Agents**

### One-sentence thesis

> A skill call or high aggregate score does not by itself establish useful transfer. For an interactive ARC agent, audit four distinct links—**availability → activation → behavioral influence → task utility**—and test causal influence by comparing a skill-enabled policy with a matched no-skill condition on the same permitted starting state and budget.

This is a **working research hypothesis and paper direction**, not a novelty claim. The broad ideas of measuring candidate support, skill use, behavior change, and skill utility already have precedents. The potential contribution is a rigorous, opportunity-conditioned causal evaluation of **cross-level skill transfer in interactive ARC**, distinguishing “not available,” “available but unused,” “used but behaviorally inert,” “behavior changed but not useful,” and “positive or negative utility.” The current saved record does not establish that novelty or any AGI-3 result.

## 2. Why this could be useful to ARC researchers

ARC-AGI-3 adds a continual, stateful question: when a procedure learned on one level is available later, does the agent retrieve it, does it actually change the action, and does that change help under the action-efficiency objective? Prior ARC work already separates proposal/search from selection; recent skill-evaluation work also measures behavior change and skill utility. Neither generic stage separation nor “skills can change behavior” is a novelty claim. The candidate contribution is a **cross-level causal-transfer audit** that makes opportunity, activation, behavioral influence, and signed utility separate, with matched no-skill counterfactuals. A low final score—or a frequent skill-call count—alone cannot tell a researcher whether the failure came from:

1. **No support:** no eligible skill exists for the current state/task, so the skill mechanism was not tested.
2. **No uptake:** a skill exists but the agent does not invoke it; this is a retrieval/selection failure, not evidence the skill itself is bad.
3. **No behavioral effect:** the skill is invoked but does not change the chosen action or policy relative to the matched no-skill condition.
4. **Behavior without utility:** the skill changes behavior but does not improve, or harms, task progress/action efficiency.
5. **Useful transfer:** an available skill changes behavior and improves a predeclared objective on a later level, under a matched budget.

The practical artifact would be a **skill-transfer evidence ledger**: per-level/decision support counts, skill identity/version and precondition match, activation, matched behavioral delta, outcome, cost, and failure/rollback. Do not collapse these links into one “skill reuse” or score number. This extends the existing AGI-3 design draft’s per-step logging and skill fields, but remains a proposed study, not evidence.

### Proposed reporting quantities

Keep the static-program and interactive-agent ledgers distinct; do not pool them. For the legacy static-program studies, preserve their existing task/candidate funnel. For the target ARC-AGI-3 agent, the proposed skill-transfer chain is:

`level/state → eligible skill set + precondition match → skill available → skill activated → action/policy change vs matched no-skill → environment progress/action cost → transfer label`

Report at each link: numerator and denominator; decision/episode unit; skill/version and evidence lineage; support count; precondition confidence; activation rate conditional on availability; matched action/policy divergence; score/progress and action efficiency; wall-time/token cost; and negative-transfer/fallback events. Report unconditional treatment effect over the full assigned cohort as primary; conditional-on-activation analyses are descriptive because activation is post-treatment and can be selected by the agent.

Use explicit denominators and stage-specific missingness codes. A score tie with no skill activations is not evidence that the skill itself is ineffective; an activation count without an outcome counterfactual is not evidence that the skill helped.

### Evaluation logic to test

Let `Z` assign a matched game/episode to the skill-enabled or no-skill policy, and `Y` be the predeclared outcome (official score/action efficiency, with cost reported separately). The primary effect is the intention-to-treat difference in `Y` across matched assignments. Skill availability, precondition match, activation, and action divergence are mechanism diagnostics—not substitutes for the primary outcome. Because activation is post-assignment, do not call a comparison conditioned on “skill was used” causal unless a valid same-state intervention/replay is available. If the environment cannot reproduce/fork a decision state, report local action divergence descriptively and keep the causal claim at the full matched-episode level. The expected result may be “not evaluable due to no support/uptake,” not “skill transfer disproven.”

## 3. Prior-art boundary and what the project can support

A first-pass literature scan found substantial overlap with the broad ideas. **[“Tracing the Thoughts of a Coding Agent Playing ARC-AGI-3”](https://arxiv.org/html/2610.11450v1)** follows scripts and notes across levels, reports rare cross-level script reuse, abandonment, and stale-memory negative transfer. **[“Skill Use or Skill Theater?”](https://arxiv.org/html/2607.27484)** proposes matched no-skill counterfactuals to measure whether a skill causally changes decisions and whether it helps or harms; **[“A Framework for Evaluating Agentic Skills at Scale”](https://arxiv.org/html/2606.17819)** measures skill availability, behavior change, and utility in controlled tasks. In ARC-AGI-3, **[arc-skill](https://arc-skill.vercel.app/)** requires falsifiable action predictions and compares against public score context. So neither skill reuse logging, skill ablation, nor prediction-before-action is a safe novelty claim.

A provisional gap worth testing in a deeper review: a single **cross-level, action-budgeted transfer protocol** that links precondition-qualified skill support, actual uptake, matched behavioral influence, and signed score/action-efficiency impact, while explicitly treating stale-skill negative transfer. The saved ASFT work has a potentially relevant skill/invariant provenance and support vocabulary, but it has no AGI-3 results. This is only a candidate differentiation; a systematic prior-art review must establish whether the combination is genuinely missing, and an authorized AGI-3 experiment must demonstrate its value before any novelty claim.

The strongest existing evidence is a carefully bounded pattern across separate studies—not a pooled causal result:

- **Phase 13B:** transfer-aware, frequency-only, and no-transfer rankers tied on the corrected primary top-k endpoint. The audit describes low ranking discrimination in that pool; it does not show that ranking never matters.
- **Phase 13C:** 44 eligible synthetic candidate rows were all selected; SCT, always-create, and random-create tied on the primary net-value endpoint. The random policy’s creation probability degenerated to 1.0. Memory-only was stronger on that endpoint, with unequal opportunity counts, so it is a serious but not universally proven alternative.
- **Phase 13G:** the bounded symbolic adapter exactly fit 3/600 discovery, 5/200 transfer, and 2/200 holdout tasks under a ten-program scan; it produced zero invariant candidates, skills, and capabilities. These are public-training split/program-fit diagnostics, not official ARC leaderboard accuracy. A frozen-config/code budget mismatch and repeated-holdout exposure are disclosed, so this is a bounded implementation diagnosis, not a general ARC/theory verdict.
- **Phase 13 synthetic mechanisms:** recurring operation-level patterns, reflection/rotation skill construction, some reuse, and simulator reasoning-step proxy reductions are observed narrowly inside controlled generators.
- **Phase 14 synthesis:** the evidence does not validate the full `Experience → Invariant → Skill → Transfer → Capability → Intelligence` chain. Transfer-to-capability is the first major unestablished causal bridge; intelligence construct validity is absent.
- **Current Phase 2I-A:** the fail-closed runner and synthetic tests are engineering evidence. WP3 remains incomplete, the candidate-production run is unauthorized, and no nonzero qualified invariant population has been established. Do not present the Phase 2I run as a result.

The Phase 13/14 source of truth is [`PHASE-14J Final Scientific Conclusions`](../experiments/PHASE-14J-FINAL-SCIENTIFIC-CONCLUSIONS-V1/phase14j_final_scientific_conclusions.md) and the [`13H Master Evidence Package`](../experiments/PHASE-13H-EVIDENCE-CONSOLIDATION-V1/master_evidence_package.md). The WP3/Phase 2I constraints are summarized in [`WP0–WP6`](../experiments/ASFT-V1.1-PHASE-2I-A-CANDIDATE-PRODUCTION-ENABLEMENT-V1/wp0_wp6_end_to_end_summary.md).

## 4. How to turn the idea into a useful contribution

### Minimum artifact that other researchers can use

1. A small, documented **skill-transfer ledger** with fields for skill ID/version, source evidence, preconditions, applicability decision, activation, predicted effect, observed effect, fallback/rollback, and outcome/cost.
2. An audit report that distinguishes `NO_SUPPORT`, `NOT_ACTIVATED`, `NO_ACTION_CHANGE`, `ACTION_CHANGE_NO_GAIN`, `POSITIVE_TRANSFER`, and `NEGATIVE_TRANSFER`; never count “skill mentioned” or “skill called” as proof of useful transfer.
3. A paired comparison protocol that controls the game/level start state, model, harness, and action/time budget, with intention-to-treat outcome as the primary comparison.
4. A replay/reproducibility tool that checks the saved interaction log and links every transferred skill to its originating evidence and later use.
5. The exact ARC-AGI-3 notebook/entry and score receipt once the submission is built; the paper must describe that same agent, not the earlier ARC-AGI-2 pipeline.

### Future experiment sketch — not authorized to run now

- Compare `NO_SKILL`, `RAW_REPLAY` (reuse prior successful code/sequence without a robust precondition gate), and `VERIFIED_SKILL` (explicit preconditions plus predicted-effect check and fallback). Add a placebo/shuffled-skill condition only if a clean, budget-matched protocol is feasible.
- Freeze model, prompt, harness, memory policy, game/level seeds, action budget, primary outcome, and analysis before any run; use only permitted public/development material and the official evaluator. Do not inspect hidden outcomes.
- Primary outcome: intention-to-treat difference on official score/action efficiency and level progress over the full assigned game/episode cohort. Secondary diagnostics: support rate, activation conditional on support, action divergence, precondition violations, recovery/fallback, negative transfer, and compute/tokens.
- Use exact same-state replay for local causal influence only if the environment officially permits deterministic reset/replay. Otherwise keep per-step action differences descriptive and make causal claims only at the matched episode level.
- Log every skill’s preconditions, expected state transition, termination, evidence count, provenance, cost, and failure behavior. Do not label a one-off macro as transferable without a predeclared validation rule.
- Preserve all failures and zero-support/zero-uptake cases; no threshold tuning after yield/outcome. Run only after the relevant research gates and explicit authorization are satisfied; this sketch does not authorize Phase 2I, Phase 3B, Phase 3D, or access to confirmatory outcomes.

## 5. Rubric mapping

| Paper criterion | Evidence this concept must provide |
|---|---|
| **Accuracy** | A real late/eligible Kaggle ARC-AGI-3 submission ID, notebook version, and official score from the linked interactive agent. The Paper Track uses the linked score; confirm whether a late code submission is acceptable to the paper judges. |
| **Universality** | Show the audit applies across a known synthetic generator and the ARC submission, without claiming all ARC systems are covered. |
| **Progress** | Show that the protocol separates inert, unused, useful, and harmful skill transfer, and that verified preconditions/fallback improve the action-efficiency tradeoff over raw replay. The concept alone is not progress evidence. |
| **Theory** | Explain the hypothesized chain from learned evidence to precondition match, activation, changed action, and task utility; distinguish causal effects from descriptive mechanism logs. |
| **Completeness** | Publish the exact notebook, ledger schema, budgets, all attrition, ablations, limits, and the matching score receipt. |
| **Novelty** | Differentiate from ARC-AGI-3 script-tracing/negative-transfer studies and general causal skill-ablation frameworks; show the specific cross-level, action-budgeted, precondition-qualified protocol adds something useful. Novelty remains unverified. |

This concept could improve **Theory, Completeness, and possibly Progress**. Without a valid linked score and a genuinely useful intervention, Accuracy and Progress are weak, making a top-three result uncertain. A win cannot be promised.

## 6. Paper outline within the 1,500-word limit

1. **Title + abstract (100–130 words):** distinguish observed skill reuse from causal, useful cross-level transfer; no AGI claim.
2. **Motivation / prior work (180–220):** connect ARC-AGI-3 skill traces, negative transfer, and causal skill evaluation; state the narrow unresolved gap.
3. **Method (300–350):** skill-transfer ledger, matched conditions, causal estimand, action budget, and exact submitted agent.
4. **Results (350–420):** actual ARC-AGI-3 linked-agent score and only authorized, directly relevant results. Label prior synthetic and ARC-AGI-2 findings as background; do not imply they validate the AGI-3 agent.
5. **Why it matters (180–220):** how another team can use the audit to diagnose wasted search/ranking effort.
6. **Limitations (150–200):** bounded DSL, config mismatch, zero candidate population, separate phases, no full theory validation, and late-submission eligibility uncertainty.
7. **Reproducibility / conclusion (100–150):** exact notebook, commit, entry ID, license, and concise take-away.

The Kaggle writeup maximum is 1,500 words; this research concept is not itself the final writeup.

## 7. Immediate gates and action

1. **Late-entry eligibility:** owner confirms the intended track is ARC-AGI-3, the team joined that track, and the late-submission route is available. The ARC-AGI-3 rules require registration before the code track’s Entry Deadline; the user’s report addresses this at a high level, but the Kaggle account should still be checked and an actual late submission ID/score captured. Code-track rules say late submissions are not prize-eligible for that code competition. Separately, Paper Track rules say its team must match a team making an ARC-AGI-2/3 submission, and ARC Prize says the linked code submission need not score highly; neither text explicitly says the linked code submission must itself be on-time/prize-eligible. Thus late linkage looks plausible but is not guaranteed. Confirm whether the sponsor accepts a late, non-code-prize-eligible ARC-AGI-3 submission for Paper Prize Accuracy/eligibility; retain written confirmation plus the generated ID/score.
   **Sponsor query to send:** “Our team is registered in ARC-AGI-3 and matches our intended Paper Track team, but we did not make a final code submission by the ARC-AGI-3 deadline. Kaggle currently allows us to make a late submission and generate an ID/score. Would that late, non-code-prize-eligible ARC-AGI-3 submission satisfy the Paper Track’s linked-code-submission requirement, and can its score be used for the Paper Track Accuracy criterion?”
2. **Track fit:** owner confirms ARC-AGI-3. Build the paper around the exact interactive agent submitted to that track. The existing `validation/experiments/agi3/README.md` is a design draft with no runs/results; it is a planning reference, not evidence. The cross-level skill-transfer idea remains a proposed study, not an AGI-3 finding.
3. **Code alignment:** when submission work begins, select the exact agent and ensure the paper describes only what that notebook implements. Do not retrofit the paper to a design the submitted code does not contain.
4. **Research boundary:** continue paper analysis from saved Phase 13/14 records; do not run Phase 2I, inspect hidden outputs, or use WP3 AI-provisional labels as human evidence without separate authorization and valid human review records.
5. **Owner-supplied facts:** provide the Kaggle account’s existing entry status (whether rules were accepted before Oct 26), track, team name/ID, and resulting late submission ID/score. Never send credentials. Confirm the paper team matches the code-submission team.
6. **Submit paper early:** target Nov 8 UTC due to the official Kaggle/ARC deadline discrepancy; submit the final writeup, public notebook link, and required cover/media, not a draft.

## Decision

The clearest research direction to investigate next is **“Does a skill actually transfer?”**—separating skill availability, activation, behavioral influence, and signed utility across ARC-AGI-3 levels, with matched no-skill comparisons and action-efficiency outcomes. This is more specific and useful than the initial generic candidate-coverage idea, but it overlaps with existing skill-causal and ARC-AGI-3 memory research; novelty is unverified. The saved synthetic/ARC-AGI-2 results only motivate the question and do not establish an AGI-3 finding. Per the user’s direction, the next step is to refine the question, prior-art boundary, and protocol first; submission/code work can follow once the idea is clear.
