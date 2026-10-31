# EXP-IDT-11-13

- **experiment_id**: `EXP-IDT-11-13`
- **claim**: `IDT`
- **dataset_version**: `synthetic-v1`
- **seeds**: `[0, 1, 2, 3, 4]`
## configuration

- `noise`: `trace operation insertion`

## thresholds


## metrics

- `VST`: `1.0`
- `RANK_STABILITY`: `0.76`
- `sparse_mean_IS`: `1.8`

## statistics

- `VST`: `{'n': 5.0, 'mean': 1.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 1.0, 'ci_high': 1.0, 'confidence': 0.95}`
- `RANK_STABILITY`: `{'n': 5.0, 'mean': 0.76, 'std': 0.08944271909999162, 'variance': 0.008000000000000005, 'ci_low': 0.6816014406183979, 'ci_high': 0.8383985593816021, 'confidence': 0.95}`
- `sparse_mean_IS`: `{'n': 5.0, 'mean': 1.8, 'std': 1.0062305898749053, 'variance': 1.0125, 'ci_low': 0.9180162069569759, 'ci_high': 2.681983793043024, 'confidence': 0.95}`

## raw_results

| experiment_id | claim | seed | dataset_version | configuration | metrics | variation_scores | clean_top | noisy_top | noise_rank_overlap | sparse_observations | failure_cases | observations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXP-IDT-11-13 | IDT | 0 | synthetic-v1 | {'variations': 4, 'sparse_per_family': 1} | {'VST': 1.0, 'RANK_STABILITY': 0.8, 'sparse_mean_IS': 2.25, 'clean_mean_IS': 5.75, 'sparse_candidates': 3.0, 'clean_candidates': 6.0} | {'reflection': 1.0, 'rotation': 1.0, 'counting': 1.0, 'grouping': 1.0} | [('apply_reflection',), ('find_symmetry',), ('find_rotation',), ('apply_rotation',), ('count_objects',)] | [('apply_reflection',), ('find_symmetry',), ('detect_object', 'find_symmetry'), ('find_rotation',), ('apply_rotation',)] | 0.8 | 4 | [] | {'noise_candidate_count': 13, 'clean_validation_count': 4} |
| EXP-IDT-11-13 | IDT | 1 | synthetic-v1 | {'variations': 4, 'sparse_per_family': 1} | {'VST': 1.0, 'RANK_STABILITY': 0.8, 'sparse_mean_IS': 0.0, 'clean_mean_IS': 5.75, 'sparse_candidates': 0.0, 'clean_candidates': 6.0} | {'reflection': 1.0, 'rotation': 1.0, 'counting': 1.0, 'grouping': 1.0} | [('apply_reflection',), ('find_symmetry',), ('find_rotation',), ('apply_rotation',), ('count_objects',)] | [('apply_reflection',), ('find_symmetry',), ('find_rotation',), ('apply_rotation',), ('verify_output',)] | 0.8 | 4 | [] | {'noise_candidate_count': 9, 'clean_validation_count': 4} |
| EXP-IDT-11-13 | IDT | 2 | synthetic-v1 | {'variations': 4, 'sparse_per_family': 1} | {'VST': 1.0, 'RANK_STABILITY': 0.8, 'sparse_mean_IS': 2.25, 'clean_mean_IS': 5.75, 'sparse_candidates': 3.0, 'clean_candidates': 6.0} | {'reflection': 1.0, 'rotation': 1.0, 'counting': 1.0, 'grouping': 1.0} | [('apply_reflection',), ('find_symmetry',), ('find_rotation',), ('apply_rotation',), ('count_objects',)] | [('apply_reflection',), ('find_symmetry',), ('find_rotation',), ('apply_rotation',), ('verify_output',)] | 0.8 | 4 | [] | {'noise_candidate_count': 9, 'clean_validation_count': 4} |
| EXP-IDT-11-13 | IDT | 3 | synthetic-v1 | {'variations': 4, 'sparse_per_family': 1} | {'VST': 1.0, 'RANK_STABILITY': 0.6, 'sparse_mean_IS': 2.25, 'clean_mean_IS': 6.28125, 'sparse_candidates': 3.0, 'clean_candidates': 8.0} | {'reflection': 1.0, 'rotation': 1.0, 'counting': 1.0, 'grouping': 1.0} | [('detect_object', 'find_symmetry', 'apply_reflection'), ('apply_reflection',), ('find_symmetry',), ('find_rotation',), ('detect_object', 'find_rotation', 'apply_rotation')] | [('apply_reflection',), ('find_symmetry',), ('find_rotation',), ('apply_rotation',), ('count_objects',)] | 0.6 | 4 | [] | {'noise_candidate_count': 8, 'clean_validation_count': 6} |
| EXP-IDT-11-13 | IDT | 4 | synthetic-v1 | {'variations': 4, 'sparse_per_family': 1} | {'VST': 1.0, 'RANK_STABILITY': 0.8, 'sparse_mean_IS': 2.25, 'clean_mean_IS': 5.75, 'sparse_candidates': 3.0, 'clean_candidates': 6.0} | {'reflection': 1.0, 'rotation': 1.0, 'counting': 1.0, 'grouping': 1.0} | [('apply_reflection',), ('find_symmetry',), ('find_rotation',), ('apply_rotation',), ('count_objects',)] | [('apply_reflection',), ('find_symmetry',), ('find_rotation',), ('detect_object', 'find_rotation', 'apply_rotation'), ('apply_rotation',)] | 0.8 | 4 | [] | {'noise_candidate_count': 12, 'clean_validation_count': 4} |

## results

- `VST`: `{'n': 5.0, 'mean': 1.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 1.0, 'ci_high': 1.0, 'confidence': 0.95}`
- `RANK_STABILITY`: `{'n': 5.0, 'mean': 0.76, 'std': 0.08944271909999162, 'variance': 0.008000000000000005, 'ci_low': 0.6816014406183979, 'ci_high': 0.8383985593816021, 'confidence': 0.95}`
- `sparse_mean_IS`: `{'n': 5.0, 'mean': 1.8, 'std': 1.0062305898749053, 'variance': 1.0125, 'ci_low': 0.9180162069569759, 'ci_high': 2.681983793043024, 'confidence': 0.95}`

- **failure_cases**: `[]`
## observations


- **seed**: `None`
## metric_definitions

- `VST`: `{'name': 'VST', 'formula': 'successful_variations / total_variations', 'interpretation': 'variation survival', 'valid_range': '[0, 1]', 'failure_condition': '< 0.60'}`
- `RANK_STABILITY`: `{'name': 'RANK_STABILITY', 'formula': 'overlap(top_k_clean, top_k_perturbed) / k', 'interpretation': 'invariant ranking stability', 'valid_range': '[0, 1]', 'failure_condition': '< 0.60'}`
- `SPARSE_MEAN_IS`: `{'name': 'SPARSE_MEAN_IS', 'formula': 'mean IS under sparse traces', 'interpretation': 'sparse-data invariant strength', 'valid_range': '[0, inf)', 'failure_condition': '< 0'}`

- **timestamp_utc**: `2026-10-31T10:31:11.410466+00:00`
- **record_schema**: `phase-13a-v1`
