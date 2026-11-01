# Intelligence-Metric Analysis

## Frozen implementation

Phase 13E selects `evaluation.growth_metrics.compute_ig` as confirmatory: `IG = .35*CGR + .25*TG + .20*UG + .15*CCG + .05*CompG`. IGR is the round-to-round difference in IG. IE is `IG / experiences`, where experiences is the 32 discovery traces plus cumulative held-out tasks.

These formula outputs are reproducibly computed. Their components are repository-defined skill utility, measured transfer score, portfolio CapU, successful-family coverage, and composition-count deltas. There is no independent intelligence label or externally validated criterion in Phase 13E.

## Mean versus trajectory

Across seed-level round averages, IG is `0.2294` (95% CI `[0.2245,0.2343]`) and IGR is `0.00904` (`[0.00903,0.00906]`). However, round-average IG is approximately `.6573, .0801, .1442, .0362`, while IGR is `.6573, -.5772, .0641, -.1080`. The positive four-round means are heavily influenced by the initial transition from a zero prior state; IG/IGR are not positive or increasing each round.

IE averages `0.0043`, but its mean OLS slope is `-0.00394` (95% CI `[-0.00421,-0.00367]`). Because IE is defined as IG divided by cumulative experience, this establishes a falling internal ratio in this run, not independently measured deterioration in human-like intelligence efficiency.

## Judgment

“Intelligence metrics are computable” is supported. “IG/IGR/IE measure intelligence growth” is not established. The latter would require an independent behavioral criterion, a demonstrated relationship beyond shared formula components, and validation beyond the generator.
