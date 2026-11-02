# Phase 1E.2 — Capability Definition

## Working behavioral definition

A **capability** is a persistent, generalizable behavioral competence that enables an agent to produce measurable positive utility on a predeclared class of tasks, including unseen instances. It is established by external task behavior and evaluator-scored outputs—not by C_t, CGR, IG, IGR, or the existence/size of an internal capability object.

A capability claim has four necessary properties:

1. **Behavioral utility:** correct/quality-scored performance improves over a fixed no-learning or pre-training comparison under the same task and resource budget.
2. **Generality:** success is repeated on independently generated held-out instances and at least two surface/template partitions; exact answer replay alone does not qualify as generalization.
3. **Persistence:** performance remains after a preregistered no-refresh interval (e.g. 20 intervening tasks) and is not just immediate task-specific priming.
4. **Transfer:** for a transfer-capability claim, performance is positive on at least one disjoint family; for a cross-domain capability claim, it is positive in at least two independent domains.

The taxonomy specifies narrower subtypes; not every C1 single-skill unit must claim cross-domain transfer. It must still persist, generalize across held-out variants, and provide behavioral benefit.

## Behavioral capability-unit gate

A candidate unit is behaviorally validated only if, on independent evaluator-scored tasks:

- at least 20 held-out trials are available for the relevant capability test;
- accuracy/quality is at least 0.70 with a 95% cluster-aware lower bound at least 0.05 above the fixed baseline;
- the result holds over at least two held-out surface/template partitions;
- delayed retention is at least 90% of immediate performance after the fixed no-refresh interval; and
- paired net task utility is positive under the frozen resource-cost conversion.

Thresholds and task-score rubrics are design targets to confirm on development/calibration data before any confirmatory outcomes. They cannot be tuned on confirmation. A result that fails one criterion is reported as a partial/failed capability claim, not rescued by an internal score.

## Growth definition

**Behavioral capability growth** is an increase in the independently scored future battery (or number of validated task families) from a disjoint pre-learning baseline to a disjoint post-learning/retention battery, with paired improvement exceeding the SOI and no unacceptable regression in previously validated families. A rise in C_t, CGR, IG, or capability-object size alone is explicitly **not growth**.

## Failure criteria

A capability claim fails or remains unsupported if any of the following occurs: only internal metrics rise; performance does not exceed the same-budget baseline; success is confined to exact repeats; gains disappear after delay; no unseen variants/families transfer; composition/adaptation fails its task rubric; the evaluator or target uses CGR/C_t/IG; or resource usage differs outside the common cap. Missing or leaked outcome data produce `unavailable`, not zero or a pass.