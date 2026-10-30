# ASFT Metrics

Pointers for Capability Growth Metrics (CGM) and related quantities. Config registry: `configs/metrics.yaml`.

## Invariant Strength (IS) — IDT

\[
IS(I) = Frequency \times Consistency \times Generality
\]

Threshold: `configs/thresholds.yaml` → `invariants.minimum_invariant_strength` (default `5.0`).

## Skill Creation Value (SCV) — SCT

\[
SCV = Reuse \times AG \times TS - CreationCost
\]

Create skill when `SCV > skill_creation_threshold` (default `0.0`).

## Skill Utility (SU)

\[
SU = AccuracyGain \times CostReduction \times Transferability
\]

## Transfer Score (TS)

\[
TS = Performance_{after} - Performance_{before}
\]

## Capability Growth Rate (CGR)

\[
CGR = \frac{Capability_t - Capability_{t-1}}{\Delta t}
\]

## Intelligence Growth (IG)

\[
IG = f(AG, SU, TS, CGR)
\]

where Abstraction Gain \(AG = RC_{before} - RC_{after}\).

## Code homes

| Metric | Module |
| --- | --- |
| IS | `src/invariants/strength.py`, `src/evaluation/invariant_metrics.py` |
| SCV / SU | `src/skills/trigger.py`, `src/evaluation/skill_metrics.py` |
| TS | `src/evaluation/transfer_metrics.py`, `src/transfer/` |
| CGR / IG | `src/evaluation/growth_metrics.py` |
