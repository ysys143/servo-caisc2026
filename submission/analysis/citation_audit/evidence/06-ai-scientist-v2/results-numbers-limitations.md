# AI Scientist-v2: results, numbers, limitations, and review conditions

## Audit scope and identity

- Source: `The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search`, Yamada, Lange, Lu et al., arXiv:2504.08066v1, dated 10 April 2025.
- Local PDF: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/The AI Scientist-v2 Workshop-Level Automated Scientific Discovery via Agentic Tree Search.pdf`
- PDF identity check: 69 pages, SHA-256 `53bafd3028e3f8829a3d85220e84dcf0d18934f9b75c092a60de303ff3644bd2`.
- Reading coverage: pages 1-69 sequentially, including the main paper, author contributions, hyperparameters, prompts, all three generated manuscripts, AI Scientist team reviews, code reviews, workshop reviews, references, and ethical/IRB disclosures. Page numbering restarts inside the generated manuscripts; page numbers below use the PDF page unless explicitly marked as generated-paper pagination.
- Scope restriction: this audit assesses the PDF and its embedded evidence. No API, external model, or other source PDF was used.

## System configuration and claimed workflow

Pages 1-8 describe an end-to-end system that generates ideas, searches literature with Semantic Scholar, writes and executes code, aggregates experiments, makes figures, writes a manuscript, and uses an AI reviewer with VLM feedback. The v2 changes claimed over v1 are removal of fixed human-authored code templates, a progressive four-stage experiment manager, parallel agentic tree search, and VLM-assisted review/refinement (pp. 1-8).

The four stages are: preliminary investigation, hyperparameter tuning, research agenda execution, and ablation studies. Stage 1 stops after a minimal working prototype; Stage 2 requires convergence and successful execution across at least two datasets; Stages 3 and 4 stop when their computational budgets are exhausted. The manager selects a best node after each stage and launches replications for mean and standard deviation (p. 5). The paper therefore supports staged automated experimentation, but the selection criterion is an LLM evaluator and a scalar node score, not an independent scientific-validity or novelty gate.

The reported model settings are: Claude 3.5 Sonnet v2 for code generation, GPT-4o for LLM/VLM feedback, and GPT-4o for summary reports; each uses 8,192 max tokens, with temperatures 0.5, 0.5, and 1.0 respectively. Tree-search settings are debug probability 1.0, maximum debug depth 3, maximum runtime one hour per node, and node allocations of 21, 12, 12, and 12 for stages 1-4. The claimed process usually takes several hours and at most 15 hours per paper (p. 21).

The prompts explicitly require at least one literature search before finalizing an idea, but they also instruct the model to propose “high-impact” and “publishable at top ML conferences” ideas and to be creative/novel (pp. 22-30). These are generation objectives, not evidence that the resulting ideas are novel or conference-level.

## Submission count, human selection, and peer review

The evaluation submitted three fully autonomous manuscripts to the ICLR 2025 ICBINB workshop (pp. 1-2, 31). Table 4 records exactly one accepted manuscript, `Compositional Regularization: Unexpected Obstacles in Enhancing Neural Network Generalization`, with score 6.33; `Unveiling the Impact of Label Noise on Model Calibration in Deep Learning` and `Real-world Challenges in Pest Detection using Deep Learning: an Investigation into Failures and Solutions` were rejected (p. 31).

The main text states that the accepted paper had an average reviewer score of 6.33, roughly top 45%, and would have been accepted after meta-review if human-generated (p. 2). The workshop material shows the actual review evidence: Reviewer 1 gave 7, Reviewer 2 gave 6, and Reviewer 3 gave 6, for an arithmetic mean of 6.33; all were “No Award” and confidence values were 4, 2, and 3 respectively (pp. 39-40). The document does not provide a meta-review text or a formal human-acceptance threshold calculation. Therefore “acceptance-worthy” is supported as the authors' counterfactual assessment, but “accepted” or “passed peer review” must be qualified: one paper received positive workshop reviews, but the AI-generated submission was withdrawn and did not appear on OpenReview.

Human selection was not absent. The author-contribution statement says Yamada, Lange, Hu, and others read and validated many AI-generated papers, checked code, and selected submissions; Lu, Clune, and David Ha evaluated AI-generated submissions (p. 19). The paper also reports cooperation with ICLR leadership and workshop organizers, University of British Columbia IRB approval H24-02652, and withdrawal/non-publication of the AI papers by agreement (pp. 13-14). Thus the generation and paper production were automated, but the three-paper evaluation set and submission process included human validation, selection, communication, and oversight.

## Submission 1: compositional regularization

The generated idea proposes a compositional regularizer for sequence models; the final generated paper uses an LSTM, an embedding layer, a fully connected output, synthetic arithmetic expressions, mean squared error, and a regularization term defined as the mean squared difference between successive *input embedding* states. The generated manuscript writes these as hidden states, but the AI Scientist code review identifies the implementation as embeddings, not LSTM hidden states (generated pp. 2-3; PDF pp. 34, 42-43).

Reported setup: 1,000 randomly generated training expressions and 200 test expressions, 30 epochs, Adam, MSE, default lambda 0.1, and test accuracy defined by a tolerance around the regression output (generated p. 3). The code review found a serious overlap risk: with one-digit expressions, 1,000 training and 200 test samples, repeated checks found approximately 57% average test/training overlap for addition and multiplication (PDF p. 42). This weakens the interpretation of “unseen combinations” and generalization.

The main generated results claim approximately 84% baseline test accuracy, no improvement from higher lambda, and degradation as operator complexity increases (generated pp. 2-4). The embedded review disputes or qualifies several details: Figure 1 visually reaches only about 40%, Figure 3's caption says validation accuracy where validation loss increases, and the attention-augmented LSTM actually reaches 100% in the reported original setup. A rerun in the code review obtained 100% for numbers 1-9 but 56% for 10-19; the baseline obtained 85% and 0% respectively (PDF pp. 34-40, 44). The review's conclusion is that the first attention result is a simple task and does not establish broad compositional generalization.

Ablations cover embedding dimensions 16/32/64/128, attention, lambda sweeps, LSTM versus simple RNN, dropout rates, and related training details (generated pp. 5-8). However, the text contains parameter inconsistencies: the generated appendix lists lambda values including 0.3, 0.5, 0.7, and 1.0, while the code-review annotations flag values such as 0.2 and 0.01; the paper states ReLU although the implementation does not use it; the displayed dropout figure does not show the claimed sweep; and training lengths vary between 20, 30, and 50 in the review annotations. The AI team review scored soundness 3/5, presentation 2/5, contribution 3/5, workshop overall 5/10 borderline accept, and confidence 4/5 (pp. 41-44).

## Submission 2: label noise and calibration

The generated idea proposes symmetric and asymmetric synthetic label noise on CIFAR-10 and MNIST, calibration evaluation with ECE/reliability diagrams, mitigation methods, real-world noisy datasets, and ablations. The generated paper reports CIFAR-10, MNIST, and Fashion-MNIST with ResNet-18; symmetric/asymmetric noise at 10-50%; ECE and reliability diagrams; cross-entropy with SGD; initial learning rate 0.1; decay at epochs 50 and 75; 100 epochs; batch size 128; and temperature scaling (generated pp. 1-4; PDF pp. 45-52).

The embedded team/code review shows that this record is not internally reliable without qualification. The review notes that the actual experiments used cosine annealing rather than the stated step decay, and the generated paper's figures do not show temperature-scaling results or reliability diagrams. Temperature scaling was implemented in code but never used. Figure 1's text reports approximately 85% baseline accuracy and ECE up to 0.35, while the review annotations identify the corresponding values as approximately 75% and 0.23-0.24. The claim that asymmetric noise is uniformly worse is also qualified because the displayed ECE pattern rises and then falls at higher noise rates (PDF pp. 47-53, 55-57).

The generated paper says standard mitigation methods offer limited calibration improvement, but the displayed evidence does not establish that conclusion for temperature scaling or label smoothing. The AI team review assigns soundness 2/5, presentation 1/5, contribution 1/5, workshop overall 3/10 reject, conference overall 2/10 strong reject, and confidence 4/5. It specifically identifies unsupported results, missing/incorrect citations, unreadable or duplicated figures, and missing reliability diagrams (pp. 53-54). The workshop reviews independently give both reviewers a rating of 3, with confidence 5 and 4 (p. 57).

## Submission 3: pest detection

The generated idea proposes real-world pest detection with data quality analysis, robustness testing, environmental variability, failure analysis, and improvement strategies. The system-generated paper instead uses an ImageNet-pretrained ResNet-18 fine-tuned on the Crop Pest and Disease dataset, simulated test-time augmentations, learning-rate experiments, and separate models on EuroSAT, MedMNIST, and CIFAR-10 (generated pp. 1-4; PDF pp. 58-64).

The source reports 25,126 images across 22 pest/disease classes and a 70/15/15 train/validation/test split, but an explicit dataset-preparation note says a manually downloaded Kaggle dataset was reduced to one tenth, approximately 2,500 images, for speed. Baseline learning-rate values were 1e-4, 5e-4, 1e-3, 5e-3, and 1e-2; each was trained for 10 epochs with batch size 32 and Adam. Test-time augmentations were brightness/contrast changes, Gaussian blur, and random affine transformations. Environmental Robustness Score (ERS) is accuracy under challenging conditions divided by accuracy under normal conditions (PDF pp. 58-60, 63).

The manuscript calls the additional-dataset work “multi-dataset training” and “domain adaptation,” but the internal review says the final experiments trained separate models on individual EuroSAT, MedMNIST, and CIFAR-10 datasets. A domain-discriminator/multi-dataset implementation existed but did not run successfully and was not the selected result. Thus the reported cross-dataset comparison is not evidence of a model trained jointly across datasets or of real agricultural domain adaptation (PDF pp. 60, 65-66).

The source also contains a mismatch between claims and results: the abstract and discussion frame deployment in real agricultural settings, but only synthetic augmentations were used and no real-world deployment was performed. The workshop reviews score the paper 3/10 reject, 7/10 accept, and 4/10 reject, with concerns about unmotivated ERS, limited learning-rate sweeps, missing dataset citations, unclear multi-dataset terminology, and lack of real-world testing (pp. 67-69). The second reviewer recommends acceptance despite these issues; the other two reviewers support rejection or major revision, so the record does not support a positive consensus.

## Costs, compute, failures, and reproducibility

The only explicit system-level compute figures are per-node runtime of one hour, stage node allocations of 21/12/12/12, and an experienced end-to-end runtime range of several hours to at most 15 hours per generated paper (p. 21). The paper does not provide a total GPU-hour, dollar cost, token count, number of model calls, or aggregate number of nodes actually executed for the three submissions. It says experiments were run in parallel and the generated compositional paper notes a single NVIDIA GPU, but no complete resource ledger is reported (pp. 5, generated p. 8).

Failure evidence is substantial: the v2 pipeline produced two rejected papers; the compositional paper had train/test overlap and a misleading attention conclusion; the label-noise paper discussed unexecuted calibration experiments and omitted figures; and the pest paper's attempted domain-adaptation/multi-dataset path failed and the final interpretation overstated what was tested (pp. 42, 53-57, 65-66). These are direct limitations of the reported artifacts, not merely future-work speculation.

## Overall assessment of evidentiary support

**Overall verdict: major_revision.** The PDF supports the narrower claim that AI Scientist-v2 is an automated ML-oriented research pipeline with template-free idea-to-manuscript generation, agentic tree search, parallel execution, VLM review assistance, and a small workshop submission study. It also supports that one of three generated manuscripts received a 6.33 mean workshop review score and was assessed by the authors as acceptance-worthy under a human-authorship counterfactual.

The following stronger formulations are not supported without qualification: that the system achieved formal workshop acceptance; that the three-paper sample demonstrates reliable scientific discovery; that the review result was independent of human selection and validation; that “multi-dataset training” or domain adaptation was actually completed in the pest study; that calibration mitigation was empirically evaluated in the label-noise study; or that the accepted compositional paper demonstrated genuine compositional generalization. The embedded human reviews and code reviews themselves document these gaps.

## Required correction targets

1. Replace “accepted”/“passed peer review” with “one of three papers received a 6.33 workshop review average and was judged acceptance-worthy after meta-review under a human-authorship counterfactual”; state that the AI paper was withdrawn and not publicly posted.
2. State explicitly that human researchers selected/validated submissions, checked code, managed workshop communication, and obtained IRB/organizer approval.
3. Report the three-submission denominator whenever the one-positive result is mentioned.
4. Separate executed experiments from planned or implemented-but-unused code for label-noise calibration and pest domain adaptation.
5. Replace “multi-dataset training” in the pest summary with separate per-dataset transfer/fine-tuning experiments unless the failed joint-training path is being discussed as a failure.
6. Treat all generated-paper numerical claims as conditional on the embedded review/code-review corrections, especially the 57% overlap estimate, attention 100%/56%/baseline 85%/0% checks, label-noise 75% versus 85% and 0.23-0.24 versus 0.35 discrepancies, dataset reduction to approximately one tenth, and inconsistent hyperparameters.

EVIDENCE_COMPLETE: yes
