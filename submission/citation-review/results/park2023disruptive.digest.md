# Digest: park2023disruptive

**Full citation:** Park, M., Leahey, E., & Funk, R. J. (2023). "Papers and patents are becoming less disruptive over time." *Nature* 613, 138–144. (PDF is the accepted/preprint manuscript form, 56p; affiliations: Carlson School of Management, U. Minnesota; Dept. of Sociology, U. Arizona.)

_Digest written BLIND — based ONLY on this paper, with no knowledge of what the citing manuscript claims._

---

## Thesis / Problem

Central claim: across 6 decades, papers and patents have become **less disruptive** — i.e., increasingly less likely to "break with the past" and push science/technology in genuinely new directions, and more likely to consolidate (extend/entrench) existing knowledge.

Motivating puzzle: theories of scientific/technological change treat discovery as an *endogenous* "shoulders of giants" process, and recent decades saw exponential growth in knowledge volume — conditions that *should* be ripe for major advances. Yet field-specific studies suggest progress is slowing. The paper tests this at scale with a single unified metric and reconciles the slowdown with the "shoulders of giants" view by tracing it to a **narrowing use of prior knowledge**.

## Method — DISRUPTION measure (KEY for the audit)

**YES — this paper is built entirely around a field-level DISRUPTION / novelty metric: the CD index (CD5).** This is the load-bearing fact.

- The **CD index** ("Consolidation–Disruption index") is a **citation-network-based quantitative measure** that characterizes whether a paper/patent is *consolidating* or *disruptive*.
- **Intuition:** if a work is disruptive, future work citing it tends *not* to also cite its predecessors (the work eclipses what came before). If consolidating, future work citing it *also* cites its predecessors (the work builds on and reinforces prior knowledge).
- **Range: −1 (fully consolidating) to +1 (fully disruptive).** Zero = midpoint.
- **CD5** = the index computed using a **5-year forward citation window** after publication. (Alternative windows — 10-year, and all-citations-to-2017 — tested in Extended Data Fig. 2.)
- The CD index is **NOT original to this paper.** It is drawn from **Funk & Owen-Smith (2017), *Management Science* 63:791–817** (ref 12, "A dynamic network measure of technological change"). This paper *applies* it at scale and validates the declining-disruption finding; it does not invent the measure.
- Validation: CD index "has been validated extensively in prior research, including through correlation with expert assessments" (refs 12, 29).
- Corroborating (non-CD) indicators used: type-token ratio of titles/abstracts (word diversity), new-word-pair novelty, "atypical combinations" measure (Uzzi et al. 2013, ref 32), and verb-usage shifts (creation/discovery verbs → improvement/application verbs). Alternative disruption operationalizations also tested (Bornmann et al. DI5^(lnok), ref 35; Leydesdorff et al. DI*, ref 36).

So: **the paper's core metric is a field-level disruption/novelty index (the CD index), used to quantify how "disruptive" vs. "consolidating" papers and patents are.** This matches the description of it as a "disruption" measure of novelty.

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| 45 million papers | Abstract / Summary (l.19) | Total papers across **6 large-scale datasets** combined (WoS + JSTOR + APS + MAG + PubMed, plus the replication corpora). This is the headline "45M" figure. |
| 3.9 million patents | Abstract (l.19) | Patents from USPTO Patents View. |
| 6 large-scale datasets | Abstract (l.19) | Number of data sources. |
| 6 decades | Abstract (l.19) | Temporal span of analysis. |
| CD index | Abstract (l.20); "Measurement of disruptiveness" (l.69) | The core "novel quantitative metric" (ref 12) characterizing consolidation vs. disruption. |
| −1 to +1 | l.74 | Range of CD index (−1 consolidating, +1 disruptive). |
| CD5 (5-year window) | l.75 | Primary operationalization. |
| 24,659,076 papers | Fig. captions; Methods "WoS data" (l.523) | **Main WoS analytical sample**, 1945–2010 (after removing non-research docs). Note: distinct from the 45M cross-dataset figure. |
| 3,912,353 patents | Methods "Patents View data" (l.533) | Main Patents View analytical sample, utility patents 1976–2010. |
| 25 million papers (1945–2010) | l.52 | WoS papers described in main text intro (rounded). |
| 390 million citations; 25M titles; 13M abstracts | l.54–55 | WoS content. |
| 35 million citations; 3.9M patent titles/abstracts | l.55 | Patents View content. |
| 20 million papers | l.57 | Combined size of the 4 replication corpora (JSTOR, APS, MAG, PubMed). |
| Kohn & Sham (1965): CD5 = **−0.22** | l.78 | Example of a *consolidating* Nobel paper (density functional method). |
| Watson & Crick (1953): CD5 = **0.62** | l.79 | Example of a *disruptive* Nobel paper (DNA structure). |
| Papers decline 91.9% → 100% | l.87–89 | CD5 drop 1945→2010: Social Sciences 0.52→0.04 (91.9%); Physical Sciences 0.36→0 (100%). |
| Patents decline 78.7% → 91.5% (main text) | l.90–91 | Computers & Comm. 0.30→0.06 (78.7%); Drugs & Medical 0.38→0.03 (91.5%). (Fig. 2 caption gives slightly different framing: 93.5%–96.4%.) |
| Title type-token decline: papers 76.5%–88% | l.106–107 | Word-diversity decline, 1945–2010 (Social Science 76.5% → Technology 88%). |
| Patent title decline 32.5%–81% | l.107–108 | Chemical 32.5% → Computer & Comm. 81%. |
| n=635 Nobel papers; n=223,745 Nature/PNAS/Science | Fig. 5 caption (l.401) | High-quality subsample; decline persists → not a quality artifact. |
| n=5,030,179 disruptive papers; n=1,476,004 patents | Fig. 4 caption (l.386) | Conservation-of-highly-disruptive-work analysis (CD5 > 0). |
| Highly disruptive threshold CD5 > 0.25 | Fig. 4 caption (l.396) | Definition for inset composition plots. |
| WoS archive: 65M docs, 28,968 journals, 735M citations, 1900–2017 | Methods (l.518–520) | Full source scale before subsetting. |
| Patents View: 6.5M patents, 92M citations, 1976–2017 | Methods (l.528–529) | Full source scale; 91% utility patents. |

## Scope & Limitations (as stated by authors)

- CD index is "a relatively new indicator... will benefit from future work on its behavior and properties, especially across data sources and contexts" (l.224–225).
- Studies of different **citation practices** (which vary across fields) would be informative — acknowledged as a caveat (l.225–226).
- Analysis window deliberately 1945–2010 (papers) / 1976–2010 (patents); pre-1945 WoS and post-2010 excluded (post-2010 needs forward-citation years; pre-1945 less reliable).
- Growth-of-knowledge regression gave **conflicting** signs: positive effect of knowledge stock on paper disruptiveness, **negative** for patents (l.182–183) — resolved via the "availability ≠ use" argument.

## Does NOT claim / Boundaries

- Does **NOT** claim disruptive/breakthrough science has stopped: the **absolute number** of highly disruptive works stays roughly **constant** over time ("conservation") — only the *rate/proportion* declines (l.131–140, l.215–223).
- Does **NOT** attribute the decline to declining research **quality**, changing **citation/publication/authorship practices**, or **field-specific** factors — explicitly rules these out via robustness checks (premier-venue & Nobel subsamples, normalized CD variants, regression controls, Monte Carlo rewiring) (l.144–172).
- Does **NOT** claim "low-hanging fruit" exhaustion explains it (cross-field similarity argues against it) (l.96–98, l.145–146).
- Does **NOT** invent the CD index (that is Funk & Owen-Smith 2017, ref 12). It is not a paper primarily about AI, LLMs, or automated science — it is a science-of-science / bibliometrics study.
- The mechanism it *does* endorse: decline linked to a **narrowing in the use of prior knowledge** (less diverse citations, more self-citation, older cited work) (l.176–202).

## Section Map

1. Summary/Abstract (l.16–28)
2. Intro — slowdown concerns, explanations, gaps (l.29–59)
3. **Measurement of disruptiveness** — defines CD index / CD5 (l.61–83)
4. **Declining disruptiveness** — Fig. 2, CD5 over time by field (l.85–98)
5. **Linguistic change** — word diversity, novelty, verb shifts (l.100–129)
6. **Conservation of highly disruptive work** — absolute counts stable (l.131–140)
7. **Alternative explanations** — quality, data, practices ruled out (l.144–172)
8. **Growth of knowledge and disruptiveness** — availability vs. use (l.176–202)
9. **Discussion** — implications, limitations, policy (l.204–234)
10. References (l.238–348), Figure/Extended Data captions (l.352–511), Methods (l.515+)
