# Phase 2I — Candidate Eligibility Contract

## Ranked object remains unchanged

The only candidate object eligible for the original RQ1 is a generated `Invariant` hypothesis from the trace-mining candidate-generation stage. The Phase 1C/production R1 score still ranks invariant candidates. No trace fragment, `MinedPattern`, `AggregatedStructure`, solver program, `SkillCandidate`, `Skill`, or `Capability` may be relabeled as an invariant to create a population.

## Status ladder (do not collapse)

`trace → fragment → mined pattern → aggregated structure → invariant proposal → generation-accepted invariant → structurally qualified invariant → calibration-feature-ready/rankable invariant → transfer-verified/promotion/skill states`.

Phase 2I's candidate-production success is counted at the **generation-accepted invariant** stage, with structural qualification reported separately. Transfer verification, skill promotion, and future value are downstream and are not population entry criteria for the candidate-yield diagnostic.

## Outcome-blind inclusion rules

A candidate counts as generation-accepted only if it:

1. is an `Invariant` object emitted by the frozen generator;
2. has a stable canonical ID and complete lineage to its source trace(s), task(s), representation version, and discovery split;
3. passes the selected pre-outcome recurrence/support and frozen rejection policy;
4. is deduplicated within its representation arm under the frozen canonical identity rule; and
5. is not selected or filtered using held-out task outputs, future utility, Oracle values, or a performance-based candidate quota.

Candidate feature coverage/availability is a separate field. T=0 with observed eligible calibration attempts is distinct from missing T due to no opportunities. No future transfer threshold is introduced to qualify candidates; otherwise the population would be selected on the target it is meant to evaluate.

## Fixed thresholds and implementation reconciliation

The candidate pipeline must use the Phase 2F preregistered downstream settings: support/frequency 5, cross-trace support 5, consistency 1.0, at least two independently assigned families, and the existing rejection policy. The current generic Python defaults are not interchangeable with the audited run config. Before any run, freeze code, `MiningConfig`, `InvariantPolicy`, identity implementation, and serialization hashes and verify the runtime is using those exact values. No support-floor relaxation or threshold search is permitted in the primary candidate-production run.

A family annotation must be assigned independently of the representation's chosen solver program. If no independently justified family map exists, the two-family eligibility rule is **unavailable**, not inferred from representation labels.

## Deduplication and identity risk

`InvariantIdentity` currently fingerprints normalized origin and pattern signature; its fingerprint payload does not include `task_families`, despite the dataclass storing them. Before use, owner review must confirm whether exact operation signature alone is the intended canonical identity across independently annotated families. Record both canonical ID and full family/source evidence so a hash collision or over-aggregation cannot be hidden.

## Current status

This contract is a Phase 2I run specification, not an execution result. The Phase 2I run is blocked until its code/config hashes, independent family annotations, and representation/trace adapters pass preflight. The historical Phase 2E rejected proposals do not count as eligible candidates.