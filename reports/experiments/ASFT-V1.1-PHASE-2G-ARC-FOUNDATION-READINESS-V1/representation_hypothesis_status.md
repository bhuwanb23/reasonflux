# Phase 2G.6 — Representation Hypothesis Status

## Classification: **H4 — Unresolved**

The evidence strongly supports the narrower statement that the **deployed bounded ten-program representation/search implementation had very low found-fit coverage** on the audited task set. It does not establish that representation was the primary causal bottleneck, or that a richer representation will activate ASFT mechanisms.

### Evidence in favor of representation as a contributor

- Phase 2A documents a whole-grid ten-program DSL with no explicit object/relation solution language or general composition.
- Phase 2B fullscan finds exact training-demo fits on 10/1,000 tasks (1.0%); Phase 2C S4 reproduces that finite-DSL rate.
- Phase 2D shows that successful trace supply is sparse, so the deployed end-to-end system does not build a rich mechanism substrate.

### Evidence against an automatic “representation was the cause” conclusion

- Under the same representation, Phase 2C coverage rises 2→5→10 per 1,000 as the candidate cap rises; search budget affects found-fit coverage.
- Phase 13G had a config/discovery budget mismatch and first-fit behavior; parameter inference and candidate order can mask fits.
- Phase 2E finds an independent support-threshold bottleneck: the current threshold5 is impossible given max observed support3. Relaxed patterns are generic control-flow traces, not established semantic invariants.
- Phase 2F has not implemented or tested any alternative; no paired representation effect is available.

### Status meaning

H4 does not mean representation is irrelevant. It means the primary causal question is not answered. Phase 2F makes the hypothesis falsifiable in principle, but R2–R7 implementations, HCC, fresh common task set, family annotations, and preregistered practical margins are still pending. No causal representation claim is permitted.