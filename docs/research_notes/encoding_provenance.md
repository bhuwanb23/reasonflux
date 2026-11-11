# Encoding provenance — line endings and frozen hashes

**Status:** explanatory note; it does not change any result, disposition, or archived record.  
**Prepared:** 2026-11-10  
**Applies to:** Phase 13H and Phase 14J source manifests, and the WP3 annotation packets.

## Why this note exists

Several saved manifests record SHA-256 digests over the exact bytes of text artifacts. Those digests were produced on a Windows working tree where some CSV/JSON files used CRLF line endings, while the Git blobs for the same files are stored with LF. A checkout on another platform — or a normalized checkout on Windows — therefore changes the bytes without changing the text.

The repository now enforces LF for text artifacts via [`.gitattributes`](../../.gitattributes). Annotation packets have been checked out with LF so their recorded hashes verify exactly on every platform. Some earlier source manifests still contain CRLF-derived digests. Their **content** is unchanged; only the line-ending encoding differs.

## Verification rule

For a manifest digest that does not match the LF file:

1. Convert the file's LF bytes to CRLF in memory: `raw.replace(b"\n", b"\r\n")`.
2. Hash that byte string with SHA-256.
3. The result must equal the recorded digest.

A mismatch that is **not** explained by this rule is a content change and must be treated as an integrity failure.

This rule is implemented in [`tests/submission/test_submission_readiness.py`](../../tests/submission/test_submission_readiness.py). The test suite fails if any listed source is missing, changed, or mismatched for a reason other than line endings.

## Files with CRLF-derived digests

### Phase 13H `source_manifest.json`

- `reports/experiments/PHASE-13D-TRANSFER-V1/posthoc_pairwise_baselines.csv`
- `reports/experiments/PHASE-13E-CAP-GROWTH-V1/seed_summary.csv`
- `reports/experiments/PHASE-13F-BASELINE-ABLATION-V1/seed_summary.csv`

### Phase 14J `source_hashes.csv`

- `reports/experiments/PHASE-14B-IDT-CRITICAL-ANALYSIS-V1/idt_scorecard.csv`
- `reports/experiments/PHASE-14B-IDT-CRITICAL-ANALYSIS-V1/threats_to_validity.csv`
- `reports/experiments/PHASE-14C-SCT-CRITICAL-ANALYSIS-V1/sct_scorecard.csv`
- `reports/experiments/PHASE-14C-SCT-CRITICAL-ANALYSIS-V1/scv_predictor_comparison.csv`
- `reports/experiments/PHASE-14C-SCT-CRITICAL-ANALYSIS-V1/threats_to_validity.csv`
- `reports/experiments/PHASE-13C-SCT-V1/reuse_statistics.csv`
- `reports/experiments/PHASE-13C-SCT-V1/matched_controls.csv`
- `reports/experiments/PHASE-13C-SCT-V1/candidate_level.csv`
- `reports/experiments/PHASE-13D-TRANSFER-V1/posthoc_pairwise_baselines.csv`
- `reports/experiments/PHASE-13E-CAP-GROWTH-V1/seed_summary.csv`
- `reports/experiments/PHASE-13E-CAP-GROWTH-V1/seed_round_arm.csv`
- `reports/experiments/PHASE-13F-BASELINE-ABLATION-V1/master_result_matrix.csv`
- `reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/task_outcomes.csv`
- `reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/discovery_trace_quality.csv`
- `reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/growth.csv`
- `reports/experiments/PHASE-14G-ARC-FAILURE-ANALYSIS-V1/source_hashes.csv`

## What is not changed

- No metric, seed, task outcome, threshold, or disposition is recomputed.
- The annotation packets are byte-exact under LF and are tested directly.
- The S3 provenance exclusion is unaffected; see [s3_provenance_date_reconciliation.md](s3_provenance_date_reconciliation.md).
- The archived execution record remains untouched.

If a future correction wants byte-identical legacy digests, it should add a new versioned manifest that records the encoding explicitly, rather than editing the historical manifest or silently changing the files.
