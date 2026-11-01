# EXP-IDT-14 — Critical interpretation

**Role:** exploratory, posthoc controlled synthetic stress test. It is not a replacement for or repair of the frozen Phase 13B primary result.

## Design and observed result

After the Phase 13B ranking tie was observed, a deliberately frequent no-op operation, `normalize_grid`, was inserted into discovery traces in three of four synthetic families. The intended stress was to separate recurrence/frequency ranking from transfer-aware selection. Top-k=1 remained the primary outcome and top-k=2 secondary; the report discloses excluded prototypes.

| Metric | ASFT | Frequency-only | No-transfer | Random |
|---|---:|---:|---:|---:|
| Top-k=1 mean TU | 0.164866 | 0.000000 | 0.000000 | 0.059557 |
| ASFT top-k=1 SD | 0.001100 | — | — | — |
| ASFT top-k=1 95% CI | [0.163902, 0.165831] | — | — | — |
| Top-k=2 mean TU | 0.096322 | 0.082433 | 0.082433 | — |

Frequency-only/no-transfer selected the inserted frequent no-op first; ASFT did not. The result is consistent with the intended mechanism: on this constructed confound, ASFT's transfer-related score can prevent frequency from dominating the top-1 choice.

## What it establishes

It establishes **sensitivity to this specific designed confound** in this exploratory synthetic configuration. It is useful diagnostic evidence that the ranking logic is not merely a frequency sort under every possible candidate pool.

## What it does not establish

- It is not an independent or preregistered replication: the stressor followed observation of the 13B tie.
- It does not change the Phase 13B strict per-seed gate or turn that failed gate into a pass.
- It does not demonstrate a natural-distribution or generally applicable advantage over frequency-only ranking.
- It does not validate IS as a reliable predictor of transfer across task families or domains.
- The top-k=1 result must not replace the original Phase 13B top-k=2 primary endpoint.

**Decision:** retain as exploratory mechanism evidence; do not pool it with the primary Phase 13B result or use it to claim general IDT-3 success.

**Source:** [`EXP-IDT-14/report.md`](../EXP-IDT-14/report.md), [`record.json`](../EXP-IDT-14/record.json).
