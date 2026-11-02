# Phase 1G — Outcome-Response Audit

The contract runner exercises distinct status profiles to prove the framework does not force a single favorable interpretation:

| Constructed profile | Coverage | Accuracy / downstream | Chain result | Interpretation |
|---|---|---|---|---|
| Coverage high, accuracy low | observed `.80` | observed `.20` | break observed | Coverage and accuracy remain distinct. |
| Coverage low, accuracy low | observed `.10` | observed `.10` | break observed | Low performance is not automatically assigned to representation alone. |
| Coverage high, transfer low | observed `.80` | transfer-stage break | break observed | Adequate coverage can expose downstream failure. |
| No eligible skill-transfer pairs | observed coverage | transfer unavailable | chain unavailable downstream | Zero eligibility is not zero transfer. |
| All pipeline stages activate | observed | observed | chain activated | Full activation is representable by the status logic. |

**Evidence boundary:** the numeric rates and status profiles above are hand-constructed contract fixtures, not ARC task results, solver outputs, or observed performance. No predictor ranking was used to construct them. They verify only that the code can represent high/low coverage and accuracy separately, activation/non-activation, transfer unavailability, and a full-chain path. They do not favor any anticipated outcome.