# Phase 11E-3 notes — Intelligence Growth Model

## Assumptions

- Intelligence is the rate of converting experience into transferable capabilities,
  not raw skill count.
- IG = weighted sum of AG, SU, TS, CGR, CP, AD (`src/evaluation/intelligence.py`).
- IGR / IA / IE / Elasticity are finite-difference helpers over IG trajectories.
- System IntelligenceState builds on Phase 11E-2 `compute_system_capability_state`.
- Intelligence claims must pass evidence + intelligence-level robustness checks.

## Success criteria

- IG/IGR/IA/IE/Elasticity compute on synthetic trajectories.
- Maturity stages: emerging → developing → generalizing → compositional → adaptive.
- Audits flag skill hoarding, transfer collapse, fragmentation, composition
  failure, adaptation failure, and growth illusion.
- Opt-in `write_intel=True` syncs IG/IGR/stage into `CapabilityState`.
- New files ≤ 300 lines; `pytest tests/ -q` green.
