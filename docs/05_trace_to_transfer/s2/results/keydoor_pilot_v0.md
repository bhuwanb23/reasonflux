# S2 Implementation Pilot v0 — Audit Note

**Purpose:** retain the first exploratory output rather than erase it after the R1-Max implementation was strengthened.  
**Status:** exploratory only; not a decision-grade Claim N result.

## Captured output

The first script run used an earlier prototype: I0's color-match predictor was directly encoded, while R1 was only a positive-trace shared-slot macro and abstained outside that macro. The command output recorded at the time was:

```text
T2T-S2-KeyDoor-Run-v1: N-PASS; B-PASS
N I0: 8/8 accuracy; abstain=0
N R1-Max: 4/8 accuracy; abstain=4
B I0-G0-no-boundary-update: false_activation=2/4; applicable_coverage=2/2
B I1-G1-CE-updated: false_activation=0/4; applicable_coverage=2/2
```

The pilot JSON was later overwritten by the revised run; this note preserves the exact stdout summary, not an invented full per-row artifact.

## Why v0 cannot support N

After seeing the apparent N-PASS, review against S1.4 identified that the replay comparator did not compile a conditional rule from the available negative source traces. R1-Max was then strengthened to search a frozen source-only predicate grammar, source examples were expanded to identify the failed base predicates, and I0 was changed to check its predeclared relation against the same source examples. The same N holdout was reused for the revised run.

Therefore the v0 result is an exploratory pilot and must not be reported as support for Claim N. The v1 tie is also exploratory rather than an independent confirmation because it uses the same exposed holdout after a result-informed baseline/model revision. The correct decision-grade Claim N status for S2 is **BLOCKED pending a separately frozen version and fresh evaluation contexts**. The raw v1 score remains useful evidence that the stronger script can reproduce I0 on this fixture.

## Boundary result note

The boundary code, G0/G1 definitions, B holdout, and B criterion were unchanged between v0 and v1. Both outputs were 2/4 to 0/4 false activations with applicable coverage 2/2 retained. This is reported as a bounded deterministic mechanism demonstration, not population evidence or harm reduction.
