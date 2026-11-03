# WP3-AI-PILOT — Exploratory Only

**Not Independent Annotation**  
**Not Eligible For Family Qualification**  
**Not Eligible For Candidate Eligibility**  
**Not Eligible For Phase 2I Execution**  
**Not Eligible For WP3 Completion**

| Task ID | AI Pass B primary family | Secondary tags | Confidence | Training-pair evidence | Counter-hypothesis rationale |
|---|---|---|---|---|---|
| `45bbe264` | `SPATIAL_CHANGE` | `OBJ_RELATION` | MEDIUM | 1–3 | The demonstrations consistently extend rows/columns through marked cells; the geometric extension is primary. |
| `69889d6e` | `PATTERN_COMPLETION` | `COUNT_REPLICATION` | MEDIUM | 1–4 | The output fills out a repeated diagonal motif; repetition is present but completion best describes the result. |
| `36fdfd69` | `COLOR_ATTRIBUTE` | `OBJ_RELATION` | LOW | 1–3 | Several marked regions change color, but the rule selecting which cells change may be relational; not resolved confidently. |
| `c0f76784` | `REGION_TOPOLOGY` | `FRAME_BOUNDS` | HIGH | 1–3 | Enclosed interiors are filled without changing the outer bounds; enclosure is the governing feature. |
| `7447852a` | `PATTERN_COMPLETION` | `COUNT_REPLICATION` | LOW | 1–3 | The added cells appear to regularize a periodic arrangement rather than simply increase an object count. |
| `e9c9d9a1` | `COLOR_ATTRIBUTE` | `REGION_TOPOLOGY` | LOW | 1–3 | New colors occupy repeated bands/areas; the output could be read as region filling or color assignment. |
| `dc46ea44` | `SPATIAL_CHANGE` | `PATTERN_COMPLETION` | MEDIUM | 1–3 | Existing small shapes change location/orientation across examples; no new sequence is needed to explain it. |
| `aab50785` | `OBJ_RELATION` | `FRAME_BOUNDS` | LOW | 1–5 | The crop likely depends on selecting a meaningful subpattern, making target selection potentially primary. |
| `b74ca5d1` | `PATTERN_COMPLETION` | `SPATIAL_CHANGE` | LOW | 1–3 | Repeated local motifs appear completed/regularized, but geometric transformation is also plausible. |
| `1b59e163` | `SPATIAL_CHANGE` | `COUNT_REPLICATION` | LOW | 1–2 | The output relocates or duplicates an arrangement; the demonstrations do not clearly separate movement from replication. |
| `ff805c23` | `PATTERN_COMPLETION` | `FRAME_BOUNDS` | LOW | 1–3 | The crop preserves a smaller motif from a larger repeated design; pattern selection may be more central than crop itself. |
| `e9bb6954` | `SPATIAL_CHANGE` | `COMPOSITE_RULE` | LOW | 1–4 | Lines/regions are extended and several cells recolored; spatial construction is the tentative primary reading. |

This is a second rubric-conditioned output from the same AI assistant, not an independent coder's output.
