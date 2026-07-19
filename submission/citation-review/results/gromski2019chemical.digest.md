# Digest: gromski2019chemical (BLIND first-pass)

**Full title:** "How to explore chemical space using algorithms and automation"
**Authors:** Piotr S. Gromski, Alon B. Henson, Jarosław M. Granda, Leroy Cronin (WestCHEM, School of Chemistry, University of Glasgow)
**Venue:** Nature Reviews Chemistry — PERSPECTIVE (opinion/review article, not primary research)
**DOI:** 10.1038/s41570-018-0066-y (published 2019)

---

## Thesis / Problem

Extending the reactivity of a *given* class of molecules is relatively straightforward; the discovery of **genuinely new (novel) reactivity** and the molecules that result is a wholly more challenging problem. The authors define **novel** = a reaction/outcome that is *unpredictable* using current chemical knowledge (an "outlier" relative to prediction), as distinct from merely "new" (not previously observed).

Central claim: **Searching chemical space using automation AND algorithms improves the probability of discovery.** The two levers are treated as complementary:
- **Automation** enables routine chemical tasks to be performed more quickly, consistently, with less manual labour and lower variability, and lets each operation be logged/linked to results (reproducibility, archiving).
- **Algorithms** facilitate searching of chemical knowledge databases and, more generally, use ML/statistical modelling to predict the chemistry under investigation.

They propose a **"chemical intelligence" / chemical artificial intelligence (CAI)** vision: automated chemical reactor systems controlled by algorithms and monitored by a **sensor array**, navigating chemical space more quickly, efficiently, and *without bias*, yielding not just new molecules but unpredictable (novel) reactivity. The framing goal is to "replace serendipity with certainty."

---

## Method / Structure of the argument

This is a conceptual Perspective, not an experiment. It builds a vocabulary and framework:
- **Chemical space** = entire universe of known+unknown molecules + the transformations connecting them (a network of reactions). It is **large and sparse** (some regions dense clusters, others nearly empty).
- **Mapping / utility function** = simplifies raw measured data into comparable values (e.g., molecular weight, change in IR peak intensity, UV/vis wavelength shift) to turn "chemical space" into a searchable "search space."
- Two search avenues: **theoretical** (searching databases/knowledge graphs) and **experimental** (physically running reactions).
- Two families of search algorithm: **instance-based** (simulated annealing, genetic algorithms, particle swarm optimization — pick next experiment from prior data) and **model-based** (build a model of the space; DoE designs, SVM, self-organizing maps, kriging, random forest).
- Three-step programmable **novelty test** (Fig 6): repeatable? → observed previously? → predictable? → novel.

### IMPORTANT — physical characterization (NMR, MS) and the physical loop

**YES, the paper is emphatically about the physical execution loop, not just in-silico search.** Key evidence:

1. **Chemistry as inherently physical/costly.** "The expansion of chemical knowledge by searching for new molecules and chemical reactions is an inherently practical endeavour" (l.29-31). "chemistry costs both time and physical resources, resulting in a limit on the number of experiments that can be conducted and the speed at which they can be safely performed" (l.95-99). This "reaction budget" is a recurring justification.

2. **Physical characterization instruments are the mapping function / feedback.** The measured outputs come from real analytical instruments physically executed on real reactions:
   - **NMR** — real-time in-line NMR spectroscopy cited as enabling "real-time chemistry" (ref 8, Sans/Cronin, self-optimizing organic reactor via in-line NMR; cited at l.62 "coupled with real-time chemistry").
   - **GC–MS** — MacMillan/Hartwig random-search workflow: "the potential coupling for each reaction is estimated on the basis of gas chromatography–mass spectrometry (GC–MS) measurements"; "GC–MS hits — Peaks of significant intensity and molecular weight indicate new bond formation" (Fig 3b, l.708-713, 872-873, 889).
   - **LC/MS/ELS** — Beeler et al. workflow: "liquid chromatography/mass spectrometry/electrophoretic light scattering (LC/MS/ELS) screening, structure elucidation and reaction optimization" (l.855-857).
   - **UV/vis, IR** — used as mapping-function probes (IR peak intensity change, UV/vis peak wavelength shift; l.134-141); "Instruments: UV/vis, IR, etc." listed on the control side (Fig 4b, l.1153).
   - **Luminescence/fluorescence quenching** — Glorius mechanism-based screening (Fig 1b).
   - **In-line spectrometer** — Krishnadasan nanoparticle platform monitors emission spectra (l.1442-1443).
   - **HPLC** — ChemOS autonomously calibrating HPLC analysis (l.1463-1465).

3. **The "two separate worlds" statement (strongest).** Fig 4b: "Closed-loop robots work across two separate worlds. The control uses different operations needed to perform the desired reactions, such as fluid handling, measuring instruments and sensors, and communication and device-level control. **The search algorithm operates entirely in silico** with data from both a priori knowledge... and the live database of current experimental results" (l.1290-1297). I.e., the algorithm is in silico, but it is coupled to and depends on a *physical control side* (pumps, valves, actuators, containers, sensors, instruments) that physically runs reactions and takes measurements. Listed control-side hardware: "Fluid handling, actuators (pumps, valves); Containers (batch/flow, single/multiple); Sensors (cameras, scales, etc.); Chemical operations (distillation, separation, etc.)" (l.1157-1176).

4. **Automation explicitly required to feed the models.** "To gather sufficient experimental data to create good models, it is useful to use automation" (l.1310-1312). Section "Automating the search": automation reduces manual labour/time for reaction preparation and work-up, decreases variability, and enables logging of exact operations linked to results (l.1314-1332).

So the paper does argue chemistry needs **both** automation (to physically execute + measure) and algorithms (to search/decide) for a closed physical loop. It does not phrase it as "NMR/MS *require* physical execution" in those exact words, but the entire architecture presumes physical experiments whose products are physically characterized by these instruments and fed back to an in-silico algorithm.

---

## FACTS TABLE (exhaustive)

| Value / claim | Location | Context |
|---|---|---|
| Glorius mechanism-based screening discovered **two** promising substrate classes after screening only **100 compounds** | l.287-289, 307 | fluorescence/luminescence-quenching used as mapping function (Fig 1b); ref 18 |
| Quenchers identified incl. **1H-benzotriazole** and **4-methoxyphenol** | l.310-311 | Glorius example |
| High-throughput virtual screening narrowed **1.6 million** possible molecules → **thousands** of promising novel OLED molecules, then synthesized new OLEDs | l.480-485 | Aspuru-Guzik / Gómez-Bombarelli; ref 28 (Nat. Mater. 15, 1120-1127, 2016) |
| MacMillan "accelerated serendipity" random search → discovery of a **new C–H arylation reaction** | l.845, 901-902 | ref 32 (McNally, Prier, MacMillan, Science 334, 1114-1117, 2011) |
| Photocatalysed α-aminocyanobenzene coupling product hit at **11% yield** | Fig 3b, l.727 | MacMillan workflow example |
| Ir(ppy)2(dtbpy)PF6 photocatalyst; Na2CO3, DMF, 23 °C, 26 W lamp | Fig 3b, l.691, 721-722 | MacMillan workflow conditions |
| Santanilla nanomole-scale HTE: **more than 1,500** experiments using as little as **0.02 mg** of material | l.1361-1362 | ref 23 (Santanilla et al., Science 347, 49-53, 2015) |
| Heat map: **1,536** [Pd]-catalysed coupling reactions | Fig 4a, l.962, 1289 | Santanilla HTE |
| Reaction matrix: **6 bases · 8 nucleophiles · 8 catalysts · 4 electrophiles** | Fig 4a, l.1025-1027 | Santanilla design |
| Example transformation: **57% yield, 25 mg scale, DMSO, rt** | Fig 4a, l.1085-1087 | Santanilla scale-up |
| SVM model (trained on historical reactions + physicochemical descriptors) predicted crystallization outcomes and **outperformed human experimenters** | l.1242-1247 | Raccuglia vanadium selenites (Fig 3c); ref 47 (Nature 533, 73-76, 2016) |
| Random forest ensemble substantially outperformed linear regression for yield prediction (Buchwald–Hartwig amination) | l.1259-1272 | Doyle; ref 50 (Ahneman et al., Science 360, 186-190, 2018) |
| Deep reinforcement learning w/ recurrent neural networks **outperformed current optimization algorithms** | l.931-937 | ref 42 (Zhou, Li, Zare, ACS Cent. Sci. 3, 1337-1344, 2017) |
| Knowledge-graph representation **G = (M, R, E)**: M molecular nodes, R reaction nodes, E directed reaction edges | Fig 3a, l.867-868 | Segler & Waller; ref 29 |
| Retrosynthesis automated via **deep neural networks + symbolic AI**, trained on ~all known organic chemistry | l.826-833 | Segler/Preuss/Waller; ref 31 (Nature 555, 604-610, 2018) |
| Burke MIDA-boronate platform = **three modules**: deprotection, coupling, purification | l.1390-1391 | ref 56 (Li et al., Science 347, 1221-1226, 2015) |
| Krishnadasan nanoparticle platform: microfluidic reactor + in-line spectrometer; mapping fn = **"dissatisfaction coefficient"** (0=satisfaction, 1=dissatisfaction); algorithm = **SNOBFIT** | l.1441-1455 | ref 61 |
| ChemOS: portable/modular software framework for closed-loop systems; learned dye colour space; autonomously calibrated HPLC | l.1456-1465 | Aspuru-Guzik; ref 62 (Roch et al., Sci. Robot. 3, eaat5559, 2018) |
| "No free lunch theorem": no single algorithm optimal for all problems | l.1203-1208 | ref 46 (Wolpert & Macready, 1997) |
| Model-based DoE designs listed: two-level factorial, Plackett–Burman, full factorial, Box–Behnken, Doehlert | l.974-1199 | search-algorithm taxonomy |
| Model-building algorithms listed: SVM, self-organizing maps, kriging, random forest | l.1210-1272 | search-algorithm taxonomy |
| Three discovery categories in order of impact: new reactivity > new reactions > new molecules | l.1467-1477 | "Uncovering novelty" |
| Three-step novelty test: repeatable? → observed previously? → predictable? → **novel** | Fig 6, l.1678-1702 | programmable novelty definition |
| CAI = **Chemical Artificial Intelligence** | l.1652-1653 | Conclusions |
| Funding: EPSRC (9 grants) + ERC project 670467 SMART-POM | l.2011-2018 | Acknowledgements |

---

## Scope & limitations (as stated by the paper)

- It is a **Perspective/opinion** piece, not new experimental data — it curates and frames existing work.
- Databases mostly **lack negative results** and give no uncertainty estimate on source data (l.342-347) — a stated limitation for database-driven discovery.
- **Virtual screening cannot predict the unknown** (l.412-413) — a stated boundary distinguishing it from molecular design.
- DoE/model algorithms **cannot be applied as a black box**; require understanding the application/data structure (no free lunch theorem) (l.1200-1208).
- Predictability (hence novelty) is "potentially very difficult to objectively determine"; experts often disagree; the system can only judge novelty "from its internal perspective," so an outcome novel to a platform may not be novel given broader knowledge (l.1544-1557).

## Does NOT claim / boundaries

- Does **not** claim a fully autonomous end-to-end "AI chemist" has been built; it forecasts ("in the not-too-distant future") such systems.
- Does **not** present its own benchmark, dataset, or quantitative comparison — no original results.
- Does **not** address LLMs, agentic AI, or hallucination (predates them; 2019).
- Does **not** argue algorithms alone suffice — repeatedly insists the physical/automation side (running reactions, physical characterization, sensors) is indispensable and coupled to the in-silico search.

## Section map

1. **Abstract** (l.6-27) — thesis: automation + algorithms + sensor array → search chemical space without bias.
2. **Algorithms in chemistry** (l.28-83) — defines algorithm, ML, chemical space; single-parameter optimization vs ML.
3. **[chemical space / mapping function]** (l.84-314) — search space, mapping/utility function, Glorius quenching example (Fig 1).
4. **Building databases** (l.316-485) — virtual screening vs molecular design (Fig 2); chemometrics; OLED example.
5. **Searching chemical space** (l.487-833) — theoretical (knowledge graphs, retrosynthesis; Fig 3a) vs experimental; random search / accelerated serendipity (Fig 3b); ML crystallization (Fig 3c).
6. **[instance-based vs model-based algorithms]** (l.834-1312) — algorithm taxonomy, DoE, SVM/SOM/kriging/random forest, Pd HTE (Fig 4a), closed-loop two-worlds (Fig 4b).
7. **Automating the search** (l.1314-1465) — automation rationale; Santanilla HTE, Burke MIDA, flow synthesis, Krishnadasan nanoparticles, ChemOS.
8. **Uncovering novelty** (l.1467-1613) — outlier-based novelty definition; three-step test (Fig 5, Fig 6).
9. **Conclusions** (l.1615-1677) — CAI, "replace serendipity with certainty."
10. **References** (65), acknowledgements, author contributions.
