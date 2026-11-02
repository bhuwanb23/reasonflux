# Phase 1G.1 — Historical ARC Failure Audit

**Sources:** Phase 13G evidence package, Phase 14G failure/cascade/representation audits, Phase 14H causal-chain review, Phase 14I validity analysis, Phase 14J final scorecard/conclusions. Read-only; no run was repeated.

## Executive verdict

Phase 13G demonstrated that the **tested bounded ARC adapter did not activate the ASFT chain**. It did not demonstrate that ASFT succeeds on ARC, and it did not falsify IDT/SCT/transfer/CGM as general theories. The first observed bottleneck was extremely low task-to-program fit coverage in a ten-program symbolic DSL, compounded by a support threshold. The representation explanation is a strong proximate implementation diagnosis, not an established unique cause.

## What happened in Phase 13G

- Dataset: 1,000 ARC-AGI-2 public training task IDs split 600 discovery / 200 transfer / 200 holdout. Official evaluation JSON was not extracted, parsed, scored, or used for feedback. A temporary archive containing evaluation blobs was downloaded during reconnaissance; only filenames were listed; it was deleted. Do not claim no evaluation bytes were ever downloaded.
- Representation: ten fixed primitive programs: identity; horizontal/vertical reflection; three rotations; transpose/anti-transpose; constant translation; bijective recoloring. Full-inventory exact demonstration fit was 3/600 discovery, 5/200 transfer, and 2/200 holdout. These are fit/coverage counts, not test accuracy.
- Budget discrepancy: frozen config/preregistration says three candidates per task, while the discovery function defaults to ten. Thus 3/600 is a full-inventory discovery scan, not the yield at the declared scored-arm budget. Only `reflect_vertical` among the three fitted discovery programs is in the first three fixed programs. This is source/results audit, not a rerun.
- Traces: 600/600 discovery rows are schema-valid; only three contain successful exact-demo-fit traces, one each for reflection, rotation, and recoloring. A valid failure trace is not a successful program trace.
- Invariants: the miner saw three successful traces, each program with support one, while minimum frequency and cross-trace support were five. It produced zero raw patterns/structures/candidates. There was no meaningful diverse candidate contest.
- Skills: support-qualified program pool was empty; 0 eligible programs and 0 promoted skills. Skill formation was mechanically blocked by upstream evidence/thresholds.
- Transfer: learned-skill applicability denominator was zero, so skill-transfer precision is unavailable, not zero. ASFT exact task transfer accuracy was 0/200 within the bounded solver. The B2 episodic-memory arm solved 1/200 transfer tasks; this was nearest-episode reuse without invariant abstraction, not ASFT skill transfer.
- Capability/growth: zero validated capability groups; C_t/CGR/IG unavailable in every prefix, not zero growth or evidence of no intelligence.
- Accuracy: ASFT holdout exact task accuracy was 1/200 (0.005); all five arms were 1/200 on the same holdout. Attempt 01 generated predictions in memory before report serialization failed; attempt 02 repaired serialization but reused the same frozen holdout. It is not independent replication or pristine holdout confirmation.
- Reporting defect: Phase 13G growth output labels discovery-prefix sizes 100–600 as `n_successful_traces`; those values are prefix lengths, not verified successful-trace counts. The saved discovery evidence has only three successful exact-fit traces. Treat the label as a known implementation/reporting bug, not as additional trace evidence.

## Formal failure cascade

See `arc_failure_cascade.csv` for each stage, status, denominator, and interpretation. The critical sequence is:

**bounded program coverage (3/600) → only three successful traces → zero supported invariant candidates → no eligible skills → learned-skill transfer unavailable (while bounded ASFT task accuracy is measured and poor) → no capability groups/metrics available.**

Task loading and trace schema succeeded. The issue was not generic file ingestion or serializer failure; most valid traces encode failed search under a small DSL.

## What was not shown

- **“ASFT fails on ARC” as a theory-wide claim:** not shown. The tested adapter had very low representation coverage and could not activate downstream stages.
- **“Representation caused everything” or is the unique/primary causal root:** not shown. Representation and program budget interacted; no factorial comparison of language expressivity, search, support thresholds, and downstream mechanisms isolated causes.
- **“The representation was the only bottleneck”:** not shown. The threshold gate and tiny successful trace diversity also block discovery; later stages cannot be assessed.
- **“ASFT succeeds on ARC”:** not shown. The current adapter did not activate skills/capabilities and had 0/200 transfer accuracy, with 1/200 holdout exact accuracy shared by all arms.
- **“Transfer/capability is zero”:** not measured for learned skills/capability because denominators/groups were absent. Status is unavailable.

## What Phase 14 concluded

Phase 14G diagnoses a strong *proximate* representation/coverage bottleneck and calls out the budget discrepancy; it explicitly says representation is not proven to be the unique cause. Phase 14I classifies ARC external validity as very high risk and restricts inference to the bounded adapter. Phase 14H/14J conclude the mechanism chain is not validated externally and the ARC test is neither theory validation nor theory falsification.

## How Phase 1G prevents a repeat

- Bind config and runtime candidate budgets through one versioned configuration and automated parity checks; record actual candidate trials per task/arm.
- Permit full-inventory scans only as separately labeled diagnostic coverage, never as scored-arm performance or budget-compliant discovery.
- Lock discovery/transfer/holdout manifests and gold before any prediction; no holdout reuse for tuning, debugging, or reruns.
- Score coverage, traces, invariant candidates, skills, transfer, capabilities, and exact/partial accuracy in separate tables with independent denominators.
- Record all failed searches, rejected candidates, negative transfer, unavailable denominators, and reasons.
- Include representation variants and/or a predeclared adequacy check so the benchmark can find downstream failure even when coverage is adequate; it does not assume representation is the sole bottleneck.

**Audit conclusion:** the current ARC adapter failed to activate the chain and did not validate ASFT. The cause is not fully isolated. Phase 1G must report stage-by-stage results and remain able to conclude that representation is *not* the primary bottleneck.