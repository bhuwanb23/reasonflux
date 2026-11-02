# Phase 2E.7 — Invariant Discovery Yield

Yield is reported over **successful discovery traces** (miner input) and over **600 discovery tasks** (task productivity). The Phase 2C conditions reuse the same task IDs. Transfer/holdout traces are excluded from miner input.

| Source | Successful discovery traces | Current raw patterns | Current candidate proposals / accepted | Current invariant yield per task | Relaxed-S2 proposals / accepted | Proposal yield per successful trace (S2) |
|---|---:|---:|---:|---:|---:|---:|
| Phase 13G historical | 3 | 0 | 0 / 0 | 0 observed final invariants / 600; candidate survival N/A | 2 / 0 | 0.667 / 3 |
| S1 | 1 | 0 | 0 / 0 | 0 / 600; candidate survival N/A | 0 / 0 | 0 / 1 |
| S2 | 2 | 0 | 0 / 0 | 0 / 600; candidate survival N/A | 2 / 0 | 1.000 / 2 |
| S3 | 3 | 0 | 0 / 0 | 0 / 600; candidate survival N/A | 2 / 0 | 0.667 / 3 |
| S4 | 3 | 0 | 0 / 0 | 0 / 600; candidate survival N/A | 2 / 0 | 0.667 / 3 |

At current settings, trace→pattern yield is 0/3, 0/1, 0/2, 0/3, 0/3 because the support floor eliminates all signatures. Candidate→invariant yield is not estimable on the frozen path: no candidates were input to validation. In the relaxed sweep, candidate-proposal→accepted-generation-candidate yield is **0/2** wherever proposals exist; they are rejected before validation. No final semantic invariant is observed.

The diagnostic validator bypass is reported separately: it can produce F-C-G `VALIDATED` states for 2/2 historical, S3, and S4 proposals, but none is transfer-verified or promotable; S2 yields 0/2 structural validations. These same-trace diagnostic states are not included as discovered-invariant yield. Full step-level counts and denominators appear in `candidate_generation_audit.csv`.