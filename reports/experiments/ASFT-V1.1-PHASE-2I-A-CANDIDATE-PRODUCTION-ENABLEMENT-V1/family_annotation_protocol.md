# WP3 — Independent Task-Family Annotation Protocol

## Status and boundary

WP3 is active. This protocol is intended to support independent, outcome-blind annotation of only the 600 previously exposed historical `discovery` IDs. It does not assign new confirmation/replication splits. No labels are yet accepted or frozen; the current label map remains unavailable until the independent coding and adjudication steps are complete.

Annotators receive only task IDs and training input/output demonstrations through the train-only packet builder. They must not receive test inputs/outputs, test-derived predictions, R1/R3 programs or traces, candidate yield, prior program-derived family labels, or future-value/outcome fields. The packet format contains only `task_id` and `train_pairs` plus blank annotation fields.

## Unit and coding principle

The unit is one ARC task. Assign one **primary semantic rule family** based on the transformation regularity supported by the task's training demonstrations. Do not use a solver's chosen operation or internal representation. The question is “what kind of task-level rule is evidenced by the examples?”, not “which registered program solved it?”

Annotators may add secondary descriptors, but only the adjudicated primary family is used for the ≥2-family candidate eligibility count. If demonstrations support multiple materially different explanations, record `UNKNOWN_AMBIGUOUS`; never force a family.

## Primary ontology (mutually exclusive coding)

| Code | Family | Positive coding rule | Do not use merely because… |
|---|---|---|---|
| `OBJ_RELATION` | Object selection/relational rule | The task rule selects or changes entities by a semantic property, rank, containment, adjacency, alignment, or relation among entities. | A solver internally parsed components. |
| `SPATIAL_CHANGE` | Spatial arrangement/orientation | The central regularity changes location, orientation, or geometric arrangement of existing content. | A local pixel difference happens to move. |
| `COLOR_ATTRIBUTE` | Color/attribute recoding | The central rule maps, replaces, or assigns color/visual attributes while spatial organization is secondary. | A solver used a recolor primitive. |
| `COUNT_REPLICATION` | Counting/repetition | Counts, multiplicity, periodic repetition, tiling, or number-dependent output structure determine the transformation. | Several objects are present. |
| `PATTERN_COMPLETION` | Pattern/symmetry completion | The output completes, extrapolates, or regularizes a repeated/symmetric visual pattern. | Any operation can be described as a pattern. |
| `REGION_TOPOLOGY` | Region/connectivity/topology | Enclosure, connectivity, separation, filling, boundaries, or region topology is the governing rule. | A parser has connected components. |
| `FRAME_BOUNDS` | Frame/extent/bounds | Crop, padding, canvas extent, border/frame, or bounding region is the central transformation. | Output dimensions happen to differ. |
| `SYMBOLIC_SEQUENCE` | Symbolic/arithmetic sequence | Numeric, ordinal, coordinate, sequence, or arithmetic structure determines the output. | Colors are represented numerically in code. |
| `COMPOSITE_RULE` | Irreducibly composite rule | Two or more mechanisms are jointly necessary and no primary mechanism is supported by the priority rules below. | A simple rule has multiple execution steps. |
| `UNKNOWN_AMBIGUOUS` | Insufficient/ambiguous evidence | Available demonstrations do not support one stable primary family, or multiple explanations remain observationally equivalent. | The task is simply difficult. |

### Primary-family decision rules

1. Identify the simplest task-level regularity that explains **all** provided training pairs; cite pair indices as evidence.
2. If one mechanism determines target selection and another is only the resulting action, code the selection/relational mechanism when selection is essential; otherwise code the action mechanism.
3. If a rule is driven by count/sequence/arithmetic, use `COUNT_REPLICATION` or `SYMBOLIC_SEQUENCE` even if the surface action is geometric/color change.
4. If the rule completes a systematic pattern or symmetry, use `PATTERN_COMPLETION` unless the examples clearly show a purely local geometric transformation without completion.
5. Use `COMPOSITE_RULE` only if removing either mechanism breaks the explanation and no primary mechanism dominates; record the required components as secondary tags.
6. Use `UNKNOWN_AMBIGUOUS` rather than infer hidden intent, access test data, or consult solver traces.

The rubric is representation-neutral and labels are not defined by the R1/R3 grammar. Annotators must provide a short rationale in their own words plus supporting training-pair indices. Rationale is retained for audit and is not exposed to the miner.

## Independent coding and adjudication

- Two qualified annotators independently code all 600 discovery tasks using separate copies of the same train-only packet. They cannot see one another's labels/rationales or any solver traces/programs/results.
- Record primary family, optional secondary tags, confidence (`HIGH/MEDIUM/LOW`), evidence pair indices, rationale, and `UNKNOWN_AMBIGUOUS` flag.
- Compute pre-adjudication exact agreement and Cohen's κ for the primary nominal label; report the full confusion matrix and missing/ambiguous rates. If κ < 0.70, pause, clarify the rubric without seeing candidate yield, and have both annotators recode the affected/full set under a new rubric version.
- A third adjudicator resolves disagreements from training demonstrations and the rubric only. Preserve both original labels, adjudication decision, and reason. No majority/vote is silently substituted for adjudication.
- Freeze the adjudicated task→primary-family map and annotation/rubric hashes before candidate generation. Keep unknowns explicit; candidates with fewer than two supported families cannot pass the family gate.

## Annotation-input integrity

The packet builder reads the Phase 13G split manifest only for task IDs assigned to `discovery`; it excludes transfer/holdout IDs and does not copy pair counts, test metadata, or paths into annotation rows. The task JSON loader decodes the top-level `train` array only and fails closed if the file layout does not place that field before any `test` field. It does not decode test inputs, test outputs, or hidden evaluation fields. Generated packets are scanned for forbidden field names and sentinel values before release.

## Current blocker

A genuinely independent second annotator and adjudicator have not been supplied or authorized in this workspace. One AI assistant cannot truthfully self-certify two independent blind annotations. A separate 12-task AI pilot exists at `wp3_ai_pilot_v1/`; it is explicitly non-qualifying protocol-development material and does not change this requirement. Until two independent human label streams and a separate adjudication exist, the family map remains blank and the ≥2-family eligibility endpoint unavailable; do not use pilot labels as a substitute.

## Provisional full-packet pass

`wp3_provisional_v1/` contains a complete first pass over all 600 discovery tasks, produced by three deterministic AI policies behind the same train-only boundary:

- Agent A: mechanism-first scoring over structural features.
- Agent B: counter-hypothesis pass with the rubric's priority tiers.
- Agent C: adjudication of A/B disagreements only.

Every record is tagged `AI_PROVISIONAL`. The bundle reports descriptive agreement (476/600 exact, Cohen's κ ≈ 0.72) and a 37.7% `UNKNOWN_AMBIGUOUS` rate. Those figures describe agreement between two rule policies, not between human readers, and cannot satisfy any WP3 gate condition. The bundle exists to give human reviewers a finished draft and a prioritised disagreement list. See `wp3_provisional_v1/wp3_completion_review.md` and `wp3_provisional_v1/provisional_manifest.json`.

