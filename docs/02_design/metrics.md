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

## Capability representation scores (11E-1)

CapU / CCov / strength / confidence live in `src/capability/`. See
[capability.md](capability.md).

## Capability function and CGR (11E-2)

\[
C_t = w_{su}\cdot\overline{SU} + w_{ts}\cdot\overline{TS} + w_{cov}\cdot CCov + w_{comp}\cdot CP
\]

\[
CGR = \frac{C_t - C_{t-1}}{\Delta t},\quad
CA = \frac{CGR_t - CGR_{t-1}}{\Delta t},\quad
CSR = \frac{NewCapability}{ExistingCapability}
\]

Component deltas: \(TG\), \(CCG\), \(CompG\), \(UG\).

## Capability Growth IG aggregator (11E-2)

\[
IG_{growth} = w_{cgr}\,CGR + w_{tg}\,TG + w_{ug}\,UG + w_{ccg}\,CCG + w_{compg}\,CompG
\]

Defaults: `configs/thresholds.yaml` → `growth:`.

## Intelligence Growth Model (11E-3)

\[
IG = w_{ag}\,AG + w_{su}\,SU + w_{ts}\,TS + w_{cgr}\,CGR + w_{cp}\,CP + w_{ad}\,AD
\]

\[
IGR = \frac{IG_t - IG_{t-1}}{\Delta t},\quad
IA = \frac{IGR_t - IGR_{t-1}}{\Delta t},\quad
IE = \frac{IG}{Experiences}
\]

Elasticity = ΔIG per new task family. Maturity stages: emerging → developing →
generalizing → compositional → adaptive.

Intelligence claims require evidence; detectors cover skill hoarding, transfer
collapse, fragmentation, composition failure, adaptation failure, growth illusion.

## Code homes

| Metric | Module |
| --- | --- |
| IS | `src/invariants/strength.py`, `src/evaluation/invariant_metrics.py` |
| SCV / SU | `src/skills/trigger.py`, `src/evaluation/skill_metrics.py` |
| TS | `src/evaluation/transfer_metrics.py`, `src/transfer/` |
| CapU / CCov | `src/capability/utility.py`, `src/capability/coverage.py` |
| C_t / CGR / CA | `src/evaluation/growth_metrics.py` |
| TG / CCG / CompG / UG | `src/evaluation/growth_components.py` |
| Growth robustness | `src/evaluation/growth_checks.py` |
| IG / IGR / IA / IE | `src/evaluation/intelligence.py` |
| IntelligenceState | `src/evaluation/intelligence_state.py` |
| IntelligenceGraph | `src/evaluation/intelligence_graph.py` |
| Intel robustness | `src/evaluation/intelligence_checks.py` |
