# Negative-transfer evidence — Phase 13D

## What the saved diagnostic shows

The corrected Phase 13D review includes 190 evaluable forced-transfer diagnostic applications. In every forced case, the saved success-probability value falls (`P_after < P_before`), so the forced harm rate is 1.0. The same rows have normalized accuracy-NTR 0.0: the task remains exact-correct after transfer. The demonstrated harm signal is therefore a drop in the simulator's success-probability estimate, not an increase in observed exact task failures.

The `SAFE_RETRIEVAL_GUARD` rejected all 90 evaluable rows in the targeted negative-transfer check; ten rows are unavailable. The task-level records label these as negative-taxonomy checks. This is evidence the guard rejects the particular forced mismatch cases used in that diagnostic.

## What it does not show

- No broad balanced test of guard sensitivity and specificity across held-out beneficial and harmful transfer cases.
- No general false-positive rate on genuinely helpful retrievals.
- No proof that all harmful transfers cause actual task failure; the exact-accuracy NTR is zero in the forced diagnostics.
- No proof that a transfer-safety classifier is calibrated for arbitrary tasks or operation families.

**Verdict:** targeted negative-transfer detection/rejection is supported narrowly. General helpful-versus-harmful transfer discrimination is not established.

**Source:** [`posthoc_corrected_criteria.json`](../PHASE-13D-TRANSFER-V1/posthoc_corrected_criteria.json), [`task_level.jsonl`](../PHASE-13D-TRANSFER-V1/task_level.jsonl), [`posthoc_reanalysis.py`](../PHASE-13D-TRANSFER-V1/posthoc_reanalysis.py).
