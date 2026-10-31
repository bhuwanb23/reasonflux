# EXP-IDT-BASELINES

- **experiment_id**: `EXP-IDT-BASELINES`
- **claim**: `IDT`
- **dataset_version**: `synthetic-v1`
- **seeds**: `[0, 1, 2, 3, 4]`
## configuration

- `comparison`: `top-k valid invariant rate`

## thresholds


## metrics

- `ASFT`: `0.14094047619047617`
- `frequency_only`: `0.12010714285714286`
- `random_pattern`: `0.03767857142857143`

## statistics

- `ASFT`: `{'n': 5.0, 'mean': 0.14094047619047617, 'std': 0.005281610375942676, 'variance': 2.7895408163265335e-05, 'ci_low': 0.13631102564541928, 'ci_high': 0.14556992673553307, 'confidence': 0.95}`
- `frequency_only`: `{'n': 5.0, 'mean': 0.12010714285714286, 'std': 0.005281610375942675, 'variance': 2.7895408163265332e-05, 'ci_low': 0.11547769231208595, 'ci_high': 0.12473659340219977, 'confidence': 0.95}`
- `random_pattern`: `{'n': 5.0, 'mean': 0.03767857142857143, 'std': 0.05013162945794644, 'variance': 0.0025131802721088435, 'ci_low': -0.0062629317871515724, 'ci_high': 0.08162007464429444, 'confidence': 0.95}`

## raw_results

| experiment_id | claim | seed | dataset_version | configuration | metrics | comparison | asft_outperforms_random | asft_outperforms_frequency | failure_cases | observations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXP-IDT-BASELINES | IDT | 0 | synthetic-v1 | {'top_k': 4} | {'ASFT': 0.13708333333333333, 'frequency_only': 0.11624999999999999, 'random_pattern': 0.020833333333333332, 'ASFT_advantage': 0.020833333333333343, 'ASFT_valid_top_rate': 1.0, 'frequency_valid_top_rate': 1.0} | [{'baseline': 'ASFT transfer-aware', 'score': 0.13708333333333333}, {'baseline': 'frequency-only', 'score': 0.11624999999999999}, {'baseline': 'random pattern', 'score': 0.020833333333333332}, {'baseline': 'no-transfer validation', 'score': 0.11624999999999999}] | True | True | [] | {'n_candidates': 6} |
| EXP-IDT-BASELINES | IDT | 1 | synthetic-v1 | {'top_k': 4} | {'ASFT': 0.14672619047619048, 'frequency_only': 0.12589285714285714, 'random_pattern': 0.020833333333333332, 'ASFT_advantage': 0.020833333333333343, 'ASFT_valid_top_rate': 1.0, 'frequency_valid_top_rate': 1.0} | [{'baseline': 'ASFT transfer-aware', 'score': 0.14672619047619048}, {'baseline': 'frequency-only', 'score': 0.12589285714285714}, {'baseline': 'random pattern', 'score': 0.020833333333333332}, {'baseline': 'no-transfer validation', 'score': 0.12589285714285714}] | True | True | [] | {'n_candidates': 6} |
| EXP-IDT-BASELINES | IDT | 2 | synthetic-v1 | {'top_k': 4} | {'ASFT': 0.13708333333333333, 'frequency_only': 0.11624999999999999, 'random_pattern': 0.020833333333333332, 'ASFT_advantage': 0.020833333333333343, 'ASFT_valid_top_rate': 1.0, 'frequency_valid_top_rate': 1.0} | [{'baseline': 'ASFT transfer-aware', 'score': 0.13708333333333333}, {'baseline': 'frequency-only', 'score': 0.11624999999999999}, {'baseline': 'random pattern', 'score': 0.020833333333333332}, {'baseline': 'no-transfer validation', 'score': 0.11624999999999999}] | True | True | [] | {'n_candidates': 6} |
| EXP-IDT-BASELINES | IDT | 3 | synthetic-v1 | {'top_k': 4} | {'ASFT': 0.14672619047619048, 'frequency_only': 0.12589285714285714, 'random_pattern': 0.12589285714285714, 'ASFT_advantage': 0.020833333333333343, 'ASFT_valid_top_rate': 1.0, 'frequency_valid_top_rate': 1.0} | [{'baseline': 'ASFT transfer-aware', 'score': 0.14672619047619048}, {'baseline': 'frequency-only', 'score': 0.12589285714285714}, {'baseline': 'random pattern', 'score': 0.12589285714285714}, {'baseline': 'no-transfer validation', 'score': 0.12589285714285714}] | True | True | [] | {'n_candidates': 8} |
| EXP-IDT-BASELINES | IDT | 4 | synthetic-v1 | {'top_k': 4} | {'ASFT': 0.13708333333333333, 'frequency_only': 0.11624999999999999, 'random_pattern': 0.0, 'ASFT_advantage': 0.020833333333333343, 'ASFT_valid_top_rate': 1.0, 'frequency_valid_top_rate': 1.0} | [{'baseline': 'ASFT transfer-aware', 'score': 0.13708333333333333}, {'baseline': 'frequency-only', 'score': 0.11624999999999999}, {'baseline': 'random pattern', 'score': 0.0}, {'baseline': 'no-transfer validation', 'score': 0.11624999999999999}] | True | True | [] | {'n_candidates': 6} |

## results

- `ASFT`: `{'n': 5.0, 'mean': 0.14094047619047617, 'std': 0.005281610375942676, 'variance': 2.7895408163265335e-05, 'ci_low': 0.13631102564541928, 'ci_high': 0.14556992673553307, 'confidence': 0.95}`
- `frequency_only`: `{'n': 5.0, 'mean': 0.12010714285714286, 'std': 0.005281610375942675, 'variance': 2.7895408163265332e-05, 'ci_low': 0.11547769231208595, 'ci_high': 0.12473659340219977, 'confidence': 0.95}`
- `random_pattern`: `{'n': 5.0, 'mean': 0.03767857142857143, 'std': 0.05013162945794644, 'variance': 0.0025131802721088435, 'ci_low': -0.0062629317871515724, 'ci_high': 0.08162007464429444, 'confidence': 0.95}`

- **failure_cases**: `[]`
## observations


- **seed**: `None`
## metric_definitions

- `ASFT`: `{'name': 'ASFT', 'formula': 'valid top-k invariants / k', 'interpretation': 'ASFT ranking quality', 'valid_range': '[0, 1]', 'failure_condition': '< 0.70'}`
- `FREQUENCY_ONLY`: `{'name': 'FREQUENCY_ONLY', 'formula': 'valid top-k frequency-ranked invariants / k', 'interpretation': 'frequency-only ranking quality', 'valid_range': '[0, 1]', 'failure_condition': '< 0.70'}`
- `RANDOM_PATTERN`: `{'name': 'RANDOM_PATTERN', 'formula': 'valid top-k random patterns / k', 'interpretation': 'random-pattern quality', 'valid_range': '[0, 1]', 'failure_condition': '< 0.70'}`

- **timestamp_utc**: `2026-10-31T10:31:11.468338+00:00`
- **record_schema**: `phase-13a-v1`
