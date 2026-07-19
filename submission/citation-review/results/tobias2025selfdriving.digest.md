# Digest: tobias2025selfdriving

**Full cite:** Tobias AV, Wahab A. 2025. Autonomous 'self-driving' laboratories: a review of technology and policy implications. *R. Soc. Open Sci.* 12: 250646. DOI 10.1098/rsos.250646. Received 30 Mar 2025; accepted 16 Jun 2025.
**Authors/affil:** Alexander V. Tobias & Adam Wahab, Dept of Biotechnology and Life Sciences, The MITRE Corporation, McLean, VA, USA.
**Funding:** MITRE Independent Research and Development Program. **AI-use declaration:** "We have not used AI-assisted technologies in creating this article."
**Type:** Review article (invited "Review", Subject Category: Science, society and policy).

---

## Thesis / problem

A review-and-perspective on **self-driving laboratories (SDLs)** — systems that combine AI with laboratory automation to perform research in chemistry, materials science, and biology, in some cases automating "nearly the entire scientific method" (hypothesis generation → design → execution → analysis → conclusions → updated hypotheses). The paper couples a **technology survey** (types, autonomy levels, worked examples across three domains + cloud labs + implementation costs) with an extended **policy/societal analysis** (intellectual property, safety & security, labour-force impact).

**Load-bearing framing (IMPORTANT for audit):** The paper's central intellectual claim is that **software autonomy — not hardware — is "preeminent."** It argues laboratory robots "almost never perform tasks that would be outright impossible for a human laboratory worker," so "progress in chemistry, materials or biology is most impacted by the intellectual content of experiments" (§2.1). In §6 it reinforces this via **Moravec's paradox**: robotics/hardware for lab automation falls in the "easy for humans" category, whereas the intellectual/software side is where AI's strength and the transformative potential lie. It also calls optimization experiments (the dominant SDL use) "low-hanging fruit."

**Self-declared scope limit:** "This report is **not** intended to serve as a comprehensive review of the SDL field. For that, we recommend the review by Tom et al. [6]." (§1) It focuses on "influential developments and contemporary issues."

## Method

Narrative literature review + subject-matter-expert interviews (acknowledged: Gomes/CMU, Ross King/Cambridge & Chalmers, Garcia Martin/LBNL, Padmanabhan Esq., Romero/Duke, Wadsworth Esq.). No new experiments or quantitative meta-analysis. Draws on two published autonomy-classification schemes (a 1-D SAE-analogy scale [8]; a 2-D hardware×software scale from Tom et al. [6]).

---

## Direct answer to the IMPORTANT question

**Is it a REVIEW of SDL TECHNOLOGY that documents the RAPID MATURATION of the underlying HARDWARE (and policy implications)?**

- **REVIEW of SDL technology + policy implications** — YES. Technology survey (§2) plus substantial policy chapters on IP (§3), safety/security (§4), and labour (§5).
- **"Rapid maturation of the underlying HARDWARE"** — **This characterization is NOT what the paper emphasizes, and is partly contrary to its argument.** (a) The paper explicitly ranks **software/intellectual autonomy as "preeminent"** and repeatedly **de-emphasizes hardware** ("robots almost never perform tasks impossible for a human"; hardware tasks are "easy for humans" per Moravec's paradox). (b) The developmental arc it presents is **decades-long, not rapid**: first HPLC-separation SDL 1982 [20], first reaction-optimization chemistry SDL 1988 [19], DENDRAL 1960s–70s, an "AI winter" through the 1990s, Adam 2009 — with recent acceleration attributed largely to the **AI/LLM wave (ChatGPT 2022)**, i.e. software, not hardware. (c) It does describe hardware advances (mobile robotic chemist, A-Lab's three stations, six-axis arms, 150-instrument platforms), but as instances within a broader survey, not as the organizing thesis. A manuscript citing this paper for a claim that it "documents rapid hardware maturation" would be **mischaracterizing** its emphasis.

---

## FACTS TABLE (exhaustive)

### Autonomy classification
| value | location | context |
|---|---|---|
| Level 1 "assisted operation" | §2.1 / Table 1 | machine assistance w/ lab tasks (liquid handlers, data-analysis SW) |
| Level 2 "partial autonomy" | §2.1 / Table 1 | ≥1 "intellectual" aspect automated; e.g. predictive ML or dynamic workflow planner Aquarium [11] |
| Level 3 "conditional autonomy" | §2.1 / Table 1 | **minimum to qualify as an SDL**; autonomous ≥1 cycle of scientific method; human intervention only for anomalies. Ex: iBioFab [12], Mobile Robot Chemist [13] |
| Level 4 "high autonomy" | §2.1 / Table 1 | hypothesis tester automating protocol gen/execution/analysis/hypothesis adjustment. Ex: Adam [14], Eve [15], MicroCycle [16] |
| "To date, Level 4 is the maximal autonomy reached by SDLs" | §2.1 | current ceiling claim |
| Level 5 "full autonomy (AI researcher)" = "not yet achieved / has not yet been realized" | §2.1 / Table 1 | speculative top level |
| 2-D scheme [6]: hardware autonomy Levels 0–3; software autonomy by closed-loop cycles + who sets search-space/experiment-selection | §2.1 / Table 2 | Level-4 SDL must be ≥L2 in both dims; Level-5 must be L3 in both |
| SAE J3016 driving-automation taxonomy is the analogy source [7] | §2.1 | autonomy-levels borrowed from self-driving cars |

### Chemistry SDLs (§2.2 + Table 3)
| value | location | context |
|---|---|---|
| DENDRAL, Stanford, 1960s [17] | §2.2 | "first example of ML software capable of scientific hypothesis formation"; predicted chemical structures from mass-spec |
| Meta-DENDRAL, 1970s [18] | §2.2 | added "closed-loop learning"; learned bond-breaking heuristics |
| First published chemistry SDL for reaction optimization = **1988** [19] | §2.2 | robotic arm + UV-vis spectrophotometer; optimized phosphotungstic-acid + drug reactions; "meets the criteria for Level-3 autonomy" |
| First Level-3 SDL for post-reaction chemical separation = **1982** [20] | §2.2 | used HPLC; auto-adjusted mobile-phase solvent mix |
| "AI winter" through the 1990s [21] | §2.2 | decline in SDL research |
| Univ. of Liverpool solid-state synthesis SDL [22] | §2.2 | three multipurpose robots orchestrated by "ARChemist" SW; **only one experimental cycle** (proof-of-principle) |
| **A-Lab** (Lawrence Berkeley Nat. Lab) [23] | §2.2 | Level-4; solid-state synth of inorganic powders; literature data + ML + active learning; proposes **up to five** synthesis routes/target; **three integrated stations**; uses Materials Project [24] |
| **A-Lab success rate = "71−74% of the target materials it was presented"** | §2.2 | headline A-Lab statistic |
| RoboRXN (IBM) [25] | §2.2→§2.3 wrap | cloud computing + AI + commercial automation; literature→knowledge-graph; discovered sulfonium photoacid generators via retrosynthesis; "Level-3 software autonomy" |
| Jensen lab, MIT SDL [26] | §2.2 | closed-loop molecular discovery; custom "Master Control Network (MCN)"; optimizes λ-max absorption, lipophilicity, photo-oxidative degradation rate |
| 2007 [27] | Table 3 | "early example (2007) of a modern closed-loop SDL"; CdSe nanoparticles; chip continuous-flow microreactor + online fluorescence; "dissatisfaction coefficient" scalar minimized |
| 2022 [28] | Table 3 | Suzuki–Miyaura coupling; sampled **11 substrate pairs, 7 catalysts, 3 solvents, 2 bases, 2 temperatures**; manual reagent dispensing/post-analysis |
| 2018 [29] | Table 3 | mobile organic-synthesis robot "inspired by human chemical intuition"; ML predicts Suzuki–Miyaura reactivity |
| Mobile Robot Chemist, 2020 [13] | Table 3 | dexterous mobile robot; improved photocatalysts for H₂ from water; **"performed 688 experiments in 8 days"**; batched Bayesian optimization w/o chemical-theory model |
| Synbot, 2023 [30] | Table 3 | "especially large (**9.35 × 6.65 m**)" SDL; three SW layers (AI / robot-software / robotic) |

### Materials science SDLs (§2.3 + Table 4)
| value | location | context |
|---|---|---|
| "Approximately **20% of the industrial base and 70% of technical innovations** rely on advanced materials" [32] | §2.3 | motivation stat |
| Materials Genome Initiative (US) [33]; European Advanced Materials 2030 Initiative [34] | §2.3 | national/multinational programs |
| MAPs function as "Level-3 or higher SDLs" [35] | §2.3 | materials acceleration platforms defn |
| **Ada** (Berlinguette lab, UBC) [39] | §2.3 | thin-film MAP; enhanced hole mobility of organic material for perovskite solar cells; Bayesian optimization; "first MAP to autonomously optimize composition and processing parameters for thin films" |
| Ada upgrade [40] | §2.3 | added six-axis robotic arm + multi-objective ML; palladium thin films; "new synthesis conditions **more than 50°C below** the prior state of the art" |
| **AMANDA** (Univ. Erlangen-Nuremberg) [41] | §2.3 | distributed hub-and-spoke MAP; LineOne MAP "composed of **150 automated instruments spanning 37 different device types**" |
| Distributed organic-laser-emitter SDL [42] | §2.3 | "at least **nine institutions across three continents**"; central AI coordinated **five SDLs**; "discovering **21 new organic solid-state materials** with state-of-the-art laser performance" |
| Battery-electrolyte distributed MAP [43] | §2.3 | "Research groups in **five countries**"; FINALES brokering SW; sites DTU, SINTEF (Norway), EPFL (Switzerland), Dassault Systèmes (UK & Germany), Helmholtz Inst. Ulm (Germany); "exposing laboratories as a service" |
| 3D-printer MAP, 2021 [36] | Table 4 | "first three-dimensional printer-based MAP"; syringe extruder + in-line machine vision; modulated **four** printing params (prime delay, print speed, x-position, y-position) |
| Adhesive-materials MAP, 2022 [37] | Table 4 | semi-autonomous (needs human intervention); four-axis arm; Bayesian optimization of epoxy base-to-accelerant ratio |
| Perovskite-crystal MAP, 2020 [38] | Table 4 | discovered novel chiral perovskite crystals; **reinforcement learning**; workcell→SDL→remote-access evolution; "sophisticated security layer" |

### Biology SDLs (§2.4 + Table 5)
| value | location | context |
|---|---|---|
| AlphaFold [44] | §2.4 | cited as AI-for-biology exemplar |
| **Adam** [14], 2009, Ross King (Aberystwyth + Cambridge) | §2.4 | "first example of a biology SDL"; cultured yeast, generated own functional-genomics hypotheses; "**successfully identified three genes encoding an orphan enzyme involved in lysine biosynthesis**" |
| Bernard Dixon caveat (Current Biology) [49] | §2.4 | Adam's conclusions "predicated on being provided an accurate and extensive biological model" |
| **Eve** [15], 2015, Ross King multi-institute | §2.4 | Level-4; targeted dihydrofolate reductase of malaria parasites (not human enzyme); QSAR-driven; "identified **TNP-470** as a promising lead compound for malaria treatment" |
| **Genesis** [3], under development, King | §2.4 | planned Level-4; "**1000 microbioreactors**"; ~**20,000** yeast strains; thousands of culture conditions; ~**10,000** compounds; measures ~**100 metabolites** & ~**6000 genes** per culture |
| Eve systems-biology proof-of-principle, 2019 [50] | §2.4 | smaller-scale AI-powered model development |
| **SAMPLE** (Romero, then Univ. Wisconsin), 2024 [52] | §2.4 | enzyme-engineering SDL; Gaussian-process model; compared **four** Bayesian-optimization strategies; glycoside hydrolase family 1; "variants **at least 12°C more stable**... by searching **less than 2%** of the full combinatorial landscape" |
| **MicroCycle** (Novartis), 2024 [16] | §2.4 | Level-4 integrated drug-discovery SDL; "perhaps the best-in-class platform" |
| **FutureHouse** (est. late 2023, philanthropy-funded) [53] | §2.4 | AI Scientists for biology; belief they can "increase the experimental and analytical productivity of human scientists by **10- to 100-fold**"; focuses on AI "engine", not end-to-end lab |
| 2021 remote screening SDL [46] | Table 5 | gov lab + corporate collaborator; "required testing only **7%** of the variable combinations"; Bayesian optimization |
| RPE-cell SDL, 2022 [47] (Kanda) | Table 5 | humanoid robot w/ robotic arms; "**88% improved production**"; "tested **143 cell culture conditions in 111 days**" |
| **BioAutomata**, 2019 [12] | Table 5 | microbial strain engineering on iBioFAB [48]; lycopene in *E. coli*; "**Enhanced lycopene production 1.8-fold over 3 cycles from searching less than 1% of the variable space**" |

### Cloud labs (§2.5) & costs (§2.6)
| value | location | context |
|---|---|---|
| Cloud-lab defn: remotely-controlled lab-as-a-service run via executable code [54–57] | §2.5 | terminology reserved narrowly |
| Emerald Cloud Lab throughput "**46 620 versus 8880**" samples/yr (cloud vs traditional) [58] | §2.5 | comparative capacity |
| SAMPLE [52] ran on Strateos cloud lab; Strateos "terminated public subscription-based access... pivoted to private on-premises" [59] | §2.5 | 2nd cloud-lab example is SAMPLE |
| **Coscientist** [60] (Gomes group CMU + Emerald Cloud Lab) | §2.5 | AI chemist; Symbolic Lab Language; "partially based on the **GPT-4** large language model from OpenAI" |
| ECL AI Scientific Advisory Board, 2023 [62] | §2.5 | evidence cloud labs moving toward AI |
| Off-the-shelf/customized commercial systems "upwards of **$1 million USD**" [63] | §2.6 | cost |
| Mass-produced general-purpose robots "as low as approximately **$10 000 USD**" [64] | §2.6 | cost |
| FINDUS liquid-handling workstation "**$400 USD**" [65] | §2.6 | open-hardware cost |
| Jubilee multi-tool gantry "**$100–$2000**" [66] | §2.6 | open-hardware cost |
| Lab setup "**$800K USD** for equipment... annual maintenance **$80K USD**"; cloud-lab subscription "monthly fees starting around **$50K USD**" | §2.6 | comparative economics |
| ChemOS [74], AiiDA [73], ChemCrow [79] | §2.6 | orchestration/planning software examples; ChemCrow = LLM + chemistry tools |

### IP, safety/security, labour
| value | location | context |
|---|---|---|
| Title 35 §101 U.S. Code; "conception" = touchstone of inventorship, only "natural persons" [80,81] | §3.1 | legal basis |
| Major patent offices: AI not eligible for inventorship [82,83]; AI-assisted OK if human made significant contribution to every claim | §3.1 | consensus |
| In-silico evolved antennas, mid-1990s, genetic algorithms [86] | §3.1 | early non-human "invention" |
| **DABUS** (Stephen Thaler): flashlight + container lid; applications rejected; USPTO ruled incomplete, upheld by two U.S. courts [5] | §3.2 | AI-inventorship test case |
| Australian appeals court ruled for Thaler 2021 [87]; **reversed 2022** [88] | §3.2 | jurisdictional flip |
| SDLs = "emerging **dual-use** technology" | §4 | safety/security framing |
| Coscientist supplementary "dual-use study": system "significantly reduces the entry barrier for ill-intentioned low-knowledge actors" [60] | §4.2 | quoted misuse concern |
| HAL 9000 / *2001: A Space Odyssey* (1968) | §4.2 | rhetorical security analogy |
| Anthropic Responsible Scaling Policy [97]; "autonomous replication in the real world" | §4.2 | AI-containment reference |
| "fully **60%** of U.S. employment in 2018 was in job specialties that did not exist in 1940" [103] | §5 | new-work argument |
| BLS 2023: **16,500** chemists (19-2031); **2860** materials scientists (19-2032); **6780** microbiologists (19-1022); **21,120** biochemists/biophysicists (19-1021); total ≈ **48,000** | §5.1 | SDL-relevant workforce size |
| **2,858,710** customer-service reps (43-4051) in 2023 [108] | §5.1 | contrast: far more AI-exposed occupation |
| Acemoglu & Restrepo 2018 [102]; ATM/bank-teller counterexample [110]; Autor et al. automate-vs-augment [101] | §5 / §5.2 | labour-economics scaffold |
| Ross King interview: near term (~**10 years**) SDLs likely "productivity 'force multipliers'" (augmenting > displacing) | §5.2 | expert forecast |
| Moravec's paradox [111]; Mitchell "Why AI is Harder Than We Think" 2021 [21]; optimizations = "low-hanging fruit" | §6 | conclusion themes |

---

## Scope & limitations (self-stated)
- **Not** a comprehensive SDL review; defers to Tom et al. [6] (§1).
- No new empirical work; narrative synthesis + expert interviews.
- Acknowledges "few published accounts of AI-driven experiments performed in cloud labs" (§2.5) — the self-driving-cloud-lab evidence base is thin (essentially SAMPLE [52] and Coscientist [60]).
- Labour analysis limited to U.S. BLS categories; forecasts explicitly "difficult to predict" (§5.2).
- Perspective/opinion content is heavy (recommendations, predictions) alongside review content.

## Does NOT claim / boundaries
- Does NOT claim Level-5 (full AI researcher) SDLs exist — "not yet achieved."
- Does NOT claim hardware is the preeminent or rate-limiting factor — argues the **opposite** (software/intellectual autonomy is preeminent; hardware/robotics tasks are "easy for humans").
- Does NOT claim SDLs will broadly displace scientists — cites evidence of "no broad-based displacement" of high-skill jobs and forecasts augmentation over the near term.
- Does NOT claim AI can currently be a legal inventor — the consensus reported is the reverse.
- Does NOT present the field as newly/suddenly emerged — traces roots to the 1960s–1980s.
- Does NOT report SDL-generated inventions as currently patentable ("We have not yet seen how inventions generated this way can be patented").

## Section map
1. Introduction (scope; defers comprehensive review to Tom et al. [6])
2. Types, examples and significance of SDLs — 2.1 Levels of autonomy · 2.2 Chemistry · 2.3 Materials science · 2.4 Biology · 2.5 Self-driving cloud labs · 2.6 Costs and challenges of SDL implementation
3. Intellectual property considerations — 3.1 Inventorship and conception · 3.2 AI and SDL inventions under the law
4. Safety and security — 4.1 Risks · 4.2 Recommendations for prevention and mitigation
5. Potential impact: labour force — 5.1 Some labour statistics · 5.2 Labour effects are difficult to predict
6. Conclusions
