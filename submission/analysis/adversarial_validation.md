# Three-round adversarial validation record

Date: 2026-07-22. Target: Servo Schema 4 and package release 4.0.0.

This is release evidence, not proof that every source interpretation is uniquely
correct. The rounds attack different failure surfaces so one successful gate
cannot mask another.

## Round 1: formal-contract and mutation resistance

- The Schema 4 regression suite passed 103 tests; the one temporarily excluded
  test concerned the not-yet-updated external publication pointer.
- Negative mutations reject reused event identity, a revision without a
  distinct `W_A` production occurrence, cross-lineage successors, malformed
  occurrence identifiers, and predicate/status implication violations.
- A positive counterexample confirms that two distinct artifact lineages may
  independently use version 1.
- The canonical tables passed schema, graph, component, relation, evidence, and
  closure validation after C01 was conservatively returned to `unknown` and C05
  was represented by distinct later execution and evidence records.

## Round 2: manuscript, citation, and cross-surface consistency

- The whole-state citation and manuscript gate passed: 62 papers, 131 atomic
  claims, 14 frozen core reports, seven audit tests, three XeLaTeX builds, public
  release readiness, and repository/PDF synchronization.
- The reader-facing English manuscript contains no R-number development log or
  numbered internal schema label. The chronological record is repository-only.
- The generated English and private Korean closure tables both encode C01
  experimental adaptation as `unknown`; BioPlanner is consistently described as
  an evaluation benchmark for LLM-generated protocol pseudocode.
- PDF text scans found no internal R-number, obsolete schema, stale release URL,
  or obsolete BioPlanner-generator claim. Visual inspection covered the title,
  case/closure tables, and final appendix page.

## Round 3: clean-package reproducibility

- The finalized package was zipped, unpacked into a fresh temporary directory,
  and validated with isolated uv cache and environment directories.
- Both `public-regeneration` and `release-ready` returned `SERVO2_OK` from the
  unpacked copy.
- The prepublication clean-copy ZIP SHA-256 was
  `997a6bfdffa1add7ac60914a979b17af4e33662c58cd21c8853433fa2c2a508b`;
  final publication hashes are recorded by the release manifest and external
  publication pointer after the published attestation is generated.

No unresolved high- or critical-severity finding remained at the end of these
three rounds. Publication-pointer synchronization remains a final transaction:
it must occur only after the release asset is uploaded and independently
downloaded.
