# Phase 1G.4 — Discovery Benchmark Specification

## Objective

Measure trace production and structure discovery independently of transfer, capability, and task accuracy. Do not infer discovery success from candidate count alone or infer discovery failure from downstream transfer when no candidates existed.

## Outputs

1. **Trace yield:** attempts, schema-valid traces, successful demo-fits, deterministic replay success, and unique trace signatures.
2. **Trace diversity:** distinct operation/structure signatures, entropy or concentration under a frozen definition, cross-task recurrence, and distribution of failure codes. A thousand failed-search traces do not equal a thousand successful reasoning examples.
3. **Candidate yield:** proposed structures/invariants per successful trace and per task, duplicates, provenance, and rejection/validation reasons.
4. **Discovery yield:** unique candidates that pass preregistered independent validation ÷ attempted tasks and ÷ successful traces, with both denominators.
5. **Stage sufficiency:** number of successful traces and independently annotated/held-out opportunities versus the frozen minimum required to test recurrence.

## Procedures

- Discovery uses development/confirmation tasks only; transfer and final holdout tasks are held out from candidate mining and all fitting.
- Discovery trace fields and candidate scoring rules are frozen before confirmation; no test gold or benchmark labels enter candidate formation.
- Invariant validators use disjoint task IDs/withheld demonstration pairs, counterexample probes, or independent blind annotations. Record validation evidence and disagreements.
- Keep all unsuccessful searches and candidate rejections. A candidate pool of zero is an observed count; whether invariant discovery was testable depends on trace sufficiency.

## Decision labels

`activated` means at least one candidate passes frozen independent validation with adequate denominators. `not_activated` means the stage had adequate valid opportunities but no candidate passed. `inconclusive` means support/annotation precision was inadequate; `unavailable` means a required data source/denominator was absent. These labels describe this benchmark result, not the truth/falsity of IDT.