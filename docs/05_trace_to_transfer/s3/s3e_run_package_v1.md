# T2T-S3-E Run Package v1 — Authorization Review Copy

**Readiness:** `READY FOR AUTHORIZATION REVIEW`  
**Execution authorization:** `NOT AUTHORIZED`  
**Package:** `T2T-S3-RA-v0.2.0`  
**S3-RB:** PASS, reference `S3-RB-IND-2026-11-05-001`  
**Run performed:** no. **Outcomes generated/exposed:** no. **Claim N assigned:** no.

This document freezes the context-only run inputs and rules for a later authorization decision. It is not an authorization to execute S3.

## 1. Frozen artifact inventory and counts

| Artifact / role | Count | SHA-256 |
|---|---:|---|
| `source_manifest.json` | 7 contexts | `1fd28ae53e0572397c1bddf375c229586a8f91e31576886dcffe29173b8c97be` |
| `heldout_manifest.json` | 105 primary contexts; 35 cells × 3 | `be64f2882958da7db39c536d00ea6ea90ac6607447fb1ad1d5d2ae95428fb003` |
| `diagnostic_manifest.json` | 10 diagnostic contexts; 5 surfaces × 2 | `ff658b783be09a06802f45881c88226de3e49a8e78314bdb62d1b935de641d52` |
| `context_role_map.json` | 122 unique assignments | `859541c5f3ca2f0375111cbff379c29fe2b2a82895e6abe0582821a63b62318b` |
| `manifest_hashes.json` | hash inventory | `93abee614afe00b43a8a89cbda89dc72c783d05f51cbb2220bdda8402804372d` |

All 35 primary cells are represented and eligible in the generated manifests. No count substitutions or rebalancing occurred. `manifest_hashes.json` lists SHA-256 hashes for the generated artifacts and all frozen construction inputs; its own digest is recorded above, outside that file.

## 2. Frozen role and count policy

- **Source:** exactly 7 contexts, one per frozen R4 feature contrast; no additional source contexts.
- **Held-out primary:** 3 contexts per eligible cell; 35 cells; 105 contexts in this manifest.
- **Diagnostics:** exactly 2 unknown-required-state contexts per surface family; 10 total. These are not primary-scored contexts.
- **Roles:** source, held-out primary, and held-out diagnostic context IDs are pairwise disjoint. Every context ID has exactly one role-map row.
- **H-ROLE/H-COMPOSED:** each required context passed the frozen role-slot eligibility constructor. If a later integrity recheck fails, STOP; do not substitute, rebalance, or alter counts.

The exact base-state/template definitions are in `canonical_base_contexts_v1.md`; counts are frozen in `counts_decision_required.md`; the generation and validation rules are in `manifest_generation_spec.md`.

## 3. Outcome and predictor-access boundary

The manifests contain state/action inputs and evaluator metadata only. They contain no observed/expected effect, outcome label, prediction, score, or `Delta_N`. No world transition was evaluated while constructing them.

At a later authorized run, the predictor adapter must pass only the declared observable state/action interface to each arm. Do **not** pass `context_id`, role, cell ID, semantic-family name, template ID, replicate index, or any other manifest metadata to an arm. `context_id` is logging/provenance only. The evaluator keeps the role map and cell metadata private to the evaluation/reporting layer. Held-out outcomes remain unavailable until all arm predictions for the context have been recorded.

Unknown-required-state policy is frozen in `unknown_state_policy_v1.md`: diagnostic-only, excluded from primary accuracy, separately accounted, no hidden-state labels, and no conversion to success/no-effect. The 10 diagnostic records preserve `path_clear=null`; no outcome label is attached.

## 4. Resource vector and environment

Apply `resource_vector_v1.md` without variation:

- one prediction opportunity per arm/context;
- one evaluator-owned world access per context, shared for scoring and only after predictions are committed;
- identical observation/action/predicate/source-manifest access for I0 and R0–R4;
- held-out prediction access only; no adaptive refit, retries, post-holdout updates, extra source traces, predicates, or transformation metadata.

Use the existing deterministic world, transformations, arms, and scorer. The recorded workspace runtime fingerprint is Python 3.13.16 / pytest 9.0.3. Capture and compare exact runtime/dependency hashes before any authorized execution; do not introduce environment variation without owner review.

## 5. Planned execution protocol — inactive until authorization

If and only if a separate explicit authorization is issued:

1. Verify all files against `manifest_hashes.json` and verify the recorded S3-RA package freeze.
2. Load the exact source/held-out/diagnostic manifests and role map. Do not expose held-out cell/semantic metadata to predictors.
3. Generate source training labels only under the authorized run, then fit source-only arms according to the frozen rules. Do not refit or update from held-out data.
4. For each primary held-out context, record exactly one prediction per arm before the evaluator obtains its one world result. No retries.
5. Keep diagnostic-only records outside the primary endpoint and report their inventory/handling separately without hidden labels.
6. Apply the already-frozen scorer and N decision rule only under that authorization. Any mismatch, role overlap, label leakage, altered code, or unapproved configuration change triggers STOP and invalidates the run.

No step in this section has been performed.

## 6. Authorization decision record

- Decision: **UNSET — no S3 execution authorization granted**
- Authorized run/version, if later approved: **UNSET**
- Owner / date / authorization reference: **UNSET**

Only the project owner may complete this record. A separate explicit approval is required before any source-label generation for fitting, arm fitting, held-out prediction/evaluation, outcome exposure, scoring, or Claim N classification.

## 7. Readiness gate

**S3-E package:** complete for authorization review.  
**S3 execution:** not authorized.  
**Claim N:** unresolved; no outcomes exist.
