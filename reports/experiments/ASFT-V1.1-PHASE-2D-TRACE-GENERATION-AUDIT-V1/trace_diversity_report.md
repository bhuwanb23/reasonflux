# Phase 2D.5 — Trace Diversity Benchmark

## Definitions

- **Unique trace IDs** count task-specific records; they are not evidence of distinct reasoning patterns.
- **Unique solution signatures (D1)** count successful `(program, inferred parameter context)` signatures.
- **Structural diversity (D2)** counts Phase 13G's coarse first-demonstration structural buckets among successful traces. It is a diagnostic label, not an ARC semantic family.
- **Operation diversity (D3)** counts distinct operation labels and program-operation entropy.
- **Template diversity (D4)** counts distinct operation-sequence templates, including the common no-fit template.

## Results across all 1,000 tasks in each condition

| Condition | Successful traces | Unique solution signatures | Structural buckets among successes | Unique operation labels | Operation-sequence templates | Exact discovery support max |
|---|---:|---:|---:|---:|---:|---:|
| S1 | 2 | 2 | 1 | 6 | 3 | 1 |
| S2 | 5 | 4 | 1 | 8 | 5 | 1 |
| S3 | 10 | 8 | 2 | 11 | 8 | 1 |
| S4 | 10 | 8 | 2 | 11 | 8 | 1 |

At the discovery-only level, S1 has one successful signature, S2 two, and S3/S4 three; every exact program/context signature has distinct-task support **1**. Under fullscan, there is one program-level overlap between discovery and transfer (`recolor_bijection`), but the inferred color-map contexts do not recur exactly across the two splits. This is only a potential reusable operator label, not evidence of successful transfer.

The no-fit trace template dominates every condition. A large number of unique task IDs therefore coexists with very little successful-solution diversity and no repeated support. Structural buckets collapse successful traces to one or two coarse groups; this does not establish that ARC itself has only one or two semantic families. Split-level counts, entropy, and templates are in `trace_diversity_summary.csv`.