# Digest: odonoghue2023bioplanner

**Full title:** "BioPlanner: Automatic Evaluation of LLMs on Protocol Planning in Biology"
**Venue:** Accepted at EMNLP 2023 (official version in ACL Anthology). Preprint arXiv:2310.10632v1, 16 Oct 2023.
**Authors:** Odhran O'Donoghue, Aleksandar Shtedritski, John Ginger, Ralph Abboud, Ali Essa Ghareeb, Justin Booth, Samuel G Rodriques.
**Affiliations:** Align to Innovate; Francis Crick Institute; Future House; University of Oxford.
**Dataset name:** BioProt. Code/data: github.com/bioplanner/bioplanner.

---

## Thesis / problem
Automatically generating accurate protocols for scientific experiments would be a major step toward automating science, but (a) LLMs struggle with multi-step / long-horizon planning, and (b) there is no established *automatic* way to evaluate the accuracy of a generated protocol — evaluation has required manual expert review. NLG metrics (BLEU, BERTScore) fail because protocols are sensitive to tiny details (order of actions, substance relations) and the same protocol can be validly described at many granularities. The paper's answer: convert protocol writing into a **pseudocode reconstruction task** that can be scored automatically, and release a dataset (BioProt) to support it.

## Method — the two questions, answered directly

**(1) Does BioPlanner GENERATE experimental PROTOCOLS via pseudocode AND auto-evaluate LLMs on protocol planning? YES — with an important scope caveat.**

The core framework is a **teacher/student** setup (Fig 1):
- A **teacher** model (GPT-4) converts a full free-text protocol (title + description + step-by-step instructions) into (i) a protocol-specific set of **pseudofunctions** (the admissible action space) and (ii) **pseudocode** using only those pseudofunctions. This generated pseudocode, after an automatic feedback/error loop plus manual review, becomes the **ground truth**.
- A **student** model is then given only the admissible pseudofunctions + a short description and must reconstruct the pseudocode from scratch. This "converts the process of writing a scientific protocol into a series of multiple-choice questions (pick a pseudofunction from a provided set)", which is scored automatically.
- Tasks defined (Sec 4): **Next-Step Prediction**, **Protocol Generation** (full pseudocode), **Function Retrieval** (identify which pseudofunctions a protocol needs). Models evaluated: GPT-3.5, GPT-4, and (appendix) Llama2-7B.
- Separately, a **Real-World Validation** (Sec 5.5-5.6): a Toolformer-like CoT GPT-4 agent retrieves pseudofunctions from BioProt and generates a *novel* protocol. So the framework does also GENERATE novel protocols (not just reconstruct), but only 2 were generated and 1 executed.

So: it (a) auto-generates pseudocode ground-truth protocols, (b) auto-evaluates LLM protocol-planning ability against that ground truth, and (c) in a small demo, generates + lab-executes a novel protocol.

**(2) Are the validation signals/metrics described as WEAK / insufficient to autonomously close a loop (no biological-validity ground truth)? SUBSTANTIALLY YES.**

Two distinct "validation" layers must not be conflated:
- **The automatic metrics measure pseudocode-RECONSTRUCTION fidelity against the (LLM-generated, manually-corrected) ground-truth pseudocode — NOT biological validity / experimental success.** The ground truth is itself GPT-4 output that was manually edited (see Table 3). There is no experimental / wet-lab ground-truth signal in the automatic loop. The metrics are: function accuracy, function precision/recall, normalized Levenshtein distance (order), argument-name precision/recall, argument-value BLEU, and SciBERTScore (cosine similarity of SciBERT-encoded argument values).
- **The GPT-4-as-evaluator self-evaluation signal is explicitly weak.** Given description + admissible functions + ground-truth pseudocode + predicted pseudocode, GPT-4 is asked which better matches the description. Result: GPT-4 "only performs slightly above chance in identifying the ground truth protocol, versus LLM generations, although it is unclear whether this is because the machine-generated protocols are largely correct, or because GPT-4 is unable to distinguish correct from incorrect protocols." The paper also cites prior work that GPT evaluators prefer longer/more coherent but not necessarily more correct generations, and that self-evaluation contradicts human evaluation / is systematically biased.
- **Biological validity is checked only by manual review + a single lab execution**, not by the automatic metrics. Of 2 generated novel protocols, only the E. coli one was actually run; it succeeded (cells viable after -80 °C storage). The Symbiodinium protocol was not executed ("we did not have Symbiodinium available").
- The Conclusion itself hedges performance: evaluating GPT-3.5/GPT-4 "we find that there is more to be desired in terms of performance." Function retrieval "results on this task appear generally poor."

Net: the framework provides a *robust automatic proxy* for planning ability (better than NLG metrics), but the paper does NOT claim its automatic signal captures biological correctness, and its one biological-validity check is a single manual lab run — i.e., the automatic loop has **no biological-validity ground truth** and cannot by itself close an autonomous discovery loop.

## FACTS TABLE (exhaustive)

| value / finding | exact location | context |
|---|---|---|
| Protocols.io has **over 9,000** public protocols | Sec 3.1 (l.259) | source database |
| BioProt = **100 protocols** | Table 1 (l.382) | final curated dataset size |
| Average number of steps = **12.5** | Table 1 (l.383) | dataset stat |
| Average total protocol length = **641.0 tokens** | Table 1 (l.384) | dataset stat |
| Average tokens per step = **52.6** | Table 1 (l.385) | dataset stat |
| Average tokens per original description = **83.8** | Table 1 (l.386) | dataset stat |
| Average tokens per generated (GPT-4) description = **66.3** | Table 1 (l.387) | machine descriptions are shorter |
| Avg pseudofunctions per protocol = **10.3** | Table 2 (l.393) | pseudocode stat |
| Avg pseudofunctions per step = **0.82** | Table 2 (l.394) | pseudocode stat |
| Avg lines of pseudocode = **17.2** | Table 2 (l.395) | pseudocode stat |
| **59%** of generated protocols required **no edits** (59 of 100 completely accurate) | Table 3 (l.440); l.448 | manual verification headline |
| **24%** had 1-3 edited lines; **17%** had >3 edited lines | Table 3 (l.441-442) | verification breakdown |
| Avg **11.8** line edits in edited files | Table 3 (l.443) | verification breakdown |
| Most common error = **missing units** (usually harmless); more impactful = missing step details / unexplained material composition | l.450-458 | error taxonomy |
| Models: **GPT-3.5, GPT-4** (OpenAI API); Llama2-7B (appendix) | Sec 5.1; App D | models under test |
| Embeddings for nearest-neighbour = **text-embedding-ada-002** | l.649-650 | implementation |
| **Next-step (GPT-4, no shuffle):** accuracy **70.6**, fn precision 97.1, recall 94.9, arg SciBERTScore 87.9, BLEU 0.351 | Table 4 (l.595-608) | GPT-4 best next-step acc |
| **Next-step (GPT-3.5, no shuffle):** accuracy **65.0**, precision 97.7, recall 94.7, SciBERTScore 88.5, BLEU 0.363 | Table 4 (l.568) | GPT-3.5 next-step |
| Shuffling functions drops accuracy sharply: GPT-4 70.6→**57.0**, GPT-3.5 65.0→**36.1** | Table 4 (l.574-595) | function order is a leaked signal |
| GPT-4 consistently beats GPT-3.5 on next-step *function* prediction; GPT-3.5 slightly better on *arguments* | l.665-668 | result |
| **Protocol generation:** biggest GPT-4>GPT-3.5 gap is in Levenshtein (order); precision/recall of functions similar | l.674-680; Table 5 | GPT-4 better at ordering |
| Shuffling input functions consistently lowers protocol-generation performance | l.680; Table 5 | robustness finding |
| **Function retrieval (GPT-4):** Nearest P **32.5** / R **39.2**; Random P **48.8** / R **49.4** | Table 6 (l.833-843) | "generally poor" |
| **Function retrieval (GPT-3.5):** Nearest P **24.2** / R **35.7**; Random P **36.7** / R **45.2** | Table 6 (l.821-831) | poor; nearest harder than random |
| Nearest-neighbour retrieval worse than random b/c semantically identical fns (Mix vs MixSubstance) penalized | l.859-864 | ambiguity artifact |
| **GPT-4-as-evaluator score** (rate GPT-4 prefers model output over ground truth): GPT-3.5 35.6-40.9; GPT-4 40.9-43.9 | Table 8 (l.1026-1049) | "only slightly above chance" |
| GPT-4-generated descriptions **consistently outperform** original scientist descriptions (e.g., next-step acc 46.1→48.4) | Table 7 (l.926-996); l.999-1001 | machine descriptions help |
| Total API cost ≈ **$1000** | Limitations (l.1106-1107) | resource note |
| Real-world validation: **2** novel protocols generated (E. coli glycerol stock; Symbiodinium DNA extraction+gel); **1** (E. coli) executed | Sec 5.5-5.6 (l.904-1071) | biological validation |
| E. coli protocol ran successfully: cells viable after -80 °C, grew on nutrient agar after ~10 h; control (no E. coli) no growth | Fig 3 (l.1078-1084); l.1069-1072 | single wet-lab success |
| Both generated protocols reviewed by a scientist, judged "accurate and sufficient for a competent lab scientist to follow" | l.1064-1067 | manual (not automatic) validity check |
| **Llama2-7B** significantly underperforms GPT-3.5/GPT-4 in function selection; feedback *distracts* Llama; could NOT complete next-step prediction | App D (l.1571-1586); Tables 9-10 | open-source model weak; feedback loop helps GPT not Llama |
| Human benchmark — function selection: Precision **87.5%**, Recall reported as "0.84%" (n=20) → "significant increase over GPT-4" | App F (l.1609-1611) | human > GPT-4 on retrieval (note: recall figure printed as 0.84% is internally inconsistent with the >GPT-4 claim; likely 84%) |
| Human benchmark — next-step prediction accuracy **54.8%** (n=32), arg P/R 97%/95%; "roughly comparable to GPT-4 in shuffled setting" | App F (l.1615-1617) | human ≈ GPT-4 shuffled |
| Ground-truth pseudocode generated via one-shot prompt + automatic feedback loop (flags: invalid Python, no pseudofunctions defined, missing args, missing units) then GPT-4 self-check | Sec 3.2 (l.402-413) | how ground truth is built |

## Scope & limitations (as stated in paper)
- **Paid closed API** (GPT-3.5/GPT-4), ~$1000 total; authors call for testing open-source LLMs (Sec 7 Limitations).
- **Biology only**; extensible in principle to chemistry / materials science but not demonstrated there (Limitations).
- **Misuse risk** acknowledged: framework/dataset could inform synthesis of harmful compounds; authors state they curated BioProt to exclude easily-misused protocols.
- Ground truth is **LLM-generated then manually corrected** — not an independently authored gold standard; 41% of protocols needed some edit.
- The automatic evaluation exploits that pseudofunctions are "defined in the order they appear in the original protocol," which leaks ordering; shuffling is introduced to remove this crutch.

## Does NOT claim / boundaries
- Does **NOT** claim the automatic metrics measure biological validity or experimental success — they measure fidelity of reconstructed pseudocode to a pseudocode ground truth.
- Does **NOT** claim a fully autonomous closed-loop discovery system; BioPlanner is an *evaluation framework + dataset*, plus a small proof-of-concept generation demo.
- Does **NOT** claim strong self-evaluation: GPT-4-as-evaluator is only "slightly above chance," and the paper explicitly cautions GPT evaluators favor longer/coherent over correct outputs.
- Does **NOT** validate broadly in the wet lab — only **1** protocol (a standard E. coli overnight-culture + glycerol cryopreservation, not a scientific discovery) was executed; the second was reviewed but not run.
- Does **NOT** claim state-of-the-art protocol generation — "there is more to be desired in terms of performance"; function retrieval is "generally poor."
- Does **NOT** claim superiority to humans — human function-selection precision (87.5%) exceeds GPT-4; human next-step is comparable to GPT-4.

## Section map
- **Abstract** (l.32-57): automatic evaluation framework + BioProt; teacher→pseudocode, student→reconstruct; evaluate GPT-3/GPT-4; externally validate by generating + running one lab protocol.
- **Fig 1** (l.79-83): teacher/student pseudocode evaluation schematic.
- **Intro** (l.100-159): motivation; NLG-metric failure; robotic-planning inspiration (closed admissible action set); six contributions.
- **Related Works** (l.163-237): LLMs for science; task decomposition; planning (PDDL, tool-use); evaluating LLM scientists (manual today); automatic evaluation & self-evaluation biases.
- **Sec 3 BioProt dataset** (l.241-503): 3.1 collection from Protocols.io (>9,000); 3.2 translate to pseudocode via GPT-4 + feedback loop (Fig 2, Table 1/2); 3.3 manual verification (Table 3, 59% no edits); 3.4 machine-generated descriptions.
- **Sec 4 Metrics & evaluation** (l.504-638): Next-Step Prediction (accuracy, arg precision/recall, BLEU, SciBERTScore); Protocol Generation (+ normalized Levenshtein Ldn for order); Function Retrieval.
- **Sec 5 Experiments** (l.640-1084): 5.1 implementation; 5.2 results (Tables 4-6); 5.3 GPT-4 as evaluator (Table 8, "slightly above chance"); 5.4 machine descriptions; 5.5 real-world validation setup (Toolformer-like CoT agent, 2 protocols); 5.6 real-world results (E. coli executed, Fig 3).
- **Sec 6 Conclusion** (l.1086-1099): framework + dataset + tasks/metrics; "more to be desired in performance"; one lab-executed protocol.
- **Sec 7 Limitations** (l.1101-1137): paid API/$1000; other fields; misuse.
- **Appendices** (l.1351-1640): A filtering; B prompts; C qualitative (protocol id 145 ethanol precipitation); D Llama2-7B eval (Tables 9-10); E data/code; F human benchmarking.
