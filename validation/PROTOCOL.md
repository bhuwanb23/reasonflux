# Global Validation Protocol

**Protocol version:** 0.1-draft  
**State:** `DRAFT — MUST BE REVIEWED AND FROZEN BEFORE CONFIRMATORY RUNS`  
**Protocol owner:** REQUIRED_BEFORE_RUN  
**Reviewers:** REQUIRED_BEFORE_RUN  
**Frozen date / git commit / SHA-256:** REQUIRED_BEFORE_RUN

## 1. Objective and scope

Test three separate claims in two separate competition settings. ARC-AGI-2 and ARC-AGI-3 use different input/output contracts and primary evaluators; report them separately. Shared code may cover trace/event storage, candidate-skill records, and the trigger, but do not combine scores across tracks into one unvalidated “intelligence” number.

## 2. Roles and responsibilities

| Role | Named owner | Responsibility |
|---|---|---|
| ARC-AGI-2 implementation | REQUIRED_BEFORE_RUN | Static grid solver adapter, baseline, Kaggle notebook |
| ARC-AGI-3 implementation | REQUIRED_BEFORE_RUN | Interactive agent adapter, baseline, Kaggle notebook |
| Evaluation/data | REQUIRED_BEFORE_RUN | Splits, scorer, budgets, leakage review, run completeness |
| Research protocol | REQUIRED_BEFORE_RUN | Freeze hypotheses/metrics; approve deviations |
| Paper/reproducibility | REQUIRED_BEFORE_RUN | Claim-evidence mapping, citations, reproduction instructions |

A person may hold multiple roles, but identify a reviewer who did not implement the relevant analysis.

## 3. Required controls

Every hypothesis comparison must, as applicable, hold fixed:

- task/game IDs, source experience, task order or randomized schedule, and train/validation/test split;
- solver/agent, model weights, prompting, decoding/search settings, tool access, memory allowance, and initialization;
- per-task time, token, GPU/CPU, action, or search-node budget;
- evaluator version and output schema;
- number and identity of random seeds.

Record any unavoidable difference. If compute cannot be matched exactly, report both quality and cost and state the confound. Compare paired task/game outcomes whenever possible.

## 4. Dataset partition and leakage safeguards

- Record exact file paths (or upstream dataset IDs), versions, dates, task IDs, and SHA-256 hashes in the data manifest.
- Partition by task family / generating rule / composition where this is known—not merely by random examples from the same template. Document how family labels were obtained.
- Use training data for model/library construction; validation data for design and threshold selection; held-out test data only once for confirmatory evaluation.
- Do not use Kaggle hidden-test labels, private leaderboard feedback, or results from the held-out set to tune prompts, DSL operators, thresholds, stopping criteria, or metric weights.
- For ARC-2, test task-specific program consistency only on that task's demonstrations; do not leak query answers into candidate generation or ranking.
- For ARC-3, define episode boundaries, what state/memory persists across games, and whether resets are part of the official contract. Do not assume cross-game feedback is available.
- Keep a written audit of manual labeling, hand-coded rules, and any model/checkpoint pretraining data. Disclose known overlap or unknown provenance.

## 5. Baselines and variants

At minimum run the same base system under:

1. `B0_NO_LEARNED_SKILLS`: baseline solver/agent with no learned skill library.
2. `B1_STATIC_OR_SIMPLE_LIBRARY`: non-ASFT control, such as a fixed library or frequency-based candidate policy; define exactly what qualifies before running.
3. `V1_IDT_ONLY`: invariant discovery enabled, but no SCT promotion gate; all eligible candidates are handled using the preregistered simple policy.
4. `V2_IDT_SCT`: invariant discovery plus the preregistered SCT trigger.
5. `V3_IDT_SCT_CGM`: CGM is logged/evaluated; it must not alter decisions in the primary CGM validation unless an additional intervention is explicitly preregistered.

For H2, directly compare never-store, always-store, and SCT-triggered policy. If a component cannot be implemented in a track, mark it `NOT_APPLICABLE` with reason; do not silently substitute a different treatment.

## 6. Metrics and analysis

- **Competition performance:** use the official/current track evaluator and record its version. ARC-2 uses the competition's task/output scoring; ARC-3 uses the official environment/scoring. Never replace these with an in-house score without labeling it secondary.
- **Efficiency:** preselect the primary resource measure for each track (wall-clock, model tokens, GPU seconds, search nodes, actions, or another logged budget). Record the full budget and observed use.
- **Transfer:** compare the same held-out targets after source-task experience against a control receiving matched compute and exposure but not the learned skill/invariant. Specify source/target families and order before running.
- **Skill utility:** report performance change and resource-cost change separately. Do not multiply unnormalized quantities or call a custom product a validated utility measure.
- **Uncertainty:** primary comparison is paired by task/game. Preselect a confidence interval method and resampling unit. Recommended default for task-level data: paired bootstrap over task/game IDs, 10,000 resamples, fixed seed, with the number of IDs stated. If there are repeated random seeds, report seed-level variability separately; do not treat correlated tasks as independent seeds.
- **Multiplicity:** designate H1 and H2 as confirmatory only if there is enough held-out data and the team can freeze all decisions. H3 is exploratory by default. If several confirmatory outcomes are tested, preselect a family-wise correction (e.g. Holm) and report adjusted results.
- **Practical relevance:** set a minimum meaningful effect `delta_min` and a tolerable regression bound `regression_margin` before the run. Do not set these after seeing results.

All track-specific primary metrics, aggregation, `delta_min`, guardrails, exclusions, sample sizes, and seeds are `REQUIRED_BEFORE_RUN` in the track plan.

## 7. Run completeness / acceptance checklist

A run is eligible for confirmatory analysis only if all are present:

- frozen protocol version and code commit/hash;
- complete data manifest and split IDs/hash;
- environment and hardware manifest;
- configuration and all seeds;
- all attempted task/game IDs, including failures/timeouts;
- native output artifact and evaluator output;
- trace, candidate, skill-create/reject/reuse/retire events (for ASFT variants);
- stdout/stderr and run status;
- analysis script, raw per-task metrics, summary table, uncertainty interval;
- deviations and exclusion log, even if empty.

Missing artifacts make a run `PILOT` or `FAILED_RUN`, never silently `CONFIRMATORY`.

## 8. Decision rules

- Support a claim only if its preregistered primary effect clears both the statistical rule and minimum practical effect, while staying within the declared regression guardrail.
- If results are noisy, underpowered, or lack a valid baseline, label them `INCONCLUSIVE`—not “validated.”
- Negative/null findings must remain in the results index and be considered for the paper.
- Any post-hoc change gets a new protocol version and new run IDs; prior data remain archived.

## 9. Competition versus research validation

Kaggle entry requirements (offline execution, runtime, schema, team association, license, model/data constraints) must be checked against the live rules for each track. Competition score is an important outcome but does not by itself establish a causal effect of IDT/SCT/CGM. The paper must describe the method present in the linked submission, and must distinguish competition results from controlled research evaluation.
