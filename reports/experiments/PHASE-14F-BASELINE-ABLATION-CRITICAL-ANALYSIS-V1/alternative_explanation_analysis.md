# Alternative-Explanation Analysis

## Memory/retrieval

Phase 13C provides the clearest memory-friendly outcome: MEMORY_ONLY net value `1.325` vs SCT `.345`, with 440/440 applications and 418 correct vs SCT 223/440 applications and 201 correct. This is evidence exact trace retrieval can outperform skill abstraction on that synthetic stream. It is not an identical comparison to B2 in later phases, where ASFT wins several phase-specific metrics. Memory is a serious live alternative, not a total explanation for every phase.

## Frequency and simple reuse heuristics

Phase 13B frequency-only ties transfer-aware ASFT and no-transfer under both recorded accounting versions. Phase 13F's A1.1_FREQUENCY_ONLY arm ties ASFT on task utility/CGR. In Phase 13C, SCV10 has a descriptive shadow-value association (`ρ=.700`), but frequency (`ρ=.748`) and p_reuse (`ρ=.884`) are at least as strongly associated. These correlations do not prove frequency or reuse causality, but they prevent attributing observed value uniquely to the ASFT ranking logic.

## Randomness

Random controls are not uniform across phases. Phase 13C RANDOM_CREATE collapses to ALWAYS_CREATE because all eligible calibration candidates have positive SCV10 and frozen random-create probability is 1.0. Phase 13F B3 random skill creation ties ASFT on its primary utility/CGR pair; Phase 13D B3 random-skills performs much worse on its transfer utility endpoint. “Randomness rejected” is therefore only true for specific controls/outcomes.

## Compression

The 13D B4 compression proxy is at least tied/slightly ahead on a small transfer-utility contrast; 13E/F favor ASFT under other outcome gates. The proxy is not a canonical DreamCoder implementation, so neither side of this phase-dependent record resolves the broad compression alternative.

## Generator, task regularity, and metric construction

Repeated synthetic families, shared operation vocabularies, positive candidate eligibility, and task/candidate scoring can create reuse or internal-score growth without demonstrating uniquely necessary abstraction. The no-selection/no-lifecycle ties in certain runs are consistent with low decision pressure in those specific candidate pools; they do not establish that the whole benchmark can never discriminate methods. Positive CGR/IG differences can also arise from the CGM measurement pathway without a task-utility gain.

**Conclusion:** memory, simple ranking/reuse, compression, generator regularity, and metric construction all remain plausible partial explanations. No one has been proven to explain everything; ASFT-specific causal necessity is not established.
