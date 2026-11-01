# EXP-IDT-BASELINES

- **experiment_id**: `EXP-IDT-BASELINES`
- **claim**: `IDT`
- **dataset_version**: `synthetic-v1`
- **seeds**: `[0, 1, 2, 3, 4]`
## configuration

- `comparison`: `top-k unique-semantic mean transfer utility`

## thresholds


## metrics

- `ASFT`: `0.09580853174603174`
- `frequency_only`: `0.09580853174603174`
- `no_transfer`: `0.09580853174603174`
- `random_pattern`: `0.06311337425595238`
- `ASFT_advantage`: `0.0`
- `ASFT_minus_no_transfer`: `0.0`
- `ASFT_minus_random`: `0.03269515749007936`

## statistics

- `ASFT`: `{'n': 5.0, 'mean': 0.09580853174603174, 'std': 0.0007360996628500603, 'variance': 5.418427136479724e-07, 'ci_low': 0.09516332379943283, 'ci_high': 0.09645373969263064, 'confidence': 0.95}`
- `frequency_only`: `{'n': 5.0, 'mean': 0.09580853174603174, 'std': 0.0007360996628500603, 'variance': 5.418427136479724e-07, 'ci_low': 0.09516332379943283, 'ci_high': 0.09645373969263064, 'confidence': 0.95}`
- `no_transfer`: `{'n': 5.0, 'mean': 0.09580853174603174, 'std': 0.0007360996628500603, 'variance': 5.418427136479724e-07, 'ci_low': 0.09516332379943283, 'ci_high': 0.09645373969263064, 'confidence': 0.95}`
- `random_pattern`: `{'n': 5.0, 'mean': 0.06311337425595238, 'std': 0.007711731781729573, 'variance': 5.947080707333797e-05, 'ci_low': 0.056353867522385616, 'ci_high': 0.06987288098951916, 'confidence': 0.95}`
- `ASFT_advantage`: `{'n': 5.0, 'mean': 0.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 0.0, 'ci_high': 0.0, 'confidence': 0.95}`
- `ASFT_minus_no_transfer`: `{'n': 5.0, 'mean': 0.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 0.0, 'ci_high': 0.0, 'confidence': 0.95}`
- `ASFT_minus_random`: `{'n': 5.0, 'mean': 0.03269515749007936, 'std': 0.007866042753993163, 'variance': 6.187462860764834e-05, 'ci_low': 0.025800393711065267, 'ci_high': 0.039589921269093456, 'confidence': 0.95}`

## raw_results

| experiment_id | claim | seed | dataset_version | configuration | metrics | ranking_diagnostics | comparison | asft_outperforms_random | asft_outperforms_frequency | asft_outperforms_no_transfer | failure_cases | observations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXP-IDT-BASELINES | IDT | 0 | synthetic-v1 | {'top_k': 2, 'score': 'mean transfer utility', 'candidate_level': 'shared validated semantic-consolidated pool'} | {'ASFT': 0.09692460317460319, 'frequency_only': 0.09692460317460319, 'no_transfer': 0.09692460317460319, 'random_pattern': 0.06489955357142858, 'ASFT_advantage': 0.0, 'ASFT_minus_no_transfer': 0.0, 'ASFT_minus_random': 0.03202504960317461, 'ASFT_valid_top_rate': 1.0, 'frequency_valid_top_rate': 1.0, 'no_transfer_valid_top_rate': 1.0} | {'asft_order': ['reflection', 'rotation', 'count_objects', 'group_by_color'], 'frequency_order': ['reflection', 'rotation', 'count_objects', 'group_by_color'], 'no_transfer_order': ['reflection', 'rotation', 'count_objects', 'group_by_color'], 'asft_equals_frequency_order': True, 'asft_equals_no_transfer_order': True, 'distinct_semantic_candidates': 4, 'held_out_utility_by_semantic_candidate': {'reflection': 0.1660714285714286, 'rotation': 0.027777777777777776, 'count_objects': 0.0, 'group_by_color': 0.0}, 'mean_transfer_utility_at_k': {'1': {'ASFT': 0.1660714285714286, 'frequency_only': 0.1660714285714286, 'no_transfer': 0.1660714285714286}, '2': {'ASFT': 0.09692460317460319, 'frequency_only': 0.09692460317460319, 'no_transfer': 0.09692460317460319}, '3': {'ASFT': 0.06461640211640213, 'frequency_only': 0.06461640211640213, 'no_transfer': 0.06461640211640213}, '4': {'ASFT': 0.048462301587301596, 'frequency_only': 0.048462301587301596, 'no_transfer': 0.048462301587301596}}} | [{'baseline': 'ASFT transfer-aware', 'score': 0.09692460317460319}, {'baseline': 'frequency-only', 'score': 0.09692460317460319}, {'baseline': 'no-transfer validation', 'score': 0.09692460317460319}, {'baseline': 'random pattern', 'score': 0.06489955357142858}] | True | False | False | [] | {'n_candidates': 6} |
| EXP-IDT-BASELINES | IDT | 1 | synthetic-v1 | {'top_k': 2, 'score': 'mean transfer utility', 'candidate_level': 'shared validated semantic-consolidated pool'} | {'ASFT': 0.09513888888888888, 'frequency_only': 0.09513888888888888, 'no_transfer': 0.09513888888888888, 'random_pattern': 0.06453993055555556, 'ASFT_advantage': 0.0, 'ASFT_minus_no_transfer': 0.0, 'ASFT_minus_random': 0.03059895833333333, 'ASFT_valid_top_rate': 1.0, 'frequency_valid_top_rate': 1.0, 'no_transfer_valid_top_rate': 1.0} | {'asft_order': ['reflection', 'rotation', 'count_objects', 'group_by_color'], 'frequency_order': ['reflection', 'rotation', 'count_objects', 'group_by_color'], 'no_transfer_order': ['reflection', 'rotation', 'count_objects', 'group_by_color'], 'asft_equals_frequency_order': True, 'asft_equals_no_transfer_order': True, 'distinct_semantic_candidates': 4, 'held_out_utility_by_semantic_candidate': {'reflection': 0.1625, 'rotation': 0.027777777777777776, 'count_objects': 0.0, 'group_by_color': 0.0}, 'mean_transfer_utility_at_k': {'1': {'ASFT': 0.1625, 'frequency_only': 0.1625, 'no_transfer': 0.1625}, '2': {'ASFT': 0.09513888888888888, 'frequency_only': 0.09513888888888888, 'no_transfer': 0.09513888888888888}, '3': {'ASFT': 0.06342592592592593, 'frequency_only': 0.06342592592592593, 'no_transfer': 0.06342592592592593}, '4': {'ASFT': 0.04756944444444444, 'frequency_only': 0.04756944444444444, 'no_transfer': 0.04756944444444444}}} | [{'baseline': 'ASFT transfer-aware', 'score': 0.09513888888888888}, {'baseline': 'frequency-only', 'score': 0.09513888888888888}, {'baseline': 'no-transfer validation', 'score': 0.09513888888888888}, {'baseline': 'random pattern', 'score': 0.06453993055555556}] | True | False | False | [] | {'n_candidates': 6} |
| EXP-IDT-BASELINES | IDT | 2 | synthetic-v1 | {'top_k': 2, 'score': 'mean transfer utility', 'candidate_level': 'shared validated semantic-consolidated pool'} | {'ASFT': 0.0959201388888889, 'frequency_only': 0.0959201388888889, 'no_transfer': 0.0959201388888889, 'random_pattern': 0.04969618055555556, 'ASFT_advantage': 0.0, 'ASFT_minus_no_transfer': 0.0, 'ASFT_minus_random': 0.046223958333333336, 'ASFT_valid_top_rate': 1.0, 'frequency_valid_top_rate': 1.0, 'no_transfer_valid_top_rate': 1.0} | {'asft_order': ['reflection', 'rotation', 'count_objects', 'group_by_color'], 'frequency_order': ['reflection', 'rotation', 'count_objects', 'group_by_color'], 'no_transfer_order': ['reflection', 'rotation', 'count_objects', 'group_by_color'], 'asft_equals_frequency_order': True, 'asft_equals_no_transfer_order': True, 'distinct_semantic_candidates': 4, 'held_out_utility_by_semantic_candidate': {'reflection': 0.1640625, 'rotation': 0.027777777777777776, 'count_objects': 0.0, 'group_by_color': 0.0}, 'mean_transfer_utility_at_k': {'1': {'ASFT': 0.1640625, 'frequency_only': 0.1640625, 'no_transfer': 0.1640625}, '2': {'ASFT': 0.0959201388888889, 'frequency_only': 0.0959201388888889, 'no_transfer': 0.0959201388888889}, '3': {'ASFT': 0.06394675925925926, 'frequency_only': 0.06394675925925926, 'no_transfer': 0.06394675925925926}, '4': {'ASFT': 0.04796006944444445, 'frequency_only': 0.04796006944444445, 'no_transfer': 0.04796006944444445}}} | [{'baseline': 'ASFT transfer-aware', 'score': 0.0959201388888889}, {'baseline': 'frequency-only', 'score': 0.0959201388888889}, {'baseline': 'no-transfer validation', 'score': 0.0959201388888889}, {'baseline': 'random pattern', 'score': 0.04969618055555556}] | True | False | False | [] | {'n_candidates': 6} |
| EXP-IDT-BASELINES | IDT | 3 | synthetic-v1 | {'top_k': 2, 'score': 'mean transfer utility', 'candidate_level': 'shared validated semantic-consolidated pool'} | {'ASFT': 0.0959201388888889, 'frequency_only': 0.0959201388888889, 'no_transfer': 0.0959201388888889, 'random_pattern': 0.06768120659722222, 'ASFT_advantage': 0.0, 'ASFT_minus_no_transfer': 0.0, 'ASFT_minus_random': 0.02823893229166667, 'ASFT_valid_top_rate': 1.0, 'frequency_valid_top_rate': 1.0, 'no_transfer_valid_top_rate': 1.0} | {'asft_order': ['reflection', 'rotation', 'count_objects', 'group_by_color'], 'frequency_order': ['reflection', 'rotation', 'count_objects', 'group_by_color'], 'no_transfer_order': ['reflection', 'rotation', 'count_objects', 'group_by_color'], 'asft_equals_frequency_order': True, 'asft_equals_no_transfer_order': True, 'distinct_semantic_candidates': 4, 'held_out_utility_by_semantic_candidate': {'reflection': 0.1640625, 'rotation': 0.027777777777777776, 'count_objects': 0.0, 'group_by_color': 0.0}, 'mean_transfer_utility_at_k': {'1': {'ASFT': 0.1640625, 'frequency_only': 0.1640625, 'no_transfer': 0.1640625}, '2': {'ASFT': 0.0959201388888889, 'frequency_only': 0.0959201388888889, 'no_transfer': 0.0959201388888889}, '3': {'ASFT': 0.06394675925925926, 'frequency_only': 0.06394675925925926, 'no_transfer': 0.06394675925925926}, '4': {'ASFT': 0.04796006944444445, 'frequency_only': 0.04796006944444445, 'no_transfer': 0.04796006944444445}}} | [{'baseline': 'ASFT transfer-aware', 'score': 0.0959201388888889}, {'baseline': 'frequency-only', 'score': 0.0959201388888889}, {'baseline': 'no-transfer validation', 'score': 0.0959201388888889}, {'baseline': 'random pattern', 'score': 0.06768120659722222}] | True | False | False | [] | {'n_candidates': 8} |
| EXP-IDT-BASELINES | IDT | 4 | synthetic-v1 | {'top_k': 2, 'score': 'mean transfer utility', 'candidate_level': 'shared validated semantic-consolidated pool'} | {'ASFT': 0.09513888888888888, 'frequency_only': 0.09513888888888888, 'no_transfer': 0.09513888888888888, 'random_pattern': 0.06875, 'ASFT_advantage': 0.0, 'ASFT_minus_no_transfer': 0.0, 'ASFT_minus_random': 0.02638888888888888, 'ASFT_valid_top_rate': 1.0, 'frequency_valid_top_rate': 1.0, 'no_transfer_valid_top_rate': 1.0} | {'asft_order': ['reflection', 'rotation', 'count_objects', 'group_by_color'], 'frequency_order': ['reflection', 'rotation', 'count_objects', 'group_by_color'], 'no_transfer_order': ['reflection', 'rotation', 'count_objects', 'group_by_color'], 'asft_equals_frequency_order': True, 'asft_equals_no_transfer_order': True, 'distinct_semantic_candidates': 4, 'held_out_utility_by_semantic_candidate': {'reflection': 0.1625, 'rotation': 0.027777777777777776, 'count_objects': 0.0, 'group_by_color': 0.0}, 'mean_transfer_utility_at_k': {'1': {'ASFT': 0.1625, 'frequency_only': 0.1625, 'no_transfer': 0.1625}, '2': {'ASFT': 0.09513888888888888, 'frequency_only': 0.09513888888888888, 'no_transfer': 0.09513888888888888}, '3': {'ASFT': 0.06342592592592593, 'frequency_only': 0.06342592592592593, 'no_transfer': 0.06342592592592593}, '4': {'ASFT': 0.04756944444444444, 'frequency_only': 0.04756944444444444, 'no_transfer': 0.04756944444444444}}} | [{'baseline': 'ASFT transfer-aware', 'score': 0.09513888888888888}, {'baseline': 'frequency-only', 'score': 0.09513888888888888}, {'baseline': 'no-transfer validation', 'score': 0.09513888888888888}, {'baseline': 'random pattern', 'score': 0.06875}] | True | False | False | [] | {'n_candidates': 6} |

## results

- `ASFT`: `{'n': 5.0, 'mean': 0.09580853174603174, 'std': 0.0007360996628500603, 'variance': 5.418427136479724e-07, 'ci_low': 0.09516332379943283, 'ci_high': 0.09645373969263064, 'confidence': 0.95}`
- `frequency_only`: `{'n': 5.0, 'mean': 0.09580853174603174, 'std': 0.0007360996628500603, 'variance': 5.418427136479724e-07, 'ci_low': 0.09516332379943283, 'ci_high': 0.09645373969263064, 'confidence': 0.95}`
- `no_transfer`: `{'n': 5.0, 'mean': 0.09580853174603174, 'std': 0.0007360996628500603, 'variance': 5.418427136479724e-07, 'ci_low': 0.09516332379943283, 'ci_high': 0.09645373969263064, 'confidence': 0.95}`
- `random_pattern`: `{'n': 5.0, 'mean': 0.06311337425595238, 'std': 0.007711731781729573, 'variance': 5.947080707333797e-05, 'ci_low': 0.056353867522385616, 'ci_high': 0.06987288098951916, 'confidence': 0.95}`
- `ASFT_advantage`: `{'n': 5.0, 'mean': 0.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 0.0, 'ci_high': 0.0, 'confidence': 0.95}`
- `ASFT_minus_no_transfer`: `{'n': 5.0, 'mean': 0.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 0.0, 'ci_high': 0.0, 'confidence': 0.95}`
- `ASFT_minus_random`: `{'n': 5.0, 'mean': 0.03269515749007936, 'std': 0.007866042753993163, 'variance': 6.187462860764834e-05, 'ci_low': 0.025800393711065267, 'ci_high': 0.039589921269093456, 'confidence': 0.95}`

- **failure_cases**: `[]`
## observations


- **seed**: `None`
## metric_definitions

- `ASFT`: `{'name': 'ASFT', 'formula': 'mean TU of top-k transfer-aware invariants', 'interpretation': 'ASFT transfer-aware ranking utility', 'valid_range': '(-inf, inf)', 'failure_condition': '<= baseline'}`
- `frequency_only`: `{'name': 'FREQUENCY_ONLY', 'formula': 'mean TU of top-k frequency-ranked invariants', 'interpretation': 'frequency-only ranking utility', 'valid_range': '(-inf, inf)', 'failure_condition': '>= ASFT'}`
- `no_transfer`: `{'name': 'NO_TRANSFER', 'formula': 'mean TU of top-k IS-ranked invariants', 'interpretation': 'transfer-blind intrinsic-strength ranking utility', 'valid_range': '(-inf, inf)', 'failure_condition': '>= ASFT'}`
- `random_pattern`: `{'name': 'RANDOM_PATTERN', 'formula': 'mean TU of top-k random patterns', 'interpretation': 'random-pattern ranking utility', 'valid_range': '(-inf, inf)', 'failure_condition': '>= ASFT'}`
- `ASFT_advantage`: `{'name': 'ASFT_ADVANTAGE', 'formula': 'ASFT TU - frequency-only TU', 'interpretation': 'transfer-aware ranking advantage', 'valid_range': '(-inf, inf)', 'failure_condition': '<= 0'}`
- `ASFT_minus_no_transfer`: `{'name': 'ASFT_MINUS_NO_TRANSFER', 'formula': 'ASFT TU - no-transfer TU', 'interpretation': 'transfer-aware versus no-transfer paired advantage', 'valid_range': '(-inf, inf)', 'failure_condition': '<= 0'}`
- `ASFT_minus_random`: `{'name': 'ASFT_MINUS_RANDOM', 'formula': 'ASFT TU - random-pattern TU', 'interpretation': 'transfer-aware versus random-pattern paired advantage', 'valid_range': '(-inf, inf)', 'failure_condition': '<= 0'}`

- **timestamp_utc**: `2026-10-31T13:42:26.928715+00:00`
- **record_schema**: `phase-13a-v1`
