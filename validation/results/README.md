# Results Archive

No empirical results are present yet. Keep this statement until the first complete run has been independently checked.

## Layout

```text
results/
  agi2/H1_IDT/<run_id>/...   ARC-2 run artifacts
  agi2/H2_SCT/<run_id>/...
  agi2/H3_CGM/<run_id>/...
  agi3/H1_IDT/<run_id>/...   ARC-3 run artifacts
  agi3/H2_SCT/<run_id>/...
  agi3/H3_CGM/<run_id>/...
  shared/tables/              Derived, script-generated summary tables
  shared/figures/             Paper figures generated from archived metrics
```

Within each run folder, preserve source outputs unchanged. Store per-task/game rows in `metrics.jsonl` or `per_task_metrics.csv`; summaries must be generated from them by versioned code. Never edit raw predictions after evaluation.

## Required result reporting

Every table/figure caption states track, split, run IDs, variant, budget, evaluator version, number of task/game IDs, number of seeds, uncertainty method, and whether result is `PILOT`, `CONFIRMATORY`, or `DEVIATION`. Include failed runs/timeouts in counts. The paper must not quote a public leaderboard score as if it came from this local experiment.

## Result index

| run_id | track | hypothesis | status | primary finding (neutral) | artifacts | reviewer/date |
|---|---|---|---|---|---|---|
| None yet | — | — | NOT_RUN | No run artifacts have been created. | — | — |
