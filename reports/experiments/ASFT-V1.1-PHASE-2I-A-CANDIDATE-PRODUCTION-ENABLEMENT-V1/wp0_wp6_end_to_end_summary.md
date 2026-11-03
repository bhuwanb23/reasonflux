# Phase 2I-A Work Package Summary — WP0 through WP6

**As of:** 2026-11-03  
**Overall status:** WP0, WP1, WP2, WP4, WP5, and WP6 engineering deliverables are implemented and synthetic-tested. WP3 independent annotation is **not complete**. Therefore Phase 2I-A is **not fully complete**, the ARC candidate-production run remains **not authorized**, and Phase 3 remains blocked.

## Executive summary

The software and frozen configuration needed for a future paired R1/R3 diagnostic are substantially in place. The R3 grammar was owner-approved; the parser/search, common trace contract, runtime policy, synthetic HCC control, and fail-closed runner are implemented and tested. A commit-pinned remote 600-task AI-provisional family bundle has now been audited by hashes and source-packet identity. It is explicitly non-qualifying and does not replace WP3.

The remaining scientific prerequisite is a genuinely independent family annotation process: two separate human coders and a separate human adjudicator must code the 600 permitted discovery tasks from training demonstrations only. The remote AI policies cannot satisfy that requirement. No ARC candidate-production run has been performed.

## WP-by-WP status

| WP | Status | Work completed and evidence | What this does **not** establish |
|---|---|---|---|
| **WP0 — Specification lock** | **Complete** | Owner-approved R3 grammar addendum v1 records the prior ambiguity resolutions. The reflection mapping was also corrected by actual effect: R1 horizontal reflection flips left/right and pairs with R3 vertical-axis reflection; R1 vertical reflection flips top/bottom and pairs with R3 horizontal-axis reflection. | Does not authorize an empirical run or resolve the remaining external annotation and run-authorization gates. |
| **WP1 — R3 parser and bounded search** | **Complete** | Deterministic object parser, selectors/actions, canonical candidate IDs, enumeration and training-demonstration exact-fit search are implemented with the frozen cap of 10. Focused R3 contract tests: **11 passed**. | A finite-budget no-fit is only “not found within this language and budget”; it is not proof of ARC impossibility or full language coverage. |
| **WP2 — Common traces and adapters** | **Implemented and tested, with a disclosed integration limitation** | R1/R3 semantic adapters, effect-based reflection aliases, zero-offset move → identity mapping, a separate provenance sidecar, and an independent four-step semantic-trace validator are implemented. Synthetic parity uses the frozen WP4 miner. | The full four-event fixture may yield zero candidates because common control events can overaggregate under the frozen `min_core_length=1` setting. That parity test is not a positive-yield test. WP5’s action-only miner fixture does not prove full production trace-to-candidate integration. |
| **WP3 — Independent family annotation** | **Not complete; held** | The ontology/protocol and two blank, train-only packets for the 600 discovery IDs are prepared. The latest remote bundle at commit `eb3c6a2cb04afe6a7289e30e7141fdec9b64fa99` adds blinded review packets, but its manifest reports **0 human reviews** and **0% human-gate completion**. All 14 declared output hashes match; the family-map SHA-256 is `79e92048b6c840deaf04d9a0136d9c09304789effac51ced32f5fa1d024123bd`. | The label streams remain `AI_PROVISIONAL`; all 600 coder and adjudicator rows are `UNREVIEWED`, with empty reviewer IDs, timestamps, and sign-offs. The map remains `PROVISIONAL_NOT_ADJUDICATED_BY_HUMAN`; the remote review packets are prompts for future review, not completed human coding. WP3 remains incomplete. |
| **WP4 — Frozen policy and identity** | **Complete** | Owner-approved runtime config and factory, structural eligibility diagnostic, family-excluded identity policy, arm-separated ledger, and collision checks are implemented. Focused runtime tests: **5 passed**. Frozen settings: support/cross-trace **5/5**, max fragment **4**, min core **1**, successful-trace bias on, consistency **1.0**, minimum **2** families, generality floor **0**, transfer-evidence gate off. | Does not supply independent family labels or promote candidates. Transfer-typed candidates may pass the Phase 2I structural diagnostic without promotion. |
| **WP5 — Synthetic HCC control** | **Implemented and tested; synthetic only** | `ASFT-2I-HCC-SYNTH-V1`: **120** in-memory tasks, six rules with 20 tasks each, three synthetic layout cohorts, and **240** exact demonstration checks per arm. Both arms produced six matching generator-accepted and structurally eligible candidates in the isolated miner control. HCC-to-ARC namespace rejection is tested. | Candidate mining uses oracle-selected one-action fixtures. It does not test actual R1/R3 search coverage, full four-event integration, ARC candidate yield, or scientific performance. |
| **WP6 — Runner, logs, and provenance** | **Implemented and synthetic end-to-end tested** | Registered R1/R3 search adapters; explicit task-ID-file interface; path-confined streaming train-only source; 10-trial and task/demo/grid caps; per-search time and worker address-space limits; train-demo, family-map, and code hashes; opaque trial/candidate IDs; stage ledger; paired ID/budget checks; HCC exclusion; and exact output-file/field/hash audit. Synthetic file → search → trace validation → miner → artifact audit tests pass. ARC mode requires a separate run-specific authorization bound to the run’s hashes. | No ARC source map, independently frozen WP3 family map, or run authorization was supplied. No real ARC files were opened and no actual ARC output artifacts exist to audit. |

## Remote WP3 review-bundle audit

The latest source bundle is pinned in `package_manifest.json` to GitHub commit `eb3c6a2cb04afe6a7289e30e7141fdec9b64fa99`; no duplicate review packets are retained locally. All **14/14** output hashes declared in its manifest match the downloaded files, and the local train-only source packet matches the bundle's source SHA-256. The updated task-family map SHA-256 is `79e92048b6c840deaf04d9a0136d9c09304789effac51ced32f5fa1d024123bd`.

The new files are **human-review packets**, not completed human annotations. The manifest reports **0 reviews**, **0% human-gate completion**, 600/600 tasks missing complete A/B human reviews, and no role-C human adjudication records. Direct CSV inspection confirms A/B labels and adjudication remain `AI_PROVISIONAL`; every A/B/C/map row is `UNREVIEWED`, with reviewer IDs, timestamps, and sign-off hashes empty. The 600-task coverage and descriptive AI-policy agreement do not satisfy WP3. No AI draft is promoted, and Phase 2I remains unauthorized.

## Verification and provenance

- Combined synthetic regression suite: **68 passed**.
- R3 focused contract suite: **11 passed**.
- Package finalizer: **PASS**, with **15/15** required local package artifacts present after removing the superseded local AI-pilot files.
- Provenance verification: **52/52** recorded SHA-256 entries match.
- Test data used for new plumbing checks: synthetic fixtures and the prepared train-only annotation packets; the remote AI-provisional bundle was hash-audited but its labels were not used by the runner or Phase 2I.

## Current decision and next dependency

- **Phase 2I ARC candidate production:** not run and not authorized.
- **Phase 3:** blocked.
- **Next required step:** obtain two genuinely independent coders and a separate adjudicator to complete the 600-task train-only annotation protocol. Then freeze and hash that human-adjudicated map, finish the run-specific protocol/review, and obtain separate authorization before any ARC run.

A Phase 2I-A completion review should wait until WP3 is genuinely complete. No pilot label or synthetic result may be substituted for that gate.
