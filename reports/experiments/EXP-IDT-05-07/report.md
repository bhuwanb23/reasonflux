# EXP-IDT-05-07

- **experiment_id**: `EXP-IDT-05-07`
- **claim**: `IDT`
- **dataset_version**: `synthetic-v1`
- **seeds**: `[0, 1, 2, 3, 4]`
## configuration

- `per_family`: `6`

## thresholds


## metrics

- `IP`: `1.0`
- `IR`: `1.0`
- `confidence`: `0.66`
- `IS`: `5.85625`

## statistics

- `IP`: `{'n': 5.0, 'mean': 1.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 1.0, 'ci_high': 1.0, 'confidence': 0.95}`
- `IR`: `{'n': 5.0, 'mean': 1.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 1.0, 'ci_high': 1.0, 'confidence': 0.95}`
- `confidence`: `{'n': 5.0, 'mean': 0.66, 'std': 0.0, 'variance': 0.0, 'ci_low': 0.66, 'ci_high': 0.66, 'confidence': 0.95}`
- `IS`: `{'n': 5.0, 'mean': 5.85625, 'std': 0.23758222260935266, 'variance': 0.0564453125, 'ci_low': 5.648003826642619, 'ci_high': 6.064496173357381, 'confidence': 0.95}`

## raw_results

| experiment_id | claim | seed | dataset_version | configuration | thresholds | metrics | detected_invariants | valid_invariants | expected_invariants | confidence_distribution | failure_cases | observations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXP-IDT-05-07 | IDT | 0 | synthetic-v1 | {'families': ['reflection', 'rotation', 'counting', 'grouping'], 'per_family': 6} | {'precision': 0.7, 'recall': 0.75} | {'IP': 1.0, 'IR': 1.0, 'confidence': 0.66, 'IS': 5.75} | 6 | 6 | 4 | [0.66, 0.66, 0.66, 0.66, 0.66, 0.66] | [] | {'expected_families_found': 4.0, 'validated': 4} |
| EXP-IDT-05-07 | IDT | 1 | synthetic-v1 | {'families': ['reflection', 'rotation', 'counting', 'grouping'], 'per_family': 6} | {'precision': 0.7, 'recall': 0.75} | {'IP': 1.0, 'IR': 1.0, 'confidence': 0.66, 'IS': 5.75} | 6 | 6 | 4 | [0.66, 0.66, 0.66, 0.66, 0.66, 0.66] | [] | {'expected_families_found': 4.0, 'validated': 4} |
| EXP-IDT-05-07 | IDT | 2 | synthetic-v1 | {'families': ['reflection', 'rotation', 'counting', 'grouping'], 'per_family': 6} | {'precision': 0.7, 'recall': 0.75} | {'IP': 1.0, 'IR': 1.0, 'confidence': 0.66, 'IS': 5.75} | 6 | 6 | 4 | [0.66, 0.66, 0.66, 0.66, 0.66, 0.66] | [] | {'expected_families_found': 4.0, 'validated': 4} |
| EXP-IDT-05-07 | IDT | 3 | synthetic-v1 | {'families': ['reflection', 'rotation', 'counting', 'grouping'], 'per_family': 6} | {'precision': 0.7, 'recall': 0.75} | {'IP': 1.0, 'IR': 1.0, 'confidence': 0.66, 'IS': 6.28125} | 8 | 8 | 4 | [0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66] | [] | {'expected_families_found': 4.0, 'validated': 6} |
| EXP-IDT-05-07 | IDT | 4 | synthetic-v1 | {'families': ['reflection', 'rotation', 'counting', 'grouping'], 'per_family': 6} | {'precision': 0.7, 'recall': 0.75} | {'IP': 1.0, 'IR': 1.0, 'confidence': 0.66, 'IS': 5.75} | 6 | 6 | 4 | [0.66, 0.66, 0.66, 0.66, 0.66, 0.66] | [] | {'expected_families_found': 4.0, 'validated': 4} |

## results

- `IP`: `{'n': 5.0, 'mean': 1.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 1.0, 'ci_high': 1.0, 'confidence': 0.95}`
- `IR`: `{'n': 5.0, 'mean': 1.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 1.0, 'ci_high': 1.0, 'confidence': 0.95}`
- `confidence`: `{'n': 5.0, 'mean': 0.66, 'std': 0.0, 'variance': 0.0, 'ci_low': 0.66, 'ci_high': 0.66, 'confidence': 0.95}`
- `IS`: `{'n': 5.0, 'mean': 5.85625, 'std': 0.23758222260935266, 'variance': 0.0564453125, 'ci_low': 5.648003826642619, 'ci_high': 6.064496173357381, 'confidence': 0.95}`

- **failure_cases**: `[]`
## observations


- **seed**: `None`
## metric_definitions

- `IP`: `{'name': 'IP', 'formula': 'valid_invariants / detected_invariants', 'interpretation': 'invariant precision', 'valid_range': '[0, 1]', 'failure_condition': '< 0.70'}`
- `IR`: `{'name': 'IR', 'formula': 'discovered_expected / expected_invariants', 'interpretation': 'invariant recall', 'valid_range': '[0, 1]', 'failure_condition': '< 0.75'}`
- `confidence`: `{'name': 'CONFIDENCE', 'formula': 'mean evidence confidence', 'interpretation': 'invariant confidence', 'valid_range': '[0, 1]', 'failure_condition': '< 0.70'}`
- `IS`: `{'name': 'IS', 'formula': 'frequency * consistency * generality', 'interpretation': 'invariant strength', 'valid_range': '[0, inf)', 'failure_condition': '<= 0'}`

- **timestamp_utc**: `2026-10-31T12:10:03.303231+00:00`
- **record_schema**: `phase-13a-v1`
