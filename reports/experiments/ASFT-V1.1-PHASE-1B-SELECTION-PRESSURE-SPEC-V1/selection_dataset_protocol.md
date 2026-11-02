# 1B.8 — Selection Dataset & Split Protocol

## Dataset unit and layout

The independent unit is a **candidate-panel batch seed**. Each batch contains 20 candidates (four each of types A–E), a fixed capacity of eight, and ten held-out task opportunities per candidate lane. Candidate rows, task rows, and policy arms are nested/repeated within batch; they are not independent replicates.

Proposed immutable tables (generated only in later implementation/experiment phases):

- `batch_manifest`: split, batch ID, seed, generator/version, task schedule, K, horizon, hashes.
- `candidate_card`: selector-visible ID/features, feature provenance, technical eligibility, no hidden label.
- `candidate_truth_sealed`: latent type/expected value and oracle fields; separate access-controlled file.
- `task_manifest`: candidate lane, opportunity index/stratum, paired no-skill baseline task ID, seed, order, split.
- `selector_decisions`: policy/version, score/rank, selected flag, tie-break trace, pressure assertions.
- `outcome_ledger`: exact task results, paired baseline, resource use, FNV components, failures and availability.

Each selector card and outcome record has stable IDs. Outcome IDs never appear in cards, feature-generation filenames, or selector API payloads.

## Splits

| Split | Planned size | Purpose / access |
|---|---:|---|
| Calibration | 20 independent batches | Set only the resource-to-TEU conversion and inspect instrument reliability. No candidate-value threshold or selector retuning from confirmation. Calibration outputs are never confirmation evidence. |
| Development | 20 independent batches | Debug generator, taxonomy contract, pressure checker, and code. May be iterated; report all iterations. Do not use for final effect claims. |
| Confirmatory | At least 100 independent batches, with exact N frozen by the rule below | Primary RQ2 test; candidate truth/outcomes remain sealed until selector choices, pressure checks, code/config hashes, and preregistration are locked. |
| Replication | Same N as confirmation, independent batch seeds and task IDs | Re-run the frozen protocol after confirmation lock. This is same-protocol seed replication, not independent-domain validation. Keep sealed until the protocol/analysis artifact is locked. |

Each batch represents 20 candidates and 200 candidate-opportunity rows. At the 100-batch floor, each confirmatory/replication split contains 2,000 candidates and 20,000 candidate-opportunity rows. The number of independent units remains 100 batches, not 20,000 task rows.

### Sample-size rule

The target is **at least 100 independent batches** per confirmatory and replication split. Before confirmation, use calibration-only batch-level paired variance and a frozen simulation to calculate the minimum N giving at least 90% power to detect the SOI (+0.10 TEU/slot) against the Holm-corrected five-comparator family, under the preregistered paired design. Set final N to the larger of 100 and that value, capped at 300. If required N exceeds 300, do not run underpowered confirmation: redesign or classify the claim as not yet testable. Publish the simulation and freeze the resulting N before opening confirmatory outcomes. No decrease in N after calibration.

## Split integrity and leakage prevention

- Generate disjoint seed namespaces, candidate IDs, task IDs, and RNG streams for all four splits; save seed lists and hashes before outcomes.
- Never reuse Phase 13C or 13F outcome rows as Phase 1B confirmation/replication.
- Calibration may determine `lambda` only under the formula already stated; it cannot alter SCV, SOI, quota, K, selector rules, endpoints, task strata, or confirmation seeds.
- Development can test pressure and plumbing. Any change after viewing development performance must be versioned and followed by newly generated untouched confirmatory/replication seeds.
- For confirmation, compute candidate cards and selector decisions, run pressure gates, serialize and hash the complete decision file, and only then unlock the outcome store. Labels are revealed after every policy choice is immutable.
- If a confirmatory pressure gate fails, mark the batch unavailable before outcomes and use only the next predeclared reserve seed. Never redraw based on value/outcome.
- If outcome access occurs before a technical failure, the batch is exposed; do not replace it or reuse its seed as unseen data.
- Replication remains unopened until confirmation analysis code and report are frozen. The replication outcome cannot be used to modify the primary analysis.

## Claim boundary

Balanced challenge panels deliberately overrepresent types relative to any natural stream. Phase 1B/Phase 4 can answer whether SCV discriminates under known, decision-rich competition; it does not estimate deployment prevalence, open-world validity, or generalization beyond the synthetic generator. Phase 9 independent-generator replication remains necessary for broader claims.