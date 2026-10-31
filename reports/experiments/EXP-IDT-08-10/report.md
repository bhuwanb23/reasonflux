# EXP-IDT-08-10

- **experiment_id**: `EXP-IDT-08-10`
- **claim**: `IDT`
- **dataset_version**: `synthetic-v1`
- **seeds**: `[0, 1, 2, 3, 4]`
## configuration

- `transfer_tasks`: `held-out synthetic batch`

## thresholds


## metrics

- `PEARSON`: `0.43123657749350297`
- `SPEARMAN`: `0.588095238095238`
- `TS`: `0.30238095238095236`
- `TU`: `0.14094047619047617`

## statistics

- `PEARSON`: `{'n': 5.0, 'mean': 0.43123657749350297, 'std': 0.04277244528112439, 'variance': 0.0018294820753267796, 'ci_low': 0.39374556508901903, 'ci_high': 0.4687275898979869, 'confidence': 0.95}`
- `SPEARMAN`: `{'n': 5.0, 'mean': 0.588095238095238, 'std': 0.07172557300662888, 'variance': 0.00514455782312925, 'ci_low': 0.5252261566191566, 'ci_high': 0.6509643195713194, 'confidence': 0.95}`
- `TS`: `{'n': 5.0, 'mean': 0.30238095238095236, 'std': 0.01304101327393254, 'variance': 0.00017006802721088472, 'ci_low': 0.2909502102943921, 'ci_high': 0.3138116944675126, 'confidence': 0.95}`
- `TU`: `{'n': 5.0, 'mean': 0.14094047619047617, 'std': 0.005281610375942676, 'variance': 2.7895408163265335e-05, 'ci_low': 0.13631102564541928, 'ci_high': 0.14556992673553307, 'confidence': 0.95}`

## raw_results

| experiment_id | claim | seed | dataset_version | configuration | metrics | n_transfer_records | pairs | transfer_utility_ranking | failure_cases | observations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXP-IDT-08-10 | IDT | 0 | synthetic-v1 | {'discovery_per_family': 6, 'transfer_per_family': 3} | {'PEARSON': 0.39999999999999997, 'SPEARMAN': 0.5357142857142857, 'TS': 0.2928571428571428, 'TU': 0.13708333333333333, 'cross_family_reuse': 2} | 7 | [{'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 9.0, 'ts': 0.25, 'tu': 0.25, 'source_family': 'reflection', 'target_family': 'reflection'}, {'invariant_id': 'INV-cd89c6e9697e31c5', 'is': 6.75, 'ts': 0.25, 'tu': 0.25, 'source_family': 'rotation', 'target_family': 'rotation'}, {'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 9.0, 'ts': 0.25, 'tu': 0.25, 'source_family': 'reflection', 'target_family': 'reflection'}, {'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 9.0, 'ts': 0.4, 'tu': 0.4, 'source_family': 'reflection', 'target_family': 'counting'}, {'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 9.0, 'ts': 0.4, 'tu': 0.4, 'source_family': 'reflection', 'target_family': 'grouping'}, {'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 9.0, 'ts': 0.25, 'tu': 0.25, 'source_family': 'reflection', 'target_family': 'reflection'}, {'invariant_id': 'INV-cd89c6e9697e31c5', 'is': 6.75, 'ts': 0.25, 'tu': 0.25, 'source_family': 'rotation', 'target_family': 'rotation'}] | [{'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 9.0, 'tu': 0.23249999999999998, 'coverage': 0.75}, {'invariant_id': 'INV-cd89c6e9697e31c5', 'is': 6.75, 'tu': 0.041666666666666664, 'coverage': 0.25}] | [] | {'credited_pairs': 7} |
| EXP-IDT-08-10 | IDT | 1 | synthetic-v1 | {'discovery_per_family': 6, 'transfer_per_family': 3} | {'PEARSON': 0.4780914437337574, 'SPEARMAN': 0.6666666666666666, 'TS': 0.31666666666666665, 'TU': 0.14672619047619048, 'cross_family_reuse': 4} | 9 | [{'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 10.5, 'ts': 0.25, 'tu': 0.25, 'source_family': 'reflection', 'target_family': 'reflection'}, {'invariant_id': 'INV-cd89c6e9697e31c5', 'is': 5.25, 'ts': 0.25, 'tu': 0.25, 'source_family': 'rotation', 'target_family': 'rotation'}, {'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 10.5, 'ts': 0.4, 'tu': 0.4, 'source_family': 'reflection', 'target_family': 'grouping'}, {'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 10.5, 'ts': 0.25, 'tu': 0.25, 'source_family': 'reflection', 'target_family': 'reflection'}, {'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 10.5, 'ts': 0.4, 'tu': 0.4, 'source_family': 'reflection', 'target_family': 'counting'}, {'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 10.5, 'ts': 0.4, 'tu': 0.4, 'source_family': 'reflection', 'target_family': 'grouping'}, {'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 10.5, 'ts': 0.25, 'tu': 0.25, 'source_family': 'reflection', 'target_family': 'reflection'}, {'invariant_id': 'INV-cd89c6e9697e31c5', 'is': 5.25, 'ts': 0.25, 'tu': 0.25, 'source_family': 'rotation', 'target_family': 'rotation'}, {'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 10.5, 'ts': 0.4, 'tu': 0.4, 'source_family': 'reflection', 'target_family': 'grouping'}] | [{'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 10.5, 'tu': 0.2517857142857143, 'coverage': 0.75}, {'invariant_id': 'INV-cd89c6e9697e31c5', 'is': 5.25, 'tu': 0.041666666666666664, 'coverage': 0.25}] | [] | {'credited_pairs': 9} |
| EXP-IDT-08-10 | IDT | 2 | synthetic-v1 | {'discovery_per_family': 6, 'transfer_per_family': 3} | {'PEARSON': 0.4, 'SPEARMAN': 0.5357142857142857, 'TS': 0.2928571428571428, 'TU': 0.13708333333333333, 'cross_family_reuse': 2} | 7 | [{'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 9.75, 'ts': 0.25, 'tu': 0.25, 'source_family': 'reflection', 'target_family': 'reflection'}, {'invariant_id': 'INV-cd89c6e9697e31c5', 'is': 6.0, 'ts': 0.25, 'tu': 0.25, 'source_family': 'rotation', 'target_family': 'rotation'}, {'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 9.75, 'ts': 0.25, 'tu': 0.25, 'source_family': 'reflection', 'target_family': 'reflection'}, {'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 9.75, 'ts': 0.4, 'tu': 0.4, 'source_family': 'reflection', 'target_family': 'counting'}, {'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 9.75, 'ts': 0.4, 'tu': 0.4, 'source_family': 'reflection', 'target_family': 'grouping'}, {'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 9.75, 'ts': 0.25, 'tu': 0.25, 'source_family': 'reflection', 'target_family': 'reflection'}, {'invariant_id': 'INV-cd89c6e9697e31c5', 'is': 6.0, 'ts': 0.25, 'tu': 0.25, 'source_family': 'rotation', 'target_family': 'rotation'}] | [{'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 9.75, 'tu': 0.23249999999999998, 'coverage': 0.75}, {'invariant_id': 'INV-cd89c6e9697e31c5', 'is': 6.0, 'tu': 0.041666666666666664, 'coverage': 0.25}] | [] | {'credited_pairs': 7} |
| EXP-IDT-08-10 | IDT | 3 | synthetic-v1 | {'discovery_per_family': 6, 'transfer_per_family': 3} | {'PEARSON': 0.4780914437337574, 'SPEARMAN': 0.6666666666666666, 'TS': 0.31666666666666665, 'TU': 0.14672619047619048, 'cross_family_reuse': 4} | 9 | [{'invariant_id': 'INV-02a30b2b5dd074b7', 'is': 10.5, 'ts': 0.25, 'tu': 0.25, 'source_family': 'reflection', 'target_family': 'reflection'}, {'invariant_id': 'INV-b2ef40c97323c287', 'is': 5.25, 'ts': 0.25, 'tu': 0.25, 'source_family': 'rotation', 'target_family': 'rotation'}, {'invariant_id': 'INV-02a30b2b5dd074b7', 'is': 10.5, 'ts': 0.4, 'tu': 0.4, 'source_family': 'reflection', 'target_family': 'grouping'}, {'invariant_id': 'INV-02a30b2b5dd074b7', 'is': 10.5, 'ts': 0.25, 'tu': 0.25, 'source_family': 'reflection', 'target_family': 'reflection'}, {'invariant_id': 'INV-02a30b2b5dd074b7', 'is': 10.5, 'ts': 0.4, 'tu': 0.4, 'source_family': 'reflection', 'target_family': 'counting'}, {'invariant_id': 'INV-02a30b2b5dd074b7', 'is': 10.5, 'ts': 0.4, 'tu': 0.4, 'source_family': 'reflection', 'target_family': 'grouping'}, {'invariant_id': 'INV-02a30b2b5dd074b7', 'is': 10.5, 'ts': 0.25, 'tu': 0.25, 'source_family': 'reflection', 'target_family': 'reflection'}, {'invariant_id': 'INV-b2ef40c97323c287', 'is': 5.25, 'ts': 0.25, 'tu': 0.25, 'source_family': 'rotation', 'target_family': 'rotation'}, {'invariant_id': 'INV-02a30b2b5dd074b7', 'is': 10.5, 'ts': 0.4, 'tu': 0.4, 'source_family': 'reflection', 'target_family': 'grouping'}] | [{'invariant_id': 'INV-02a30b2b5dd074b7', 'is': 10.5, 'tu': 0.2517857142857143, 'coverage': 0.75}, {'invariant_id': 'INV-b2ef40c97323c287', 'is': 5.25, 'tu': 0.041666666666666664, 'coverage': 0.25}] | [] | {'credited_pairs': 9} |
| EXP-IDT-08-10 | IDT | 4 | synthetic-v1 | {'discovery_per_family': 6, 'transfer_per_family': 3} | {'PEARSON': 0.39999999999999997, 'SPEARMAN': 0.5357142857142857, 'TS': 0.2928571428571428, 'TU': 0.13708333333333333, 'cross_family_reuse': 2} | 7 | [{'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 10.5, 'ts': 0.25, 'tu': 0.25, 'source_family': 'reflection', 'target_family': 'reflection'}, {'invariant_id': 'INV-cd89c6e9697e31c5', 'is': 5.25, 'ts': 0.25, 'tu': 0.25, 'source_family': 'rotation', 'target_family': 'rotation'}, {'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 10.5, 'ts': 0.25, 'tu': 0.25, 'source_family': 'reflection', 'target_family': 'reflection'}, {'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 10.5, 'ts': 0.4, 'tu': 0.4, 'source_family': 'reflection', 'target_family': 'counting'}, {'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 10.5, 'ts': 0.4, 'tu': 0.4, 'source_family': 'reflection', 'target_family': 'grouping'}, {'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 10.5, 'ts': 0.25, 'tu': 0.25, 'source_family': 'reflection', 'target_family': 'reflection'}, {'invariant_id': 'INV-cd89c6e9697e31c5', 'is': 5.25, 'ts': 0.25, 'tu': 0.25, 'source_family': 'rotation', 'target_family': 'rotation'}] | [{'invariant_id': 'INV-a4f872d69c07cbc0', 'is': 10.5, 'tu': 0.23249999999999998, 'coverage': 0.75}, {'invariant_id': 'INV-cd89c6e9697e31c5', 'is': 5.25, 'tu': 0.041666666666666664, 'coverage': 0.25}] | [] | {'credited_pairs': 7} |

## results

- `PEARSON`: `{'n': 5.0, 'mean': 0.43123657749350297, 'std': 0.04277244528112439, 'variance': 0.0018294820753267796, 'ci_low': 0.39374556508901903, 'ci_high': 0.4687275898979869, 'confidence': 0.95}`
- `SPEARMAN`: `{'n': 5.0, 'mean': 0.588095238095238, 'std': 0.07172557300662888, 'variance': 0.00514455782312925, 'ci_low': 0.5252261566191566, 'ci_high': 0.6509643195713194, 'confidence': 0.95}`
- `TS`: `{'n': 5.0, 'mean': 0.30238095238095236, 'std': 0.01304101327393254, 'variance': 0.00017006802721088472, 'ci_low': 0.2909502102943921, 'ci_high': 0.3138116944675126, 'confidence': 0.95}`
- `TU`: `{'n': 5.0, 'mean': 0.14094047619047617, 'std': 0.005281610375942676, 'variance': 2.7895408163265335e-05, 'ci_low': 0.13631102564541928, 'ci_high': 0.14556992673553307, 'confidence': 0.95}`

- **failure_cases**: `[]`
## observations


- **seed**: `None`
## metric_definitions

- `PEARSON`: `{'name': 'PEARSON', 'formula': 'corr(IS, TS)', 'interpretation': 'linear IS-transfer correlation', 'valid_range': '[-1, 1]', 'failure_condition': '<= 0'}`
- `SPEARMAN`: `{'name': 'SPEARMAN', 'formula': 'corr(rank(IS), rank(TS))', 'interpretation': 'rank IS-transfer correlation', 'valid_range': '[-1, 1]', 'failure_condition': '<= 0'}`
- `TS`: `{'name': 'TS', 'formula': 'performance_after - performance_before', 'interpretation': 'transfer score', 'valid_range': '(-inf, inf)', 'failure_condition': '<= 0'}`
- `TU`: `{'name': 'TU', 'formula': 'transfer benefit per reuse', 'interpretation': 'transfer utility', 'valid_range': '(-inf, inf)', 'failure_condition': '<= 0'}`

- **timestamp_utc**: `2026-10-31T10:31:11.215609+00:00`
- **record_schema**: `phase-13a-v1`
