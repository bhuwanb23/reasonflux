# Project Idea V2 — Trace-to-Transfer
## Evidence-Gated Skill Genesis for Interactive ARC Agents

**Status:** superseded by [`Project Idea V3 — From Trace to Transfer`](arc_prize_2026_project_idea_v3.md). This earlier broad skill-transfer framing is retained for history; it is not a finished novelty claim, preregistration, run authorization, code submission, score, or promise of a Paper Prize.  
**Target track per owner:** ARC-AGI-3.  
**One-sentence recommendation:** Build the paper around one testable idea: an agent should learn **conditional, falsifiable skills from experience**—not merely save successful action traces—and promote/reuse them only when their scope and expected future value are supported by evidence.

## 1. The project we should pursue

### Working title

**Trace-to-Transfer: Evidence-Gated Skill Formation for ARC-AGI-3**

### Core research question

> Can an interactive agent turn repeated experience into a compact, parameterized skill that transfers to a later level and reduces action cost—without replaying stale, level-specific behavior?

### Main hypothesis

> A skill represented as a **conditional action/effect rule**—with explicit preconditions, parameters, predicted state change, termination, provenance, and fallback—will produce more reliable cross-level transfer than storing and replaying raw action sequences, when skill creation and reuse are gated by prospective evidence and net value.

This preserves the original ASFT intuition—**experience → recurring structure → concept/skill → future task becomes easier**—but narrows it to a mechanism that can be built and falsified. “Capability growth” and “intelligence growth” should remain interpretations for future work, not claims this paper tries to prove.

## 2. What is the actual contribution?

The contribution is **not** “we have a skill library,” “skills are useful,” or “we predict before acting.” Those ideas already appear in prior systems. The candidate contribution is the coupled **skill-genesis and transfer contract**:

1. **Distill, do not copy.** From successful and failed interaction traces, propose a parameterized rule that captures a recurring state/action/effect relation. Avoid hard-coded colors, coordinates, and level-specific state unless they are explicitly part of the skill’s scope.
2. **State when it applies.** Each skill carries observable preconditions and a scope estimate, not just a name or action macro.
3. **Make the claim falsifiable.** Record the expected next-state/effect and termination condition. Check the effect during use; if it mismatches, stop, fall back, and record a counterexample rather than blindly continuing.
4. **Learn when to promote.** A candidate remains provisional until evidence supports recurrence, consistency, applicability, and useful transfer. Creation/promotion should consider future benefit against authoring, validation, maintenance, and negative-transfer costs. The existing SCV intuition is useful, but its terms need track-specific units and outcome-blind estimators; do not treat the existing formula as validated.
5. **Measure transfer prospectively.** Compare against no-skill and raw-replay controls at matched game/level starts and action budgets. Report score/action efficiency and costs separately. A reused skill is not automatically a useful skill.

A compact skill record might be:

`preconditions + parameters → action policy → predicted effect → termination/fallback + provenance/confidence`

The paper’s claim should be about **evidence-gated skill formation**, not about a complete theory of AGI.

## 3. Why this fits ARC Prize’s goals

ARC Prize says its mission is to advance open-source AGI research and defines its north star around efficient learning of new skills; ARC-AGI-3 makes adaptation interactive. The Paper Prize rewards conceptual progress and scores Accuracy, Universality, Progress, Theory, Completeness, and Novelty equally; its Progress criterion asks whether the work increases the chance of anyone reaching 85% on ARC-AGI. [Official ARC Prize mission and 2026 goals](https://arcprize.org/competitions/2026) · [Paper Prize rubric and requirements](https://arcprize.org/competitions/2026/paper)

Trace-to-Transfer is aimed at a meaningful ARC problem: **how experience from one level becomes useful, safe, action-efficient behavior on a new level**. It also offers a reusable artifact—skill schema, validation logic, and evaluation protocol—rather than a one-off score trick. Open sourcing the code, logs/schema, and reproducibility instructions is essential.

## 4. Why it could stand apart—and what we must not claim

The 2025 Paper Prize winners each presented a legible mechanism tied to evidence: recursive refinement in TRM, self-improving evolutionary program synthesis in SOAR, and MDL-driven per-task optimization in CompressARC. The lesson is to make one mechanism understandable, test it against alternatives, and explain why it works—not to make a broad architecture diagram. [Official 2025 results](https://arcprize.org/blog/arc-prize-2025-results-analysis)

**Relevant prior art is substantial.** ARC-AGI-3 work has traced code/scripts across level boundaries and documented abandonment and stale-memory transfer ([“Tracing the Thoughts…”](https://arxiv.org/html/2610.11450v1)). General agent-skill work tests skill/no-skill behavior and utility ([“Skill Use or Skill Theater?”](https://arxiv.org/html/2607.27484); [“A Framework for Evaluating Agentic Skills at Scale”](https://arxiv.org/html/2606.17819)). ARC-AGI-3 agents also use predictive action checks and executable world models ([arc-skill](https://arc-skill.vercel.app/); [“Executable World Models for ARC-AGI-3”](https://arxiv.org/html/2605.05138v1)). Therefore, do **not** claim to be first to create skills, reuse memory, test a skill’s effect, log negative transfer, or predict an action.

**Provisional differentiation to test in a deeper review:** most closely related approaches appear to study these pieces separately—script lifecycle, causal skill influence, or world-model prediction. Our candidate distinction is their integration into a learned **conditional skill object**, whose creation and later transfer are governed by explicit evidence and whose utility is tested under ARC-AGI-3’s action-efficiency constraint. This is only a gap hypothesis. A systematic literature search may narrow it further or show that it is already covered. No novelty score is earned by the name “Trace-to-Transfer.”

## 5. How it connects to the original ASFT assumptions

| Original idea / ASFT contribution | Keep, refine, or defer |
|---|---|
| Repeated experience contains stable structure | **Keep as H1.** In ARC-AGI-3, specify the stable object as an action/effect relation across varying states/levels—not an operation label supplied by a synthetic generator. |
| Invariants → concepts → skills | **Keep as a theory scaffold; simplify for the first study.** Operationalize an invariant as reusable evidence about state/action/effect structure. Do not add a subjective concept-generation stage unless it changes a measurable decision. |
| Skills are generated by learning, not just retrieved | **Make this the central contribution.** The learned skill must generalize beyond a stored trace and include a validated domain of applicability. |
| SCT: create when expected future value exceeds cost | **Keep as the promotion hypothesis.** Define estimator, evidence available at decision time, costs, missing values, and threshold before any run. Do not use hidden target outcomes to decide a skill should have existed. |
| Transfer and negative transfer matter | **Keep and strengthen.** A skill may help, be inert, or harm. Track all three; do not count invocation frequency as success. |
| Composition creates higher capabilities | **Defer.** Test atomic/conditional skill transfer first. Composition would multiply confounds and prior-art burden. |
| CGM / “intelligence growth” | **Defer or exploratory only.** Use official task performance and action efficiency as outcomes. Do not report an unvalidated composite as intelligence. |
| Skill lifecycle, retirement, and provenance | **Retain as supporting machinery.** They make the artifact practical but are not separate headline contributions in this short paper. |

## 6. A small, falsifiable study design (future work only)

### Core comparison

- **B0 — No learned skills:** same base agent and budget, with no cross-level learned-skill library.
- **B1 — Raw replay:** retain/reuse successful action traces or macros with minimal abstraction, representing ordinary episodic/script memory.
- **V1 — Evidence-gated conditional skills:** distill parameterized precondition/effect contracts from experience; validate and fall back on mismatch; promote only under a frozen evidence/value rule.
- If feasible, add **always-store conditional candidates** to isolate whether the creation/promotion trigger helps beyond the representation itself.

Hold fixed the base model, prompt, tools, memory and context budgets, game order, environment/API version, action budget, and time budget. State exactly what can persist across episodes and games. Compare on paired game/level starts where the official environment permits; report full-assignment outcomes as primary. Because skill activation is post-treatment, do not make causal claims merely by comparing episodes where a skill happened to be invoked. Only claim same-state action influence when an allowed deterministic replay/fork makes the counterfactual valid.

### Measures

- **Primary:** official ARC-AGI-3 score under the exact evaluator used by the linked code entry.
- **Predeclared efficiency secondary:** actions to level progress/completion or official action-efficiency component; report model tokens, wall time, and skill-construction/validation cost separately.
- **Mechanism diagnostics:** candidate support, precondition match, skill creation/promotion, activation, predicted-effect accuracy, fallback, cross-level reuse, stale-skill failures, negative transfer, and retention/retirement.
- **Uncertainty:** paired by game/level where valid; report per-game outcomes and run-to-run variability. Do not treat many within-game actions as independent samples.

### What would support or weaken the claim

**Support:** the evidence-gated method improves the predeclared held-out outcome versus both no-skill and raw-replay controls at matched budgets; the gain survives per-game reporting; action savings exceed skill creation/validation costs; negative transfer is contained by preconditions/fallback; the skill ledger shows actual transfer rather than mere storage or invocation.

**Weaken/falsify:** no skill candidates form; skills are unavailable or never activated; raw replay performs equally well; gated skills fail to improve outcomes; costs erase savings; stale/negative transfer offsets benefits; results occur only on source-like levels; or effects disappear under matched budgets.

No thresholds should be relaxed after observing yield. A zero-support result means the mechanism was not exercised under that setup; it does not establish that skill formation is impossible.

## 7. What the current evidence can honestly contribute

Current evidence gives a *motivation*, not validation of Trace-to-Transfer on ARC-AGI-3:

- Phase 13B: transfer-aware ranking tied frequency-only and no-transfer on its corrected primary endpoint. This warns against leading with ranker sophistication.
- Phase 13C: all 44 eligible synthetic candidates were selected; SCT, always-create, and random-create tied on the primary net-value endpoint, while the random policy degenerated to always-create. This is a direct reason to ask whether the skill-creation gate has real choice and evidence behind it; it is not evidence that the gate works generally.
- Phase 13G: the bounded ARC-AGI-2 adapter produced sparse exact-demo fits and zero invariant candidates/skills/capabilities; a budget/config mismatch and holdout exposure are disclosed. It is not an AGI-3 result and does not show that invariant or skill formation is impossible.
- Phase 14 synthesis: the complete ASFT chain, transfer-to-capability bridge, and intelligence interpretation remain unestablished.
- The local ARC-AGI-3 validation plan is a **design draft with no runs/results**. The current workspace does not contain the intended runnable AGI-3 submission agent or its score.

The project’s strongest strategic bottleneck remains **knowledge-object/skill generation and qualification**, not another ranker, composite metric, or broad readiness phase.

## 8. Critical constraints and timing

- The user chose ARC-AGI-3 and says the team has joined and can submit late. That route is separate from scientific validation. The paper must ultimately describe the exact linked interactive agent.
- Public rules say the linked code submission need not achieve a high score, but the Paper Track uses its score for Accuracy. Ordinary code-track rules say late submissions are not prize-eligible for that code competition; whether a late entry can support Paper Prize eligibility/Accuracy is not explicit and should be confirmed. This does not change the present task: clarify the research idea first.
- **Do not run Phase 2I** or access hidden/test outcomes. Phase 3B is blocked and Phase 3D unauthorized. Phase 3A is plumbing only, not scientific validation. This proposal is a discussion/design artifact and does not authorize those runs.
- The Paper Track deadline is close and official pages disagree by a day; the strategy memo uses Nov 8 UTC as the conservative target. A complete, novel, controlled AGI-3 study should not be invented or rushed into existence just to fill a paper. If the current agent cannot support the claim, submit only a narrower truthful account—or use the project as the basis for a stronger next-cycle study.

## 9. Recommendation

**Choose Trace-to-Transfer as the leading project direction, not yet as the final paper claim.** It unifies the original insight that skills should be *generated through learning* with the current ASFT evidence boundary and an ARC-AGI-3-specific problem: how an agent converts limited experience into a valid, reusable procedure that improves future play efficiently.

The idea becomes genuinely competitive only if three things are achieved: (1) a defensible novelty boundary after systematic prior-art review; (2) an exact, operational skill-generation/qualification mechanism; and (3) evidence from matched, budget-controlled outcomes showing transfer rather than memorization, reuse counts, or synthetic success. The paper should then make this one contribution legible and open source. **No one can responsibly promise a win; this is the strongest coherent route currently supported by the project and the literature scan.**
