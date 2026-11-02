Excellent. Phase 1A is arguably the most important subphase in all of v1.1 because if we audit the benchmarks properly, we avoid repeating the exact mistakes that caused most of the ambiguity in v1.0.

Think of it this way:

Phase 14
=
What failed?

Phase 1A
=
Why did the benchmark allow that failure?

ASFT v1.1 Phase 1A
Benchmark Audit & Pressure Analysis

Phase ID

ASFT-V1.1-PHASE-1A


Objective

Perform a forensic audit of every v1.0 benchmark before designing any new benchmark.

Core Principle

We are not auditing:

Theory


We are auditing:

The tests of the theory.

Key Research Question

Did the benchmark genuinely create the conditions necessary to evaluate the claim?

Phase 1A Structure
1A.1 Benchmark Inventory

1A.2 Benchmark Classification

1A.3 Pressure Audit

1A.4 Baseline Audit

1A.5 Construct Audit

1A.6 External Validity Audit

1A.7 Decision-Divergence Audit

1A.8 Failure Attribution Audit

1A.9 Benchmark Redesign Requirements

1A.10 Phase 1A Exit Review

1A.1 Benchmark Inventory
Goal

Create a complete inventory of every benchmark used in v1.0.

Inputs
Phase 13B

Phase 13C

Phase 13D

Phase 13E

Phase 13F

Phase 13G

Output Table
Benchmark	Purpose13B	IDT
13C	SCT
13D	Transfer
13E	CGM
13F	Baselines
13G	ARC
Questions

For every benchmark:

What was tested?

What was measured?

What was compared?

What was concluded?

1A.2 Benchmark Classification
Goal

Determine benchmark type.

Every benchmark gets tagged:

Discovery
Finds patterns

Selection
Chooses candidates

Ranking
Orders candidates

Transfer
Measures reuse

Capability
Measures growth

External
Tests generalization

Output

Benchmark taxonomy.

1A.3 Pressure Audit

This is the most important section.

Goal

Determine whether a benchmark actually created pressure.

Ranking Pressure

Example:

13B

Transfer-aware
=
Frequency
=
No-transfer


Result:

No ranking pressure.

Selection Pressure

Example:

13C

44/44 selected


Result:

No selection pressure.

Lifecycle Pressure

Example:

No meaningful retirement decisions.


Result:

No lifecycle pressure.

Output
Benchmark	Pressure Level13B	None
13C	None
13D	Moderate
13E	Weak
13G	N/A
1A.4 Baseline Audit
Goal

Evaluate baseline quality.

Questions

Did the baseline:

Actually challenge the claim?


Example:

Good
MEMORY_ONLY


because it exposed a real weakness.

Weak
NEVER_CREATE


because it is too easy to beat.

Output

Baseline quality score.

1A.5 Construct Audit
Goal

Determine whether benchmarks measured what they claimed.

Examples:

Transfer

Measured:

Step reduction


Claimed:

Transfer.


Need to check:

Is that sufficient?

CGR

Measured:

Internal score.


Claimed:

Capability growth.


Need to audit.

Output
Metric	Construct RiskIS	High
SCV	Moderate
CGR	High
IG	Very High
1A.6 External Validity Audit
Goal

Determine whether benchmark generalizes.

Questions:

Synthetic only?

Multiple generators?

Real-world?

ARC?


Example:

13B
Synthetic only.

13G
External attempt.

Output

External validity map.

1A.7 Decision-Divergence Audit

This is a new critical audit.

Goal

Measure whether competing methods actually made different decisions.

Example:

13B
Same ranking.

13C
Same selection.

13F
Same skills created.


Result:

No identifiable advantage possible.

Output
Benchmark	Divergence13B	0
13C	0
13F	0
1A.8 Failure Attribution Audit
Goal

Separate:

Theory failure


from

Benchmark failure


Example:

SCT

Observed:

Tie.


Question:

Because SCT is wrong?

OR

Because no decisions differed?


Example:

ARC

Observed:

No skills.


Question:

Theory wrong?

OR

Coverage bottleneck?

Output

Failure Attribution Matrix.

1A.9 Benchmark Redesign Requirements
Goal

Generate mandatory requirements for Phase 1B–1G.

Example:

From 13B

Requirement:

Rankers must disagree.

From 13C

Requirement:

Good and bad candidates must exist.

From 13E

Requirement:

External capability criterion required.

From 13G

Requirement:

Coverage measured separately from accuracy.

Output

Master Requirement List.

1A.10 Exit Review
Required Deliverables
benchmark_inventory.csv

benchmark_classification.csv

pressure_audit.csv

baseline_audit.csv

construct_audit.csv

external_validity_audit.csv

decision_divergence_audit.csv

failure_attribution_audit.csv

benchmark_redesign_requirements.csv

phase1A_review.md

Phase 1A Success Criteria

PASS only if:

Inventory
100% benchmark coverage.

Pressure
Every benchmark classified
by pressure level.

Divergence
Every benchmark evaluated
for decision divergence.

Constructs
Every metric classified
by construct-validity risk.

Redesign
Every v1.0 weakness converted
into a v1.1 requirement.

Most Important Deliverable

If I had to choose only one output from Phase 1A, it would be:

benchmark_redesign_requirements.csv


because that file becomes the direct input for:

Phase 1B
Selection Pressure Benchmark

Phase 1C
Ranking Pressure Benchmark

Phase 1D
Memory Challenge Benchmark


and ensures every v1.1 benchmark exists to solve a specific failure discovered in v1.0 rather than introducing new, unvalidated ideas.