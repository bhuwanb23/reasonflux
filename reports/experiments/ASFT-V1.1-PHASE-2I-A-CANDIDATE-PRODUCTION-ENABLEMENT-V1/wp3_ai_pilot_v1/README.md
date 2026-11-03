# WP3-AI-PILOT — Exploratory Only

**Not Independent Annotation**  
**Not Eligible For Family Qualification**  
**Not Eligible For Candidate Eligibility**  
**Not Eligible For Phase 2I Execution**  
**Not Eligible For WP3 Completion**

## Purpose

This is the explicitly authorized, non-qualifying AI pilot for checking whether the frozen family rubric is usable. It is protocol-development material only. It does not replace the required two independent human coders or separate human adjudicator.

## What was done

- Selected 12 of the 600 discovery-only train packets by a deterministic hash of task ID and pilot version; no solver results or labels influenced selection.
- Created two rubric-conditioned AI passes and a separate AI adjudication pass from the training demonstrations only.
- Computed descriptive agreement, confusion counts, label distribution, and an ambiguity-rate check.
- Kept all pilot files in this isolated directory. They are not imported by the Phase 2I runner, candidate identity ledger, or family eligibility code.

The passes were produced by the same AI assistant in separate rubric-conditioned reviews. They are **not independent annotators**; agreement statistics here are descriptive prompt-sensitivity measurements, not reliability evidence. The adjudication is likewise not independent.

## Result at a glance

- Sample: 12 tasks; 4/12 primary-family labels matched between AI passes (33.3%).
- Descriptive Cohen's κ: 0.232.
- AI adjudication retained `UNKNOWN_AMBIGUOUS` for 4/12 tasks (33.3%).
- The pilot suggests the rubric needs clearer decision guidance for crop-versus-target selection, color change versus relational selection, and pattern completion versus spatial change.

These are small-sample rubric-debugging signals, not estimates about the 600-task population.

## Files

- `prompt_specification.md` — pass instructions and the non-independence boundary.
- `pass_A.md`, `pass_B.md` — the two exploratory label streams.
- `ai_adjudication.md` — exploratory resolution notes, preserving unresolved cases.
- `agreement_report.md` — agreement table and rubric stress-test findings.
- `pilot_manifest.json` — source packet, sample, version, scope locks, and file hashes.
