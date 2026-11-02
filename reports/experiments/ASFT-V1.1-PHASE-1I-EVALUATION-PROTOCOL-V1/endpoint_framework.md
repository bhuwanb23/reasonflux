# Phase 1I.4 — Endpoint Framework

## Endpoint roles

Every confirmatory/replication experiment freezes one and only one **primary endpoint**. It is the single outcome that drives the primary claim decision. Additional measures are labeled secondary or diagnostic before outcomes.

| Role | Purpose | Decision authority |
|---|---|---|
| **Primary** | Directly operationalizes the registered hypothesis/estimand. One per confirmatory claim family or experiment. | Sole driver of pass/contradicted/inconclusive for the primary hypothesis, subject to integrity and multiplicity gates. |
| **Secondary** | Provides supporting or contextual evidence; may test separately registered secondary hypotheses. | Cannot rescue, replace, or reverse a primary miss. Any confirmatory secondary requires a prespecified multiplicity family. |
| **Diagnostic** | Mechanism activity, coverage, selection rate, latency, failure stage, activation, calibration, or other interpretation aid. | Never a substitute primary endpoint; it localizes mechanisms and explains unavailable/non-informative outcomes. |

## Required endpoint definition

For each endpoint record: stable ID; construct name and operational definition; source fields/evaluator; units; direction; task/population; analysis denominator; aggregation; missingness strategy; time horizon; SOI; uncertainty method; scoring code/hash; independent validation evidence; whether it uses internal metrics; and the allowed interpretation. “Accuracy,” “capability,” “transfer,” or “intelligence” without an operational definition is not a complete endpoint.

## Selection and hierarchy

- Exactly one decision-driving primary endpoint. If the scientific claim is inherently multicomponent, define one prespecified composite or a conjunctive pass rule before outcome access; do not count several endpoints as several chances to pass.
- Primary denominator follows the estimand, preferably intention-to-treat over all eligible/randomized opportunities. Conditional per-attempt values are secondary/diagnostic unless explicitly registered as primary.
- Coverage, activation, task accuracy, transfer, capability, and intelligence are separate constructs. One cannot be silently substituted for another.
- Internal scores (IG, IGR, IE, CGR, C_t, SCV, IS, internal utility) may not serve as external target labels or independent outcome scores unless separate validation and authorization are preregistered. Phase 1F's general prohibition on internal scores defining external targets remains in force.
- Any endpoint change after outcome inspection is a protocol deviation/new version, not a correction of the original primary result.

## Illustrative mappings (not default registrations)

| Claim family | Example primary endpoint | Secondary examples | Diagnostic examples |
|---|---|---|---|
| SCT creation policy | Future net utility per eligible candidate/opportunity under frozen costs | Precision, matched-memory net value | Selection/activation rate, candidates rejected, failure reasons |
| IDT ranking | Held-out future task utility at frozen top-k | Paired rank utility at other preregistered k values | Rank correlation, top-k divergence, candidate coverage |
| Memory challenge | Family-specific held-out utility or retention endpoint | Query cost, cross-context accuracy | Bytes, retrieval inspections, match/no-match rates |
| Capability validation | Independent held-out behavioral breadth/retention score | Task-family subscales | Coverage and capability-layer activation |
| Intelligence validation | Future behavior-only learning/adaptation endpoint, not IG | Independent transfer/generalization outcomes | IG predictor availability/calibration; diagnostic only |
| ARC generalization | Frozen held-out exact task accuracy if the preregistered system reaches scoring stage | Partial task metric if explicitly registered | Budgeted coverage, schema-valid trace, invariant/skill activation, failure cascade |

These examples do not define, unlock, or replace the registered endpoint for any existing phase.

## Primary result categories

The primary endpoint is analyzed under the preregistered SOI and interval/decision rule. The claim state is one of supported, contradicted, inconclusive, unavailable, or non-informative. A primary endpoint can be measured while a mechanism claim remains non-informative because decisions did not diverge. Missing score is never encoded as zero unless zero is an observed, valid score by design.