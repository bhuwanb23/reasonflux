# AI_PROVISIONAL — NOT HUMAN ANNOTATION — NOT WP3-ELIGIBLE

**Not Independent Human Annotation**  
**Not Eligible For Family Qualification**  
**Not Eligible For Candidate Eligibility**  
**Not Eligible For Phase 2I Execution**  
**Not Eligible For WP3 Completion**  

## Scope

Descriptive comparison of two deterministic, rubric-conditioned AI policies over all 600 discovery tasks. These are prompt-sensitivity diagnostics for a rule-based classifier, not human inter-annotator reliability and not estimates of annotation quality on unseen tasks.

## Agreement

- Tasks compared: **600**
- Exact primary-family matches: **476/600**
- Observed agreement: **0.7933**
- Chance agreement: **0.2629**
- Cohen's kappa (descriptive): **0.7196**
- Kappa band: **acceptable at the WP3 threshold**
- Disagreements: **124**
- `UNKNOWN_AMBIGUOUS` in pass A: **226** (37.7%)
- `UNKNOWN_AMBIGUOUS` in pass B: **264** (44.0%)
- Missing labels: **A=0, B=0**

### Confusion matrix

Rows are pass A; columns are pass B.

| A \ B | OBJ_RELATION | SPATIAL_CHANGE | COLOR_ATTRIBUTE | COUNT_REPLICATION | PATTERN_COMPLETION | REGION_TOPOLOGY | FRAME_BOUNDS | SYMBOLIC_SEQUENCE | UNKNOWN_AMBIGUOUS |
|---|---|---|---|---|---|---|---|---|---|
| OBJ_RELATION | 6 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 16 |
| SPATIAL_CHANGE | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| COLOR_ATTRIBUTE | 0 | 0 | 125 | 1 | 4 | 58 | 0 | 0 | 8 |
| COUNT_REPLICATION | 0 | 0 | 0 | 24 | 0 | 0 | 0 | 0 | 11 |
| PATTERN_COMPLETION | 0 | 0 | 0 | 0 | 16 | 0 | 0 | 0 | 1 |
| REGION_TOPOLOGY | 0 | 0 | 0 | 1 | 0 | 62 | 0 | 0 | 3 |
| FRAME_BOUNDS | 0 | 0 | 0 | 0 | 2 | 5 | 13 | 2 | 2 |
| SYMBOLIC_SEQUENCE | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 1 |
| UNKNOWN_AMBIGUOUS | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 221 |

### Marginals

| Family | Pass A | Pass B |
|---|---:|---:|
| OBJ_RELATION | 25 | 6 |
| SPATIAL_CHANGE | 8 | 7 |
| COLOR_ATTRIBUTE | 196 | 125 |
| COUNT_REPLICATION | 35 | 26 |
| PATTERN_COMPLETION | 17 | 22 |
| REGION_TOPOLOGY | 66 | 130 |
| FRAME_BOUNDS | 24 | 16 |
| SYMBOLIC_SEQUENCE | 3 | 4 |
| UNKNOWN_AMBIGUOUS | 226 | 264 |

## Interpretation boundary

A high kappa here means the two rule policies were written to agree, not that two independent readers would agree. The WP3 gate requires human coders and a separate human adjudicator; this report cannot satisfy it.
