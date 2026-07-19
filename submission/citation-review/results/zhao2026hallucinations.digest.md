# Digest: zhao2026hallucinations

**Title:** LLM hallucinations in the wild: Large-scale evidence from non-existent citations
**Authors:** Zhenyue Zhao, Yihe Wang (co-first, †), Toby Stuart, Mathijs De Vaan, Paul Ginsparg, Yian Yin
**Affiliations:** Cornell (Information Science), UCLA (Sociology), Tsinghua (CS), UC Berkeley (Haas School of Business)
**Length:** 16 pages. Reference accessed-dates run into 2026 (e.g., NYT dated Apr 21 2026); data cutoff late 2025 (analysis window Jan 2020–Aug 2025).

---

## Thesis / Problem

LLMs generate plausible-but-false information ("hallucination"), but the **real-world magnitude and consequences remain poorly understood** — prior work relied on controlled/simulated settings or small hand-checked samples. This paper uses **scientific citations as a uniquely verifiable object** (a cited reference either exists or it does not) to conduct a **population-scale audit of hallucinated ("non-existent") citations "in the wild."** Central claim: LLM hallucinations are "infiltrating knowledge production at scale," threatening the reliability and equity of science.

## Method — does it document a large-scale/ecosystem SURGE in fabricated / non-existent citations?

**YES, unambiguously.** The paper's core empirical finding is a **sharp, corpus-wide rise in non-existent references following widespread LLM adoption**, with the steepest growth beginning **mid-2024** (~18 months after ChatGPT's late-2022 release).

- **Scale of audit:** 111 million references across 2.5 million papers in **four corpora** — arXiv, bioRxiv, SSRN, PubMed Central (PMC).
- **Verification pipeline:** Extract references → parse structured fields → query locally-hosted Elasticsearch index built from **Semantic Scholar + OpenAlex** → string-similarity matching. Unmatched entries routed through GPT-4o-mini cleaning (to drop non-academic sources / fix parsing) → re-query → final **Google Scholar** third-party API lookup. Focuses on **one specific error type: references with non-existent titles.**
- **Identification design (key methodological move):** Does NOT classify individual references as hallucinated. Instead tracks the **rate of unmatched citations over time**, uses **pre-LLM (pre-2023) unmatched rate as baseline** for ordinary bibliographic/matching error, and interprets the **post-LLM excess of unmatched citations as the population-level signature of hallucination.** A regression framework estimates the excess.
- **Main evidence of surge:** Unmatched rate stable through late 2022 (baseline), then **increased sharply in 2023**, with steepest rise from mid-2024. Estimated hallucination rate as of Aug 2025 reaches 0.39% (arXiv) / 0.21% (bioRxiv) / **1.91% (SSRN)** / 0.27% (PMC). Extrapolated total: **146,932 hallucinated citations in 2025 alone** (explicitly framed as a **lower bound**). Growth continues through data cutoff "with no signs of plateauing."

The paper frames this as "the **first** large-scale, cross-disciplinary audit of LLM hallucinations in real-world knowledge work."

---

## FACTS TABLE (exhaustive)

### Headline / abstract figures

| Value | Location | Context |
|---|---|---|
| 111 million references | Abstract (p.1), l.31 | Total references audited |
| 2.5 million papers | Abstract, l.31 | Total papers audited across 4 corpora |
| 4 corpora: arXiv, bioRxiv, SSRN, PMC | Abstract, l.31–32 | Datasets |
| 146,932 hallucinated citations | Abstract l.33; also Discussion l.319 | "Conservative estimate" for 2025 alone |
| Sharp rise "following widespread LLM adoption" | Abstract l.32 | Core surge claim |
| 6.4 pp / 7.6% relative | Abstract l.253–254 | Over-crediting of male-named authors |

### Corpus sizes & citation counts

| Value | Location | Context |
|---|---|---|
| arXiv: 1,465,145 preprints | l.127–128 | Jan 2020–Aug 2025; math/physical/computational sciences |
| arXiv: 44,107,529 citations | l.130 | 60.9% LaTeX (source bib extraction); rest via GROBID from PDFs |
| bioRxiv: 261,928 preprints | l.130 | biological / life sciences |
| bioRxiv: 21,183,111 citation records | l.131–132 | XML from platform's in-house processing |
| SSRN: 421,698 preprints | l.133 | social sciences, law, humanities |
| SSRN: 26,815,043 citations | l.135 | metadata via Crossref (full text not public) |
| PMC: 374,807 manuscripts | l.139 | 10% random sample of recent papers, 2020–2025; peer-reviewed full-text |
| PMC: 19,245,787 references | l.139 | extracted |

### Verification pipeline match/unmatch rates

| Value | Location | Context |
|---|---|---|
| 95.1% | l.109 | References matched by initial Elasticsearch (Semantic Scholar + OpenAlex) pipeline |
| 2.33% | l.114 | Unmatched rate after GPT-4o-mini cleaning step (exclude non-academic strings) |
| 1.54% | l.115 | Unmatched rate after refining title extraction & re-querying |
| Stable through late 2022 | l.144 | Baseline error rate before LLM era |
| Sharp increase in 2023 | l.147–148 | Emergence of hallucinated citations |

### Hallucination rates & magnitudes (as of Aug 2025)

| Value | Location | Context |
|---|---|---|
| arXiv 0.39%; bioRxiv 0.21%; SSRN 1.91%; PMC 0.27% | l.155 | Estimated hallucination rate (regression coefficients), Aug 2025 |
| Steepest rise begins mid-2024 | l.156 | ~18 months after ChatGPT late-2022 release |
| Monthly est.: arXiv 3,353; bioRxiv 478; SSRN 767; PMC 8,140 | l.165–166 | Excess unmatched refs per month, Aug 2025 |
| 146,932 | l.166–167 | Total across 4 corpora for 2025 (if trends persist to year-end) |
| "very likely a lower bound" | l.170–171 | Method lenient on formatting/spelling; only checks title existence |

### Paper-level distribution (diffuse contamination)

| Value | Location | Context |
|---|---|---|
| 2 to 23 pp | l.178–179 | Increase in proportion of papers with ≥1 hallucinated reference (range across datasets) |
| 50%+ unmatched: arXiv 0.102 pp; bioRxiv 0.172 pp; SSRN 2.016 pp; PMC 0.018 pp | l.180–182 | Increase in papers heavily contaminated — small |
| 0–10% unmatched: arXiv 3.615 pp; bioRxiv 1.462 pp; SSRN 7.373 pp; PMC 1.430 pp | l.182 | Increase in lightly-contaminated papers — much larger. Refutes "few bad apples" |
| 19.9% to 91.4% | l.188 | Hallucination rate of LLM-generated citations in prior experimental studies (2023–2025), across models |

### LLM-use association

| Value | Location | Context |
|---|---|---|
| Higher in social sciences & computer science | l.190 | Field heterogeneity in hallucination rates |
| Pearson r = 0.441, P<0.001 | l.196, Fig.1k | Subfield-level correlation: estimated LLM use in writing vs hallucination rate (arXiv) |
| Holds at paper level | l.197–198, Fig.1l | Papers with higher estimated LLM usage → higher hallucination rate |

### Hallucination citers (who produces them)

| Value | Location | Context |
|---|---|---|
| Fewer prior pubs: 62.1% (arXiv), 62.6% (bioRxiv), 73.2% (SSRN), 27.4% (PMC) | l.221–223 | vs matched control (last-author prior papers up to 2022) |
| Zero prior pubs: 32.1% (arXiv), 9.3% (bioRxiv), 51.0% (SSRN), 3.7% (PMC) | l.223–224 | Citers much more likely to have zero prior publications |
| Productivity increase: 1.93× (arXiv), 2.22× (bioRxiv), 3.13× (SSRN), 1.33× (PMC) | l.230–231 | Relative rise pre-2023 → 2025; gap with controls "largely closed" |
| Hallucination rate attenuates with team size | l.231–232, Fig.2b | Solo/small teams higher than large teams |

### Beneficiaries (who gets credited)

| Value | Location | Context |
|---|---|---|
| 22.2% less likely | l.247 | Authors in hallucinated citations less likely to match any existing profile (invented names) |
| 68.8% more publications | l.250 | Conditional on matching: hallucinated cites over-credit high-productivity authors |
| 58.3% more citations | l.251 | Over-credit high citation-impact authors |
| 6.4 pp / 7.6% relative | l.253–254 | Over-credit male-named authors (gender disparity) |
| 12 pp weaker | l.262 | First–last author seniority hierarchy weaker in hallucinated refs; also smaller teams |

### Systemic responses / failure modes

| Value | Location | Context |
|---|---|---|
| 30,981 manuscripts | l.282 | arXiv manuscripts rejected by moderation (dataset analyzed) |
| 2.2% by Aug 2025 (4.5×) | l.284 | Hallucination rate in rejected manuscripts vs accepted |
| 78.8% | l.289 | Non-existent citations that PASS moderation and appear on arXiv |
| 2,241 bioRxiv preprints | l.293 | Preprints with unmatched refs traced to PMC published versions |
| 85.3% | l.295 | Hallucinations in preprints that PERSIST into published record |
| 0.11%–0.24% | Fig.3b caption, l.919 | Middle-decile PMC journal hallucination range; no monotonic gradient with journal impact |
| Citation-only entries growing since 2024 | l.309–311, Fig.3c | Google Scholar entries unlinked to real pubs but already cited; replicates across all 4 corpora (Fig. S10) |

---

## Scope & Limitations

- **Error type is narrow by design:** only references with **non-existent titles** (following [21] Asai et al.). Excludes fields whose citation norms omit titles.
- **Corpus-level, not document-level:** estimates *prevalence net of baseline*, does NOT classify individual references as hallucinated. "Hallucinated citations" throughout = estimated **excess** unmatched above pre-LLM baseline.
- **False negatives:** niche venues, heavily mathematical documents, title-less citation norms.
- **False positives:** LLMs generating a real title with incorrect metadata — argued to be minor relative to reported magnitudes (cites [20] Tramèr).
- **Estimates are a lower bound** (repeated: l.170–171, l.328, Abstract "conservative").
- Analysis window Jan 2020–Aug 2025; PMC is a 10% sample; SSRN uses Crossref metadata only.

## Does NOT claim / explicit boundaries

- Does NOT claim every unmatched citation is a hallucination — explicitly baselines against pre-LLM unmatched rate (l.94–98).
- Does NOT detect the "more prevalent and harder-to-detect variant" — **real citations deployed to support claims the sources do not actually make** (miscitation/citation-content errors, l.349–352, cites [35]–[38]); calls this an open challenge.
- Does NOT detect hallucinated **assertions in unstructured prose** — notes citation verification is "among the easiest hallucination detection problems" (l.358–359); the harder problems remain intractable.
- Does NOT claim causal proof of LLM authorship of any individual citation — evidence is associational (LLM-use signatures, field patterns, timing), described as "consistent with LLM use being a major driver."
- Frames science as a **best-case / lower-bound** domain; argues unstructured domains (govt reports, legal filings, clinical notes, journalism) likely worse but does not measure them.

## Section Map

1. **Abstract** (p.1) — headline: 111M refs / 2.5M papers, sharp rise, 146,932 in 2025, equity distortions.
2. **Introduction** (unnumbered, p.2–3) — motivation; hallucinations "in the wild"; prior approaches (prompting experiments = upper bound; tool-based domain audits = tens–hundreds of cases); this paper's baseline-differencing approach.
3. **Estimating hallucinated references at scale** (p.3–4) — verification pipeline (Elasticsearch/Semantic Scholar/OpenAlex, GPT-4o-mini cleaning, Google Scholar); four datasets; unmatched-rate time trend (Fig. S2).
4. **Results** (p.4–8):
   - *The rise and distribution of hallucinated citations* (Fig. 1) — rates, magnitudes, diffuse distribution, field heterogeneity, LLM-use correlation.
   - *Hallucination citers and their beneficiaries* (Fig. 2) — junior/less-productive citers; productivity catch-up; credit skew toward prominent, male, small-team authors; spillover to co-cited valid references.
   - *Systemic responses and failure modes* (Fig. 3) — arXiv moderation leakage (78.8%), preprint→journal persistence (85.3%), journal-impact stratification, Google Scholar citation-only accumulation.
5. **Discussion** (p.9–10) — "first large-scale audit"; systems-level (not individual-carelessness) framing; two compounding channels (path-dependent citation propagation; model-training feedback loop, cites [34] model collapse); limitations; generalizability to unstructured domains.
6. **Figures 1–3** (p.11–13).
7. **References [1]–[39]** (p.14–16).
