# Theory vs. Implementation — Phase 13G

| Question | Finding |
|---|---|
| Did the deployed Phase 13G bounded ARC system demonstrate learning? | No: no invariants, ASFT skills, capabilities, or learned-skill transfer; very low bounded task accuracy. |
| Did it demonstrate IDT is false? | No. The learner saw only three successful traces, with one example per distinct program, below frozen support thresholds. |
| Did it demonstrate SCT is false? | No. No invariant-derived skill candidates were available; SCT had no eligible ARC skill pool. |
| Did it demonstrate learned transfer is false? | No for the learned ASFT mechanism: precision denominator is zero. However ASFT exact transfer task accuracy is 0/200 within the bounded solver and should remain reported. B2 memory's 1/200 is a different mechanism. |
| Did it demonstrate CGM is false? | No. No validated ARC capability units existed; CGR/IG are unavailable, not zero outcomes. |
| Is the implementation's ARC coverage failure real? | Yes. Full 10-program discovery fit is 3/600; transfer/holdout full-inventory fit are 5/200 and 2/200; main arms are limited to three trials. The frozen config also says three per task, but `discover()` defaults to ten, a material budget discrepancy. |
| Is this only an ARC “difficulty” result? | Not isolated. Low DSL fit is the proximate observed failure, while task complexity and representation are coupled in this design. |

## Scientific boundary

It is fair to say the **current tested ARC implementation did not work adequately** and did not provide ARC validation. It is not fair to convert the absence of learned candidates into a direct falsification or vindication of the higher-level theories. The correct class is **implementation/external-validity failure with theory mechanisms unavailable**.
