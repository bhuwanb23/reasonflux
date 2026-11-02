# Phase 2F Prospective Comparison — Preregistration Template

**Template only. Do not execute until every required field is completed, frozen, hashed, and authorized.**

## A. Conditions and implementation freeze

- Phase/package/version:
- Primary comparison: R1 vs R3 (or justified pre-run amendment):
- Secondary comparisons and multiplicity plan:
- Registry row IDs and taxonomy:
- Code/grammar/parser/adapter/interpreter hashes per representation:
- Primitive, object, relation, hierarchy, composition, and parameter rules:
- Candidate identity/order/enumeration; ambiguity handling:
- Independent task-family annotation source/hash and blind status:
- HCC generator, truth labels outside solver input, expected plumbing assertions:

## B. Data and access

- Common prospective task IDs and split manifest/hash:
- Task-set disjointness from representation development and prior outcome review:
- Training-demo-only coverage/trace inputs:
- Test-output sealed evaluator and separate authorization, if any:
- Historical Phase 13G holdout is not pristine confirmation; state any replacement:

## C. Frozen budget and evaluator

Confirm parity across registry, config, runtime, and logs:

- B1 max candidate trials/task: 10 (Phase 2C S4 reference) or pre-authorized amendment:
- B2 search depth: 1 flat complete-program trial:
- B3 primary traces/task-condition: 1; high-level steps ≤4:
- B4 wall clock: 30 seconds/search:
- B5 memory: 2,048 MiB:
- B6 primary tasks/condition: 1,000; replay: 1,000:
- Fit rule: exact reproduction of all training demonstrations:
- Stop rule and no-fit/parser/budget/ambiguity states:
- Search/candidate-selection algorithm and evaluator hashes:

## D. Downstream freeze

- Phase 2E TraceMiner + thresholds: frequency 5, cross-trace 5, consistency 1.0; policy version/hash:
- Shared independent family labels available? If no, mark family breadth unavailable and specify effect on candidate policy:
- Candidate generation/rejection and validation versions:
- SkillConfig/qualification/adapter/executor versions:
- Transfer eligibility definition, applicable-task denominator and threshold:
- Capability config/state machine:
- No post-outcome threshold, baseline, endpoint, or adapter changes:

## E. Endpoints and decision rules

- Primary paired endpoint: exact training-demo-fit coverage:
- Primary comparator: R1:
- Practical coverage margin δ_coverage (must be numerically frozen before run):
- Activation margins by trace, invariant, skill, transfer, capability stage:
- Secondary endpoints and denominators:
- Statistical unit task ID; paired CI method, resamples/seed, multiplicity:
- Missing/unavailable/blocked/upstream states:
- Accuracy endpoint (only if separately authorized):
- Bottleneck decision mapping B1–B5:

## F. Integrity gates and stop rules

- Coverage runner fails closed if any test target is parsed or accessed.
- Config=runtime=log parity and hashes must pass.
- Parser and independent trace validator pass implementation controls.
- HCC expected rules are detected and oracle plumbing passes; HCC is not ARC evidence.
- Any representation adapter or family label unavailable is reported as such, not zero.
- Any split overlap, holdout reuse, leakage, hash mismatch, budget breach, or post-outcome rule change blocks confirmatory interpretation.

**Authorization and freeze date:**  
**Independent reviewer:**  
**Pre-run artifact hashes:**