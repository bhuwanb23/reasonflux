# Package F — ARC External-Validity Evidence

**Phase:** 13G bounded ARC-AGI-2 DSL validation.  
**Question:** Do traces→invariants→skills→transfer→capability growth operate on disjoint ARC discovery, transfer, and holdout tasks?

## Protocol and boundaries

- ARC-AGI-2 public data were pinned to commit `f3283f727488ad98fe575ea6a5ac981e4a188e49`; the Phase 13G package contains the protocol, task split, frozen DSL, arm outputs, and source disclosure.
- 1,000 public training tasks were assigned disjointly to 600 discovery / 200 transfer / 200 holdout task IDs. The official evaluation set was not scored.
- The bounded adapter has 10 symbolic programs. Exact demonstration-fit rates were 3/600 discovery, 5/200 transfer, and 2/200 holdout. The DSL did not operationalize several major ARC families (including object/counter/grouping-style concepts); the rates therefore characterize coverage of this adapter, not the full ARC problem distribution.
- Main evaluation used three task trials per task where supported. All five arms scored 1/200 exact holdout task accuracy (0.5%). The transfer and capability endpoints cannot be treated as a completed full-system mechanism chain.

## Results

- Only three discovery tasks supplied exact-fitting traces; the invariant support threshold was five. Result: **zero invariant candidates**.
- Result: **zero skills and zero capabilities**; IS, IG, and downstream capability growth were unavailable, not zero-valued evidence for a successful mechanism.
- Every arm had 1/200 exact holdout accuracy; ASFT had no advantage over B1–B4.
- The task-level result is not evidence that ASFT solves ARC and is not an official ARC-AGI-2 evaluation score.

## Exposure / protocol deviations

Attempt 01 produced predictions in memory but failed during report serialization (`KeyError: 'task_id'`). The defect was corrected by task-ID serialization and representation of unsupported-task stability; the same frozen holdout was rerun. Attempt 02 is not independent confirmation. The first attempt and exposure are preserved in the Phase 13G package.

The temporary upstream archive included evaluation blobs. Only archive filenames were listed; no evaluation JSON was extracted, parsed, or scored, and the archive was deleted. A pre-run training-grid schema audit was performed. These deviations are disclosed; do not say that no evaluation bytes were ever downloaded.

## Judgment

**ARC external validity is not demonstrated.** The outcome is a bounded-DSL low-coverage null: it is informative that this adapter did not create the proposed mechanism chain, but does not fairly test an unrestricted ARC reasoner or prove impossibility. A future ARC study would require a frozen, materially broader program inventory and coverage audit before the untouched evaluation is used, with no iterative holdout tuning and no reuse of the 13G holdout as independent confirmation.

Source: [Phase 13G evidence package](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/evidence_package.md); official source and pinned commit metadata are preserved under `datasets/arc/arc-agi-2/`.
