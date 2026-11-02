# Phase 1D / RQ3 — Preregistration Template

**Status:** design template; no run-specific fields are invented or confirmation authorized.

## Identity and frozen artifacts

- Protocol version/date: `[complete]`
- Task generator, base solver, arm implementations, evaluator code/version hashes: `[complete]`
- Development/confirmatory/replication task and seed manifests: `[complete]`
- Memory/abstraction payload schemas and canonicalization rules: `[complete]`
- Cost conversion coefficients and endpoint code hash: `[complete]`
- Storage/retrieval/exposure audit code hashes: `[complete]`
- Outcome store checksum, custodian, access log, and sealed-state proof: `[complete]`
- Exact independent panel N from calibration-only power/precision analysis: `[complete before confirmatory run]`

## Question, arms, and scope

**RQ3:** Does abstraction-only M4 improve held-out net utility over memory-only M1, M2, and M3 in non-exact challenge families B–F under common budgets?

**Secondary:** RQ3A memory sufficiency on A; RQ3B abstraction on B–F; RQ3C hybrid M5 versus each single representation; RQ3D transition across exact-repeat probability `p={0,.25,.50,.75,1}` and shift level `s={0,1,2,3}`.

- Arms: B1a M1, B1b M2, B1c M3, B2 M4, B3 M5, B4 random retrieval, B5 no learning, B6 Oracle post-lock only.
- Families A–F, including explicit allowlist of Family A repeat pairs: `[hash and list]`.
- Candidate/representation budget, storage, compute, retrieval and horizon caps: as `budget_matching_protocol.md`; run-specific values: `[freeze]`.

## Endpoint and primary family

- Primary endpoint: HNU macro-average across B–F, formula and units: `[freeze]`.
- Storage amortization, compute/retrieval costs, utility/partial-credit rubric, and coefficients λ: `[freeze using calibration only]`.
- Family A positive-control endpoint: report separately; not in primary B–F macro-average.
- SOI: `+0.10` normalized utility per task opportunity.
- Primary contrasts: B2−B1a, B2−B1b, B2−B1c; Holm-adjusted familywise alpha 0.05.
- Hybrid secondary contrasts: B3−B2 and B3−each B1 variant.
- Independent unit: paired panel/generator-seed cluster; not tasks or memory objects.

## Splits, leakage, and budgets

- Split assignments and disjointness hashes: `[complete]`.
- Every family in confirmatory and replication: `[verify]`.
- Family A planned exposure pairs and B–F no-exposure proof: `[complete]`.
- Storage/retrieval/exposure/Oracle audit logs and outcomes-store seal: `[complete before confirmation]`.
- Resource caps, actual-use counters, overrun policy: `[freeze]`.
- Missingness/exclusion rule and incident handling: as in `memory_metrics.md` and `leakage_control_protocol.md`.

## Sample size and inference

- Calibration-only panel variance/power/precision analysis and code/seed: `[complete]`.
- Final independent panel N: `[freeze]`.
- Paired cluster estimator, interval method, multiplicity code, transition model, and sensitivity analyses: `[freeze]`.
- No candidate/task-level pseudo-replication, interim efficacy peeking, or outcome-dependent stopping.

## Decision states

- **Supported:** B2−B1a/b/c adjusted lower 95% bounds all exceed SOI on B–F primary endpoint.
- **Contradicted at the SOI:** at least one adjusted upper 95% bound is below SOI; report comparator-specific result, not “memory always wins.”
- **Inconclusive:** valid data but intervals cross SOI or comparisons are mixed.
- **Unavailable:** leakage/budget/lock failure, invalid denominator, or missingness threshold breached.
- Hybrid and family-specific conclusions remain secondary unless separately preregistered.

## Signatures and lock

- Protocol author/reviewer/date: `[complete]`
- Independent data custodian confirms sealed future labels: `[complete]`
- Pre-outcome policy/budget/exposure lock timestamp and hashes: `[complete]`
- Outcome access timestamp/authorized evaluator: `[post-lock only]`
- Replication manifest and preregistration hash: `[complete before replication]`