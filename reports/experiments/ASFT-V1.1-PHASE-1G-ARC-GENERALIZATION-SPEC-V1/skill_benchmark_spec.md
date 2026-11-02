# Phase 1G.6 — Skill Formation Benchmark Specification

## Skill unit

A skill is a versioned reusable operation/policy with explicit preconditions, inputs, outputs, resource costs, provenance, and a measurable behavioral effect. It is not merely an invariant label, compressed trace, or internal object count.

## Independent formation outputs

Report candidate skills, created skills, promoted skills, failed/rejected proposals, promotion rate, survival under disjoint validation, complexity/resource cost, and provenance to invariant/experience records. Skill formation can be assessed and reported even if downstream transfer fails; never erase or recode the skill count because transfer is null.

## Formation/promotion checks

Before promotion, verify reproducible execution, correct behavior on held-out demonstration pairs or a development-only skill test, stable preconditions, bounded resource use, and a frozen minimum support threshold. Keep candidate creation, validation, and promotion as separate stages. Thresholds and minimum counts are calibrated on development and preregistered.

## Reporting outcomes

- `activated`: ≥1 skill independently passes formation/promotion criteria with adequate evidence.
- `not_activated`: adequate validated invariant opportunities existed but no skill passed.
- `inconclusive`: too few/low-quality invariant opportunities to evaluate formation.
- `unavailable`: skill evidence or required scoring denominator is absent.

Transfer is evaluated only afterward and with its own eligible-skill denominator. No transfer denominator is not a skill-formation failure.