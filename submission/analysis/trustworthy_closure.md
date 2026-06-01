# Mechanical vs. Trustworthy Closure: a descriptive, external-signal check

This file addresses the reviewer concern that the central claim risks circularity:
if "trustworthy closed-loop discovery" is judged by the same validator fields used as
predictors, the validator-completeness/trustworthiness link cannot be tested, only
restated. We therefore separate two outcomes and code the second one independently:

- **Mechanical closure** — does the system close a generate -> execute -> validate ->
  regenerate loop at all? Read from `A_loop_status` in `systems.csv`
  (`closed-comp` / `closed-wetlab` = closed).
- **Trustworthy closure** — when externally scrutinized, were the system's closed-loop
  outputs actually reliable? Coded in `trustworthy_closure.csv` from signals
  **external to the system's own validator** (independent replication, post-hoc human
  audit, documented hallucination, real human peer review), with a source per system.

The predictor (`A_Vcalibrated`, from `systems.csv`) and the outcome
(`trustworthy_closure`, from `trustworthy_closure.csv`) thus come from different
sheets and different evidence, which is what breaks the circularity.

## External-signal coding (six core systems)

| system | mechanical loop | `Vcalibrated` | external signal (source) | trustworthy closure |
|--------|-----------------|---------------|--------------------------|---------------------|
| Robot Scientist / Adam | closed-wetlab | 1 | yeast functional-genomics hypotheses experimentally confirmed and published (King et al. 2009, *Science*; Sparkes et al. 2010) | **yes** |
| AI Scientist (2024) | closed-comp | 0 | hallucinated results (e.g. ablation tables); authors advise not taking generated content at face value (Lu et al. 2024) | **no** |
| AI Scientist (Nature 2026) | closed-comp | 1 | outputs passed human peer review (ICLR workshop track only---a weak social signal, not independent replication); published in *Nature* (Lu et al. 2026) | **weak** |
| NovelSeek | closed-comp | 1 | reports closed-loop benchmark gains across twelve tasks; no independent third-party replication/audit located (Zhang et al. 2025) | **unknown** |
| Coscientist | partial-task | 1 | real chemistry executed, but the discovery loop is not closed (Boiko et al. 2023) | n/a (loop open) |
| Agent Laboratory | partial-task | 0 | automated reviewer over-estimates quality by +2.3 vs. human PhD students; human-directed (Schmidgall et al. 2025) | **no** |

**Evidence grading.** Trustworthy closure is graded by external-evidence strength:
**yes** = independent replication / formal proof / audited benchmark; **weak** =
peer-review or venue acceptance only (a noisy social signal); **unknown** = none
located; **no** = documented unreliability. Calibration itself is refined into
`V_present` vs `V_gating` in `multicoder/rubric_calib.txt` and `reliability_report.md`
(\S2b); trustworthy closure tracks gating calibration, not mere validator presence.

## Descriptive contingency (reproduced by `association_descriptive.py`)

Over the four **mechanically closed** systems, crossing validator calibration with the
externally-coded outcome (counts only):

```
Vcal=0 x trustworthy=no       : 1  (AI Scientist (2024))
Vcal=1 x trustworthy=unknown  : 1  (NovelSeek)
Vcal=1 x trustworthy=weak     : 1  (AI Scientist (Nature 2026))
Vcal=1 x trustworthy=yes      : 1  (Robot Scientist)
```

## How to read this (and how not to)

- **Direction-consistent, not a test.** The single mechanically-closed system without a
  calibrated validator (AI Scientist v1) is exactly the one external sources judge
  untrustworthy; the calibrated closed systems are trustworthy (2) or unverified (1).
  No cell contradicts the calibration reading (no `Vcal=1 & untrustworthy`, no
  `Vcal=0 & trustworthy`).
- **Mechanical closure does not require completeness.** AI Scientist v1 and NovelSeek
  close a computational loop at low `Vcompleteness` (=1); this is why the manuscript
  states the claim about *trustworthy* closure, not mechanical closure, and rests it
  on the calibration sub-construct rather than the holistic ordinal.
- **Far too small for inference.** With six core systems (four closed), no confidence
  interval or p-value is meaningful; we deliberately report none. This is a
  transparency check on the direction of the association, not a hypothesis test, and
  `NovelSeek = unknown` is reported rather than imputed.
- The manuscript accordingly presents the validator/trustworthiness relationship as an
  **organizing hypothesis**, not an established causal determinant.

## Regeneration

`python3 association_descriptive.py` re-joins `systems.csv` (validator labels) with
`trustworthy_closure.csv` (external outcome) and reprints the per-system table and the
contingency above.
