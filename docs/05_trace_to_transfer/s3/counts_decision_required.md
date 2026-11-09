# S3-E Count Decision — Frozen Owner Values

**Status:** owner count policy frozen; context manifests are being materialized under this policy.  
**No execution:** S3 remains unrun; no outcomes or `Delta_N` are generated.

## 1. Source manifest — exact count

Freeze **exactly 7 source contexts**, with no additional source contexts: one for each required R4 contrast.

| Required source contrast | Frozen count |
|---|---:|
| ALL_TRUE | 1 |
| ONLY_FALSE_KEY_IS_KEY | 1 |
| ONLY_FALSE_TARGET_IS_TARGET | 1 |
| ONLY_FALSE_TARGET_CLOSED | 1 |
| ONLY_FALSE_AGENT_ADJACENT | 1 |
| ONLY_FALSE_PATH_CLEAR | 1 |
| ONLY_FALSE_KEY_UNLOCKS_SELECTED_TARGET | 1 |
| **Total** | **7** |

This is the deterministic minimum identifiability set, not a statistical sample-size or power choice. Additional source contexts are fixed at **0**.

## 2. Held-out primary manifest — uniform per-cell count

The frozen suite has five surface families crossed with seven scored semantic families: **35 primary cells**. Freeze **3 contexts per eligible cell**, giving target total **105 primary held-out contexts**.

| Surface | Scored semantic families | Contexts per eligible cell | Target contexts |
|---|---|---:|---:|
| H-ID | POS-VALID; NEG-WRONG-RELATION; NEG-TARGET-OPEN; NEG-NONADJACENT; NEG-BLOCKED-PATH; NEG-WRONG-ROLE; NEG-ABSENT-KEY | 3 | 21 |
| H-APP | same seven | 3 | 21 |
| H-LAYOUT | same seven | 3 | 21 |
| H-ROLE | same seven | 3 | 21 |
| H-COMPOSED | same seven | 3 | 21 |
| **Total** | **35 cells** | **3 per eligible cell** | **105** |

If any cell is ineligible, keep it in the manifest with planned count 0, denominator 0, and a specific reason. Do not substitute, rebalance, lower counts, or silently omit it. If the required count cannot be achieved before outcome exposure, STOP and request owner review. No ineligibility has been assumed; it must be checked during context construction.

## 3. Diagnostic manifest — exact count

Freeze **2 `UNKNOWN_REQUIRED_STATE` diagnostic contexts per held-out surface family**:

| Surface family | Diagnostic count |
|---|---:|
| H-ID | 2 |
| H-APP | 2 |
| H-LAYOUT | 2 |
| H-ROLE | 2 |
| H-COMPOSED | 2 |
| **Total** | **10** |

These contexts are diagnostic-only, outside the primary endpoint and denominator. Preserve the unknown required field; do not generate, infer, or attach an effect label.

## 4. Eligibility, denominator, and stop rules

- H-ROLE/H-COMPOSED eligibility requires at least two targets sharing closed-state and agent-adjacency facts and occupying distinct coordinate slots.
- The canonical templates in `canonical_base_contexts_v1.md` are designed to satisfy this condition for all seven primary semantic families and all three replicates. The manifest builder must verify each recipe application. If any required context fails, stop before outcome exposure; do not repair by changing counts or cell definitions.
- All 35 primary cell IDs must be declared. The number of context rows per eligible cell must equal 3. An ineligible cell must remain declared with denominator 0 and reason.
- Primary denominator is the union of all eligible primary held-out context IDs. Diagnostic contexts are reported separately and never added to it.
- Source count is 7; held-out primary target count is 105, less only if a cell is explicitly marked ineligible under the frozen policy; diagnostic count is 10.

## 5. Manifest implications

`source_manifest.json` must contain exactly the seven source contrasts and no extras. `heldout_manifest.json` must declare all 35 cells and contain three contexts per eligible cell. `diagnostic_manifest.json` must contain ten diagnostic-only contexts. `context_role_map.json` must map every one of these context IDs exactly once, with no overlap between source and held-out/diagnostic roles.

All manifests contain context state/action and metadata only. They contain no observed effect, expected effect, prediction, score, or outcome field. The count freeze does not authorize fitting, evaluation, outcome exposure, `Delta_N`, or Claim N classification.
