# Phase 1G.9 — ARC Accuracy Benchmark Specification

## Outcomes

- **Exact task accuracy:** number of tasks for which every hidden test output exactly matches evaluator gold ÷ scored tasks.
- **Partial pixel accuracy:** number of correct predicted cells ÷ total scored cells, pooled only under frozen task weighting; also report per-task average to prevent large grids dominating.
- **Family/phenomenon accuracy:** exact and partial outcomes by independently annotated or preregistered category; preserve ambiguous/unknown categories and annotator agreement.
- **Transfer accuracy:** exact task success within explicitly eligible skill-transfer attempts, reported separately from all-task transfer-split accuracy.

Use task ID as the independent unit. Report denominators and confidence intervals; candidate trials and multiple test pairs are nested. Include fixed-search/no-learning, episodic-memory, random, compression-proxy, and ASFT arms under identical task and runtime budgets. Report unsupported tasks as failures for bounded-system accuracy, while keeping their representation status separate.

## Separation rule

Accuracy is computed from system test outputs and independent evaluator gold. Coverage is computed from demonstration fit/search under the frozen representation without reading test outputs. Transfer requires an eligible skill/task pairing and a matched contrast. None may be substituted for another. A system may have high demo-fit coverage and low test accuracy; low coverage and low accuracy; or high coverage with low transfer. Report the vector of outcomes and failure stages, never a single conflated “ARC score.” Official/private ARC evaluation results remain unclaimed unless a separately authorized, protocol-compliant submission is actually made and scored.