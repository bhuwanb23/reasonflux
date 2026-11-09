# S3 provenance date reconciliation — submission hold

**Prepared:** 2026-10-28  
**Status:** unresolved; T2T/S3 is excluded from the current submission-facing draft. This note does not alter the immutable execution record.

## Discrepancy

- Current manuscript date: 2026-10-28.
- S3 execution record `reports/experiments/T2T-S3-EXEC-2026-11-05-001/s3_execution_record.json`: `completed_at` is 2026-11-05.
- The record timestamp is later than today's date. This cannot be resolved by editorial wording alone.

## Handling decision

Preserve the S3 execution record exactly as archived. Do not edit its timestamp, rerun S3, or silently replace the date in a paper. The user's statement that dates may be changed is taken as permission to correct *submission-facing metadata after verification*, not as evidence of what the true execution date was.

Before external submission:

1. Check an independent contemporaneous source (e.g., session event log, immutable file creation/audit history, or signed run manifest) for the actual execution date.
2. If the source confirms a transcription/date bug, write a separately versioned provenance correction that links the original hash-identified record and gives the corrected date with evidence. Do not modify the immutable original.
3. If no independent confirmation is available, omit the S3 empirical result from the submission-facing manuscript and describe the archived record only as unverified/provenance-inconsistent; do not present 105/105 as a verified contemporaneous result.
4. Do not backdate the manuscript or change the current date merely to make the dates align.

## Effect on manuscript

`arc_claim_evaluation_case_study_draft_v4.md` is the current submission-facing draft and excludes T2T/S3 from the abstract, empirical narrative, table, and figure. It retains a concise exclusion note for transparency. Earlier drafts retain the provisional S3 discussion for historical reference only and are superseded. That draft must not be treated as ready to submit.
