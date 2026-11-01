# Phase 13G preflight — PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1

**Status:** preregistration/config frozen before outcome run. **Dataset:** ARC-AGI-2 public training set at upstream commit `f3283f727488ad98fe575ea6a5ac981e4a188e49`, Apache-2.0. **Split:** 600 discovery / 200 internal transfer / 200 final holdout by fixed SHA-256 task-ID ordering. Official public evaluation JSON was not extracted, parsed, scored, or used as feedback; the archive-transport deviation below is disclosed. A pre-run schema audit parsed the 1,000 public training JSONs (including eventual holdout) only for rectangularity/color-domain checks; it did not compare input/output transformations or score outcomes. **Output:** `reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/`.

## Frozen scope

Phase 13G uses a new bounded ARC adapter and does not re-label the existing synthetic `GridSolver` as an ARC solver. The DSL is fixed at ten programs: identity, two reflections, three rotations, transpose, anti-transpose, constant translation, and bijective recoloring. Every selected program must exactly fit all demonstrations; main arms evaluate at most three program trials. Unsupported tasks remain visible. Exact task success requires every test output in that task to match. Only holdout is an independent final comparison; transfer is used to validate skill candidates and is descriptive after that use.

The output taxonomy explicitly does not infer the requested semantic classes without ground truth: direct transformation labels are available for reflection/rotation/translation; symmetry is only a measurable property; counting, grouping, object detection, and pattern completion are not operationalized in v1. Cross-semantic-family transfer is unidentifiable from the unlabeled ARC files; structural-bucket transfer is descriptive.

## Component path

The runner emits real `ReasoningTrace`/`ReasoningStep` objects, mines discovery-only successful traces with the repository `TraceMiner`, creates candidates from the resulting `Invariant` objects, evaluates measured transfer using the internal transfer IDs, then calls the existing `from_invariant`/`qualify_candidate`/`Skill`/skill utility and capability/IG APIs. No Phase 13C–13F files, thresholds, or results are altered. No output-based threshold tuning is permitted. Phase 13G artifacts include compact task-level results, serialized traces, six main SVG figures, six CSV tables, source/data hashes, and an explicit unavailable/null record.

## Baselines and metrics

B1 is fixed-order no-learning search; B2 is nearest episodic memory over discovery traces; B3 is deterministic random ordering over the shared eligible program pool; B4 is exact repeated-trace compression only, explicitly not canonical DreamCoder. All arms share candidate programs, exact demonstration verification, test tasks, and the three-trial limit. Candidate trials are an algorithmic search-cost proxy, not human time or FLOPs. Final paired contrasts use a task-ID bootstrap with 10,000 resamples (seed 1307). Existing repository IS, SCV, skill utility, capability and IG formulas remain in force; absent validated capability groups make IG unavailable.

## Data handling deviation

During source discovery, a temporary upstream compressed archive containing both training and evaluation blobs was downloaded. The archive's filename listing was queried; no evaluation task JSON was extracted, parsed, or scored, and the archive was deleted. The training task list was then fetched from upstream `data/training.txt`, and only the 1,000 individually pinned training JSON files were stored and validated. This transport deviation is stated in the preregistration, dataset README, run manifest, and final report. It does not support a claim that no evaluation bytes were ever downloaded, but evaluation outputs were not analyzed or used as feedback.

## Software/data preflight

- Upstream list count: 1,000 unique training IDs.
- Local ARC training files: 1,000; all task JSONs parsed; all input/output grids rectangular with colors 0–9.
- Split integrity: 600/200/200 IDs, disjoint and exhaustive; file SHA-256s and pair counts recorded in `datasets/arc/arc-agi-2/split_manifest.json`.
- Contract tests: `PYTHONPATH=src:. python -m pytest -q tests/test_phase13g_contracts.py` — **7 passed**.
- Module compile and config JSON parse passed. The full experiment has not started as of this preflight record.

## Confirmation command

After protocol/source review, run once:

```bash
PYTHONPATH=src:. python -u -m experiments.phase13g.cli --confirm
```

The CLI refuses to overwrite an existing Phase 13G output directory, hashes source/config/data/splits before the first outcome run, writes the pre-holdout routing lock before reading holdout task JSONs, and writes a failure manifest on exceptions. If a run is incomplete, preserve it rather than silently restarting over the same output.

## Attempt 01 integrity addendum

The initial confirmation attempt returned all transfer/holdout task predictions in memory, then failed during evidence serialization (`KeyError: 'task_id'`). No numeric outcome table was persisted or inspected. The failed run is preserved at `reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1-ATTEMPT-01-REPORT-WRITE-FAILED/`. The software-only fixes are to serialize the missing task ID in discovery records and represent stability as unavailable for unsupported tasks (which are outside the preregistered stability denominator). Attempt 02 uses the identical protocol and holdout; it is not an independent replication or a pristine holdout because attempt 01 already algorithmically read the same holdout outputs. This limitation must remain in the evidence package.
