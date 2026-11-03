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

## Two separate completion scales

**AI draft completion: 100%.** All 600 tasks have an Agent A draft, an Agent B draft, and an Agent C synthesis with a full audit trail. Nothing is missing for review.

**Human gate completion: 0%.** No record carries a human sign-off. Every row is `review_status=UNREVIEWED` with an empty `reviewer_id`, `reviewed_at_utc`, and `sign_off_sha256`. A human review is only counted when a signed record verifies against the exact draft hash it claims to judge; editing a CSV value cannot create one.

## Where reviewer effort should go

| Priority class | Tasks | What it means |
|---|---:|---|
| `A_CODERS_DISAGREE` | 124 | the two AI passes reached different families; these decide whether the rubric is usable |
| `B_UNRESOLVED_AMBIGUOUS` | 221 | no family was asserted; may indicate a missing rubric decision rule |
| `C_LOW_CONFIDENCE` | 49 | families agree but evidence is weak |
| `D_ROUTINE_CONFIRM` | 206 | agreement with at least medium confidence; spot-check only |

See `disagreement_priority_queue.csv` for the ranked task list and `reviewer_A_packet.jsonl`, `reviewer_B_packet.jsonl`, `reviewer_C_packet.jsonl` for blinded review packets.

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
| Annotator A completed | AI DRAFT ONLY — no human coder has signed a review |
| Annotator B completed | AI DRAFT ONLY — no human coder has signed a review |
| Independent annotators | NOT MET — both passes are deterministic policies in one repository |
| Adjudicator completed | AI DRAFT ONLY — no human adjudicator has signed a review |
| Cohen's kappa >= 0.70 | DESCRIPTIVE ONLY — measures policy agreement, not reader reliability |
| Disagreements adjudicated | AI DRAFT ONLY — 124 tasks queued for human adjudication |
| Family map frozen and hash-pinned | NOT MET — hash-pinned but not human-adjudicated |
| No prohibited data accessed | MET — train-only packet, verified hashes |

**WP3 remains INCOMPLETE.** The map produced here is `AI_PROVISIONAL` and must not be used for family qualification, candidate eligibility, Phase 2I execution, or any capability claim. Promoting it requires signed human reviews that verify against these draft hashes; see `wp3_human_review.py` for the enforcement rule.

## What this is useful for

1. A complete, reproducible first pass over all 600 discovery tasks.
2. A ranked disagreement queue so human effort lands on the 124 conflicting cases first.
3. Blinded A, B, and adjudicator packets that let real coders review without seeing each other's labels.
4. Evidence about which rubric families are mechanically detectable and which need human judgement, including a quantified `UNKNOWN_AMBIGUOUS` rate.

## What this is not

- Not human annotation, and not a substitute for the two independent coder streams.
- Not reliability evidence; kappa measures agreement between two rules, not between readers.
- Not a validated family map; label accuracy against ground truth is unmeasured.
