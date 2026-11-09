# BL1-P0 — Bounded Prior-Art Review

**Review date:** 2026-11-05  
**Status:** planning-only review; no implementation, data generation, or experiment.  
**Question:** Is the chain *counterexamples → better applicability-boundary precision → maintained useful coverage* sufficiently uncovered to justify BL1?

## Decision summary

**No defensible novelty remains for the proposed BL1 claim as currently framed.** The broad mechanism—use negative/failure evidence to revise a learned region in which a skill or option is eligible—is established in counterexample-guided refinement, robot-skill precondition learning, and, most directly, hierarchical reinforcement learning's learned option initiation sets. Prior work also explicitly treats the precision/usefulness tradeoff: initiation sets should reflect where an option succeeds without collapsing so far that a useful option is excluded.

A narrowly controlled, matched comparison of *counterexample labels versus no counterexample labels* on a frozen skill and held-out contexts may be an unreported experimental contrast in this project's proposed form. That difference is not enough, on the bounded review, to make the existing one-chain claim a distinct research contribution: the underlying learning target, failure-derived negative examples, classifier/boundary update, and usefulness/coverage concern are already covered. Establishing only a local effect on a small synthetic fixture would be a replication or application, not a meaningful distinct result under the current charter.

**P0 recommendation: terminate BL1 before P1.** This is a bounded review, not a claim of exhaustive literature coverage. It does not affect or reinterpret any prior T2T/S3 result.

## Coverage by prior-art family

| Prior-art family | What is already covered | Relevance to BL1 |
|---|---|---|
| Counterexample-guided synthesis and abstraction refinement | CEGIS iteratively refines a candidate using counterexamples; CEGAR refines an abstraction after counterexample analysis. | The general feedback loop is not novel. These works do not by themselves establish an option-applicability contribution, but they remove novelty from the mechanism stated at that level. |
| Learned robot skill preconditions / option initiation sets | A skill's precondition or an option's initiation set represents where it can be started. Existing methods learn these regions using positive successful and negative failed execution examples, often with a classifier. | Direct overlap with boundary learning from failed/inapplicable executions. |
| Counterexample-guided environment bounds | Failed verification returns counterexamples used to refine a learned conservative behavior bound. | Direct precedent for the broader sequence of counterexample → boundary/bound refinement, although the target is an environment model rather than skill applicability. |
| Modern initiation-set learning | Initiation-set work explicitly addresses how to estimate where an option succeeds, classifier labels from successful/failed trajectories, adaptation to changing policies, pessimistic shrinking, and quality/usefulness. | Strongest overlap: it covers both refining applicability boundaries with negative/failure evidence and preserving an initiation region useful to the agent. |

## Closest and foundational sources

1. **Bagaria et al., “Effectively Learning Initiation Sets in Hierarchical Reinforcement Learning,” NeurIPS 2023.** The paper describes initiation sets as states where an option is likely to succeed; presents the basic classifier framing using successful trajectories as positive examples and failed trajectories as negative examples; and proposes methods addressing non-stationarity and pessimistic shrinkage. It evaluates initiation-set accuracy/quality in MiniGrid and Montezuma's Revenge, grasp selection in Robosuite, and downstream option use in MuJoCo. Its explicit concern that a learned set can shrink and become too small to remain useful is particularly close to BL1's “maintained useful coverage” condition. This is the decisive closest prior art. [Paper](https://proceedings.neurips.cc/paper_files/paper/2023/file/e8da56eb93676e8f60ed2b696e44e7dc-Paper-Conference.pdf)
2. **Konidaris et al., “Robot Learning from Demonstration by Constructing Skill Trees,” IJRR (2012).** Describes learning initiation sets with a classifier from trial-and-error examples, using successful executions as positive and failed executions as negative examples; discusses incremental updates from newly received negative examples. [Paper](https://all.cs.umass.edu/pubs/2012/cst_ijrr_12.pdf)
3. **Sutton, Precup & Singh, “Between MDPs and semi-MDPs: A Framework for Temporal Abstraction in Reinforcement Learning,” AIJ (1999).** Establishes the options framework, including the initiation set as a component of an option. [Paper](https://people.cs.umass.edu/~barto/courses/cs687/Sutton-Precup-Singh-AIJ99.pdf)
4. **“Robustly Learning Composable Options in Deep Reinforcement Learning,” IJCAI (2021).** Uses initiation-region classifiers and failure-driven shrinkage/refinement in composable options. [Paper](https://www.ijcai.org/proceedings/2021/0298.pdf)
5. **Chen et al., “Counter-Example Guided Learning of Bounds on Environment Behavior,” CoRL (2019).** Learns a conservative behavior bound and uses verification counterexamples to refine it. The target differs from BL1, but the counterexample-guided boundary-refinement pattern is explicit. [Record and abstract](https://mlanthology.org/corl/2019/chen2019corl-counterexample/)
6. **Solar-Lezama, “The Sketching Approach to Program Synthesis” (2009), and Clarke et al., counterexample-guided abstraction refinement (CEGAR).** Foundational precedents for iterative counterexample-guided candidate/abstraction refinement. [CEGIS paper](https://people.csail.mit.edu/asolar/papers/Solar-Lezama09.pdf); [CEGAR paper](https://web.stanford.edu/class/cs357/cegar.pdf)
7. **Kroemer, Niekum & Konidaris, “A Review of Robot Learning for Manipulation,” JMLR 22 (2021).** Situates learning robot skills and their pre-/postconditions in a mature literature; useful context, not the decisive evidence by itself. [Review](https://www.jmlr.org/papers/volume22/19-804/19-804.pdf)

## What might still be different—and why it does not rescue this BL1

The proposed contrast isolates a specific intervention: keep the candidate skill, initial boundary, evidence access, resources, and held-out suite fixed, while allowing counterexample labels to update the boundary in one arm only. The sources above do not necessarily make that exact protocol or the precise paired metric a named standalone contribution. However:

- it tests an already established learning operation on an already established target (skill applicability/initiation set);
- the closest work already learns initiation sets from success/failure labels and directly studies their quality and risk of losing useful coverage;
- choosing precision, recall/coverage, and false activation as a particular reporting bundle is not, by itself, a substantive algorithmic or conceptual distinction;
- a short synthetic test could demonstrate local behavior, but cannot on its own distinguish a new method from an instance-level replication or support broad transfer claims.

To reopen the idea would require a separately defined contribution that is not merely “failure examples improve an applicability classifier,” plus a literature review focused on that contribution. That would be a new owner decision, not BL1-P1, and is outside this P0.

## Evidence limits and integrity boundary

- This was a bounded source review, not a systematic review or exhaustive search; no absence-of-prior-art claim is made.
- The review relies most heavily on accessible primary paper text/abstracts and bibliographic records listed above. A recent GitHub issue surfaced in search but is not treated as peer-reviewed or reliable prior-art evidence and does not affect the decision.
- The S2 observation (false activations 2/4→0/4; applicable-context coverage 2/2) remains a toy-fixture observation only; it is not validation or novelty evidence.
- S3 is not rerun, modified, reused as held-out evaluation data, or reinterpreted. Its frozen finite synthetic predictive estimand remains N-FAIL.
- No implementation, context generation, model fitting, or experiment has occurred or is authorized by this review.

## P0 disposition

The proposed BL1 claim chain is substantially covered by prior art, with direct overlap in option initiation-set learning and its precision/usefulness tradeoff. Under the owner's stop rule, terminate BL1 at P0. Do not create BL1-P1.
