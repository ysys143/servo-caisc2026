# Digest: park2023generative

**Title:** Generative Agents: Interactive Simulacra of Human Behavior
**Authors:** Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein
**Venue:** UIST '23 (The 36th Annual ACM Symposium on User Interface Software and Technology), Oct 29 - Nov 1 2023, San Francisco. arXiv:2304.03442v2 [cs.HC], 6 Aug 2023. 22 pages.
**DOI:** 10.1145/3586183.3606763

---

## Thesis / Problem

Believable proxies of human behavior can empower interactive applications (immersive environments, rehearsal spaces, prototyping tools). The paper introduces **generative agents**: computational software agents that simulate believable human behavior by extending an LLM with an architecture that (a) stores a complete natural-language record of the agent's experiences (memory stream), (b) synthesizes memories over time into higher-level reflections, and (c) retrieves them dynamically to plan behavior. Problem addressed: first-order prompting conditions behavior only on the current environment; believable agents also need long-term coherence over a vast, constantly-growing memory.

## Method — IS THIS AN LLM-SIMULATION STUDY?

**YES. This is unambiguously an LLM-simulation-of-human-behavior study.** Generative agents draw on a generative model (LLM) to simulate believable human behavior. 25 LLM-powered agents populate an interactive sandbox world "Smallville" (reminiscent of The Sims). The underlying model is **gpt-3.5-turbo (ChatGPT)** — GPT-4 API was invitation-only at time of writing, so they used ChatGPT. Agents plan days, form relationships, spread information, and coordinate group activities (e.g., a Valentine's Day party) emergently from a single seed suggestion.

**DOES IT INVOLVE STATISTICAL EVALUATION OF SIMULATED BEHAVIOR? YES.** Two evaluations:
1. **Controlled evaluation (Sec 6):** Agents are "interviewed" in natural language across 5 categories (self-knowledge, memory, plans, reactions, reflections). 100 human evaluators (Prolific) ranked believability of 5 conditions (full architecture + 3 ablations + human crowdworker baseline). Rank data → **TrueSkill ratings**; statistical significance via **Kruskal-Wallis test** + **Dunn post-hoc** + **Holm-Bonferroni** correction. Effect size via **Cohen's d**.
2. **End-to-end evaluation (Sec 7):** 25 agents interact over 2 full game days; descriptive measurements of information diffusion, relationship formation (network density), and coordination.

Architecture components (observation/memory, reflection, planning) each shown via ablation to critically contribute to believability.

---

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| 25 agents ("twenty-five") | Abstract, Sec 3.1 (L411), Sec 7 | Number of unique agents populating Smallville sandbox |
| "over four decades" / "past four decades" | Intro L105, Sec 2.2 L288 | How long researchers have envisioned believable agent proxies |
| gpt3.5-turbo (ChatGPT) | Sec 4 L684-690 | LLM powering the agents; GPT-4 API was invitation-only so ChatGPT used |
| 3 main architecture components | Intro L143-151, Sec 4 | memory stream, reflection, planning |
| decay factor = 0.995 | Sec 4.1 L735 | Recency exponential decay per sandbox game hour |
| Importance scale 1 to 10 | Sec 4.1 L742 | LLM prompted to rate poignancy of a memory |
| Importance = 2 for "cleaning up the room"; 8 for "asking your crush out on a date" | Sec 4.1 L751-752 | Example importance-score outputs |
| Importance = 2 for "cleaning up the room" (returned by prompt) | Sec 4.1 L751 | Prompt example returns integer 2 |
| score = α_recency·recency + α_importance·importance + α_relevance·relevance | Sec 4.1 L767-768 | Retrieval scoring formula |
| all α = 1 | Sec 4.1 L768 | All three weights set to 1 in implementation |
| Scores normalized to [0,1] via min-max scaling | Sec 4.1 L765-766 | Retrieval score normalization |
| Reflection importance-sum threshold = 150 | Sec 4.2 L801 | Reflection triggered when sum of importance for latest events exceeds 150 |
| "roughly two or three times a day" | Sec 4.2 L802-803 | How often agents reflected in practice |
| 100 most recent records | Sec 4.2 L807 | Records queried to generate reflection questions |
| "3 most salient high-level questions" | Sec 4.2 L811 | Prompt asks for 3 questions to reflect on |
| "5 high-level insights" | Sec 4.2 L827 | Reflection prompt asks for 5 insights |
| Plan divided into 5 to 8 chunks | Sec 4.3 L905-906 | Broad-strokes daily plan granularity |
| Recursive decomposition: hour-long → 5–15 minute chunks | Sec 4.3 L916-920 | Plan refinement granularity |
| 180 minutes from 9am, Feb 12th 2023 | Sec 4.3 L867-868 | Example plan entry (Klaus at Oak Hill College Dorm desk) |
| Eddy Lin age 19 | Sec 4.3 L888 | Example prompt agent |
| Klaus Mueller age 20 | Appendix B L2020 | Self-intro sample response |
| Abigail Chen age 25 | Sec 6.5.2 L1305 | Animator; self-intro sample |
| Dates: Feb 12/13/14 2023 | Sec 4.3, 3.4.3 | Simulation in-game calendar (Valentine's Day = Feb 14) |
| Valentine's Day party 5 to 7 p.m. on February 14th | Sec 3.4.3 L633-634 | Isabella's seeded intent |
| 100 participants / evaluators | Sec 6.1 L1169, Sec 6.3 L1227 | Recruited from Prolific for believability ranking |
| within-subjects design | Sec 6.1 L1169 | Study design |
| 5 conditions | Sec 6.2 | full architecture + 3 ablations + human crowdworker |
| 5 question categories, 5 questions each = 25 questions | Sec 6.1 L1136-1140, Appendix B L2092 | Interview structure (self-knowledge, memory, plans, reactions, reflections) |
| $15.00 per hour | Sec 6.3 L1225 | Evaluator pay rate |
| Participation ~30 minutes | Sec 6.3 L1229 | Duration of evaluator task |
| Median age score = 4 (25-34 years old) | Sec 6.3 L1229-1230 | Participant demographics |
| 25 female, 73 male, 2 non-binary | Sec 6.3 L1231 | Gender of 100 participants |
| 42 bachelor's, 5 higher degree, 13 associate's, rest high school | Sec 6.3 L1231-1233 | Education of participants |
| 73.0% Caucasian, 7.0% Hispanic, 6.0% Asian, 10.0% African American, 4.0% other | Sec 6.3 L1234-1235 | Race/ethnicity of participants |
| Evaluators: U.S., fluent English, >18 years | Sec 6.3 L1224 | Eligibility criteria |
| 25 crowdworkers (one unique worker per agent) | Sec 6.2 L1208-1209 | Human baseline authored responses |
| 4 sets of crowdworker responses re-generated | Sec 6.2 L1217-1218 | Failed quality check, redone by other workers |
| 3 ablated architectures | Sec 6.2 L1184-1189 | (1) no obs/no refl/no plan, (2) no refl/no plan, (3) no refl |
| Full architecture: μ = 29.89, σ = 0.72 | Sec 6.5.1 L1279 | TrueSkill rating, most believable |
| No reflection: μ = 26.88, σ = 0.69 | Sec 6.5.1 L1282 | Next best condition |
| No reflection or planning: μ = 25.64, σ = 0.68 | Sec 6.5.1 L1282-1283 | Third |
| Crowdworker condition: μ = 22.95, σ = 0.69 | Sec 6.5.1 L1283-1284 | Human baseline |
| No memory/planning/reflection (fully ablated): μ = 21.21, σ = 0.70 | Sec 6.5.1 L1284-1286 | Worst condition; represents prior state of the art |
| Cohen's d = 8.16 ("eight standard deviations") | Sec 6.5.1 L1290-1291 | Effect size: prior-work baseline vs full architecture |
| Kruskal-Wallis H(4) = 150.29, p < 0.001 | Sec 6.5.1 L1292-1293 | Overall significance of rank differences |
| Dunn post-hoc: all pairwise p < 0.001 except crowdworker vs fully-ablated | Sec 6.5.1 L1294-1297 | The two worst conditions not sig. different from each other |
| Sam's mayoral candidacy awareness: 1 (4%) → 8 (32%) | Sec 7.1.2 L1437-1439 | Information diffusion over 2 days |
| Isabella's party awareness: 1 (4%) → 13 (52%) | Sec 7.1.2 L1439-1440 | Information diffusion over 2 days |
| No one who claimed to know info had hallucinated it (candidacy/party) | Sec 7.1.2 L1441-1442 | Verified against memory stream |
| Network density: 0.167 → 0.74 | Sec 7.1.2 L1443-1444 | Relationship formation over simulation |
| Network density formula η = 2·|E| / |V|(|V|−1) | Sec 7.1.1 L1427 | Undirected graph, 25 vertices |
| 453 agent responses re relationship awareness; 1.3% (n=6) hallucinated | Sec 7.1.2 L1444-1446 | Hallucination rate in relationship interviews |
| 12 agents (diffusion path) heard about party, aside from Isabella | Fig 9 L1422-1423 | Valentine's party invitation diffusion path |
| 5 out of 12 invited agents showed up | Sec 7.1.2 L1450-1451 | Coordination result at party |
| "five agents, including Klaus and Maria, show up... at 5 pm" | Sec 3.4.3 L643-644 | Party attendance (narrative) |
| 7 invited-but-did-not-attend agents; 3 cited conflicts, 4 expressed interest but no plan | Sec 7.1.2 L1452-1460 | Follow-up interviews of no-shows |
| 2 full game days | Sec 7 L1364-1365, Sec 6 L1121 | Duration of end-to-end simulation |
| 3 common modes of erratic behavior | Sec 7.2 L1467-1468 | location misplacement, norm misclassification, instruction-tuning formality |
| Stores close ~5 pm | Sec 7.2 L1491-1492 | Norm agents sometimes violated |
| "roughly a year" to build architecture | Sec 8.3 L1629 | Time cost noted re misuse deterrence |
| "thousands of dollars in token credits" / "multiple days" | Sec 8.2 L1567 | Cost of simulating 25 agents for 2 days |
| 1 real second = 1 game minute | Appendix A L2084 | Sequential run rate (roughly real-time game time) |
| John Lin description (~14 semicolon phrases) | Sec 3.1 L416-434 | Example single-paragraph seed memory |
| Phaser (web game dev framework) | Sec 5 L1017 | Sandbox environment engine |
| Environment as tree data structure | Sec 5.1 | Areas/objects; containment relationship = edges |
| 2 prompts for context summary | Sec 4.3.1 L950-952 | Relationship + action-status queries |
| 3 summary queries for agent summary cache | Appendix A L2073-2075 | core characteristics, current daily occupation, feeling about recent progress |
| 109 references | References section (numbered [1]–[109]) | Bibliography count |
| TrueSkill = generalization of Elo for multiplayer; used by Xbox Live | Sec 6.4 L1243-1246 | Rating system rationale |
| Dependent variable = believability | Sec 6.1 L1133-1134 | Central DV, per prior work on agents |

---

## Scope & Limitations (as stated by the paper)

- Evaluation limited to a **relatively short timescale** (2 game days) and a **single human crowdworker baseline** that does NOT represent maximal/expert human performance ("not the gold standard"). (Sec 8.2)
- Substantial cost/time: thousands of dollars, multiple days for 25 agents / 2 days. Not real-time interactive. (Sec 8.2)
- Robustness largely unknown: vulnerable to prompt hacking, memory hacking, hallucination. (Sec 8.2)
- Inherits imperfections/biases of underlying LLM; may struggle with marginalized subpopulations due to limited data. (Sec 8.2)
- Ablated architectures were given the same accumulated memory as the full architecture rather than re-simulated — differences are a "conservative estimate." (Sec 6.2)
- Environment design was manual, not automatic; not the focus. (Sec 3.2 footnote 4)
- Agent behavior described with human-action verbs is a "shorthand for readability," NOT a claim of genuine agency (agents akin to animated Disney characters). (footnote 1, L172-176)

## Does NOT Claim / Boundaries

- Does NOT claim agents have genuine human-like agency (explicit disclaimer, footnote 1).
- Does NOT claim to replicate a specific real-world social-science dataset or reproduce human statistical distributions — the "human" comparison is a crowdworker roleplay believability baseline, NOT a benchmark against real human survey/behavioral data.
- Does NOT claim LLMs alone are sufficient — architecture (memory/reflection/planning) is required.
- Does NOT position generative agents as a substitute for real human input in studies/design; recommends they only prototype early-stage ideas. (Sec 8.3)
- Does NOT use GPT-4 for the agents (used ChatGPT/gpt-3.5-turbo).
- The statistical tests (TrueSkill, Kruskal-Wallis, Dunn, Cohen's d) evaluate **human-judged believability rankings of agent responses**, NOT accuracy against ground-truth human behavior data.

## Section Map

- **1 Introduction** (L101) — motivation, contributions
- **2 Related Work** (L220): 2.1 Human-AI Interaction; 2.2 Believable Proxies of Human Behavior; 2.3 LLMs and Human Behavior
- **3 Generative Agent Behavior and Interaction** (L383): 3.1 Agent Avatar & Communication (incl. 3.1.1 Inter-Agent Communication, 3.1.2 User Controls); 3.2 Environmental Interaction; 3.3 Example "Day in the Life"; 3.4 Emergent Social Behaviors (3.4.1 Information Diffusion, 3.4.2 Relationship Memory, 3.4.3 Coordination)
- **4 Generative Agent Architecture** (L660): 4.1 Memory and Retrieval; 4.2 Reflection; 4.3 Planning and Reacting (4.3.1 Reacting and Updating Plans, 4.3.2 Dialogue)
- **5 Sandbox Environment Implementation** (L1012): 5.1 From Structured World Environments to Natural Language, and Back Again
- **6 Controlled Evaluation** (L1109): 6.1 Evaluation Procedure; 6.2 Conditions; 6.3 Human Evaluators; 6.4 Analysis; 6.5 Results (6.5.1 Full Architecture Bests Others, 6.5.2 Remember but With Embellishments, 6.5.3 Reflection Required for Synthesis)
- **7 End-to-End Evaluation** (L1357): 7.1 Emergent Social Behaviors (7.1.1 Measurements, 7.1.2 Results); 7.2 Boundaries and Errors
- **8 Discussion** (L1516): 8.1 Applications; 8.2 Future Work and Limitations; 8.3 Ethics and Societal Impact
- **9 Conclusion** (L1645)
- **Acknowledgments; References [1]–[109]; Appendix A Architecture Optimizations; Appendix B Agent Interview Questions**

---

*Digest based ONLY on the paper itself (arXiv:2304.03442v2). Blind reading — no manuscript claims consulted.*
