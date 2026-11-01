# Causal Chain Analysis

## Question and verdict

The proposed sequence is `Experience → Invariant → Skill → Transfer → Capability Growth → Intelligence Growth`. The saved record supports the first three **as narrow synthetic pipeline behaviors**, but the full causal chain is not validated. The first major evidential break is **Transfer → Capability Growth**: reuse occurs, and capability scores rise in one synthetic cohort, but the evidence does not establish that transfer causes or reliably predicts those increases. The subsequent Capability → Intelligence link is also unvalidated.

This is not a claim that downstream metrics never rise. Phase 13E's mean CGR, IG, and IGR are positive within its ten-seed cohort. The claim is that their presence does not establish the proposed causal links.

## Link-by-link reconstruction

### C1 — Experience → Invariants: narrow synthetic support

Phase 13B reports the four expected synthetic operation-family signatures in 5/5 seeds, with IP/IR of 1.0 within the designed vocabulary. This demonstrates repeatable detection of operation-level signatures in a generator with known operations and overlapping labels. It does not establish blinded semantic discovery, open-ended abstraction, or a general law that experience alone creates invariants. Transfer-aware ranking also ties frequency-only and no-transfer on the primary corrected benchmark; the exploratory no-op stress test is not a pass on that superiority claim.

### C2 — Invariants → Skills: operational construction, not policy superiority

Phase 13C records 44 skill instances across ten confirmation seeds: 22 reflection and 22 rotation. Validated synthetic candidates are turned into stored skill objects. This is direct evidence that the pipeline can construct and retain those representations. But the selection policy did not discriminate in the primary confirmation set: all 44 eligible rows were selected; SCT, ALWAYS_CREATE, and RANDOM_CREATE tie at net value `0.345`. The evidence does not establish SCT/SCV necessity, unique policy value, or broad skill emergence.

### C3 — Skills → Transfer: narrow reuse and simulator-cost support

The Phase 13C ledger records 201 correct, positive-credit SCT applications among 223 applications (440 eligible opportunities); the 91/91 attempted cross-family results are restricted to the available reflection/rotation skill pool and generated cases. Mean normalized step reduction is `0.227` among correct applications. Corrected Phase 13D reports success-gated normalized RCR `0.149288` (95% interval `[0.131979,0.157943]`) and positive task-transfer utility in covered cells. This supports successful synthetic reuse and the repository's reasoning-step cost proxy—not wall-clock time, FLOPs, search reduction, broad transfer, or superiority to every baseline.

Memory-only retrieval also performs strongly in 13C, so the observed reuse benefit is not uniquely attributable to abstraction/skill construction.

### C4 — Transfer → Capability Growth: first major evidential break

- 13D mean CGR is `-0.060` across nine evaluable seeds. Its positive descriptive TS–CGR association (`r≈0.483`) coexists with that negative mean and does not establish causation.
- 13E has positive mean CGR (`0.2946`) but TS–CGR `r=-0.503` with a confidence interval spanning zero. Its no-SCT ablation has zero CGR contrast.
- 13F's no-transfer condition has higher task utility than ASFT by `0.036344`, while ASFT has a higher CGR by `0.287172`.

These results differ in phase, task stream, and endpoint. They do not form a consistent transfer-to-growth effect. The 13E preregistered `C_t`→next-round utility correlation (`r=0.0498`, CI `[0.0163,0.0922]`) is a distinct weak same-cohort association; it is not a mediation or transfer-to-growth test.

### C5 — Capability Growth → Intelligence Growth: construct link not validated

Phase 13E computes positive mean IG (`0.2294`) and IGR (`0.00904`), while IE has a negative slope. IG is a weighted composite of internal growth quantities, and IGR/IE are derived from it. No independent human, real-world, held-out-domain, or other external intelligence criterion is reported. Positive index values establish the arithmetic behavior of the frozen metric, not that intelligence grew.

## Why the chain is not validated by adjacent positive results

The evidence is spread across phases and protocols. Each phase has different candidate pools, tasks, outcomes, baseline policies, and metrics. The chain was not tested as a single randomized mediation sequence in which each transition is independently manipulated and downstream effects are measured on common held-out instances. A positive result at one link cannot be composed with an unrelated positive result at another to prove the full causal chain.

**Decision:** C1–C3 survive only in bounded synthetic operational language; C4 is the first missing causal bridge; C5 is unvalidated at the construct level. The conjunction required by the original ASFT theory is not established.
