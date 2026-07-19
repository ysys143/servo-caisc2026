# Digest: sparkes2010robot

**Full citation (from paper):** Sparkes A, Aubrey W, Byrne E, Clare A, Khan MN, Liakata M, Markham M, Rowland J, Soldatova LN, Whelan KE, Young M, King RD. "Towards Robot Scientists for autonomous scientific discovery." *Automated Experimentation* 2010, 2:1. doi:10.1186/1759-4499-2-1. Received 14 July 2009; Accepted/Published 4 January 2010.

**Article type:** REVIEW (labeled "REVIEW" / "Review" on p.1, lines 6, 10, 29). This is a *review/description* paper by the Robot Scientist group, NOT the primary results paper. Adam's actual discovery results were published in King et al. 2009 *Science* "The Automation of Science" (ref [24]) and the original Robot Scientist in King et al. 2004 *Nature* (ref [23]); this paper reviews/summarizes them.

---

## Thesis / problem

Reviews "the main components of autonomous scientific discovery, and how they lead to the concept of a Robot Scientist" — a system that "uses techniques from artificial intelligence to automate all aspects of the scientific discovery process." Describes the group's two prototype Robot Scientists, Adam and Eve. Argues that (a) both physical and intellectual aspects of science should be automated, and (b) the reporting of science should be "fully formalised" (logic-based) to make it reproducible/reusable. Adam is presented as proof-of-potential; Eve is still under development.

---

## Method: what Adam actually does

**(a) Scientific DOMAIN — YES, yeast functional genomics.** Adam does microbial growth experiments to "study functional genomics in the yeast *Saccharomyces cerevisiae*, specifically to identify the genes encoding 'locally orphan enzymes'" (lines 191-193). A locally orphan enzyme = an enzyme known to exist in an organism but whose corresponding gene is unidentified (definition distinct from Pouliot & Karp's "orphan enzyme," lines 193-196). Adam identified twelve genes responsible for catalysing specific reactions in the metabolic pathways of *S. cerevisiae* (abstract, lines 20-22).

**(b) Hypothesis generation + robotic experimentation + statistical validation — YES, all three (full closed loop).**
- *Hypothesis generation:* abductive (line 206). Uses a logical model of yeast metabolism (based on the Förster iFF708 model, written in Prolog) + KEGG bioinformatic database + homology search (PSI-BLAST and FASTA) to hypothesise candidate genes (ORFs) encoding locally orphan enzymes (lines 200-206, 289-296). Two levels of hypothesis: (1) `encodesORFtoEC(ORF, E.C.)`; (2) `affectsgrowth(compound, deletant)` derived by logical inference (lines 206-221). Adam's *early* work used Inductive Logic Programming (C-Progol 5) in a restricted form of Abductive Logic Programming, for aromatic amino acid metabolism (lines 281-288).
- *Robotic experimentation:* designs two-factor experiments (deletant strains ± metabolites vs wild-type controls), uses Latin-square microplate design to detect small differences above noise, executes on a laboratory robotic system with three robotic arms (lines 223-228, 251, 364-368).
- *Statistical validation:* growth curves (optical density) fitted/smoothed/de-noised with cubic splines; biologically significant parameters (growth rate, lag time) extracted; multiple replicates analysed by machine learning — **random forests** [30] — "to obtain statistically significant results that can be used to either confirm or refute hypotheses" (lines 372-378). Knowledge then updates the system model; cycle repeats.

**(c) ACTIVE-LEARNING / experiment-selection policy — NOT present / NOT emphasized in THIS paper.** The paper never uses the term "active learning." It describes the loop as "hypothesis-driven closed-loop learning" (Figure 1) — generate hypotheses, design experiments to test them, run, analyse, update model, repeat. Adam's experiment design is a fixed two-factor / Latin-square assay design to *test* generated hypotheses (lines 223-228, 364-368); there is NO description of a cost-minimizing or entropy/information-gain experiment-SELECTION policy for choosing which hypothesis/experiment to run next. (Note: the well-known active-learning / cost-minimizing experiment selection is a feature of the earlier King et al. 2004 *Nature* Robot Scientist work [ref 23], but it is NOT described or emphasized in the body of this 2010 review.) The closest thing to experiment selection is for **Eve** (still under development): ML+QSAR "generate hypotheses about what it considers would be useful compounds to test next" and iteratively cycle testing compounds (lines 452-462) — a targeted/greedy screening strategy, again not labeled "active learning."

**(d) Autonomy / closed-loop claim + timeframe.** Adam is "intended to be fully automated, with human intervention required only to supply library strain stocks and consumables" (lines 276-278). Explicitly framed as "closed-loop learning" (lines 37-40, 151-154, Figure 1). Adam physically commissioned "at the end of 2005" (lines 189-190). Eve physically commissioned "in the early part of 2009" (line 441), both software and biological assays still under development. Paper argues for the term "Robot Scientist" (over "Laboratory Assistant") because Adam "has discovered new knowledge about gene function in S. cerevisiae that has been independently verified" (lines 644-647).

---

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| Twelve genes identified | Abstract L20-22; L386 | Genes responsible for catalysing specific reactions in metabolic pathways of yeast S. cerevisiae |
| 20 hypotheses | L384-385 | Adam conceived 20 hypotheses concerning identity of genes encoding 13 locally orphan enzymes |
| 13 locally orphan enzymes | L384-385 | Target enzymes for the 20 hypotheses |
| 12 confirmed | L386 | Adam tested all 20 hypotheses, confirmed correctness of 12 "with a high degree of confidence" [ref 24] |
| 3 verified by manual experiments | L386-387 | Conventional manual biological experiments verified 3 of the 12 conclusions |
| 6 further supported by literature | L392-393 | Additional literature searches revealed evidence supporting a further 6 |
| 1 incorrect conclusion | L401-403 | Adam wrong on one of original 20 hypotheses (gene YIL033C predicted glutaminase; actually cAMP-dependent protein kinase subunit) — highlights weakness (model does not represent kinase control) |
| 11 metabolites | L406-407 | Assays Adam performed to confirm glutaminase activity of YIL033C deletant |
| Adam commissioned end of 2005 | L189-190 | Physical commissioning |
| Up to 1000 experiments/day | L256 | Adam's experiment-creation throughput |
| ~4 days | L257 | Typical experiment duration |
| 595 nm | L259 | Optical density measurement wavelength (proxy for cellular growth) |
| Two microtitre plate readers | L260 | Molecular Devices Spectramax 190 (Fig 3 item 9) |
| Three robotic arms | L251 | Serve Adam's automated instruments (2× Caliper Twister II + IAI Scara) |
| Cubic splines | L373 | Fit/smooth/de-noise growth curves |
| Random forests [30] | L375 | ML for statistically significant confirm/refute of hypotheses |
| MySQL | L381 | Custom relational database storing all data + meta-data |
| Forster iFF708 model | L201-202 | Basis of Adam's logical yeast-metabolism model (Prolog) |
| KEGG | L202-203, L355 | Bioinformatic/genome database used for hypotheses |
| PSI-BLAST, FASTA | L204, L359 | Homology / sequence-similarity search techniques |
| C-Progol 5 [27,28] | L281-282 | ILP program used in Adam's EARLY work (aromatic amino acid metabolism) |
| LABORS: 10 levels deep, >10,000 research elements | L431 | Nested tree structure formalising Adam's investigations; expressed in Datalog [36]; publicly available |
| EXPO, LABORS, EXACT | L418-423 | Ontologies (EXPO generic → LABORS custom for Adam; EXACT for experimental actions) |
| Joined OBI consortium Oct 2008 | L428 | LABORS aligned with OBI representations |
| Eve commissioned early 2009 | L441 | Physical commissioning; software + assays still under development |
| >10,000 compounds/day | L443 | Eve's compound-screening throughput |
| 14,400 compounds | L466, L472 | Maybridge "Hitfinder" library Eve will use |
| Rule of five → 200,000; then → 14,400 | L469-472 | Two-stage filtering (Lipinski's rule of five [38], then Pharmacophore Fingerprinting [39] + cluster analysis) to build Hitfinder library |
| QSAR [37] | L446-448 | Quantitative structure-activity relationship, to be integrated into Eve's drug screen |
| Not cost-effective vs humans (currently) | L707-708 | Authors explicitly say they "would not currently consider them to be 'cost-effective' in comparison to human scientists" |
| Adam robotic system inventory | Fig 3, L342-351 | Liconic STR602 freezer; Caliper Presto & Sciclone i1000 liquid handlers; Thermo 384 multidrop; 2× Caliper Twister II arms; Bio-Tek ELx405 washer; Agilent VSpin centrifuge; 3× Liconic STX40 incubators; 2× Spectramax 190 readers; Variomag shaker; IAI Scara arm; 2 plate slides; 2 HEPA filters; enclosure; 4 control computers + networked server |
| Eve robotic system inventory | Fig 5, L583-592 | Labcyte Echo 550 acoustic liquid handler; BMG Pherastar & Polarstar readers; MDS ImageXpress Micro imager; Cytomat incubator/dry store; 2× Mitsubishi arms; Agilent Bravo; Thermo Combi multidrops; etc.; 2 computers + server |
| Eve physically connected to Adam | L515-517 | Linear track slide allows microtitre plate transfer in either direction |

---

## Scope & explicit limitations (stated by authors)

- Systems are "still just prototypes" (L641); future hardware/software will increase their independence.
- Adam's system model "does not represent kinase control mechanisms," causing the one incorrect conclusion (YIL033C) (L409-411, L676).
- Robot Scientist relies on publicly available databases and is susceptible to errors therein (same as human scientists) (L661-671). Mitigation for Adam: primarily used only ONE public database (KEGG) and manually updated the model where conflicts were noticed before automated hypothesis generation (L672-674).
- Data-analysis algorithms may be less able to handle experimental-measurement flaws than a human; physical issues (plastic-ware flaws, instrument faults, plate misplacement) currently easier for a human to notice (L680-703).
- NOT cost-effective vs humans currently (L704-714).
- Eve: software and biological assays "still under development"; Eve's capabilities described in future tense ("Eve will...") (L442-462, L521-543). Eve's compound library "not a large... library by industrial standards"; aim is "proof-of-principle" (L472-476).

---

## Does NOT claim / boundaries (important for citation audit)

- **Does NOT frame a "six-component" discovery system.** The paper reviews "the main components of autonomous scientific discovery" and enumerates ~5 elements (L32-40): computer-controlled instruments; integrated robotic automation; a computational model of the object of study; AI/ML to create hypotheses & interpret results (closed-loop learning); formalisation of the discovery process. The cycle is described as 4-5 stages (generate hypotheses → design experiments → run physical experiments → analyse/interpret → repeat). There is no enumerated "six-component" framework; a citation asserting this paper instantiates a "full six-component discovery system" would be an overstatement/mismatch.
- **Does NOT emphasize active learning.** No use of the term "active learning"; no description of a cost/information-gain experiment-SELECTION policy in this paper (see (c) above). Attribute active-learning experiment selection to King et al. 2004 *Nature* [ref 23], not to this review.
- This is a **review/description** paper — the quantitative discovery result (12 genes) is attributed here to King et al. 2009 *Science* [ref 24]. Adam's discovery is described, not newly reported.
- Does not claim general-purpose scientific discovery: Adam is domain-specific (yeast metabolism); Eve is domain-specific (drug screening / chemical genetics), still under development.
- Does not claim human-level innovation/serendipity: acknowledges "the underlying artificial intelligence components fail to meet human expectations for innovative thought" (L656-657).

---

## Section map

1. **Abstract** (L15-28) — reviews components, introduces Adam & Eve, 12-gene result claim, formalisation argument.
2. **Review: Towards the full automation of scientific discovery** (L29-159) — history of AI-in-discovery systems (DENDRAL/Meta-DENDRAL, AM/EURISKO, KEKADA, BACON/ABACUS/Fahrenheit/IDS, Schmidt-Lipson natural-laws); closed-loop learning; deduction/induction/abduction; formal recording of data.
3. **The Robot Scientist concept** (L160-181) — definition; Figure 1 (hypothesis-driven closed-loop learning).
4. **Robot Scientist prototypes** (L182-186) — Adam (proven) & Eve (under development).
5. **A Robot Scientist to study yeast metabolism — 'Adam'** (L187-438) — subsections: domain/locally-orphan-enzymes, hypothesis levels, robotic system (Fig 2, Fig 3), software (C-Progol 5, bioinformatics method steps 1-4, cubic splines, random forests, MySQL), **Adam's results** (20 hyp / 12 confirmed / YIL033C error), **Formalisation** (EXPO/LABORS/EXACT, OBI, Datalog).
6. **A Robot Scientist to study chemical genetics and drug design — 'Eve'** (L439-604) — goal (ML+QSAR drug screen), Hitfinder library, robotic system (Fig 4, Fig 5), three-stage software (mass screening / hit verification / targeted screening), formalisation.
7. **The Future** (L616-635, note: interleaved with Discussion in text order) — Adam+Eve working together (yeast, bacteria, C. elegans).
8. **Discussion** (L618-714) — "Laboratory Assistant" vs "Scientist"; serendipity/innovation; database errors; data-analysis flaws; costs.
9. **Conclusions** (L716-724) — Robot Scientists automate all aspects of discovery; reproducibility.
10. **Appendix** (L725-746) — URLs & instrument vendor notes 1-10.
11. **References** (L839-956) — 39 references.
