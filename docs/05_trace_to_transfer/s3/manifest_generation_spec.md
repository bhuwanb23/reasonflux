# S3-E Manifest Generation Specification v1

**Status:** frozen for context-only manifest materialization.  
**Owner authorization:** context-only source/held-out manifest generation approved.  
**S3 execution:** not authorized; no outcome exposure or scoring.

## 1. Authorized scope

Materialize only the frozen observable source/held-out/diagnostic context records and role metadata. Do not call `RelationalUnlockWorld.step`, generate effects/outcomes, fit or predict with any arm, evaluate held-out contexts, score, calculate `Delta_N`, or assign Claim N status.

The S3-RA package `T2T-S3-RA-v0.2.0` remains code-frozen. The later owner approval covers manifest construction only and does not change the package's historical freeze-state fields or authorize evaluation.

## 2. Frozen inputs

- `canonical_base_contexts_v1.md` — exact source contrasts, seven primary semantic templates, replicate coordinate offsets, diagnostic masking, and ID rules.
- `counts_decision_required.md` — exactly 7 source contexts; 3 per eligible primary cell across 35 cells (target 105); 2 diagnostics per each of five surface families (10 total); fixed stop policy.
- `transformation_cells_v1.json` — five surface recipes and seven scored semantic families.
- `src/t2t_s3/generator.py` and `src/t2t_s3/transforms.py` — named deterministic recipe constructors and transformations.
- `source_manifest_schema.json`, `heldout_manifest_schema.json`, and `context_role_map_schema.json` — manifest validation contracts.
- `resource_vector_v1.md` and `unknown_state_policy_v1.md` — owner-frozen access and unknown-state policies.

## 3. Required outputs

1. `source_manifest.json` — exactly 7 context-only source contrast rows.
2. `heldout_manifest.json` — all 35 primary cells declared; three context rows per eligible cell, at most 105 total.
3. `diagnostic_manifest.json` — exactly 10 unknown-required-state diagnostic contexts (two per held-out surface family), no exact effect labels.
4. `context_role_map.json` — exactly one role assignment for each manifest context; source and held-out IDs disjoint.
5. `manifest_hashes.json` — SHA-256 hashes of the four context/role artifacts and the frozen input documents/schemas. It does not hash itself.

All output manifests contain observable state/action plus role/cell/provenance metadata only. No effects, labels, predictions, scores, or outcomes are permitted.

## 4. Deterministic construction

- Source contexts are constructed exactly as listed in `canonical_base_contexts_v1.md`. Derive and verify only the six observable source feature bits using `source_only_features`; do not derive outcome labels.
- For each of the seven held-out semantic templates and replicate indices `0,1,2`, apply each of the five named surface recipes exactly once, producing one context for each of the 35 cell IDs per replicate.
- Use the fixed context-ID formats in `canonical_base_contexts_v1.md`; embedded `state.context_id` must equal the manifest-level context ID. Transform action references with the recipe ID map; preserve a missing-key action reference as a fresh absent ID.
- Construct the two diagnostic contexts per surface by applying the surface recipe to a complete POS-VALID template and then setting only `path_clear=null`. This ordering permits H-ROLE/H-COMPOSED recipe construction without filling the diagnostic unknown field.
- Do not sort transformed object arrays; recipe record-order transformations are part of the declared surface realization.

## 5. Eligibility and validation

Before hashing or accepting any manifests:

1. Validate JSON structure against the three schemas. Also apply semantic checks schemas cannot express: unique context IDs/trace IDs, exact source contrast coverage, vector-to-contrast agreement, state/action context-ID agreement, relation resolution for complete contexts, and absence of role overlap.
2. Verify source count exactly 7 and no extras.
3. Verify every one of the 35 primary cell IDs is declared. Eligible cells contain exactly 3 primary contexts. Ineligible cells remain declared with count 0 and a concrete reason. Any failure to meet a required count triggers STOP; no substitution/rebalancing.
4. Verify there are 10 diagnostic records, exactly two per surface family; each has `endpoint_scope=DIAGNOSTIC_ONLY`, `diagnostic_reason=UNKNOWN_REQUIRED_STATE`, and a preserved null required field.
5. For every H-ROLE and H-COMPOSED primary context, verify the named recipe can construct a coordinate-slot permutation from at least two targets sharing closed-state/adjacency facts and distinct positions. If any required context is ineligible, STOP and request owner review.
6. Verify no duplicate IDs, no source/held-out/diagnostic role overlap, exact counts, and all contexts appear exactly once in the role map.
7. Verify manifests have no `observed_effect`, `expected_effect`, `effect`, `outcome`, `prediction`, `accuracy`, `score`, or label-valued field. Do not call `world.step` or any fitter/scorer.

## 6. Serialization and hashing

Serialize each JSON artifact as UTF-8, sorted object keys, compact separators, and arrays in their defined order. Compute SHA-256 over the exact serialized bytes. `manifest_hashes.json` records hashes for source, held-out, diagnostic, and role-map artifacts, plus this specification, canonical templates, count policy, schemas, transformation-cell manifest, resource vector, unknown-state policy, and frozen package manifest. Exclude the hash file itself from its own content; the run package records its digest separately.

## 7. Stop conditions

Stop manifest materialization without changing counts or definitions if a required base context cannot be built, a role recipe fails, counts do not match, an ID collides, a role overlaps, a schema/semantic check fails, or any outcome/effect would need to be generated or exposed. Report the exact blocker and preserve the already-frozen inputs.
