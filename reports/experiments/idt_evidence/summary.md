# IDT Evidence Package

- **Phase 13B success:** `False`
- **Seeds:** `[0, 1, 2, 3, 4]`

## Discovery

- **reflection:** discovery rate `1.000`, IS `6.000`
- **rotation:** discovery rate `1.000`, IS `3.000`
- **counting:** discovery rate `1.000`, IS `5.067`
- **grouping:** discovery rate `1.000`, IS `4.900`

## Quality

- IP: `1.000 ± 0.000`
- IR: `1.000 ± 0.000`
- Confidence: `0.660`

## Transfer

- Pearson IS–TS: `1.000`
- Spearman IS–TS: `1.000`
- TU: `0.066`

## Baseline comparison (predeclared top-k = 2)

- ASFT mean transfer utility: `0.095809`
- Frequency-only: `0.095809`
- No-transfer: `0.095809`
- Random pattern: `0.063113`
- Paired ASFT − frequency-only: `0.000000` (95% normal CI `0.000000` to `0.000000`)
- Paired ASFT − no-transfer: `0.000000`
- ASFT ranking identical to frequency on all seeds: `True`
- ASFT ranking identical to no-transfer on all seeds: `True`
- Strict per-seed superiority gate passed: `False`; a tie is not a win.

## Robustness

- VST: `1.000`
- Rank stability: `0.720`

## Interpretation

These results evaluate IDT on the governed synthetic mechanism dataset. They measure discovery, quality, transfer, and robustness; they are not ARC leaderboard results.
