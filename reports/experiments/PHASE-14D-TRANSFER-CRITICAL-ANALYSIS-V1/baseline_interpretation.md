# Baseline Interpretation

## Corrected Phase 13D comparison

The authoritative posthoc paired contrasts are ASFT-minus-comparator transfer utility over ten seeds: B1 `+0.018909` (95% interval `[0.016727,0.020000]`), B2 `+0.015273` (`[0.013091,0.016364]`), B3 `+0.728909` (`[0.706364,0.761273]`), and B4 compression proxy `-0.001091` (`[-0.003273,0]`). Thus ASFT is positive against B1–B3 but not strictly above B4; the all-mandatory-baseline criterion fails. B4 is not DreamCoder.

Phase 13D's original frozen `criteria.json`/aggregate dashboard and the corrected posthoc files must remain distinguishable. The corrected view repairs pairwise lookup and composition coverage; it is authoritative for these posthoc conclusions, without overwriting the original record or pretending it was the original dashboard output.

## Why phase results cannot be pooled

- Phase 13C compares SCT and MEMORY_ONLY using its own net-value and cost accounting. MEMORY_ONLY has higher net value (`1.325` vs `0.345`) and 418/440 correct applications versus 201/440 SCT.
- Phase 13F uses separate arms and a joint utility/CGR decision rule. ASFT-minus-X1_NO_TRANSFER task utility is `-0.0363`, composed-task utility `-0.3412`, and CGR `+0.2872`; ASFT's status varies by comparator.
- Phase 13D transfer utility, Phase 13C positive-credit reuses, and Phase 13F utility/CGR are different protocols and endpoints. They cannot be averaged into a single comparative effect.

**Conclusion:** a transfer-specific gain against some controls is not a general performance advantage. State comparator, phase, endpoint, and accounting version for each contrast.
