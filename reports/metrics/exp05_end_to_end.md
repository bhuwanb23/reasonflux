# exp05_end_to_end

- **experiment**: `exp05_end_to_end`
- **contribution**: `ASFT`
## asft

- `name`: `asft_full`
- `capability_score`: `0.8309`
- `cgr`: `0.013333`
- `ig`: `0.278`
- `reuse_credited`: `27`
- `n_skills`: `6`

## baselines

| name | capability_score | cgr | ig | reuse_credited |
| --- | --- | --- | --- | --- |
| no_learning | 0.0 | 0.0 | 0.0 | 0 |
| skill_storage | 0.0 | 0.0 | 0.0 | 6 |
| random_skill_creation | 0.5201 | 0.0 | 0.078 | 6 |
| dreamcoder_like | 0.6832 | 0.0 | 0.1025 | 6 |

- **beats_all_baselines**: `True`
- **success**: `True`
## rounds

| round | n_traces | n_invariants | n_skills | n_new_skills | n_capabilities | capability_score | cgr | ig | reuse_credited |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 16 | 6 | 4 | 4 | 2 | 0.84313 | 0.0 | 0.276469 | 6 |
| 1 | 32 | 4 | 6 | 2 | 3 | 0.804241 | -0.038889 | 0.260914 | 7 |
| 2 | 48 | 4 | 6 | 0 | 3 | 0.817574 | 0.013333 | 0.275969 | 7 |
| 3 | 64 | 4 | 6 | 0 | 3 | 0.830907 | 0.013333 | 0.277969 | 7 |

## summary

- `success`: `True`
- `rounds`: `4`
- `n_traces`: `64`
- `n_invariants`: `4`
- `n_skills`: `6`
- `n_capabilities`: `3`
- `library_size`: `6`
- `reuse_attempts`: `32`
- `reuse_credited`: `27`
- `transfer_rate`: `0.8438`
- `mean_transfer_benefit`: `0.5042`
- `transfer_records`: `27`
- `initial_capability`: `0.84313`
- `trough_capability`: `0.804241`
- `final_capability`: `0.830907`
- `recovered_from_trough`: `True`
- `cgr`: `0.013333`
- `ig`: `0.277969`

