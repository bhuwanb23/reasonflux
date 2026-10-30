Phase 11A: Repository & Code Architecture

This is the final design phase before implementation.

After Phase 11A, a new engineer should be able to open the repository and immediately understand:

What ASFT is
What each module does
What data flows where
How experiments run
How results are generated


This is not a coding phase.

This is a software architecture phase.

Phase 11A Goals

Design:

✅ Repository structure

✅ Module boundaries

✅ Data flow

✅ Interfaces

✅ Configuration strategy

✅ Experiment organization

✅ Testing organization

✅ Research reproducibility

✅ Future extensibility

Architectural Philosophy

Most research codebases become:

research_final.py

research_final_v2.py

research_final_v3_final.py

research_final_v3_final_FIXED.py


We do NOT want that.

Instead:

Research Contribution
↓
Module
↓
Interface
↓
Implementation

Top-Level Repository
asft/

├── README.md
├── requirements.txt
├── configs/
├── datasets/
├── src/
├── experiments/
├── baselines/
├── tests/
├── reports/
├── notebooks/
├── papers/
└── docs/

Root Directory Explanation
README.md

Purpose:

Project identity.

Contains:

What is ASFT?

How to run?

Research contributions

Architecture overview

requirements.txt

Dependencies only.

Keep minimal.

Example:

numpy

pandas

networkx

scikit-learn

matplotlib

configs/

Configuration layer.

Purpose:

Avoid hardcoding.

Structure:

configs/

├── default.yaml
├── experiments.yaml
├── thresholds.yaml
└── metrics.yaml


Examples

skill_creation_threshold: 2.0

minimum_invariant_strength: 5.0

datasets/

Stores task datasets.

Structure:

datasets/

├── synthetic/
│   ├── reflection/
│   ├── rotation/
│   ├── counting/
│
└── arc/


Why?

We decided during Phase 8B:

Synthetic First

ARC Second

src/

The heart of the system.

Structure:

src/

├── core/
├── traces/
├── invariants/
├── skills/
├── evaluation/
├── transfer/
├── utils/
└── pipelines/


Everything important lives here.

src/core/

Core data models.

Purpose:

Shared objects.

Structure:

core/

task.py

trace.py

invariant.py

skill.py

capability.py


Examples

Task

ReasoningTrace

Invariant

Skill

CapabilityState


Everything imports from here.

src/traces/

Contribution support:

IDT


Purpose:

Trace logging.

Storage.

Management.

Structure:

traces/

logger.py

trace_store.py

trace_similarity.py

normalizer.py


Responsibilities

Capture traces

Store traces

Normalize traces

Compare traces

src/invariants/

Contribution:

Invariant Discovery Theory


Purpose:

Invariant detection engine.

Structure:

invariants/

cluster.py

pattern_mining.py

strength.py

ranking.py

detector.py


Responsibilities

Trace Clustering

Pattern Discovery

IS Computation

Invariant Ranking

src/skills/

Contribution:

Skill Creation Trigger Theory


Purpose:

Skill lifecycle.

Structure:

skills/

candidate.py

trigger.py

promotion.py

library.py

retrieval.py

retirement.py


Responsibilities

Generate Candidates

Compute SCV

Create Skills

Store Skills

Retrieve Skills

src/evaluation/

Contribution:

Capability Growth Metrics


Purpose:

All measurements.

Structure:

evaluation/

invariant_metrics.py

skill_metrics.py

transfer_metrics.py

growth_metrics.py

reports.py


Responsibilities

Compute:

IS

SU

TS

CGR

IG

src/transfer/

Purpose:

Explicit transfer experiments.

Structure:

transfer/

task_mapper.py

reuse_engine.py

transfer_tracker.py


Responsibilities

Measure:

Task A
↓
Task B


effects.

src/utils/

Generic utilities.

Structure:

utils/

config.py

logging.py

serialization.py

visualization.py


Keep generic code here.

src/pipelines/

This becomes the orchestration layer.

Structure:

pipelines/

trace_pipeline.py

invariant_pipeline.py

skill_pipeline.py

evaluation_pipeline.py

full_asft_pipeline.py


Example

Task
↓
Trace
↓
Invariant
↓
Skill
↓
Evaluation


Executed here.

experiments/

Research experiments.

Structure:

experiments/

exp01_invariants/

exp02_skills/

exp03_transfer/

exp04_growth/

exp05_end_to_end/


One folder per paper experiment.

This maps directly to Phase 9C.

baselines/

Critical for publication.

Structure:

baselines/

no_learning/

skill_storage/

dreamcoder_like/

random_skill_creation/


Never mix baseline code with ASFT code.

tests/

Testing layer.

Structure:

tests/

test_traces.py

test_invariants.py

test_skills.py

test_transfer.py

test_metrics.py


Every major module gets tests.

reports/

Generated outputs.

Structure:

reports/

figures/

tables/

metrics/

logs/


Stores:

Figure 1

Figure 2

Table 1

etc.


for paper generation.

notebooks/

Exploration only.

Structure:

notebooks/

invariant_analysis.ipynb

skill_analysis.ipynb

growth_analysis.ipynb


Rule:

Never put production logic here.

papers/

Paper writing support.

Structure:

papers/

outline.md

figures/

tables/

drafts/


Directly linked to Phase 9E.

docs/

Architecture documents.

Structure:

docs/

architecture.md

metrics.md

experiments.md

roadmap.md


Allows future contributors to onboard.

Data Flow Architecture

This is the most important diagram.

Task
↓
Trace Logger
↓
Trace Store
↓
Invariant Detector
↓
Invariant Ranking
↓
Skill Trigger
↓
Skill Library
↓
Transfer Engine
↓
Evaluation Engine
↓
Reports

Module Dependency Graph

Very important.

core
│
├── traces
│
├── invariants
│
├── skills
│
├── transfer
│
└── evaluation


Rule:

Evaluation
cannot depend
on experiments


Keep dependencies clean.

Research-to-Code Mapping

This is crucial.

Research Contribution	Code ModuleIDT	traces + invariants
SCT	skills
CGM	evaluation
Transfer Hypothesis	transfer
End-to-End ASFT	pipelines
MVP Build Order

Engineering sequence:

1 Core Models

2 Trace Logger

3 Trace Store

4 Invariant Detector

5 IS Metrics

6 Skill Trigger

7 Skill Library

8 Transfer Engine

9 Evaluation Engine

10 Experiments

What We Intentionally Exclude

Not in v0.1:

LLMs

Neural Networks

Meta-Reasoner

Concept Graphs

ARC-3 Agents

World Models

Autonomous Planning


Keep MVP focused.

Deliverables of Phase 11A

✅ Repository structure

✅ Source architecture

✅ Module boundaries

✅ Data flow design

✅ Dependency graph

✅ Experiment structure

✅ Baseline structure

✅ Testing structure

✅ Paper integration structure

✅ MVP implementation order

Most Important Outcome

The biggest decision of Phase 11A is:

ASFT will be organized around research contributions, not around algorithms.

Meaning:

Invariant Discovery Theory
↓
Code Module

Skill Creation Trigger Theory
↓
Code Module

Capability Growth Metrics
↓
Code Module


This keeps the repository aligned with the paper, experiments, and scientific claims.

Next Deep-Dive Phase

Phase 11B: Data Models & Interfaces

There we will fully specify:

Task
ReasoningTrace
Invariant
Skill
CapabilityState
all interfaces between modules
serialization formats
versioning strategy
API contracts

This becomes the actual blueprint developers use while implementing the repository.