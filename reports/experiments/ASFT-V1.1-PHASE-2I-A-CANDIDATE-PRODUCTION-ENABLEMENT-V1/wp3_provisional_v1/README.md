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

## Reproduce

```
python experiments/phase2ia/wp3_provisional.py
```

## Permitted and prohibited use

Permitted: rubric debugging, sampling disagreements for human review, estimating the `UNKNOWN_AMBIGUOUS` rate, and prioritising reviewer effort.

Prohibited: treating any label as a human annotation, passing `task_family_map.csv` into family qualification or candidate eligibility, running Phase 2I on it, or reporting the kappa as inter-annotator reliability.
