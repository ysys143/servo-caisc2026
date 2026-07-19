# Digest: gottweis2026coscientist

**Full title:** Accelerating scientific discovery with Co-Scientist
**Venue:** Nature, Vol. 655, 9 July 2026, pp. 487–496. DOI 10.1038/s41586-026-10644-y. Open access.
**Dates:** Received 20 Mar 2025; accepted 11 May 2026; published online 19 May 2026.
**Lead authors:** Juraj Gottweis, Wei-Hung Weng, Alexander Daryin, Tao Tu, et al. (Google Cloud AI Research / Google DeepMind / Google Research, with Stanford, Imperial College London, Sequome, Houston Methodist). Corresponding: Gottweis, Weng, Kohli, Pawlosky, Karthikesalingam, Natarajan.

---

## Thesis / problem
Scientists face a "breadth and depth conundrum": topics need deep subject expertise, yet insight arises from broad cross-disciplinary knowledge (p.487, lines 43–46). The paper introduces **Co-Scientist**, a **multi-agent AI system built on Gemini** designed as a "structured scientific thinking engine" that, given a research goal in natural language, generates **novel, original research hypotheses and experimental protocols** for experimental verification (abstract; p.487–489). It positions itself as going *beyond* literature-summarization / "deep research" tools by generating new knowledge and novel hypotheses (p.489 "Introducing Co-Scientist"; Methods criterion 3, lines 1802–1804).

## Method — is it a MULTI-AGENT HYPOTHESIS-GENERATION system? **YES.**
- Compound, multi-agent AI system built on Google's Gemini (Gemini 2.0 models used as the base foundational LLM for **all** agents in this study; Methods lines 1791–1793). Framework is explicitly **model agnostic / model-portable** (lines 580–582, 1614–1617, 1942–1946).
- **Supervisor agent** parses the natural-language research goal, derives a research-plan configuration, and dynamically allocates resources to specialized worker agents within an **asynchronous, continuous task-execution framework / task queue** (Fig. 1b; Methods lines 1812–1835, 1864–1873).
- **Six specialized agents** mirroring the scientific method (lines 452–454, 1874–1918):
  1. **Generation agent** — literature exploration via web search, simulated scientific debates (self-critique/self-play), iterative assumption identification, research expansion.
  2. **Reflection agent** — simulates peer reviewer; review types: initial, full (with web search), deep verification, observation, simulation, recurrent/tournament (lines 1978–2044).
  3. **Ranking agent** — Elo-based tournament with pairwise multi-turn scientific-debate comparisons; top-ranked get multi-turn debates, lower-ranked get single-turn (lines 2046–2070).
  4. **Proximity agent** — builds proximity/similarity graph for clustering, de-duplication (lines 2072–2078).
  5. **Evolution agent** — refines top hypotheses (grounding, coherence/feasibility, inspiration, combination, simplification, out-of-box); **generates new hypotheses, does not modify/replace existing ones** (lines 2079–2104).
  6. **Meta-review agent** — synthesizes recurring patterns from all reviews/debates into a meta-review critique appended to agent prompts; enables "feedback propagation and learning **without back-propagation** (no fine-tuning or RL)" (lines 1935–1941, 2106–2127). Also generates final research overview and suggests research contacts.
- Persistent **context memory** for long-horizon reasoning (lines 1829–1832).

### Generate–tournament–evolve mechanism
- Generation agent curates initial hypotheses → Reflection agent reviews → **Ranking agent runs an Elo-based tournament** (initial Elo = **1,200** for each new hypothesis, line 2057) using pairwise scientific-debate matches to find win/loss patterns → Evolution/Proximity/Meta-review agents operate on the tournament state to improve quality → Supervisor re-weights and re-samples agents based on summary statistics → loop repeats, scaling **test-time compute** (lines 365–374, 1919–1934). This "generate, debate, evolve" loop is a **self-improving loop** (lines 158–159, 1596–1601). Elo is described as *not the direct optimization target* — its increase *emerges* from feedback loops (lines 550–553).

## Does it include EXPERIMENTAL BIOMEDICAL VALIDATION (wet-lab)? **YES — in vitro wet-lab for two of three tasks; AMR was in-silico recapitulation matched to an independent experimental study.**
Three end-to-end biomedical validations (Table 1; Fig. 1c), all with expert-in-the-loop:
1. **Drug repurposing for AML** — **in vitro wet-laboratory** cell-line viability assays (Fig. 3–4). Wet-lab performed with expert oncologist oversight + Signios Biosciences team; AML cell lines from R. Majeti lab (Stanford). Explicitly framed as an "initial biological validation step" / "viability check," **not** a replacement for preclinical/clinical validation (lines 884–890).
2. **Liver fibrosis novel-target discovery** — **in vitro** using human hepatic organoids + live-cell imaging; anti-fibrotic activity confirmed (lines 1564–1575).
3. **AMR (cf-PICI mechanism)** — Co-Scientist independently proposed the top hypothesis **in silico in 2 days**; this **matched** the primary discovery of an independent, co-timed genomic+experimental study (refs 2, 21) **before that study completed peer review** — i.e., recapitulation, not wet-lab run by the system (lines 1577–1588). Co-Scientist itself did not run bacterial experiments.

> Note the Fig. 1c caption's blanket phrasing "All hypotheses generated by Co-Scientist were subsequently verified through independent in vitro laboratory experiments" (lines 413–414) — for AMR the "verification" is the independent co-timed lab study, not experiments driven by the system.

---

## FACTS TABLE (exhaustive)

### Evaluation / benchmarking
| Value | Location | Context |
|---|---|---|
| 203 distinct research goals | p.490 lines 533–535; Fig. 2a caption line 810 | Elo test-time-compute scaling analysis; goals entered until **3 February 2025**; predominantly biomedicine, also math and physics |
| 10 temporal buckets (equal size, sequential 10% each) | p.490 lines 537–541 | Hypotheses partitioned by generation time to measure Elo improvement |
| 15 research goals | p.490 lines 554–556; Fig. 2b; line 810 | Subset curated as challenging problems by **seven biomedical experts** (PhD holders, postdocs/faculty) |
| 11 of the 15 goals | p.491 lines 594–596; Fig. 2c; line 810 | Small-scale blinded expert evaluation (novelty/impact/preference) |
| Preference rank 2.36; novelty 3.64; impact 3.09 (out of 5) | p.491 lines 826–829 | Co-Scientist averages across 11 expert-evaluated goals; most preferred vs baselines |
| Baseline models (Elo tournament) | p.490 lines 564–567 | Gemini 2.0 Pro Experimental, Gemini 2.0 Flash Thinking Experimental 12-19, OpenAI o1, OpenAI o3-mini-high, DeepSeek R1 |
| LLM-as-a-judge evaluators | p.491–492 lines 837–841 | OpenAI o3-mini-2025-01-31, o1-preview-2024-09-12, Gemini 2.0 Pro Experimental, Gemini 2.0 Flash Thinking Experimental 01-21 (4 judges) |
| Elo initial rating = 1,200 | Methods line 2057 | Assigned to each newly added hypothesis |
| No performance saturation observed | p.490 lines 576–578 | Suggests further test-time compute scaling could keep improving quality |

### Ablation results (Methods, lines 2200–2235)
| Value | Location | Context |
|---|---|---|
| Novelty score 6.14 → 2.38 (out of 10) | lines 2210–2213 | Reflection agent **without** search wrongly rated known non-novel ideas high (6.14); **with** search correctly low (2.38) |
| Correctness score 7.4 → 8.46 (out of 10) | lines 2214–2215 | Search tool raised avg correctness on known-correct ideas |
| GPQA AUC 0.643 → 0.651 | lines 2215–2218 | Search tool effect; base LLM = Gemini 2.0 Flash |
| GPQA precision 70.9% → 75.4% | lines 2223–2224 | Evolution agent iterative refinement |
| Hypothesis quality score 4.7 → 5.6 | lines 2224–2225 | Evolution agent, constructed dataset |
| Meta-review AUC 0.521 → 0.597 | lines 2229–2231 | Correctness-review prediction, constructed dataset |
| Meta-review AUC 0.629 → 0.634 | lines 2231–2232 | GPQA diamond dataset |

### Drug repurposing / AML wet-lab (Figs. 3–4, Extended Data)
| Value | Location | Context |
|---|---|---|
| 2,300 approved drugs across 34 cancer types | p.492 lines 871–873 | Constrained search space for repurposing predictions; oncologist expert review |
| 5 AML/control cell lines | p.492 lines 881–883 | AML: MOLM-13, KG-1a, HL-60, NOMO-1; non-AML control: TK6 |
| 30 top-ranked drug candidate hypotheses | p.492 lines 896–897 | Shared with expert oncologists for selection |
| 5 initial repurposing candidates | p.492 lines 911–913 | binimetinib, pacritinib, cerivastatin, pravastatin, dimethyl fumarate |
| 3 of 5 inhibited cell viability | p.492 lines 914–915 | binimetinib, pacritinib, cerivastatin (pravastatin & DMF little/no effect — Ext Data Fig. 4) |
| Binimetinib IC50 as low as 2 nM | p.492 lines 916–918 | In all AML cell lines except NOMO-1; much higher in TK6 control |
| Binimetinib MOLM-13 IC50 = 0.01 µM (0.003–0.025) | Fig. 3a line 1143 | Dose-response |
| Pacritinib MOLM-13 IC50 = 0.73 µM (0.38–1.35) | Fig. 3b line 1133 | Dose-response |
| Cerivastatin MOLM-13 IC50 = 6.73 µM (1.8–32) | Fig. 3c line 1123 | Dose-response |
| 3 autonomous novel candidates (no oversight) | p.492 lines 934–935 | nanvuranlat, KIRA6, leflunomide (no DepMap scores or expert feedback given) |
| KIRA6 = IRE1α inhibitor | p.492 lines 936–942 | Novel candidate; targeting IRE1α in AML explored before (ref 25) but not with KIRA6 |
| KIRA6 IC50: KG-1a 10 nM; TK6 180 nM; NOMO-1 144 nM; MOLM-13 1,750 nM; HL-60 870 nM | p.492–493 lines 1197–1201 | Nanomolar–low micromolar; most effective in KG-1a |
| 18-fold separation (KG-1a vs TK6) | p.492 lines 1201–1202; Fig. 3 caption 1188 | Selective therapeutic window |
| 7 drug combinations evaluated | p.493 lines 1232–1233 | In MOLM-13 and KG-1a |
| Dual example: JNJ-64619178 + selinexor | p.493 lines 1234–1236; Fig. 4a,b | Predominantly synergistic in MOLM-13 |
| Triple example: JQ1 + olaparib + MSA2 | p.493 lines 1235–1236; Fig. 4c,d | Synergy analysis (HSA / Bliss) |
| KG-1a = TP53 mutant | p.493 lines 1237–1238 | Context-dependent (mix of synergy/antagonism) |
| 11 individual drugs, IC50 baseline | Ext Data Table 1, lines 2467–2478 | In MOLM-13 and KG-1a; 72–96 h exposure |
| n = 3 biological triplicates | Fig. 3 caption line 1193; Methods lines 2240–2246 | All in vitro experiments |
| Binimetinib clinical niche: frail, pretreated AML; UGT1A1 metabolism avoids CYP3A4 interactions | p.494 lines 1548–1553 | Structured translational analysis output |

### Liver fibrosis (lines 1564–1575)
| Value | Location | Context |
|---|---|---|
| 3 epigenetic targets/modifiers identified | lines 1568–1571 | 3 top-ranked hypotheses selected by experts |
| 2 of 3 drugs showed significant anti-fibrotic activity | lines 1570–1571 | In human hepatic organoids, no cellular toxicity |
| Vorinostat = FDA-approved | lines 1571–1573 | One effective drug already FDA-approved (for cancer) → repurposing opportunity |

### AMR / cf-PICI (lines 1577–1588; Fig. 1c)
| Value | Location | Context |
|---|---|---|
| Hypothesis generated in 2 days | lines 322–324, 1583 | Co-Scientist matched empirical findings that took scientists ~10 years (2015–2024) |
| Top hypothesis: cf-PICIs interact with diverse phage tails to expand host range | lines 1581–1582 | Matched independent co-timed study (refs 2, 21) before peer review |
| Bacterial species incl. E. coli, Klebsiella pneumoniae | lines 1580 | cf-PICIs carry virulence & antibiotic-resistance genes |

### System / software / infrastructure
| Value | Location | Context |
|---|---|---|
| Gemini 2.0 = base LLM for all agents | Methods lines 1791–1793, 1942 | Study used Gemini 2.0; framework model-agnostic |
| Model-agnostic; cites Gemini 3, GPT 5.4, Opus 4.6 | Discussion lines 1614–1617 | Future frontier models expected to improve system |
| Python 3.11.7; pandas 2.1.4; numpy 1.26.4; seaborn 0.12.2; matplotlib 3.8.0 | Code availability lines 2289–2291 | Analysis stack |
| GraphPad Prism 10.6.0 | lines 2292–2293 | Dose-response curve fitting / IC50 |
| Julius AI statistical software (accessed Nov 2025) | lines 2294–2295 | Dose-effect / combination synergy analysis |
| GPQA diamond, DepMap Q2 2024, Open Targets Platform | Data availability lines 2262–2268 | Public datasets used for dev/benchmarking |
| Full source code NOT publicly available | Code availability lines 2270–2280 | Proprietary infra, compute, safety; experimental access program instead; pseudocode (Supp. Note 8) + prompts (Supp. Note 9) provided |
| Human time: AML prompt < 1 h; final review ~3 h | Methods lines 2176–2186 | Expert clinician time investment |
| NIH awards 1R01DC021133, 1R24OD035408 to G.P. | Funding line 2362 | Funding |

---

## Scope & limitations (explicit)
- Elo is **auto-evaluated, not independent ground truth** (Fig. 2 caption; Ext Data Fig. 1 caption lines 2384–2385); expert evaluations are "subjective... not objective ground truth" (line 830).
- Wet-lab AML experiments are a **viability check / initial biological validation**, deliberately simple methodology; not a replacement for preclinical/clinical validation; in vitro efficacy does not guarantee in vivo/clinical success (lines 884–890, 1241–1252).
- Validation overall "remains preliminary" (lines 1632–1633); small evaluation scale → "further studies necessary for any reliable conclusions" (lines 843–844).
- Knowledge constrained to **open-access literature** (paywall omissions, lack of negative results); risk of propagating erroneous/irreproducible findings (lines 1621–1629).
- Inherits underlying-model limits: imperfect factuality, potential hallucinations (lines 1630–1631).
- Risks: diminished critical thinking, homogenized research, worsening reproducibility crisis without peer review/guardrails (lines 1634–1643).
- No statistical methods predetermined sample sizes; n=3 based on standard practice, not power analysis (lines 2236–2246).

## Does NOT claim / boundaries
- **Not** a closed-loop autonomous lab — integration with lab-automation platforms is stated as **future work** ("In the fullness of time...", lines 1659–1661).
- **Not** a fully autonomous scientist replacing humans — explicitly "augment, rather than replace, human scientific reasoning" (lines 1639–1640); designed for a "scientist-in-the-loop" collaborative paradigm (lines 359–364).
- **No RL / fine-tuning / back-propagation** used for the self-improvement loop — learning is via meta-review feedback appended to prompts (lines 1935–1941); RL from human/experimental feedback listed as future work (lines 1650–1653).
- Wet-lab / experiments performed by human experts and collaborators, **not** by the system autonomously.
- AMR result is a **recapitulation** of an independent discovery, not a system-run wet-lab validation.
- No in vivo, no clinical trials, no human-subjects data (Reporting summary: sex/gender/ethics all N/A).

## Section map
- **Abstract** (p.487) — multi-agent Gemini system; generate/critique/refine; test-time compute; tournament evolution; three biomedical validations incl. AML in vitro.
- **Introduction** (p.487–489) — breadth/depth conundrum; system overview; three validation areas; Fig. 1.
- **Key contributions** (p.489) — (i) Introducing Co-Scientist; (ii) test-time compute scaling; (iii) expert-in-the-loop; (iv) end-to-end biomedical validation.
- **Co-Scientist overview** (p.489) — 5 default criteria; 4 components; Table 1.
- **System analysis and evaluation** (p.490–492) — Agent ablation; Scaling test-time compute (203/15 goals, Fig. 2a,b); Expert evaluation (11 goals, Fig. 2c); LLM-as-judge.
- **Real-world validations** (p.492–495) — Drug repurposing; AML wet-lab; single-agent candidates (KIRA6); synergistic combinations (Fig. 4); clinical translation design; liver fibrosis; AMR recapitulation.
- **Discussion** (p.495) — model-agnostic; limitations; future directions.
- **Conclusion** (p.495–496).
- **Methods** (p.496 onward) — architecture; research-plan config; each specialized agent in detail; expert-in-the-loop; tool use (incl. AlphaFold, Supp. Note 11); ablation; statistics; data/code availability.
- **Extended Data** — Figs. 1–6 (AI-augmented expertise, LLM preference ranking, binimetinib/other cell lines, low-effect drugs, dual & triple combination synergy); Tables 1–2 (IC50s; combination synergy summary).
- **Reporting summary** — statistics, software, human-data (all N/A), dual-use (all "No").
