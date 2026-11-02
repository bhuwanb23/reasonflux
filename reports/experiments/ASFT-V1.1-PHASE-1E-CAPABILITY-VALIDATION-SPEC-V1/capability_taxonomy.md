# Phase 1E.3 — Capability Taxonomy

All categories are defined by external behavior. Internal `cap-cross-domain` object labels, C_t, CGR, IG, and portfolio membership do not determine category assignment.

| Type | Behavioral construct | Independent measurement |
|---|---|---|
| C1 Single-Skill Capability | One learned operation/rule supports a stable competence. | Novel-instance success for one skill across ≥2 held-out surface/template partitions; retention and utility gates in `capability_definition.md`. |
| C2 Multi-Skill Capability | Two or more distinct learned skills jointly enable a task beyond any one skill alone. | Held-out tasks requiring the joint skill set; compare to best single-skill arm and no-learning baseline under matched budgets. |
| C3 Transfer Capability | Competence carries to a disjoint task family not used to form the skill. | Cross-family task success and paired utility on unseen families; no exact memory key or demonstrations from test family. |
| C4 Compositional Capability | Previously validated components solve a new ordering/combination. | Success on held-out compositions; compare with best single component and shuffled/wrong composition controls. |
| C5 Adaptive Capability | System improves after a bounded amount of new evidence under changed conditions. | Pre/post adaptation performance on unseen tasks after exactly the same demonstration budget; report learning curve and retained gain. |
| C6 Cross-Domain Capability | One behavioral principle functions across distinct domains with separate surface/task generators. | Successful transfer on at least two disjoint domains, each meeting the independent family-level capability gate. |

## Anti-collapse rule

An object may instantiate more than one behavioral subtype only when each test's external criterion is separately passed. A single aggregate score cannot automatically label C1–C6. Report each subtype with its task set, denominator, uncertainty, cost, and baseline comparison. If the relevant test is absent or too small, mark that subtype unavailable.