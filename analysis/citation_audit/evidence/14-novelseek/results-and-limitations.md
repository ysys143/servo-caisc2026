# NovelSeek PDF: Results and Limitations

## Scope and reading record

- Audited source: `NovelSeek - When Agent Becomes the Scientist.pdf`, 34 pages.
- The paper itself is titled `InternAgent: When Agent Becomes the Scientist - Building Closed-Loop System from Hypothesis to Verification` (p. 1). The filename and paper title therefore use different names; this record treats them as the same single supplied PDF.
- I read the document in page order from p. 1 through p. 34, including the references and appendices. No other PDF was opened. No API or model call was made for this audit.
- This record reports claims made by the paper. It does not independently reproduce the experiments.

## Experimental design

The proposed system is a closed-loop multi-agent pipeline with four linked stages: self-evolving idea generation, human-interactive feedback, idea-to-methodology construction, and multi-round experiment planning/execution (pp. 2-3). The paper's execution loop is operational rather than merely conceptual: code is attempted, exceptions and tracebacks are captured, the code context is analyzed, a fix is formulated, and the cycle repeats until success or an iteration threshold (p. 8). For complex repositories it uses OpenHands; for single-file or limited-scope tasks it uses Aider (p. 8).

The idea-generation setup is specified as follows: the Survey Agent reviews 50 papers, the generation agent produces 15 ideas, each idea is evolved into 3 ideas, the top 5 are selected, and the evolution runs for at most 4 rounds. The methodology agent initializes and refines each selected idea once. Code generation/debugging uses Claude-3.7-Sonnet, with at most 4 debug attempts, at most 5 Aider runs, and at most 3 OpenHands runs (p. 12). The paper states that the idea-generation agents are based on GPT-4o (p. 12).

For the main quantitative comparison, the paper runs 10 InternAgent-generated ideas per task (Tables 1-4, pp. 13-14). It reports both maximum performance and the average over experiments that achieved performance gains, plus counts in the form `improved / successful / tested` (pp. 13-14). A few-shot reaction-yield experiment uses 5 independent repeats because of high variance (Table 7, p. 15). Adaptive Evolution is ablated on AutoRYP, Auto2DCls, and AutoSenCls (Table 8, p. 16). Human idea evaluation uses 20 ideas per system per task, five reviewers, and four scoring dimensions (pp. 20, 27-29).

## Task domains and benchmarks

The paper evaluates 12 tasks across scientific, time-series, NLP, image, point-cloud, and multimodal settings (pp. 9-11):

| Task | Dataset/benchmark | Baseline | Metric |
|---|---|---|---|
| AutoRYP reaction yield prediction | Suzuki-Miyaura, 5,760 reactions | LoRA-finetuned LLaMA3-8B | R2 |
| AutoMD molecular dynamics | MD17, seven molecules | VisNet | Force-MAE |
| AutoPower power-flow estimation | IEEE 39-Bus | SenseFlow | PQ-node RMSE |
| AutoTSF time-series forecasting | ETTh1 | DLinear | average MAE at 96/192/336/720 horizons |
| AutoTPPR perturbation-response transcription prediction | Perturb-seq | GEARS | Top-20 DE MSE |
| AutoEAP enhancer activity prediction | UMI-STARR-seq | DeepSTARR | Housekeeper PCC |
| AutoSenCls sentiment classification | SST-2 | BERT-base | accuracy |
| Auto2DCls image classification | CIFAR-100 | Wide ResNet | top-1 accuracy |
| Auto3DCls point-cloud classification | ModelNet40 | PointNet | overall accuracy |
| Auto2DSeg semantic segmentation | Pascal VOC 2012 | DeepLabV3Plus | mIoU |
| AutoPCDet 3D autonomous-driving detection | ONCE | CenterPoint/OpenPCDet code | mAP, with vehicle classes merged |
| AutoVLM vision-language fine-tuning | filtered geometry subset of URSA; evaluated on MathVista geometry | LLaVA-OneVision, with SigLIP and Qwen2.5-Math-7B-Instruct modules | QA accuracy, answers extracted using GPT-4o |

The task descriptions and metrics are in pp. 9-11. For AutoVLM, natural images are excluded and data are downsampled to finish within 20 hours on 8 A800 GPUs (p. 11). For AutoPCDet, the paper says code irrelevant to the baseline was filtered to avoid knowledge leakage (p. 11). These are computational benchmark tasks; they are not wet-lab or physical-robot experiments.

## Baseline comparisons and quantitative results

The main tables compare the supplied baseline, DOLPHIN where supported, and InternAgent-generated code. DOLPHIN cannot modify the project-level multi-file baselines for Auto2DSeg, AutoPCDet, and AutoVLM, so those cells are marked unavailable rather than a direct comparison (Table 2, p. 13).

Maximum results reported by InternAgent versus baseline are: AutoRYP R2 35.4 vs 27.6; AutoMD Force-MAE 0.148 vs 0.158; AutoPower RMSE 0.00426 vs 0.00473; AutoTSF MAE 0.4331 vs 0.4382; AutoTPPR MSE 0.146 vs 0.197; AutoEAP HK-PCC 0.79 vs 0.65. On the second group, AutoSenCls is 93.5 vs 91.0 accuracy, Auto2DCls 83.3 vs 81.2, Auto3DCls 95.5 vs 91.0, Auto2DSeg 81.0 vs 78.8 mIoU, AutoPCDet 65.9 vs 65.0 mAP, and AutoVLM 67.6 vs 67.1 QA accuracy (Tables 1-2, p. 13). Metric direction differs: lower is better for Force-MAE, RMSE, MAE, and MSE; higher is better for the other reported metrics.

Across the 10 ideas per task, InternAgent's improved/successful/tested counts are AutoRYP 4/6/10, AutoMD 4/8/10, AutoPower 5/6/10, AutoTSF 3/7/10, AutoTPPR 5/5/10, AutoEAP 8/8/10, Auto2DCls 5/7/10, Auto3DCls 3/6/10, AutoSenCls 9/9/10, Auto2DSeg 6/9/10, AutoPCDet 2/5/10, and AutoVLM 1/5/10 (Tables 3-4, pp. 13-14). Thus the paper's own counts show that not every generated idea improved performance and that execution success is materially lower on some repository-level tasks, especially AutoPCDet and AutoVLM.

The few-shot AutoRYP repeat study is more stable for ADAGT than the baseline at train-set=60: baseline 24.2 +/- 4.2 versus ADAGT 34.8 +/- 1.1 over five repeats. At train-set=100, baseline is 35.5 +/- 4.9 versus ADAGT 38.7 +/- 1.7 (Table 7, p. 15). The AE ablation reports, for example, AutoRYP max R2 34.7 without AE versus 35.4 with AE, and Auto2DCls max accuracy 81.6 versus 83.3 (Table 8, p. 16). The paper attributes this to analyzing prior results and re-planning subsequent experiments (p. 17).

Against other automated systems, Table 9 reports InternAgent AutoRYP max/average R2 35.4/33.5 at total cost $3, versus AI-Researcher 12.3/- at $25; AI-Scientist-V2 produced no reported result at $15. For Auto2DCls, InternAgent reports 83.3/82.2 at $3, versus AI-Researcher 80.3/- at $32 and no reported AI-Scientist-V2 result at $10 (p. 17). The paper says both systems were given the same code templates and used GPT-4o-2024-08-06 for ideas and Claude-3-7-Sonnet-20250219 for code generation, but the table does not provide a successful AI-Scientist-V2 metric for these tasks (p. 17).

Reported resource costs are 0.1-192 A100 GPU hours for training across the tasks, about $0.6 per idea-generation session in the summarized cost tables, and $0.4-$1.2 per coder-debug run depending on task complexity (Tables 5-6, p. 14). The strongest time examples in the abstract are AutoRYP 27.6% to 35.4% in 12 hours, AutoEAP 0.65 to 0.79 in 4 hours, and Auto2DSeg 78.8% to 81.0% in 30 hours (p. 2).

## Feedback loop and multi-agent roles

The Survey Agent performs literature review or deep research, updating queries from generated technical terms (pp. 6, 16). The Code Review Agent reads repository/file structure and functions to give the idea and methodology agents code context (pp. 4-5). The Idea Generation/Innovation Agent proposes and evolves ideas. The Assessment Agent critiques and scores ideas. The Method Development Agent initializes a method from the idea, task description, baseline, and literature, then refines it using automated assessment and human feedback (pp. 7-8). The Coder Agent implements and debugs. The Orchestration Agent coordinates communication, ranking, workflow timing, and the points at which human feedback is requested (p. 7).

The feedback loop has two sources: direct human feedback and automatically generated agent feedback (pp. 6-7). Human feedback can add domain-specific guidance, redirect a proposal, and refine high-scoring ideas. Agent feedback includes critiques, scores, code/runtime results, and experimental performance. The experimental loop decomposes a method into steps, observes performance after each step, and changes the next plan; the Auto3DCls example shows gains of +0.5%, +1.2%, +1.6%, then a -0.8% degradation before removing the harmful components and ending at +2.1% (p. 19). The AutoTPPR visualization similarly shows successive performance reflections and final +0.051 MSE improvement (p. 30).

## Human interaction and human study

Human involvement is an optional interactive control point in the system, not a human-operated execution of every experiment. The Orchestration Agent chooses feedback points, especially after high-scoring ideas (p. 7). The paper presents a user entry/task-selection interface, idea-tree visualization, human-computer interaction interface, code generation, and auto-debug interface (p. 34). It also describes a whitelist trial application requiring intended scenario, research task, and institution information (pp. 29-30).

The formal human evaluation covers only four tasks: reaction yield prediction, 2D semantic segmentation, 2D image classification, and point-cloud autonomous driving. For each task, both systems generate 20 ideas; five qualified reviewers score the ideas for soundness, contribution, overall rating, and confidence (pp. 20, 27). Reviewers must be Ph.D. holders or candidates with top-tier AI-conference reviewing experience, spend at least 10 minutes per idea, and may search literature and check redundancy (p. 29). InternAgent's reported overall scores exceed AI-Scientist-V2 on all four listed tasks, e.g. 4.35 vs 3.50 for reaction yield and 5.10 vs 3.10 for point-cloud autonomous driving (Table 10, p. 21). This is an evaluation of generated ideas, not a human-vs-agent comparison of scientific discoveries in real-world settings.

## Computational-only scope and limits of the evidence

All reported validation is computational: fixed public datasets, baseline repositories, generated code, GPU training, and benchmark metrics. The paper discusses autonomous scientific research broadly and notes that real-world closed loops would require robotics, handling unexpected variables, and noise, but it does not report physical laboratory, field, or robotic experiments (pp. 2, 22). Therefore, the results support automated computational research workflows, not general autonomous science in the physical world.

The paper itself identifies several limitations and open problems:

1. Knowledge retrieval remains incomplete. The proposed future work calls for paper-relationship graphs, meta-analysis, structured representations, and retrieval augmentation to reduce hallucinated viewpoints and citations (p. 22).
2. Knowledge understanding and representation by VLM/LLM is still a challenge, especially for extracting concepts, methods, findings, patterns, and connections from many papers (p. 22).
3. Agent capability and feedback adaptation need improvement. Future agents should self-modify goals and plans and learn from the environment, other agents, and human experts (p. 22).
4. The authors call for scientific-discovery benchmarks that assess idea value, method/code alignment, and generalization beyond the presented scenarios, rather than novelty alone (p. 22).
5. The reported success counts expose execution fragility: only 5/10 AutoPCDet and 5/10 AutoVLM ideas ran successfully, and only 2/10 ideas improved performance for each (Table 4, p. 14). The paper's broad 12-task claim therefore includes uneven per-task reliability.
6. The main DOLPHIN comparison is structurally incomplete for the three project-level tasks because DOLPHIN cannot modify their multi-file baselines (Table 2, p. 13). The AI-Scientist-V2 comparison also contains missing result cells in Table 9 (p. 17).
7. The abstract compares time to human researchers, saying humans typically need months for a similar reaction-yield improvement, but the document does not present a controlled human experiment for that specific end-to-end result. The formal human study instead scores ideas on four tasks (pp. 2, 20-21, 27-29).
8. The pipeline depends on substantial model/API usage and GPU clusters. The paper explicitly notes associated costs and describes a whitelist application because of massive API-key calls and GPU compute requirements (p. 29). Its cost claims are therefore infrastructure- and model-dependent rather than hardware-independent.
9. The AutoVLM metric extracts answers using GPT-4o (p. 11), so that result includes an additional model-based evaluator in the measurement path. This is distinct from a direct exact-match evaluation and should be treated as an evaluation dependency.
10. The related-work discussion acknowledges that current autonomous research systems are often tested on simple or narrow tasks and that robust experiment-to-idea feedback and systematic real-world evaluation standards remain unresolved (p. 22).

## Overall evidence judgment

Within the supplied PDF, the evidence supports the narrower claim that InternAgent can generate, implement, and iteratively test ideas on a diverse set of computational ML and AI-for-science benchmarks, often improving the stated baselines under the paper's experimental setup. It does not establish physical-world autonomous scientific discovery, universal generalization, or that every generated idea is executable or beneficial. The strongest constraints are computational-only validation, uneven execution/improvement rates, incomplete cross-system comparisons, model/API and GPU dependence, and the authors' own call for stronger value, alignment, and generalization benchmarks.

EVIDENCE_COMPLETE: yes
