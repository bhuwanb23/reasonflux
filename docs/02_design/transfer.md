# Transfer-Aware Invariant Discovery (Phase 11C-4)

Transfer is part of the **learning mechanism**, not only an evaluation metric.
An invariant is fully accepted only after it shows measurable benefit beyond its
discovery task family.

Code under `src/transfer/`. Ranking bridge: `src/invariants/transfer_aware.py`.
System-level TS: `src/evaluation/transfer_metrics.py`. Thresholds:
`configs/thresholds.yaml` (`transfer:`).

## Pipeline

```
Candidates (11C-2)
 → Validate F×C×G×T×R (11C-3)
 → Transfer Test
 → Transfer Memory
 → ITS / TU / NTR
 → Transfer Graph + Promotion Gate
 → SCT (11D)
```

Refined ranking term: **T = ITS × TU**.

## Taxonomy

| Type | When | Expected band |
| --- | --- | --- |
| Near | Same family or identical op sets | `very_high` |
| Moderate | Shared core ops, different family | `medium` |
| Compositional | Target = source core + extra ops | `medium_to_high` |
| Structural | `structural=True` or 2+ extra mechanisms | `high` |

Helpers: `classify_transfer`, `expected_transfer_band` in `taxonomy.py`.

## Memory model

`TransferRecord` stores one attempt (`benefit`, `reasoning_reduction` in `[0,1]`).
`TransferMemory` tracks attempts / successes / failures / coverage (distinct
target families) and builds a `TransferMemorySummary`.

## Metrics

| Metric | Formula |
| --- | --- |
| ITS | `sum(benefits) / attempts` |
| NTR | `failures / attempts` |
| TU | `success_rate × reasoning_reduction × task_coverage` |
| Weighted T | `ITS × TU` |
| Confidence | `min(1, attempts / confidence_attempts_norm) × success_rate` |
| TS (system) | `performance_after − performance_before` |

Defaults: `min_transfer_attempts=2`, `min_its=0.5`, `ntr_limit=0.3`,
`confidence_attempts_norm=5`.

## Transfer graph

`TransferGraph` is pure Python (no networkx). Nodes = task families; directed
weighted edges = successful transfers. Built via `from_records`.

## Negative transfer

High NTR (failed applications that harm or fail on targets) blocks promotion.
Example: reflection forced onto pure counting with repeated failures.

## Promotion gate

`evaluate_transfer_gate` requires validation F/C/G (when provided) plus:

- `attempts >= min_transfer_attempts`
- `ITS >= min_its`
- `NTR <= ntr_limit`

`confirm_transfer` advances `VALIDATED → TRANSFER_VERIFIED`, sets
`transfer_contribution = ITS`, and records transfer evidence.

## Success / failure criteria

- **Success:** high-ITS invariants (e.g. reflection) outrank high-frequency /
  zero-transfer patterns (e.g. verify-output); graph links discovery family to
  related targets; gate promotes only evidenced transfer.
- **Failure:** insufficient attempts, low ITS, or NTR above limit → rejected.

## File map

| Module | Role |
| --- | --- |
| `taxonomy.py` | TransferType + classify |
| `records.py` / `memory.py` | Evidence storage |
| `metrics.py` | ITS / TU / NTR / TransferConfig |
| `graph.py` | Family transfer graph |
| `transfer_tracker.py` | Record / summary / scores API |
| `task_mapper.py` | Cross-family `TaskPair`s |
| `gate.py` | Promotion gate + lifecycle |
| `invariants/transfer_aware.py` | Rank with T = ITS×TU |
| `evaluation/transfer_metrics.py` | System TS |

## Non-goals

Skill creation / SCV (11D), CGR learning, transfer predictors, failure-mode
catalogue (11C-5).
