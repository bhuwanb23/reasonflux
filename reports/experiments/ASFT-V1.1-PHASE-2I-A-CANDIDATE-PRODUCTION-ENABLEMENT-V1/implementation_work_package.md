# Phase 2I-A — Candidate Production Enablement Work Package

## 1. Objective and boundary

**Objective:** implement the frozen prerequisites that make the Phase 2I R1-vs-R3 candidate-production diagnostic runnable. Success for this work package is a reproducible, tested pipeline and frozen inputs/configuration—not nonzero yield.

Phase 2I-A does **not** run the 600-task ARC diagnostic, inspect or score test outputs, estimate candidate yield, alter the Phase 1C construct, establish invariant impossibility, authorize Phase 3B/3D, or create a new readiness phase. An ARC candidate-production run is **not authorized** by this work package. After the engineering deliverables are complete, a run-specific protocol and separate authorization remain necessary.

The empirical critical path is specifically the **ARC invariant-candidate production path**: representation/parser → semantic trace → mining/generation → independent family qualification → candidate identity/registry. This locates the current bottleneck upstream of Phase 3 pressure/power/calibration; it does not establish that other ASFT questions are resolved or that all roadmap risk reduces to this path.

## 2. Frozen scientific invariants

1. The ranked object remains the generated `Invariant` candidate. Traces, fragments, patterns, structures, solver programs, skills, and capabilities remain distinct pipeline stages.
2. Compare R1 current ten-program reference with only Phase 2F R3 object-centric representation. Do not substitute R2/R4–R7 if R3 is difficult.
3. Retain the Phase 2I thresholds: frequency/support 5, cross-trace support 5, consistency 1.0, and at least two independently annotated task families; retain the existing candidate rejection rules. Resolve runtime/default and generator/qualification discrepancies before freeze, not after yield is known.
4. Candidate acceptance for this diagnostic is pre-outcome generation/structural eligibility. Do not require transfer/future-value observations to create the population, and do not use future utility to select it.
5. The historical 600 discovery IDs are development-only, already exposed, demonstrations-only material. This work package does not execute them. No test outputs, hidden outcomes, confirmation/replication allocation, or future-value data may be used.
6. A no-fit, parser failure, unavailable annotation, budget exhaustion, no trace, no pattern, rejection, and missing feature remain separate states. No missing denominator is converted to zero.
7. Any eventual P1 returns through Phase 3A-R; it does not unlock Phase 3B. P2/P3/P4/P5 retain Phase 2I decision rules.

## 3. Workstream order and deliverables

### WP0 — Lock design ambiguities before implementation

Resolve every `OPEN_BEFORE_CODE` entry in `ambiguity_register.csv` through a versioned, owner-approved addendum to the R3 grammar/trace contract. The implementation may not make undocumented semantic choices. Record exact definitions, tests, version, and SHA-256. This is specification completion within the work package, not a redesign of RQ1.

### WP1 — R3 parser and finite candidate enumerator

Implement the Phase 2F R3 object parser and one-selector/one-action grammar only. Suggested home: `src/representations/r3.py` with isolated unit tests. It must provide deterministic object records/IDs, parse status, canonical candidate IDs, deterministic enumeration, training-demo-only parameter inference, exact demo-fit, invalid-candidate reasons, and a ten-trial ceiling. No relations, groups, compositions, hidden helpers, learned heuristics, test-output access, or candidate-coverage quota.

Freeze code + grammar hashes only after tests pass. Failed/ambiguous parses are explicit parser states, not `NOT_FOUND`.

### WP2 — Common semantic trace schema and R1/R3 adapters

Define one versioned schema with a common event vocabulary, stage, semantic operation/scope, and canonical source lineage. Add deterministic adapters for R1 and R3 that emit no more than one valid trace per task/condition and at most four high-level steps; the complete search ledger is stored separately. Candidate-specific transformation meaning must survive normalization; generic “validate / reason / verify” control traces alone are insufficient. Raw parameters, program IDs, arm labels, test outputs, and family labels must not be mined as operation tokens.

Test the schema validator, one-to-one mapping tables, round-trip serialization, invalid cases, and the same downstream miner on both adapters. If a common semantic representation cannot preserve the defined operation meanings without arm-specific leakage, stop and request a protocol decision rather than weakening the construct.

### WP3 — Independent task-family annotation

Create a family ontology/rubric and frozen assignment file for the 600 allowed discovery IDs. Annotators see only permitted task training demonstrations and stable task IDs; they do not see R1/R3 solver programs, traces, candidate outputs/yield, or test outputs. Use independent double annotation, adjudication under the written rubric, report pre-adjudication agreement and missing/ambiguous labels, freeze the final mapping/hash before any Phase 2I run, and keep it in a separate input channel from solver traces. No family assignment may be inferred from representation, solver program, or mined signature. If usable independent families cannot be assigned, the ≥2-family eligibility endpoint is unavailable—not waived.

**Non-qualifying remote AI-provisional bundle:** A commit-pinned 600-task bundle is recorded in `package_manifest.json`. Its three deterministic AI policies share feature code, ontology, and author; its label map is explicitly not human-adjudicated. The reported agreement statistics are descriptive policy-agreement measures, not human reliability. The map cannot satisfy WP3, support family or candidate eligibility, or authorize a Phase 2I run. Two independent human coding streams and a separate human adjudicator remain required.

### WP4 — Candidate policy/config and identity freeze

Produce one machine-readable runtime config and a runtime assertion that the exact values used are the registered values. Pin the miner, generator, rejection implementation, structural-qualification stage, trace normalizer, and identity/serialization code. Explicitly separate:

- proposal/accepted-candidate production using the frozen frequency, cross-trace, consistency, family, and rejection requirements; and
- downstream qualification/transfer/feature readiness, which remains separately reported and cannot use future utility to decide population entry.

Resolve the existing `InvariantIdentity` behavior (family evidence stored but excluded from fingerprint), and verify that the same canonical operation signature has a declared identity policy across families and arms. Preserve full source/family provenance even when candidates deduplicate. Do not silently patch identity semantics or alter the Phase 1C construct.

### WP5 — HCC positive plumbing control (BUILD)

Build a deterministic, versioned synthetic corpus for the six specified known-rule families, with labels kept out of solver inputs and with equivalent registered programs verified for each compared representation. Test that the shared evaluator, trace adapters, fixed miner, candidate generator, and rejection path behave as expected under controlled recurring/diverse synthetic traces. HCC is a software contract only: place outputs in a separate control namespace and hard-fail any attempt to mix HCC with ARC task IDs or candidate counts. A passing HCC is not ARC evidence.

**WP5 implementation boundary/result (2026-11-02):** `experiments/phase2ia/hcc_control.py` (`ASFT-2I-HCC-SYNTH-V1`) builds 120 in-memory tasks (20 per known rule; three synthetic layout cohorts), evaluates two train demonstrations per task under both registered R1 operation effects and R3 object actions (240 exact demo checks per arm), adapts the matched events, and verifies the frozen WP4 miner/generator/rejection/structural-check path. The miner positive control receives an explicitly oracle-selected one-action observation from each adapter trace so the known action pattern is not bridged by common control events when the frozen `min_core_length=1` aggregation setting is used. It is therefore a candidate-stage plumbing check—not search coverage, not a full four-event trace-to-candidate integration result, and not ARC evidence. The observed control had six matching generator-accepted and six structurally eligible candidates per arm. All identifiers use the `HCC-` namespace; a negative test rejects their inclusion in an ARC task-ID input list. No outputs are written to ARC registries or mixed with ARC candidate counts.

### WP6 — Deterministic runner, logs, and provenance

Create a run interface that accepts an explicit registered arm, allowed task-ID file, demonstrations-only loader, frozen config, and resource limits; it must fail closed on forbidden outputs/paths. Log per-task search trials/candidate IDs/stopping reason/parser status, trace validation, and every downstream attrition stage. Add independent checks that the R1/R3 IDs and order match, the cap is identical, HCC cannot enter ARC yield, all outputs have lineage, and the frozen policy hashes match. Provide a replay test on synthetic fixtures only as part of this work package.

**WP6 synthetic engineering implementation (2026-11-02):** `experiments/phase2ia/runner.py`, `search_adapters.py`, and `train_only_source.py` provide paired R1/R3 search callbacks using the registered ten-candidate languages, a task-ID-file entry point, a path-confined train-only streaming source, hard worker time/memory limits, cell/task/trial caps, family-map and train-demo hashes, opaque per-trial candidate IDs, candidate-stage ledgers, arm-separated identities, stable serialization, and an exact output-file/field/hash audit. ARC mode is fail-closed without a separate authorization manifest bound to protocol/task/source-allowlist/family-map/config/resource-limit/arm/grammar/runner/adapter/search-code hashes. Synthetic end-to-end tests cover file source → bounded search → semantic trace → miner → serialized-artifact audit; they also reject a trailing test-output sentinel and verify path, field, budget, and HCC boundaries. WP6 engineering plumbing is implemented and synthetic-tested. This does not constitute an ARC run or audit of actual ARC artifacts: no ARC source map, independent WP3 family map, or run authorization is supplied, and none is opened or invoked.

Add an artifact-boundary audit over every ARC input, intermediate, log, registry, and report: no generated ARC artifact may contain task test outputs, derived/predicted test outputs, hidden evaluation fields, or outcome-bearing fields. Enforce an explicit field/path allowlist, scan serialized artifacts against the forbidden-field policy, record the audit result and artifact hashes, and include a negative test proving the runner rejects a test-output sentinel. HCC may contain only its own synthetic oracle data in its isolated namespace; HCC gold outputs must never be confused with ARC task test outputs or enter ARC artifacts.

Do not invoke the ARC run as part of implementation, unit testing, package QA, or finalization.

## 4. Completion criteria (engineering DoD)

Phase 2I-A is complete only when all are true:

- R3 grammar ambiguities are resolved, versioned, owner-approved, and hash-pinned; parser and enumerator contract tests pass.
- R1 and R3 adapters satisfy the same tested, versioned semantic trace schema and independent trace validation; no program-specific or outcome-derived labels leak into mined events.
- Family ontology, double-annotation/adjudication protocol, labels, agreement report, and hash are frozen independently of solver outputs.
- A single runtime config exactly instantiates Phase 2F values and the unchanged candidate policy; runtime asserts and provenance hashes pass.
- Candidate identity and cross-arm/within-arm deduplication semantics are documented and tested; lineage is complete.
- HCC generator/oracle tests pass in an isolated namespace and exclusion tests prove HCC cannot count toward ARC yield.
- Runner access controls, equal budgets, separate attrition states, reproducibility, and provenance checks pass on synthetic fixtures.
- **No generated ARC artifact contains task test outputs, derived/predicted test outputs, hidden evaluation fields, or outcome-bearing fields.** A field/path allowlist, serialized-artifact audit, forbidden-sentinel rejection test, and artifact hashes are retained as acceptance evidence; HCC synthetic oracle outputs remain isolated from ARC artifacts.
- Worktree scope and all generated artifacts are inventoried; no unrelated pending work is modified.

Passing these criteria means **“Phase 2I implementation enabled” only**. It does not mean the empirical run is authorized or that candidates exist.

## 5. Handoff after engineering completion

Prepare a run-specific protocol listing exact code/config/annotation/trace hashes, task ID list/hash, randomization/replay seeds (if any), read restrictions, planned artifacts, decision rules, and abort criteria. Review against Phase 2I's frozen protocol and confirm no outcome/test data access. Only then may the owner authorize the diagnostic run. Report every registered arm and all attrition stages; do not select by yield. Any nonzero accepted-candidate population returns through Phase 3A-R review.

## 6. Roles (not assigned here)

- **Representation implementer:** R3 parser/enumerator and deterministic search semantics.
- **Trace/mining implementer:** event schema, adapters, validation and downstream parity.
- **Independent annotation team:** family ontology application, double annotation and adjudication; no solver-output access.
- **Policy/identity reviewer:** reconcile config, candidate entry rules and canonical identity.
- **Independent QA reviewer:** HCC isolation, data-boundary tests, hashes, replay/provenance and worktree scope.

The same person should not unilaterally approve their own family adjudications or policy/identity changes.
