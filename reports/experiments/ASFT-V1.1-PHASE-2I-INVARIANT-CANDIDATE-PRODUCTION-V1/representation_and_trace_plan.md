# Phase 2I — Representation and Trace Production Plan

## R1 faithful reference

R1 uses the current ten-program whole-grid representation and the Phase 2C corrected S4 execution contract. It is the same finite language as the historical Phase 13G reference, but must run with config/runtime/log parity. Historical R0 results and the old budget mismatch are audit-only.

## R3 object-centric candidate-production arm

Use the existing Phase 2F R3 specification only: deterministic same-color 4-connected object parser; stable object IDs; finite object-local selectors; one object action per candidate; no relation graph, hierarchy, composition, or hidden helpers. Maximum ten complete candidate trials/task, deterministic enumeration, exact training-demo fit, identical resource caps. R3 implementation/grammar hashes are not present; Phase 2I must implement and hash this before execution.

## Trace contract

Both representations must feed the same frozen downstream miner and candidate pipeline. Every task/condition emits at most one structurally valid trace under the same high-level four-step cap, with full trial ledger separate. The trace representation must preserve enough **candidate-specific semantic operation information** for recurrence mining while keeping the schema comparable across R1/R3. This interface is currently unresolved: Phase 2D/2E observed repeated generic control/verification operations, not semantic ARC transformation rules.

Before running, specify and test exactly how an R3 object action and an R1 whole-grid operation are represented as normalized trace events, including parameter handling, failure traces, deduplication within trace, and source IDs. Do not add arm-specific trace steps, hand-label invariant signatures, or alter max trace steps after seeing candidate yield. If the common trace contract cannot encode the necessary semantics, report the run as not ready; do not quietly change downstream mining.

## Positive control

A Phase 2F HCC known-rule corpus may be used in an isolated software contract to verify that the unchanged miner/candidate pipeline can emit candidates under sufficient, diverse recurring traces. It is synthetic plumbing only; its candidates cannot enter the ARC registry, count toward ARC yield, or establish ARC validity. The HCC must use the same support/trace schema and demonstrate outcome-blind labels.

## Readiness status

R1 is the available reference. R3 and HCC are specified but not implemented; a common semantic trace adapter and independent family annotation are also not yet frozen. Thus this plan does not claim a runnable Phase 2I experiment.