# Phase 1G / RQ6 — Preregistration Template

**Status:** design template; no empirical ARC run is authorized.

## Protocol identity and representation

- Protocol version/date and preregistration timestamp: `[complete before confirmation]`
- ARC dataset/source, license, split manifests, task IDs, and SHA-256: `[complete]`
- Representation/DSL version and semantic test suite hashes: `[complete]`
- Search algorithm, candidate ordering, deduplication, timeout, compute caps: `[freeze]`
- Per-task candidate budget in config and runtime: `[same frozen integer; parity assertion]`
- Any full-inventory scan: `[declare as diagnostic and exclude from scored-arm budgeted outcomes]`
- Failure reason taxonomy/schema: `[freeze]`

## Stage measures and thresholds

- Budgeted demo-fit coverage definition/denominator: `[freeze]`
- Full-inventory diagnostic coverage definition: `[freeze separately]`
- Trace schema, successful trace/replay, diversity, and discovery-yield rules: `[freeze]`
- Invariant candidate definition, validation pool, annotations, recurrence/support threshold, survival: `[freeze]`
- Skill formation/promotion/survival thresholds and resource costs: `[freeze]`
- Transfer eligibility, attempts, utility conversion, negative-transfer and zero-denominator rule: `[freeze]`
- Capability behavioral definition: Phase 1E external criteria; ARC-adapted thresholds and minimum N: `[freeze from development only]`
- Exact/partial/family accuracy definitions and confidence intervals: `[freeze]`
- Stage activation/not-activated/inconclusive/unavailable rules: `[freeze]`

## Arms, baselines, and budgets

- ASFT implementation/version: `[hash]`
- B1 fixed-order/no-learn search: `[definition]`
- B2 nearest-episode memory retrieval (not full exact-answer replay): `[definition]`
- B3 random selection/order among same qualified pool: `[definition]`
- B4 exact trace-signature compression proxy (not canonical DreamCoder): `[definition]`
- Random/chance and any external reference solver: `[definition]`
- Per-arm candidate, compute, memory, context, query, and wall-time limits: `[freeze identical or explain matched estimand]`
- Candidate trials, actual resources, and attempted task counts: `[runtime counter/hash]`

## Split, holdout, and evaluator lock

- Development/discovery manifest: `[hash]`
- Confirmatory transfer and holdout manifests: `[hash]`
- Independent replication manifest: `[disjoint task IDs/templates/seeds/domains]`
- Gold store custodian, access controls, evaluator blinding, and audit log: `[complete]`
- Holdout one-time evaluation schedule and lock time: `[complete]`
- Official/private evaluation access: `[none unless separately authorized and logged]`
- Duplicate/near-duplicate detection across splits: `[code and results]`

## Primary/secondary endpoints and inference

- Primary RQ6 estimand: `[freeze; report mechanism activation and paired task utility]`
- Stage-specific metrics/denominators: coverage, trace, candidate/invariant, skill, transfer, capability, accuracy: `[freeze]`
- Smallest effects/adequacy and cluster-aware uncertainty method: `[freeze from development only]`
- Independent unit (task ID) and nesting/cluster structure: `[freeze]`
- Missingness, unsupported tasks, failure and exclusion rules: `[freeze]`
- Baselines and multiplicity plan: `[freeze]`

## Outcome-response and interpretation commitments

- `activated`, `not_activated`, `inconclusive`, and `unavailable` definitions per stage: `[freeze]`
- Overall outcome labels: `supported` only if the entire chain activates with preregistered downstream behavioral utility and replication; `not activated under this protocol` if adequate evidence localizes a stage break; `inconclusive` if denominators/support are inadequate; `unavailable` if data/integrity fails. None alone is a theory-wide falsification: `[freeze]`
- Coverage-high/accuracy-low and other mixed profiles remain reportable: `[confirm]`
- Zero invariant count is not theory failure; zero eligible transfer denominator is unavailable: `[confirm]`
- Representation is a hypothesis; state what evidence would show downstream break despite adequate coverage: `[freeze]`
- No outcome-driven representation, budget, or threshold changes.

## Integrity and signatures

- C1 config/runtime budget parity: `[automated test PASS]`
- C2 sealed holdout single-use/replication split: `[audit PASS]`
- C3 evaluation isolation / no test gold or forbidden metrics: `[audit PASS]`
- C4 coverage/accuracy/stage transparency: `[schema validation PASS]`
- C5 failure logging completeness: `[audit PASS]`
- Independent preregistration reviewer, data custodian, and implementation owner: `[signatures]`
- Empirical authorization/readiness decision: `[separate approval; not granted by this template]`