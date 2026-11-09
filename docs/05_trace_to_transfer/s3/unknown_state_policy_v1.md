# S3-E Unknown-Required-State Policy v1

**Owner decision:** APPROVED  
**Policy:** `UNKNOWN_REQUIRED_STATE = DIAGNOSTIC_ONLY = EXCLUDED_FROM_PRIMARY_CLAIM_N_ENDPOINT`  
**Status:** frozen for S3-E; execution remains unauthorized.

## Rule

A context is `UNKNOWN_REQUIRED_STATE` when a field required by the frozen world rule is unknown or incomplete, so the simulator cannot assign an exact `SUCCESS` or `NO_EFFECT` effect without using hidden state. Under the current `RelationalUnlockWorld` contract, `step` returns no effect for such a state.

Unknown state is not a prediction error. Do not coerce it to success, no-effect, wrong, or any other hidden-state-derived label.

## Handling

- Exclude these contexts from the primary Claim N accuracy denominator.
- If included in a manifest, mark them `DIAGNOSTIC_ONLY` with reason `UNKNOWN_REQUIRED_STATE` and report their count/reasons separately from all primary cells.
- Preserve full accounting: report planned diagnostic count, generated diagnostic count, and any excluded/ineligible diagnostic context with its reason. Do not silently drop them.
- Do not infer, impute, access, or attach hidden-state labels or exact effect labels.
- Do not fit or update I0/R0–R4 from diagnostic contexts.
- Primary complete contexts remain in the fixed primary denominator. For those, wrong, abstained, invalid, and missing predictions score zero under the existing scorer.

## Stop condition

If the world contract is changed so an unknown-required context receives an exact outcome, or if any hidden-state label is created/accessed, stop. The policy, world, scoring contract, and version must be prospectively revised and re-reviewed before any execution authorization.
