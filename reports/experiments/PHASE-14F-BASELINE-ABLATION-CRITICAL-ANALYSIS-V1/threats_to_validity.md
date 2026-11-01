# Threats-to-Validity Assessment

| ID | Severity | Threat | Analysis constraint |
|---|---|---|---|
| BLA-01 | High | Memory-friendly synthetic stream / raw trace retrieval | Treat Phase 13C MEMORY_ONLY as a strong protocol-specific counterexample; do not generalize or pool with skill-store B2. |
| BLA-02 | High | Positive/eligible candidate pool | 13C all eligible candidates selected; SCV10 was positive for all calibration candidates. This weakens primary discrimination, not all future selection tests. |
| BLA-03 | High | Low selection/lifecycle pressure | 13F selection arms build the full common pool and lifecycle toggles tie. Nulls show no effect in these runs, not component irrelevance. |
| BLA-04 | High | Generator/task distribution | Synthetic task families, shared operations, and repeated opportunities can favor retrieval or skill reuse in protocol-specific ways. |
| BLA-05 | High | Cross-phase endpoint mismatch | Net value, TU, TS, task utility, CGR, composed-task utility, and ARC accuracy are not common-scale measures. Never pool. |
| BLA-06 | High | Compression baseline is a proxy | B4 is not canonical DreamCoder; retain its competitiveness without making canonical compression claims. |
| BLA-07 | Medium-high | Random comparator definitions differ | RANDOM_CREATE, random pattern, B3_RANDOM_SKILL_CREATION, and random-SCV are separate baselines. |
| BLA-08 | High | Phase 13B accounting lineage | Pre-correction `.1431299603` and corrected `.0958085317` tie/fail; identify version for magnitude claims. |
| BLA-09 | Medium-high | Posthoc Phase 13D correction | Use corrected paired baselines and preserve original dashboard; posthoc is not an independent replication. |
| BLA-10 | High | Metric-layer ablation confounding | CGM/capability removal can change CGR by design while task utility is unchanged. |
| BLA-11 | High | Phase 13G low ARC DSL coverage | No invariants/skills/capabilities means baseline separation cannot identify mechanism superiority. |
| BLA-12 | Medium | Correlational metric predictors | SCV/frequency/p_reuse correlations are descriptive; policy-level incremental advantage must be demonstrated separately. |

**Severity interpretation:** high means the risk materially limits an across-phase causal or superiority claim, not that saved results are invalid.
