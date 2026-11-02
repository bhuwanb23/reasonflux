# Phase 2B — Provenance and QA Validation

## Final QA results

- **Source/artifact records:** 1,062 SHA-256 records in `source_manifest.json` and `source_hashes.csv`: 1,000 ARC task files, 47 protocol/implementation/historical-source records, and 15 Phase 2B artifacts.
- **Hash integrity:** all 1,062 recorded files matched their manifest digests. The 1,000 task-file raw-byte hashes also matched both the ARC source manifest and the Phase 13G split manifest. Raw-file hashing is lineage QA only; task test-output fields were not parsed or used by the benchmark.
- **Run identity:** runner, frozen config, preregistration, dataset split manifest, and dataset source manifest hashes match `run_manifest.json`.
- **Task outcome table:** 1,000 unique task IDs; split totals are discovery 600, transfer 200, holdout 200. Budgeted C1 fits are a subset of fullscan fits; both modes emit and independently validate one trace per task; C3 equals exact demo fit; C4 is zero; C5–C7 are explicitly blocked upstream.
- **Summary consistency:** split/aggregate counts reconcile to task-level rows. Fullscan counts reproduce the saved Phase 13G demo-fit totals: 3/600, 5/200, and 2/200. Accuracy is `NOT_MEASURED_BY_DESIGN` in every summary row.
- **Stage framework:** seven C1–C7 rows parsed and validated.
- **CSV/JSON parsing:** all four CSV files and all three JSON files parse. CSV row counts: stage framework 7; task outcomes 1,000; split summary 4; hash index 1,062.
- **Local Markdown links:** all 19 package-relative links resolve.
- **Isolation static check:** benchmark runner contains no `task['test']`/`task["test"]` subscript and no `solve_task()` call. The fail-closed loader parses only the first top-level `train` array and stops before the following field. No test accuracy, ARC score, or efficacy statistic was computed.

## Interpretation boundary

QA confirms source lineage, output consistency, and the declared coverage-only dataflow. It does not validate ARC semantic labels, establish that bounded no-fit means unrepresentable, demonstrate a causal representation bottleneck, or establish ASFT efficacy. Phase 13G historical outcomes were not changed.