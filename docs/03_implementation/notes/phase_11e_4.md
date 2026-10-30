# Phase 11E-4 notes — Evaluation & Benchmarking Framework

## Assumptions

- Harness reuses CapU / CGR / IG APIs from 11E-1–3 (no formula re-derivation).
- Benchmarks L1–L4 are synthetic trajectories; L4 uses `arc_family` tags only
  (no ARC dataset download).
- Baselines A–D and ablations A1–A5 are config-driven transforms of scenario steps.
- Reports are JSON + Markdown under `reports/metrics/` (no interactive dashboard).

## Success criteria

- `run_evaluation_pipeline` runs layered evaluation and writes reports.
- Growth scenarios succeed; Baseline A fails success criteria.
- Ablation A5 weakens capability scores vs full ASFT path.
- Statistics (mean/median/variance/CI) attach to longitudinal series.
- All new modules ≤ 300 lines; `pytest tests/ -q` green.
