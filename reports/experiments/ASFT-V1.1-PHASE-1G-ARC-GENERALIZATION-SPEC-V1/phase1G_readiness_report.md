# ASFT v1.1 Phase 1G — Readiness Report

**Phase ID:** `ASFT-V1.1-PHASE-1G`  
**Package:** `ASFT-V1.1-PHASE-1G-ARC-GENERALIZATION-SPEC-V1`  
**RQ6:** Can the invariant → skill → transfer → capability chain activate on ARC under a protocol-conformant representation with measurable downstream benefit?

## Executive decision

- **PASS for specification layer.**
- **PASS for contract layer — 42/42 checks.**
- **BLOCKED for empirical execution.**
- **RQ6 untested.**

No ARC search, task evaluation, confirmatory or replication outcome, or new ARC score was generated. Contract fixtures are code-path tests only and are not empirical evidence.

## Historical ARC audit

Phase 13G evaluated 1,000 public ARC-AGI-2 training task IDs in 600/200/200 discovery/transfer/holdout splits. The ten-program DSL achieved full-inventory exact demo fits of 3/600, 5/200, and 2/200 respectively; the frozen config declared three candidates per task while `discover()` defaulted to ten. All 600 discovery trace rows were schema-valid, but only three were successful exact-demo-fit traces. The invariant miner had zero raw patterns/candidates with a minimum support of five; no support-qualified skill pool or skills formed. Learned-skill transfer denominator was zero (transfer unavailable); bounded ASFT exact transfer-task accuracy was 0/200. There were zero capability groups, so C_t/CGR/IG were unavailable. Holdout exact accuracy was 1/200 for all five arms, but the same holdout was reused after attempt 01 generated predictions in memory; it was not pristine independent confirmation. A B2 nearest-episode memory arm solved 1/200 transfer tasks, which is not ASFT skill transfer.

Phase 14G identifies low bounded-DSL coverage plus support thresholds as the dominant proximate bottleneck, while saying representation is not uniquely proven as cause. Phase 14H/14I/14J conclude ARC did not validate or falsify ASFT theory; downstream mechanisms were untestable under the observed coverage and gates. A temporary archive containing evaluation blobs was downloaded during reconnaissance; only filenames were listed and the archive deleted. The official evaluation JSON was not extracted, parsed, scored, or used as feedback. The downloaded-archive deviation remains disclosed.

## Failure map and scope

The package records every stage separately: ingestion, budgeted/full-scan representation coverage, valid/successful traces, invariant candidates, skills, eligible transfer, external capability units, and exact/partial/family accuracy. A zero count can mean observed non-activation; an absent denominator is unavailable; inadequate support is inconclusive. Coverage is demo-fit under a frozen representation/budget, not task accuracy. Accuracy is evaluator-scored held-out output, not coverage or transfer. The formal cascade is `arc_failure_cascade.csv`.

## Construct and protocol independence

**Q1: Can coverage be measured independently of accuracy? YES.** Coverage uses training demonstrations and candidate search only; test gold is excluded. Separate code functions and contracts test coverage, exact accuracy, partial pixel accuracy, and family accuracy.

**Q2: Can the benchmark localize a chain break? YES, by specification and stage contracts.** Stage states include `activated`, `not_activated`, `inconclusive`, and `unavailable`; downstream unavailable states do not erase the observed upstream break.

**Q3: Can activation fail? YES.** The contracts admit fully activated, not-activated, mixed, inconclusive, and unavailable profiles.

**Q4: Does it prevent known protocol failures? Specified and contract-checked, not production-audited.** Config/runtime parity, explicit diagnostic-only full scans, holdout one-time use, evaluation isolation, and failure logging are mandatory. The contracts reject the known mismatch/reuse scenarios.

**Q5: Can representation be found not to be the primary bottleneck? YES, conditionally.** The protocol requires adequate budgeted coverage and downstream opportunities, ideally across the historical adapter and a materially distinct, independently justified representation variant or high-coverage reference condition. If invariant/skill/transfer stages remain inactive with adequate coverage/support, the break localizes downstream. If adequate coverage never occurs, representation is not exonerated and the cause remains unresolved.

## Readiness gates

| Gate | Status | Evidence / remaining work |
|---|---|---|
| Gate 1 — Contracts | **PASS, interface scope** | 42/42 stage separation, denominator, budget, holdout, and integrity checks. |
| Gate 2 — Coverage framework | **PASS specification/contract** | Budgeted/full-scan coverage distinct from accuracy; zero vs unavailable rules. |
| Gate 3 — Representation audit | **PASS specification; implementation pending** | Historical DSL and limitations documented; alternate/reference representation not built. |
| Gate 4 — Activation definitions | **PASS specification/contract** | Stage-wise activation, non-activation, inconclusive, unavailable; no forced positive result. |
| Gate 5 — ARC task runner | **PENDING** | No v1.1 search/annotation/evaluator implementation or outcomes. |
| Gate 6 — Frozen analysis | **PENDING** | Exact representation, task splits, thresholds, sample size, baselines, and uncertainty rules need development calibration and lock. |
| Gate 7 — Replication | **SPECIFIED; NOT GENERATED** | Disjoint tasks/templates/seeds required; no replication run. |
| Gate 8 — Protocol integrity review | **PASS contract; production audit pending** | Synthetic checks catch config mismatch and holdout reuse; sealed-gold/access controls not implemented. |
| Empirical authorization | **BLOCKED** | This specification does not authorize ARC confirmatory runs, Phase 3/IDT, or SCT experiments. |

## Final decision

> Phase 1G has a diagnosable, stage-separated ARC benchmark specification and passing contracts. It does not show that ASFT works on ARC, that representation caused the earlier failure, or that transfer/capability will emerge. The benchmark is designed to identify whether failure occurs at coverage, trace generation, invariant discovery, skill formation, transfer, capability formation, or task accuracy—and does not assume representation is the sole bottleneck.