# Baseline Interpretation

## Phase 13E paired outcomes

| Comparator | Final C_t difference | Mean all-task utility difference | Decision |
|---|---:|---:|---|
| B1 no learning | `+1.1785` (lower CI `+1.1428`) | `-0.0361` (lower CI `-0.0363`) | Fail: utility lower despite higher C_t |
| B2 skill storage only | `+1.1785` | `+0.0773` | Pass |
| B3 random skill creation | `+0.1603` | `+0.0776` | Pass |
| B4 compression proxy | `+0.3455` | `+0.0752` | Pass |

The preregistered gate requires positive lower confidence bounds on both final C_t and all-task utility. B1 is not a pass. A high CGM score against a no-learning arm with no capability portfolio is not, on its own, an external-performance validation.

## Phase 13F independent protocol

The joint task-utility/CGR gate fails B1 (utility `-0.0363`, CGR `+0.2872`) and B3 (both contrasts zero), and passes B2 (utility `+0.0749`, CGR `+0.2872`) and B4 (utility `+0.0749`, CGR `+0.0814`). Comparator and endpoint matter. B4 is a compression proxy, not canonical DreamCoder.

**Conclusion:** baseline superiority is mixed; do not pool Phase 13E and 13F estimates or call CGM universally superior.
