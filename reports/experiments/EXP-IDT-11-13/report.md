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
- `RANK_STABILITY`: `0.72`
- `sparse_mean_IS`: `1.8`
- `clean_mean_IS`: `5.85625`
- `sparse_candidates`: `2.4`
- `clean_candidates`: `6.4`
- `sparse_strong_fraction`: `0.0`
- `clean_strong_fraction`: `0.0`
- `sparse_precision`: `1.0`
- `sparse_recall`: `0.2`

## statistics

- `VST`: `{'n': 5.0, 'mean': 1.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 1.0, 'ci_high': 1.0, 'confidence': 0.95}`
- `RANK_STABILITY`: `{'n': 5.0, 'mean': 0.72, 'std': 0.10954451150103327, 'variance': 0.012000000000000009, 'ci_low': 0.6239817664728937, 'ci_high': 0.8160182335271062, 'confidence': 0.95}`
- `sparse_mean_IS`: `{'n': 5.0, 'mean': 1.8, 'std': 1.0062305898749053, 'variance': 1.0125, 'ci_low': 0.9180162069569759, 'ci_high': 2.681983793043024, 'confidence': 0.95}`
- `clean_mean_IS`: `{'n': 5.0, 'mean': 5.85625, 'std': 0.23758222260935266, 'variance': 0.0564453125, 'ci_low': 5.648003826642619, 'ci_high': 6.064496173357381, 'confidence': 0.95}`
- `sparse_candidates`: `{'n': 5.0, 'mean': 2.4, 'std': 1.3416407864998738, 'variance': 1.8, 'ci_low': 1.2240216092759677, 'ci_high': 3.575978390724032, 'confidence': 0.95}`
- `clean_candidates`: `{'n': 5.0, 'mean': 6.4, 'std': 0.8944271909999159, 'variance': 0.7999999999999999, 'ci_low': 5.616014406183979, 'ci_high': 7.183985593816022, 'confidence': 0.95}`
- `sparse_strong_fraction`: `{'n': 5.0, 'mean': 0.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 0.0, 'ci_high': 0.0, 'confidence': 0.95}`
- `clean_strong_fraction`: `{'n': 5.0, 'mean': 0.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 0.0, 'ci_high': 0.0, 'confidence': 0.95}`
- `sparse_precision`: `{'n': 5.0, 'mean': 1.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 1.0, 'ci_high': 1.0, 'confidence': 0.95}`
- `sparse_recall`: `{'n': 5.0, 'mean': 0.2, 'std': 0.11180339887498948, 'variance': 0.0125, 'ci_low': 0.10200180077299732, 'ci_high': 0.2979981992270027, 'confidence': 0.95}`

## raw_results

| experiment_id | claim | seed | dataset_version | configuration | metrics | variation_scores | clean_top | noisy_top | noise_rank_overlap | sparse_observations | failure_cases | observations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXP-IDT-11-13 | IDT | 0 | synthetic-v1 | {'variations': 4, 'sparse_per_family': 1} | {'VST': 1.0, 'RANK_STABILITY': 0.8, 'sparse_mean_IS': 2.25, 'clean_mean_IS': 5.75, 'sparse_candidates': 3.0, 'clean_candidates': 6.0, 'sparse_strong_fraction': 0.0, 'clean_strong_fraction': 0.0, 'sparse_precision': 1.0, 'sparse_recall': 0.25} | {'reflection': 1.0, 'rotation': 1.0, 'counting': 1.0, 'grouping': 1.0} | [('apply_reflection',), ('find_symmetry',), ('find_rotation',), ('apply_rotation',), ('count_objects',)] | [('apply_reflection',), ('find_symmetry',), ('detect_object', 'find_symmetry'), ('find_rotation',), ('apply_rotation',)] | 0.8 | 4 | [] | {'noise_candidate_count': 11, 'clean_validation_count': 4} |
| EXP-IDT-11-13 | IDT | 1 | synthetic-v1 | {'variations': 4, 'sparse_per_family': 1} | {'VST': 1.0, 'RANK_STABILITY': 0.8, 'sparse_mean_IS': 0.0, 'clean_mean_IS': 5.75, 'sparse_candidates': 0.0, 'clean_candidates': 6.0, 'sparse_strong_fraction': 0.0, 'clean_strong_fraction': 0.0, 'sparse_precision': 1.0, 'sparse_recall': 0.0} | {'reflection': 1.0, 'rotation': 1.0, 'counting': 1.0, 'grouping': 1.0} | [('apply_reflection',), ('find_symmetry',), ('find_rotation',), ('apply_rotation',), ('count_objects',)] | [('apply_reflection',), ('find_symmetry',), ('find_rotation',), ('find_rotation', 'apply_rotation'), ('apply_rotation',)] | 0.8 | 4 | [] | {'noise_candidate_count': 9, 'clean_validation_count': 4} |
| EXP-IDT-11-13 | IDT | 2 | synthetic-v1 | {'variations': 4, 'sparse_per_family': 1} | {'VST': 1.0, 'RANK_STABILITY': 0.8, 'sparse_mean_IS': 2.25, 'clean_mean_IS': 5.75, 'sparse_candidates': 3.0, 'clean_candidates': 6.0, 'sparse_strong_fraction': 0.0, 'clean_strong_fraction': 0.0, 'sparse_precision': 1.0, 'sparse_recall': 0.25} | {'reflection': 1.0, 'rotation': 1.0, 'counting': 1.0, 'grouping': 1.0} | [('apply_reflection',), ('find_symmetry',), ('find_rotation',), ('apply_rotation',), ('count_objects',)] | [('apply_reflection',), ('find_symmetry',), ('find_rotation',), ('find_rotation', 'apply_rotation'), ('apply_rotation',)] | 0.8 | 4 | [] | {'noise_candidate_count': 11, 'clean_validation_count': 4} |
| EXP-IDT-11-13 | IDT | 3 | synthetic-v1 | {'variations': 4, 'sparse_per_family': 1} | {'VST': 1.0, 'RANK_STABILITY': 0.6, 'sparse_mean_IS': 2.25, 'clean_mean_IS': 6.28125, 'sparse_candidates': 3.0, 'clean_candidates': 8.0, 'sparse_strong_fraction': 0.0, 'clean_strong_fraction': 0.0, 'sparse_precision': 1.0, 'sparse_recall': 0.25} | {'reflection': 1.0, 'rotation': 1.0, 'counting': 1.0, 'grouping': 1.0} | [('detect_object', 'find_symmetry', 'apply_reflection'), ('apply_reflection',), ('find_symmetry',), ('find_rotation',), ('detect_object', 'find_rotation', 'apply_rotation')] | [('apply_reflection',), ('find_symmetry',), ('find_symmetry', 'apply_reflection'), ('find_rotation',), ('find_rotation', 'apply_rotation')] | 0.6 | 4 | [] | {'noise_candidate_count': 10, 'clean_validation_count': 6} |
| EXP-IDT-11-13 | IDT | 4 | synthetic-v1 | {'variations': 4, 'sparse_per_family': 1} | {'VST': 1.0, 'RANK_STABILITY': 0.6, 'sparse_mean_IS': 2.25, 'clean_mean_IS': 5.75, 'sparse_candidates': 3.0, 'clean_candidates': 6.0, 'sparse_strong_fraction': 0.0, 'clean_strong_fraction': 0.0, 'sparse_precision': 1.0, 'sparse_recall': 0.25} | {'reflection': 1.0, 'rotation': 1.0, 'counting': 1.0, 'grouping': 1.0} | [('apply_reflection',), ('find_symmetry',), ('find_rotation',), ('apply_rotation',), ('count_objects',)] | [('apply_reflection',), ('find_symmetry',), ('detect_object', 'find_symmetry'), ('find_rotation',), ('find_rotation', 'apply_rotation')] | 0.6 | 4 | [] | {'noise_candidate_count': 13, 'clean_validation_count': 4} |

## results

- `VST`: `{'n': 5.0, 'mean': 1.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 1.0, 'ci_high': 1.0, 'confidence': 0.95}`
- `RANK_STABILITY`: `{'n': 5.0, 'mean': 0.72, 'std': 0.10954451150103327, 'variance': 0.012000000000000009, 'ci_low': 0.6239817664728937, 'ci_high': 0.8160182335271062, 'confidence': 0.95}`
- `sparse_mean_IS`: `{'n': 5.0, 'mean': 1.8, 'std': 1.0062305898749053, 'variance': 1.0125, 'ci_low': 0.9180162069569759, 'ci_high': 2.681983793043024, 'confidence': 0.95}`
- `clean_mean_IS`: `{'n': 5.0, 'mean': 5.85625, 'std': 0.23758222260935266, 'variance': 0.0564453125, 'ci_low': 5.648003826642619, 'ci_high': 6.064496173357381, 'confidence': 0.95}`
- `sparse_candidates`: `{'n': 5.0, 'mean': 2.4, 'std': 1.3416407864998738, 'variance': 1.8, 'ci_low': 1.2240216092759677, 'ci_high': 3.575978390724032, 'confidence': 0.95}`
- `clean_candidates`: `{'n': 5.0, 'mean': 6.4, 'std': 0.8944271909999159, 'variance': 0.7999999999999999, 'ci_low': 5.616014406183979, 'ci_high': 7.183985593816022, 'confidence': 0.95}`
- `sparse_strong_fraction`: `{'n': 5.0, 'mean': 0.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 0.0, 'ci_high': 0.0, 'confidence': 0.95}`
- `clean_strong_fraction`: `{'n': 5.0, 'mean': 0.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 0.0, 'ci_high': 0.0, 'confidence': 0.95}`
- `sparse_precision`: `{'n': 5.0, 'mean': 1.0, 'std': 0.0, 'variance': 0.0, 'ci_low': 1.0, 'ci_high': 1.0, 'confidence': 0.95}`
- `sparse_recall`: `{'n': 5.0, 'mean': 0.2, 'std': 0.11180339887498948, 'variance': 0.0125, 'ci_low': 0.10200180077299732, 'ci_high': 0.2979981992270027, 'confidence': 0.95}`

- **failure_cases**: `[]`
## observations


- **seed**: `None`
## metric_definitions

- `VST`: `{'name': 'VST', 'formula': 'successful_variations / total_variations', 'interpretation': 'variation survival', 'valid_range': '[0, 1]', 'failure_condition': '< 0.60'}`
- `RANK_STABILITY`: `{'name': 'RANK_STABILITY', 'formula': 'overlap(top_k_clean, top_k_perturbed) / k', 'interpretation': 'invariant ranking stability', 'valid_range': '[0, 1]', 'failure_condition': '< 0.60'}`
- `sparse_mean_IS`: `{'name': 'SPARSE_MEAN_IS', 'formula': 'mean IS under sparse traces', 'interpretation': 'sparse-data invariant strength', 'valid_range': '[0, inf)', 'failure_condition': '< 0'}`
- `clean_mean_IS`: `{'name': 'CLEAN_MEAN_IS', 'formula': 'mean IS under full traces', 'interpretation': 'reference invariant strength', 'valid_range': '[0, inf)', 'failure_condition': '< 0'}`
- `sparse_candidates`: `{'name': 'SPARSE_CANDIDATES', 'formula': 'candidate count under sparse traces', 'interpretation': 'sparse candidate count', 'valid_range': '[0, inf)', 'failure_condition': '< 0'}`
- `clean_candidates`: `{'name': 'CLEAN_CANDIDATES', 'formula': 'candidate count under full traces', 'interpretation': 'reference candidate count', 'valid_range': '[0, inf)', 'failure_condition': '< 0'}`
- `sparse_strong_fraction`: `{'name': 'SPARSE_STRONG_FRACTION', 'formula': 'strong sparse invariants / sparse invariants', 'interpretation': 'sparse over-promotion rate', 'valid_range': '[0, 1]', 'failure_condition': '> clean rate'}`
- `clean_strong_fraction`: `{'name': 'CLEAN_STRONG_FRACTION', 'formula': 'strong full-data invariants / full invariants', 'interpretation': 'reference strong-confidence rate', 'valid_range': '[0, 1]', 'failure_condition': '< 0'}`
- `sparse_precision`: `{'name': 'SPARSE_PRECISION', 'formula': 'valid sparse invariants / sparse invariants', 'interpretation': 'sparse-data precision', 'valid_range': '[0, 1]', 'failure_condition': '< 0.70'}`
- `sparse_recall`: `{'name': 'SPARSE_RECALL', 'formula': 'discovered sparse expected / expected invariants', 'interpretation': 'sparse-data recall', 'valid_range': '[0, 1]', 'failure_condition': '< 0'}`

- **timestamp_utc**: `2026-10-31T13:42:26.791382+00:00`
- **record_schema**: `phase-13a-v1`
