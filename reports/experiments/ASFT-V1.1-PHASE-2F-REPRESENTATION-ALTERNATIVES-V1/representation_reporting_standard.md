# Phase 2F.9 — Representation Comparison Reporting Standard

Every representation comparison must include:

## Identity and parity

- Phase ID, package, representation ID/version/taxonomy, code/grammar/parser/adapter hashes, exact primitive/object/relation/composition definitions.
- Same task IDs, split, demonstrations, input validation, evaluator and outcome-access sequence.
- Configured, runtime-enforced, and logged B1–B6 budgets; candidate pool vs evaluated trials; search order, stop reason, compute/time/memory. Any mismatch invalidates the causal contrast.
- Coverage-only runner access audit. Never include test targets in coverage or trace generation.

## Outcomes by stage

- **Coverage:** exact-demo-fit counts/rates and no-fit/parser/budget states.
- **Trace:** generated, independently valid, successful, diversity/support, and trace yield.
- **Invariant:** pre-threshold support distribution, patterns, proposals, rejections, validated invariants, and invariant yield.
- **Skill eligibility:** eligible and reason-coded blocked/unavailable counts.
- **Transfer eligibility:** applicability denominator and eligible skills separate from transfer outcome.
- **Capability eligibility:** criteria/denominators and `UNAVAILABLE` versus zero.
- **Accuracy:** separate sealed outcome, exact-task metric, comparator, split, uncertainty, and authorization; otherwise `NOT_MEASURED`.

## Analysis and interpretation

Use task ID as the paired unit. Report arm-specific numerators, denominators, discordant win/loss/tie counts, paired differences/intervals, and prespecified practical margins. Include failures and unavailable outcomes; no imputation. Freeze task family annotation, invariant thresholds, and representation equivalence mapping before run. Report HCC separately and never as ARC evidence. Do not label the best observed representation “best” from an exploratory comparison or promote it to confirmatory evidence post hoc.