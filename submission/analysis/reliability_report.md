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
deterministic. The coders are blind to one another and to the author's labels,
but **not** to system identity (the systems are widely known and may be
memorized); this is stated as a limitation in the paper. Coder A (author) labels
in `../systems.csv` cover the core systems reported in Table 1, while this
multi-vendor reliability coding extends to all 14 Tier-1 systems (see
`multicoder/target_systems.md`).

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
kernel). The cleanest framing the evidence supports: **V-completeness gates whether a
closed loop can reliably *track truth* at all; G and pi gate how productive that
loop is once V is complete.** (The structural near-miss in (a) shows a loop can
close *mechanically* on an uncalibrated V; what V-completeness gates is
trustworthy closure, not the mere flow of feedback.) The one pure-G advance with no V improvement (OpenAI
unit-distance disproof) is *not* closed-loop -- it is single-shot, certified
post hoc by human mathematicians.

### Search summary (candidates and dispositions)

Each row consolidates a system already discussed in (a)-(c) above; the table is a
structured restatement of that search, not new evidence. "Direction" refers to
the refutation each candidate was tested against.

| candidate system | direction tested | counterexample? | disposition / why not | source basis |
|---|---|---|---|---|
| AI Scientist v1 (Sakana 2024) | (a) V-incomplete yet loop-closed | **partial -- structural near-miss** | closes generate->execute->validate->regenerate on a biased, uncalibrated V; refutes structural necessity but not *trustworthy* closure (output unreliable) | LLM self-score + LLM reviewer, balanced acc. ~0.65 (Lu et al. 2024) |
| Coscientist | (a) | no | V-incomplete; rescued by a human at the novelty/significance gate | Boiko et al. 2023 |
| Agent Laboratory | (a) | no | adds a V_s layer but uncalibrated (+2.3 over-estimation vs. PhD students); loop does not close without a human | Schmidgall et al. 2025 |
| DeepScientist | (a) / (c) | no | human at the final gate; capability gain exploits an already-complete benchmark V | catalog (target_systems.md) |
| Robot Scientist / Adam | (a) / (b) | no | V-complete via a calibrated wet-lab measurement; loop closes within scope | King/Sparkes et al. 2009-2010 |
| FunSearch / AlphaEvolve | (a) / (c) | no | closes via a near-oracle numeric evaluator; the G/pi gain rides an already-complete V | Romera-Paredes et al. 2023 |
| DeepSeek-Prover-V1.5 | (a) / (c) | no | closes via a formal-kernel oracle (calibrated V); not V-incomplete | Xin et al. 2024 |
| A-Lab / mobile robotic chemist / closed-loop battery opt. | (b) V-complete yet loop-open | no | loop *closes* within scope; the only openness is a scope/economic choice (fixed candidate list, cost/safety), not a V property | as surveyed (autonomous materials/chem labs) |
| ERA | (c) G/pi gain, V unchanged | no (confirms) | recombination gain exploits an already-complete validator | catalog (target_systems.md) |
| OpenAI unit-distance disproof | (c) pure-G, no V improvement | no | *not* closed-loop: single-shot, certified post hoc by human mathematicians | catalog (target_systems.md) |

**Net:** zero clean counterexamples on the trustworthy-closure reading; one
structural near-miss (AI Scientist v1), reported in the manuscript's Limitations.
The category "V-complete yet loop-open for V-independent reasons" is near-empty in
the published record, which is itself evidence for the direction of the association.

## 2b. Calibration: a construct-validity refinement

A later review found AI Scientist (Nature 2026) author-coded `Vcalibrated=1` while
all three blind coders coded `0`, calling the calibration label disputed. The cause
was construct conflation: the single `Vcalibrated` field mixed two questions. We
split it (`multicoder/rubric_calib.txt`):
- `V_present`: a calibrated validation layer EXISTS anywhere in the system.
- `V_gating`: the layer that DECIDES acceptance is itself calibrated.
- `novelty_gate`: what gates novelty/significance.

Blind re-coding of all 14 systems by two model-pinned vendors (claude-opus-4-8,
gpt-5.5; the `agy` CLI returned empty output in this headless run and was excluded;
`multicoder/run_calib.py`, `compute_calib.py`, `codings_calib.csv`):

| construct     | claude = codex | claude = author | character |
|---------------|----------------|-----------------|-----------|
| V_present     | 14/14          | 13/14           | near-universal (low discriminating power) |
| V_gating      | 13/14 (92%)    | 12/14           | the decisive, reproducible construct |
| novelty_gate  | 10/14          | 10/14           | noisier (5-way categorical) |

With two vendors Fleiss' kappa is undefined, so the counts above are RAW agreement;
the chance-adjusted Cohen's kappa is V_present 1.00, V_gating 0.86, novelty_gate 0.53
(`compute_calib.py`). **There is no human gold standard here, and "author" does not
mean a human reference.** Both the blind coders and the `author`/Coder-A labels were
produced with AI assistance (Claude, per the AI Involvement Checklist; the human
author directs and owns the labels but did not hand-code them). The blind `claude`
coder shares its model family with the author labels, so author-vs-`claude` agreement
is **not independent**; the meaningful signal is the cross-vendor `claude`-vs-`codex`
agreement (two different vendors), e.g. V_gating Cohen's kappa 0.86. These statistics
are a transparency measure, not human-level reliability; independent human
adjudication of the labels remains future work.

- **The dispute resolves.** For AI Scientist (Nature 2026) the author and both
  coders agree under the split: `V_present=1` (a calibrated empirical replication
  layer exists -- what the author label captured) and `V_gating=0` (acceptance is
  gated by a biased LLM reviewer / social peer review -- what the coders captured).
  The old disagreement was the conflation, not noise.
- **The decisive construct is reproducible.** Gating calibration agrees across
  vendors on 13/14 systems, more cleanly than the old holistic label.
- **No calibrated automated novelty gate exists** (`novelty_gate=calibrated_auto`
  on 1/28 codings, itself a coder error), empirically grounding the
  novelty-non-automatability open problem.

We therefore frame the survey as exposing failure modes in validator architecture
(mechanical closure without trustworthy gating; validation presence without decisive
calibration; external acceptance without independent replication), not as estimating
an association.

## 3. Net effect on the manuscript

1. The cross-system coding is operationalized (rubric), independently
   multi-coded by three model-pinned blind vendors over 14 systems, and released
   as machine-readable supplementary material with a representative source quote
   and resolvable citation per system, and a validator/regeneration script.
2. The central claim is stated as an association whose decisive sub-construct
   (calibration) shows substantial cross-vendor agreement (Fleiss kappa = 0.79),
   while the noisier aggregate ordinal (V-completeness, kappa = 0.39) is reported
   honestly -- including that independent coders disagree with the author on
   exactly that ordinal.
3. The one structural counterexample (AI Scientist v1) is reported in the
   limitations; the published per-system labels (`analysis/systems.csv`,
   author/Coder A) remain the conservative reference, with the multi-vendor
   matrix (`analysis/multicoder/codings.csv`) as the reliability evidence.

## What the validator scripts do and do NOT check (reviewer disclosure)

Two limitations of this package are stated plainly so reviewers do not over-read it:

1. **Formal integrity, not semantic entailment.** `build_servo_tables.py` and
   `build_domain_tables.py` enforce only that every row has a non-empty
   `source_quote` and a `citation_key` resolvable in `references.bib`; they reject
   uncited or unquoted rows. They do **not** verify that the quote semantically
   entails each coded field (e.g. that the quote actually supports `Vcalibrated=1`
   or `loop_status=closed-comp`), nor that the quote is verbatim and in-context.
   `systems.csv` carries **one representative quote per system**, not one quote per
   component, so per-component coding judgments (S, G, E, V, M, pi and the binary
   indicators) still require the reader to consult the cited primary source. The
   scripts make the table *reproducible*, not the coding *independently validated*.

2. **`trustworthy_closure` is only partly external to V.** The outcome signals used
   to code `trustworthy_closure` (independent replication, post-hoc audit,
   documented hallucination, real human peer review / publication) are intended to
   be external to each system's *automated* validator design, but two of them ---
   peer review and publication --- are themselves a form of human validation and
   therefore overlap the V_human layer that counts toward V-completeness. A system
   that includes V_human in its loop is mechanically more likely to have a
   peer-review/publication outcome available to code as "trustworthy." The check is
   thus direction-consistent but **not a clean external test**; combined with the
   six-system size and the author-curated candidate list behind the counterexample
   search, it is offered as a transparency artifact, not as independent confirmation
   of the V-completeness reading. The paper states this in its Limitations.
