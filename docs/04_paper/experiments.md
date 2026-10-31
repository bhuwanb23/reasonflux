# ASFT Experiments

Maps Phase 9C experiment matrix to repository folders. Enable flags live in `configs/experiments.yaml`.

Claim → module → metric → experiment → artifact traceability:
[claim_traceability.md](claim_traceability.md). Run readiness per experiment:
[v0_1_readiness.md](../00_project/v0_1_readiness.md).

| Folder | Contribution | Question | Runnable now |
| --- | --- | --- | --- |
| `experiments/exp01_invariants/` | IDT | Can invariant extraction find reusable patterns? Does high IS predict transfer? | No — runner not implemented |
| `experiments/exp02_skills/` | SCT | Does create-when-SCV>0 reduce future reasoning cost vs always-search? | No — runner not implemented |
| `experiments/exp03_transfer/` | Transfer | How much does solving Task A improve Task B? | No — runner not implemented |
| `experiments/exp04_growth/` | CGM | Do TS / CGR / IG track capability growth over time? | Yes — `run.py` |
| `experiments/exp05_end_to_end/` | ASFT | Does the full pipeline produce coherent paper-facing evidence? | No — `run_full_asft_pipeline` is a stub |

Only `exp04_growth` is `enabled: true` in `configs/experiments.yaml`. Experiments
above run on synthetic scenario data, not on learned traces.

## Baselines (separate code)

| Folder | Role |
| --- | --- |
| `baselines/no_learning/` | Independent per-task solving |
| `baselines/skill_storage/` | Store skills without IDT / SCV |
| `baselines/dreamcoder_like/` | Compression-style primitive growth |
| `baselines/random_skill_creation/` | Skills without SCV decision |

## Outputs

Generated artifacts go under `reports/{figures,tables,metrics,logs}/` for paper assembly in `papers/`.
