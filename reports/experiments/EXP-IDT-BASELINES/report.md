# EXP-IDT-BASELINES

- **experiment_id**: `EXP-IDT-BASELINES`
- **claim**: `IDT`
- **dataset_version**: `synthetic-v1`
- **seeds**: `[0, 1, 2, 3, 4]`
## configuration

- `comparison`: `top-k unique-semantic mean transfer utility`

## thresholds


## metrics

- `ASFT`: `0.14312996031746034`
- `frequency_only`: `0.14312996031746034`
- `no_transfer`: `0.14312996031746034`
- `random_pattern`: `0.09451404389880953`

## statistics

- `ASFT`: `{'n': 5.0, 'mean': 0.14312996031746034, 'std': 0.0022082989885501576, 'variance': 4.876584422831649e-06, 'ci_low': 0.14119433647766366, 'ci_high': 0.145065584157257, 'confidence': 0.95}`
- `frequency_only`: `{'n': 5.0, 'mean': 0.14312996031746034, 'std': 0.0022082989885501576, 'variance': 4.876584422831649e-06, 'ci_low': 0.14119433647766366, 'ci_high': 0.145065584157257, 'confidence': 0.95}`
- `no_transfer`: `{'n': 5.0, 'mean': 0.14312996031746034, 'std': 0.0022082989885501576, 'variance': 4.876584422831649e-06, 'ci_low': 0.14119433647766366, 'ci_high': 0.145065584157257, 'confidence': 0.95}`
- `random_pattern`: `{'n': 5.0, 'mean': 0.09451404389880953, 'std': 0.012682027032437882, 'variance': 0.00016083380965148522, 'ci_low': 0.0833979613446762, 'ci_high': 0.10563012645294287, 'confidence': 0.95}`

## raw_results

| experiment_id | claim | seed | dataset_version | configuration | metrics | comparison | asft_outperforms_random | asft_outperforms_frequency | asft_outperforms_no_transfer | failure_cases | observations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXP-IDT-BASELINES | IDT | 0 | synthetic-v1 | {'top_k': 2, 'score': 'mean transfer utility', 'candidate_level': 'ASFT semantic-consolidated; baselines raw-pattern'} | {'ASFT': 0.13978174603174603, 'frequency_only': 0.13978174603174603, 'no_transfer': 0.13978174603174603, 'random_pattern': 0.09436383928571429, 'ASFT_advantage': 0.0, 'ASFT_valid_top_rate': 1.0, 'frequency_valid_top_rate': 1.0, 'no_transfer_valid_top_rate': 1.0} | [{'baseline': 'ASFT transfer-aware', 'score': 0.13978174603174603}, {'baseline': 'frequency-only', 'score': 0.13978174603174603}, {'baseline': 'no-transfer validation', 'score': 0.13978174603174603}, {'baseline': 'random pattern', 'score': 0.09436383928571429}] | True | False | False | [] | {'n_candidates': 6} |
| EXP-IDT-BASELINES | IDT | 1 | synthetic-v1 | {'top_k': 2, 'score': 'mean transfer utility', 'candidate_level': 'ASFT semantic-consolidated; baselines raw-pattern'} | {'ASFT': 0.1451388888888889, 'frequency_only': 0.1451388888888889, 'no_transfer': 0.1451388888888889, 'random_pattern': 0.09891493055555556, 'ASFT_advantage': 0.0, 'ASFT_valid_top_rate': 1.0, 'frequency_valid_top_rate': 1.0, 'no_transfer_valid_top_rate': 1.0} | [{'baseline': 'ASFT transfer-aware', 'score': 0.1451388888888889}, {'baseline': 'frequency-only', 'score': 0.1451388888888889}, {'baseline': 'no-transfer validation', 'score': 0.1451388888888889}, {'baseline': 'random pattern', 'score': 0.09891493055555556}] | True | False | False | [] | {'n_candidates': 6} |
| EXP-IDT-BASELINES | IDT | 2 | synthetic-v1 | {'top_k': 2, 'score': 'mean transfer utility', 'candidate_level': 'ASFT semantic-consolidated; baselines raw-pattern'} | {'ASFT': 0.1427951388888889, 'frequency_only': 0.1427951388888889, 'no_transfer': 0.1427951388888889, 'random_pattern': 0.07313368055555555, 'ASFT_advantage': 0.0, 'ASFT_valid_top_rate': 1.0, 'frequency_valid_top_rate': 1.0, 'no_transfer_valid_top_rate': 1.0} | [{'baseline': 'ASFT transfer-aware', 'score': 0.1427951388888889}, {'baseline': 'frequency-only', 'score': 0.1427951388888889}, {'baseline': 'no-transfer validation', 'score': 0.1427951388888889}, {'baseline': 'random pattern', 'score': 0.07313368055555555}] | True | False | False | [] | {'n_candidates': 6} |
| EXP-IDT-BASELINES | IDT | 3 | synthetic-v1 | {'top_k': 2, 'score': 'mean transfer utility', 'candidate_level': 'ASFT semantic-consolidated; baselines raw-pattern'} | {'ASFT': 0.1427951388888889, 'frequency_only': 0.1427951388888889, 'no_transfer': 0.1427951388888889, 'random_pattern': 0.09990776909722222, 'ASFT_advantage': 0.0, 'ASFT_valid_top_rate': 1.0, 'frequency_valid_top_rate': 1.0, 'no_transfer_valid_top_rate': 1.0} | [{'baseline': 'ASFT transfer-aware', 'score': 0.1427951388888889}, {'baseline': 'frequency-only', 'score': 0.1427951388888889}, {'baseline': 'no-transfer validation', 'score': 0.1427951388888889}, {'baseline': 'random pattern', 'score': 0.09990776909722222}] | True | False | False | [] | {'n_candidates': 8} |
| EXP-IDT-BASELINES | IDT | 4 | synthetic-v1 | {'top_k': 2, 'score': 'mean transfer utility', 'candidate_level': 'ASFT semantic-consolidated; baselines raw-pattern'} | {'ASFT': 0.1451388888888889, 'frequency_only': 0.1451388888888889, 'no_transfer': 0.1451388888888889, 'random_pattern': 0.10625000000000001, 'ASFT_advantage': 0.0, 'ASFT_valid_top_rate': 1.0, 'frequency_valid_top_rate': 1.0, 'no_transfer_valid_top_rate': 1.0} | [{'baseline': 'ASFT transfer-aware', 'score': 0.1451388888888889}, {'baseline': 'frequency-only', 'score': 0.1451388888888889}, {'baseline': 'no-transfer validation', 'score': 0.1451388888888889}, {'baseline': 'random pattern', 'score': 0.10625000000000001}] | True | False | False | [] | {'n_candidates': 6} |

## results

- `ASFT`: `{'n': 5.0, 'mean': 0.14312996031746034, 'std': 0.0022082989885501576, 'variance': 4.876584422831649e-06, 'ci_low': 0.14119433647766366, 'ci_high': 0.145065584157257, 'confidence': 0.95}`
- `frequency_only`: `{'n': 5.0, 'mean': 0.14312996031746034, 'std': 0.0022082989885501576, 'variance': 4.876584422831649e-06, 'ci_low': 0.14119433647766366, 'ci_high': 0.145065584157257, 'confidence': 0.95}`
- `no_transfer`: `{'n': 5.0, 'mean': 0.14312996031746034, 'std': 0.0022082989885501576, 'variance': 4.876584422831649e-06, 'ci_low': 0.14119433647766366, 'ci_high': 0.145065584157257, 'confidence': 0.95}`
- `random_pattern`: `{'n': 5.0, 'mean': 0.09451404389880953, 'std': 0.012682027032437882, 'variance': 0.00016083380965148522, 'ci_low': 0.0833979613446762, 'ci_high': 0.10563012645294287, 'confidence': 0.95}`

- **failure_cases**: `[]`
## observations


- **seed**: `None`
## metric_definitions

- `ASFT`: `{'name': 'ASFT', 'formula': 'mean TU of top-k transfer-aware invariants', 'interpretation': 'ASFT transfer-aware ranking utility', 'valid_range': '(-inf, inf)', 'failure_condition': '<= baseline'}`
- `frequency_only`: `{'name': 'FREQUENCY_ONLY', 'formula': 'mean TU of top-k frequency-ranked invariants', 'interpretation': 'frequency-only ranking utility', 'valid_range': '(-inf, inf)', 'failure_condition': '>= ASFT'}`
- `no_transfer`: `{'name': 'NO_TRANSFER', 'formula': 'mean TU of top-k IS-ranked invariants', 'interpretation': 'transfer-blind intrinsic-strength ranking utility', 'valid_range': '(-inf, inf)', 'failure_condition': '>= ASFT'}`
- `random_pattern`: `{'name': 'RANDOM_PATTERN', 'formula': 'mean TU of top-k random patterns', 'interpretation': 'random-pattern ranking utility', 'valid_range': '(-inf, inf)', 'failure_condition': '>= ASFT'}`

- **timestamp_utc**: `2026-10-31T12:10:04.135573+00:00`
- **record_schema**: `phase-13a-v1`
