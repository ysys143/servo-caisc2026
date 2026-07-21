# Frozen recommendation-quality rubric

This rubric is frozen before `r24-run-003`. It evaluates paired recommendation sets without revealing whether a set came from the baseline or SERVO condition. It does not use a human coder or claim to measure human usefulness.

## Unit and blinding

The unit is one anonymous source record, one originating vendor, and its paired baseline/SERVO outputs. The two non-originating vendors judge the pair independently. A fixed-seed permutation assigns the labels A and B; a separate fixed-seed draw determines which judge receives the first orientation, and the other receives its reverse. Judges see only the source packet, each output's diagnostics and cited evidence, and its recommendations. They do not see condition names, the SERVO manual, probe keys, manuscript conclusions, the originating vendor, or another judge's response. A/B relabelling cannot conceal stylistic or structural cues, so the design guarantees label blinding but not condition indistinguishability.

## Dimension scores

Each dimension receives 0, 1, or 2. A judge must cite the recommendation ID and source evidence ID supporting each score.

1. **Evidence support**
   - 0: a material recommendation relies on a claim absent from or contradicted by the packet.
   - 1: recommendations are mostly grounded, but at least one material link is incomplete or indirect.
   - 2: every material recommendation is supported by the cited packet evidence and introduces no unsupported system fact.
2. **Diagnosis--remedy fit**
   - 0: the proposed action does not address the linked diagnosis or would leave the stated failure unchanged.
   - 1: the action partially addresses the diagnosis but misses an important mechanism or boundary.
   - 2: the action directly addresses the diagnosed mechanism at the reported system boundary.
3. **Actionability**
   - 0: the recommendation is aspirational or cannot be implemented as stated.
   - 1: an implementable direction is present but actor, component, or operation is underspecified.
   - 2: the affected component, proposed change, and operational decision are explicit enough to implement or test.
4. **Success-check verifiability**
   - 0: no observable test or falsifiable outcome is supplied.
   - 1: an observable is named, but the comparator, threshold, or required evidence is materially incomplete.
   - 2: observable, comparator or threshold, and required evidence jointly define a reproducible check.
5. **Scope proportionality**
   - 0: the recommendation exceeds the evidence, treats non-reporting as failure, or claims a property outside the diagnosed target.
   - 1: the direction is defensible but its scope or certainty is broader than the packet warrants.
   - 2: scope and certainty match the evidence, including abstention where the source is ambiguous.
6. **Set-level coverage and non-redundancy**
   - 0: the set misses the main evidenced problem or is dominated by duplicates.
   - 1: it covers the main problem but has a material omission or redundant actions.
   - 2: it covers distinct material problems with non-duplicative actions and no unsupported padding.

## Comparative decision

After scoring both sets, choose `A`, `B`, or `tie`. Prefer a set only when its evidence-grounded design advice is materially better under the six dimensions; recommendation count alone is never a reason to prefer it. The equal-weight mean is a descriptive summary, not a validity threshold. Judges may return `not_judgable` only when the packet or one output is malformed or missing.

## Reporting boundary

Report dimension-level scores, preference and tie rates, inter-judge agreement, disagreements, and judge-vendor sensitivity. These automated judgments do not establish correctness, human usefulness, construct validity, or actual improvement after implementation.
