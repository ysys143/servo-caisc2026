# `robot_scientist` Identity and Frozen System Description Audit

## Lane Scope

- Active source only: `robot_scientist` / `sparkes2010robot`.
- Assigned checks: PDF/BibTeX identity and version, SHA-256, page count, sequential reading of all 11 PDF pages, visual inspection of every figure and the displayed logical predicates, and clause-level assessment of the frozen supplementary description.
- Source PDF: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Reference/Sparkes 2010 - Towards Robot Scientists for Autonomous Scientific Discovery.pdf`.
- No other source PDF was opened. No external model or API was called.

## Source Identity

- Citation key: `sparkes2010robot`.
- BibTeX type: `@article`.
- BibTeX title: *Towards Robot Scientists for autonomous scientific discovery*.
- BibTeX authors: Andrew Sparkes; Wayne Aubrey; Emma Byrne; Amanda Clare; Muhammed N. Khan; Maria Liakata; Magdalena Markham; Jem Rowland; Larisa N. Soldatova; Kenneth E. Whelan; Michael Young; Ross D. King.
- BibTeX publication: *Automated Experimentation*, volume 2, number 1, article 1 (2010), BioMed Central.
- BibTeX DOI: `10.1186/1759-4499-2-1`.
- PDF-internal title: *Towards Robot Scientists for autonomous scientific discovery* (PDF p. 1).
- PDF-internal authors: the same 12 authors in the same order as the BibTeX record (PDF p. 1).
- PDF-internal publication identity: *Automated Experimentation* 2010, `2:1`, with DOI `10.1186/1759-4499-2-1`; received 14 July 2009, accepted and published 4 January 2010 (PDF pp. 1, 10-11).
- Article type: publisher-formatted open-access **Review**, not the primary report of Adam's 2009 experimental result. The result is attributed to King et al. 2009, reference [24] (PDF pp. 1, 3, 5, 9-10).
- Absolute PDF path: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Reference/Sparkes 2010 - Towards Robot Scientists for Autonomous Scientific Discovery.pdf`.
- SHA-256: `0838ce55a216d3b5ba46b3bedb5e85194ed056dc98e5909630264f63066692cd`.
- `pdfinfo` page count: 11.
- PDF properties: unencrypted, 595 x 794 pt pages, PDF 1.4. The metadata title and author fields are blank, but the rendered title page and DOI line provide an exact publication identity. The 2015 Distiller creation timestamp is a file-production timestamp, not evidence of a different article version.
- Version status: `exact`. Title, complete author order, journal, volume/article number, year, and DOI match the BibTeX record. BibTeX `pages={1}` denotes article number 1; it does not claim that the PDF has only one rendered page. The path, hash, 11-page count, and `exact` status match the frozen core manifest.

## Full-Text and Visual Coverage

- PDF p. 1: article identity, abstract, review scope, autonomous-discovery components, Adam and Eve overview.
- PDF p. 2: historical systems, distinction between ordinary laboratory automation and closed-loop learning, and reference [23] as the origin of the Robot Scientist concept.
- PDF p. 3: Robot Scientist cycle, Adam's yeast-functional-genomics scope, metabolism model, two levels of gene/enzyme and growth hypotheses, displayed logical predicates, and Figure 1.
- PDF p. 4: Adam hardware, OD595 growth measurement, statistical analysis and model update, intended human intervention boundary, and hypothesis-generation software.
- PDF p. 5: Figure 3 hardware layout, four-step candidate-hypothesis construction, two-factor/Latin-square assay design, random-forest analysis, cycle repetition, and the start of Adam's results.
- PDF p. 6: exact human/literature confirmation counts, a documented wrong conclusion and model limitation, formalization, and the still-developing Eve system.
- PDF p. 7: Figure 4 and Eve's planned mass-screen, hit-verification, and targeted-screening workflow.
- PDF p. 8: Figure 5, Eve formalization and future work, and the opening of the independence discussion.
- PDF p. 9: prototype and independence limits, independent-verification assertion, database/model limitations, human handling of physical faults, cost discussion, and conclusion.
- PDF p. 10: appendix, author contributions, publication dates, and references 1-32, including primary Robot Scientist references [23] and [24].
- PDF p. 11: references 33-39 and the final DOI/citation line.
- Pages 1-11 were read in order with page-bounded, layout-preserving extraction. PDF pp. 1, 3-9 were rendered at 180 dpi and visually inspected. The renders confirm the title and review label; Figure 1's model-to-hypothesis-to-design-to-robot-to-observation-to-analysis-to-model loop; Adam's physical apparatus in Figures 2-3; Eve's physical apparatus in Figures 4-5; and the displayed `encodesORFtoEC(...)` and `affects growth(...)` predicates on PDF p. 3. The article contains no tables and no mathematical acquisition-function equation.

## Frozen Description

> An autonomous laboratory system for yeast functional genomics. It forms hypotheses about gene-enzyme relationships using a model of metabolism, selects which experiments to run via an active-learning criterion weighing expected information against cost, physically executes growth experiments with laboratory robotics, measures cell growth, and applies a statistical hypothesis test to accept or reject before forming the next round. It predates large language models. Final scientific conclusions were confirmed by human scientists.

## Clause-Level Assessment

| Frozen clause | Status | PDF evidence and assessment |
|---|---|---|
| "An autonomous laboratory system for yeast functional genomics" | **Supported with qualification** | Adam was designed for microbial growth experiments in *S. cerevisiae* functional genomics, specifically locally orphan enzymes (PDF p. 3). Its software was intended to automate experimentation cycles, with routine human intervention limited to supplying strain stocks and consumables (PDF p. 4). However, the authors call Adam and Eve prototypes and say they are not independent workers (PDF pp. 8-9); humans also manually updated Adam's model when database conflicts were noticed and remained better at detecting some physical failures (PDF p. 9). "Autonomous" is accurate for the bounded experimental loop, not for general scientific independence or a human-free installation. |
| "It forms hypotheses about gene-enzyme relationships using a model of metabolism" | **Supported** | Adam combined a logical yeast-metabolism model based on iFF708, KEGG, and PSI-BLAST/FASTA to generate candidate ORF-to-enzyme hypotheses (PDF p. 3). It also inferred compound/deletant growth-effect hypotheses from the first level. PDF pp. 4-5 describe the Prolog reaction-pathway model and the four-step construction of candidate ORF-to-E.C. mappings. |
| "selects which experiments to run via an active-learning criterion weighing expected information against cost" | **Unsupported by this source and materially over-specific** | The complete 11-page review contains no occurrence of `active learning`, `Bayes`/`Bayesian`, `information gain`, `expected information`, `entropy`, or `mutual information`. It says Adam **designs assays to test hypotheses**: a two-factor comparison with replicates (PDF pp. 3-4) and a Latin-square microplate layout intended to detect small effects above background noise (PDF p. 5). It then says Adam tested all 20 hypotheses (PDF p. 5). The cost passages concern Eve's hoped-for screening economy and the capital/maintenance cost of Robot Scientists, not an acquisition rule (PDF pp. 6, 9). Reference [23], King et al. 2004, is cited as the origin of the Robot Scientist concept on PDF p. 2, but this review does not restate any selection objective from that work. Thus this PDF cannot substantiate the frozen cost-information criterion. |
| "physically executes growth experiments with laboratory robotics" | **Supported** | Adam created microtitre experiments with automated liquid handlers and three robotic arms, could create up to 1,000 individual experiments per day, and ran typical experiments for four days (PDF p. 4; Figures 2-3 on PDF pp. 4-5). Experiment-layout and volume files were passed to robot-control software for execution (PDF p. 5). |
| "measures cell growth" | **Supported with measurement qualification** | Adam measured optical density at 595 nm with two microtitre plate readers. The resulting time series was treated as a **proxy** for cellular growth and phenotype, then smoothed to extract growth rate, lag time, and related parameters (PDF pp. 4-5). The source does not describe direct cell counting. |
| "applies a statistical hypothesis test to accept or reject" | **Partially supported; `a statistical hypothesis test` is too specific** | PDF p. 4 says growth curves were smoothed, biologically significant parameters extracted, and the results statistically analyzed to determine whether hypotheses were confirmed or refuted. PDF p. 5 says parameters from multiple replicates were analyzed using random forests to obtain statistically significant results that could confirm or refute hypotheses. The review does not name a classical hypothesis test, test statistic, null distribution, alpha level, calibrated acceptance threshold, or a literal accept/reject gate. "Statistical and machine-learning analysis used to confirm or refute" is source-faithful; "a statistical hypothesis test" is not established at this level of specificity. |
| "before forming the next round" | **Supported as a conceptual cycle, with implementation detail omitted** | Figure 1 sends statistical/ML analysis to new knowledge and model update, then back to hypothesis generation (PDF p. 3). PDF pp. 4-5 say gained knowledge updates the yeast-metabolism model and the cycle can repeat with further hypothesis generation. The paper does not specify an optimized stopping rule or acquisition function governing the next round. |
| "It predates large language models" | **Supported as a chronological characterization** | Adam was commissioned at the end of 2005 (PDF p. 3), its primary discovery report is from 2009 (reference [24]), and this review was published in 2010 (PDF pp. 9-10). The architecture uses logic programming, bioinformatics, random forests, robotics, and relational databases rather than LLMs (PDF pp. 3-5). The paper naturally does not use the later term "large language model," but the pre-LLM characterization is chronologically sound. |
| "Final scientific conclusions were confirmed by human scientists" | **Partially supported but overgeneralized** | Adam experimentally confirmed 12 of 20 hypotheses with high confidence. Conventional manual biological experiments verified **3** of those conclusions, and detailed literature searches supplied evidence for **6 more** (PDF pp. 5-6). The paper later summarizes the new gene-function knowledge as independently verified (PDF p. 9), but the precise accounting does not say that humans experimentally confirmed all 12. It also documents one incorrect conclusion caused by the metabolism model's missing kinase regulation (PDF p. 6). Human confirmation was downstream checking, not the internal gate shown in Figure 1. The clause must state the actual counts and separate manual experiments from literature support. |

## Autonomous Loop Versus Human Work

### Reported autonomous loop

- Figure 1 shows a machine-centered loop: system model and knowledge base -> hypothesis generation -> experiment generation/design -> robotic execution -> experimental observations -> statistical/ML analysis -> new knowledge and model update -> another hypothesis cycle (PDF p. 3).
- In Adam, gene/enzyme candidates came from a logical metabolism model and bioinformatics; two-factor replicated assays and Latin-square layouts tested resulting growth predictions; OD595 curves were smoothed and analyzed; and supported/refuted results could update the model (PDF pp. 3-5).
- Routine operation was intended to need humans only for strain stocks and consumables (PDF p. 4). This is a real bounded autonomous wet-lab loop, not merely a software simulation.

### Human work outside or around that loop

- The independent manual experiments and literature searches on PDF pp. 5-6 are **post hoc confirmation of selected conclusions**, not a human acceptance step between every machine cycle.
- Humans manually updated the background model when conflicts were noticed before automated hypothesis generation (PDF p. 9). The knowledge base therefore was not produced and maintained autonomously end to end.
- Human scientists and technicians supplied materials, maintained the robotic systems, performed manual experiments, and handled physical anomalies that the prototype could not reliably detect (PDF pp. 4, 9-10).
- The paper explicitly calls the systems prototypes and concedes that they were not independent workers (PDF pp. 8-9). Autonomy must remain scoped to the programmed discovery cycle.

## Pre-LLM Active Learning Versus Modern Bayesian EIG

- **What this PDF demonstrates:** pre-LLM hypothesis-driven closed-loop experimentation and assay design. Adam generated candidate hypotheses from a logical domain model, designed replicated experiments to test them, executed them, and fed analyzed results back into the model (PDF pp. 3-5).
- **What this PDF does not demonstrate:** an acquisition function choosing the next experiment by expected information, entropy reduction, posterior KL divergence, mutual information, or a combined information-cost utility. None of those terms or equations appears in the full text.
- The Latin-square layout is an experimental-design device for detecting small quantitative effects above background noise (PDF p. 5); it is not evidence of Bayesian EIG. Random forests are used in result analysis (PDF p. 5); their presence does not turn the experiment-selection policy into Bayesian design.
- Reference [23] identifies a 2004 primary Robot Scientist paper, but the present review cites it only while introducing the concept (PDF pp. 2, 10). Any claim about that earlier system's active-learning policy needs the primary source itself. No inference about its precise objective should be imported from the reference title.
- More generally, a pre-LLM method called "active learning" would still not automatically be a modern Bayesian EIG policy. EIG requires an explicit expected reduction in posterior uncertainty, commonly expressible as expected KL divergence or mutual information under a probabilistic model. This PDF provides no such criterion. The defensible characterization from this source is **hypothesis-driven closed-loop experiment design**, not **Bayesian-optimal EIG selection**.

## Material Boundaries and Omissions

1. **This is a review source.** Adam's result is summarized here and attributed to King et al. 2009 [24], so detailed result claims should prefer that primary report (PDF pp. 5, 9-10).
2. **Adam and Eve have different evidence status.** Adam had produced reported discoveries; Eve was physically commissioned, but its software and biological assays were still under development, and much of its targeted-screening description is future tense (PDF pp. 3, 6-8).
3. **Experiment design is not experiment acquisition.** Replication, two-factor comparisons, and Latin-square plate layouts support robust hypothesis testing but do not evidence information-cost selection (PDF pp. 3-5).
4. **The validation mechanism is underspecified.** The review names smoothing, parameter extraction, random forests, statistical significance, and confirm/refute outcomes, but not a formal test or calibrated decision threshold (PDF pp. 4-5).
5. **The model could mislead the loop.** Adam reached an incorrect conclusion because kinase regulation was absent from its metabolism model (PDF p. 6), and the authors discuss database errors and limited background knowledge (PDF p. 9).
6. **Human confirmation is neither complete nor gating.** Three conclusions received conventional manual experimental verification and six more received literature support; this checking was outside the machine's internal cycle (PDF pp. 5-6; Figure 1 on PDF p. 3).
7. **Cost is not an acquisition objective here.** The paper says the prototypes were not then cost-effective relative to human scientists (PDF p. 9), which is distinct from choosing experiments by an information-to-cost utility.

## Recommended Corrected Description

Adam was a pre-LLM prototype Robot Scientist for yeast functional genomics. Using a logical model of yeast metabolism, KEGG, and sequence-similarity methods, it generated candidate gene-enzyme and predicted growth-effect hypotheses. It designed replicated two-factor growth assays with Latin-square microplate layouts, executed them on an integrated robotic laboratory, measured OD595 growth curves as a proxy for cell growth, and used smoothing, random forests, and statistical analysis to confirm or refute hypotheses and update the model for another cycle. This 2010 review does not document an active-learning acquisition rule that trades expected information against cost, and it provides no Bayesian EIG objective; that mechanism requires a separate primary citation if asserted. Humans supplied stocks and consumables, sometimes corrected the background model, and performed downstream validation: conventional experiments verified 3 of the 12 machine-confirmed conclusions, while literature searches supported 6 more. Those human checks were not an internal acceptance gate. Eve was physically commissioned but its software, assays, and targeted-screening loop were still under development in this paper.

## Overall Verdict

**`major_revision`** for the frozen supplementary description.

The bounded autonomous wet-lab loop, yeast domain, metabolism-model hypotheses, robotic growth assays, OD595 measurements, iterative analysis, and pre-LLM chronology are well supported. Material revision is required because the active-learning information-cost criterion and modern Bayesian EIG interpretation are absent from this source, the named statistical hypothesis test is more specific than the review's method account, and the human-confirmation sentence overstates both coverage and its role in the loop.

## Completion Checklist

- [x] BibTeX title, complete author list, journal, volume/article number, year, and DOI checked against the PDF.
- [x] Absolute PDF path, SHA-256, and 11-page count verified locally.
- [x] Version status assessed as `exact` against the publisher-formatted article.
- [x] PDF pages 1-11 read in order, including the appendix, author contributions, references, and final DOI line.
- [x] Figures 1-5 and the displayed logical predicates inspected through rendered PDF pages.
- [x] Confirmed that the paper contains no table or mathematical acquisition-function equation.
- [x] Every clause of the frozen supplementary description assessed.
- [x] Adam's autonomous cycle separated from material supply, model maintenance, manual experiments, literature checking, and physical-fault handling by humans.
- [x] Pre-LLM closed-loop experiment design separated from modern Bayesian EIG.
- [x] Adam's reported results separated from Eve's still-developing workflow.
- [x] Only the assigned evidence file was created.

SYSTEM_DESCRIPTION_ASSESSED: yes
EVIDENCE_COMPLETE: yes
