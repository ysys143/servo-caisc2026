# Digest: darvish2024organa

**Title:** Organa: A Robotic Assistant for Automated Chemistry Experimentation and Characterization
**Authors:** Kourosh Darvish, Marta Skreta, Yuchi Zhao, Naruki Yoshikawa, Sagnik Som, Miroslav Bogdanovic, Yang Cao, Han Hao, Haoping Xu, Alán Aspuru-Guzik, Animesh Garg, Florian Shkurti
**Venue/ID:** arXiv:2401.06949v2 [cs.RO], 7 Jan 2025 (Cell Press *Device*-style formatting; "Experimental Procedures", "Lead contact", supplemental Notes S1–S9). Project page: https://ac-rad.github.io/organa/ ; code: https://github.com/ac-rad/organa
**PDF:** 49 pages (main + Supplemental Notes S1–S9).

---

## Thesis / Problem

Chemistry experiments are resource- and labor-intensive (e.g., manually polishing electrodes in electrochemistry), and traditional lab-automation infrastructure adapts poorly to new experiments. Organa is an **assistive robotic system that automates diverse physical chemistry experiments** using perception + decision-making tools, keeping chemists in the loop. It uses LLMs to derive experiment goals, handle disambiguation, and generate experiment logs/reports; it plans and executes tasks with visual feedback and supports scheduling + parallel execution. It is a continuation of the authors' prior work CLAIRify [7]/[67].

## Method — DOES IT AUTOMATE PHYSICAL EXECUTION? **YES.**

Organa **physically executes** wet-lab chemistry with a real robot arm + real lab hardware. This is real-world robotic execution, not simulation.

- **Robot & hardware:** Franka Emika Panda arm + Robotiq 2F-85 gripper; Dynamixel XM540-W150 servo for extra DOF; Cavro XCalibur syringe pump (12-port ceramic valve, Tecan); IKA RET control-visc (heating/stirring/weighing); Sartorius BCA2202-1S scale; Orion ROSS pH probe; portable low-cost potentiostat [47]; robotic polishing station [14]; Intel RealSense D435i + ZED Mini cameras.
- **Four physical experiments actually run by the robot:**
  1. **Solubility screening** — robot iteratively pours water, stirs, estimates turbidity via in-hand-camera vision (adapted from HeinSight [19]); solutes: salt (NaCl), sugar (sucrose), alum (KAl(SO₄)₂).
  2. **Recrystallization** — alum; modified solubility test with pre-heated solvent; robot produces crystals.
  3. **pH testing** — red-cabbage anthocyanin indicator; robot pours acetic acid (vinegar) and sodium bicarbonate (baking soda) to show color change.
  4. **Electrochemistry** — measures redox potential of a quinone (AQS) solution at different pH, builds a Pourbaix diagram; **includes fully automated mechanical polishing of a glassy-carbon working electrode** (a labor-intensive manual step), then OCP + cyclic voltammetry with a 3-electrode system.
- **Physical robot skills implemented:** pick&place + insertion (IK via TRAC-IK [79], PRM* [80] path planning); constrained motion planning (orientation constraints to prevent spills); liquid + granular powder pouring (weight-feedback PD controller); electrode polishing (polishing station + robot arm).
- **Planning/reasoning stack (software):** Organa.Reasoner (GPT-4 for interaction/reasoning, Whisper speech-to-text, ElevenLabs text-to-speech; ReAct prompting; CLAIRify/GPT-3.5-turbo to convert NL→XDL); Organa.Planner (Temporal-PDDLStream = PDDLStream [25] adapted with PDDL2.1 [39] durative actions + a time-variant cost function for simultaneous TAMP + scheduling → parallel execution); Organa.Perception (Grounding DINO [71] + SAM [74] + PCA pose estimation on ZED depth); Organa.Analyzer (MLE + posterior/marginal parameter estimation, auto PDF report generation).

**IMPORTANT nuance (for citation accuracy):** The RESULTS demonstrations (solubility, recrystallization, pH, and the 3 complete electrochemistry runs) were **physically executed** by the robot. HOWEVER, the *user-study interaction portion* deliberately did NOT physically re-run experiments: the Organa-experiment task script states "Note: we won't actually be running the experiment, we will call values from a previous experiment in the backend" — this replay was only to keep the human-interaction test consistent across the 8 participants. So: physical execution is genuine for the demonstrations; the user-study interaction sessions used backend-replayed values.

---

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| Automates solubility, pH, recrystallization, electrochemistry | Abstract; Results | Four fundamental chemistry experiments physically executed |
| 19-step plan executed in parallel | Abstract; Results (parallel exec) | Electrochemistry quinone characterization for flow batteries |
| Frustration & physical demand reduced by >50% | Abstract | User study result |
| Users save avg **80.3%** of time | Abstract | Overall time saving with Organa |
| Solubility = mass of solute dissolved in 100 g solvent | Solubility section | Definition used |
| Accuracy 7.2% (salt/NaCl), 11.2% (sugar/sucrose), 12.3% (alum) | Solubility section | Error vs literature [42] |
| Solubility: 7-step plan, avg **25.63 min** per test, run 2× | Solubility; Autonomy eval | Execution time |
| Recrystallization: 8-step plan, **44.80 min**, run 1× | Recrystallization; Autonomy eval | Alum recrystallization |
| pH: 6-step plan, **3.85 min**, run 1× | pH; Autonomy eval | Red cabbage indicator demo |
| Electrochemistry: 114 (=6×19) steps, **130.00 min**, run 2× | Autonomy eval | Full electrochemistry campaign |
| Solution: 2 mM sodium AQS (Sigma Aldrich) + 0.1 M NaCl + 0.1 M buffer | Electrochem setup | AQS = anthraquinone-2-sulfonate |
| Buffers: acetate (pH 4,5), phosphate (pH 6,7,8), carbonate (pH 9) | Electrochem setup | Six buffer solutions |
| Electrode polished **30 s** on robotic polishing station [14]; washed **30 s** deionized water | Electrochem procedure | Automated mechanical polishing |
| 3 cycles CV; window **-1.5 V to 0.5 V**; scan rate **100 mV/s** | Electrochem procedure | Cyclic voltammetry params |
| Redox potential = avg of oxidation & reduction peak potentials | Electrochem procedure | Calculation method |
| Theoretical slopes: **-59 mV/pH** (pH<pKa1), **-30 mV/pH** (pKa1–pKa2), **0 mV/pH** (pH>pKa2) | Quinone characterization | Two/one/zero-proton reactions |
| Reported AQS: **pKa1 = 7.68, pKa2 = 10.92** [49] | Quinone characterization | Literature dissociation constants |
| Organa slopes (pH<pKa1): **-61.3, -61.8, -61.0 mV/pH** | Quinone characterization | 3 runs |
| Organa pKa1 estimates: **8.12, 7.86, 8.10** | Quinone characterization | 3 runs |
| Only investigated up to pKa1 (pKa2 in corrosive pH region) | Quinone characterization | Safety limit; pH>9 not tested in robotics lab |
| Action durations simplified: 1T (≤60s), 2T (≤120s), 3T (>180s) | Parallel exec | To avoid state-space explosion |
| Plan = sequence of **19 actions** | Parallel exec | Some single-agent, some joint |
| Sequential plan avg **21.67 min**; parallel **17.10 min**; **21.1%** reduction | Parallel exec | Efficiency gain |
| Planning time (12 trials): sequential **61.52±0.1 s**; temporal TAMP **186.3±46.0 s** | Parallel exec | Overhead of joint TAMP+scheduling |
| Fig 5: sequential single-buffer test = **1,346 s (22.43 min)**; parallel = **1,071 s (17.85 min)** | Fig 5 caption | Gantt chart per buffer |
| Action legend times: transfer-liquid 70.4s, move 16.3s, wash 30.0s, polish 30.0s, mix-solution 40.0s, redox-potential 150.1s, measure-pH 32.2s, clean 341.0s, empty 88.9s | Fig 5 legend | Per-action durations |
| Efficiency gain restated as **274 s (21.1%)** | Discussion | Parallel vs sequential electrochem |
| User study: **8 chemists**, Dept. of Chemistry, Univ. of Toronto | Note S4 | 25% female, 75% male; ages ~20s–30s; novice→13-yr expert; none Organa members |
| Manual: 3 pH values ×4 measurements = **24 data points** per subject | Test modes | Manual electrochemistry |
| Manual experimentation avg **>30 min** (36.83 min in Fig 7) | Quantitative results; Fig 7 | Baseline |
| Organa startup: **7.35 min** (written), **4.27 min** (spoken) | Quantitative results; Fig 7 | Interaction time |
| Organa troubleshooting: avg **1.30 min** | Quantitative results | Feedback on errors |
| CLAIRify-style workflow: **17.65 min** | Quantitative results; Fig 7 | Manual step-by-step |
| False positives: **3 of 40** correct-result experiments incorrectly alerted (8 users × 5 experiments w/o bugs) | Quantitative results | Error detection |
| False negatives: **1 of 8** introduced-error experiments missed | Quantitative results | Error detection |
| Combined: Organa pKa1 = **8.03**, chemists = **8.02** | Quantitative results; Fig 6 | Comparable |
| Combined: slope Organa = **-61.3 mV/pH**, chemists = **-62.7 mV/pH** | Quantitative results; Fig 6 | Comparable |
| Fig 6: Organa 3 data points/pH, chemists 4 data points/pH | Fig 6 caption | |
| Fig 4: MLE pKa1 = **7.86** (single run); slope MLE = **-61.8 mV/pH** | Fig 4 caption | Single experimental run |
| Discussion: solubility **10.2 ± 2.2%** mean±std | Discussion | Across solubility estimates |
| Discussion: slope **-61.4 ± 0.5 mV/pH**, pKa1 **8.03 ± 0.17** across 3 runs | Discussion | Electrochemistry reproducibility |
| NASA-TLX: frustration halved; physical demand reduced **fourfold** | Discussion; qualitative | Self-rated workload |
| Users saved **88.4%** of time via audio vs manual (3 buffers) | Discussion | Temporal workload |
| Half of users uncertain about trusting full autonomy | Discussion | Trust finding |
| Perception dataset: **135 RGBD images**, **17 scenes**, 4 transparent objects + 1 polishing plate per scene | Note S1 | Real electrochemistry-setup dataset |
| Object position MAE **3.5 cm** avg (small beaker 2.4 cm best; large flask 5.1 cm worst) | Note S1 | Pose estimation accuracy |
| Radius outlier removal improved MAE **4.5 → 3.5 cm** | Note S1 | Point-cloud filtering |
| Table S1 AP glass @IoU 0.25/0.50/0.75 = **94.9 / 93.9 / 90.7**; plate = **81.4 / 38.6 / 37.1** | Table S1 | Detection precision |
| ZED Mini depth error **1.5%** over 10 cm–3 m range | Note S1 | But degrades on transparent objects |
| Perception at view pose takes **~20 s** | Electrochem setup | Object detection + pose |
| Grounding DINO Swin-T backbone; SAM ViT-B backbone; prompts "glass object", "plate" | Note S1 | Perception implementation |
| Reasoner: GPT-4 (reasoning), Whisper (STT), ElevenLabs (TTS) | Note S2 | Interaction stack |
| CLAIRify: GPT-3.5 Turbo (gpt-3.5-turbo) NL→XDL | Note S2; refs | Structured-language generation |
| Memory summarized every k=3 experiments | Note S2 | Token reduction |
| Startup phase collects: experiment def, lab setup, example experiment (rationale/procedure/expected output), stopping criterion | Fig 9; Note S2 | Four key info items |
| CV counter & reference electrodes = silver wires; working = glassy carbon | Note S5 | 3-electrode system |
| Funding: CFREF-2022-00042 (Canada First Research Excellence Fund) | Acknowledgments | Univ. Toronto Acceleration Consortium |
| No competing interests; no new materials generated | Declarations; Resource availability | |

---

## Scope & Limitations (explicitly stated)

- **Human-in-the-loop, NOT fully autonomous end-to-end.** Half the users expressed uncertainty trusting a robot to run start-to-finish.
- **No online replanning** — limits adaptability to execution uncertainties. LLM-based replanning is future work; validating LLM plans remains a challenge.
- **Cannot auto-prepare the experimental setup** (e.g., retrieving clean beakers/vials, inserting tubes/probes) — a mobile-robot capability currently lacking.
- **PDDL domain complexity** makes it hard for non-planning-expert chemists to modify.
- **Perception limited:** relies on independent (not multimodal) sensor modalities; transparent-object perception still not robustly model-free; pose accuracy depends on ZED depth quality.
- **pH range limited to ≤9** in robotics lab (safety); pKa2 region (corrosive) not experimentally probed → high pKa2 variance.
- **Pouring accuracy** of robot is main solubility error source (scale + Dynamixel motor resolution/latency).
- Specialized liquid/solid dispensers could improve accuracy where feasible.

## Does NOT claim / Boundaries

- Does NOT claim fully autonomous scientific discovery; it is an **assistive** system optimizing human-robot collaboration and lab-resource efficiency.
- Does NOT generate new materials (explicit: "This study did not generate new materials").
- Does NOT claim novel chemistry findings — it **reproduces literature results** (solubility vs [42]; AQS pKa/slope vs theory & [49]) to validate reliability/modularity.
- CLAIRify (prior work) only supports sequential single-experiment planning; Organa's new contributions vs CLAIRify: multi-experiment reasoning, feedback/reports, transparent-object perception without AprilTags, and parallel execution via joint TAMP+scheduling.
- The user-study interaction sessions used backend-replayed experimental values (not live robot runs) for cross-participant consistency.

## Section Map

- **Introduction** — motivation, SDL challenges, contributions (3), related work (lab automation, electrochemistry automation, perception, LLM planners: CLAIRify, ChemCrow [28], Coscientist/Boiko [29]), TAMP + scheduling background.
- **Results** — Solubility; Recrystallization; pH; Electrochemistry (task/setup/quinone characterization; sequential vs parallel efficiency); User Study (test modes, metrics: NASA-TLX/SUS/custom, quantitative + qualitative results).
- **Discussion** — reliability/reproducibility; modularity; autonomy & robustness; efficiency/parallelism; safety; chemist-Organa interaction; limitations.
- **Experimental Procedures** — resource availability; architecture (Fig 9); LLM interaction/reasoning (Reasoner, ReAct, CLAIRify NL→XDL, disambiguation); TAMP with scheduling (Temporal-PDDLStream, Algorithm 1, Fig 10); perception (turbidity, Grounding DINO + SAM + PCA pose); robot skills (pick/place/insert, constrained motion, pouring, electrode polishing); data analysis & report generation (MLE/posterior, PDF report).
- **Supplemental** — S1 perception analysis + Table S1; S2 Reasoner prompts; S3 ambiguity/uncertainty examples; S4 user study (participants, protocol, SUS/NASA-TLX/custom questionnaires); S5 perception hardware; S6 action hardware; S7 parameter-estimation math; S8 integrated PDDLStream w/ scheduling (PDDL snippets); S9 example auto-generated report (Figs S5–S11).

---

## 2-line reply

Q: Does ORGANA automate the physical execution of wet-lab chemistry (robotic assistant + characterization)?
A: **YES** — a Franka Panda arm + real lab hardware (pump, stirrer, potentiostat, pH sensor, robotic polishing station) physically execute solubility, recrystallization, pH, and electrochemistry experiments, including fully automated mechanical polishing of a glassy-carbon electrode and CV characterization of a quinone (AQS) for flow batteries; human-in-the-loop (not fully autonomous end-to-end).
