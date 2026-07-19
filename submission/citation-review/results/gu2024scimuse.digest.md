# Digest — gu2024scimuse

**Title:** Interesting Scientific Idea Generation using Knowledge Graphs and LLMs: Evaluations with 100 Research Group Leaders
**Authors:** Xuemei Gu, Mario Krenn (Max Planck Institute for the Science of Light, Erlangen)
**Venue/ID:** arXiv:2405.17044v3 [cs.AI], 7 Jan 2025
**Read:** full paper (main text + Supplementary Information), 14 pages.

---

## Thesis / Problem

The volume of scientific literature makes it hard for researchers to find novel, impactful, and especially *interdisciplinary* ideas. The paper asks two questions: (1) Are AI-generated research ideas compelling to *experienced* scientists (not just PhD students, as in prior small studies)? and (2) How can we predict/improve the quality of such ideas? They introduce **SciMuse**, a system that generates personalized research-collaboration ideas, and run the largest human evaluation of AI-generated ideas to date.

## Method — direct answers to the audit questions

**Does SciMuse use KNOWLEDGE GRAPHS + LLMs for scientific idea generation? — YES.**
- Builds a large evolving knowledge graph from scientific literature: nodes = scientific concepts, edges = concept co-occurrence in titles/abstracts, augmented with citation data as an impact proxy. Concepts extracted via the RAKE algorithm from ~2.44M preprint (arXiv/bioRxiv/chemRxiv/medRxiv) titles+abstracts, refined (GPT + Wikipedia + manual) to a final **123,128 concepts**; edges from **58M** OpenAlex papers.
- Generation: for two researchers (A, B), extract each one's concepts from their last-2-years publications, refine with GPT-4, build personalized subgraphs, pick a concept pair, and prompt **GPT-4** (with self-reflection: generate 3 ideas, refine twice, select best) to write a personalized collaboration project. This KG-representation was introduced in ref [12] (Gu & Krenn 2024, impact forecasting).

**Does structuring semantic memory as a relational corpus / knowledge-graph IMPROVE the QUALITY of the generated hypotheses/ideas? — NUANCED / largely NO for generation, YES for SELECTION.**
- CRITICAL FINDING: They find **no significant difference in interest levels** between ideas generated from (1) random concept pairs, (2) highest-predicted-impact concept pairs, or (3) NO concept pair at all (a KG-free "sanity" baseline where GPT-4 works only from paper titles). See Results "Properties of interesting research suggestions" and Supp. Fig. S1. So the KG does **not** measurably raise the *generation* quality of ideas over a no-KG LLM baseline in the human ratings.
- Where the KG DOES add value: (a) it lets them *analyze* which graph features correlate with interest, and (b) it enables a supervised neural network — using **only knowledge-graph features, not the generated text** — to *predict/select* which ideas will be highly rated, achieving precision well above random. So the claim "structuring memory as a KG improves idea QUALITY (as evaluated by group leaders)" is only supported in the weak sense of *intelligent concept-pair selection can influence interest rankings* — not that KG-grounded generation beats plain-LLM generation. Authors' own words: "intelligent concept pair selection alone can significantly influence interest rankings in the graph-based approach."

**Evaluated with research group leaders? — YES.**
- 110 research group leaders from 54 Max Planck Institutes; 104 natural-science, 6 social-science. 4,451 responses; each rated up to 48 projects on interest scale 1 ("not interesting") to 5 ("very interesting"). Reported as "over 100" / "the largest human evaluation of AI-generated research ideas to date."

**Does it CLOSE a discovery loop, or just generate/rank ideas? — It does NOT close a loop.**
- SciMuse only *generates* ideas and *predicts their interest*. No hypothesis is executed, no experiment run, no result fed back. The Discussion explicitly frames closed-loop automation as FUTURE work: "Currently, while large-language models have been integrated into laboratories, the main idea of the experiment has been provided by human scientists. In the future, one might envision the entire scientific process becoming fully automated — from the generation of an interesting idea, as we demonstrate here, to its automated execution." So SciMuse = idea generation + interest prediction only; explicitly the "idea" front-end of a not-yet-closed loop.

**Prediction methods (two, fundamentally different):**
1. Supervised small neural network (PyTorch), 25 best-performing KG features (from 144 computed; 141 from ref [12] + 3 distance/impact features), 50 hidden neurons, dropout, Monte Carlo cross-validation. Trained on human rankings, uses NO generated text.
2. GPT zero-shot pairwise ranking (GPT-3.5 / GPT-4o / GPT-4o-mini), ELO tournament (initial 1400), 22,000–45,000 pairwise comparisons, no human-evaluation feedback.

---

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| 58 million research papers | Abstract, Results, Supp. A | OpenAlex papers used to form KG edges (papers containing ≥2 concepts). |
| 92 million papers | Supp. A | OpenAlex journal papers with title+abstract+citation after filtering; 58M of these have ≥2 concepts. |
| ~2.44 million papers | Fig.1 caption, Results, Supp. A/B | arXiv/bioRxiv/chemRxiv/medRxiv preprints for concept extraction; cutoff Feb 2023. |
| 123,128 concepts | Fig.1 caption, Results, Supp. B | Final refined concept list (KG nodes). |
| 726,439 concepts | Supp. B | Initial RAKE candidate list (2-word ≥9 articles; >3-word ≥6). |
| 368,825 concepts | Supp. B | After automated tools + manual review. |
| 286,311 concepts removed | Supp. B | Removed by GPT-3.5 refinement. |
| 40,614 entries restored | Supp. B | Restored via Wikipedia (mistakenly removed). |
| 100 / "over 100" research group leaders | Title, Abstract, Discussion | Headline evaluator count. |
| 110 research group leaders | Fig.2 caption, Results ("Large-scale human evaluation") | Actual number invited/participating. |
| 104 natural / 6 social science | Results | Field split of the 110. |
| 54 Max Planck Institutes | Results | Institutes the 110 leaders came from. |
| 87 Max Planck Institutes | Supp. C | Total MPIs classified: 68 nat, 19 soc. |
| 4,451 responses / suggestions | Abstract, Fig.2 caption, Results | Total evaluated ideas. |
| 4,400 / "more than 4,400" | Abstract | Rounded headline figure for ideas ranked. |
| up to 48 projects per leader | Results | Max ratings per evaluator. |
| scale 1–5 | Results, Fig.2c | 1 = not interesting, 5 = very interesting. |
| 394 rated 5 (very interesting) | Fig.2 caption, Results | Count at top rating. |
| 713 rated 4 | Fig.2 caption | Count at rating 4. |
| 1,107 projects (≈25%) rated 4 or 5 | Results | "nearly 25%" high-interest. |
| 2,996 suggestions/responses | Results, Figs.3–4, Supp. H–K | Subset generated using KG concept pairs (used for correlation analysis + prediction). |
| 59.7 mean papers (median 36.0, range 9–402) | Results, Supp. Table S1 | Evaluators' publication stats (as of Jan 1 2024). |
| 3,759.7 mean citations (median 1630.0, range 20–85,778) | Results, Supp. Table S1 | Evaluators' citation stats. |
| 8 knowledge-graph features | Fig.3 caption | Features correlated with interest in Fig.3. |
| 50 equal bins/groups | Fig.3 caption, Results | Binning for correlation plots. |
| 144 features computed | Supp. H | Total per concept pair (141 from ref [12] + 3). |
| 25 best-performing features | Fig.4 caption, Supp. H, Table S2 | NN input features. |
| 50 neurons, 1 hidden layer, 1 output | Results, Supp. H | NN architecture. |
| ROC AUC 64.5% (NN), 67.3% (GPT-4o) | Fig.4a caption | Binary-classification AUC ("nearly 2/3"). |
| top-1 precision 70% (NN), 51.0% (GPT-4o), 52.9% (GPT-3.5) | Fig.4b caption | Top-N precision. |
| top-5 precision 60.4% (NN), 46.7% (GPT-4o), 43.7% (GPT-3.5) | Fig.4b caption | Top-N precision. |
| top-3 precision 66.4% (NN), 45.0% (GPT-4o), 47.2% (GPT-3.5) | Results (Predicting interest) | N=3 precision; NOTE: differs from Fig.4b's top-1/top-5 numbers. |
| random-selection baseline ≈23% | Results, Fig.4b | Base rate of high-interest ideas. |
| 22,000–45,000 pairwise comparisons | Results, Supp. J | GPT ELO tournament matches (per model). |
| ELO initial score 1400 | Results, Supp. J | Zero-shot ranking start value. |
| 10,000 pairwise selections | Fig.S4 caption | (Alternate stated count for ELO matches — note discrepancy with 22k–45k.) |
| 130 iterations | Supp. H | Monte Carlo CV iterations until AUC std < 1e-3. |
| lr=0.003, dropout=20%, weight decay=0.0007 | Supp. H | NN hyperparameters; train/val/test = 75/15/10%. |
| GPT-4 | Results | Idea-generation LLM. |
| GPT-3.5, GPT-4o, GPT-4o-mini | Results, Supp. J–M | Zero-shot ranking models. |
| GPT-4 vs GPT-4o test: 31.1% vs 60.56% (8.3% draw) | Supp. M | 3 leaders, 180 pairs; GPT-4o preferred. |
| GPT-4o vs GPT-o1: 11/11 favored GPT-o1 | Supp. M | 1 leader, 11 pairs; o1 always preferred. |
| 1665 → April 2023 | Results | Temporal span of the evolving KG (Hooke's Jupiter spot to present). |
| self-reflection: 3 ideas, refine twice | Results | Generation prompt technique (ref [30] Self-Refine). |
| up to 7 paper titles per researcher | Results | Provided to GPT-4 in generation prompt. |
| prior studies: 6 NLP / 3 social-science / 10 CS+biomed PhD students | Intro (refs 14–16) | Small-scale baselines SciMuse contrasts against. |

## Prior small-scale evaluations SciMuse positions against
- SciMON [14] — 6 NLP PhD students. Yang et al. [15] — 3 social-science PhD students. ResearchAgent [16] — 10 PhD students (CS + biomedicine). SciMuse's contribution is scale (110 experienced group leaders) and evaluator seniority.

## Scope & Limitations / "Does NOT claim"
- Does NOT close a discovery/experimentation loop; no execution, no wet-lab or computational validation of generated ideas. Loop-closing is explicitly future work.
- Does NOT show KG-grounded generation produces *more interesting ideas* than a KG-free LLM baseline — interest levels are statistically indistinguishable across random / high-impact / no-concept generation modes (Supp. Fig. S1). KG value is in *analysis and interest prediction/selection*, not in raising raw generation quality.
- Interest = *self-reported researcher interest*, not novelty, correctness, feasibility, or realized impact. No claim that highly-rated ideas lead to successful projects.
- Prediction accuracy is modest (AUC ≈ 2/3); the emphasis is top-N precision for surfacing a few good ideas, not full-list accuracy.
- Evaluator pool is heavily natural-science skewed (104/110) and confined to the Max Planck Society; "humanities/social sciences" representation is small (6 leaders).
- Prompt-engineering improvements (Supp. L) did NOT yield more interesting ideas.
- Ideas are framed specifically as *collaboration* proposals between two researchers, not standalone hypotheses.

## Section map
1. **Introduction** — problem, prior small-scale studies (refs 14–16), motivation for experienced-evaluator study.
2. **Results** — (a) Knowledge graph generation; (b) Personalized research suggestions; (c) Large-scale human evaluation (110 leaders, 4,451 responses); (d) Properties of interesting suggestions (KG-feature correlations, Fig.3; no-difference-across-generation-modes finding); (e) Predicting interest (supervised NN + GPT zero-shot ELO, Fig.4).
3. **Discussion** — largest evaluation to date; two prediction methods; interdisciplinarity value; future closed-loop automation vision.
4. **Acknowledgements / Ethics / Data & Code** — GitHub artificial-scientist-lab/SciMuse, Zenodo dataset.
5. **Supplementary A–M** — datasets, concept-list pipeline, MPI classification, prompts, Fig.S1 three-method interest, NN details (Fig.S2), decision trees (Fig.S3), zero-shot ranking (Fig.S4), five-method comparison (Fig.S5), prompt engineering, GPT-4o/o1 small tests, Table S1 (researcher stats), Table S2 (top-25 features).

## Verdict on likely citation uses
- SAFE to cite for: KG+LLM system for scientific idea generation; largest human evaluation of AI-generated ideas (100+/110 group leaders, 4,451 ratings); LLM/NN prediction of idea interest; 58M-paper / 123,128-concept KG.
- RISKY / would be a MISCITATION: claiming SciMuse "closes a discovery loop" or executes/validates ideas (it does not); claiming KG structuring *improves generated-idea quality* over plain-LLM generation (the paper's own finding is *no significant difference* across generation modes — the KG helps *predict/select*, not *generate*, more-interesting ideas).
