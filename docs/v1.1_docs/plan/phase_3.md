Perfect. Under the brutal-honesty framework, Phase 3 is where science finally begins.

Phases 1 and 2 built:

Phase 1
=
Trustworthy benchmarks

Phase 2
=
Trustworthy ARC diagnostics


Phase 3 is the first phase that can actually answer:

Does IDT work?


not:

Can IDT be tested?


That distinction is critical.

ASFT v1.1 Phase 3
IDT Revalidation

Phase ID

ASFT-V1.1-PHASE-3


Research Question (RQ1)

Does transfer-aware ranking (IDT)
produce higher future value than
simpler ranking policies under a
valid pressure benchmark?

Historical Starting Point

Current status:

Phase 13B

FAILED


because:

Transfer-aware

=

Frequency

=

No-transfer


under observed top-K rankings.

Current evidence:

IDT superiority
❌ Not established

IDT falsified
❌ Not established


Therefore Phase 3 exists to answer:

Does transfer-aware ranking
actually matter?

Phase 3 Structure

I would split it into:

3A Implementation Readiness

3B Calibration & Freeze

3C Development Benchmark

3D Confirmatory Benchmark

3E Replication Benchmark

3F IDT Verdict

Phase 3A
Implementation Readiness

Purpose:

Build exactly the benchmark
specified in Phase 1C.


Required Components

Rankers
R1 Transfer-Aware

R2 Frequency

R3 Reuse

R4 Compression

R5 Random

R6 Oracle

Pressure Metrics
TopK-RDR

Kendall Divergence

Independent Endpoint
FNTU@K

Contract Revalidation

Re-run:

26/26 contracts


on actual implementation.

Exit:

Ready

or

Blocked

Phase 3B
Calibration & Freeze

Purpose:

Freeze everything
before outcomes.


Required Freeze

Final N
Cluster-based

SOI
+0.10 FNTU


(or updated value)

Task Set
Frozen

Analysis
Frozen

Hashes
Frozen

Replication Plan
Frozen


Exit:

Preregistration Complete

Phase 3C
Development Benchmark

Purpose:

Test plumbing

Not test IDT.


Questions:

Does pressure exist?

Do rankers diverge?

Does evaluation work?


Allowed Outcomes:

Fix bugs

Tune implementation

Validate assumptions


Forbidden:

Claim success


Exit:

Development Complete

Phase 3D
Confirmatory Benchmark

This is the first real scientific phase.

Primary Endpoint

FNTU@K


Primary Comparison

R1

vs

R2 Frequency


Secondary

R1 vs R3

R1 vs R4

R1 vs R5


Outcome States

Supported
R1 exceeds all required comparators
by frozen criteria.

Contradicted
One or more comparators superior.

Tie
Within equivalence bounds.

Inconclusive
Precision insufficient.

Unavailable
Protocol failure.

Non-Informative
Pressure absent.

Phase 3E
Replication Benchmark

Purpose:

Repeat on disjoint population.


Required

New seeds

New task families

New candidate pools


Not:

Same benchmark rerun.


Possible Replications

R1
Within Generator

R2
Cross Generator

R3
Cross Domain

Phase 3F
IDT Verdict

This is the most important phase.

Possible Outcomes

V1
IDT Supported


Requirements:

Confirmatory win

Replication win

V2
IDT Weakly Supported


Requirements:

Confirmatory win

Replication pending

V3
IDT Not Supported


Requirements:

Ties

or

No meaningful advantage

V4
IDT Contradicted


Requirements:

Comparator superior

V5
Unavailable


Requirements:

Protocol failure

Phase 3 Readiness Gates
Gate P3-1
Phase 1C benchmark implemented.

Gate P3-2
26/26 contracts pass.

Gate P3-3
Pressure validated.

Gate P3-4
Final N frozen.

Gate P3-5
Analysis frozen.

Gate P3-6
Outcome store sealed.

Gate P3-7
Replication plan frozen.

What Phase 3 Must NOT Do

It must NOT conclude:

IDT works


because:

Transfer score correlates.


It must NOT conclude:

IDT works


because:

Development benchmark looked good.


It must NOT conclude:

IDT works


because:

Synthetic fixtures succeeded.


Only:

Confirmatory

+

Replication


can support the claim.

The Three Questions I'll Judge Phase 3 On
Q1
Can Frequency beat IDT?


If not:

Bad benchmark.

Q2
Can Compression beat IDT?


If not:

Bad benchmark.

Q3
Can IDT lose?


If not:

Bad science.

What Would Make Phase 3 Successful

Not:

IDT wins.


Successful Phase 3 means:

We obtain a trustworthy answer.


Possible trustworthy answers include:

IDT wins.

IDT ties.

IDT loses.

IDT unresolved.


All four outcomes would be scientifically valuable.

Recommended Next Breakdown

I would now decompose Phase 3 into:

3A.1 Benchmark Implementation

3A.2 Ranker Validation

3A.3 Pressure Validation

3A.4 Endpoint Validation

3A.5 Readiness Review


and start with Phase 3A: Implementation Readiness, because until the actual Phase 1C benchmark exists in executable form, no IDT revalidation can legitimately begin.