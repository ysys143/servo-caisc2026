# Digest: boiko2023emergent

**Full title (article body):** "Autonomous chemical research with large language models"
(NOTE: the paper's title does **not** contain the word "emergent" — the bibkey slug is a citing-side label. The system is named **Coscientist**. If the manuscript refers to this work as "emergent" behaviour, that is the manuscript's framing, not the paper's title. The paper does use "emerge" once in the Discussion — "These capabilities *emerge* when LLMs gain access to relevant research tools" (l.1704) — but never claims novel/emergent *science*.)
**Journal:** Nature 624, 570-577, 21/28 December 2023. DOI 10.1038/s41586-023-06792-0. Open access.
**Received** 20 April 2023; **accepted** 27 October 2023; **published online** 20 December 2023.
**Authors:** Daniil A. Boiko, Robert MacKnight, Ben Kline, Gabe Gomes. (Carnegie Mellon University — Chemical Engineering / Chemistry / Scott Institute; Ben Kline is Emerald Cloud Lab.)

---

## Thesis / problem
Can an LLM-driven agent, given the right tools, **autonomously design, plan and execute** real chemical experiments? The paper presents **Coscientist**, a **GPT-4-driven** multi-LLM agent equipped with tools — internet search, documentation search/retrieval, a Python code-execution sandbox, and robotic/cloud experimentation APIs — and demonstrates it on **six tasks**. Framed explicitly as a **"proof of concept"** (l.1699) for a **"(semi-)autonomous"** system (title of Discussion / l.1700). Headline demonstration: it designed and ran real **palladium-catalysed cross-coupling** reactions (Suzuki-Miyaura and Sonogashira), with products confirmed by GC-MS.

## Method — is Coscientist a tool-augmented LLM system? (yes) + how the architecture works
**Yes — Coscientist is exactly a tool-augmented, multi-LLM agent.** Architecture (Fig 1):
- **Planner** = a GPT-4 chat-completion instance (the "assistant"). It receives the user's plain-text prompt (e.g. "perform multiple Suzuki reactions"); command outputs are fed back as user messages. Its action space is defined by four modular commands (l.75-77): **GOOGLE, PYTHON, DOCUMENTATION, EXPERIMENT**.
- **GOOGLE → Web searcher** (itself another LLM): turns prompts into queries, runs Google Search API, browses pages, funnels answers back to Planner.
- **PYTHON → Code execution**: runs generated code in an **isolated Docker container** (NOT reliant on any LLM). The Planner LLM can **fix code on software errors** (l.194).
- **DOCUMENTATION → Docs searcher**: retrieval + summarization over API docs via **ada-embedding + distance-based vector search**. Demonstrated for the **Opentrons OT-2 Python API** and **Emerald Cloud Lab (ECL) Symbolic Lab Language (SLL)**.
- **EXPERIMENT → Automation**: executes generated code on physical hardware (OT-2 liquid handler, ECL cloud lab) or emits a procedure for manual execution.

### Feedback from measured outcomes — DOES THE LOOP CLOSE? (crux; answer: PARTIAL, and only over lookup data for the "optimization" loop)
There are **three distinct feedback pathways**, closing to very different degrees:

1. **Software / error-correction loop — FULLY CLOSED (but not "measured outcomes").** Code-execution and hardware-API *errors* are returned to the Planner, which revises code. Explicit example: Coscientist used an incorrect heater-shaker method name, the run failed, it consulted the OT-2 docs, corrected the protocol, and it "ran successfully" (l.749-752). This is feedback from **software errors, not from measured experimental results**.

2. **Optimization "game" (Fig 6) — CLOSED-LOOP, but the "measurement" is a LOOKUP from pre-collected datasets, NOT a fresh physical measurement.** Coscientist selects reaction conditions → is told the **yield** → lists observations → selects next conditions, for up to 20 iterations. Crucially: "any reaction proposed by Coscientist would be **within these datasets and accessible as a lookup table**" (l.1628-1629). The two datasets are **Perera et al. (Suzuki, flow)** and **Doyle's Buchwald-Hartwig** (Ahneman et al.). Normalized advantage **increases over iterations**, which the authors read as evidence the model "can effectively reuse the information obtained" (l.1674-1676). So this loop closes on **historical benchmark data**, not on live instrument readouts.

3. **Physical wet-lab measurement → next autonomous decision — NOT CLOSED (human-mediated).** For the real cross-coupling experiments (Fig 5), Coscientist designed and executed a single protocol; the **GC-MS analysis confirming biphenyl / tolane products was performed and interpreted by the authors post hoc** (l.753-761), and is **not** fed back into any further Coscientist decision. This is a single design→execute cycle, not a closed physical optimization loop.

4. **Perception feedback (color problem, Fig 4) — PARTIAL / single-shot.** Coscientist prepared samples, requested UV-Vis measurements, was **handed a NumPy array of spectra**, then generated code to find max-absorbance wavelengths and solve — but "it required a guiding prompt asking it to think through how different colours absorb light" (l.706-708). Measured data *is* returned to the agent here, but as a one-shot perception step, not iterative optimization.

**Net:** the design-plan-execute-fix loop is closed **in software**; the "optimization" loop is closed only **over lookup-table yields**; the **physical-measurement-to-decision loop is open / human-mediated** in this paper. And the setup is explicitly **"not yet fully automated (plates were moved manually)"** though "no human decision-making was involved" (l.716-717).

### Novelty / significance validation — ABSENT (not a claim of the paper)
Coscientist does **no** novelty or significance assessment. Every task targets **known** chemistry:
- Synthesis planning is of **known compounds** (aspirin, acetaminophen, benzoic acid, ethyl acetate, nitroaniline, ibuprofen, phenolphthalein).
- The wet-lab reactions are **textbook named reactions** (Suzuki-Miyaura, Sonogashira).
- The "optimization" targets are **pre-existing published datasets** used as lookup tables.
There is no hypothesis generation about new science, no novelty ranking, no significance judgement. The paper's contribution is autonomous **design/planning/execution**, not discovery of new chemistry.

## FACTS TABLE (exhaustive)

| value / finding | exact location | context |
|---|---|---|
| **Six tasks** demonstrated | abstract (l.21-24); l.59-65 | (1) synthesis planning of known compounds; (2) navigating hardware docs; (3) high-level cloud-lab commands; (4) low-level liquid-handler control; (5) multi-module integrated experiment; (6) optimization over collected data |
| **GPT-4-driven**; four commands GOOGLE/PYTHON/DOCUMENTATION/EXPERIMENT | l.17-18; l.75-77 | system architecture |
| Web-search benchmark = **seven compounds** | l.206; Fig 2a | synthesis-planning test set |
| Baselines: **GPT-3.5, GPT-4, Claude v1.3, Falcon-40B-Instruct**; browsing versions **search-gpt-4, search-gpt-3.5-turbo** | l.207-211 | Falcon called "one of the best open-source models at the time" per OpenLLM leaderboard |
| Scoring scale **1-5**; **scores below 3 = task failure**; labelling "inherently subjective" | l.213-224 | 5=detailed+accurate w/ quantities … 1=incorrect/failed |
| **All non-browsing models incorrectly synthesized ibuprofen** | l.228; l.372-373 | non-browsing failure |
| GPT-4 Web Searcher reached **max scores** for acetaminophen, aspirin, nitroaniline, phenolphthalein; **only one** to hit min-acceptable **3** for ibuprofen; **lower** on ethyl acetate & benzoic acid | l.378-382 | browsing improves planning; framed as grounding vs "hallucinations" |
| OT-2 API docs embedded with **OpenAI ada** model; distance-based vector search | l.554-557; Fig 3a | documentation retrieval |
| ECL SLL: **three investigations** — prompt-to-function, prompt-to-SLL, prompt-to-samples | l.563-566 | SLL "currently unknown to the GPT-4 model" (l.562) |
| **114 ECL experiment functions** text-embedded | Fig 3d (l.497-499) | prompt-to-function corpus |
| ExperimentHPLC run at ECL on a **caffeine standard sample**; **air bubble injected** with analyte | l.575-585 | real cloud-lab execution; flagged need for automated QC |
| Prompt-to-samples over **1,110 Model samples** from the ECL catalogue | l.595 | e.g. query "Acetonitrile" returns relevant stock solutions |
| OT-2 liquid-handler control: prompts like "colour every other line…" → accurate protocols; **no internet access** granted for this task | l.606-611 | Fig 4b-e |
| Color problem: **red/yellow/blue** in wells of a **96-well plate**; system must ID colours + positions with no prior info | l.614-617 | multi-module (liquid handler + UV-Vis) toy task |
| Cross-coupling reagents: phenylacetylene, phenylboronic acid, multiple aryl halides, **two catalysts, two bases**, solvent; source + target plates | l.719-724; Fig 5b | Pd-catalysed Suzuki-Miyaura + Sonogashira |
| **OT-2 heater-shaker module released after the GPT-4 training-data cutoff** | l.713-714 | used to force reliance on docs, not memorized API |
| Suzuki product (biphenyl): GC-MS signal at **9.53 min**, fragment at **76 Da** | l.755-757; Fig 5i | product confirmation |
| Sonogashira product (tolane): GC-MS signal at **12.92 min** | l.757-759; Fig 5j | product confirmation |
| Coscientist "**does not make chemistry mistakes**" (never picks phenylboronic acid for Sonogashira) | l.731-732 | reagent-selection reliability claim |
| **DBU** base selected more often with **PEPPSI-IPr** complex (preference switches for Sonogashira); **bromobenzene** chosen more often for Suzuki than Sonogashira | l.735-738; Fig 5f,g | run-to-run behaviour analysis |
| Web sources: **Wikipedia ~half** of cases; ACS & RSC journals among **top five** | l.744-746; Fig 5h | URL-frequency analysis |
| Compound-library computational study over **five transformations**: Diels-Alder, Michael addition, esterification, Buchwald-Hartwig amination, Mizoroki-Heck; uses **RDKit** + SMILES DB | l.765-767; l.1011-1016; l.1285-1289 | scaling reagent-selection to large libraries |
| Optimization datasets: **Perera et al. (Suzuki, flow)** and **Doyle's Buchwald-Hartwig** (Ahneman et al.) | l.1623-1627; refs 50, 51 | fully-mapped condition spaces used as lookup tables |
| **Max 20 iterations** = **5.2%** (dataset 1) and **6.9%** (dataset 2) of total space | l.1639-1641 | optimization budget |
| Only **hard rule**: actions in **JSON**; unparseable JSON → player alerted | l.1637-1639 | game protocol |
| Suzuki optimization: 3 approaches — GPT-4 **with prior info (10 random yields)**, GPT-4 without, GPT-3.5 without | l.1658-1661; Fig 6c | GPT-3.5 gives few points due to bad JSON schema adherence |
| Both GPT-4 approaches show **higher NMA / normalized advantage than standard Bayesian optimization** | l.1680-1684; Fig 6c | BO line "stays around zero"; authors caution it may reflect explore/exploit balance |
| Buchwald-Hartwig: GPT-4 over **compound names vs SMILES** → **similar** performance; model can reason about reactivity **from SMILES alone** | l.1690-1696; Fig 6f,g | reasoning-from-representation claim |
| C-N cross-coupling scheme: **1 min, 100 °C** | Fig 6a (l.1316) | reaction condition |
| GPT-4 released **14 March 2023** | l.36-37 | context |
| Independent & parallel to Auto-GPT / BabyAGI / LangChain; **ChemCrow** cited as parallel chemistry example | l.57-59; refs 23-26 | positioning |
| Dual-use / safety study | l.1712-1713 (Discussion); Supplementary "Safety implications: Dual-use study" | brief study; data/code withheld pending US AI regulation |

## Scope & limitations (how the paper frames autonomy)
- **Explicitly "(semi-)autonomous" and a "proof of concept"** (l.1699-1701). The strongest wet-lab demonstration was **not fully automated — plates were moved manually** (l.716), though the authors state "no human decision-making was involved" (l.717).
- The **optimization** claim rests on **lookup-table datasets**, not live measurement: "any reaction proposed by Coscientist would be within these datasets and accessible as a lookup table" (l.1628). Authors even flag they cannot rule out dataset contamination of GPT-4 training data (l.1670-1673).
- Bayesian-optimization comparison is **hedged**: the BO advantage line near zero "may not be indicative of their performance" due to exploration/exploitation balance (l.1685-1687).
- Data/code **deliberately withheld** for safety "until the development of US regulations"; only a **"simpler implementation"** is released on GitHub (gomesgroup/coscientist), which "may not produce the same results" (l.1900-1911). Reviewers had access to the web app.
- Grading of synthesis quality is "inherently subjective" and may vary between labellers (l.222-224).

## Does NOT claim / boundaries
- Does **NOT** claim **fully autonomous** operation — self-described "(semi-)autonomous," with manual plate transfers in the flagship experiment.
- Does **NOT** claim any **novel scientific discovery** — all compounds/reactions/datasets are known; no novelty or significance validation is performed or claimed.
- Does **NOT** close the loop on **physical measurements**: GC-MS confirmation of the real reactions was done/interpreted by the authors, not fed back to the agent for a next decision.
- Does **NOT** perform live experimental optimization — the optimization "campaign" queries pre-collected **lookup tables**, not instruments.
- Does **NOT** provide a rigorous head-to-head with Bayesian optimization (comparison explicitly caveated).
- Does **NOT** release full data/code/prompts (safety hold); results are reproducible only via a simpler, non-identical implementation.
- Does **NOT** claim the "emergent"/reasoning behaviour is proven — "some researchers believe the community is only starting to understand all the capabilities of GPT-4" (l.1291); capabilities "**emerge** when LLMs gain access to relevant research tools" (l.1704) is a tooling claim, not an emergence-of-new-science claim.

## Section map
- **Abstract** (l.15-26): Coscientist, GPT-4, six tasks, Suzuki cross-coupling optimization, versatility/efficacy/explainability.
- **Intro** (l.28-65): LLM progress; GPT-4; chemical-automation background (refs 17-22); the six tasks; positioning vs Auto-GPT/BabyAGI/LangChain/ChemCrow.
- **Coscientist system architecture** (l.67-198): Planner + four commands; Web searcher; Docs searcher; Docker code execution; error-correction by the Planner LLM (Fig 1).
- **Web search module** (l.204-392): seven-compound benchmark; baselines incl. Claude 1.3 & Falcon-40B; 1-5 scale; browsing improves planning; hallucination grounding (Fig 2).
- **Documentation search module** (l.395-597): ada embeddings + vector search; OT-2 API; ECL SLL three investigations; ExperimentHPLC on caffeine; air-bubble QC; 1,110 samples (Fig 3).
- **Controlling laboratory hardware** (l.599-708): OT-2 liquid handler; plate-drawing prompts; UV-Vis color problem with NumPy-array feedback (Fig 4).
- **Integrated chemical experiment design** (l.710-767): full Suzuki + Sonogashira design→execute; post-cutoff heater-shaker; GC-MS product confirmation; heater-shaker error→doc→fix; five-transformation compound-library study with RDKit (Fig 5).
- **Chemical reasoning capabilities** (l.1291-1696): optimization "game" over Perera & Doyle datasets as lookup tables; normalized advantage / NMA metric; GPT-4 vs GPT-3.5 vs Bayesian optimization; names vs SMILES; reasoning from SMILES (Fig 6).
- **Discussion** (l.1698-1713): proof of concept; capabilities emerge with tools; safety / dual-use concerns.
- **Technology use disclosure** (l.1715-1719); **Data/Code availability** (l.1898-1911; safety hold + simpler GitHub impl); Acknowledgements, Author contributions, Competing interests (aithera.ai co-founders; ECL ties); References (52); **Extended Data Figs 1-3** (colour-problem transcript; generated OT-2 code; extra Bayesian-optimization comparisons).
