# Prospective holdout protocol

## Purpose

The holdout evaluates whether the frozen Servo contract can represent a new
system without schema repair. It is summative evidence about application, not a
population estimate or a test of scientific outcome quality.

## Freeze before coding

Record the following before inspecting a candidate for Servo coding:

1. candidate identity and evidence that it was not used to develop the current
   predicate contract;
2. version, configuration, task regime, and case boundary;
3. primary-source files, SHA-256 hashes, and allowed source locations;
4. target properties and endpoints;
5. the exact schema, predicate-contract, validator, and commit hashes.

## Required instantiation

Produce complete case, endpoint, artifact, event, edge, reliability, witness,
status, evidence-ledger, and selection records in a separate holdout directory.
Run the same public-regeneration and source-byte audits used for core cases.
Report unmatched concepts, `unknown` statuses, validator failures, coding time,
and any lossy provenance mappings.

## Contamination rule

No schema, predicate, enum, validator, or decision-rule change is allowed after
coding begins. If any such change is necessary, classify the candidate as
formative, record the failure, freeze the revised contract, and select a new
untouched holdout. A repaired case cannot be reported as summative evidence.

## Current state

No case currently satisfies this protocol. The six complete cases informed
framework development, and the seven domain anchors are deliberately partial.
Until a prospective instantiation passes, the manuscript must describe
portability as a design objective supported by mappings, not as demonstrated
out-of-sample applicability.
