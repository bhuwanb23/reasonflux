# Phase 1B Pressure Validation Report

**Validation:** pre-outcome implementation/contract test on synthetic fixtures.  
**Result:** pressure gate passed on 100/100 fixture panels.  
**Boundary:** these are not research batches or outcome evidence. The 100 panels reuse one deterministic feature/type recipe while seeds change IDs, randomized arrival order, and random-selector draws.

## Frozen gate

Each panel contains 20 candidates, K=8 slots, and an equal storage budget of eight units (one per candidate). S1–S5 select eight; S6 Never is the required zero-rate sentinel; S7 Oracle is excluded from pressure metrics. For every panel, SCV must differ from Frequency, Reuse, and Random by at least 0.10 symmetric-difference rate. Contested SDR is the mean pairwise divergence among S1–S4 and must be at least 0.20. The pressure validator only accepts public candidate cards and selector sets—it does not accept truth labels or outcomes.

For sets A and B, `D(A,B)=|A △ B|/N`. The check runs before the synthetic truth record is used by the separate outcome-response sanity test.

## 100-fixture results

| Measure | Result | Requirement | Status |
|---|---:|---:|---|
| Fixtures evaluated | 100 | 100 contract fixtures | PASS |
| Pressure gate | 100/100 | 100% pass | PASS |
| Mean contested SDR | 0.3682 | ≥0.20 | PASS |
| Minimum contested SDR | 0.2500 | ≥0.20 | PASS |
| Maximum contested SDR | 0.5000 | — | — |
| Mean / minimum SCV–Frequency divergence | 0.4000 / 0.4000 | ≥0.10 each panel | PASS |
| Mean / minimum SCV–Reuse divergence | 0.4000 / 0.4000 | ≥0.10 each panel | PASS |
| Mean / minimum SCV–Random divergence | 0.4590 / 0.3000 | ≥0.10 each panel | PASS |
| S1–S5 selection/storage | 8/20; 8/8 units | K=8; budget=8 | PASS |
| S6 Never | 0/20 | Sentinel exception | PASS |

## Pairwise divergence matrix — fixture seed 0

| Selector | S1 SCV | S2 Frequency | S3 Reuse | S4 Random | S5 Always-cap | S6 Never |
|---|---:|---:|---:|---:|---:|---:|
| S1 SCV | 0.00 | 0.40 | 0.40 | 0.60 | 0.40 | 0.40 |
| S2 Frequency | 0.40 | 0.00 | 0.00 | 0.50 | 0.60 | 0.40 |
| S3 Reuse | 0.40 | 0.00 | 0.00 | 0.50 | 0.60 | 0.40 |
| S4 Random | 0.60 | 0.50 | 0.50 | 0.00 | 0.40 | 0.40 |
| S5 Always-cap | 0.40 | 0.60 | 0.60 | 0.40 | 0.00 | 0.40 |
| S6 Never | 0.40 | 0.40 | 0.40 | 0.40 | 0.40 | 0.00 |

Frequency and reuse tie in this fixture; that is acceptable. The criterion is that SCV differs from each serious baseline and the contested SDR threshold is passed—not that every baseline pair be artificially forced apart.

## Limits and next gate

This test establishes that the fixture interface/gate detects policy divergence and does not need outcome access. It does **not** validate the actual candidate/task generator, a powered independent dataset, empirical costs, or selector performance. Before confirmatory evaluation, rerun the pressure test on the actual frozen generator, hash every panel/order, and demonstrate the outcome store is sealed until after pressure is locked. A failure blocks confirmation; it is not a null effect.