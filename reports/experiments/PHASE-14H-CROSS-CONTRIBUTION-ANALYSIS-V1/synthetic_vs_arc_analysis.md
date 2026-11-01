# Synthetic-vs-ARC Chain Analysis

## Synthetic evidence

The controlled synthetic runs use a bounded and known operation vocabulary. They provide evidence for repeated operation-signature detection (13B), construction of reflection/rotation skill objects (13C), some successful skill reuse and simulator step-cost reduction (13C/13D), and computable capability/growth metrics (13E/13F). Evidence strength is narrow at each stage: expected labels share vocabulary with the generator, SCT selection ties always/random creation, raw memory retrieval is a strong alternative in 13C, and growth results vary across phases and metrics.

The defensible synthetic subchain is:

`experience → recurring operation-level patterns → stored reflection/rotation skills → some successful reuse / step-cost proxy reduction`

The bridge from transfer to capability growth is not established; the capability-to-intelligence interpretation is not validated.

## ARC-AGI-2 bounded implementation

Phase 13G uses 600 discovery, 200 transfer, and 200 holdout tasks from the public training split and a ten-program fixed DSL. Full-inventory exact demonstration fits are 3/600, 5/200, and 2/200. These are demo-fit coverage—not test-task accuracy or semantic ARC family counts. All 600 discovery trace records are schema-valid, but only three are successful exact-fit traces, and the invariant miner returns zero candidates.

The budget audit adds an important protocol/implementation qualification: the frozen config says three candidates per task, but the saved `discover()` function defaults to ten. Only the `reflect_vertical` fit among the three observed successful discovery programs is in the first three fixed candidates. The 3/600 result is therefore a full-inventory yield, not a yield under the declared three-candidate limit.

With zero invariants, ASFT skills and capabilities do not form. Consequently, learned-skill transfer precision is unavailable; ASFT transfer task accuracy is 0/200. B2's one transfer success is an episodic-memory event, not learned ASFT transfer. All five arms score 1/200 on holdout, with the same-holdout retry caveat.

## What the contrast means

ARC's first observed break is **upstream**: bounded program coverage and successful trace yield, followed by the invariant support gate. Later stages are not separately tested once no invariant candidates are available. The run establishes failure of this ARC implementation to activate the chain. It does not establish that downstream mechanisms would fail if a richer, properly budgeted representation produced sufficient data, and it does not establish that they would succeed.

## Comparison table

| Stage | Synthetic | ARC bounded adapter |
|---|---|---|
| Experience → patterns | Narrow repeatable operation signatures in known generator | Most tasks fail full-DSL exact-demo fit; trace records valid but successful fits rare |
| Patterns → skills | 44 reflection/rotation skill instances in 13C | 0 skills; no invariant candidates |
| Skills → transfer | Positive reuse and cost-proxy results in constrained synthetic tasks | Learned-skill denominator zero; ASFT exact transfer accuracy 0/200 |
| Transfer → capability | Not causally established; phase-specific CGR results mixed | No capabilities; downstream link unavailable |
| Capability → intelligence | Indices computed; construct validity not established | IG/CGR unavailable due no validated capability group |

**Boundary:** the ARC result is not an official evaluation score and cannot alone establish or falsify IDT, SCT, transfer theory, CGM, or intelligence-growth claims.
