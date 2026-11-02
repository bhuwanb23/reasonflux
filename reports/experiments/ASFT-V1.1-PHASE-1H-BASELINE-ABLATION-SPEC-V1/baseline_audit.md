# Phase 1H.1 — Historical Baseline Audit

**Scope:** read-only synthesis of Phases 13B–13G and Phase 14F (with Phase 14F's source lineage for 13C–13G and 13B). No experiment was rerun; no historic baseline, endpoint, or outcome was changed.

## Executive finding

Several alternatives **survive**: memory/retrieval is a sharp comparator-specific counterexample; frequency-only tied informed ranking in 13B and 13F; a compression proxy narrowly defeats ASFT's corrected transfer-utility gate in 13D; random/heuristic controls tie in low-pressure pools. These are not universal victories. Results change by phase, comparator implementation, candidate pool, opportunity count, endpoint, and coverage.

The main weaknesses were **comparison identification**, not simply “bad baselines”: 13B rankers produced the same order; 13C selected all 44 candidates and RANDOM_CREATE degenerated to ALWAYS_CREATE; 13F selectors constructed the same four candidates; 13G had a budget/config mismatch and no activated learned mechanism chain. A comparison with no decision divergence cannot establish a selection advantage.

## Phase-by-phase audit

### Phase 13B / EXP-IDT-BASELINES — ranking alternatives

- Corrected informed ASFT, frequency-only, and no-transfer ranking all score `0.0958085` mean top-k transfer utility; the pre-correction record is separately `0.143130` for the same tied arms. Do not combine these versions.
- The rank orders are identical across the five saved seeds, so the primary ranking comparison did not exercise a distinct selected set.
- Random-pattern comparison is lower (`0.063113` corrected mean), so ASFT beats that comparator on this endpoint, but it does not pass the strict all-control gate because frequency/no-transfer tie it.
- Interpretation: random is informative for a floor; frequency and no-transfer are the surviving, stronger controls for the ranking claim.

### Phase 13C — skill-creation alternatives

- Primary mean net value: SCT `.345`, ALWAYS_CREATE `.345`, RANDOM_CREATE `.345`, NEVER_CREATE `0`, MEMORY_ONLY `1.325`.
- All 44 eligible confirmation candidates were selected by SCT/always/random. All calibration candidates had positive SCV10; frozen random-create probability was `1.0`. Random-create therefore degenerated to always-create, and the selection-policy comparison had no action divergence.
- MEMORY_ONLY applied all 440 eligible opportunities and was correct on 418; SCT applied 223/440 and was correct on 201. This is a strong alternative explanation in that simulator/cost protocol, but opportunities attempted differ. The net-value gap (`1.325` vs `.345`) combines application frequency and correctness; it is not a matched per-attempt effect.
- Source qualification: Phase 13C MEMORY_ONLY retrieves raw trace exemplars, selects a matching trace, extracts one macro operation, and applies it to eligible tasks. It is not literal full-solution exact episodic replay, nor a learned skill store.
- NEVER_CREATE is a floor/control, not a demanding substitute for learning. It must not be the sole comparator.

### Corrected Phase 13D — transfer-policy baselines

ASFT-minus comparator transfer-utility differences: B1 no-learning `+.018909`; B2 memory-only `+.015273`; B3 random skills `+.728909`; B4 compression proxy `−.001091` (95% CI `[−.003273,0]`). The strict all-baseline superiority gate fails on B4. Preserve this corrected analysis and its posthoc provenance; do not promote it to a rerun or pool it with other phases.

### Phase 13E — capability/growth baselines

Under its joint final-C_t and task-utility rule, ASFT passes B2 skill-storage-only, B3 random-skill-creation, and B4 compression proxy; it fails B1 because all-task utility is lower by `−.0361`, despite final C_t difference `+1.1785`. C_t is an internal score, not independent evidence that the baseline was inferior in external capability.

### Phase 13F — task-utility/CGR baselines and ablations

The joint task-utility/CGR gate passes B2 and B4, fails B1 (lower utility despite higher CGR), and fails B3 because both contrasts are exactly zero. ASFT, no-SCV, and random-SCV each construct four skills from the same four-item common pool. Equal action sets mean SCV did not show incremental selection value in that pool. B4 remains a proxy, not canonical DreamCoder.

### Phase 13G — bounded ARC baselines

All five arms have the same holdout exact accuracy `1/200=.005`; the learned invariant/skill/capability chain did not activate because coverage was very low. The config says three candidates per task while discovery defaults to ten, and the same holdout was reused after attempt 01 produced predictions in memory. This is not a fair mechanism-ranking result or pristine replication. The B2 nearest-episode memory policy's `1/200` transfer success is not ASFT skill transfer and not exact-answer replay.

## Which alternatives survive?

| Alternative | Audit status | Boundary |
|---|---|---|
| Memory/retrieval | **Survives; strong in 13C** | Distinct B2 implementations must remain separate; 13C raw-trace exemplar result has unmatched application counts. |
| Frequency-only | **Survives** | Ties ASFT in corrected 13B and 13F frequency-only; 13C frequency statistic is at least as predictive as SCV10 of shadow value, not necessarily a policy win. |
| Compression | **Survives; mixed** | B4 slightly wins the corrected 13D transfer endpoint and loses selected 13E/13F joint criteria; proxy only. |
| Random | **Survives as a necessary control** | Sometimes beaten, but ties when selection degenerates; same eligible pool and repeated seeds required. |
| No-learning | **Mixed, not universally weak** | Can be a floor, but ASFT has lower task utility than B1 in 13E/13F. Keep as a diagnostic, never the only baseline. |
| Hybrid memory+frequency | **Not historically tested as a stable common implementation** | Mandatory v1.1 control; future evidence required. |
| Oracle | **Analysis-only upper bound** | Not a feasible opponent; cannot support a deployable-system win. |

## Cross-phase rule

Do not pool Phase 13C MEMORY_ONLY with Phase 13D MEMORY_ONLY, Phase 13E skill-storage-only, Phase 13F B2_MEMORY_SKILL_STORE, or Phase 13G nearest-episode B2. Do not pool endpoints: 13B top-k transfer utility, 13C net value, 13D transfer utility, 13E joint C_t/task utility, 13F joint task utility/CGR, and 13G exact accuracy are non-interchangeable. Report each baseline implementation, opportunity count, activation path, and endpoint under its own evidence boundary.