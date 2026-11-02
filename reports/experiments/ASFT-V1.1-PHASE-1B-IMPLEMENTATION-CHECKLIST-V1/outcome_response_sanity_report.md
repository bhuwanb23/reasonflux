# Phase 1B — Outcome-Response Sanity Report

**Purpose:** verify that the selected-set value calculation can report a genuine SCV loss, tie, or win under separately supplied candidate outcomes.  
**Scope:** deterministic synthetic contract fixture only; not a Phase 4 run, not a calibration sample, and not evidence about real SCV performance.

## Why this check was added

A pressure test alone can show that selectors choose differently while leaving a second failure possible: a value aggregator that cannot fairly register one policy as worse. This report adds an intentionally adverse fixture where candidates selected by SCV include four high-scoring deceptive candidates with poor horizon value, while other selectors select alternatives. The choices are locked first; only then is the separate fixture truth used to verify endpoint behavior.

The candidate-level truth recipe, outcomes, and costs are separate from SCV score calculation. The test asks whether the aggregation reports the stipulated contrast; it does not claim that these are observed ASFT task outcomes.

## Selected-set results for contract fixture 0

Primary-style fixture calculation is mean candidate net value per available slot, with K=8. Values are direct computations from the separate synthetic `TruthRecord` fixture (not a production-sealed outcome store), not empirical estimates.

| Policy | Selected type counts A/B/C/D/E | Net value per slot (TEU) | Difference vs SCV (TEU) | Fixture reading |
|---|---|---:|---:|---|
| S1 SCV | 4 / 0 / 0 / 4 / 0 | **−0.5500** | 0.0000 | Selects four positive A and four deceptive negative D; misses rare high-impact E. |
| S2 Frequency | 0 / 0 / 4 / 4 / 0 | −3.1750 | −2.6250 | Lower than SCV in this fixture. |
| S3 Reuse probability | 0 / 0 / 4 / 4 / 0 | −3.1750 | −2.6250 | Lower than SCV in this fixture. |
| S4 Random | 2 / 2 / 3 / 0 / 1 | **+1.2313** | **+1.7813** | Outperforms SCV on the stipulated outcomes. |
| S5 Always, capacity-limited | 3 / 2 / 1 / 1 / 1 | **+1.1688** | **+1.7188** | Outperforms SCV on the stipulated outcomes. |
| S6 Never | 0 / 0 / 0 / 0 / 0 | **0.0000** | **+0.5500** | No-learning anchor outperforms SCV here. |
| S7 Oracle | 4 / 0 / 0 / 0 / 4 | +2.9500 | +3.5000 | Analysis ceiling only; excluded from policy competition. |

The machine-readable rows, selected IDs, type counts, and values are in [`outcome_response_sanity.csv`](outcome_response_sanity.csv).

## What the fixture establishes

- The metric pipeline can report SCV **losing** to random, capacity-limited always, and never-create.
- The same fixture reports SCV **winning** over frequency and reuse-only.
- CT-9B supplies a separate equal-value fixture; all K-sized policies tie when candidate outcomes are identical.
- Together with the pre-outcome divergence tests, the harness can distinguish decision pressure from outcome quality and can represent win/tie/loss patterns.

## What it does not establish

- It does not estimate SCV's average advantage, power, robustness, or real-task performance.
- The feature and truth recipes are fixed synthetic test data, not independently generated task results.
- These numbers must never be cited as ASFT experimental findings or used to tune the Phase 4 candidate generator.
- The only confirmatory result will come from the separately frozen candidate/task generator and untouched outcome split after all unlock gates pass.

**Brutal-honesty conclusion:** the contract suite now has an explicit adverse-value case where SCV loses. This is a test of the benchmark's ability to expose failure—not a claim that the later benchmark has already shown SCV to fail.