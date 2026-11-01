# 14I-E — Implementation Validity

## Question

Could software, protocol-to-code differences, or measurement implementations explain the outcomes or change what was actually tested?

| Issue | Evidence | Validity consequence |
|---|---|---|
| Bounded ARC adapter | Ten fixed programs; low exact-demo coverage; several task concepts not operationalized | ARC result applies to this adapter, not broad ARC reasoning. |
| Discovery budget mismatch | Frozen config declares 3 candidates/task; `discover()` defaults to 10; scored arms use 3 | 3/600 is a full-inventory discovery yield, not declared-budget yield. Only reflection among the three observed fits is among the first three fixed programs. |
| Growth output mislabeled | `n_successful_traces` records prefix length 100–600, not successful-trace count | True successful discovery count is 3 under the 10-program scan; do not cite prefix length as success count. |
| Attempt-01 report failure | Phase 13G produced predictions in memory, then serialization failed; same holdout reused | Not independent/pristine holdout confirmation. |
| Phase 13B accounting correction | Absolute TU changed between recorded versions; ranker tie and gate failure remain | Keep version labels; no blending of magnitude estimates. |
| Phase 13D corrected posthoc view | Reporting/lookup and coverage issues audited with saved outcomes | Report as corrected analysis; not a rerun or independent replication. |
| Phase 13C CLI display defect | CLI showed calibration seed labels; saved record identifies confirmation seeds 20–29 | Reporting defect is documented; rely on frozen saved record, not console line. |
| Cost-model sensitivity | Phase 13C frozen `MC=0.06`; net value changes under cost sensitivity | Net value is conditional on simulator cost assumptions. |
| Synthetic trace provenance | Synthetic traces produced by known solver logic | Limits inference from trace recurrence to independent, general reasoning. |

## Verdict

**High overall; critical for ARC adapter estimates.** These issues are localized and disclosed. They require precise estimand labels, not blanket rejection of all saved results. No Phase 13 outputs were changed for this validity review.
