# WP3-AI-PILOT — Exploratory Only

**Not Independent Annotation**  
**Not Eligible For Family Qualification**  
**Not Eligible For Candidate Eligibility**  
**Not Eligible For Phase 2I Execution**  
**Not Eligible For WP3 Completion**

## Source and blinding

Both passes used only the 12 sampled rows from the existing blank, train-only annotator packet. Each row contained a stable task ID and training input/output pairs only. No test fields, solver programs, traces, candidate results, candidate yields, program-derived families, or future outcomes were read or supplied. The passes used the same sample and the same frozen ontology version.

## AI Pass A instruction

For each task, infer the simplest primary semantic rule family that explains all shown training pairs. Use the ontology in `family_annotation_protocol.md`; cite pair indices and briefly explain the task-level regularity. Prefer a primary mechanism when supported. Use `UNKNOWN_AMBIGUOUS` if the examples do not distinguish plausible explanations. Do not use solver-language names as evidence. Record a confidence estimate, but do not overstate certainty.

## AI Pass B instruction

Review the same training-only tasks under a counter-hypothesis lens. Before choosing a family, check whether the apparent action is secondary to target selection, repetition/count, symmetry/pattern completion, or region structure. Challenge the simplest Pass-A-style interpretation and use `UNKNOWN_AMBIGUOUS` when the primary mechanism cannot be separated from a plausible alternative from the demonstrations alone. Cite pair indices and confidence.

## AI adjudication instruction

Compare the two AI outputs against the rubric and demonstrations. Preserve agreement; for disagreement, state the competing readings and select a primary family only if the training examples support the rubric's priority rules. Otherwise retain `UNKNOWN_AMBIGUOUS`. This pass is a same-assistant synthesis, not a third independent adjudicator.

## Independence and use limits

Pass A, Pass B, and adjudication are all outputs of the same AI assistant in one conversation. Pass B is a counter-hypothesis review and may be influenced by earlier reasoning; it is not a separately hosted or genuinely blind stream. The separate prompts do not create independent annotators or a blind human adjudication process. Consequently:

- no pass is a WP3 coder stream;
- agreement and κ are descriptive only;
- adjudicated labels are not frozen or accepted family labels;
- no label may enter the Phase 2I runner, candidate registry, or ≥2-family eligibility gate;
- this pilot does not complete WP3 or authorize Phase 2I/Phase 3.
