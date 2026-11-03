# Phase 3A — Candidate Pool Validation

## Protocol checked

The Phase 1C benchmark fixes `N=40`, `K=8`, hidden primary archetypes A–H, 8 each for the frequent-useless B and rare-useful C classes, opaque IDs, an independently randomized arrival order, and an allowlisted public feature card. Those quotas are a controlled fixture recipe, not population prevalence claims.

The Phase 3A engine validates N, K, uniqueness, opaque hash ID syntax, exact deterministic randomized permutation from a panel seed, and the card schema. The 26-contract development runner uses the Phase 1C synthetic `make_panel` generator; labels and truth remain in separate maps keyed by opaque ID. All five competitive rankers receive the identical pool.

## Results

| Criterion | Development result | Real/confirmatory result |
|---|---|---|
| N=40, K=8 | PASS on fixture | No actual candidate pool supplied |
| B/C quota and A–H diversity | Fixture quota verified outside engine | Not a natural prevalence target; no real taxonomy/semantic adjudication |
| Unique, opaque IDs | PASS: 40/40 synthetic IDs | No candidate registry/ID provenance supplied |
| Randomized arrival order | PASS: deterministic seeded permutation revalidated | Actual pool and signed seed manifest absent |
| Allowlist / hidden-field exclusion | PASS: exact eight-field card schema; no type, family, outcome, or future value | No production serializer/payload captured for audit |
| Exact shared pool across R1–R5 | PASS: all complete orders contain the same 40 IDs | Only exercised on the synthetic fixture |

## Diversity and leakage boundary

The Phase 1C A–H quotas and engineered feature recipes create diversity by construction in the fixture; they do not establish semantic diversity among actual invariant candidates. No real candidate corpus with deduplicated candidate signatures, source lineage, calibration opportunity counts, or hidden-class adjudication was available. No evidence supports a claim that actual candidate pools satisfy diversity or offer enough independent ranking alternatives.

The engine prevents ranker access to the hidden label/outcome mappings at the API boundary. The synthetic generator necessarily knows its class recipe; therefore the data-flow demonstration is not a production access-control audit.

**Verdict:** candidate-pool validator and synthetic fixture **PASS**; actual candidate-pool qualification/diversity **UNAVAILABLE**. N=40 remains the prespecified fixture value only; a different empirical frozen N needs a documented, outcome-blind justification.