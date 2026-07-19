# szymanski2026correction — FULL-TEXT blind digest (READ)

**Source:** Author Correction, "An autonomous laboratory for the accelerated synthesis of inorganic
materials," Nature 650(8100):E1, published online 19 Jan 2026. DOI 10.1038/s41586-025-09992-y
(PMC12872444). Corrects Nature 624:86 (DOI 10.1038/s41586-023-06734-w, 29 Nov 2023).
**Full text obtained:** europepmc fullTextXML → text; archived at
`ai_scientist/2_Domain_Applications/Materials/Szymanski 2026 - A-Lab Author Correction (Nature, fulltext).txt`.
Read in full (blind agent v-corrreader) + orchestrator Tier-2 verbatim re-check.

## (a) What the correction changes and why
Two post-publication concern clusters:
1. **Novelty claim walked back.** Verbatim: "We acknowledge that the original claims of material
   novelty were subject to misinterpretation---their intention was to indicate that the materials
   were new to the prediction platform, not necessarily new to science."
2. **Diffraction re-analysis.** "concerns were raised about the unambiguous identification of the
   compound structures using diffraction." Authors manually re-analyzed (peer-reviewed post-pub).

## (b) FACTS TABLE (verbatim)
| # | Fact | Value | Quote |
|---|------|-------|-------|
| F1 | reported successes confirmed correct | **36 of 40** | "the prediction platform came to the correct conclusion in 36 of its 40 reported successes, with 4 compounds being inconclusive" |
| F2 | inconclusive | **4** | "with 4 compounds being inconclusive" |
| F3 | successful-count update | exclude the 4 inconclusive | "updated to exclude four target materials whose presence is inconclusive from XRD alone" |
| F4 | compound removed (training-data leakage) | **1** (Zn2Cr3FeO8) | "removed one compound from the discussion (Zn2Cr3FeO8) that was mistakenly included in the training data" |
| F5 | figure updated | Fig. 2 | "reflected in Fig. 2" |

## (c) What the correction does NOT say
- **"57" appears NOWHERE.** No "X of Y targeted compounds" headline. Its only ratio is **36 of 40
  reported successes**. It never states a target denominator (no 57, 58, or 41 in the correction body).

## Adjudication — C131
- **VERDICT: MISCHARACTERIZATION (with INACCURATE-NUM component).** The manuscript's "36 of 57
  targeted compounds~\citep{szymanski2026correction}" is not supported by the correction: it mixes
  the correction's "36 of 40 reported successes" numerator with an inferred 57-targets denominator
  (58 original - 1 removed) the correction never states, reframing "confirmed-of-reported-successes"
  as "realized-of-targets." **Fix applied** (2026-07-19): EN L234 / KO L282 changed to "initially
  reporting 41 of 58 target compounds synthesized, revised after post-publication re-analysis to
  36 of 40 reported successes confirmed (4 inconclusive)"---original 41/58 cited to szymanski2023alab,
  revision cited to szymanski2026correction.

## Reverse findings
- **R (HIGH)** Novelty walk-back omitted: compounds re-scoped to "new to the prediction platform,
  not necessarily new to science." Material only if the manuscript leans on A-Lab as a *novel*-material
  exemplar (it does not---its point is the fixed escalation rule---so noted, not applied).
- **R (MED)** 4 inconclusive compounds---now included in the fixed text.
- **R (MED)** 1 compound removed for training-data leakage (Zn2Cr3FeO8).
- **R (LOW-MED)** trigger was doubt about structure identification via diffraction.
