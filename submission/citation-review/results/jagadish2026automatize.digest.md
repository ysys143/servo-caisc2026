# Digest — jagadish2026automatize

**Full title:** "Can we automatize scientific discovery in the cognitive sciences?"
**Authors:** Akshay K. Jagadish, Milena Rmus, Kristin Witte, Marvin Mathony, Marcel Binz, Eric Schulz (corresponding: eric.schulz@helmholtz-munich.de)
**Affiliations:** Princeton AI Lab (Princeton University); Institute for Human-Centered AI, Helmholtz Munich; LMU Munich
**Venue/ID:** arXiv:2603.20988v1 [cs.AI], 22 Mar 2026. 5 pages, 21 references.
**Type:** Perspective / opinion / position piece (a "vision" paper, not an empirical study — no new experiments, data, or results are reported here).

---

## Thesis / Problem

The cognitive sciences try to understand intelligence by formalizing cognitive operations as computational models. The standard discovery cycle has four stages: (1) researchers develop a paradigm, (2) collect human data, (3) handcraft and test a predefined model class, (4) the community reviews and iterates. This manual pipeline is bottlenecked by the slowness of human involvement at every step (hypothesis-to-publication can span years) and by a hypothesis space limited to researchers' familiar designs, intuitions, and biases.

**Proposal:** a paradigm shift to a "fully automated, in silico science of the mind" that implements every stage of the discovery cycle using LLMs — an end-to-end automated closed loop. The four automated stages map to: proposing experiments (LLM/grammar as experiment sampler), generating data (foundation model of cognition as synthetic-behavior generator), synthesizing models (LLM-based program synthesis over algorithmic hypotheses), and closing the loop (LLM-critic optimizing "interestingness"). The loop is framed as a "high-throughput in-silico discovery engine" that surfaces informative experiments/mechanisms for later validation in real human populations.

---

## Method (there is no empirical method — it is a proposed architecture)

The paper describes a conceptual four-component pipeline (Figure 1):
1. **Proposing experiments** — a formal task language; suggested starting point is generative grammars over experiments (e.g., a grammar over Markov Decision Processes / MDPs, spanning multi-armed bandits to multi-step planning). Proposes eventually using an LLM itself as an "intelligent experiment sampler" that refines designs from feedback.
2. **Generating data** — synthetic behavioral data produced by a **foundation model of human cognition**, specifically "recent iterations of the Centaur model" (ref 12). Tasks expressed in natural language; choices/outcomes appended to trial history and re-prompted trial-by-trial. Plans to scale datasets by an order of magnitude and condition generation on subject-specific metadata (demographics, questionnaire/psychiatric scores) to simulate targeted participant profiles.
3. **Synthesizing models** — replace handcrafted models with LLM-based program synthesis; cites the authors' own GeCCo pipeline (Rmus and Jagadish et al., ref 16) synthesizing cognitive models as Python functions with iterative feedback refinement; also evolutionary/hybrid approaches (AlphaEvolve ref 17, FunSearch ref 18).
4. **Closing the loop** — an LLM-critic ("LLM-as-judge") scores each discovery tuple for "interestingness" (novelty, compressibility/simplicity, qualitative signatures, transferability) and biases the next experiment proposal.

### IMPORTANT — targeted audit questions

**(A) Does it discuss using a BEHAVIORAL FOUNDATION MODEL as a proxy for experiments (synthetic participant data in lieu of human subjects)?**
**YES — explicitly and centrally.** The entire "Generating data" section (lines 98–117) proposes generating **synthetic behavioral data** using **foundation models of cognition** (Centaur, ref 12) *in place of* collecting data from human participants. Quote: "the cycle proceeds to the generation of synthetic behavioral data. This is achieved using recent iterations of the Centaur model, a foundation model of human cognition." It claims such models "can generate de novo data that are often indistinguishable from human behavior" and can be conditioned on demographics/psychometrics to "simulate not just a generic agent, but a targeted participant profile" (e.g., "a 30-year-old individual with high scores in obsessive-compulsive traits"). Figure 1 labels this step "Cognitive foundation model produces behavioral data for proposed set-up." So: the behavioral foundation model IS the proxy for running experiments on human subjects.

**(B) Does it explicitly FLAG synthetic data as a hypothesis accelerator NOT ground truth?**
**YES — explicitly.** In the Discussion (lines 185–190): "Second, synthetic data generation is not guaranteed to be a faithful substitute for humans. Behavioral foundation models may rely on shortcuts, drift toward 'average' subjects, or fail under genuine distribution shift. Even plausible-looking behavior can be produced for the wrong reasons, yielding an illusion of mechanistic clarity. **A pragmatic stance is to treat such models as accelerators for hypothesis generation rather than as ground truth**: they should be continuously calibrated against benchmark effects, challenged with adversarial tasks designed to expose heuristics, and, where appropriate, complemented or replaced by smaller, local simulators tuned to specific task families." The Abstract and body also repeatedly frame outputs as candidates "for subsequent validation in real human populations" / "validated in vivo with human participants."

**(C) Does it give NO criterion for escalating to in-vivo validation? (i.e., is a criterion absent?)**
**Largely YES — no concrete/operational escalation criterion is given.** The paper repeatedly asserts that top outputs should be validated with real humans, but the only selection rule offered is qualitative: "**The highest-scoring discoveries** can then be validated in vivo with human participants" (line 160) — "highest-scoring" per the LLM-critic's interestingness metric. It also says outputs are surfaced "for subsequent validation in real human populations" (abstract) and calls for "norms that keep automated discovery tethered to empirical validation" (line 213). But there is **no explicit threshold, no statistical gate, no quantitative decision rule, no cost/benefit criterion, and no procedure** specifying *when* or *how much* to escalate to in-vivo testing. The critic's calibration recommendations ("continuously calibrated against benchmark effects," "adversarial tasks") describe ongoing checks, not an escalation trigger. So the caveat (accelerator-not-ground-truth) is present, but a concrete escalation criterion for moving from synthetic to human validation is effectively absent — it is left as a hand-wave to "highest-scoring."

---

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| arXiv:2603.20988v1 [cs.AI] | line 9 | Preprint ID / category |
| 22 Mar 2026 | line 9 | Submission date |
| 5 pages | footers "2/5"…"5/5" | Paper length |
| 6 authors | lines 3–4 | Jagadish, Rmus, Witte, Mathony, Binz, Schulz |
| 3 affiliations | lines 5–7 | Princeton AI Lab; Helmholtz Munich (Institute for Human-Centered AI); LMU Munich |
| eric.schulz@helmholtz-munich.de | line 11 | Corresponding author |
| 21 references | lines 225–261 | Reference count |
| Four stages / four-stage cycle | lines 28–32, 43–44 | Discovery cycle: propose experiments → generate data → synthesize models → close loop |
| Centaur model | lines 100, 105; ref 12 | The named foundation model of human cognition used to generate synthetic behavioral data; ref 12 = "A foundation model to predict and capture human cognition. Nature 644, 1002–1009 (2025)" |
| Nature 644, 1002–1009 (2025) | ref 12 (line 246) | Centaur citation (Binz et al.) |
| GeCCo | lines 127–128; ref 16 | "Guided generation of Computational Cognitive Models" pipeline; ref 16 = Rmus, Jagadish, Mathony, Ludwig & Schulz, NeurIPS (Thirty-ninth Annual Conference on NeurIPS) |
| FunSearch | line 134; ref 18 | Program-search example; ref 18 = Romera-Paredes et al., Nature 625, 468–475 (2024) |
| AlphaEvolve | ref 17 (line 252) | Evolutionary coding agent; arXiv:2506.13131 (2025), Novikov et al. |
| MDPs (Markov Decision Processes) | lines 87–89 | Proposed grammar substrate; "formally defined by environmental states, transition dynamics, and reward structures" |
| multi-armed bandits → multi-step planning | line 89 | Range of decision tasks MDP grammar can capture; refs 10, 11 |
| "order of magnitude" | line 108 | Planned scale-up of datasets for foundation models |
| "30-year-old individual with high scores in obsessive-compulsive traits" | lines 111–112 | Example of targeted synthetic participant profile |
| Metadata fields (Fig 1) | lines 62–69 | Age, Sex, Education, Diagnosis, Questionnaires, Health status, Genetic risk, Life history |
| Critic report dimensions (Fig 1) | lines 76–81 | Interestingness, Novelty, Fit to literature, Quality, Uncertainty |
| "interestingness" | lines 21, 147, 154, 197 | Core loop-closing metric; LLM-critic / LLM-as-judge scores discovery tuples |
| Discovery tuple | lines 150–151 | (proposed experiment, simulated participant profile(s), generated data, model space) scored by critic |
| Library of Babel (Borges) | lines 164–167, 213 | Central metaphor: automated science risks generating mostly worthless "books"; goal is to surface the rare valuable ones |
| "validated in vivo with human participants" | line 160 | Escalation endpoint; only the "highest-scoring discoveries" |
| Funding: NAM Fellowship (Scully Peretsman foundation); Helmholtz Association; ERC Starting Grant "Towards an Artificial Cognitive Science"; Wellcome Discovery Award | lines 218–220 | Acknowledgements |

---

## Scope & Limitations (as stated by the paper itself)

The Discussion is candid about failure modes; it frames the "central risk" as **epistemic failure** ("producing persuasive-looking results that are scientifically hollow"), not merely technical failure. Named weaknesses, one per pipeline stage:
1. **Experiment design** bounded by the expressibility/interpretability of the task grammar — "No search procedure can discover what the representation forbids"; grammar must cover many domains and be pressure-tested.
2. **Synthetic data** not guaranteed faithful to humans (shortcuts, drift to "average" subjects, distribution shift, "illusion of mechanistic clarity") — hence the accelerator-not-ground-truth stance and calibration recommendations.
3. **Model discovery over programs** is a rugged, non-smooth optimization space; tiny code edits break models; distinct mechanisms can be behaviorally indistinguishable; LLM search inherits training priors/stylistic biases; metrics can be gamed; no guarantee of global optimum.
4. **Interestingness signal** "both enticing and dangerous" — a critic could reward "theatrical novelty," drift to edge cases, or be gamed into "superficial weirdness." Recommends a multi-objective critic (novelty + robustness + parsimony + generalization + unification), not a single scalar oracle.

## Does NOT claim / Boundaries

- Does **not** report any empirical results, benchmarks, or new experiments — it is a forward-looking proposal ("imminent reality," "vision").
- Does **not** claim to eliminate the human scientist: "this does not eliminate the scientist"; humans "define the problem, the expressiveness of the task language, the structure of the output model family, evaluation principles, the shape of the expected theory, and other constraints." Automation is framed as an "amplifier."
- Does **not** claim synthetic data can replace human validation — explicitly positions it as accelerator, with final validation "in vivo."
- Does **not** provide an operational/quantitative criterion (threshold, statistical gate, decision rule) for *when* to escalate a discovery to in-vivo human testing — only "highest-scoring."
- Does **not** claim foundation models reliably generalize out-of-distribution — acknowledges this "remains a subject of ongoing debates," citing only that "current evidence suggests they can (at least to some extent)" extrapolate (ref 14).

## Section Map

- **Abstract** (lines 13–23)
- **Introduction** (lines 25–46) — standard 4-stage cycle, its structural constraints, the inflection-point argument
- **Figure 1** (lines 52–85) — the automated discovery cycle diagram (experimentalist → cognitive foundation model → modeller → critic)
- **Proposing experiments** (lines 48–96) — grammars over experiments, MDPs, LLM-as-experiment-sampler
- **Generating data** (lines 98–117) — Centaur / cognitive foundation model produces synthetic behavioral data, metadata conditioning
- **Synthesizing models** (lines 119–137) — LLM program synthesis, GeCCo, FunSearch/AlphaEvolve
- **Closing the loop** (lines 139–161) — objective for discovery, optimal experimental design, interestingness, LLM-critic, in-vivo validation of highest-scoring
- **Discussion** (lines 163–215) — Library of Babel metaphor, four failure modes, upside (individual differences / computational psychiatry, neuroscience, perception, generalization crisis)
- **Acknowledgements** (lines 217–220)
- **References** (lines 224–261) — 21 entries
