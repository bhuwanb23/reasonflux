# exp01_invariants

- **experiment_id**: `exp01_invariants`
- **seed**: `0`
- **dataset_version**: `synthetic-v1`
## configuration

- `per_family`: `6`

## dataset


## thresholds

- `n_validated`: `1`
- `mean_is`: `0.0`

## metrics

- `IS`: `7.875`

## results

- `experiment`: `exp01_invariants`
- `experiment_id`: `EXP-01`
- `seed`: `0`
- `dataset_version`: `synthetic-v1`
- `configuration`: `{'per_family': 6}`
- `thresholds`: `{'n_validated': 1, 'mean_is': 0.0}`
- `contribution`: `IDT`
- `n_traces`: `24`
- `n_candidates`: `6`
- `n_validated`: `4`
- `is_summary`: `{'n': 4.0, 'mean': 7.875, 'max': 9.0, 'min': 6.75, 'above_threshold': 4.0, 'threshold': 5.0}`
- `metrics`: `{'IS': 7.875}`
- `reflection_found`: `True`
- `rotation_found`: `True`
- `invariants`: `[{'signature': 'apply_reflection', 'frequency': 12, 'consistency': 1.0, 'generality': 0.75, 'is': 9.0, 'families': 'counting, grouping, reflection'}, {'signature': 'find_symmetry', 'frequency': 12, 'consistency': 1.0, 'generality': 0.75, 'is': 9.0, 'families': 'counting, grouping, reflection'}, {'signature': 'find_rotation', 'frequency': 9, 'consistency': 1.0, 'generality': 0.75, 'is': 6.75, 'families': 'counting, grouping, rotation'}, {'signature': 'apply_rotation', 'frequency': 9, 'consistency': 1.0, 'generality': 0.75, 'is': 6.75, 'families': 'counting, grouping, rotation'}]`

- **failure_cases**: `[]`
## observations


## metric_definitions

- `IS`: `{'name': 'IS', 'formula': 'frequency * consistency * generality', 'interpretation': 'invariant strength', 'valid_range': '[0, inf)', 'failure_condition': '<= 0'}`

- **timestamp_utc**: `2026-10-31T12:31:08.612021+00:00`
- **record_schema**: `phase-13a-v1`
