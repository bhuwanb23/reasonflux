Phase 7: Research Contribution Definition

This is arguably the most important phase after all our investigations.

A weak paper says:

"Here are 15 ideas."

A strong paper says:

"Here are 3 contributions. Each one is novel, measurable, and important."

After everything we've done, I would not use the example contributions exactly as-is. We should refine them into the strongest possible form.

Phase 7 Goal

Reduce the entire ASFT framework into exactly 3 research contributions:

Contribution 1
How abstractions are discovered

Contribution 2
When new skills should be created

Contribution 3
How intelligence growth should be measured


Notice something:

These correspond directly to the three biggest gaps we identified across:

ARC philosophy
ARC winners
DreamCoder
Neuro-symbolic systems
Cognitive science
Contribution 1
Invariant Discovery Theory (IDT)
Research Problem

Current systems are good at:

Finding solutions


But poor at:

Finding what remains true across solutions

Core Claim

Transferable knowledge emerges from discovering invariants across reasoning experiences.

Main Hypothesis

Suppose an agent solves:

Task A
Task B
Task C


Instead of storing:

Solution A
Solution B
Solution C


The agent extracts:

Invariant I


that explains all three.

Example

Observed:

Mirror Red Shape
Mirror Blue Shape
Mirror Green Shape


Invariant:

Reflection

Scientific Contribution

Introduce:

Invariant Strength (IS)

IS(I)=Frequency×Consistency×GeneralityIS(I) = Frequency \times Consistency \times Generality
Why This Matters

DreamCoder compresses recurring programs.

IDT attempts to discover recurring explanatory structure.

This is our first major distinction from existing work.

Validation Experiment

Question:

Can invariant extraction predict transfer?


Measure:

High IS
↓
Higher Transfer Score

One-Sentence Contribution

We introduce Invariant Discovery Theory, which models transferable knowledge as stable structures recurring across reasoning experiences.

Contribution 2
Skill Creation Trigger Theory (SCT)

This may actually be our strongest contribution.

Research Problem

Current systems can:

Use Skills
Store Skills
Retrieve Skills


But rarely answer:

When should a new skill be created?

Core Claim

A new skill should emerge when the expected reduction in future reasoning cost exceeds the cost of creating the skill.

Main Hypothesis

Instead of:

More Search
More Search
More Search


the system asks:

Should I create a reusable skill?

Formal Criterion

Using our previous work:

SCV=Reuse×AG×TS−CreationCostSCV = Reuse \times AG \times TS - CreationCost

where:

AG = Abstraction Gain
TS = Transfer Score

Create skill if:

SCV>0SCV > 0
Why This Matters

This is the first explicit theory we have encountered answering:

How does an agent decide that a new skill is worth inventing?

Neither ARC winners, DreamCoder, nor most neuro-symbolic systems explicitly center this decision process.

Validation Experiment

Compare:

Baseline
Always Search


vs

ASFT
Create Skill When SCV > 0


Measure:

Future Reasoning Cost

One-Sentence Contribution

We introduce Skill Creation Trigger Theory, a decision-theoretic mechanism for determining when reusable skills should emerge from repeated reasoning.

Contribution 3
Capability Growth Metrics (CGM)

This is our evaluation contribution.

Research Problem

Current ARC systems are evaluated primarily through:

Accuracy


But ARC's philosophy is closer to:

Skill Acquisition Efficiency


than static task performance. On the Measure of Intelligence explicitly defines intelligence around efficient skill acquisition and generalization.

Core Claim

Intelligence should be measured by how much solving one task improves performance on future tasks.

Main Hypothesis

Instead of asking:

Did Task A get solved?


Ask:

How much easier did Task B become?

Metrics
Transfer Score
TS=Performanceafter−PerformancebeforeTS = Performance_{after} - Performance_{before}
Capability Growth Rate
CGR=Capabilityt−Capabilityt−1ΔtCGR = \frac {Capability_t-Capability_{t-1}} {\Delta t}
Intelligence Growth
IG=f(AG,SU,TS,CGR)IG = f(AG,SU,TS,CGR)
Why This Matters

This contribution gives us a way to evaluate:

Agent Improvement


rather than:

Single Task Success

Validation Experiment

Measure:

Task A
↓
Task B
↓
Task C


and track:

TS
CGR
IG


over time.

One-Sentence Contribution

We introduce Capability Growth Metrics, a framework for quantifying how task experience translates into future problem-solving capability.

Final Research Story

Now everything compresses beautifully.

Contribution 1
Invariant Discovery Theory
How abstractions are discovered

Contribution 2
Skill Creation Trigger Theory
When new skills should be created

Contribution 3
Capability Growth Metrics
How intelligence growth should be measured

The Complete Research Narrative

This is the story I would tell in the paper:

Experience
↓
Invariant Discovery
(IDT)

↓

Skill Creation
(SCT)

↓

Capability Growth
(CGM)

↓

Future Tasks Easier

Final Compression Test

If a reviewer asks:

"What are your contributions?"

The answer should fit in 30 seconds:

Invariant Discovery Theory (IDT): a framework for extracting transferable abstractions from reasoning experiences.
Skill Creation Trigger Theory (SCT): a principled mechanism for deciding when new reusable skills should be created.
Capability Growth Metrics (CGM): a new way to measure intelligence growth through transfer and future task improvement.

That's focused, defensible, and much stronger than presenting AAA as a giant AGI architecture. It also aligns directly with the ARC emphasis on skill acquisition, transfer, and generalization rather than isolated task solving.