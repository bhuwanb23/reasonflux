# Evaluation and Reporting Plan — Design Only

## Claim-linked reporting

Every paper statement must map to one of `N, A, B, C, D, E` in the claim-evidence map. Report a claim as supported, weakened, inconclusive, or untested; never infer downstream links from upstream success.

## Required result tables (future)

1. **Run integrity:** variant, commit/hash, model/config, environment/evaluator version, seed, budget, status, exclusions.
2. **Skill formation:** candidate counts, support contexts, rejected candidates, promotion decisions, provenance completeness.
3. **Claim N:** raw replay vs strong replay vs invariant representation on held-out prediction and end-to-end outcome at matched resources.
4. **Claim B:** boundary metrics with and without counterexample evidence; coverage and false-activation rates together.
5. **Claims C/D:** harmful transfer events and full-cohort score/action efficiency, including per-game outcomes and costs.
6. **Claim E:** official score plus all baseline comparisons, uncertainty and cost accounting.
7. **Failures:** counterexamples, abstentions, action mismatch, stale transfer, timeout, crash and missing artifact counts.

## Reporting rules

- Distinguish public/development diagnostics from official hidden evaluation.
- Report score and resource costs separately; do not hide cost behind a weighted utility scalar.
- Report the full denominator and all failed/abstained cases.
- Label synthetic and ARC-AGI-2 results as background, not ARC-AGI-3 evidence.
- Report exact code/notebook version, submission ID, score receipt and team match once available.
- State limitations, negative transfer, null results and novelty uncertainty prominently.

## Paper decision rule

Do not write a result claim before a matching run artifact exists. A concept/paper direction can be developed now; a Paper Track submission must describe a real working linked AGI-3 entry. Late-entry eligibility is a separate unresolved rules question; it does not alter the scientific claim ceiling.
