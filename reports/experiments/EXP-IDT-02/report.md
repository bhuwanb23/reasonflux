# EXP-IDT-02

- **experiment_id**: `EXP-IDT-02`
- **claim**: `IDT`
- **dataset_version**: `synthetic-v1`
- **seeds**: `[0, 1, 2, 3, 4]`
## configuration

- `family`: `rotation`
- `per_family`: `6`

## thresholds


## metrics

- `IS`: `3.0`
- `discovery`: `1.0`

## statistics

- `IS`: `{'n': 5.0, 'mean': 3.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 3.0, 'ci_high': 3.0, 'confidence': 0.95}`
- `discovery`: `{'n': 5.0, 'mean': 1.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 1.0, 'ci_high': 1.0, 'confidence': 0.95}`

## raw_results

| experiment_id | experiment | claim | seed | dataset_version | configuration | thresholds | metrics | n_traces | n_candidates | n_ranked | expected_signature | expected_found | top_invariants | failure_cases | observations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXP-IDT-02 | rotation_discovery | IDT | 0 | synthetic-v1 | {'family': 'rotation', 'per_family': 6} | {'discovery': True} | {'IS': 3.0, 'discovery': 1.0, 'rank': 2.0} | 6 | 5 | 5 | ['find_rotation', 'apply_rotation'] | True | [{'rank': 1, 'invariant_id': 'INV-21fc62fe0f5c3383', 'signature': ['detect_object'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}, {'rank': 2, 'invariant_id': 'INV-489db88e598d48b3', 'signature': ['find_rotation'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}, {'rank': 3, 'invariant_id': 'INV-5851606191e6a4cf', 'signature': ['verify_output'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}, {'rank': 4, 'invariant_id': 'INV-6ba811ae991258da', 'signature': ['detect_object', 'find_rotation', 'apply_rotation', 'verify_output'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'moderate', 'families': ['rotation']}, {'rank': 5, 'invariant_id': 'INV-cd89c6e9697e31c5', 'signature': ['apply_rotation'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}] | [] | {'validated': 5} |
| EXP-IDT-02 | rotation_discovery | IDT | 1 | synthetic-v1 | {'family': 'rotation', 'per_family': 6} | {'discovery': True} | {'IS': 3.0, 'discovery': 1.0, 'rank': 2.0} | 6 | 5 | 5 | ['find_rotation', 'apply_rotation'] | True | [{'rank': 1, 'invariant_id': 'INV-21fc62fe0f5c3383', 'signature': ['detect_object'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}, {'rank': 2, 'invariant_id': 'INV-489db88e598d48b3', 'signature': ['find_rotation'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}, {'rank': 3, 'invariant_id': 'INV-5851606191e6a4cf', 'signature': ['verify_output'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}, {'rank': 4, 'invariant_id': 'INV-6ba811ae991258da', 'signature': ['detect_object', 'find_rotation', 'apply_rotation', 'verify_output'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'moderate', 'families': ['rotation']}, {'rank': 5, 'invariant_id': 'INV-cd89c6e9697e31c5', 'signature': ['apply_rotation'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}] | [] | {'validated': 5} |
| EXP-IDT-02 | rotation_discovery | IDT | 2 | synthetic-v1 | {'family': 'rotation', 'per_family': 6} | {'discovery': True} | {'IS': 3.0, 'discovery': 1.0, 'rank': 2.0} | 6 | 5 | 5 | ['find_rotation', 'apply_rotation'] | True | [{'rank': 1, 'invariant_id': 'INV-21fc62fe0f5c3383', 'signature': ['detect_object'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}, {'rank': 2, 'invariant_id': 'INV-489db88e598d48b3', 'signature': ['find_rotation'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}, {'rank': 3, 'invariant_id': 'INV-5851606191e6a4cf', 'signature': ['verify_output'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}, {'rank': 4, 'invariant_id': 'INV-6ba811ae991258da', 'signature': ['detect_object', 'find_rotation', 'apply_rotation', 'verify_output'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'moderate', 'families': ['rotation']}, {'rank': 5, 'invariant_id': 'INV-cd89c6e9697e31c5', 'signature': ['apply_rotation'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}] | [] | {'validated': 5} |
| EXP-IDT-02 | rotation_discovery | IDT | 3 | synthetic-v1 | {'family': 'rotation', 'per_family': 6} | {'discovery': True} | {'IS': 3.0, 'discovery': 1.0, 'rank': 2.0} | 6 | 5 | 5 | ['find_rotation', 'apply_rotation'] | True | [{'rank': 1, 'invariant_id': 'INV-21fc62fe0f5c3383', 'signature': ['detect_object'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}, {'rank': 2, 'invariant_id': 'INV-489db88e598d48b3', 'signature': ['find_rotation'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}, {'rank': 3, 'invariant_id': 'INV-5851606191e6a4cf', 'signature': ['verify_output'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}, {'rank': 4, 'invariant_id': 'INV-6ba811ae991258da', 'signature': ['detect_object', 'find_rotation', 'apply_rotation', 'verify_output'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'moderate', 'families': ['rotation']}, {'rank': 5, 'invariant_id': 'INV-cd89c6e9697e31c5', 'signature': ['apply_rotation'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}] | [] | {'validated': 5} |
| EXP-IDT-02 | rotation_discovery | IDT | 4 | synthetic-v1 | {'family': 'rotation', 'per_family': 6} | {'discovery': True} | {'IS': 3.0, 'discovery': 1.0, 'rank': 2.0} | 6 | 5 | 5 | ['find_rotation', 'apply_rotation'] | True | [{'rank': 1, 'invariant_id': 'INV-21fc62fe0f5c3383', 'signature': ['detect_object'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}, {'rank': 2, 'invariant_id': 'INV-489db88e598d48b3', 'signature': ['find_rotation'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}, {'rank': 3, 'invariant_id': 'INV-5851606191e6a4cf', 'signature': ['verify_output'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}, {'rank': 4, 'invariant_id': 'INV-6ba811ae991258da', 'signature': ['detect_object', 'find_rotation', 'apply_rotation', 'verify_output'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'moderate', 'families': ['rotation']}, {'rank': 5, 'invariant_id': 'INV-cd89c6e9697e31c5', 'signature': ['apply_rotation'], 'frequency': 3, 'consistency': 1.0, 'generality': 1.0, 'is': 3.0, 'confidence': 'weak', 'families': ['rotation']}] | [] | {'validated': 5} |

## results

- `IS`: `{'n': 5.0, 'mean': 3.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 3.0, 'ci_high': 3.0, 'confidence': 0.95}`
- `discovery`: `{'n': 5.0, 'mean': 1.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 1.0, 'ci_high': 1.0, 'confidence': 0.95}`

- **failure_cases**: `[]`
## observations


- **seed**: `None`
## metric_definitions

- `IS`: `{'name': 'IS', 'formula': 'frequency * consistency * generality', 'interpretation': 'invariant strength', 'valid_range': '[0, inf)', 'failure_condition': '<= 0'}`
- `discovery`: `{'name': 'DISCOVERY', 'formula': 'expected_invariant_found', 'interpretation': 'discovery success', 'valid_range': '[0, 1]', 'failure_condition': '< 1'}`

- **timestamp_utc**: `2026-10-31T12:10:03.173016+00:00`
- **record_schema**: `phase-13a-v1`
