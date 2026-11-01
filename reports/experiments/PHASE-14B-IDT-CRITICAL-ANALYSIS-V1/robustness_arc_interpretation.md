# IDT robustness and ARC interpretation

## Synthetic robustness

The saved Phase 13B diagnostics are mixed and must be reported metric by metric:

- **Variation survival (VST):** 1.0 under the tested synthetic variation/perturbation.
- **Rank stability:** 0.72 under the stored noise/stability diagnostic—moderate and imperfect, not invariance to noise generally.
- **Sparse-data behavior:** precision 1.0 but recall 0.20; mean IS 1.8 and mean candidate count 2.4. A high precision score therefore coexists with substantial missed expected signatures when evidence is sparse.

The positive VST result does not cancel the sparse-recall limitation. These are perturbations within synthetic-v1 and its known operation vocabulary; they do not test semantic distribution shift, new trace representations, unknown solvers, or external domains.

**Judgment:** partial, metric-specific robustness. Do not describe the full discovery process as broadly robust.

## Phase 13G bounded ARC adapter

Saved Phase 13G evidence reports three discovery traces, three exact-demo-fit tasks, zero accepted invariant candidates, zero promoted skills/capabilities, and unavailable IS–transfer / invariant-growth measures. The bounded DSL holdout exact-task accuracy was 0.005. Exact-demo-fit on the discovery side was only 3/600, below the frozen minimum support threshold of five; the adapter therefore had insufficient eligible support to promote an invariant under its current representation.

This is a **null result for the bounded ARC adapter**. It shows that the implemented trace→invariant pipeline did not demonstrate invariant discovery or transfer on this run. It does not establish that ARC as a whole contains no invariants or that unrestricted IDT cannot work on ARC. The result's external-validity force is constrained by DSL coverage, low exact-fit discovery coverage, and the post-software-fix reuse of the same holdout after the first attempt generated predictions in memory.

The source record also discloses that the temporary upstream archive included evaluation blobs; only filenames were listed, no evaluation JSON was extracted or parsed/scored, and the archive was deleted. Do not state that no evaluation bytes were ever downloaded.

## External-validity decision

- “ARC-level invariant discovery has not been demonstrated by this adapter” — supported.
- “This adapter provides evidence against unrestricted IDT as a theory” — not supported.
- “The ARC adapter has a substantial coverage/representation bottleneck” — supported as a limitation of this implementation.

**Source:** [`Phase 13G evidence package`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/evidence_package.md).
