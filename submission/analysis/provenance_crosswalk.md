# Provenance and workflow crosswalk

Servo reuses the object-and-relation layer of established provenance models
where possible. It is a scientific-diagnostic profile, not a replacement base
provenance ontology. The mapping is loss-aware because several Servo fields
carry scientific semantics that generic provenance vocabularies do not require.

| Servo construct | PROV-DM / Workflow Run RO-Crate analogue | Reused semantics | Servo-specific increment |
|---|---|---|---|
| Versioned artifact | PROV `Entity`; derivation/revision; RO-Crate input/output entity | Identity, generation, use, derivation, revision | Bounded artifact identity required by a predicate witness |
| Evaluation or execution event | PROV `Activity`; RO-Crate `CreateAction`/run | Occurrence with inputs, outputs, and time/order | Scientific target property, evaluator endpoint, reliability link, update semantics |
| Human or system actor | PROV `Agent` and association | Responsibility/association | Component-specific authority category rather than generic authorship |
| Producer and consumer route | Generation and Usage | Entity/activity direction | Typed epistemic, feedback-control, artifact-revision, and human-mediation roles |
| Workflow plan and run | Workflow Run RO-Crate workflow plan/run | Executable plan, run, code, inputs, outputs | Bounded case/version/configuration/task-regime identity |
| Closure witness | No direct base-vocabulary equivalent | Can be serialized as a connected provenance subgraph | Predicate-specific minimum path and evidential status |

This table is a construct-level correspondence, not evidence that the current
records can already be transformed losslessly into a conforming PROV or
Workflow Run RO-Crate package. Servo's additional target, reliability,
authority, epistemic-route, and closure fields identify what a future profile
would need to preserve rather than flatten into generic annotations. Executable
serialization, formal conformance, and portability remain unestablished until a
serializer and the relevant conformance and round-trip tests are supplied.

Primary specifications:

- W3C PROV-DM: <https://www.w3.org/TR/prov-dm/>
- Workflow Run RO-Crate: <https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/>
