# ReasonFlux Validation Workspace

This folder is the source of truth for **implementation validation, experiment plans, run metadata, and results** for IDT, SCT, and CGM on ARC-AGI-2 and ARC-AGI-3.

> **Status at creation:** Protocol/template scaffold only. No validation runs or result values are recorded here yet. Never enter anticipated, fabricated, or leaderboard-inferred values as experiment results.

## Folder map

```text
validation/
  README.md                       How to use this workspace
  PROTOCOL.md                     Required controls, freezing, leakage, analysis
  HYPOTHESES.md                   Falsifiable claims, outcomes, decision rules
  EXPERIMENT_MATRIX.csv           Variants and comparisons to preregister
  ENVIRONMENT_TEMPLATE.yaml       Hardware/software manifest per run
  DATA_MANIFEST_TEMPLATE.csv      Dataset/split provenance and hashes
  RUN_LOG_TEMPLATE.csv            One row per execution
  CLAIM_EVIDENCE_TEMPLATE.csv     Paper claim-to-evidence audit
  DEVIATIONS.md                   All protocol deviations, including failures
  experiments/agi2/               ARC-AGI-2-specific experiment plan
  experiments/agi3/               ARC-AGI-3-specific experiment plan
  results/<track>/<hypothesis>/<run_id>/  Immutable raw run bundle
  results/shared/                 Cross-track analyses and paper tables
  scripts/new_run.py              Create a run bundle from templates
```

## Required workflow

1. **Before any confirmatory run:** edit and approve `PROTOCOL.md`, `HYPOTHESES.md`, both track plans, and `EXPERIMENT_MATRIX.csv`. Fill all `REQUIRED_BEFORE_RUN` fields. Commit/hash the frozen protocol. Record date, owner, and code commit.
2. **Make data splits first:** create immutable task/game ID lists and hashes in `DATA_MANIFEST_TEMPLATE.csv`; do not tune on test/held-out labels. Keep Kaggle hidden-test data/labels out of local experiments.
3. **Run baselines before ASFT:** execute no-skill and simple-library controls on the same tasks, budgets, hardware, model, and output evaluator.
4. **Create a run directory:** `python validation/scripts/new_run.py --track agi2 --hypothesis H1_IDT --run-id 20261029_agi2_H1_IDT_v01 --owner NAME`. The helper rejects overwrites. Copy the environment/data manifests into each run bundle and fill them.
5. **Save raw artifacts:** predictions/actions, traces, skill decisions, metrics, stdout/stderr, configuration, environment manifest, dataset manifest, code commit/hash, and run log. Raw outputs are immutable; derived summaries go under `results/shared/` or the appropriate `processed/` folder.
6. **Analyze exactly as preregistered:** primary metric, task aggregation, confidence interval, exclusions, and decision rule must be fixed before results are inspected. Mark any additional analysis as exploratory.
7. **Update the claim-evidence table:** paper claims may only use evidence with a reproducible run ID and artifact path.

## Run ID and result layout

Use lowercase track folder (`agi2` or `agi3`), canonical hypothesis names (`H1_IDT`, `H2_SCT`, `H3_CGM`), and unique run IDs. Recommended bundle:

```text
results/agi2/H1_IDT/20261029_agi2_H1_IDT_v01/
  manifest.yaml
  environment.yaml
  data_manifest.csv
  config.yaml
  metrics.json
  predictions.json              # or track-native output
  traces.jsonl
  skill_events.jsonl
  stdout.log
  stderr.log
  NOTES.md
```

Large model files/checkpoints should not be copied into this repo; record their source, exact version, license, and cryptographic hash in the manifest, and preserve them in approved storage.

## Interpretation labels

Use only these labels in tables and reports:

- `NOT_RUN` — no execution exists.
- `SMOKE_TEST` — checks loading/interface/schema only; not evidence for a hypothesis.
- `PILOT` — exploratory or underpowered; informs protocol only.
- `CONFIRMATORY` — preregistered, frozen, controlled run.
- `FAILED_RUN` — execution failed; retain logs and diagnose.
- `DEVIATION` — protocol changed; report the change and do not silently pool with confirmatory results.

## Important distinction

A successful Kaggle submission demonstrates that a notebook ran and produced a valid competition artifact. It does **not** by itself validate IDT, SCT, or CGM. Hypothesis evidence requires controlled comparisons on held-out tasks/games, tracked budgets, and documented uncertainty. Public leaderboard results are not substitutes for local, reproducible experiments.
