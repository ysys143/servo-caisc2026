# Digest: zhang2025novelseek

**IMPORTANT NAMING NOTE.** The bibkey is `zhang2025novelseek` and the PDF filename says "NovelSeek", but the paper as read (arXiv:2505.16938**v3**, 22 Jul 2025) is titled **"InternAgent: When Agent Becomes the Scientist – Building Closed-Loop System from Hypothesis to Verification"** by the **InternAgent Team, Shanghai Artificial Intelligence Laboratory**. The system is called **InternAgent** throughout this version; "NovelSeek" was an earlier name for the same project (GitHub: `Alpha-Innovator/InternAgent`; HF: `U4R/InternAgent`; project page `alpha-innovator.github.io/InternAgent-project-page/`). A citing manuscript may refer to it as NovelSeek, InternAgent, or both. Everything below is stated in the paper's own terms as "InternAgent".

---

## Thesis / Problem
AI is transforming scientific research paradigms. The paper introduces **InternAgent, a unified closed-loop multi-agent framework** to conduct **Autonomous Scientific Research (ASR)** across diverse scientific fields — automating the full cycle from idea generation to experimental verification. It targets two central ASR challenges: (1) generating proposals that are both *effective and novel*, and (2) achieving *closed-loop feedback* for end-to-end experimental validation of those proposals (Sec. 1, lines 129-144).

## Method — what InternAgent is
A **unified closed-loop multi-agent framework** for ASR (abstract, line 102-104). It is an **end-to-end auto-research pipeline** covering **four main modules**: self-evolving idea generation, human-interactive feedback, idea-to-methodology construction, and multi-round experiment planning and execution (Sec. 1, lines 145-147).

Organized into **three primary capabilities** (Sec. 2, lines 195-198):
1. **Self-evolving Idea Generation with Human-interactive Feedback** (Sec. 2.1)
2. **Comprehensive Idea-to-Methodology Construction** (Sec. 2.2)
3. **Evolutionary Experimental Planning and Execution** / multi-round automated experiment execution (Sec. 2.3)

**It is a closed loop from hypothesis to verification** (title; conclusion lines 2231-2237). All experiments are **computational** (ML modeling / coding on datasets) — no physical/wet-lab robotics is performed by the system itself (though the intro's general ASD definition mentions robotics, lines 120-122).

**Specialized agents** (Sec. 2.1):
- **Survey Agent** — searches scientific papers; two modes: (1) *literature review mode* (broad keyword search, relevance scoring of abstracts via function R: L_abs × T → [0,1]) and (2) *deep research mode* (downloads/reads full texts, generates new keyword combinations).
- **Code Review Agent** — analyzes baseline code (repo- and file-level); uses Python `ast` for static analysis without execution and `multiprocessing` for scalability; two scenarios (review user code / search GitHub).
- **Idea Innovation Agent** — dual role: *idea generation* (high-temperature LLM, function G: (T,B,L)→I) and *idea evolution* (G: (I,C,L)→I′).
- **Assessment Agent** — multidimensional scoring across five dimensions: **coherence, credibility, verifiability, novelty, alignment**; scores 0–10, weighted summation; also enforces diversity among top-ranked ideas.
- **Human-interactive Feedback** — two types: human-provided and agent-generated.
- **Orchestration Agent** — coordinates all agents and timing of human feedback.
- **Method(ology) Development Agent** (Sec. 2.2) — *Methodology Initialization* (T: I×T×B×L→M) and *Methodology Refinement* (R: M×C×L→M′).
- **Coder module** (Sec. 2.3.1) — dual-strategy: **Aider** for single/limited-scope files; **OpenHands** for complex repo-level code. Exception-guided debugging cycle: (1) execution attempt, (2) exception capture/traceback, (3) contextual code understanding, (4) strategy formulation, (5) targeted implementation — iterated to threshold.
- **Adaptive Evolution (AE)** (Sec. 2.3.2) — structured iterative implementation with per-stage performance assessment and re-planning (vs. single-pass).

## EXACT NUMBER OF SCIENTIFIC TASKS/DOMAINS
**The paper states InternAgent spans exactly TWELVE (12) scientific research tasks** — stated repeatedly and consistently:
- Fig. 1 caption (line 91-94): "InternAgent can support **12 types of scientific research tasks** ranging from the AI field to the science field".
- Abstract (line 105): "demonstrated its versatility across **12 scientific research tasks**".
- Sec. 1 (line 157): "validated across **12 scientific research tasks**".
- Sec. 3.1.1 (line 842): "We select **12 distinct tasks**".
- Sec. 3.2 (line 1317): "InternAgent can support **12 different tasks**".
- Conclusion (line 2232): "supports **12 types of scientific research tasks**".

**Important nuance:** the "12 scientific research tasks" span **BOTH the AI field AND the science field** — they are not all natural-science tasks. They include AI/CV/NLP benchmark tasks (image classification, semantic segmentation, sentiment) alongside natural-science tasks (chemistry, biology, power systems).

**The 12 tasks (with internal names, datasets, baselines; Sec. 3.1.1):**
1. **Reaction Yield Prediction (AutoRYP)** — Suzuki-Miyaura dataset (Perera 2018), 5,760 reactions; baseline LoRA-finetuned LLaMA3-8B.
2. **Molecular Dynamics (AutoMD)** — MD17 (Chmiela 2017), 7 molecules; baseline VisNet.
3. **Power Flow Estimation (AutoPower)** — IEEE 39-Bus (39 buses, 10 generators, 19 load buses, 46 lines); baseline SenseFlow.
4. **Time Series Forecasting (AutoTSF)** — ETTh1; baseline DLinear (avg of 96/192/336/720).
5. **Transcription Prediction for Perturbation Response (AutoTPPR)** — Perturb-seq (Norman 2019); baseline GEARS.
6. **Enhancer Activity Prediction (AutoEAP)** — UMI-STARR-seq (Arnold 2013); baseline DeepSTARR.
7. **Sentiment Analysis / Classification (AutoSenCls)** — SST-2 (~67,000 train); baseline BERT-base.
8. **2D Image Classification (Auto2DCls)** — CIFAR-100 (60,000 imgs, 100 classes); baseline Wide Residual Networks (WRN).
9. **3D Point Cloud Classification (Auto3DCls)** — ModelNet40 (12,311 CAD, 40 categories); baseline PointNet.
10. **2D Semantic Segmentation (Auto2DSeg)** — Pascal VOC 2012 (20 classes+bg, 1,464 train / 1,449 val); baseline DeepLabV3Plus.
11. **3D Point Cloud Autonomous Driving (AutoPCDet)** — ONCE dataset; baseline CenterPoint (on OpenPCDet).
12. **Large Vision-Language Model Fine-tuning (AutoVLM)** — URSA geometry subset; baseline LLaVA-Onevision (SigLIP + Qwen2.5-Math-7B-Instruct); trained ≤20h on 8×A800.

Five modalities named (Sec. 3.1.1, line 843-846): science, time series, natural language, image, point cloud — covering both discriminative and generative tasks.

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| **12** scientific research tasks | Fig. 1 caption / abstract / Sec 1 / Sec 3.1.1 / Sec 3.2 / conclusion | Number of tasks InternAgent supports (see above) |
| 4 main modules | Sec. 1, line 145-147 | self-evolving idea gen, human-interactive feedback, idea-to-methodology, multi-round experiment planning/execution |
| 3 primary capabilities | Sec. 2, line 195-198 | idea gen w/ feedback; idea-to-methodology; evolutionary experiment execution |
| 3 key advantages | Abstract, line 104-114 | Scalability, Interactivity, Efficiency |
| Reaction yield: 27.6% → 35.4% in 12 hours | **Abstract**, line 111-112 | "increased from 27.6% to 35.4% in just 12 hours" (baseline→max, matches Table 1 R²) |
| Reaction yield: 24.2%±4.2 → 34.8%±1.1 in 12 hours | **Sec. 1**, line 160-162 | different framing: few-shot train-set=60 numbers (from Table 7), "human researchers typically require several months" |
| Enhancer activity: 0.65 → 0.79, 4 hours | Abstract line 112-113; Sec. 1 line 163-167 | Pearson correlation; baseline DeepSTARR 0.65 → 0.79 |
| 2D semantic segmentation: 78.8% → 81.0% in 30 hours | Abstract line 113-114; Sec. 3.2 line 1330-1332 | called "precision" in abstract but metric is **mIoU**; DeepLabV3Plus baseline |
| **Table 1 (Max Perf)** AutoRYP R²: 27.6 / 31.8(+4.2) / 35.4(+7.8) | Table 1, line 1066-1071 | Baseline / Dolphin / InternAgent |
| Table 1 AutoMD Forces-MAE: 0.158 / 0.152 / 0.148 | Table 1 | lower=better |
| Table 1 AutoTPPR MSE: 0.00473 / 0.00455 / 0.00426 | Table 1 | lower=better |
| Table 1 AutoEAP HK-PCC: 0.65 / 0.76 / 0.79 (max) | Table 1 | higher=better |
| Table 1 AutoTSF MAE: 0.197 / 0.173 / 0.146 (max) | Table 1 (columns scrambled in text extraction) | lower=better |
| Table 1 AutoPower RMSE: 0.4382 / … / 0.4331 (max) | Table 1 (scrambled) | lower=better |
| **Table 1 (Avg Perf)** AutoRYP R²: 27.6 / 31.3(+3.7) / 33.5(+5.9) | Table 1, line 1082-1094 | Baseline / Dolphin / InternAgent |
| **Table 2 (Max)** AutoSenCls Acc: 91.0 / 92.5(+1.5) / 93.5(+2.5) | Table 2, line 1144-1148 | |
| Table 2 Auto2DCls Top-1: 81.2 / 82.0(+0.8) / 83.3(+2.1) | Table 2 | |
| Table 2 Auto3DCls OA: 91.0 / 93.9(+2.9) / 95.5(+4.5) | Table 2 | |
| Table 2 Auto2DSeg mIoU: 78.8 / [Dolphin n/a] / 81.0(+2.2) | Table 2 | Dolphin can't do project-level |
| Table 2 AutoPCDet mAP: 65.0 / [n/a] / 65.9(+0.9) | Table 2 | |
| Table 2 AutoVLM QA: 67.1 / [n/a] / 67.6(+0.5) | Table 2 | |
| SoTA claim: 3D point cloud cls 95.5% (no pretraining) vs 95.3% (human, with pretraining) | Sec. 3.2, line 1176-1179 | Auto3DCls / ModelNet40 |
| AutoRYP: InternAgent +3.6 over Dolphin on max | Sec. 3.2, line 1176 | |
| **Table 3** improved/successful/tested (out of 10) | Table 3, line 1200-1219 | Dolphin vs InternAgent — AutoRYP 2/3/10 vs 4/6/10; AutoMD 2/4/10 vs 4/8/10; AutoPower 2/4/10 vs 5/6/10; AutoTSF 0/3/10 vs 3/7/10; AutoTPPR 2/3/10 vs 5/5/10; AutoEAP 2/4/10 vs 8/8/10 |
| **Table 4** improved/successful/tested | Table 4, line 1231-1259 | Auto2DCls 2/4/10 vs 5/7/10; Auto3DCls 2/5/10 vs 3/6/10; AutoSenCls 4/7/10 vs 9/9/10; Auto2DSeg [-] vs 6/9/10; AutoPCDet [-] vs 2/5/10; AutoVLM [-] vs 1/5/10 |
| AutoPCDet execution success 50%; Auto2DSeg 90% | Sec. 3.2, line 1306-1307 | 5/10 and 9/10 |
| **Table 5** Training time (A100 h): AutoRYP 6, AutoMD 10, AutoPower 5, AutoTSF 0.1, AutoTPPR 1, AutoEAP 1 | Table 5, line 1280-1303 | |
| Table 5 Idea-Gen cost (gpt-4o): $0.6 each (all tasks) | Table 5 | per idea |
| Table 5 Coder-Debug (claude-3.7-sonnet): 0.7/0.5/1.0/0.4/0.9/0.6 | Table 5 | per run |
| **Table 6** Training time (A100 h): Auto2DCls 2, Auto3DCls 0.8, AutoSenCls 0.3, Auto2DSeg 30, AutoPCDet 9, **AutoVLM 192** | Table 6, line 1358-1385 | AutoVLM most expensive |
| Table 6 Coder-Debug: 0.7/0.6/0.7/1.1/1.2/1.0 | Table 6 | |
| **Table 7** few-shot yield, train-set=60: Baseline 24.2±4.2, GAT 34.1±1.4, ADAGT 34.8±1.1 | Table 7, line 1405-1431 | 5 repeats; InternAgent reduces variance |
| Table 7 train-set=100: Baseline 35.5±4.9, GAT 37.4±4.0, ADAGT 38.7±1.7 | Table 7 | |
| **Table 8** Ablation AE — AutoRYP Max R²: Baseline 27.6, w/o AE 34.7, w/ AE 35.4 | Table 8, line 1506-1563 | |
| Table 8 Auto2DCls Max Acc: 81.2 / 81.6 / 83.3; Avg 81.2 / 81.5 / 82.2 | Table 8 | AE improves max +1.7, mean +0.7 (line 1713-1714) |
| Table 8 AutoSenCls Max Acc: 91.0 / 92.4 / 93.5; Avg 91.0 / 91.9 / 92.5 | Table 8 | |
| AE: AutoRYP perf-gain rate 40% vs 20% w/o AE | Sec. 3.3, line 1717-1718 | 4/10 vs 2/10 |
| **Table 9** AutoRYP Max R²: Baseline 27.6, AI-Scientist-V2 **12.3**, InternAgent 35.4 | Table 9, line 1666-1707 | AI-Scientist-V2 falls *below* baseline (struggles to write runnable code) |
| Table 9 total cost AutoRYP: AI-Scientist-V2 $15, AI-Researcher $25, InternAgent $3 | Table 9 | |
| Table 9 Auto2DCls Max Acc: Baseline 81.2, AI-Sci-V2 80.3, InternAgent 83.3 | Table 9 | AI-Researcher unable to improve baselines |
| Table 9 total cost Auto2DCls: AI-Sci-V2 $10, AI-Researcher $32, InternAgent $3 | Table 9 | |
| InternAgent ≈ 1/6 cost of AI-Researcher on AutoRYP | Sec. 3.3, line 1741-1742 | (table: $3 vs $25) |
| **Table 10** Human eval (soundness 1-4 / contribution 1-4 / overall 1-10 / confidence 1-5); 20 ideas/task, 5 reviewers | Table 10, line 2091-2178 | InternAgent vs AI-Scientist-V2 |
| Table 10 Reaction Yield: AI-Sci-V2 1.42/1.45/3.50/3.50; InternAgent 3.09/2.66/4.35/4.00 | Table 10 | |
| Table 10 2D Sem Seg: AI-Sci-V2 1.84/2.07/2.95/3.64; InternAgent 2.41/2.35/4.05/3.48 | Table 10 | |
| Table 10 2D Image Cls: AI-Sci-V2 2.78/2.82/4.40/3.87; InternAgent 3.15/3.10/5.85/3.32 | Table 10 | |
| Table 10 PC Autonomous Driving: AI-Sci-V2 2.15/2.47/3.10/3.94; InternAgent 2.75/2.95/5.10/4.10 | Table 10 | |
| Human eval covers 4 of the 12 tasks | Appendix B.2, line 2504-2508 | reaction yield, 2D sem seg, 2D image cls, PC autonomous driving |
| Reviewers ≥10 min/idea; must hold Ph.D. or be Ph.D. candidate w/ top-venue review experience (ICLR/ICML/NeurIPS/CVPR/ICCV/ACL) | Appendix B.2, line 2577-2586 | |
| **Implementation:** GPT-4o for survey/code-review/generation/self-evolving/orchestration agents | Sec. 3.1.3, line 983-984 | |
| Survey agent searches/reviews **50 papers**; idea-gen produces **15 ideas** | Sec. 3.1.3, line 985-986 | |
| Self-evolving: each idea → 3 ideas, select top 5, max **4** evolutions | Sec. 3.1.3, line 987-988 | |
| Idea-to-methodology: each idea initialized+refined **once** | Sec. 3.1.3, line 988-989 | |
| **Claude-3.7-Sonnet** for code generation/debug; max debug attempts **4** | Sec. 3.1.3, line 990-991 | |
| Max runs: **5** for Aider, **3** for OpenHands | Sec. 3.1.3, line 992-993 | |
| Fair-comparison: GPT-4o-2024-08-06 (idea) + Claude-3-7-Sonnet-20250219 (code) | Sec. 3.3, line 1732-1733 | vs AI-Researcher |
| Software: React frontend, cloud-native/Kubernetes backend; whitelist trial at discovery.intern-ai.org.cn | Appendix C, line 2594-2682 | "first end-to-end ASR multi-agent framework" |

## Scope & Explicit Limitations
- Human novelty evaluation covers only **4 of the 12 tasks** (cost-limited; Appendix B.2, line 2504).
- Paper concedes "we observed many promising phenomena, while also identifying **certain technical modules that require improvement**" (Sec. 1, line 188-189).
- **Future Outlook (Sec. 6)** names four unresolved technical challenges: (1) Knowledge Retrieval (incl. RAG to mitigate LLM hallucination), (2) Knowledge Understanding and Representation, (3) Agent Capability Enhancement (self-modification), (4) Scientific Discovery-related Benchmark Construction (evaluating an idea's *value* not just novelity, and method-vs-code alignment).
- Related Works concedes most current systems (incl. by implication) are "still evaluated primarily on relatively simple tasks or within narrow scientific domains" (Sec. 5, line 2220-2225).

## Does NOT claim / Boundaries
- Does **not** perform physical/wet-lab or robotic experiments; all 12 tasks are computational ML/coding on existing benchmark datasets (improving baseline model performance).
- Does **not** claim to discover new real-world scientific knowledge validated experimentally in the physical world — "verification" = running code and measuring benchmark metric improvements over baselines.
- Does **not** claim fully autonomous with zero human input as a requirement — human-interactive feedback is a *supported/optional* feature, and the framework can integrate expert feedback at multiple points.
- The "12 scientific research tasks" is **not** 12 purely natural-science domains — it explicitly mixes AI-field tasks (image cls, segmentation, sentiment, VLM) and science-field tasks (chemistry, biology, power). Do not overstate as "twelve scientific disciplines".
- Claims of being "first": conclusion says "closed-loop multi-agent framework **for the first time**" (line 2231); Appendix C says "**first** end-to-end ASR multi-agent framework" (line 2609-2610). It positions AI Scientist (Lu 2024) as "among the first" fully-automated ML pipeline (line 2200-2202), distinct from its own claim.
- Two different reaction-yield numbers appear (abstract 27.6→35.4; intro 24.2→34.8) — different experimental settings, not a contradiction; cite the matching one carefully.

## Section Map
- **Fig. 1** (p.1) — 12 tasks overview.
- **Abstract** — 3 advantages, 3 headline results.
- **Sec. 1 Introduction** — ASR challenges, 4 modules, contributions.
- **Sec. 2 InternAgent** — 2.1 Self-Evolving Idea Generation w/ Human Feedback (Survey/Code Review/Idea Innovation/Assessment/Orchestration Agents); 2.2 Idea-to-Methodology (2.2.1 Initialization, 2.2.2 Refinement); 2.3 Evolutionary Experimental Planning & Execution (2.3.1 Exception-Guided Debugging, 2.3.2 Planning & Adaptive Evolution).
- **Sec. 3 Experiments** — 3.1 Setup (3.1.1 Tasks, 3.1.2 Metrics, 3.1.3 Implementation); 3.2 Results (Tables 1-6); 3.3 Insightful Analyses (Tables 7-9, survey/idea/AE analyses).
- **Sec. 4 Case Studies** — 4.1 Qualitative (Figs 5-9), 4.2 Human Evaluation (Table 10).
- **Sec. 5 Related Works** — AI Scientist / AI Scientist-V2 / AI-Researcher / Dolphin / Agent Laboratory / AgentRxiv / AI Co-Scientist.
- **Sec. 6 Conclusion and Future Works** — summary + 4 future challenges.
- **References**, **Appendix A** (contributions), **B** (evaluation details/scoring criteria), **C** (software), **D** (result analysis, Figs 8-13).
