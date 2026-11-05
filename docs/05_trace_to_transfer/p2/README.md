# P2 Deliverables — Formal Skill Object

**Contract:** `T2T-SkillObject-v1.0.0-draft`  
**P2 status:** complete for documentation/design scope, 2026-11-03.  
**Authorization boundary:** no implementation, experiments, benchmarks, ARC runs, split assignment, or restricted-outcome access.

## Outputs

- [`schema_v1.json`](schema_v1.json) — Draft 2020-12 JSON Schema for CandidateVersion, SkillVersion, EvidenceSnapshot, LifecycleEvent, PromotionDecision, ApplicabilityResult, PredictionRecord, EffectAssessment and CounterexampleRecord.
- [`interoperability_fixtures.md`](interoperability_fixtures.md) — normative synthetic fixtures, expected behavior, and failure cases. These are documentation examples, not scientific results.
- [`../formal_skill_object.md`](../formal_skill_object.md) — full normative object contract, identity/version rules, replay distinction, evidence/lifecycle semantics, validation invariants, and unresolved decisions.

## P2.1–P2.3 results

- **P2.1 Schema:** separated non-executable CandidateVersion from executable SkillVersion; pinned IDs, content digests, representation versions, typed unknowns, evidence snapshots, pre-outcome PredictionRecords, and append-only lifecycle records.
- **P2.2 Invariant vs replay:** defined raw replay, strong parameterized/compressed replay, and invariant-skill semantics. Claim N requires a distinguishable semantic increment under the same evidence and matched resources; if strong replay matches, invariant-specific value is unsupported/unidentifiable.
- **P2.3 Evidence and lifecycle:** made source evidence append-only and outcome-isolated; separated PredictionRecord from later EffectAssessment; specified support/contradiction/unknown classes, candidate and skill state paths, quarantine, successor versioning, retirement, and future validation/activation boundaries.

## Consistency and QA

Final QA: JSON parses; Draft 2020-12 meta-schema validation passes; all three embedded JSON examples (two applicability results and one prediction record) validate against the schema; negative structural controls reject `APPLICABLE` with an `UNKNOWN` predicate and reject restricted-outcome evidence; 51 Markdown files were checked with zero broken relative links. These are **schema/documentation QA only**—not implementation, experimental evidence, scientific validation, or execution authorization. Semantic checks (content-hash recomputation, reference resolution, prediction-before-outcome ordering, legal transition graph, permission manifest, and data-access policy) remain contract rules for a future authorized implementation.

## Deliberately unset

No canonical JSON/hash profile or project stable-ID scheme, state/object ontology, relation DSL operator inventory, recurrence/support/promotion threshold, confidence calibration, exact replay budget, runtime resource cap, or data split is frozen by P2. No candidate was created, promoted, validated, or run.
