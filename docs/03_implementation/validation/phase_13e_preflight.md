# Phase 13E repository preflight

**Date:** 2026-10-31  
**Repository:** `/home/user/reasonflux`  
**Status:** audit and protocol design complete; no Phase 13E confirmation seed has been run.

## Existing components inspected

- Capability model, proposals, validity constraints, lifecycle, coverage, utility, portfolio, and representation failure detectors under `src/capability/`.
- Capability growth metrics/configuration under `src/evaluation/growth_metrics.py`, `growth_config.py`, `growth_components.py`, and `portfolio.py`.
- Alternative intelligence score/state pathway under `src/evaluation/intelligence.py` and `intelligence_state.py`.
- Skill candidate, promotion, library, monitoring, reuse, composition, task generator, solver, and invariant/trace pipelines.
- Phase 13C evidence and Phase 13D corrected analysis for limits on eligible skills and composition.
- Existing uncommitted repository state. No reset, cleanup, or edits to unrelated work were made. Phase 13C/13D evidence files remain untouched.

## Material preflight findings

1. Capability proposals only include eligible active/growing/core skills and proposals are not capabilities until validated. The Phase 13E runner therefore uses the existing library proposal and validation APIs and records accepted membership/evidence.
2. Two distinct intelligence formulas exist: `growth_metrics.compute_ig` (CGR/TG/UG/CCG/CompG with `GrowthConfig` weights) and `intelligence_score` / `compute_system_intelligence_state` (AG/SU/TS/CGR/CP/AD). The former is preregistered as the sole confirmatory IG pathway because it directly uses the specified capability-growth components. No switching after outcomes.
3. Prior synthetic evidence found reflection/rotation candidates but not reliable count/group source skills; Phase 13D composition/structural-transfer findings were unavailable. Phase 13E leaves those results unavailable unless newly learned and validated; it does not create learned count/group components by hand.
4. For composition, the confirmatory task is the repository's actual rotate-then-reflect task. Only learned reflection/rotation skills and the existing composition lifecycle may supply a composition. Higher-order emergent capabilities require multiple real promoted composition skills and may therefore be unavailable.
5. B4 is an explicit repeated-operation compression proxy, not canonical DreamCoder. A5 is a behavior-matched measurement ablation; it masks portfolio/growth outputs and is not a performance comparator.
6. CGM portfolio scores remain on the repository's existing scale; the roadmap's value above 1 is illustrative and will not be matched by rescaling.

## Frozen experiment locations

- Protocol: `experiments/phase13e/preregistration.md`
- Machine config: `experiments/phase13e/config.json`
- Modular runner/analysis: `experiments/phase13e/*.py` (all source modules below 350 lines; tests enforce a 400-line ceiling)
- Contract tests: `tests/test_phase13e_contracts.py`
- Output: `reports/experiments/PHASE-13E-CAP-GROWTH-V1/`

The independent seed block is 60–69. The tests exercise the protocol, deterministic task generation, IG pathway/weights, empty-portfolio behavior, confidence intervals, and source modularity; they do not run benchmark outcomes. Confirmation begins only through the explicit `--confirm` command after the runner/config hashes are written.
