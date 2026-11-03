# WP3-AI-PILOT — Exploratory Only

**Not Independent Annotation**  
**Not Eligible For Family Qualification**  
**Not Eligible For Candidate Eligibility**  
**Not Eligible For Phase 2I Execution**  
**Not Eligible For WP3 Completion**

## Scope

Descriptive comparison of two rubric-conditioned passes from the same AI assistant on a deterministic 12-task sample of train-only discovery packets. These numbers are prompt-sensitivity diagnostics, not inter-annotator reliability and not population estimates.

## Agreement

- Exact primary-family matches: **4/12 (33.3%)**.
- Descriptive Cohen's κ: **0.232**.
- Pass A / Pass B label marginals differ substantially; `UNKNOWN_AMBIGUOUS` was used in the adjudication output for **4/12 (33.3%)** tasks.
- The small sample was hash-selected, not stratified; all task IDs belong to the existing discovery-only packet.

### Confusion matrix

Rows are AI Pass A; columns are AI Pass B. Categories are ordered: `COLOR_ATTRIBUTE`, `COMPOSITE_RULE`, `COUNT_REPLICATION`, `FRAME_BOUNDS`, `OBJ_RELATION`, `PATTERN_COMPLETION`, `REGION_TOPOLOGY`, `SPATIAL_CHANGE`.

| Pass A \ Pass B | COLOR_ATTRIBUTE | COMPOSITE_RULE | COUNT_REPLICATION | FRAME_BOUNDS | OBJ_RELATION | PATTERN_COMPLETION | REGION_TOPOLOGY | SPATIAL_CHANGE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| COLOR_ATTRIBUTE | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| COMPOSITE_RULE | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| COUNT_REPLICATION | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| FRAME_BOUNDS | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| OBJ_RELATION | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| PATTERN_COMPLETION | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| REGION_TOPOLOGY | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| SPATIAL_CHANGE | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 2 |

### Calculation

Observed agreement is 4/12 = 0.333. Chance agreement from the two pass marginals is 19/144 = 0.132. Thus κ = (0.333 − 0.132) / (1 − 0.132) ≈ **0.232**.

## Rubric stress-test findings

1. **Crop versus target selection:** Tasks `aab50785` and `ff805c23` expose uncertainty about whether the semantic selection mechanism or the visible crop/extent should be primary. Clarify the rubric's selection-versus-action priority with examples.
2. **Region topology versus color attribute:** Task `e9c9d9a1` was read as either region filling or palette assignment. Add a decision test: if boundaries/dividers determine which cells are changed, region topology is primary; otherwise consider color/attribute recoding.
3. **Pattern completion versus spatial/count rules:** Tasks `7447852a`, `b74ca5d1`, and `1b59e163` trigger different interpretations of repeated structure. Clarify when repetition is a driver (`COUNT_REPLICATION`) versus a visual regularity being completed (`PATTERN_COMPLETION`) versus movement of existing content (`SPATIAL_CHANGE`).
4. **Composite versus insufficient evidence:** Task `e9bb6954` shows that multiple visible changes do not alone justify `COMPOSITE_RULE`. Specify when the mechanisms are demonstrably jointly necessary and when to use `UNKNOWN_AMBIGUOUS` instead.
5. **Use of `UNKNOWN_AMBIGUOUS`:** Four of twelve adjudicated pilot cases remained unknown. This is not a projected rate for the full packet, but it suggests annotators need clearer examples of observational equivalence and unresolved primary mechanisms.

## Interpretation boundary

Do not use κ, confusion counts, or adjudicated pilot labels as WP3 agreement evidence. Do not freeze them, assign independent-family breadth, or pass them to the Phase 2I runner. WP3 remains incomplete until two genuine independent coding streams and a separate adjudicator are supplied.
