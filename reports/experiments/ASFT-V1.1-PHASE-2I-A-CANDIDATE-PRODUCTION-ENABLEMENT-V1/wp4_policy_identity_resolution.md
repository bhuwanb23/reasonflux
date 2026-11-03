# WP4 — Candidate Policy and Identity Resolution

**Status:** OWNER APPROVED AND FROZEN as `wp4_runtime_config_v1.json` on 2026-11-02.  
**Boundary:** This is Phase 2I-A engineering work. No candidate search, ARC task processing, family-label assignment, or Phase 2I run was performed here.

## 1. Reconciled runtime settings from the existing record

Phase 2F fixes the primary candidate-production floors at `min_frequency=5`, `min_cross_trace=5`, `min_consistency=1.0`, and at least two independent families. Phase 2E's preregistered miner settings resolve the remaining miner defaults as:

| Field | Proposed frozen value | Evidence / implementation meaning |
|---|---:|---|
| `MiningConfig.min_frequency` | 5 | distinct-trace support floor |
| `MiningConfig.min_cross_trace` | 5 | cross-trace support floor |
| `MiningConfig.max_fragment_length` | 4 | Phase 2E preregistered maximum |
| `MiningConfig.min_core_length` | 1 | Phase 2E preregistered aggregation setting; differs from the current Python default 2 |
| `MiningConfig.successful_trace_bias` | `true` | Phase 2E preregistration |
| `InvariantPolicy.min_frequency` | 5 | frozen candidate recurrence floor |
| `InvariantPolicy.min_consistency` | 1.0 | frozen stability floor |
| `InvariantPolicy.min_task_families` | 2 | families come only from WP3's independent map |
| `InvariantPolicy.min_generality` | 0.0 | Phase 2E preregistration |
| `InvariantPolicy.require_transfer_evidence` | `false` | candidate population is not selected on future transfer utility |
| `InvariantPolicy.min_transfer_events` | 0 | Phase 2E preregistration; disabled for candidate-entry check |
| `InvariantPolicy.universal_noise_generality` | 0.95 | preserve existing rejection threshold |
| task-specific terms / remaining rejection policy | unchanged code values | exact current code is hash-pinned; no edits or term tuning |

These values must be supplied explicitly to runtime objects; library defaults are not acceptable. The full proposed JSON is `wp4_runtime_config_draft.json`.

## 2. Candidate-stage separation required by the existing code

Inspection confirms:

- `TraceMiner` applies `MiningConfig` at pattern extraction and calls `generate_candidates` with an `InvariantPolicy`.
- `generate_candidates` maps structures to `Invariant` objects and invokes the existing rejection criteria. It does **not** itself reject on `min_consistency` or require two families.
- `qualify_invariant` checks recurrence, stability, generality, transfer utility, and—unless explicitly allowed—MVP taxonomy scope.
- `InvariantPolicy`'s default `require_transfer_evidence=true` conflicts with Phase 2I's explicit outcome-blind candidate-entry boundary unless disabled for this pre-outcome diagnostic.

Therefore preserve separate auditable counts for (a) invariant proposals, (b) generator-accepted candidates after the existing rejection rules, and (c) structurally eligible candidates satisfying frequency 5, consistency 1.0, and ≥2 independent families. The Phase 2I P1 decision must use the stage required by its frozen decision rule; do not silently merge these counts or alter `TraceMiner` thresholds.

### Taxonomy interaction requiring explicit approval

`classify_invariant_type` labels a multi-step pattern supported by ≥2 families as `InvariantType.TRANSFER`. `qualify_invariant` then rejects that type by default because the current MVP-supported type set contains only `operational` and `procedural`. That creates a direct conflict between the registered ≥2-family candidate rule and the default downstream MVP taxonomy gate.

**Proposed resolution:** for Phase 2I's structural candidate-population endpoint only, call structural qualification with `require_transfer_evidence=false` and `allow_unsupported_type=true`; report the resulting `InvariantType` explicitly. This does not promote a candidate to a Skill/Capability or remove the existing downstream MVP taxonomy restriction. It preserves cross-family invariant candidates as the Phase 2I object rather than excluding exactly those candidates the registered family criterion seeks to detect.

## 3. Proposed canonical identity decision

Keep the existing `InvariantIdentity` fingerprint implementation unchanged:

- ID payload remains `origin` plus normalized `pattern_signature`; implementation currently emits `INV-` plus the first 16 SHA-256 hex characters.
- `task_families` remain evidence/provenance and are intentionally excluded from the ID payload, so one recurring signature can accumulate independent family evidence rather than becoming a separate ID per family.
- The same normalized signature/origin may receive the same canonical ID in R1 and R3. Counts and candidate registries remain arm-specific; never pool arm yields. If shared, record both source arms/provenance paths.
- Keep the full pattern, family set, task IDs, trace IDs, and source-arm lineage alongside the short ID. Fail closed if one short ID is ever observed with a different full identity payload; do not silently merge a hash collision.

This is the minimum-change interpretation of the current implementation and is consistent with cross-family recurrence, but it needs explicit owner approval because the class docstring mentions families while the hash excludes them. Do not modify the hash function or extend the ID during WP4 without a new decision.

## 4. Approval record and remaining execution gates

The owner approved all three decisions on **2026-11-02**:

1. Keep generator acceptance and pre-outcome structural eligibility as separate counts; apply no transfer/future-value gate at candidate entry.
2. Allow `InvariantType.TRANSFER` for the Phase 2I structural candidate-population diagnostic only; do not alter downstream MVP/skill promotion policy.
3. Preserve the existing family-excluded identity fingerprint; report arm-specific yields/provenance separately and fail closed on full-payload collisions.

The exact settings are frozen in `wp4_runtime_config_v1.json`. WP3's independent family map is still unavailable, and no numeric family floor can fabricate or substitute labels. A Phase 2I run remains unauthorized until WP3, WP5, WP6, and the run-specific authorization gate are complete.
