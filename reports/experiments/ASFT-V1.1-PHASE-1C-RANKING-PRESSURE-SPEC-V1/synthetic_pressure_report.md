# Synthetic ranking-pressure contract report

**Scope:** deterministic synthetic interface tests only; not IDT performance evidence.

- Panels: 100
- Gate pass: 100/100
- Mean/min all-pair Top-K RDR: 0.8391 / 0.7875
- Mean/min normalized Kendall divergence: 0.4900 / 0.4538

| R1 comparison | Mean Top-K RDR | Minimum Top-K RDR |
|---|---:|---:|
| Frequency | 0.9463 | 0.7500 |
| Reuse | 0.7600 | 0.6250 |
| Compression | 0.5550 | 0.5000 |
| Random | 0.8037 | 0.3750 |

The 100 panels reuse one fixed feature/type recipe with independent seeds. They are contract fixtures, not independent research batches.
