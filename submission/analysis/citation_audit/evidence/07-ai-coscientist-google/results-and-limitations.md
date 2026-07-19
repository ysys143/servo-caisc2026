# AI Co-Scientist (Google): results, experiments, limitations

## Audit scope and evidence boundary

- Source audited: `Towards an AI co-scientist`, arXiv:2502.18864v1, the supplied 81-page PDF only.
- Page numbers below are PDF page numbers, not printed-section numbers.
- I read the document from PDF pages 1 through 81, including the main text, figures/captions, appendices, prompts, experimental supplementary information, and references. No other paper was read for this lane, and no API or model call was made.
- Claims about companion/co-timed reports are recorded only as claims made by this PDF; those reports were not used as evidence.

## What was evaluated

The paper separates internal/automated evaluation from end-to-end laboratory validation. The three application settings are explicitly classified as drug repurposing (medium complexity, combinatorial search), novel treatment-target discovery (high complexity, identifying novel targets), and explanation of bacterial gene-transfer evolution (very high complexity, complex systems) (p. 14, Table 1).

### Automated and benchmark evaluation

1. **Elo concordance with GPQA.** GPQA Diamond multiple-choice questions in biology, physics and chemistry were framed as research goals. Generated answers were bucketed by Elo in 50-point intervals beginning at 1001; correctness was checked against the benchmark ground truth. Gemini 2.0 generated 32 reference responses per question to adjust for non-uniform question difficulty. Selecting the highest-Elo answer per question produced **78.4% top-1 accuracy** (p. 14). The paper cautions that Elo itself is auto-evaluated and not ground-truth based (p. 15, Figure 3 caption).
2. **Test-time compute scaling.** The system was run on **203 distinct research goals**, mostly biomedical but including mathematics and physics, entered through February 3, 2025. Outputs were divided into ten sequential equal-size temporal buckets; for each bucket the authors computed the maximum individual Elo ("best Elo") and the mean Elo of the top 10 hypotheses, averaged across goals. Both trends increased over time, but both remain Elo-based rather than independently validated quality measures (p. 15, Figure 4 and caption).
3. **Baseline comparison.** A harder subset of **15 expert-curated research goals** was compared against Gemini 2.0 Pro Experimental, Gemini 2.0 Flash Thinking Experimental 12-19, OpenAI o1, OpenAI o3-mini-high, DeepSeek R1, and expert "best guess" solutions. The paper reports upward trends and higher Elo for the co-scientist, including above experts and baselines, but explicitly warns that auto-Elo may favor properties unrelated to scientists' preferences, quality, or accuracy (p. 16, Figure 5 caption).
4. **Human expert preference study.** Experts evaluated **11 of the 15** curated goals. They ranked four systems (1 best to 4 worst) and scored novelty and impact from 1 to 5. The co-scientist received mean preference rank **2.36**, novelty **3.64/5**, and impact **3.09/5** (p. 17). The paper labels these subjective assessments, not objective ground truth (pp. 17-18). Four LLM judges were also used for preference ranking, but the paper calls the evaluation small-scale and says larger studies are needed for reliable conclusions (p. 17).
5. **Adversarial safety evaluation.** The authors curated **1,200 adversarial research goals across 40 biomedical/scientific topics** using frontier LLMs. The system reportedly passed all rejection checks, but the dataset is not publicly released and the analysis is explicitly preliminary (p. 19). This is a safety-rejection result, not evidence of scientific hypothesis quality.

## Human intervention boundary

The system is explicitly a scientist-in-the-loop assistant, not an autonomous scientific process (p. 3). Scientists provide the natural-language goal, preferences, constraints, ideas, reviews, feedback, and chat guidance (pp. 2-3). In all three end-to-end validations, expert scientists guided the system and **prioritized the experiments** (pp. 14, 19).

### AML drug repurposing

- The constrained search covered **2,300 approved drugs across 33 cancer types**. Co-scientist review scores (1-5) and DepMap scores (0.0-1.0) were used; only pairs with review score **>=4** and DepMap **>=0.99** were sent for the prioritized expert review. The paper says DepMap was mainly a sanity filter and was unlikely to predict efficacy (pp. 19-20).
- Six board-certified hematologists/oncologists from one institution evaluated **78** NIH Specific Aims-formatted hypotheses. Four were disease-specific oncologists and two generalists; average clinical experience was **eight years**. An oncologist pre-screened/excluded implausible or poorly translatable candidates before the ratings, so the favorable ratings are selection-conditioned (p. 20).
- Thirty top-ranked candidate hypotheses were shared with oncologists for AML wet-lab selection. The experts selected five compounds with existing evidence for testing: Binimetinib, Pacritinib, Cerivastatin, Pravastatin, and DMF (pp. 21-23). Three inhibited MOLM-13 viability; Binimetinib had an IC50 as low as **7 nM** (p. 23, Figure 10).
- For the claimed novel-repurposing test, experts selected the top three from the ranked list, subject to no prior AML preclinical/clinical data: Nanvuranlat, KIRA6, and Leflunomide. Of the three, KIRA6 inhibited viability in KG-1, MOLM-13, and HL-60. Reported IC50 values were **13 nM**, **517 nM**, and **817 nM**, respectively (p. 23, Figure 11; p. 24 caption).
- The paper calls these cell-line assays an initial biological validation and a viability checkpoint, deliberately not a replacement for preclinical or clinical assessment (p. 21). It does not establish in-vivo efficacy, clinical efficacy, safety, or a causal mechanism.

### Liver fibrosis target discovery

- Experts selected **three of 15** top-ranked hypotheses, each with an experimental design, evaluation method, and anticipated results (p. 25).
- The system proposed **three** epigenetic modifiers/targets. Four drugs based on those targets were tested in a human hepatic organoid system; fibroblast activity was measured by fluorescence-labelled myofibroblast fold change. Two of the three targets' drugs showed significant anti-fibrotic activity without cellular toxicity, and one drug was FDA-approved for another indication (p. 25, Figure 12 caption and text).
- The displayed figure reports p-values versus the fibrosis-inducer group and medians, but this paper page says the detailed results will appear in an upcoming technical report; the PDF does not provide a complete experimental dataset or full statistical protocol in this lane (p. 25). Therefore the result supports targeted organoid activity only, not clinical translation or a complete target-validation package.

### Bacterial AMR / cf-PICI mechanism

- Researchers supplied a one-page background document and two relevant research articles, then posed the question of why cf-PICIs occur across diverse bacteria. The researchers already knew an unpublished experimental result from their independent work, but the paper says it was not public or revealed to the system (p. 26).
- The co-scientist's top-ranked proposal was that cf-PICIs interact with diverse phage tails to expand host range. The paper describes this as a two-day in-silico rediscovery while leveraging decades of open literature (pp. 26-27). The PDF reports convergence with an independent experimental study, but the experimental validation itself is not performed by the co-scientist paper and is deferred to a co-timed companion report (pp. 26-27).
- Thus this example is an independent hypothesis-generation/recapitulation comparison, not a blinded prospective laboratory replication by the system.

## Experimental detail and what the numbers mean

The appendix gives the AML assay setup: cells were plated at **5,000 cells per well** in 96-well plates, treated for **48 hours**, and viability was measured with an MTS assay; IC50 is defined as the concentration producing 50% maximal inhibition (pp. 60-63, Appendix A.4). The paper's headline AML results are therefore dose-response observations in cell lines under this assay, not organism-level outcomes.

The appendix also contains the constrained search dataset description, computational biology analysis, drug-selection material, the 15-axis expert rubric, and examples of generated Specific Aims (pp. 60-79). These show that generated proposals include experimental plans and assumptions, but they do not convert proposal text into evidence of successful experiments. The AlphaFold tool-use example is presented as an example of general system tooling, not as an additional end-to-end validation (p. 80).

## Explicit limitations and failure modes

1. **Incomplete literature access and missed relevance.** The system relies on open-access literature, cannot access all published work where licensing/access restrictions apply, and may incorrectly judge relevant work irrelevant (p. 27).
2. **Negative-result blindness.** Open published literature underrepresents failed experiments and negative findings, which experienced scientists may know and use for prioritization (p. 27).
3. **Weak multimodal and domain-data integration.** The system may not fully reason over figures/charts; the authors did not evaluate integration of large multi-omics datasets or biomedical knowledge graphs (p. 27).
4. **Inherited frontier-LLM faults.** Imperfect factuality, hallucination, biases, and source errors can propagate through the multi-agent/web-search system (p. 27).
5. **Preliminary metrics and narrow evaluation.** The evaluation combines auto-ratings, expert reviews, and targeted `in vitro` validation, but is preliminary. The authors call Elo limited and request broader, more objective metrics and evaluations across disciplines (p. 28).
6. **Translation gap.** Current validation does not address tissue-specific delivery, formulation, delivery efficiency, clinical-trial design, bioavailability, pharmacokinetics, or complex drug interactions. A dedicated translational team is required (p. 28).
7. **AML-specific biological limits.** Limited `in vitro` experiments cannot capture disease-model complexity, patient heterogeneity, disease variability, bioavailability, pharmacokinetics, off-target effects, patient selection, tumor microenvironment, or systemic resistance. Strong cell-line results do not guarantee in-vivo or clinical success (p. 25).
8. **Human and institutional selection bias.** Expert pre-screening occurred before the 78-proposal rating, and the clinical raters were from one institution, potentially reflecting local practice and research perspectives (p. 20). The three validation programs also used expert guidance and prioritization rather than autonomous selection (pp. 14, 19, 21, 25).
9. **Safety gaps.** The 1,200-goal adversarial test passed all checks, but it is preliminary and unreleased; the paper stresses that each iterative component and both intermediate/final hypotheses require independent safety testing (pp. 19, 29). Current safeguards include goal and hypothesis safety reviews, monitoring, logging, red teaming, and a trusted-tester program; final decisions remain with scientists (p. 30).
10. **Automation bias and homogenization.** The discussion warns that over-reliance may reduce critical thinking, homogenize ideas, and reproduce correlated LLM blind spots; factuality checks, peer review, and expert verification remain necessary (p. 32).

## Citation and claim-appropriateness audit

- **Supported by this PDF:** The architecture, scientist-in-the-loop boundary, evaluation sample sizes, reported Elo/GPQA and expert-rating numbers, AML cell-line results, liver-organoid scope, and the listed limitations are directly stated in the audited pages above.
- **Needs qualification when cited:** “Outperformed experts,” “validated,” “novel,” “promising,” and “recapitulated a breakthrough” must retain their qualifiers. The first depends on auto-Elo; expert ratings are subjective; “validated” is limited to selected `in vitro` endpoints; and AMR recapitulation is based on comparison to an unpublished independent result, with detailed evidence deferred to a companion report (pp. 15-18, 23-27).
- **Not justified as a clinical claim:** The PDF itself says none of the proposed drug candidates had undergone randomized phase III trials for the new indication (p. 21), and explicitly denies that `in vitro` evidence guarantees in-vivo efficacy or clinical success (p. 25). Citations using this paper to claim a treatment works in patients, is clinically effective, or has completed translational validation would overstate the evidence.
- **Not justified as autonomous discovery:** The experiments were guided and prioritized by domain experts; AML novel candidates were selected by experts; liver fibrosis hypotheses were selected by experts; the AMR result was compared against researchers' already-known unpublished finding (pp. 14, 19, 23, 25-27). Citations should not erase those boundaries.
- **Companion-paper dependency:** Claims about the detailed AML/liver-fibrosis/AMR laboratory findings beyond what is shown or stated here require the separately cited reports. This lane does not verify those reports because the audit scope is the supplied PDF only.

## Page coverage ledger

- pp. 1-4: abstract, motivation, system scope, three biomedical validation claims, and scientist-in-the-loop framing.
- pp. 5-13: related work, architecture, agents, hypothesis generation/review/evolution, prompts and system workflow.
- pp. 14-19: evaluation design, GPQA/Elo, test-time scaling, expert/LLM comparisons, adversarial safety, and validation setup.
- pp. 20-25: clinical-expert evaluation, AML candidate selection and cell-line results, assay interpretation, and liver-fibrosis organoid result.
- pp. 26-33: cf-PICI recapitulation, limitations, safety, safeguards, future work, discussion, and conclusion.
- pp. 34-38: main-paper references.
- pp. 39-59: appendix glossary, specialized-agent prompts, and worked system-input/output examples.
- pp. 60-63: drug-repurposing datasets, computational analysis, and AML assay details/results.
- pp. 64-79: Specific Aims evaluation data, rubric, examples, and detailed KIRA6 proposal/output.
- pp. 80-81: AlphaFold tool-use example and appendix references.

## Bottom line

The PDF supports a promising but preliminary claim: a Gemini-2.0-based multi-agent system can generate hypotheses that score well under auto-Elo and small expert studies, and selected expert-prioritized hypotheses show activity in AML cell lines and human hepatic organoids. It does not support autonomous end-to-end science, general scientific superiority, in-vivo efficacy, clinical benefit, or independent verification of the companion-study details.

EVIDENCE_COMPLETE: yes
