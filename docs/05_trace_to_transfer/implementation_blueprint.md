# Implementation Blueprint — Design Only

No implementation is authorized by this document. Build only after the novelty, object, comparator and protocol documents are reviewed and the user separately authorizes relevant work.

## Proposed modules

1. **Event adapter:** normalize permitted AGI-3 observations/actions/transitions to versioned event schema; never store credentials or hidden labels.
2. **Trace store:** append-only, hash-linked source events and run/config provenance.
3. **Candidate miner:** propose invariant/effect motifs from varied traces; output candidates plus rejection reasons and support denominators.
4. **Counterexample ledger/refiner:** classify contradictions, update candidate version/scope using only allowed evidence, preserve history.
5. **Skill compiler/runtime:** validate schema, bind parameters, check applicability, predict effect, execute within action limit, stop/fallback on mismatch.
6. **Baselines:** no-skill, raw replay, strong parameterized/compressed replay, recurrence-only; each shares the same wrapper and event instrumentation where possible.
7. **Evaluator adapter:** call only the official permitted evaluator; preserve raw output and version.
8. **Analysis/reporting:** compute prespecified summaries from immutable run artifacts; no thresholds or exclusions are selected after outcomes.

## Interfaces

- `propose(traces, config) -> CandidateBatch`
- `revise(candidate_version, counterexamples, config) -> NewCandidateVersion`
- `check_applicability(skill_version, observation) -> ApplicabilityResult`
- `predict(skill_version, observation, parameters) -> PredictedEffect`
- `execute_or_abstain(skill_version, state, budget) -> Action/Abstain/Fallback`
- `record_transition(prediction, observed_transition) -> Event + optional counterexample`

The exact API, state abstraction and serialization format remain open until T2T-P2 and P4 review.

## Required engineering properties

Deterministic version identifiers; no silent overwrites; append-only events; explicit failures/timeouts; secure secret handling; offline/runtime compliance per live rules; replayable local fixtures; budget accounting; baseline parity; and clear separation of development outputs from hidden evaluation.

## Non-goals for first implementation

No CGM controller, “intelligence growth” score, concept graph, recursive self-improvement, new model training, skill composition, or multi-agent system. Do not integrate Phase 2I or alter existing Phase 3 gates as a side effect.
