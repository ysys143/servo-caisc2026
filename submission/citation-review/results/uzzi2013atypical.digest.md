# Digest — uzzi2013atypical

**Citation:** Brian Uzzi, Satyam Mukherjee, Michael Stringer, Ben Jones. "Atypical Combinations and Scientific Impact." *Science* 342(6157), 468–472 (2013). DOI: 10.1126/science.1240474. (Report, ~5 pp.)

Based ONLY on this paper (full text via pdftotext).

---

## Thesis / Problem

Novelty is essential to creative ideas, yet new ideas are built from existing knowledge. The paper asks how scientific papers balance **atypical (novel) vs conventional** combinations of prior work, and how that balance relates to scientific **impact** (citations) and to **collaboration** (team vs solo). Central claim: the highest-impact science is grounded in *exceptionally conventional* combinations of prior work but simultaneously features an *intrusion of unusual combinations* — novelty and conventionality are not opposing factors. Such papers are ~twice as likely to be highly cited.

## Method — ATYPICALITY MEASURE (CONFIRMED)

**YES — this paper introduces and uses exactly the atypicality-of-novelty measure the manuscript attributes to it, via journal-pair z-scores linked to scientific impact.**

Pipeline:
1. For each paper, take **pairwise combinations of references** in its bibliography (co-citation pairs).
2. Count frequency of each co-citation pair across all papers published that year in Web of Science (WOS).
3. Compare observed frequencies to those **expected by chance** using **randomized citation networks** — a Monte Carlo switching algorithm that reshuffles all citation links while preserving each paper's/journal's total citation counts (in and out, forward/backward in time), so a paper with n citations keeps n citations.
4. Aggregate paper pairs into their **journal pairs** to focus on domain-level combinations.
5. Compute a **z score for each journal pair**: z > 0 = pair appears MORE often than chance = "conventional"; z < 0 = LESS often than chance = "atypical / novel".
6. Each paper gets a distribution of its journal-pair z-scores. Two summary statistics: **median z score** ("median conventionality," central tendency) and **10th-percentile z score** ("tail novelty," the unusual left tail).
7. Relate these to **impact** ("hit" papers = top 5th percentile of citations, by total citations through 8 years post-publication) and to **team size**.

This is the canonical z-score / journal-pair atypicality measure of novelty. Impact linkage is central (Fig 2, Fig 4).

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| 17.9 million papers / research articles | Abstract; §"In this study"; Conclusion | Corpus analyzed, WOS, all scientific fields |
| twice as likely (highly cited) | Abstract; Conclusion | High-conventionality + high-novelty papers vs background |
| 37.7% more likely | Abstract; §Fig 3 text | Teams (3+ authors) vs solo authors to insert novel combos into familiar domains |
| Web of Science (WOS) | §In this study | Data source |
| 122 million potential journal pairs | §We considered pairwise | From 15,613 journals indexed in WOS |
| 15,613 journals | §We considered pairwise | Journals indexed in WOS |
| z = 21.55 | §Comparing the observed | 1980 example: Tetrahedron & Experientia = conventional pairing |
| z = –17.67 | §Comparing the observed | 1980 example: Tetrahedron & Life Sciences = more unusual than chance (atypical) |
| 40.1% | §As a simple validation | Share of interdisciplinary journal pairs that were novel (z<0) in the 1990s |
| median z > 69.0 (1980s), > 99.5 (1990s) | §We found that papers | Half of papers exceed these median z scores → very high conventionality |
| 3.54% (1980s), 2.67% (1990s) | §We found that papers | Papers with median z score below zero (rare) |
| 40.8% (1980s), 40.7% (1990s) | §Focusing on each paper's left tail | Papers with 10th-percentile z score below zero |
| fewer than 4%; more than 50% above 64 | Fig 1B caption | Median z below 0 (<4%); >50% have median z above 64, 1980s/1990s |
| only 41% | Fig 1C caption | Papers (1980s & 1990s) with 10th-percentile z below 0 |
| top 5th percentile; 8 years | §Our next finding / Fig 2 | "Hit" paper definition = upper 5% of citations, total citations through 8 yrs |
| 9.11 out of 100 | §Papers with high median / Fig 2 | Hit rate: high median conventionality + high tail novelty (~2× background) |
| 5 out of 100 (5%) | §Papers with high median / Fig 2 | Background hit rate |
| 5.82 out of 100 | §show significantly lower | Hit rate: high median conventionality, low tail novelty |
| 5.33 out of 100 | §show significantly lower | Hit rate: low median conventionality, high tail novelty |
| 2.05 out of 100 | §show significantly lower / Fig 2 | Hit rate: low on both dimensions |
| 1990 to 2000 | Fig 2 caption | Sample for the hit-probability figure |
| P < 0.00001 | Fig 2 caption | Significance of hit-probability differences across categories |
| 6.7% / 23% / 26% / 44% | Fig 2 caption | Share of WOS papers in each 2×2 category (green/gold/red/blue) |
| 243 fields of science | §Further analyses | Universality check (fig S6, table S2) |
| 36.1, 39.8, 49.7% | §Collaboration text | High tail novelty share for 1, 2, 3+ authors (main text) |
| 36.2, 39.9, 49.7% | Fig 3A caption | High tail novelty share for solo, dual, 3+ authors (caption — slight variance vs text) |
| K-S: solo vs pair P=0.016; pair vs team P=0.001; team vs solo P<0.001 | §Fig 3A text & caption | Tail-novelty distributions distinct by team size |
| K-S: solo vs pair P=0.768; pair vs team P=0.417; team vs solo P=0.164 | §Fig 3B text & caption | Median conventionality: NO significant difference by team size |
| 11 equally sized categories | §In our final analysis / Fig 4 | Median-conventionality bins for regression (field fixed effects, per team size) |
| 85th to 95th percentile | §three primary findings / Fig 4 caption | Location of peak impact along median conventionality; reverses after |
| 1.4 million per year; 251 fields | §These findings / burden of knowledge | Current WOS new-article rate (note: 251 here vs 243 above) |
| Article cites 20 articles | Front matter (SI page) | "This article cites 20 articles, 9 of which can be accessed free" (26 numbered refs in list) |

## Scope & Limitations

- Observational/bibliometric; measures **co-citation journal pairings**, not semantic content of ideas. Novelty operationalized purely as unusual journal co-occurrence vs a randomized null, not conceptual novelty.
- Access to WOS via Thomson Reuters contract that forbids redistribution; summary stats/programs available on request.
- Method is at the paper/journal-pair resolution; authors note it "can be applied at the level of disciplines, papers, or topics within papers" in future work (not done here).
- Internal minor inconsistencies to flag: high-tail-novelty shares appear as 36.1/39.8/49.7% (text) vs 36.2/39.9/49.7% (Fig 3A caption); field count appears as 243 (universality analysis) vs 251 (burden-of-knowledge passage).

## Does NOT claim / Boundaries

- Does NOT claim novelty alone drives impact — the opposite: peak impact needs high conventionality WITH a novel tail; pure novelty (low conventionality) underperforms.
- Does NOT establish causation; relationships are associational/regularities ("nearly universal pattern").
- Does NOT measure semantic/conceptual atypicality — only distributional co-citation atypicality via z-scores.
- Does NOT claim teams are more conventional or less conventional than solo (no significant difference in median conventionality); teams' edge is specifically in incorporating tail novelty.

## Section Map (Uzzi content within the PDF)

- Title / authors / abstract — front.
- Intro (creativity, boundary-spanning, burden of knowledge, Newton/Darwin conventionality anecdotes).
- Methods: co-citation pairs → randomized networks (Monte Carlo) → journal-pair z scores → median z + 10th-percentile z.
- Fig 1 (novelty/conventionality distributions), Fig 2 (hit probability 2×2), Fig 3 (authorship structure), Fig 4 (regression interplay).
- Discussion / implications (creativity theory, burden of knowledge, e-books/blue-jeans analogies, future work).
- References and Notes (26 numbered entries).

**NOTE on PDF:** pdftotext output interleaves two adjacent *Science* articles (Martorell/Vočadlo inner-core paper refs 1–32; Kuchenreuther *et al.* HydG/FeFe-hydrogenase paper). All facts above are drawn strictly from the Uzzi article body/figures/refs.
