# SCT and the memory-only result — cross-phase interpretation

## Phase 13C matched primary comparison

Phase 13C's `MEMORY_ONLY` arm scores mean net value **1.325**, versus **0.345** for SCT (paired SCT-minus-memory difference `-0.980`, 95% seed-bootstrap CI `[-1.020,-0.940]`). On 440 eligible opportunities, memory applied all 440 and was correct on 418; SCT applied 223, was correct on 201, failed 22 times and had 217 no-matches. Correct/eligible was 0.950 for memory and 0.457 for SCT. In this particular repetitive synthetic task stream and the Phase 13C primary net-value accounting, exact retrieval beat skill creation.

This gives a credible alternative explanation for much of the observed benefit: replay can be cheaper than constructing abstractions when tasks recur closely. It is a strong result for this specific arm/metric—not a general proof that memory always beats reusable skills. Normalized maintenance cost is modeled in simulator units, not observed compute expenditure.

## Phase 13F is a different control

Phase 13F's `B2_MEMORY_SKILL_STORE` is a separately specified memory comparator, not an exact replication of the Phase 13C `MEMORY_ONLY` arm. It is part of a different 10-seed, multi-arm benchmark and is judged on task utility plus CGR. B2 has task utility `0.715` and CGR `0`; ASFT has task utility `0.789906` and CGR `0.287172`, so the frozen joint comparison favors ASFT. Do not pool these numbers with the Phase 13C mean net values or treat the arms as identical.

## Scientific conclusion

- SCT has **not demonstrated an advantage over memory-based retrieval** across the available tests.
- Phase 13C is evidence that memory-only retrieval can outperform SCT on a matched primary net-value outcome.
- Phase 13F prevents the stronger, universal statement that memory-based approaches are always superior.
- The defensible conclusion is mixed and comparator-specific: neither general SCT superiority nor general memory superiority has been established.
