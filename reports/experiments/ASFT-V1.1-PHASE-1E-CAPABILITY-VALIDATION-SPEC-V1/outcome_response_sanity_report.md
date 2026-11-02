# Phase 1E — Outcome-Response Sanity Audit

The decision-rule contract was checked against five **constructed interval scenarios**. The function labels a metric win only when adding CGR yields a meaningful held-out MAE reduction and the CGR slope is positively supported; it can also report equivalence, loss/inverse direction, uncertainty, or unavailability.

| Constructed scenario | ΔMAE interval | CGR slope interval | Decision-rule output |
|---|---|---|---|
| Win | `[0.04, 0.08]` | `[0.01, 0.10]` | `metric_wins` |
| Equivalent tie | `[-0.01, 0.01]` | `[-0.01, 0.01]` | `equivalent_tie` |
| Loss / inverse direction | `[-0.08, -0.03]` | `[-0.10, -0.01]` | `metric_loses` |
| Uncertain | `[-0.02, 0.04]` | `[-0.01, 0.03]` | `inconclusive` |
| Integrity failure | unavailable | unavailable | `unavailable` |

**Evidence limit:** these intervals are hand-constructed decision-rule inputs; they are not fitted predictive models, generated task outcomes, or evidence about CGR. They demonstrate that the reporting logic does not hardwire success. The actual independent task battery and model comparison are not implemented.