# ARC Threats-to-Validity Assessment

| ID | Severity | Threat | Consequence / boundary |
|---|---|---|---|
| ARC-01 | Critical | Fixed ten-program DSL with very low exact-demo coverage | 3/600 discovery; 5/200 transfer; 2/200 holdout full-inventory fits. No broad ARC claim. |
| ARC-02 | Critical | Sparse successful discovery traces plus min-support gates | Three successful traces, one per program; miner requires support five, so IDT cannot meaningfully be evaluated. |
| ARC-03 | Critical | Budget mismatch across stages: frozen config declares three candidate trials; `discover()` defaults to ten; coverage scan uses ten; scored arms use three | Discovery and coverage counts are not realized rates under the declared three-candidate limit. Source-based fixed-order inspection shows only the reflection fit among the three observed discovery fits is within the first three. This is not a rerun. |
| ARC-04 | High | Counting/grouping/object detection/pattern completion not operationalized | The “unsupported” bucket cannot be interpreted as a semantic ARC taxonomy. |
| ARC-05 | Critical | No invariant population | Skills, learned transfer precision, capabilities, and CGM are unavailable; do not turn nulls into theoretical failures or successes. |
| ARC-06 | Medium | Same frozen holdout reused after attempt-01 predictions were generated in memory | Attempt 02 is not pristine independent confirmation; preserve the disclosure. |
| ARC-07 | High | Bounded task accuracy is poor and all arms tie | Actual implementation failure remains; no ASFT advantage or mechanism attribution. |
| ARC-08 | Medium | Temporary archive contained evaluation blobs | Only filenames listed; no evaluation JSON extracted/parsed/scored; do not claim zero evaluation bytes downloaded. |
| ARC-09 | Medium | `growth.csv` field mislabels prefix length as successful-trace count | Do not cite 100–600 as successful traces; true successful discovery count is 3. |
| ARC-10 | High | No controlled DSL expansion or threshold perturbation in this saved experiment | Representation vs. difficulty vs. miner limitations cannot be causally isolated. |
| ARC-11 | Medium-high | One fit per reflection/rotation/recoloring discovery operation | Trace stability 1.0 for these three cases is not broad trace-reliability evidence. |

**Overall:** high confidence that the fixed tested representation under-covered the split; lower confidence that it uniquely explains all failure or predicts what a more expressive ASFT system would do.
