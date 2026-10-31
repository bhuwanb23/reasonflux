# EXP-IDT-14 — Confounded-Frequency Stress Test

- Exploratory; original Phase 13B gate unchanged.
- Stress test pass: `True`
- Seeds: `[10, 11, 12, 13, 14]`

## Top-1 held-out transfer utility

| Method | Mean | SD | 95% normal CI |
|---|---:|---:|---:|
| Transfer-aware | 0.164866 | 0.001100 | 0.163902–0.165831 |
| Frequency-only | 0.000000 | 0.000000 | 0.000000–0.000000 |
| No-transfer / IS-only | 0.000000 | 0.000000 | 0.000000–0.000000 |
| Random | 0.059557 | 0.017642 | 0.044093–0.075021 |

## Paired ranking differences

- ASFT − frequency: `0.164866`
- ASFT − no-transfer: `0.164866`
- ASFT − random: `0.105309`

## Mean held-out TU by k

| k | ASFT | Frequency-only | No-transfer |
|---:|---:|---:|---:|
| 1 | 0.164866 | 0.000000 | 0.000000 |
| 2 | 0.096322 | 0.082433 | 0.082433 |
| 3 | 0.064215 | 0.064215 | 0.064215 |
| 4 | 0.048161 | 0.048161 | 0.048161 |
| 5 | 0.038529 | 0.038529 | 0.038529 |

This is a designed no-op-confound stress test, not evidence that the original Phase 13B gate passed or that the result generalizes beyond this simulator.
