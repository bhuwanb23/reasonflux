# exp05_end_to_end

- **experiment**: `exp05_end_to_end`
- **contribution**: `ASFT`
## asft

- `name`: `asft_full`
- `capability_score`: `1.2302`
- `cgr`: `0.02`
- `ig`: `0.3395`
- `reuse_credited`: `21`
- `n_skills`: `6`

## baselines

| name | capability_score | cgr | ig | reuse_credited |
| --- | --- | --- | --- | --- |
| no_learning | 0.0 | 0.0 | 0.0 | 0 |
| skill_storage | 0.4387 | 0.0 | 0.0658 | 5 |
| random_skill_creation | 0.4626 | 0.0 | 0.0694 | 6 |
| dreamcoder_like | 0.782 | 0.0 | 0.1173 | 5 |

- **beats_all_baselines**: `True`
- **success**: `True`
## rounds

| round | n_traces | n_invariants | n_skills | n_new_skills | n_capabilities | capability_score | cgr | ig | reuse_credited |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 16 | 6 | 4 | 4 | 1 | 1.050167 | 0.0 | 0.307525 | 5 |
| 1 | 32 | 4 | 6 | 2 | 1 | 1.170167 | 0.12 | 0.355525 | 6 |
| 2 | 48 | 4 | 6 | 0 | 1 | 1.210167 | 0.04 | 0.341525 | 5 |
| 3 | 64 | 4 | 6 | 0 | 1 | 1.230167 | 0.02 | 0.339525 | 5 |

## summary

- `success`: `True`
- `rounds`: `4`
- `n_traces`: `64`
- `n_invariants`: `4`
- `n_skills`: `6`
- `n_capabilities`: `1`
- `library_size`: `6`
- `reuse_attempts`: `25`
- `reuse_credited`: `21`
- `transfer_rate`: `0.84`
- `mean_transfer_benefit`: `0.3143`
- `transfer_records`: `21`
- `initial_capability`: `1.050167`
- `trough_capability`: `1.050167`
- `final_capability`: `1.230167`
- `recovered_from_trough`: `True`
- `cgr`: `0.02`
- `ig`: `0.339525`

