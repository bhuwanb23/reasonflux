Phase 11: Implementation Planning
================================

Goal
----

Convert the research blueprint into a concrete implementation roadmap with module definitions, dependency order, and MVP milestones.

At the end of Phase 11, we should have:
  ✅ Detailed module specifications
  ✅ Algorithm designs for each component
  ✅ Exact inputs/outputs for every module
  ✅ Development schedule and resource allocation
  ✅ MVP scope definition for v0.1
  ✅ Risk mitigation plan

This phase ensures that implementation is never exploratory - every line of code
traces back to a figure, table, or claim in the paper blueprint.

---

Module Specifications
--------------------

Module 1: Trace Logger
---------------------

Input/Output Signature:
  Input:  Task ID, solver actions/steps, outcome (success/failure), cost metric
  Output: ReasoningTrace record written to trace store

Data Structure:
  ReasoningTrace = {
    trace_id: string,           // Unique identifier
    task_id: string,            // Source task identifier
    timestamp: float,           // When the trace was generated
    steps: [ReasoningStep],     // Sequence of cognitive operations
    outcome: { success: bool, result: any, cost: float },
    invariants: [Invariant],    // Initially empty; populated later
    skills: [SkillRef]          // Initially empty; populated later
  }

ReasoningStep = {
    step_id: string,
    operation: string,          // e.g., "detect_pattern", "apply_rule"
    inputs: [any],              // Inputs to the operation
    outputs: [any],             // Outputs from the operation
    cost: float,                // Computational cost of this step
    duration: float             // Wall-clock time
  }

Algorithm Design:
  1. Intercept task execution after completion
  2. Capture the sequence of operations performed
  3. Record the time and computational cost per operation
  4. Store the final outcome (success/failure + metric values)
  5. Associate trace with task_id for later grouping

Priority: 🔥 Highest (foundation module - everything depends on traces)
Estimated Effort: 3 days
Dependencies: None (starts immediately)

Module 2: Invariant Detector
---------------------------

Input/Output Signature:
  Input:  [ReasoningTrace, ...]  (collection of traces from same task family)
  Output: [Invariant, ...]       (detected recurring structures)

Data Structure:
  Invariant = {
    invariant_id: string,        // Unique identifier (e.g., INV-001)
    pattern_signature: [string], // Sequence of step types or features
    frequency: int,              // How many traces contain this pattern
    consistency: float,          // % of traces where pattern appears with same meaning
    generality: float,           // Across how many task families this pattern holds
    strength: float,             // Computed: frequency × consistency × generality
    associated_concepts: [string] // e.g., ["reflection", "rotation"]
  }

Algorithm Design:
  1. Normalize all traces: align step types, extract feature vectors
  2. Apply pattern mining (e.g., Apriori-like algorithm) to find frequent step sequences
  3. Calculate frequency: count of traces containing each pattern
  4. Calculate consistency: for each pattern, % of traces where it appears with same semantic meaning
  5. Calculate generality: test pattern across task families (reflection, rotation, counting, etc.)
  6. Compute strength = frequency × consistency × generality
  7. Filter: keep patterns above minimum strength threshold (e.g., > 5.0)
  8. Group similar invariants; merge related concepts

Priority: 🟡 High (validates IDT contribution)
Estimated Effort: 5 days
Dependencies: Module 1 (Trace Logger - must have traces before detecting invariants)

Module 3: Skill Creation Trigger
-------------------------------

Input/Output Signature:
  Input:  Invariant, Reuse Count, Abstraction Gain, Transfer Score, Creation Cost
  Output: Skill Creation Decision (create/don't-create) + Skill Candidate

Data Structure:
  SkillCandidate = {
    skill_id: string,                        // Unique identifier
    concept_id: string,                      // e.g., "reflection", "rotation"
    trigger_conditions: [string],           // e.g., ["symmetry_detected", "pattern_matched"]
    execution_policy: string,               // e.g., "apply_reflection", "apply_rotation"
    abstraction_gain: float,                // AG = RC_before - RC_after
    transfer_score: float,                  // TS = (Performance_after - Performance_before)
    creation_cost: float,                   // Cost to create the skill (compute + store)
    scv: float,                             // Skill Creation Value = Reuse × AG × TS - CreationCost
    reuse_count: int,                       // Initially 0; incremented each reuse
    utility: float                          // SU = AccuracyGain × CostReduction × Transferability
  }

Decision Rule:
  Compute SCV = Reuse × AG × TS - CreationCost
  If SCV > threshold (e.g., 0.0 or configurable): CREATE skill
  Otherwise: DO NOT create; continue observing

Algorithm Design:
  1. For each detected invariant, compute reuse count from trace history
  2. Compute Abstraction Gain: compare reasoning cost before/after invariant application
  3. Compute Transfer Score: measure performance improvement on related tasks
  4. Set Creation Cost: estimate based on skill complexity (step count, concept depth)
  5. Calculate SCV using the formula
  6. Apply decision rule: create if SCV > threshold
  7. If creating: generate SkillCandidate, store in Skill Library
  8. If not creating: log reason (low reuse, low AG, low TS, high cost)

Priority: 🟡 High (validates SCT contribution - the distinctive mechanism)
Estimated Effort: 4 days
Dependencies: Module 2 (Invariant Detector - needs detected invariants); Module 1 (Trace Logger)

Module 4: Skill Library
----------------------

Input/Output Signature:
  Input:  SkillCandidate (from SCT), Retrieval Request (task context, skill need)
  Output: Selected Skill (or null if no suitable skill found), Updated Library

Data Structure:
  SkillLibrary = {
    skills: [Skill],
    concepts: {concept_id: [Skill]},  // Index skills by concept
    relationships: [Relationship],      // e.g., ["reflection + rotation → transformation"]
    statistics: {
      total_skills: int,
      total_creations: int,
      total_retrievals: int,
      avg_reuse_per_skill: float,
      avg_skill_age: float              // How long skills persist
    }
  }

Skill = {
    skill_id: string,
    concept_id: string,
    trigger_conditions: [string],
    execution_policy: string,
    utility: float,
    reuse_count: int,
    creation_task_id: string,
    creation_timestamp: float,
    last_used_timestamp: float,
    associated_invariant: string
}

Relationship = {
    skill_a: string,
    skill_b: string,
    relationship_type: string,  // e.g., "composite", "prerequisite", "variant"
    strength: float
  }

Algorithm Design:
  1. Store newly created skills with full metadata
  2. Index skills by concept_id for fast retrieval
  3. On retrieval request: match task context against trigger_conditions
  4. If multiple skills match: select by highest utility × lowest age
  5. Increment reuse_count on successful retrieval and use
  6. Update last_used_timestamp
  7. Periodically prune: remove skills with very low reuse count and high age
  8. Track relationships: when two skills are used together, create Relationship entry

Priority: 🟡 High (enables skill reuse and transfer)
Estimated Effort: 4 days
Dependencies: Module 3 (Skill Creation Trigger - needs skill candidates); Module 1 (Trace Logger)

Module 5: Evaluation Framework
-----------------------------

Input/Output Signature:
  Input:  System state (traces, invariants, skills, library metrics), Task performance data
  Output: Metric package {IS, AG, SU, TS, CGR, IG} + Evaluation Report

Metric Definitions:
  IS (Invariant Strength): Already defined in Invariant; per-task aggregation
  AG (Abstraction Gain): RC_before - RC_after for skill-augmented vs. baseline
  SU (Skill Utility): AccuracyGain × CostReduction × Transferability
  TS (Transfer Score): (Performance_after - Performance_before) / B_before
  CGR (Capability Growth Rate): (Capability_t - Capability_{t-1}) / Δt
    where Capability = num_concepts × num_skills × avg(transfer_score) × avg(reuse_count)
  IG (Intelligence Growth): f(AG, SU, TS, CGR) = weighted combination

  IG = w1 × AG + w2 × SU + w3 × TS + w4 × CGR
  (weights determined by contribution importance; default: all 0.25)

Algorithm Design:
  1. After each task: compute IS from current invariants
  2. Compute AG: compare reasoning cost on current task with/without active skills
  3. Compute SU: for each skill used, accuracy_gain × cost_reduction × transferability
  4. Compute TS: track performance on transfer tasks vs. baseline
  5. Compute CGR: compare capability score before and after task sequence
  6. Compute IG: weighted combination of all above
  7. Generate Evaluation Report with per-metric values, trends, and baseline comparisons
  8. Store metrics in evaluation datastore for longitudinal analysis

Priority: 🟡 High (validates CGM contribution)
Estimated Effort: 5 days
Dependencies: Module 4 (Skill Library - needs skills to evaluate); Module 2 (Invariants); Module 3 (SCV calculations)

---

Dependency Graph
---------------

Trace Logger → Invariant Detector → Skill Creation Trigger → Skill Library → Evaluation Layer

This is the strict dependency order. Each module requires output from the previous.

Why this order matters:
  - No traces = no invariants can be detected
  - No invariants = no skill creation decisions can be made
  - No skill creation = skill library remains empty
  - No skills = no capability growth to measure

If any module is skipped or implemented out of order, the entire pipeline breaks.

---

MVP Milestones
-------------

Milestone 1: Trace Collection Prototype
  Deliverable: Working trace logger that captures ReasoningTrace from synthetic tasks
  Test Tasks: 5 reflection tasks, 5 rotation tasks
  Validation: Traces stored correctly; steps, outcomes, costs captured
  Paper Impact: Foundation for all later modules; enables IDT validation

Milestone 2: Invariant Detection Engine
  Deliverable: Can detect Reflection Invariant from 3+ repeated reflection traces
  Test: 3 reflection traces → should detect "reflection" pattern
  Validation: Invariant strength > threshold; pattern_signature matches expected
  Paper Impact: Validates IDT; enables Section 7.1 and Figure 5

Milestone 3: Skill Creation Mechanism
  Deliverable: SCV computation and create/don't-create decisions work correctly
  Test: Repeated reflection tasks → SCV > threshold → ReflectionSkill created
  Validation: Skill created automatically; SCV formula produces expected sign
  Paper Impact: Validates SCT; enables Section 7.2 and Figure 6

Milestone 4: Skill Library & Transfer
  Deliverable: Skills stored and retrieved; Task A helps Task B
  Test: Learn reflection skill on Task A; apply on Task B (reflection + counting)
  Validation: TS > 0; reasoning cost reduced; skill reuse_count incremented
  Paper Impact: Validates core ASFT thesis; enables Section 7.3 and Figure 7

Milestone 5: Capability Growth Validation
  Deliverable: CGR > 0 across task sequence; agent measurably improving
  Test: Sequence of 10+ tasks; track capability score after each
  Validation: Positive CGR; IG correlates with TS and AG
  Paper Impact: Validates CGM; enables Section 7.4 and Figure 8

---

Version Planning
---------------

v0.1: Research Prototype
  Contains (all 5 modules):
    ✅ Trace Logger
    ✅ Invariant Detector
    ✅ Skill Creation Trigger
    ✅ Skill Library
    ✅ Evaluation Framework
  Goal: Validate theory with minimal viable system
  Target: End of Phase 11 / beginning of Phase 12
  Success: All 5 modules functional; end-to-end pipeline works

v0.2: Concept Layer
  Adds:
    ✅ Concept Representation (structured concept objects)
    ✅ Concept Graphs (relationships between concepts)
  Goal: Strengthen novelty; enable more sophisticated transfer
  Target: 2-3 weeks after v0.1 functional
  Success: Concept graph enables cross-concept transfer scenarios

v1.0: ARC Integration
  Adds:
    ✅ ARC Tasks (real ARC-AGI problem formats)
    ✅ ARC-AGI-2 evaluation
    ✅ ARC-AGI-3 evaluation
    ✅ Competition-ready pipeline
  Goal: ARC Paper Track submission readiness
  Target: After v0.2 validated on synthetic tasks
  Success: System runs on ARC tasks; contributions empirically validated

---

Implementation Priority Order
----------------------------

I recommend implementing modules in this exact order:

1. **Module 1: Trace Logger** (Week 1)
   - Foundation: everything depends on traces
   - Risk: If trace design is wrong, everything downstream fails
   - Deliverable: Working trace capture from 3 synthetic task families

2. **Module 2: Invariant Detector** (Week 2-3)
   - Validates IDT contribution
   - Test with reflection/rotation/counting traces
   - Deliverable: Can detect invariants from 3+ repeated traces

3. **Module 3: Skill Creation Trigger** (Week 4)
   - Validates SCT contribution (the distinctive mechanism)
   - Test SCV computation with configurable thresholds
   - Deliverable: Automatic skill creation/rejection decisions

4. **Module 4: Skill Library** (Week 5)
   - Enables skill reuse and transfer
   - Test storage, retrieval, reuse counting
   - Deliverable: Skills persist and are reusable

5. **Module 5: Evaluation Framework** (Week 6)
   - Validates CGM contribution
   - Compute all 6 metrics: IS, AG, SU, TS, CGR, IG
   - Deliverable: Full metric package after each task

This order follows the dependency graph and ensures each module is validated
before moving to the next. You cannot successfully validate Module 5 without
Modules 1-4 working first.

---

Risk Mitigation Plan
--------------------

Risk 1: Invariant Discovery Fails
  - Symptom: No invariants detected from repeated traces
  - Mitigation: 
    - Start with very simple task family (only reflection tasks)
    - Use golden-set traces manually labeled first
    - Debug by examining: What patterns appear in 3+ traces?
    - Adjust: lower frequency threshold, adjust consistency calculation
  - Go/No-Go: If after 20 reflection traces no invariant detected → redesign trace capture

Risk 2: DreamCoder Overlap (novelty risk)
  - Symptom: Reviewers say ASFT = DreamCoder + new terminology
  - Mitigation:
    - Emphasize invariant discovery vs. program compression distinction
    - Document: ASFT discovers "what remains true"; DreamCoder compresses "what repeats"
    - Ensure SCV decision mechanism is clearly different from DreamCoder's primitive creation
    - In paper: Use exact separation: "Program Compression vs. Skill Formation Through Invariant Discovery"
  - Go/No-Go: If cannot clearly distinguish from DreamCoder → strengthen novelty case in paper

Risk 3: Transfer Signal Too Weak
  - Symptom: TS ≈ 0; skills created but no transfer observed
  - Mitigation:
    - Design transfer tasks more carefully: ensure conceptual similarity
    - Increase skill reuse threshold; ensure skills are actually used
    - Check: Are invariants actually meaningful for transfer tasks?
    - Adjust: increase task family similarity; ensure invariants match transfer needs
  - Go/No-Go: If TS remains near zero after 20 tasks → reevaluate invariant selection or task design

Risk 4: Capability Metrics Uncorrelated
  - Symptom: CGR computed but doesn't correlate with future performance
  - Mitigation:
    - Validate IS → TS → CGR chain explicitly in experiments
    - Ensure capability score weights are meaningful (not arbitrary)
    - Correlate CGR with actual transfer task performance
    - In paper: Be honest about limitations; CGR is a framework, not guaranteed predictor
  - Go/No-Go: If CGR shows no pattern after 30 tasks → revisit capability score formula

---

Paper Artifact Mapping (Phase 11 → Paper)
----------------------------------------

Every module specification maps directly to paper artifacts:

Module 1 → Section 6 (Experimental Setup), Table 1 (Experiment matrix)
  - Enables the trace-based experimental paradigm

Module 2 → Section 7.1 (Invariant Discovery), Figure 5 (Invariant results)
  - IS values, invariant precision/recall, discovered invariants per task family

Module 3 → Section 7.2 (Skill Formation), Figure 6 (Skill emergence)
  - SCV values, skill creation decisions, timeline of when skills emerge

Module 4 → Section 7.3 (Transfer), Figure 7 (Transfer performance)
  - TS values, skill reuse counts, transfer across task families

Module 5 → Section 7.4 (Capability Growth), Figure 8 (Growth curves)
  - CGR values, IG trajectory, capability score over task sequence

Experimental Matrix (Table 1):
  - Each module's output maps to an experiment column
  - Baselines compared against each module's output

Ablation Matrix (Table 3):
  - Removing each module tests its contribution
  - A1: No Invariant Detector → IDT weakened
  - A2: No Skill Trigger → SCT weakened
  - A3: No Skill Library → Transfer collapses
  - A4: No Evaluation → CGM unmeasurable
  - A5: Full system → all metrics positive

---

Phase 11 Deliverables Summary
------------------------------

✅ Module 1: Trace Logger - spec, algorithm, data structure
✅ Module 2: Invariant Detector - spec, algorithm, data structure
✅ Module 3: Skill Creation Trigger - spec, algorithm, data structure
✅ Module 4: Skill Library - spec, algorithm, data structure
✅ Module 5: Evaluation Framework - spec, algorithm, data structure
✅ Dependency graph: Trace → Invariant → Trigger → Library → Evaluation
✅ MVP milestones (5 phases from trace collection → capability growth)
✅ Version plan: v0.1 → v0.2 → v1.0
✅ Implementation priority order (1→2→3→4→5)
✅ Risk mitigation plan (4 risks with mitigations and go/no-go criteria)
✅ Paper artifact mapping (each module → paper sections/figures/tables)

---

Recommended Next Step
--------------------

After Phase 11, proceed to:

**Phase 12: Minimal Implementation (v0.1 Prototype)**

Build the smallest working ASFT prototype that validates all three contributions:
  - Trace Logger captures reasoning traces
  - Invariant Detector finds stable invariants
  - Skill Creation Trigger computes SCV and makes decisions
  - Skill Library stores and retrieves skills
  - Evaluation Framework computes IS, AG, SU, TS, CGR, IG
  - End-to-end pipeline: Task → Trace → Invariant → Skill → Transfer → Growth

Phase 12 deliverable: A Python prototype (not full AAA) that can run the
Phase 9 experiments (E1-E6) on synthetic task families and produce quantitative
outputs for all 3 contributions.

This is the bridge between the research blueprint and actual code. Once v0.1
is built and the experiments run, we have empirical evidence to support or
falsify the thesis, and the path to ARC Paper Track submission becomes clear.

---

Estimated Timeline (if starting immediately)
-------------------------------------------

Week 1-2: Module 1 (Trace Logger) + Module 2 (Invariant Detector)
Week 3-4: Module 3 (Skill Creation Trigger)
Week 5: Module 4 (Skill Library)
Week 6: Module 5 (Evaluation Framework) + integrate all modules
Week 7-8: MVP milestones 1-5 validation
Week 8+: Phase 13 (Experimental Validation on prototype)

Total: ~8 weeks from start to validated v0.1 prototype ready for experiment execution.

---

This Phase 11 document provides the complete implementation planning detail needed
to convert the ASFT research blueprint into a concrete development roadmap. Every
module is spec'd, every dependency clarified, every risk anticipated, and every
artifact mapped to the paper. This ensures implementation is never exploratory -
every line of code traces back to a claim, figure, or table in the paper blueprint.