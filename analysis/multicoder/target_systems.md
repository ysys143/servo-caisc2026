# Multi-coder target systems -- candidate universe and inclusion decision

**Inclusion criterion (from coding_protocol.md):** a system is codeable iff it
automates at least one full hypothesis -> experiment -> validation cycle
(a generation step G, an execution step E, and a validation step V producing a
signal the system uses). EXCLUDE pure predictors (e.g., AlphaFold), surveys,
benchmarks, idea/literature tools without an internal loop, epistemic-risk/meta
papers, venues, and infrastructure roadmaps.

Source corpus: `AI_Scientist_Analysis.md` (13 deep-mapped + 29 catalog ~= 42
papers; 42 `####` detail headers).

## Tier 1 -- end-to-end AI Scientist systems (INCLUDE; unambiguous) -- 14

| id | system | cite key | note |
|----|--------|----------|------|
| robot_scientist | Robot Scientist (Adam/Eve) | sparkes2010robot | wet-lab loop |
| coscientist | Coscientist | boiko2023emergent | robotic chem |
| ai_scientist_2024 | The AI Scientist (Sakana 2024) | lu2024aiscientist | closed-comp |
| ai_scientist_2026 | The AI Scientist (Nature 2026) | lu2026aiscientist | tree search |
| ai_scientist_v2 | The AI Scientist-v2 (Sakana 2025) | (catalog) | agentic tree |
| agent_laboratory | Agent Laboratory | schmidgall2025agentlab | human-directed |
| ai_coscientist_google | AI Co-Scientist (Google) | gottweis2026coscientist | multi-agent |
| ai_researcher | AI-Researcher (Tang & Xia 2025) | (catalog) | end-to-end |
| deepscientist | DeepScientist (Weng 2025) | (catalog) | exceeds SOTA |
| robin | Robin (FutureHouse 2026) | (catalog) | semi-auto bio |
| era | ERA (Google 2026) | (catalog) | recombination |
| autoresearchclaw | AutoResearchClaw (Liu 2026) | (catalog) | self-reinforcing |
| scientistone | ScientistOne (Google 2026) | (catalog) | chain-of-evidence |
| novelseek | InternAgent / NovelSeek | zhang2025novelseek | closed-comp |

## Tier 2 -- domain / self-evolving discovery loops (INCLUDE if expanding) -- 17

| id | system | cite key | domain |
|----|--------|----------|--------|
| funsearch | FunSearch | romera2023funsearch | math/algo |
| alphaevolve | AlphaEvolve | (catalog) | self-evolving |
| deepseek_prover | DeepSeek-Prover-V1.5 | xin2024deepseek | formal math |
| tsoukalas_proofsearch | AI-Driven Formal Proof Search | (catalog) | formal math |
| aletheia | Aletheia | google2026aletheia | NL math |
| chemcrow | ChemCrow | bran2023chemcrow | chemistry |
| chemreasoner | ChemReasoner | sprueill2024chemreasoner | chemistry |
| automated_social_science | Automated Social Science | manning2024automated | social sci |
| darwin_godel_machine | Darwin Godel Machine | (catalog) | self-evolving |
| aevo | AEvo (Agentic Evolution) | (catalog) | self-evolving |
| freephdlabor | freephdlabor | (catalog) | end-to-end fw |
| piflow | PiFlow | (catalog) | end-to-end fw |
| sr_scientist | SR-Scientist | (catalog) | end-to-end fw |
| organa | ORGANA | (catalog) | self-driving lab |
| automl_zero | AutoML-Zero | real2020automlzero | CS/algo |
| sartori_algo | Algorithm Discovery (Sartori) | sartori2024algodiscovery | CS/algo |
| autokernel | AutoKernel | jaber2026autokernel | CS/algo |

## Tier 3 -- borderline (method/single-shot; INCLUDE only if maximal) -- 7

| id | system | cite key | why borderline |
|----|--------|----------|----------------|
| openai_erdos | OpenAI Erdos unit-distance disproof | (catalog) | single-shot, V_human post hoc |
| ai_feynman | AI Feynman | udrescu2020afeynman | symbolic-regression method, no agent V |
| cranmer_symbolic | Discovering Symbolic Models | cranmer2020symbolic | symbolic-regression method |
| bioplanner | BioPlanner | odonoghue2023bioplanner | protocol planning; weak V |
| generative_agents | Generative Agents | park2023generative | simulation substrate, not discovery loop |
| aher_simulation | LLMs Simulate Human Subjects | aher2023turing | E-substrate, not a loop |
| eggroll | EGGROLL | (catalog) | ES scaling method, not a scientist |

## EXCLUDE (not a discovery loop) -- with reason

- **Pure predictors:** AlphaFold2 (jumper2021alphafold), IsoDDE -- no generation+search loop (rubric's explicit exclusion).
- **QA agent (not AI Scientist):** DeepResearcher -- author-noted.
- **Surveys (~8):** Tie et al., AutoResearch AI, Agentic AI Discovery, AI4Science->Agentic Science, LLM4SR, Agentic AutoSurvey, EXHYTE, "Code as Agent Harness".
- **Benchmarks (~10):** PaperBench, EXP-Bench, Curie, Auto-Bench, ResearchBench, MLAgentBench, DiscoveryBench, BLADE, WritingBench, SPOT-A.
- **Idea/lit tools without loop (~10):** LitLLM, HypER, SciAgents, PaperQA, SciMuse, Many Heads, DS-Agent, Text-Tuple-Table, AIGS, PaperDebugger, Alien Space, SciAtlas.
- **Epistemic-risk / meta:** Hidden Pitfalls, Kim et al. (AI reviewers), Vafa (world models), Wang (Human-AI collaboration), Korean vocab study, Nature editorials, Inductive Bias Probe.
- **Venues / institutional / infra:** Agents4Science, CAISc 2026, AIxBio roadmap.
- **Similar-framework (lit-review targets, not coded as systems):** HypoAgents, PiEvo.

## Scope options
- **A (Tier 1)** = 14 systems -- tight, fast, clear end-to-end set.
- **B (Tier 1+2)** = 31 systems -- matches "much more than 13"; defensible "comparable AI Scientist systems"; codex quota will not cover 31 (claude+agy carry it, codex best-effort on Tier 1).
- **C (Tier 1+2+3)** = 38 systems -- maximal; includes borderline methods.
