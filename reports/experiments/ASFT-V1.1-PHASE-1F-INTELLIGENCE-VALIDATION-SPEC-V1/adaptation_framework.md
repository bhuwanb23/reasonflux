# Phase 1F.5 — Adaptation Framework

## Construct

Adaptation is externally observed recovery or effective policy change after an unannounced, preregistered task shift. It is not IG growth, internal state change, or a system's claim that it adapted.

## Shift families

Use separate held-out sets for: (1) rule changes, (2) distribution shifts, (3) task-family shifts, and (4) vocabulary/symbol remapping. Freeze shift magnitude and reveal schedule during development; reserve confirmatory shifts and their generators unseen. At least two shift types must appear in confirmation and replication.

## Procedure

1. Measure pre-shift external performance on disjoint baseline items.
2. Apply the shift without exposing test labels; permit a fixed evidence budget (e.g., five labeled demonstrations, frozen before confirmation).
3. Probe at fixed intervals on unseen post-shift items.
4. Include no-shift, no-new-evidence, and random/chance controls with matched query, context, compute, and memory budgets.
5. Run delayed no-refresh probes to distinguish immediate adjustment from persistent adaptation.

## Outcomes

Primary adaptation secondary endpoint: normalized external recovery-curve AULC; also report examples-to-criterion, post-shift accuracy, transfer to held-out shift instances, retention, and resource cost. Analyze each shift type separately before any prespecified macro-summary. Positive adaptation must exceed the no-new-evidence and random baselines by its frozen SOI with cluster-aware uncertainty.

The adaptation scorer uses behavior only. IG may be joined as a predictor only after outputs, gold, and scores are locked. If IG affects shift selection, evidence budget, scoring, or success labels, the result is unavailable.