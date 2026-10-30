Phase 10: Engineering & Implementation Blueprint
==================================================

Goal
----

Answer the question: "If we were starting implementation tomorrow, what exactly would we build, in what order, and why?"

At the end of Phase 10, we should have:
  ✅ Module breakdown
  ✅ Interfaces
  ✅ Dependencies
  ✅ MVP milestones
  ✅ Risks
  ✅ Implementation order
  ✅ What gets built in v0.1 vs v0.2

High-Level Engineering Architecture
----------------------------------

From all previous phases, ASFT v0.1 should be reduced to five core modules:

                    ┌──────────────┐
                    │ Task Dataset │
                    └──────┬───────┘
                           │
                           ▼

                 ┌───────────────────┐
                 │ Reasoning Engine  │
                 └─────────┬─────────┘
                           │
                           ▼

                 ┌───────────────────┐
                 │ Trace Logger      │
                 └─────────┬─────────┘
                           │
                           ▼

                 ┌───────────────────┐
                 │ Invariant Detector│
                 └─────────┬─────────┘
                           │
                           ▼

                 ┌───────────────────┐
                 │ Skill Creation Trigger│
                 └─────────┬─────────┘
                           │
                           ▼

                 ┌───────────────────┐
                 │ Skill Library     │
                 └─────────┬─────────┘
                           │
                           ▼

                 ┌───────────────────┐
                 │ Evaluation Layer  │
                 └───────────────────┘

Module Breakdown
---------------

Module 1: Trace Logger
  Purpose: 
    Capture reasoning traces.
  Without traces:
    No invariants, No skills, No ASFT
  Inputs:
    Task, Solver Actions
  Outputs:
    ReasoningTrace {
      task_id,
      steps[],
      outcome,
      cost,
      timestamp
    }
  Complexity: Low
  Priority: 🔥 Highest
  Build first. Everything depends on traces.

Module 2: Invariant Detector
  Contribution: IDT
  Purpose: 
    Find recurring reasoning structures.
  Input:
    ReasoningTrace[]
  Output:
    Invariant[]
  Example:
    Input traces:
      Detect Reflect Verify
      Detect Reflect Verify
      Detect Reflect Verify
    Output:
      Reflection Invariant
  Complexity: Medium
  Priority: 🟡 High
  Build second. Converts traces into invariants.

Module 3: Skill Creation Trigger
  Contribution: SCT
  Purpose: 
    Decide: Create Skill? or Do Nothing?
  Input:
    Invariant, Reuse, Transfer, Cost
  Output:
    Skill Candidate
  Core Logic:
    SCV > Threshold → Create Skill
  Complexity: Low
  Priority: 🟡 High
  Build third. The decision mechanism that makes ASFT distinctive.

Module 4: Skill Library
  Contribution: SCT + CGM
  Purpose: 
    Store reusable skills.
  Input:
    Created Skills
  Output:
    Retrieved Skills
  Structure:
    Skill {
      skill_id,
      concept_id,
      trigger_conditions,
      execution_policy,
      utility,
      reuse_count
    }
  Complexity: Low
  Priority: 🟡 High
  Build fourth. Long-term memory for the system.

Module 5: Evaluation Framework
  Contribution: CGM
  Purpose: 
    Measure: IS, AG, SU, TS, CGR, IG
  Complexity: Medium
  Priority: 🟡 High
  Build last. Validates the three research contributions.

Implementation Dependencies
--------------------------

Important: Some modules cannot exist before others.

Trace Logger → Invariant Detector → Skill Creation Trigger → Skill Library → Evaluation Layer

This is the dependency graph.

MVP Milestones
-------------

I will divide implementation into milestones.

Milestone 1: Trace Collection
  Deliverable: Reasoning Traces
  Paper Impact: None yet. Foundation layer.

Milestone 2: Invariant Discovery
  Deliverable: Detected Invariants
  Validates: IDT

Milestone 3: Skill Creation
  Deliverable: ReflectionSkill, RotationSkill, CountingSkill
  Validates: SCT

Milestone 4: Transfer
  Deliverable: Task A helps Task B
  Validates: ASFT Core Thesis

Milestone 5: Capability Growth
  Deliverable: CGR > 0
  Validates: CGR

Version Planning
---------------

v0.1: Research Prototype
  Contains:
    ✅ Trace Logger
    ✅ Invariant Detector
    ✅ Skill Trigger
    ✅ Skill Library
    ✅ Evaluation Metrics
  Goal: Validate Theory

v0.2: Concept Layer
  Adds:
    ✅ Concept Representation
    ✅ Concept Graphs
  Goal: Strengthen novelty

v1.0: ARC Integration
  Adds:
    ✅ ARC Tasks
    ✅ ARC-AGI-2
    ✅ ARC-AGI-3
  Goal: Competition readiness

Biggest Engineering Risks
------------------------

Risk 1: Invariant Discovery
  Biggest risk. Can invariants actually be found?

Risk 2: DreamCoder Overlap
  Need clear distinction.

Risk 3: Transfer Signal
  Need measurable: TS > 0

Risk 4: Capability Metrics
  Need meaningful CGR.

Deliverables of Entire Phase 10
-------------------------------

Phase 10A: Trace Logger Design
  Define the exact data structure for ReasoningTrace.
  Implement trace collection from task solving.
  Deliverable: Working trace logger.

Phase 10B: Invariant Detector Algorithms
  Define how invariants are found from traces.
  Implement the invariant detection algorithm.
  Deliverable: Working invariant detector.

Phase 10C: Skill Creation Trigger Algorithms
  Implement SCV computation.
  Implement the create/don't-create decision rule.
  Deliverable: Working skill trigger.

Phase 10D: Skill Library Design
  Define skill representation and storage.
  Implement skill retrieval and reuse.
  Deliverable: Working skill library.

Phase 10E: Evaluation Engine Design
  Implement IS, AG, SU, TS, CGR, IG metrics.
  Design experiment evaluation pipeline.
  Deliverable: Working evaluation framework.

Phase 10F: Implementation Roadmap
  Prioritize milestones.
  Define v0.1 scope.
  Create development schedule.
  Deliverable: Complete implementation plan.

My Recommendation
----------------

Start with Phase 10A: Trace Logger Design next.

Reason: Everything depends on traces. If trace design is wrong:
  Invariant Discovery fails ↓
  Skill Formation fails ↓
  ASFT fails

So Phase 10A is the foundation of the entire implementation stack.

---

Paper Artifact Mapping
----------------------

Every module in Phase 10 maps directly to paper artifacts:

Module 1 → Section 6 (Experimental Setup), Table 1 (Experiment matrix)
Module 2 → Section 7.1 (Invariant Discovery), Figure 5 (Invariant results)
Module 3 → Section 7.2 (Skill Formation), Figure 6 (Skill emergence)
Module 4 → Section 7.3 (Transfer), Figure 7 (Transfer performance)
Module 5 → Section 7.4 (Capability Growth), Figure 8 (Growth curves)

This mapping ensures that implementation is never exploratory - every line of code
traces back to a figure, table, or claim in the paper blueprint.

---

Experimental Group Priority Order
----------------------------------

I recommend building and testing in this order:

1. Trace Logger → Verify traces are being captured correctly
2. Invariant Detector → Test with synthetic reflection/rotation tasks
3. Skill Creation Trigger → Test SCV computation and skill creation decisions
4. Skill Library → Test skill storage and reuse
5. Evaluation Framework → Test all metrics (IS, AG, SU, TS, CGR)

This order follows the dependency graph and ensures that each module is validated
before moving to the next.

---

ASFT v0.1 Success Criteria (Implementation)
------------------------------------------

Before considering v0.1 complete, all of the following must work:

  ✅ Trace Logger captures reasoning traces from task solving
  ✅ Invariant Detector finds stable invariants across repeated traces
  ✅ Skill Creation Trigger computes SCV and makes create/don't-create decisions
  ✅ Skill Library stores and retrieves created skills
  ✅ Evaluation Framework computes IS, AG, SU, TS, CGR metrics
  ✅ End-to-end pipeline: Task → Trace → Invariant → Skill → Transfer → Growth

If all of the above works, we have a valid v0.1 prototype that can proceed to
v0.2 (Concept Layer) and eventual ARC integration.

---

Baseline Implementations for Phase 10
--------------------------------------

Every module needs a baseline for comparison:

Baseline A: No Learning
  - No trace storage
  - No invariant detection
  - No skill creation
  - Pure task-solving with reset after each task

Baseline B: Skill Storage Only
  - Store skills (manually labeled)
  - Retrieve skills when needed
  - No invariant discovery, no SCT

Baseline C: DreamCoder-like
  - Program compression into primitives
  - No invariant discovery, no skill formation decision

Baseline D: Random Skill Creation
  - Create skills randomly
  - Store and retrieve randomly
  - No SCV computation, no invariant-based creation

These baselines enable the component-isolation strategy defined in Phase 9D.