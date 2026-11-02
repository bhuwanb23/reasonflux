# Phase 2C.6 — Budget Sensitivity Benchmark

## Conditions and results

All conditions hold fixed: the ten-program Phase 13G representation, exact-demo fit rule, parameter inference, task set, split manifest, and candidate order. Only the maximum candidate-trial cap changes. Each rate uses the same 1,000 task IDs; accuracy is not measured.

| Condition | Candidate cap | Effective unique pool | Discovery | Transfer | Holdout | Overall coverage / successful traces | Successful discovery support | Invariants |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| S1 | 3 | 3 | 1/600 (0.1667%) | 0/200 | 1/200 (0.50%) | **2/1,000 (0.20%)** | reflect_vertical: 1 | 0 |
| S2 | 6 | 6 | 2/600 (0.3333%) | 1/200 (0.50%) | 2/200 (1.00%) | **5/1,000 (0.50%)** | reflect_vertical: 1; rotate_270: 1 | 0 |
| S3 | 15 | 10 (finite DSL) | 3/600 (0.50%) | 5/200 (2.50%) | 2/200 (1.00%) | **10/1,000 (1.00%)** | three distinct signatures, each 1 | 0 |
| S4 | unrestricted = all 10 | 10 | 3/600 (0.50%) | 5/200 (2.50%) | 2/200 (1.00%) | **10/1,000 (1.00%)** | three distinct signatures, each 1 | 0 |

Trace records and valid traces remain 1,000/1,000 per condition by design. Successful traces rise from 2 to 5 to 10. No trace or candidate pruning occurs. The 6-candidate condition recovers three more fits than S1; the full finite scan recovers eight more than S1. S3's 15-slot cap cannot exceed the ten-program DSL; S3 and S4 are identical.

## Interpretation

Search allowance **does matter** for operational demo-fit coverage under this fixed implementation: found coverage increases fivefold from S1 to the all-ten scan (0.20% to 1.00%). This is strong descriptive evidence of a search-budget/order contribution to *found-fit coverage* in the frozen DSL. It is not evidence that more search alone would yield useful ARC accuracy or activate ASFT: even all ten candidates cover only 10/1,000 demonstrations, and no invariant candidates arise because discovery supports remain below five.

The 0.20%→0.50%→1.00% curve cannot establish that representational limits are the primary cause. The all-ten ceiling still combines the ten-program vocabulary, parameter inference, exact-demo rule, and bounded first-fit search. No alternative representation was compared. The support threshold remains unchanged and is not tuned from these outcomes.

## Accuracy and mechanism boundary

`Accuracy = NOT_MEASURED_BY_DESIGN` in every condition. Test outputs were not parsed by the Phase 2C runner. These are coverage/search diagnostics—not performance, leaderboard, transfer, capability, or intelligence results.