# Phase 1C.2 — Ranking Candidate Taxonomy

## Purpose

Create a candidate pool in which frequency, reuse, compression, and transfer evidence can recommend different structures. Types are hidden generator labels for fixture auditing; they are never fields in a ranker card or candidate ID.

## One primary class per candidate

Each candidate receives exactly one mutually exclusive primary archetype. Orthogonal quantities—frequency, local reuse, cross-family transfer, compression gain, apparent early quality, and realized future value—are separately measured attributes. Because “transfer-rich” and “compression-rich” can overlap with frequency/usefulness, a fixed priority rule assigns the primary class once at generation time: H deceptive; otherwise G compression-rich; otherwise E transfer-rich; otherwise F transfer-poor/local-only; otherwise A–D by the frequency × usefulness cell. The latent assignment is generated before any future-task outcome exists and is never revised from outcomes.

| Class | Primary archetype | Predeclared generator meaning |
|---|---|---|
| A | Frequent + useful | Common in discovery traces; positive future net value across a broad task subset. |
| B | Frequent + useless | Common in discovery traces; no meaningful future net benefit after frozen costs. |
| C | Rare + useful | Uncommon in discovery traces; high future task benefit despite low count. |
| D | Rare + useless | Uncommon and low-value. |
| E | Transfer-rich | Positive utility across multiple held-out task families, not merely local reuse. |
| F | Transfer-poor / local-only | Useful on its source/local family but little benefit on disjoint future families. |
| G | Compression-rich | Strong independently measured compression gain; task benefit is separately varied. |
| H | Deceptive | High early proxy/observed signal but low or negative held-out future value. |

## Fixed fixture quota

The contract generator uses `N=40` candidates per panel: A=4, B=8, C=8, D=4, E=4, F=4, G=4, H=4. Thus **20% are B frequent-useless and 20% are C rare-useful**; both mandatory classes are present without outcome-based postselection. `K=8` is the fixed selection budget.

These proportions define a controlled stress benchmark, not a population prevalence claim. In any later natural-data replication, report the observed taxonomy distribution; do not select confirmatory candidates based on sealed future outcomes merely to meet these percentages.

## Measurement and label controls

- Discovery frequency uses only the discovery/training traces and a frozen denominator.
- “Useful/useless” is defined from the separate, held-out future-value protocol, not from any ranking score. In synthetic panels the latent recipe is assigned before future task generation; only the outcome evaluator can join type labels after policy lists are locked.
- E/F transfer status is determined by the predeclared number and distribution of held-out families with positive transfer value, not by IDT's calibration transfer score.
- G compression gain is measured using a frozen codec/description-length procedure on allowed calibration data. It is not inferred from future utility.
- H deceptive status means early evidence is high while full-horizon future value is poor; early signal is never substituted for future truth.
- IDs are opaque hashes; arrival order is randomized independently of latent type. Candidate payload allowlists exclude `primary_type`, held-out outcomes, and future family values.

The taxonomy is a designed stress profile. Synthetic class-level pass results must not be described as evidence that natural IDT candidates follow these proportions.