# Phase 2I-A Work Package Summary — WP0 through WP6

**As of:** 2026-11-03  
**Overall status:** WP0, WP1, WP2, WP4, WP5, and WP6 engineering deliverables are implemented and synthetic-tested. WP3 independent annotation is **not complete**. Therefore Phase 2I-A is **not fully complete**, the ARC candidate-production run remains **not authorized**, and Phase 3 remains blocked.

## Executive summary

The software and frozen configuration needed for a future paired R1/R3 diagnostic are substantially in place. The R3 grammar was owner-approved; the parser/search, common trace contract, runtime policy, synthetic HCC control, and fail-closed runner are implemented and tested. A separate AI-only pilot was run to stress-test the family rubric, but it is explicitly non-qualifying and does not replace WP3.

The remaining scientific prerequisite is a genuinely independent family annotation process: two separate coders and a separate adjudicator must code the 600 permitted discovery tasks from training demonstrations only. The AI pilot cannot satisfy that requirement. No ARC candidate-production run has been performed.

## WP-by-WP status

| WP | Status | Work completed and evidence | What this does **not** establish |
|---|---|---|---|
| **WP0 — Specification lock** | **Complete** | Owner-approved R3 grammar addendum v1 records the prior ambiguity resolutions. The reflection mapping was also corrected by actual effect: R1 horizontal reflection flips left/right and pairs with R3 vertical-axis reflection; R1 vertical reflection flips top/bottom and pairs with R3 horizontal-axis reflection. | Does not authorize an empirical run or resolve the remaining external annotation and run-authorization gates. |
| **WP1 — R3 parser and bounded search** | **Complete** | Deterministic object parser, selectors/actions, canonical candidate IDs, enumeration and training-demonstration exact-fit search are implemented with the frozen cap of 10. Focused R3 contract tests: **11 passed**. | A finite-budget no-fit is only “not found within this language and budget”; it is not proof of ARC impossibility or full language coverage. |
| **WP2 — Common traces and adapters** | **Implemented and tested, with a disclosed integration limitation** | R1/R3 semantic adapters, effect-based reflection aliases, zero-offset move → identity mapping, a separate provenance sidecar, and an independent four-step semantic-trace validator are implemented. Synthetic parity uses the frozen WP4 miner. | The full four-event fixture may yield zero candidates because common control events can overaggregate under the frozen `min_core_length=1` setting. That parity test is not a positive-yield test. WP5’s action-only miner fixture does not prove full production trace-to-candidate integration. |
| **WP3 — Independent family annotation** | **Not complete; held** | The ontology/protocol and two blank, train-only packets for the 600 discovery IDs are prepared. A separate 12-task AI pilot was completed for rubric stress-testing only. It found **4/12** agreement between two prompts and descriptive κ **0.232**; the AI synthesis marked **4/12** ambiguous. | The AI passes and synthesis are from the same assistant, not independent coders or an independent adjudicator. They are not frozen labels and cannot enter family eligibility, candidate generation, Phase 2I, or Phase 3. WP3 remains incomplete. |
| **WP4 — Frozen policy and identity** | **Complete** | Owner-approved runtime config and factory, structural eligibility diagnostic, family-excluded identity policy, arm-separated ledger, and collision checks are implemented. Focused runtime tests: **5 passed**. Frozen settings: support/cross-trace **5/5**, max fragment **4**, min core **1**, successful-trace bias on, consistency **1.0**, minimum **2** families, generality floor **0**, transfer-evidence gate off. | Does not supply independent family labels or promote candidates. Transfer-typed candidates may pass the Phase 2I structural diagnostic without promotion. |
| **WP5 — Synthetic HCC control** | **Implemented and tested; synthetic only** | `ASFT-2I-HCC-SYNTH-V1`: **120** in-memory tasks, six rules with 20 tasks each, three synthetic layout cohorts, and **240** exact demonstration checks per arm. Both arms produced six matching generator-accepted and structurally eligible candidates in the isolated miner control. HCC-to-ARC namespace rejection is tested. | Candidate mining uses oracle-selected one-action fixtures. It does not test actual R1/R3 search coverage, full four-event integration, ARC candidate yield, or scientific performance. |
| **WP6 — Runner, logs, and provenance** | **Implemented and synthetic end-to-end tested** | Registered R1/R3 search adapters; explicit task-ID-file interface; path-confined streaming train-only source; 10-trial and task/demo/grid caps; per-search time and worker address-space limits; train-demo, family-map, and code hashes; opaque trial/candidate IDs; stage ledger; paired ID/budget checks; HCC exclusion; and exact output-file/field/hash audit. Synthetic file → search → trace validation → miner → artifact audit tests pass. ARC mode requires a separate run-specific authorization bound to the run’s hashes. | No ARC source map, independently frozen WP3 family map, or run authorization was supplied. No real ARC files were opened and no actual ARC output artifacts exist to audit. |

## AI pilot boundary

The pilot is in `wp3_ai_pilot_v1/`. It exists only to find rubric ambiguities and test whether category distinctions are usable. Its agreement numbers are prompt-sensitivity measurements from one AI assistant—not reliability evidence. The pilot does **not** change the frozen independent-coding requirement, create a family map, or count toward WP3 completion.

## Verification and provenance

- Combined synthetic regression suite: **68 passed**.
- R3 focused contract suite: **11 passed**.
- Package finalizer: **PASS**, with **21/21** required package artifacts present.
- Provenance verification: **58/58** recorded SHA-256 entries match.
- Test data used for new plumbing checks: synthetic fixtures and the already prepared train-only packet for the explicitly non-qualifying AI pilot.

## Current decision and next dependency

- **Phase 2I ARC candidate production:** not run and not authorized.
- **Phase 3:** blocked.
- **Next required step:** obtain two genuinely independent coders and a separate adjudicator to complete the 600-task train-only annotation protocol. Then freeze and hash that human-adjudicated map, finish the run-specific protocol/review, and obtain separate authorization before any ARC run.

A Phase 2I-A completion review should wait until WP3 is genuinely complete. No pilot label or synthetic result may be substituted for that gate.
