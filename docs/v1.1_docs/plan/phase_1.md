This is the most important phase in ASFT v1.1.

If Phase 0 is the constitution, then Phase 1 is the court system.

Phase 14 showed that many v1.0 conclusions were limited not because the mechanisms were necessarily wrong, but because:

No ranking pressure
No selection pressure
No capability validation
No intelligence validation
Unclear benchmark design


So Phase 1 exists to prevent that from happening again.

ASFT v1.1
Phase 1 — Benchmark & Evaluation Redesign

Phase ID

ASFT-V1.1-PHASE-1


Package

ASFT-V1.1-PHASE-1-BENCHMARK-DESIGN-V1


Goal

Design all benchmark environments,
evaluation protocols, pressure tests,
validation criteria, and experimental
frameworks required for v1.1.

No theory testing occurs in Phase 1.

No confirmatory data collection occurs.

Phase 1 only creates valid tests.

Phase 1 Success Definition

At the end of Phase 1 we must know:

What exactly is being tested?

How can a mechanism win?

How can it fail?

What alternative explanations exist?

What baseline must be beaten?

What constitutes pressure?

Phase Structure
Phase 1A
Benchmark Audit

Phase 1B
Selection Pressure Benchmark

Phase 1C
Ranking Pressure Benchmark

Phase 1D
Memory Challenge Benchmark

Phase 1E
Capability Validation Benchmark

Phase 1F
Intelligence Validation Benchmark

Phase 1G
ARC Evaluation Framework

Phase 1H
Baseline & Ablation Framework

Phase 1I
Evaluation Protocol

Phase 1J
Phase 1 Readiness Review

Phase 1A
Benchmark Audit
Purpose

Review every v1.0 benchmark.

Questions
Which benchmarks worked?

Which benchmarks failed?

Which benchmarks produced ties?

Which benchmarks lacked pressure?

Which benchmarks lacked validation?

Deliverables
Benchmark Inventory

Benchmark Weakness Matrix

Pressure Audit

Key Output
Benchmark	Issue13B	No ranking divergence
13C	No selection divergence
13E	No external capability target
13G	Coverage bottleneck
Exit Criteria
Every v1.0 benchmark audited.

Phase 1B
Selection Pressure Benchmark
Purpose

Force SCT and SCV to make real decisions.

Problem From v1.0
44/44 selected

↓

No meaningful test.

Design Requirements

Candidate pool must contain:

Positive-value candidates

Neutral candidates

Negative-value candidates

Mandatory Rule

At least:

20% harmful

20% neutral

20% useful


(or equivalent distribution).

Comparators
SCV

Frequency

Random

Always Create

Never Create

Success Definition

A mechanism cannot pass if:

All candidates selected.

Exit Criteria
Selection pressure demonstrably exists.

Phase 1C
Ranking Pressure Benchmark
Purpose

Force rankers to disagree.

Problem From v1.0
Transfer-aware

Frequency

No-transfer

↓

Same ranking.

Design Requirements

Include:

Frequent useful

Frequent useless

Rare useful

Rare useless

Transfer-rich

Transfer-poor

Required Property

Different rankers must produce:

Different orderings.

Comparators
Transfer-aware

Frequency

Reuse

Random

Compression-inspired

Exit Criteria
Rankers no longer tie by design.

Phase 1D
Memory Challenge Benchmark
Purpose

Test strongest surviving alternative.

Problem
Memory remains viable.

Design Requirements

Tasks where:

Exact replay succeeds

Novel composition fails

Novel context fails

Abstraction may help

Benchmark Families
Replay

Novel recombination

Context shift

Composition shift

Partial analogy

Comparators
Memory

ASFT

Hybrid

Random

Exit Criteria
Memory and abstraction
can be separated.

Phase 1E
Capability Validation Benchmark
Purpose

Give CGR external meaning.

Problem
CGR rises

↓

Meaning unknown.

Requirements

Independent capability tests.

Not derived from:

CGR

IG

ASFT internals

Example Measures
Task breadth

Generalization

Persistence

Novel-task success

Rule

Capability target must be:

Externally measured.

Exit Criteria
Capability defined independently.

Phase 1F
Intelligence Validation Benchmark
Purpose

Determine whether IG measures anything.

Problem
IG

=

Formula

Candidate Targets
Adaptation speed

Future learning

Few-shot acquisition

Transfer efficiency

Rule

Must not reuse:

IG components


as validation target.

Exit Criteria
Independent intelligence target exists.

Phase 1G
ARC Evaluation Framework
Purpose

Prevent another Phase 13G situation.

Requirements

Separate:

Coverage

Discovery

Transfer

Capability

Accuracy

Mandatory Metrics
Coverage

Invariant count

Skill count

Capability count

Transfer

Accuracy

Mandatory Rule

Coverage and accuracy must never be conflated.

Exit Criteria
ARC evaluation fully specified.

Phase 1H
Baseline & Ablation Framework
Purpose

Freeze competitors.

Required Baselines
B1
No Learning

B2
Memory

B3
Random

B4
Compression

B5
Frequency

Required Ablations
No IDT

No SCT

No SCV

No Transfer

No Capability Layer

No Lifecycle

Exit Criteria
Baselines frozen.

Phase 1I
Evaluation Protocol
Purpose

Freeze methodology.

Must Define

For every future experiment:

Primary endpoint

Secondary endpoints

Independent unit

Sample-size rationale

Replication requirement

SOI

Missing-data rule

Mandatory Rules
No threshold changes

No split changes

No metric changes

After outcomes visible

Exit Criteria
Protocol frozen.

Phase 1J
Readiness Review
Checklist
Benchmark Audit
✅

Selection Benchmark
✅

Ranking Benchmark
✅

Memory Benchmark
✅

Capability Benchmark
✅

Intelligence Benchmark
✅

ARC Framework
✅

Baselines
✅

Protocol
✅

Phase 1 Deliverables
benchmark_audit.csv

selection_pressure_spec.md

ranking_pressure_spec.md

memory_challenge_spec.md

capability_validation_spec.md

intelligence_validation_spec.md

arc_framework_spec.md

baseline_matrix.csv

evaluation_protocol.md

phase1_readiness_report.md

Phase 1 Exit Decision
PASS


only if:

Selection pressure exists

Ranking pressure exists

Memory can be separated

Capability target is external

Intelligence target is external

ARC evaluation is clean

Baselines are frozen

Protocols are frozen


Otherwise:

FAIL

Return to benchmark design.


The entire purpose of Phase 1 is to ensure that when you reach Phases 3–10, a result can actually answer the research questions instead of repeating the ambiguity that dominated several v1.0 findings.