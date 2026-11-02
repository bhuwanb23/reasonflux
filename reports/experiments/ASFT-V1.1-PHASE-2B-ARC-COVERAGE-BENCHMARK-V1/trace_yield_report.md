# Phase 2B.6 — Trace Yield Benchmark

## Definitions

- **Emitted trace rate:** traces emitted / eligible task IDs.
- **Validated trace rate:** trace records passing a separate structural check, train-grid schema validation, mode/task identity check, and consistency check between trace outcome and demo-fit result / emitted traces.
- **Successful trace rate:** independently exact-replayed demo-fit traces / eligible task IDs.
- **Diversity:** distinct successful first-fit `(program, inferred context)` signatures; Shannon entropy is computed over successful program labels.
- **Trace density:** mechanical trace steps per task; a no-fit trace has three records and a fit trace four. This is logging density, not reasoning depth.

## Results

| Mode / split | Emitted | Independently valid | Successful | Signature diversity | Program entropy (bits) | Steps/task |
|---|---:|---:|---:|---:|---:|---:|
| Budgeted / discovery | 600/600 | 600/600 | 1/600 (0.1667%) | 1 | 0 | 3.0017 |
| Budgeted / transfer | 200/200 | 200/200 | 0/200 | 0 | N/A | 3.0000 |
| Budgeted / holdout | 200/200 | 200/200 | 1/200 (0.50%) | 1 | 0 | 3.0050 |
| **Budgeted / all** | **1,000/1,000** | **1,000/1,000** | **2/1,000 (0.20%)** | **2** | **1.0000** | **3.0020** |
| Fullscan / discovery | 600/600 | 600/600 | 3/600 (0.50%) | 3 | 1.5850 | 3.0050 |
| Fullscan / transfer | 200/200 | 200/200 | 5/200 (2.50%) | 4 | 1.9219 | 3.0250 |
| Fullscan / holdout | 200/200 | 200/200 | 2/200 (1.00%) | 2 | 1.0000 | 3.0100 |
| **Fullscan / all** | **1,000/1,000** | **1,000/1,000** | **10/1,000 (1.00%)** | **8** | **2.7219** | **3.0100** |

Trace emission and structural validity are 100% by construction plus independent validation, while successful trace yield is 0.2% budgeted and 1.0% fullscan. The gap is the central measurement result: a trace record exists for every attempt, but only a small fraction encode an exact demo-fit solution.

## Representation versus search interpretation

More candidate trials on the unchanged representation revealed eight additional fits compared with the first-three condition. That isolates a search-budget/order effect on *found demo fits* in this paired diagnostic. The very low all-ten fit rate also shows a severe coverage limitation of the deployed bounded representation-plus-inference implementation. Without a matched alternative representation, the audit cannot separate missing expressivity from inference/parameterization limits. Trace scarcity therefore cannot be assigned to representation alone.

Phase 13G's `trace_schema_valid=True` flag was hard-coded. Phase 2B's 100% trace-valid count is a new independent audit of the emitted records and training inputs; it does not retroactively validate the historical flag or prove reasoning quality.