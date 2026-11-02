# Phase 1D.8 — Leakage-Control Protocol

## Threat model

The principal risk is that a memory arm receives test-task or answer information while the abstraction arm is judged on generalization—or that hidden answers leak into candidate generation, retrieval keys, pattern labels, or Oracle outputs. The protocol therefore audits storage, retrieval, and exposure separately.

## 1. Storage audit

Every stored object must include immutable metadata: `object_id`, representation type, canonical payload hash, serialized bytes, source split, source task/template ID, creation timestamp, allowed family scope, and label-access class. Before confirmation, verify:

- No object sourced from confirmatory/replication future tasks, labels, solver outputs, or answers is in any policy store.
- B1a–c and B2 use only the shared allowed training exposure, encoded according to their declared representation.
- B3's total bytes/items include both memory and abstract objects; no hidden secondary cache.
- Indexes, embeddings, summaries, failed traces, and generated candidate solutions are included in storage accounting.
- The only exact task-key overlap is the predeclared, allowlisted Family A train/test repeat pair. Its source answer is from the training demonstration, not from the sealed test label store. This planned exposure is part of the Family A treatment and must be reported separately.

## 2. Retrieval audit

Log each query and each inspected object: query ID, arm, object ID, similarity/key score, selection order, retrieved/rejected status, rule/fragment applied, retrieval budget used, and result. Verify retrieval is limited to permitted stores and ≤4 inspections per task. Any B–F retrieval of a future split item or answer invalidates the affected panel. Random retrieval must use the declared seed and the same candidate pool/cap.

## 3. Exposure and evaluator audit

- Policy APIs receive task inputs and allowed training-derived representations only; no `gold_answer`, `future_success`, hidden rule label, or test utility field.
- Keep gold outputs in a separate evaluator store; compute policy outputs first, hash/lock them, then score.
- Family A's allowed training precedent is checked against the preregistered pair list; no other task may use it as a key or answer cache.
- Oracle B6 is computed only after all ordinary outputs, resource logs, and run manifests are locked.
- Run exact-hash and near-duplicate audits across development/confirmatory/replication; retain collisions and adjudication records.

## 4. Failure response

A confirmed leakage or budget breach is not repaired by deleting only unfavorable rows. Preserve logs and hashes, mark the affected endpoint/panel invalid or unavailable under the frozen rule, and disclose the incident. Any protocol amendment must occur before a new untouched confirmatory set is opened.

## Automated gates

Storage, retrieval, exposure, and Oracle-access checks must run on every release. Phase 1D's current contract checks validate schemas and declared exceptions only; production access control, task-store separation, and exhaustive leakage audits remain unimplemented.