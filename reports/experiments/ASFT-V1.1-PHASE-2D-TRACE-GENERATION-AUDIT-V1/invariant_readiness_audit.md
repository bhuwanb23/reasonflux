# Phase 2D.7 — Invariant Readiness Audit

## Decision: **I3 — Not Ready**

The invariant miner did not receive enough successful, recurrent, diverse discovery traces to make invariant discovery a meaningful test. This conclusion is based on actual successful trace inputs and the unchanged Phase 13G TraceMiner—not on invariant strength scores.

| Condition/input | Successful discovery traces | Distinct operation signatures | Max distinct-task support | Fragments | Raw patterns | Structures | Candidates |
|---|---:|---:|---:|---:|---:|---:|---:|
| Phase 13G historical | 3 | 3 | 1 | 30 | 0 | 0 | 0 |
| S1 / cap 3 | 1 | 1 | 1 | 10 | 0 | 0 | 0 |
| S2 / cap 6 | 2 | 2 | 1 | 20 | 0 | 0 | 0 |
| S3 / cap 15, pool 10 | 3 | 3 | 1 | 30 | 0 | 0 | 0 |
| S4 / all ten | 3 | 3 | 1 | 30 | 0 | 0 | 0 |

The frozen miner/policy requires frequency/cross-trace support **5**, consistency **1.0**, and at least **2 task families**. Every successful discovery operator has support one. The miner creates fragments, but no raw patterns, structures, rejected candidates, or invariant candidates. Thus **zero invariants do not show that the miner failed on an adequate trace corpus**: the corpus never met its minimum recurrence condition, and there was no positive-control trace set to test the miner's behavior when adequate, diverse traces are supplied.

## What can be localized

- Trace production itself is not zero: one record exists per task/condition.
- Structural validity is high: all new Phase 2C-derived traces pass independent audit; historical records validate retrospectively, though generation-time validation is unproven.
- Successful trace yield is extremely low (0.2–1.0%).
- Discovery support and recurrence remain below the frozen threshold; diversity is low.
- The actual miner's pattern-extraction stage reports zero raw patterns; candidate generation never receives a candidate-bearing pattern.
- Skill, transfer, and capability readiness cannot be inferred from zero invariant candidates; their conditional denominators are zero/not estimable.

A positive-control audit with a preregistered synthetic or independently labeled trace corpus could test miner plumbing separately, but it would not count as ARC evidence or confirmatory validation.