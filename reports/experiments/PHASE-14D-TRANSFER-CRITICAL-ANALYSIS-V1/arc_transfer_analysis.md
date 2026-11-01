# ARC transfer — Phase 13G interpretation

Phase 13G used a bounded ARC-AGI-2 adapter and did not produce eligible source skills for transfer. Exact demonstration fit was 3/600 discovery tasks, 5/200 transfer tasks, and 2/200 holdout tasks. It accepted/promoted zero invariant candidates, zero skills, and zero capabilities; transfer precision therefore had a zero denominator and was unavailable. The bounded system's holdout exact-task accuracy was 0.005 across arms.

**Conclusion:** transfer on ARC was not demonstrated because the invariant/skill pipeline did not yield eligible candidates under this DSL and its coverage. This is an upstream candidate-coverage bottleneck, not a clean test proving that transfer fails on ARC in principle. Phase 13G's initial run generated predictions in memory before a reporting serialization failure; its software-fix rerun reused the frozen holdout and is not pristine independent confirmation.

Source: [`Phase 13G evidence package`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/evidence_package.md).
