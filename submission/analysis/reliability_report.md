# SERVO Cross-System Coding: Reliability and Counterexample Report

This report records the inter-coder reliability and the counterexample search
behind the cross-system coding and the framing of the V-completeness claim.
All numbers are reproduced deterministically by `analysis/multicoder/compute_fleiss.py`
over `codings.csv` and were additionally cross-checked by an independent
re-implementation (identical results).

## 1. Inter-coder reliability (multi-vendor blind coding, N = 14)

The cross-system coding was operationalized with the rubric in
`coding_protocol.md` and performed independently by **three model-pinned, blind
LLM coders from different vendors**, run headless with no access to one another's
labels, to the author's labels, or to the manuscript:

| coder | vendor | model (pinned) |
|-------|--------|----------------|
| claude | Anthropic | `claude-opus-4-8` (`--model`) |
| codex | OpenAI | `gpt-5.5` (`-m`) |
| agy | Google (Antigravity) | Gemini 3.1 Pro (High), set in `~/.gemini/antigravity-cli/settings.json` |

Coverage: 14 systems x 3 coders = 42 codings; `codex` failed on one system
(NovelSeek), so 13 systems have all three coders and one is two-coder
(claude+agy). For `agy` the model is pinned via the settings file.
The pipeline (`run_coders.py`, `compute_fleiss.py`) is re-runnable and
deterministic.

### Fleiss' kappa (the 13 systems coded by all three vendors)

| field          | raw agreement | Fleiss kappa |
|----------------|---------------|--------------|
| Vsemantic      | 1.00          | 1.00         |
| Vcalibrated    | 0.90          | 0.79         |
| loop_status    | 0.85          | 0.74         |
| Vsyntax        | 0.90          | 0.69         |
| Vhuman         | 0.79          | 0.59         |
| Vempirical     | 0.90          | 0.54         |
| Vcompleteness  | 0.69          | 0.39         |
| **mean**       | --            | **0.68**     |

Pairwise Cohen's kappa is consistent and shows no outlier vendor (e.g.,
Vcalibrated: agy-claude 0.71, agy-codex 1.00, claude-codex 0.70; loop_status:
0.75 / 0.75 / 0.74). Mean pairwise difference on the continuous H is 0.10.

### How to read these numbers

- **Reliability is substantial-to-perfect on most constructs at N = 14 across
  three independent vendors.** Semantic-validation presence is coded identically
  (kappa = 1.0), the decisive calibration construct is substantial (kappa = 0.79;
  raw 0.90), and loop status is substantial (kappa = 0.74). Because the three
  coders are different model families (Anthropic / OpenAI / Google), this reflects
  the rubric and source descriptions rather than one model agreeing with itself.
  It is an automated multi-rater transparency measure, not a claim of human-level
  inter-rater reliability.
- **The aggregate `V_completeness` ordinal is the single noisy construct**
  (kappa = 0.39). This is expected: as `coding_protocol.md` states, it is a
  holistic ordinal judgment (whether V_human counts toward the layer total;
  whether a biased layer is discounted), not a mechanical function of the binary
  indicators. We therefore rest the claim on calibration, not on this ordinal.
- **The author disagrees with the LLM coders precisely on V_completeness.**
  Against the author's (Coder A) labels on the overlapping systems, Cohen's kappa
  is high or perfect for loop_status (1.0), Vsemantic (1.0), and Vcalibrated
  (0.62-0.67), but *negative* for V_completeness (-0.25 to -0.43). The construct
  on which independent coders most disagree is exactly the holistic ordinal, and
  the construct they agree on is the calibration sub-construct the paper rests on.

## 2. Counterexample search

The protocol commits to actively seeking systems that would refute the claim,
in two directions. Three independent searches were run.

### (a) V-incomplete yet loop-closed (would refute necessity)

**Finding: no clean counterexample on the strong reading; one structural
near-miss.** The strongest candidate is **AI Scientist v1 (2024)**: it runs a
genuinely closed generate -> execute -> validate -> regenerate loop on an
*admittedly biased, uncalibrated* validator (LLM self-score + LLM reviewer at
~0.65 balanced accuracy). This refutes V-completeness as necessary for *loop
closure in the structural sense* (feedback does flow back into ideation). It
does **not** refute the claim on the substantive reading: the biased validator
yields unreliable, hallucination-prone output, so the loop closes without
reliably tracking truth. Every other V-incomplete system in the 2009-2026
corpus either (i) is rescued by a human at the final gate (Coscientist, Agent
Laboratory, DeepScientist) or (ii) closes only by switching to a near-oracle
validator (formal kernel, numeric evaluator, or wet-lab measurement: Robot
Scientist, FunSearch/AlphaEvolve, DeepSeek-Prover).

**Consequence for the paper.** This is the empirical basis for stating the
claim as an *association/correlate* ("V-completeness is the primary correlate of
closed-loop feasibility"), not as a deterministic law. The near-miss is reported
explicitly rather than suppressed.

### (b) V-complete yet loop-open for V-independent reasons (would refute sufficiency)

**Finding: no counterexample found.** Across systems with a genuinely
calibrated empirical validator across layers (Robot Scientist/Adam, A-Lab, the
mobile robotic chemist, closed-loop battery optimization), the loop *closes*
within scope. The only "openness" observed is a scope/economic choice
(fixed candidate list; human-in-the-loop for cost/safety/liability), not a
system property documented alongside a completeness claim. The category
"V-complete but open" is near-empty in the published record, which is itself
evidence for the direction of the association.

### (c) G/pi-driven closure with unimproved V (would weaken the V-centric framing)

**Finding: confirms rather than weakens.** In every closed-loop system that
gained capability from a stronger generator (G) or policy (pi) -- DeepScientist,
ERA, FunSearch/AlphaEvolve, DeepSeek-Prover -- the gain *exploited an
already-complete validator* (benchmark leaderboard, numeric oracle, or formal
kernel). The cleanest framing the evidence supports: **V-completeness gates
whether a closed loop is possible at all; G and pi gate how productive that loop
is once V is complete.** The one pure-G advance with no V improvement (OpenAI
unit-distance disproof) is *not* closed-loop -- it is single-shot, certified
post hoc by human mathematicians.

## 3. Net effect on the manuscript

1. The cross-system coding is operationalized (rubric), independently
   multi-coded by three model-pinned blind vendors over 14 systems, and released
   as machine-readable supplementary material with per-cell source quotes and a
   validator/regeneration script.
2. The central claim is stated as an association whose decisive sub-construct
   (calibration) shows substantial cross-vendor agreement (Fleiss kappa = 0.79),
   while the noisier aggregate ordinal (V-completeness, kappa = 0.39) is reported
   honestly -- including that independent coders disagree with the author on
   exactly that ordinal.
3. The one structural counterexample (AI Scientist v1) is reported in the
   limitations; the published per-system labels (`analysis/systems.csv`,
   author/Coder A) remain the conservative reference, with the multi-vendor
   matrix (`analysis/multicoder/codings.csv`) as the reliability evidence.
