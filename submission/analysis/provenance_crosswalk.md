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

The portable claim therefore has two parts: the base graph can be transformed
to common provenance objects, and Servo's additional target, reliability,
authority, epistemic-route, and closure fields remain explicit rather than being
flattened into generic annotations. This document does not claim formal PROV or
RO-Crate conformance; that would require an executable serializer and the
relevant conformance tests.

Primary specifications:

- W3C PROV-DM: <https://www.w3.org/TR/prov-dm/>
- Workflow Run RO-Crate: <https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/>
