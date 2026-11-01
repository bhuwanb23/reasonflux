# 14I-C — External Validity

## Question

Can findings generalize beyond the tasks, operations, simulator, and split actually evaluated?

### Synthetic dependence — critical

The strongest positive findings come from controlled synthetic tasks with a known, narrow operation vocabulary. Phase 13C's skill objects are reflection/rotation; 13B's labels are generator-aligned. These results support synthetic-scope statements, not broad learning or general reasoning.

### Limited operation and skill diversity — high

A 91/91 cross-family result is limited to attempted cases with the reflection/rotation skill pool. It is not transfer across independent semantic domains. Counting/grouping or other absent skills cannot be treated as tested failures or successes.

### ARC adapter and coverage — critical

Phase 13G's full ten-program exact-demo fits are 3/600 discovery, 5/200 transfer, 2/200 holdout. Only three discovery traces successfully fit; no invariant, skill, or capability forms. The fixed DSL omits important ARC operations. Scored-arm accuracy and learned-skill transfer denominators are distinct from these coverage counts.

The frozen config declares three candidates per task, but `discover()` defaults to ten. Thus discovery fit yield reflects a broader scan; only the reflection fit among the three saved discovery fits is within the first three fixed candidates. This is an additional implementation limitation—not evidence for how a richer, protocol-conformant ARC system would perform.

### ARC split and exposure — high

Phase 13G draws disjoint splits from public training tasks, not official evaluation. Attempt 01 generated predictions in memory before report failure and attempt 02 reused the same holdout. The saved estimate is not pristine independent confirmation. An upstream archive contained evaluation blobs; only filenames were listed, no evaluation JSON parsed or scored, and the archive was deleted.

## Verdict

**Very high risk for general ASFT or ARC claims.** The safe conclusion is narrow synthetic behavior plus failure of the tested bounded ARC adapter. ARC cannot alone falsify or validate the broader theory.
