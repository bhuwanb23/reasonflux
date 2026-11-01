# Metric Dictionary — Draft to Freeze Per Track

**Status:** Core concepts are defined below, but track-specific evaluators, aggregations, budgets, minimum useful effect, and exclusions remain `REQUIRED_BEFORE_RUN`. This file deliberately does **not** endorse the inconsistent products in the older Phase 3/7/8/11 docs as validated measures.

## 1. Primary score

Use the competition's evaluator for the selected track and version. Save the per-task/game outputs and the exact evaluator commit. The solver may not access hidden ground-truth labels. For controlled research on labeled public data, run the evaluator offline after predictions have been frozen.

- ARC-AGI-2: per-task outcome from the current official scoring implementation; archive the evaluator and confirm how multiple test outputs/attempts are aggregated.
- ARC-AGI-3: per-game/episode outcome from the current official evaluator; archive the exact version and game's scoring fields.

Do not mix task score percentages, model confidence, and agent reward into one number.

## 2. H1 primary effect (select one primary endpoint per track)

For task/game `i`, let `Y_i(ASFT)` and `Y_i(control)` be the same track-native outcome for paired variants on the same held-out ID, same seed where possible, and matched budget.

`Delta_Y = mean_i[Y_i(ASFT) - Y_i(control)]`

or, if efficiency is preselected as primary, define cost `C_i` and report:

`Delta_C = mean_i[C_i(control) - C_i(ASFT)]`

Positive values favor ASFT in either expression. Declare whether un-solved/failed tasks receive zero score, a capped cost, or another official value. Preserve per-ID differences; estimate a paired task/game bootstrap interval with the resampling procedure frozen in `PROTOCOL.md`.

**Transfer attribution:** only call the difference transfer if the ASFT variant receives source-task experience that controls do not receive in skill form, and all variants get matched compute/exposure. Specify sources and held-out target IDs. Otherwise call it a general solver/agent effect, not transfer.

## 3. H2 trigger value (avoid a made-up SCV product)

Do not compute `Reuse × AbstractionGain × Transfer − Cost` from unscaled or future-observed terms. Before a trigger may run, define an estimator based solely on information available at decision time:

- what training/validation observations estimate expected reuse;
- how performance/efficiency benefit and uncertainty are estimated;
- how skill creation, storage, retrieval, and failure costs are measured in the same unit (e.g. compute seconds or a preregistered utility tradeoff);
- how confidence/uncertainty affects promotion;
- what to do if evidence is missing or conflicting.

Primary H2 comparison is the **measured held-out outcome** across never-store, always-store, and SCT. Report all candidate skills and all costs. The trigger's internal predicted value is a diagnostic, not evidence of realized benefit by itself.

## 4. H3 growth measure

Use a fixed probe suite with identical scoring and budgets at each predefined checkpoint. For checkpoint `k`:

`ProbeScore_k = mean track-native score on the fixed probe IDs at checkpoint k`

`G_k = ProbeScore_k - ProbeScore_(k-1)`

Report wall-clock/compute cost, number of source experiences, and task composition separately. Do not replace the difference with an arbitrary weighted skill count. Predict a later held-out checkpoint from early `G_k` and compare with a baseline predictor using the current probe score alone; reserve independent sequences/seeds for the final predictive test.

## 5. Supporting outcomes (report separately)

- **Skill reuse rate:** fraction of promoted skills invoked at least once on held-out evaluation. Define denominator and invocation eligibility.
- **Skill success rate:** successful invocations divided by all invocations; define success from environment/task outcome, not model self-report.
- **Negative-transfer rate:** fraction of eligible target IDs where offering/invoking a skill worsens the preregistered outcome versus matched no-skill control. Record severity as a separate paired delta.
- **Creation/maintenance cost:** compute/time/memory required to discover, validate, store, retrieve, and maintain candidates; capture both amortized and one-time cost.
- **Coverage:** only use a fixed, documented universe of task/game families and a predeclared criterion for “covered.” Otherwise do not report a coverage percentage.
- **Invariant precision/recall:** only if independent labels exist, produced without access to evaluation outputs; specify annotation provenance and inter-rater reliability if human labeled.

## 6. Statistical fields required before confirmatory run

`primary_endpoint`, `aggregation`, `delta_min`, `regression_margin`, `task/game IDs`, `seeds`, `number of sequences`, `CI method`, `resampling unit`, `exclusion rules`, and `multiplicity treatment` must all be in the frozen track protocol. If missing, mark output `PILOT`, not confirmatory.
