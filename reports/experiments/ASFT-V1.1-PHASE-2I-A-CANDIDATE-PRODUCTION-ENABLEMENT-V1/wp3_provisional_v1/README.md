# AI_PROVISIONAL — NOT HUMAN ANNOTATION — NOT WP3-ELIGIBLE

**Not Independent Human Annotation**  
**Not Eligible For Family Qualification**  
**Not Eligible For Candidate Eligibility**  
**Not Eligible For Phase 2I Execution**  
**Not Eligible For WP3 Completion**  

## Purpose

A complete, reproducible first-pass family annotation of all 600 discovery tasks, produced by three deterministic AI policies. It exists so that human reviewers can start from a finished pass instead of a blank packet.

## Why this is not WP3 completion

WP3 requires two independent human annotators and a separate human adjudicator, all blind to solver outputs, candidate yield, and test data. Three policies in this repository are not independent readers: they share the same feature code, the same ontology, and the same author. Agreement between them measures policy design, not human reliability.

## Files

| File | Contents |
|---|---|
| `annotator_A_labels.csv` | Agent A mechanism-first labels for all 600 tasks |
| `annotator_B_labels.csv` | Agent B counter-hypothesis labels for all 600 tasks |
| `adjudication_log.csv` | Agent C decision and basis for every task |
| `agreement_report.md` | Descriptive agreement, kappa, confusion matrix, marginals |
| `confusion_matrix.csv` | Machine-readable A x B count matrix |
| `task_family_map.csv` | Provisional adjudicated task to family map |
| `family_map_hash.txt` | SHA-256 pin for the family map |
| `wp3_completion_review.md` | Gate-by-gate status showing WP3 remains incomplete |
| `provisional_manifest.json` | Hashes, boundary checks, and use restrictions |
| `reviewer_A_packet.jsonl` | Blinded packet for coder A: training pairs plus A's AI draft only |
| `reviewer_B_packet.jsonl` | Blinded packet for coder B: training pairs plus B's AI draft only |
| `reviewer_C_packet.jsonl` | Adjudicator packet: both coder drafts plus the AI synthesis |
| `disagreement_priority_queue.csv` | Ranked review order: conflicts, unknowns, low confidence |
| `review_packet_manifest.json` | Packet hashes, field allowlists, and blinding notes |

## Human review workflow

Every label CSV carries `review_status`, `reviewer_id`, `reviewed_at_utc`, and `sign_off_sha256`, all empty. To make a label count as human evidence:

1. A coder opens their own blinded packet and reads the training pairs and their AI draft.
2. They record a decision (`ACCEPTED_BY_HUMAN`, `EDITED_BY_HUMAN`, or `ADJUDICATED_BY_HUMAN`), a final family, and their own rationale.
3. A signed `HumanReview` record is created via `sign_review`, which binds the reviewer identity to the exact `ai_draft_record_sha256` they reviewed.
4. `verify_reviews` rejects the record if the draft changed afterwards, so a stale signature cannot be inherited by an edited label.
5. Only when both required roles are verified for all 600 tasks does `can_promote_to_human_evidence` return true.

Editing a CSV value, renaming a column, or writing a status string does not create a review; the signature check fails.

## Reproduce

```
python experiments/phase2ia/wp3_provisional.py
```

## Permitted and prohibited use

Permitted: rubric debugging, sampling disagreements for human review, estimating the `UNKNOWN_AMBIGUOUS` rate, and prioritising reviewer effort.

Prohibited: treating any label as a human annotation, passing `task_family_map.csv` into family qualification or candidate eligibility, running Phase 2I on it, or reporting the kappa as inter-annotator reliability.
