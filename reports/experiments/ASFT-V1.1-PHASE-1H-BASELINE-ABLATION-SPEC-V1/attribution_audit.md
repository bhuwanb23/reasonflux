# Phase 1H — Attribution Audit

## Question

When ASFT improves an endpoint, when can the improvement be attributed to a named component rather than memory, frequency, compression, opportunity, benchmark design, or another mechanism?

## Minimum attribution chain

A component-level contribution claim requires all of the following:

1. **Frozen claim and endpoint:** the mechanism, direction, primary outcome, SOI, analysis unit, and comparator family are preregistered.
2. **Fair comparator:** same tasks/splits, candidate pool when relevant, budget/storage/compute caps, horizon/exposure, evaluator, and config/runtime parity.
3. **Mechanism activation:** show that the component actually fires and changes a decision or system state; record activation and decision-divergence rates.
4. **Manipulation validity:** the ablation disables only the declared component (or reports direct downstream consequences); logs prove the change occurred.
5. **Causal contrast where claimed:** randomize/assign the component or policy at the independent unit, use paired/common tasks, preserve the frozen endpoint, and compare to the mapped ablation and surviving baseline alternatives.
6. **Uncertainty and replication:** cluster at the actual independent unit; report win/tie/loss/inconclusive/unavailable; replicate before broad claims.

If these conditions do not hold, report a descriptive arm difference, not a causal mechanism attribution. Correlation, positive internal score movement, or beating a single weak baseline is insufficient.

## Attribution levels

- **Metric observation:** score or internal metric changed; no behavior/theory conclusion.
- **System-level performance contrast:** one full policy differs from a baseline on a frozen endpoint under fair conditions; not component-specific unless manipulation isolates it.
- **Local component contribution:** verified removal changes a behavioral endpoint under active, matched conditions; supports contribution only in that tested setting.
- **Mechanism superiority:** component/policy beats all relevant stronger alternatives, with informative divergence and replicated benefit; still bounded to population/benchmark.
- **Theory validation:** requires an independently validated construct and generalization beyond the tested mechanism; not supplied merely by Phase 1H governance.

## Specific confounds and required response

- **Memory/retrieval:** report B2 subtypes and opportunity counts. In 13C, MEMORY_ONLY attempted 440 vs SCT 223 opportunities; net value combines match rate and correctness. This is a serious alternative, but not a matched quality-per-attempt estimate.
- **Frequency/compression:** retain them as live competitors; a proxy tie/win is comparator-specific and does not test every family member.
- **Selection degeneracy:** if all candidates are selected or all rankers choose the same set, classify selection attribution non-informative.
- **Budget/pool drift:** config/runtime mismatch or different candidate pools invalidate a direct ranking attribution.
- **Internal metric substitution:** a change in C_t/CGR/IG after removing a measurement layer is not a behavior-level causal effect.
- **Downstream cascade:** when an upstream removal disables all descendants, report both the total-system cascade and stage-specific outcomes; do not claim each downstream component independently caused the endpoint change.

## Component-existence rule

> The presence of a component in the architecture is not evidence that it is necessary or beneficial. Each component may show positive contribution, no measurable contribution, negative contribution, or unavailable contribution under the specified benchmark. The benchmark permits all four outcomes.