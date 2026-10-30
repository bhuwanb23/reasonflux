# Trace Mining (Phase 11C-2)

Executable specification for converting reasoning traces into invariant
candidates. Code: `src/traces/normalizer.py`, `src/traces/segmentation.py`,
`src/invariants/pattern_mining.py`, `src/invariants/candidate_generation.py`,
`src/invariants/detector.py`. Thresholds: `configs/thresholds.yaml` (`mining:`).

## Core principle

ASFT does **not** mine tasks, outputs, or solutions. It mines **reasoning
structures** from traces and converts them into invariant candidates.

Trace mining is structure discovery, not mere pattern counting.

## Pipeline

```
Task → Reasoning Trace
  → Trace Collection
  → Trace Normalization
  → Trace Segmentation          (fragments, not whole traces)
  → Pattern Extraction
  → Pattern Aggregation
  → Candidate Generation
  → (Phase 11C-3) Invariant Validation
```

Orchestrator: `TraceMiner.mine(traces) -> MiningResult`.
`InvariantDetector.detect(traces)` returns the candidate list only.

## Mining units (MVP)

| Unit | Example | MVP |
| --- | --- | --- |
| Operation | `find_symmetry` | yes |
| Operation pair | `find_symmetry → apply_reflection` | yes (most useful) |
| Procedure | detect → find → apply | yes (via n-grams up to length 4) |
| Trace skeleton | detect → transform → verify | no (future) |

## Stages

### 1. Collection

Input is a sequence of `ReasoningTrace` or a `TraceBatchProvider`. The miner
never consumes raw `Task` objects (Contract 1).

### 2. Normalization

`canonicalize_operation` maps synonyms (`LocateObject` → `detect_object`,
`FindMirrorAxis` → `find_symmetry`, …) so conceptually identical traces align.

### 3. Segmentation

Contiguous n-grams of length 1..`max_fragment_length` (default 4). Identical
signatures are deduped per trace so frequency counts distinct traces.

### 4. Pattern extraction

A fragment becomes a `MinedPattern` only if:

1. `frequency >= min_frequency` (default 3)
2. distinct traces `>= min_cross_trace` (default 2)
3. success/failure counters are tracked separately

Patterns are **not** invariants yet.

### 5. Aggregation

Patterns that share a contiguous common subsequence of length
`>= min_core_length` (default 2) form connected components →
`AggregatedStructure`. This merges the doc's A/B/C reflection variants into one
structure while keeping rotation separate.

### 6. Candidate generation

Structures become `Invariant` objects with `state=CANDIDATE`,
`origin="trace_mining"`, deterministic `InvariantIdentity` ids, and
`transfer_events=0` (transfer verified in 11C-3). Existing rejection criteria
filter noise; rejections are recorded in `MiningResult.rejected`.

## Failure-trace policy

Failed traces are **not** discarded. Success and failure patterns are mined and
stored separately (`success_patterns` / `failure_patterns`) as negative evidence
for future meta-reasoning. With `successful_trace_bias: true`, aggregation and
candidates prefer success patterns.

## Outputs

| Output | Content |
| --- | --- |
| Pattern inventory | `success_patterns`, `failure_patterns` |
| Pattern statistics | frequency, coverage, task families, success/failure counts |
| Candidate invariants | `candidates` (+ `rejected` with reasons) |
| Run statistics | `MiningStatistics` |

## Must NOT do

Trace mining must **not**: create skills, rank transfer utility, decide
promotion, manage memory, or compute CGR. Those belong elsewhere.

## Success criteria

Reflection, rotation, and counting structures emerge; similar traces cluster;
candidates become discoverable and distinguishable.

## Failure criteria

Noise dominates; every pattern looks important; reflection and rotation become
indistinguishable; no reusable structures emerge.
