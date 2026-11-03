# AI_PROVISIONAL — NOT HUMAN ANNOTATION — NOT WP3-ELIGIBLE

**Not Independent Human Annotation**  
**Not Eligible For Family Qualification**  
**Not Eligible For Candidate Eligibility**  
**Not Eligible For Phase 2I Execution**  
**Not Eligible For WP3 Completion**  

## What was produced

- Run ID: `ASFT-WP3-AI-PROVISIONAL-V1`
- Ontology: `WP3-ONTOLOGY-V1`; policy: `WP3-AI-PROVISIONAL-V2`
- Tasks labelled: **600** (one record per discovery task, no gaps)
- Agent A stream: 600 labels
- Agent B stream: 600 labels
- Agent C adjudication records: 600
- Exact A/B agreement: 476/600 (79.3%)
- Descriptive Cohen's kappa: 0.7196

## Final label distribution (provisional)

| Family | Tasks | Share |
|---|---:|---:|
| UNKNOWN_AMBIGUOUS | 226 | 37.7% |
| COLOR_ATTRIBUTE | 191 | 31.8% |
| REGION_TOPOLOGY | 71 | 11.8% |
| COUNT_REPLICATION | 35 | 5.8% |
| OBJ_RELATION | 25 | 4.2% |
| FRAME_BOUNDS | 24 | 4.0% |
| PATTERN_COMPLETION | 17 | 2.8% |
| SPATIAL_CHANGE | 8 | 1.3% |
| SYMBOLIC_SEQUENCE | 3 | 0.5% |

## WP3 gate status

| Gate condition | Status |
|---|---|
| Annotator A completed | PARTIAL — AI agent only |
| Annotator B completed | PARTIAL — AI agent only |
| Independent annotators | NOT MET — both passes are deterministic policies in one repository |
| Adjudicator completed | PARTIAL — AI agent, not independent |
| Cohen's kappa >= 0.70 | DESCRIPTIVE ONLY — see agreement report |
| Disagreements adjudicated | PARTIAL — resolved by policy, not by an independent adjudicator |
| Family map frozen and hash-pinned | NOT MET — provisional map is hash-pinned but not frozen for use |
| No prohibited data accessed | MET — train-only packet, verified hashes |

**WP3 remains INCOMPLETE.** The map produced here is `AI_PROVISIONAL` and must not be used for family qualification, candidate eligibility, Phase 2I execution, or any capability claim.

## What this is useful for

1. A complete, reproducible first pass over all 600 discovery tasks.
2. A concrete disagreement list for human reviewers to adjudicate first.
3. Evidence about which rubric families are mechanically detectable and which need human judgement, including a quantified `UNKNOWN_AMBIGUOUS` rate.

## What this is not

- Not human annotation, and not a substitute for the two independent coder streams.
- Not reliability evidence; kappa measures agreement between two rules, not between readers.
- Not a validated family map; label accuracy against ground truth is unmeasured.
