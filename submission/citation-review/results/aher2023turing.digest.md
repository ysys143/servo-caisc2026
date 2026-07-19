# Digest: aher2023turing (BLIND first-pass)

**Full title:** Using Large Language Models to Simulate Multiple Humans and Replicate Human Subject Studies
**Authors:** Gati Aher (Olin), Rosa I. Arriaga (Georgia Tech), Adam Tauman Kalai (Microsoft Research)
**arXiv:** 2208.10264v5 [cs.CL], 9 Jul 2023 (this version July 11 2023)
**Read basis:** full body + all appendices (A–F) + Tables 1–4 + Figures, pdftotext of the 43-page PDF.

---

## Thesis / problem

Introduces a **"Turing Experiment" (TE)**: a new type of test for evaluating *to what extent a given
language model (e.g. GPT models) can faithfully simulate different aspects of human behavior*, and for
revealing *consistent distortions* in a model's simulation. Explicitly contrasted with Turing's Imitation
Game (IG): the IG simulates a *single arbitrary individual* and has "limited diagnostic value"; a TE
instead requires simulating **a representative sample of participants in human-subject research**. The
paper carries out four TEs that attempt to **replicate well-established findings from prior human-subject
studies**, and uncovers a "hyper-accuracy distortion."

## Method — direct answers to the tasked questions

**Q1. Does it use LLMs to SIMULATE MULTIPLE HUMANS and REPLICATE human-subject studies (a Turing
Experiment)? — YES, unambiguously.** This is the paper's central contribution. A single program writes
zero-shot prompts fed to an LM; the LM's completion reconstructs a "record" (a text transcript of a
simulated experiment). Multiple distinct simulated humans are produced by varying **name + gender title**
(Mr./Ms./Mx. + surname). Four TEs replicate classic studies:
- **Ultimatum Game** (behavioral economics — fairness/rationality)
- **Garden Path Sentences** (psycholinguistics — parsing)
- **Milgram Shock Experiment** (social psych — obedience to authority)
- **Wisdom of Crowds** (collective intelligence — general-knowledge estimation)

In the first three TEs, existing findings were replicated by the largest model (LM-5); the fourth TE
revealed a distortion instead of replicating cleanly.

**Q2. Does it validate via statistical tests? — YES.** Validation uses comparison of simulation outcomes
against **external prior human-subject results**, plus quantitative statistics:
- **Validity/validity-rate Z** (fraction of generations meeting format criteria; Table 1; SE < 0.05%).
- **Pearson correlations** of acceptance probability across offers (> 0.9 within offers 1–4 and 6–9) to
  show name-sensitivity is consistent, not random.
- **Significance test on gender:** acceptance-probability distributions differ by gender of pairing at
  **p < 1e−16**.
- **Medians / IQRs / quartiles** vs. human medians+IQRs and vs. ground truth (Wisdom of Crowds, Tables 3–4).
- **Standard errors of the mean** on garden-path ungrammatical fractions (error bars).
- Counts of participants reaching each shock level vs. Milgram (1963).

**Q3. Does it discuss a CIRCULAR-VALIDITY risk (generator and simulated subjects sharing the same model,
so the validator measures model self-consistency rather than external fact)? — NO, not as such.**
This is important and nuanced:
- The paper's *validation philosophy is the opposite of circular*: outcomes are always benchmarked against
  **external human-subject data** (Milgram 1963; Christianson 2001; Moussaïd 2013; Houser & McCabe 2014;
  Krawczyk 2018; Galton 1907), never against the model's own self-report as ground truth. The "validity
  rate" Z is only a *format*-adherence measure, not a truth measure.
- HOWEVER, the paper does contain an **un-flagged self-referential structure**: in the Milgram TE the
  **same LM generates the subject's free-response behavior AND classifies (via 2-choice prompts) whether
  that behavior counts as shock / no-shock / termination / (dis)obedience** — i.e. "the LM is effectively
  also playing the role of an experimenter" (§6; App. F). The paper presents this neutrally as methodology
  and does **not** raise it as a validity/circularity concern.
- The closest *named* risks the paper does discuss are DIFFERENT from circular validity:
  (a) **Training-data contamination / memorization** ("the models have almost certainly been trained on
      descriptions of these experiments"), addressed by authoring 3 novel variations (own garden-path
      sentences, novel "submersion" destructive-obedience scenario, own general-knowledge questions), and
      by requiring TEs be zero-shot.
  (b) **Author-bias reflection**: "the simulations will reflect the biases of the [training-data] authors
      rather than the behavior of humans in the population."
- **Net:** The specific circular-validity argument (validator measures generator self-consistency, not
  external fact) is **NOT stated** in this paper. Any citation claiming Aher et al. "discuss/raise/warn of
  circular validity when generator == simulated subject" would be OVERREACHING; the paper's stated
  safeguards are external-benchmark comparison + zero-shot + novel-scenario contamination controls.

---

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| 4 TEs replicated | Abstract, §1 | Ultimatum Game, Garden Path, Milgram Shock, Wisdom of Crowds |
| 5–6 LMs evaluated (paid OpenAI API) | §1 (line 101) | first three TEs on 5 models; WoC on 6 |
| 8 models total, LM-1..LM-8 | §3 (line 339–341) | text-ada-001, text-babbage-001, text-curie-001, text-davinci-001, -002, -003, gpt-35-turbo (ChatGPT), gpt-4 |
| LMs 6–8 released recently, used only in last study | §3 (342–343) | released after first three TEs done |
| temperature = 1, top p = 1 | §3 (344) | completion sampling params (unmodified softmax) |
| U.S. 2010 Census surnames; 100 per racial group | §3, App. A | ≥90% of holders reported that race |
| 5 racial groups | App. A | Amer. Indian/Alaska Native; Asian/NHPI; Black/African American; Hispanic/Latino; White |
| 1,000-name pool | §3 (352) | 2 titles × 5 groups × 100 surnames |
| Mx. title added | §3 (353), §7 | non-binary, only in Wisdom of Crowds TE |
| hyper-accuracy distortion | Abstract, §7, §9 | present in ChatGPT & GPT-4; likely from alignment (Ouyang 2022) |
| aluminum melting point 660 °C | §1 (131), Table 3 | example "obscure quantity" answered perfectly |
| GPT-4 story: moon 238,900 miles | §1 (144) | anecdotal 5-year-old story |
| 60 mph; 3,982 hours; 166 days | §1 (146–150) | unrealistic child-arithmetic in that story |
| **Ultimatum Game first studied Güth et al. (1982)** | §4 (369) | proposer/responder split of $10 |
| endowment $10, 11 offers {0..10} | §4 (377–378) | Ultimatum Game inputs |
| 10,000 name pairs (of 1M possible) | §4 (379–380) | 500 surnames × 5 groups × 2×2 titles; each of 1,000 names used as responder 10× |
| gender diff p < 1e−16 | §4 (422) | acceptance distributions differ by pairing gender |
| male accept 60% of $2 offer (from female) | §4 (424) | chivalry direction |
| female accept 20% of $2 offer (from male) | §4 (424–425) | chivalry direction |
| Pearson r > 0.9 (offers 1–4, 6–9) | §4 (418) | name-pair consistency across offers |
| chivalry hypothesis | §4 (427–430) | Eckel & Grossman (2001) |
| 2,500 Mr.-Ms. + 2,500 Ms.-Mr. pairings | Fig 5 (456–457) | gender-distribution comparison |
| Ultimatum sources | §3 (355–356) | Houser & McCabe (2014); Krawczyk (2018) |
| **Garden path 24 sentences (12 OT + 12 RAT)** | App. D (901–903) | from Christianson et al. (2001) |
| 24 control sentences = GP + disambiguating comma | App. D (903–906) | e.g. "While the student read, the notes..." |
| 24 authored GP sentences (12 OT + 12 RAT) | App. D.1, Fig 12 | novel-variation control |
| LM-4: 3 reversed instances; LM-3 & LM-5: 0 | App. D (926–927) | GP rated lower-ungrammatical than control |
| Garden path sources | §3, App. D | Christianson et al. (2001); Patson et al. (2009); phenomenon: Crain & Steedman (1985) |
| **Milgram (1963) obedience studies** | §6 (490) | 30 shock levels |
| voltages 15–450 V, 15-V increments, 30 switches | §6, App. F (1898–1899) | slight→XXX designations |
| 300 V = 20th shock (victim starts refusing) | §6 (514–516) | inflection point |
| Milgram (1963) Exp 1: 26/40 followed to end | Fig 7 (516–517) | human baseline |
| Milgram TE: 75/100 simulated followed to end | Fig 7 (517–518) | LM-5 result |
| 25/100 sims stopped early (termination classifier) | App. F (1589) | 23 of 25 after Shock Level 20 |
| 100 uniquely named subjects | App. F (1560–1561) | top-10 surnames × 5 groups × Mr./Ms. |
| Human obedience 65.0% (n=40); LM-5 75.0% (n=100) | Fig 22 | break-off distributions |
| Novel destructive-obedience: 75 obeyed, 25 terminated early | App. F (1642–1643) | "submersion" scenario |
| spikes after 20th & 22nd submersion | App. F (1644–1645, Fig 25) | victim honks / goes silent |
| 4 experimenter prods (+Prod 1*) | Fig 21 | "please continue" ... "you have no other choice" |
| Yale University, $5 payment | App. F (1660, 1889) | setup taken from Milgram (1963) |
| Mr. Lopez record terminated after 5 disobediences at 420 V | App. F (1684–1685) | sample transcript |
| **Wisdom of Crowds: Galton (1907) 787 ox-weight estimates** | §7 (527) | median error 9 lb (<1%), IQR 74 lb |
| Moussaïd et al. (2013): 52 subjects | §7 (531–532) | general-knowledge study source |
| 10 questions (5 Moussaïd + 5 authored) | §7 (533), App. E | see truth values below |
| 1,500 simulated title+surname combos | App. E (1191–1193) | 500 surnames × 3 titles (Mr./Ms./Mx.) |
| LM-6 majority exactly correct on all 10 Qs | §7 (534–535) | extreme hyper-accuracy |
| 0 IQR = majority identical responses | App. E (1205–1206) | interpretation note |
| Truth values (10 Qs) | Table 3/4 | bones 206; Al m.p. 660; 100°C=212°F; Mars yr 687 days; sound 343 m/s; ribs 24; gold m.p. 1064; light 299,792,458 m/s; piano 88; dog chromosomes 78 |
| Human medians (5 Moussaïd Qs) | Table 3 Human col | bones 190 (IQR 108); Al 240 (532); °F 200 (195); Mars 365 (376); sound 333 (884) |
| LM-8 rounds light to 3×10^8 (300000000) | Table 4 (1428, 1510) | gpt-4 behavior |
| extra "alignment-ladder" models | App. E (1413) | davinci, text-davinci-001/002/003 tested for Wisdom-vs-Alignment |
| **Table 1 validity rates (%)** | Table 1 | UG: 88.0/93.8/99.4/98.6/99.5; GP: 97.6/99.2/97.9/95.5/95.5; WoC: 51.0/94.4/88.0/98.0/99.0 (LM-1..LM-5); all SE<0.05% |
| BIG-bench > 200 tasks (19 social, 16 emotion) | §1.1 (197–198) | Srivastava et al. (2022) |
| Commonsense Norm Bank > 1.7M moral judgments | §1.1 (198–199) | Jiang et al. (2021), Project Delphi |
| Warwick & Shah (2016): "13-year-old troublemaker" | §1 (49–50) | early IG attempt |
| Argyle et al. (2023) "Out of one, many" | §1.1 (186–189) | concurrent; survey-result probabilities (contrast: they predict survey probs, this paper replicates behavior experiments) |
| alignment cause hypothesis | §1 (133–134) | distortion "may be due to alignment (Ouyang et al., 2022)" |
| code URL | §3 (363) | github.com/GatiAher/Using-Large-Language-Models-to-Replicate-Human-Subject-Studies |

---

## Scope & limitations (as the paper states them)

- "This work is merely an initial exploration of the concept of TEs" (§9). Only a handful of LMs; single
  API vendor (OpenAI); most other LMs cannot handle the long Milgram prompts.
- Simulations may reflect **training-data author bias** rather than population behavior.
- Models "have almost certainly been trained on data that includes descriptions of these experiments" →
  contamination risk; mitigated (not eliminated) by 3 novel-variation datasets and zero-shot requirement.
- Ethics: torturing simulated agents (Darling 2016); some TEs "should simply never be performed."
- Gender findings in humans are real but "not uniformly consistent" (Eckel & Grossman 2001).
- Novel destructive-obedience results "cannot be directly compared to human responses due to differences
  in the experimental setup."

## Does NOT claim / boundaries (guard against over-citation)

- Does **NOT** claim TEs replace human-subject studies; frames them as a complementary evaluation +
  possible *pre-study* design aid ("may predate a human subject study").
- Does **NOT** claim faithful simulation of *all* behaviors — the whole point is to find which behaviors
  are distorted (e.g., Wisdom of Crowds failed to replicate; larger models did worse).
- Does **NOT** discuss "circular validity" / model-self-consistency-as-validator (see Q3 above); validation
  is external-benchmark-based. The Milgram TE's LM-as-its-own-classifier structure is used but never
  problematized.
- Does **NOT** claim a general win in the Turing/Imitation Game; explicitly says IG has "limited diagnostic
  value."
- Does **NOT** do fine-tuning; all zero-shot prompting on off-the-shelf models.
- No agent-based / multi-turn *interacting* population; each simulated human is generated independently
  (except Milgram's sequential single-subject record).

## Section map

- §1 Introduction (+ §1.1 Related Work: LMs Representing Humans; LM Evaluation; Improving LMs; Prompt
  Design; Bias in LMs; Tests of Human Simulation)
- §2 Running TEs Using LMs (queries, completion vs. k-choice prompt, validity rate Z, outputs/records,
  prompt validation to avoid p-hacking)
- §3 Models and Datasets (LM-1..LM-8; names; study-specific datasets)
- §4 The Ultimatum Game TE
- §5 Garden Path Sentences TE (brief; details in App. D)
- §6 Milgram Shock TE (details in App. F)
- §7 Wisdom of Crowds TE (details in App. E)
- §8 Risks and Limitations
- §9 Conclusion
- App. A Surnames; B TE Input Summary Table; C Ultimatum Game details; D + D.1 Garden Path details;
  E Wisdom of Crowds details (Tables 3–4); F + F.1 + F.2 Milgram Shock algorithm, transcripts, novel
  destructive-obedience scenario.
