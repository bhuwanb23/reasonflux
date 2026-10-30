# ASFT Experiments

Maps Phase 9C experiment matrix to repository folders. Enable flags live in `configs/experiments.yaml`.

| Folder | Contribution | Question |
| --- | --- | --- |
| `experiments/exp01_invariants/` | IDT | Can invariant extraction find reusable patterns? Does high IS predict transfer? |
| `experiments/exp02_skills/` | SCT | Does create-when-SCV>0 reduce future reasoning cost vs always-search? |
| `experiments/exp03_transfer/` | Transfer | How much does solving Task A improve Task B? |
| `experiments/exp04_growth/` | CGM | Do TS / CGR / IG track capability growth over time? |
| `experiments/exp05_end_to_end/` | ASFT | Does the full pipeline produce coherent paper-facing evidence? |

## Baselines (separate code)

| Folder | Role |
| --- | --- |
| `baselines/no_learning/` | Independent per-task solving |
| `baselines/skill_storage/` | Store skills without IDT / SCV |
| `baselines/dreamcoder_like/` | Compression-style primitive growth |
| `baselines/random_skill_creation/` | Skills without SCV decision |

## Outputs

Generated artifacts go under `reports/{figures,tables,metrics,logs}/` for paper assembly in `papers/`.
