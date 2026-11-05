# T2T-S1.4 — Strong Replay Stress-Test Specification

**ID:** `T2T-S1.4-StrongReplay-v1.0.0-draft`  
**Purpose:** prevent an invariant treatment from winning only because its replay comparator was artificially weak. This is a design specification; no baseline is implemented or evaluated here.

## Comparison question

For Claim N, the relevant comparison is **I0 versus R1**, not I0 versus raw replay. Counterexample-boundary updates stay disabled/frozen in both. A replay baseline that matches I0 is a substantive result against an invariant-specific increment, not a baseline failure to be relabeled after results.

## Required baseline envelope

All variants receive the exact same permitted source traces, source cutoff, normalized observable fields, target contexts, outer wrapper, prediction target/comparator, model/tool access, development opportunity, and declared resource opportunities. Build and select baselines using source/development information only; freeze artifacts before any held-out outcomes.

| Component | Strong replay must be allowed to do | Guard against straw-manning |
|---|---|---|
| Retrieval | Indexed exact/context-key retrieval; fixed similarity or typed-key lookup; deterministic candidate ranking and tie rules; same query features and retrieval budget as I0. | Do not restrict it to one arbitrary nearest trace if the shared interface permits a competent source-only index. |
| Compression | Lossless deduplication, run-length/delta encoding, shared subsequences, dictionary encoding, and removal of redundant repeated fields. | Charge storage, compile, and retrieval costs; compression may not discard information needed by the source checks. |
| Parameterization | Typed slot abstraction for repeated fields/actions/effects; deterministic rebinding from declared observable field/type/position correspondences, including new entity IDs where the schema permits. | Ambiguous or type-incompatible bindings must abstain; do not prohibit ordinary variable binding. |
| Procedure | Compile selected traces into bounded macros; use branches/control flow that were represented in source traces; use fixed source-context preconditions and exact/typed checks. | Include a competent compiler/authoring procedure, reviewed independently of I0's authors where feasible. |
| Prediction | Transport the aligned source effect through the fixed slot map and emit a prediction before action/result; abstain if no aligned effect or binding exists. | Use exactly I0's target, normalization, comparator, timestamp/order, and logging contract. |
| Optimization | Search baseline variants using a declared source-only criterion such as exact source reconstruction, description length, or source validation. | Never select R1 from target outcomes, hidden labels, or a metric chosen after results. |

## Baseline ladder

Retain component-level references and designate the strongest competent **eligible** replay variant as primary R1 before outcome access:

1. **R0 — Raw fixed trace:** exact sequence with source assumptions and stop-on-mismatch. Diagnostic only.
2. **R1-C — Compressed trace:** exact retrieval plus lossless deduplication/compression and common wrapper.
3. **R1-P — Parameterized replay:** R1-C plus typed slot binding, new-ID rebinding, and source-supported branch selection.
4. **R1-Max — Frozen source-only maximum:** best eligible R1-C/R1-P variant under identical construction/development and resource budgets, selected with a predeclared source-only criterion and independent competence review. This is the primary R1.

Report the ladder so any claimed increment can be located. Do not choose a weaker member after observing outcomes.

## Expressivity stress test

In addition to primary R1, document an **adversarial replay/compiler ceiling** before S2. Ask an independent reviewer to assess whether an ordinary trace compiler or bounded program representation can encode the proposed I0 relation from the same source evidence, without counterexample updates or target labels. The review should consider fixed field comparisons, slot equalities, state checks, and deterministic conditionals.

If a stronger relational script is admitted as a replay implementation under the agreed definition, include it as an additional stress comparator. If it reproduces I0's predictions under the same information/resources, Claim N has no demonstrated increment. If it is excluded because it directly instantiates the very relational rule under test, document the principled boundary before results and report the exclusion transparently. Do not simply declare any effective baseline “not replay” after it performs well.

This stress review does not redefine the primary R1 after outcomes. It diagnoses whether the proposed semantic distinction is operationally identifiable or merely a relabeling of a compact program/macro.

## Matching and freeze checklist

Before a future prototype test, record/freeze:

- source manifest, event cutoff, normalizer, observable inputs, and allowed annotations;
- retrieval query/index, ranking/tie behavior, top-k/candidate envelope, and retrieval compute;
- compression/parameterization/branching compiler version and source-only selection criterion;
- baseline authoring/review effort, model/tool access, token/call/compute/time budget, storage cap, and per-decision/action opportunity;
- target-effect schema, comparator, exact all-context scoring rule from S1.2, abstention handling, and common wrapper;
- immutable artifact hashes, reviewer disposition, and rules preventing target/hidden outcomes from changing a baseline; and
- all failures, no-predictions, invalid bindings, timeouts, retries, and fallback costs.

Numerical resource caps, acceptable cost trade-offs, and statistical thresholds remain **UNSET**. Use the P3/P5 resource-vector design; do not invent a composite or tune limits after outcomes.

## Pass/falsification interpretation

- If I0 does not exceed R1-Max on the S1.2 endpoint, Claim N fails its operational criterion in that test domain.
- If I0 beats R0 but not R1-Max, the gain is consistent with compression/parameterization/retrieval/ordinary engineering, not invariant-specific value.
- If the expressivity stress comparator reproduces I0, treat that as evidence that the proposed distinction is not identifiable against that program class.
- If R1 is under-resourced, weakly reviewed, or receives less source information/development opportunity, the comparison is invalid/inconclusive—not support for I0.
- If resource frontiers are unmatched or not frozen, report the test as descriptive only.

## Out of scope

No code, compiler, replay baseline, trace, environment, benchmark, ARC data, task IDs, split, evaluator, or run is created by this specification. Actual implementation belongs only to a separately authorized S2 plan, after the S1.1 minimum-claim decision is accepted.
