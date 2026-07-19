#!/usr/bin/env python3
"""Seed the citation-content-review ledger from the claims inventory.
Emits papers.tsv (59 paper rows) and ledger.tsv (atomic claim rows).
Re-running REGENERATES seeds only if the target is missing; use --force to overwrite
(overwriting discards recorded verdicts, so normally run once)."""
import os, sys, csv

HERE = os.path.dirname(os.path.abspath(__file__))
KB = "/Users/jaesolshin/Documents/GitHub/ai_scientist"

# ---- 59 papers: bibkey, relative-in-KB path, pages, type ----
PAPERS = [
 ("berk1966","0_Theoretical_Foundations/Berk 1966 - Limiting Behavior of Posterior Distributions when the Model is Incorrect.pdf",8,"short"),
 ("chaloner1995bayesian","0_Theoretical_Foundations/Chaloner Verdinelli 1995 - Bayesian Experimental Design A Review.pdf",33,"long"),
 ("ghosal2017fundamentals","0_Theoretical_Foundations/Ghosal van der Vaart 2017 - Fundamentals of Nonparametric Bayesian Inference.pdf",671,"textbook-TARGETED"),
 ("rainforth2024modern","0_Theoretical_Foundations/Modern Bayesian Experimental Design.pdf",14,"short"),
 ("foster2019variational","0_Theoretical_Foundations/Variational Bayesian Optimal Experimental Design.pdf",28,"long"),
 ("foster2021dad","0_Theoretical_Foundations/Deep Adaptive Design - Amortizing Sequential Bayesian Experimental Design.pdf",28,"long"),
 ("blau2022rl","0_Theoretical_Foundations/Reinforcement Learning for Bayesian Optimal Experimental Design.pdf",22,"long"),
 ("choudhury2026bedllm","0_Theoretical_Foundations/BED-LLM - Intelligent Information Gathering with LLMs and Bayesian Experimental Design.pdf",31,"long"),
 ("taniguchi2024cpc","0_Theoretical_Foundations/Taniguchi 2024 - Collective Predictive Coding as Model of Science.pdf",23,"long"),
 ("kaelbling1998pomdp","1_AI_Scientist_Core/Reference/Kaelbling 1998 - Planning and Acting in Partially Observable Stochastic Domains (POMDP).pdf",36,"long"),
 ("lu2024aiscientist","1_AI_Scientist_Core/Core_Systems/The AI Scientist_ Towards Fully Automated Open-Ended Scientific Discovery.pdf",186,"very-long"),
 ("lu2026aiscientist","1_AI_Scientist_Core/Core_Systems/Towards end-to-end automation of AI research.pdf",9,"short"),
 ("gottweis2026coscientist","1_AI_Scientist_Core/Core_Systems/Gottweis 2026 - Accelerating Scientific Discovery with Co-Scientist (Nature).pdf",28,"long"),
 ("aygun2026era","1_AI_Scientist_Core/Core_Systems/ERA - An AI System to Help Scientists Write Expert-Level Empirical Software.pdf",78,"very-long"),
 ("boiko2023emergent","1_AI_Scientist_Core/Core_Systems/Boiko 2023 - Autonomous Chemical Research with LLMs.pdf",48,"very-long"),
 ("schmidgall2025agentlab","1_AI_Scientist_Core/Core_Systems/Agent Laboratory - Using LLM Agents as Research Assistants.pdf",84,"very-long"),
 ("liu2026lasthuman","1_AI_Scientist_Core/Core_Systems/The Last Human-Written Paper - Agent-Native Research Artifacts.pdf",46,"very-long"),
 ("si2024novelideas","1_AI_Scientist_Core/Reference/Can Large Language Models Generate Novel Research Ideas.pdf",94,"very-long"),
 ("baek2024researchagent","1_AI_Scientist_Core/Reference/ResearchAgent - Iterative Research Idea Generation over Scientific Literature.pdf",30,"long"),
 ("gu2024scimuse","1_AI_Scientist_Core/Reference/SciMuse - Interesting Scientific Idea Generation using Knowledge Graphs and LLMs.pdf",14,"short"),
 ("huang2025popper","1_AI_Scientist_Core/Reference/Popper - Automated Hypothesis Validation with Agentic Sequential Falsifications.pdf",65,"very-long"),
 ("liu2024aigs","1_AI_Scientist_Core/Reference/AIGS Generating Science from AI-Powered Automated Falsification.pdf",36,"long"),
 ("liu2025researchbench","1_AI_Scientist_Core/Reference/ResearchBench Benchmarking LLMs in Scientific Discovery.pdf",21,"long"),
 ("kim2026aireviewers","1_AI_Scientist_Core/Reference/On the limits and opportunities of AI reviewers.pdf",91,"very-long"),
 ("lee2025spacer","1_AI_Scientist_Core/Reference/Spacer - Towards Engineered Scientific Inspiration.pdf",48,"very-long"),
 ("zhang2025novelseek","1_AI_Scientist_Core/Reference/NovelSeek - When Agent Becomes the Scientist.pdf",34,"long"),
 ("sparkes2010robot","1_AI_Scientist_Core/Reference/Sparkes 2010 - Towards Robot Scientists for Autonomous Scientific Discovery.pdf",11,"short"),
 ("aher2023turing","2_Domain_Applications/Social_Science/Using LLMs to Simulate Multiple Humans and Replicate Human Subject Studies.pdf",43,"very-long"),
 ("manning2024automated","2_Domain_Applications/Social_Science/Automated Social Science - Language Models as Scientist and Subjects.pdf",63,"very-long"),
 ("park2023generative","2_Domain_Applications/Social_Science/Generative Agents - Interactive Simulacra of Human Behavior.pdf",22,"long"),
 ("bran2023chemcrow","2_Domain_Applications/Chemistry/ChemCrow - Augmenting large-language models with chemistry tools.pdf",38,"long"),
 ("gromski2019chemical","2_Domain_Applications/Chemistry/Gromski 2019 - How to Explore Chemical Space Using Algorithms and Automation.pdf",10,"short"),
 ("sprueill2024chemreasoner","2_Domain_Applications/Chemistry/ChemReasoner - Heuristic Search over LLM Knowledge Space for Catalyst Discovery.pdf",24,"long"),
 ("kamber2026chemist","2_Domain_Applications/Chemistry/Kamber 2026 - Making Claude a Chemist.pdf",13,"report"),
 ("cheetham2024gnome","2_Domain_Applications/Materials/Cheetham 2024 - AI Driving Materials Discovery (Perspective on GNoME).pdf",7,"short"),
 ("merchant2023gnome","2_Domain_Applications/Materials/GNoME - Scaling deep learning for materials discovery.pdf",11,"short"),
 ("jumper2021alphafold","2_Domain_Applications/Biology/AlphaFold2 - Highly accurate protein structure prediction.pdf",12,"short"),
 ("odonoghue2023bioplanner","2_Domain_Applications/Biology/BioPlanner - Automatic Evaluation of LLMs on Protocol Planning in Biology.pdf",19,"long"),
 ("yanai2019night","2_Domain_Applications/Biology/Yanai Lercher 2019 - Night Science.pdf",3,"editorial"),
 ("romera2023funsearch","2_Domain_Applications/Mathematics/FunSearch - Mathematical discoveries from program search.pdf",14,"short"),
 ("google2026aletheia","2_Domain_Applications/Mathematics/Towards Autonomous Mathematics Research.pdf",42,"very-long"),
 ("xin2024deepseek","2_Domain_Applications/Mathematics/DeepSeek-Prover-V1.5.pdf",28,"long"),
 ("leiden2026","2_Domain_Applications/Mathematics/Leiden Declaration on AI and Mathematics.pdf",11,"declaration"),
 ("udrescu2020afeynman","2_Domain_Applications/Physics/AI Feynman - A physics-inspired method for symbolic regression.pdf",15,"short"),
 ("cranmer2020symbolic","2_Domain_Applications/Physics/Discovering Symbolic Models from Deep Learning with Inductive Biases.pdf",25,"long"),
 ("real2020automlzero","2_Domain_Applications/CS/AutoML-Zero - Evolving Machine Learning Algorithms From Scratch.pdf",23,"long"),
 ("surina2025algodiscovery","2_Domain_Applications/CS/Algorithm Discovery with LLMs - Evolutionary Search Meets Reinforcement Learning.pdf",34,"long"),
 ("jaber2026autokernel","2_Domain_Applications/CS/AutoKernel - Autonomous GPU Kernel Optimization via Iterative Agent-Driven Search.pdf",11,"short"),
 ("jagadish2026automatize","2_Domain_Applications/Neuroscience/Jagadish 2026 - Automatize Scientific Discovery in Cognitive Sciences.pdf",5,"editorial"),
 ("park2023disruptive","4_Epistemic_Agents_Risk/Science_of_Science/Park2023 - Papers and Patents Are Becoming Less Disruptive Over Time.pdf",56,"very-long"),
 ("uzzi2013atypical","4_Epistemic_Agents_Risk/Science_of_Science/Uzzi2013 - Atypical Combinations and Scientific Impact.pdf",6,"short"),
 ("zollman2010epistemic","4_Epistemic_Agents_Risk/Science_of_Science/Zollman 2010 - The Epistemic Benefit of Transient Diversity.pdf",28,"long"),
 ("geng2025reliable","4_Epistemic_Agents_Risk/Are LLMs Reliable AI Scientists - Assessing Reverse-Engineering of Black-Box Systems.pdf",30,"long"),
 ("vafa2025foundationmodel","4_Epistemic_Agents_Risk/What Has a Foundation Model Found - Inductive Bias Probe for World Models.pdf",21,"long"),
 ("zhao2026hallucinations","4_Epistemic_Agents_Risk/LLM Hallucinations in the Wild Large-Scale Evidence from Non-Existent Citations.pdf",16,"long"),
 ("darvish2024organa","5_Wet_Lab_Infrastructure/ORGANA A Robotic Assistant for Automated Chemistry Experimentation and Characterization.pdf",49,"very-long"),
 ("panapitiya2025autolabs","5_Wet_Lab_Infrastructure/AutoLabs Cognitive Multi-Agent Systems with Self-Correction for Autonomous Chemical Experimentation.pdf",39,"long"),
 ("szymanski2023alab","5_Wet_Lab_Infrastructure/A-Lab - An Autonomous Laboratory for the Accelerated Synthesis of Inorganic Materials.pdf",13,"short"),
 ("tobias2025selfdriving","5_Wet_Lab_Infrastructure/Autonomous Self-Driving Laboratories Review of Technology and Policy Implications.pdf",25,"long"),
]

# ---- Atomic claims: (bibkey, loc, type, claim_text) ----
# type in {NUM, METHOD, CHAR, BG, UNCITED}
C = [
 # boiko2023emergent
 ("boiko2023emergent","L69 Intro","BG","Grouped in 'AI Scientist systems have proliferated rapidly'."),
 ("boiko2023emergent","L69 Intro","CHAR","Characterized as a tool-augmented synthesis agent (Coscientist)."),
 ("boiko2023emergent","L90 Related","BG","Prior work gives qualitative characterization of individual systems, no shared framework."),
 ("boiko2023emergent","L166 Core","CHAR","Coscientist has only constrained task-level feedback; measured outcomes inform later choices; loop is partial; novelty/significance validation human-mediated."),
 # lu2024aiscientist
 ("lu2024aiscientist","L69 Intro","BG","Grouped in 'proliferated rapidly'."),
 ("lu2024aiscientist","L69 Intro","CHAR","Characterized as a closed-loop manuscript-writing pipeline (The AI Scientist)."),
 ("lu2024aiscientist","L90 Related","BG","Prior qualitative characterization, no shared framework."),
 ("lu2024aiscientist","L166 Core","METHOD","Adds V_s via a 5-ensemble GPT-4o reviewer."),
 ("lu2024aiscientist","L166 Core","NUM","Reviewer balanced accuracy 0.65 vs human 0.66."),
 ("lu2024aiscientist","L166 Core","CHAR","Enables the first structurally closed loop on a biased, uncalibrated V."),
 ("lu2024aiscientist","L215 OpenProb","METHOD","Uses a 1-10 novelty/significance score collapsing distinct properties into one scalar."),
 # lu2026aiscientist
 ("lu2026aiscientist","L69 Intro","BG","Grouped in 'proliferated rapidly'."),
 ("lu2026aiscientist","L69 Intro","CHAR","The AI Scientist closed-loop manuscript-writing pipeline (with lu2024)."),
 ("lu2026aiscientist","L90 Related","BG","Prior qualitative characterization, no shared framework."),
 ("lu2026aiscientist","L166 Core","METHOD","Stacks V_e (replication nodes with mean +/- s.d.), V_s (automated reviewer), and actual peer review (V_h via ICLR workshop)."),
 ("lu2026aiscientist","L166 Core","NUM","Automated reviewer balanced accuracy 0.69."),
 ("lu2026aiscientist","L166 Core","CHAR","Gives the most V layers in the class; internal automated acceptance gate stays uncalibrated."),
 # schmidgall2025agentlab
 ("schmidgall2025agentlab","L69 Intro","BG","Grouped in 'proliferated rapidly'."),
 ("schmidgall2025agentlab","L90 Related","BG","Prior qualitative characterization, no shared framework."),
 ("schmidgall2025agentlab","L166 Core","NUM","Agent Laboratory documents +2.3-point systematic over-estimation relative to human PhD students (NOTE: sentence cites kim2026aireviewers, not schmidgall) -- check attribution."),
 # google2026aletheia
 ("google2026aletheia","L69 Intro","BG","Grouped in 'proliferated rapidly'."),
 ("google2026aletheia","L69 Intro","CHAR","Characterized as a formal-mathematics agent (Aletheia)."),
 ("google2026aletheia","L176 Domain","BG","Listed under mathematics, natural-language."),
 ("google2026aletheia","L438 App-Domain","CHAR","Produces natural-language proofs scored by LLM and human judgment; loop closes mechanically but V_sem imperfect."),
 ("google2026aletheia","L438 App-Domain","NUM","Of 200 audited Erdos solutions only 13 (6.5%) rated meaningfully correct."),
 # liu2026lasthuman
 ("liu2026lasthuman","L69 Intro","BG","Grouped in 'proliferated rapidly'."),
 ("liu2026lasthuman","L96 Related","CHAR","Addresses the artifact layer -- output format and verification protocol -- rather than the discovery loop."),
 ("liu2026lasthuman","L171 Artifact","METHOD","ARA replaces narrative paper with a four-layer ontology (/logic,/src,/trace,/evidence); Seal automates V_syntax, V_semantic (Rigor Auditor), V_empirical; reserves V_human for significance/novelty."),
 ("liu2026lasthuman","L171 Artifact","NUM","Rigor Auditor 82.6% detection."),
 ("liu2026lasthuman","L171 Artifact","UNCITED","(uncited clause) only 45.4% of papers fully specify reproduction requirements and 90.2% of extension cost is failed exploration."),
 ("liu2026lasthuman","L211 OpenProb","NUM","Rigor Auditor achieves 82.6% average detection across five structural violation types but only 22% on orphaned-experiment violations."),
 ("liu2026lasthuman","L249 Discussion","BG","ARA a plausible entry point for shared memory w."),
 # jumper2021alphafold
 ("jumper2021alphafold","L73 Scope","CHAR","Cited as a specialized predictor without a generation-and-search loop (excluded from scope)."),
 # kaelbling1998pomdp
 ("kaelbling1998pomdp","L78 Background","BG","Grounding: model AI Scientist systems as POMDPs (belief b(s) updated by observations)."),
 ("kaelbling1998pomdp","L94 Related","BG","POMDP framework is classical."),
 # chaloner1995bayesian
 ("chaloner1995bayesian","L78 Background","BG","BED provides a normative criterion (EIG) for the search policy's information objective."),
 ("chaloner1995bayesian","L94 Related","BG","BED is classical."),
 # rainforth2024modern
 ("rainforth2024modern","L78 Background","BG","BED provides a normative EIG criterion (with chaloner)."),
 ("rainforth2024modern","L94 Related","BG","BED is classical."),
 # foster2019variational
 ("foster2019variational","L85 Background","CHAR","EIG can be approximated via variational methods."),
 # foster2021dad
 ("foster2021dad","L85 Background","CHAR","EIG can be approximated via amortized policies."),
 ("foster2021dad","L219 OpenProb","BG","In LLM systems the 'posterior' is implicit in model weights."),
 ("foster2021dad","L223 OpenProb","CHAR","Amortized EIG estimation, which remains unsolved for open-ended S."),
 # blau2022rl
 ("blau2022rl","L85 Background","CHAR","EIG can be approximated via RL."),
 # sparkes2010robot
 ("sparkes2010robot","L85 Background","METHOD","Robot Scientist's experiment selection is a domain-specific active-learning approximation."),
 ("sparkes2010robot","L92 Related","METHOD","Robot Scientist integrated hypothesis generation, robotic experimentation, and statistical validation in yeast functional genomics."),
 ("sparkes2010robot","L92 Related","CHAR","Instantiated all six SERVO components including active-learning policy, in physical wet-lab form more than a decade before LLM systems."),
 ("sparkes2010robot","L94 Related","METHOD","Most direct historical exemplar of Bayesian-optimal experiment selection: the active-learning policy."),
 ("sparkes2010robot","L162 Table1","BG","Identified as the pre-LLM Robot Scientist in Table 1."),
 # merchant2023gnome
 ("merchant2023gnome","L85 Background","METHOD","GNoME's DFT-in-the-loop active learning is an active-learning approximation."),
 ("merchant2023gnome","L176 Domain","BG","Listed under materials."),
 ("merchant2023gnome","L219 OpenProb","METHOD","Deep-ensemble uncertainty sampling approximates EIG over a tractable GNN posterior; DFT provides well-calibrated computational V."),
 ("merchant2023gnome","L230 OpenProb","NUM","GNoME predicts 380,000 stable compounds via DFT."),
 ("merchant2023gnome","L444 App-Domain","NUM","Predicts 2.2 million candidate structures (380,000 stable)."),
 ("merchant2023gnome","L444 App-Domain","METHOD","Runs DFT-in-the-loop active learning with uncertainty sampling approximating the BED ideal within the computational surrogate."),
 # si2024novelideas
 ("si2024novelideas","L90 Related","CHAR","Idea-generation study establishing quality baselines without unifying the full discovery loop."),
 # baek2024researchagent
 ("baek2024researchagent","L90 Related","CHAR","Idea-generation study establishing quality baselines without unifying the full discovery loop."),
 # gu2024scimuse
 ("gu2024scimuse","L90 Related","CHAR","Knowledge-graph-driven ideation; structuring semantic memory as relational corpus substantially improves hypothesis-generation quality; does not close the loop."),
 # lee2025spacer
 ("lee2025spacer","L90 Related","CHAR","Knowledge-graph-driven ideation (with gu2024); improves hypothesis-generation quality; does not close the loop."),
 # zhang2025novelseek
 ("zhang2025novelseek","L92 Related","NUM","NovelSeek: closed-loop multi-agent system spanning idea generation to verification across twelve scientific tasks."),
 ("zhang2025novelseek","L162 Table1","BG","Identified as the recent unified framework NovelSeek in Table 1."),
 # gottweis2026coscientist
 ("gottweis2026coscientist","L92 Related","CHAR","Co-Scientist: multi-agent hypothesis-generation system with experimental biomedical validation."),
 # taniguchi2024cpc
 ("taniguchi2024cpc","L96 Related","CHAR","Propose Collective Predictive Coding (CPC-MS) as a social model of science, recasting scientific activity as decentralized Bayesian inference across a community."),
 ("taniguchi2024cpc","L96 Related","UNCITED","(adjacent clause attributed to CPC) peer review is a Metropolis-Hastings consensus process."),
 ("taniguchi2024cpc","L249 Discussion","BG","A collective validator (extension to multi-agent collective with shared memory w)."),
 ("taniguchi2024cpc","L251 Discussion","BG","The single-agent framing's social layer is abstracted away by SERVO."),
 # romera2023funsearch
 ("romera2023funsearch","L176 Domain","BG","Listed under mathematics, formal."),
 ("romera2023funsearch","L436 App-Domain","CHAR","FunSearch validates against a formal/numeric oracle -- an evaluator function returning deterministic pass/fail."),
 # xin2024deepseek
 ("xin2024deepseek","L176 Domain","BG","Listed under mathematics, formal."),
 ("xin2024deepseek","L436 App-Domain","CHAR","DeepSeek-Prover validates against a proof kernel returning deterministic pass/fail."),
 # udrescu2020afeynman
 ("udrescu2020afeynman","L176 Domain","BG","Listed under physics."),
 ("udrescu2020afeynman","L440 App-Domain","CHAR","AI Feynman fits equations to data with deterministic search; no memory transfer across problems."),
 # cranmer2020symbolic
 ("cranmer2020symbolic","L176 Domain","BG","Listed under physics."),
 ("cranmer2020symbolic","L440 App-Domain","CHAR","Symbolic-model discovery fits equations to data with deterministic search."),
 # bran2023chemcrow
 ("bran2023chemcrow","L176 Domain","BG","Listed under chemistry."),
 ("bran2023chemcrow","L442 App-Domain","CHAR","ChemCrow validates computationally with surrogate signals and searches by beam."),
 # sprueill2024chemreasoner
 ("sprueill2024chemreasoner","L176 Domain","BG","Listed under chemistry."),
 ("sprueill2024chemreasoner","L442 App-Domain","CHAR","ChemReasoner validates computationally with surrogate signals and searches by beam."),
 # kamber2026chemist
 ("kamber2026chemist","L176 Domain","BG","Listed under chemistry."),
 ("kamber2026chemist","L442 App-Domain","BG","Physical characterization (NMR, MS) leaves the wet-lab loop open."),
 # odonoghue2023bioplanner
 ("odonoghue2023bioplanner","L176 Domain","BG","Listed under biology."),
 ("odonoghue2023bioplanner","L230 OpenProb","CHAR","BioPlanner's V metrics are insufficient to close the loop autonomously; physical execution never reached."),
 ("odonoghue2023bioplanner","L446 App-Domain","CHAR","Generates experimental protocols; validation signals weak, biological-validity metrics insufficient; effectively no search policy beyond generation."),
 # manning2024automated
 ("manning2024automated","L176 Domain","BG","Listed under social science."),
 ("manning2024automated","L448 App-Domain","CHAR","Automated-social-science pipelines validate with statistical tests over full-factorial designs."),
 # aher2023turing
 ("aher2023turing","L176 Domain","BG","Listed under social science."),
 ("aher2023turing","L200 Domain","CHAR","Social science suffers circular validity when G and E share a model."),
 ("aher2023turing","L448 App-Domain","CHAR","LLM-simulation study validating with statistical tests over full-factorial designs."),
 ("aher2023turing","L448 App-Domain","CHAR","Characteristic failure is circular validity: validator measures model self-consistency rather than external fact."),
 # park2023generative
 ("park2023generative","L176 Domain","BG","Listed under social science."),
 ("park2023generative","L448 App-Domain","CHAR","LLM-simulation study (with aher2023) validating with statistical tests."),
 # real2020automlzero
 ("real2020automlzero","L176 Domain","BG","Listed under CS/algorithms."),
 ("real2020automlzero","L450 App-Domain","CHAR","AutoML-Zero closes the loop via reliable benchmark/empirical validation and evolutionary search; residual bottleneck interpretability."),
 # surina2025algodiscovery
 ("surina2025algodiscovery","L176 Domain","BG","Listed under CS/algorithms."),
 ("surina2025algodiscovery","L450 App-Domain","CHAR","Algorithm discovery closes the loop via reliable empirical validation and LLM-guided search."),
 # jaber2026autokernel
 ("jaber2026autokernel","L176 Domain","BG","Listed under CS/algorithms."),
 ("jaber2026autokernel","L450 App-Domain","CHAR","AutoKernel closes the loop via reliable empirical validation and search."),
 # cheetham2024gnome
 ("cheetham2024gnome","L200 Domain","CHAR","Most predicted compounds still require synthesis and characterization; physical loop only partly closed."),
 ("cheetham2024gnome","L230 OpenProb","NUM","Only 736 GNoME compounds have been independently experimentally realized."),
 ("cheetham2024gnome","L444 App-Domain","NUM","Of predicted stable structures only 736 independently experimentally realized."),
 ("cheetham2024gnome","L444 App-Domain","CHAR","Critics note predicted compounds should not be equated with validated materials exhibiting demonstrated functionality."),
 # kim2026aireviewers
 ("kim2026aireviewers","L166 Core","NUM","(attribution) +2.3-point systematic over-estimation relative to human PhD students -- verify origin (kim vs schmidgall/AgentLab)."),
 ("kim2026aireviewers","L211 OpenProb","NUM","A 45-expert evaluation positions AI reviewers as complements not substitutes; they share blind spots and overlap far more than independent humans."),
 ("kim2026aireviewers","L249 Discussion","CHAR","AI reviewers already overlap far more than humans."),
 # geng2025reliable
 ("geng2025reliable","L211 OpenProb","METHOD","LLMs asked to reverse-engineer black-box systems fail to do so reliably even with systematic query access."),
 # leiden2026
 ("leiden2026","L211 OpenProb","NUM","Leiden Declaration signed by over 130 mathematicians."),
 ("leiden2026","L211 OpenProb","CHAR","Corroborates indispensability of expert oversight: AI proofs may contain almost-invisible errors resisting detection without human scrutiny."),
 ("leiden2026","L438 App-Domain","CHAR","AI-produced NL proofs may contain almost-invisible errors; V_human not replaceable."),
 # liu2025researchbench
 ("liu2025researchbench","L213 OpenProb","METHOD","Recent benchmark restricts to post-2024 findings to control contamination; evaluates inspiration-based decomposition rather than closing the expert-baseline gap."),
 # park2023disruptive
 ("park2023disruptive","L215 OpenProb","BG","Cited as an example of a disruption measure for 'novel to the field'."),
 # uzzi2013atypical
 ("uzzi2013atypical","L215 OpenProb","BG","Cited as an example of an atypicality measure for 'novel to the field'."),
 # choudhury2026bedllm
 ("choudhury2026bedllm","L219 OpenProb","METHOD","BED-LLM derives a usable EIG posterior from an LLM's predictive distributions, but for conversational queries rather than experiment design."),
 # liu2024aigs
 ("liu2024aigs","L219 OpenProb","METHOD","AIGS selects hypotheses by their survival of automated refutation; does not compute/maximize EIG."),
 # huang2025popper
 ("huang2025popper","L219 OpenProb","METHOD","Popper runs sequential falsification experiments with statistical error control; does not compute/maximize EIG."),
 # yanai2019night
 ("yanai2019night","L223 OpenProb","BG","How genuinely new hypotheses/representations arise falls outside current BED formulations."),
 # gromski2019chemical
 ("gromski2019chemical","L230 OpenProb","BG","NMR and MS characterization require physical execution that no current system knows when to invoke."),
 # jagadish2026automatize
 ("jagadish2026automatize","L230 OpenProb","CHAR","Uses a behavioral foundation model as proxy E (synthetic participant data); gives no criterion for escalating to in-vivo validation; flags synthetic data as accelerator not ground truth."),
 # aygun2026era
 ("aygun2026era","L230 OpenProb","CHAR","ERA optimizes within a fixed computational evaluator, generating expert-level empirical software judged by a held-out quality metric without physical escalation."),
 # szymanski2023alab
 ("szymanski2023alab","L234 OpenProb","NUM","A-Lab couples computational screening to robotic synthesis, reportedly realizing 36 of 57 targeted compounds; escalates by a fixed screen-then-synthesize rule."),
 # darvish2024organa
 ("darvish2024organa","L234 OpenProb","CHAR","ORGANA automates the physical execution of wet-lab experiments."),
 # panapitiya2025autolabs
 ("panapitiya2025autolabs","L234 OpenProb","CHAR","AutoLabs: self-correcting multi-agent system automating generation of hardware-ready protocols."),
 # tobias2025selfdriving
 ("tobias2025selfdriving","L234 OpenProb","BG","Reviews document the rapid maturation of the underlying hardware."),
 # zhao2026hallucinations
 ("zhao2026hallucinations","L245 Discussion","METHOD","Documented ecosystem-scale surge in fabricated citations."),
 # vafa2025foundationmodel
 ("vafa2025foundationmodel","L245 Discussion","METHOD","Strong task performance need not imply an internalized world model."),
 # zollman2010epistemic
 ("zollman2010epistemic","L249 Discussion","CHAR","Transient diversity benefits epistemic communities (must preserve epistemic diversity)."),
 # ghosal2017fundamentals
 ("ghosal2017fundamentals","L404 App-Formal","BG","Standard sufficient condition for Bayesian posterior consistency (well-specified identifying likelihood with divergent accumulated info on compact Theta)."),
 # berk1966
 ("berk1966","L408 App-Formal","BG","Under theta-dependent (non-affine) coupled validator, posterior concentrates on the KL projection theta-dagger, distinct from theta-star."),
 ("berk1966","L411 App-Formal","BG","A coupled misspecified update likelihood places the posterior at its KL minimizer."),
]

def main():
    force = "--force" in sys.argv
    p_path = os.path.join(HERE,"papers.tsv")
    l_path = os.path.join(HERE,"ledger.tsv")
    if (os.path.exists(p_path) or os.path.exists(l_path)) and not force:
        print("papers.tsv/ledger.tsv already exist; refusing to overwrite (use --force). Nothing done.")
        return
    with open(p_path,"w",newline="") as f:
        w=csv.writer(f,delimiter="\t")
        w.writerow(["bibkey","pdf_path","pages","type","read_status","n_claims","n_verified"])
        counts={}
        for bk,rel,pg,ty in PAPERS:
            counts[bk]=sum(1 for c in C if c[0]==bk)
        for bk,rel,pg,ty in PAPERS:
            w.writerow([bk, os.path.join(KB,rel), pg, ty, "PENDING", counts[bk], 0])
    with open(l_path,"w",newline="") as f:
        w=csv.writer(f,delimiter="\t")
        w.writerow(["claim_id","bibkey","loc","type","status","verdict","claim_text","evidence","fix"])
        for i,(bk,loc,ty,txt) in enumerate(C,1):
            w.writerow([f"C{i:03d}",bk,loc,ty,"PENDING","",txt,"",""])
    print(f"Wrote {len(PAPERS)} papers, {len(C)} claims.")
    # sanity: every paper has >=1 claim; every claim bibkey is a known paper
    pk={p[0] for p in PAPERS}; ck={c[0] for c in C}
    print("papers w/o claims:", sorted(pk-ck))
    print("claim keys not in papers:", sorted(ck-pk))

if __name__=="__main__":
    main()
