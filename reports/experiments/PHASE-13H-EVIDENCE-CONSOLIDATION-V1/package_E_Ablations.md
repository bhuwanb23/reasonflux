# Package E — Ablation and Component Evidence

Ablation interpretations are tied to the named frozen endpoint. A zero paired difference means no measured effect in that exact run, not proof the component can never matter. Growth-score changes are not automatically task-performance gains.

| Phase | Removal / comparison | Saved result | Judgment and limit |
|---|---|---|---|
| 13C | SCT vs always/random creation | Same mean primary net value `0.345` | No policy superiority. |
| 13C | SCV / skill value predictor | SCV10 correlates with shadow future value; policy selects all eligible candidates; frequency and p_reuse associations are at least as high | Correlation does not show incremental policy value. |
| 13C | Composition | Only rotation→reflection evaluable; required counting/grouping skills absent | Other composition cells unavailable, not failures imputed as zero. |
| 13D | A1 no invariants | ASFT-minus-ablation `+0.018909`, CI `[0.016727,0.020000]` on corrected transfer endpoint | Positive contrast on this endpoint; interpret as removal performing worse, within synthetic phase only. |
| 13D | A2 no SCT | Difference `0.000`, CI `[0,0]` | Frozen ablation-degradation criterion failed; null contribution in this run. |
| 13D | A3 no persistence | Difference `+0.017018`, CI `[0.015055,0.018000]` | Positive contrast on this synthetic endpoint. |
| 13D | A4 no composition | Difference `0.000`; status `unavailable_missing_component_skills` | Not an evaluable ablation because source component skills were missing. |
| 13E | A1 no IDT | Growth difference `+0.05950`, lower CI `+0.04198` | Growth metric lower when removed; not necessarily task utility. |
| 13E | A2 no SCT | Difference `0.000` | No growth effect observed. |
| 13E | A3 no skill library | Growth difference `+0.29463`, lower CI `+0.28570` | Strong metric-pathway dependence; does not establish capability generalization. |
| 13E | A4 no composition | Growth difference `+0.03497`, lower CI `+0.03051`; composition-value criterion mean `-0.1429` | Growth metric and composition value disagree; composition did not meet value criterion. |
| 13E | A5 no CGM | Growth measures intentionally masked; behavior preserved | Unavailable by design; not a task-performance comparator. |
| 13F | A1 no IDT | Task utility ASFT-minus `-0.002438` (CI `[-0.002680,-0.002195]`); CGR `+0.015001` (CI `[0.012947,0.017056]`) | Mixed across the preregistered outcomes. |
| 13F | A1.1 frequency-only | Utility/CGR paired differences `0` | No contribution detected in this stream. |
| 13F | A2 no SCV | Utility/CGR paired differences `0` | SCV incremental effect not detected. |
| 13F | A2.1 random SCV | Utility/CGR paired differences `0` | Randomized SCV tied; no policy contribution detected. |
| 13F | A2.2 lifecycle off | Utility/CGR paired differences `0` | Lifecycle contribution not detected in the frozen setting. |
| 13F | A2.3 no composition | ASFT utility `+0.077344`; composed-task utility `+0.6188` (source evidence); CGR contrast positive | Supports composition value on this specific frozen synthetic endpoint, unlike 13D unavailable/13E adverse value. |
| 13F | A3 no capability layer | Utility and composition-utility deltas `0`; CGR differs `+0.287172` | Metric pathway effect without task-utility difference; do not interpret as overall success. |
| 13F | X1 no transfer | ASFT-minus comparison: task utility `-0.036344`, composition utility `-0.34125`; CGR `+0.287172` | Outcomes diverge by endpoint; not a uniform advantage. |
| 13F | X4 no capability formation | Task/composition utility deltas `0`; CGR pathway differs | Component affects a metric pathway without demonstrated task-utility gain. |
| 13F | X4 no capability formation | Utility/composition utility deltas `0`, with CGR pathway difference | Component affects a metric definition/pathway, not demonstrated task performance. |
| 13G | IDT/SCT/CGM pipeline | No invariants, skills, or capabilities on bounded ARC DSL | Mechanism chain unavailable; broad inference limited by fit coverage. |

## Judgment

Evidence of component contribution is inconsistent and metric-specific. Some frozen synthetic ablations reduce growth or measured transfer; several equal the full system; composition is unavailable in one phase, adverse on a Phase 13E value criterion, and positive on one Phase 13F synthetic composition stream. No component-level causal claim generalizes beyond those exact procedures.

Full machine-readable rows: [`ablation_master_table.csv`](ablation_master_table.csv). Phase 13D values use the corrected saved-record posthoc report, not the earlier defective frozen dashboard.
