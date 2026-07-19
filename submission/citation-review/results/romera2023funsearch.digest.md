# Digest: romera2023funsearch

**Bibliographic.** Romera-Paredes, B., Barekatain, M., Novikov, A., Balog, M., Kumar, M. P., Dupont, E., Ruiz, F. J. R., Ellenberg, J. S., Wang, P., Fawzi, O., Kohli, P. & Fawzi, A. "Mathematical discoveries from program search with large language models." *Nature* 625, 468–475 (18 January 2024). Published online 14 December 2023. DOI 10.1038/s41586-023-06924-6. Open access. Affiliations: Google DeepMind (London); Dept. of Mathematics, Univ. of Wisconsin–Madison; LIP, Univ. of Lyon. Article type: Nature Article (peer-reviewed).

---

## Thesis / problem
LLMs have strong capabilities but "confabulate" (hallucinate) plausible-but-incorrect statements, which blocks their use for scientific discovery. The paper introduces **FunSearch** ("searching in the function space"): an **evolutionary procedure that pairs a pretrained (frozen) LLM with a systematic evaluator**. The evaluator guards against confabulations; the LLM supplies creative but not-necessarily-correct programs. FunSearch searches for **programs that describe *how* to solve a problem** (a `solve`/`priority`/`heuristic` function), not for the solution objects themselves. The paper claims it surpasses best-known results on (a) the **cap set problem** (extremal combinatorics) and (b) **online bin packing** (combinatorial optimization). Central argument for novelty: surpassing SOTA on established open problems proves the discoveries are genuinely new, not retrieved from training data.

## Method — the evaluator IS a formal/deterministic oracle (YES)
FunSearch validates every LLM-generated program against a **deterministic, code-executed `evaluate` function** — a formal/numeric oracle, not an LLM judge.

- **Input to FunSearch = a specification consisting of an `evaluate` function** that scores candidate solutions, plus an initial program to evolve (can be trivial) and optionally a skeleton.
- **Deterministic pass/fail + numeric score.** Evaluators execute generated programs on inputs of interest and score outputs with `evaluate`. Programs that **do not execute within imposed time/memory limits, or produce invalid outputs, are discarded** (deterministic reject). Valid programs get a real-valued score; scores across inputs are combined by an aggregation function (e.g., mean).
- **Cap set `evaluate` (Fig. 2a):** `evaluate(candidate_set, n)` returns `len(candidate_set)` **iff** `utils_capset.is_capset(candidate_set, n)` is True, else `None`. So: formal check "is this actually a cap set?" → then numeric size.
- **Bin packing `evaluate` (Fig. 2b):** returns `-count_used_bins(...)` **iff** `utils_packing.is_valid_packing(bins, problem)` is True, else `None`. Formal validity check → then negative bin count.
- **The loop (Fig. 1):** programs database (stores correct programs) → best-shot prompting samples k=2 programs from one island, sorted low→high score (`priority_v0`, `priority_v1`), appends empty `priority_v2` header → prompt fed to pretrained LLM → new programs → evaluators score via `evaluate` → correct ones stored → repeat. Evolution uses an **islands model** (multiple subpopulations) for diversity.
- **LLM:** Codey (built on the PaLM2 family), fine-tuned on code, publicly accessible via API; used **without any fine-tuning on the problems** (frozen). Chosen for fast inference over higher-quality slow inference. Results use ~10^6 samples. Appendix A compares to StarCoder (open-source) and reports results are not very sensitive to LLM choice given a large-enough code corpus.

The oracle is what distinguishes FunSearch from raw LLM use: it "guards against confabulations and incorrect ideas."

---

## FACTS TABLE (exhaustive)

### Cap set sizes — largest cap set in Z_3^n (Fig. 4a) — VERIFIED against figure image
| n | Best known | FunSearch |
|---|---|---|
| 3 | 9 | 9 |
| 4 | 20 | 20 |
| 5 | 45 | 45 |
| 6 | 112 | 112 |
| 7 | 236 | 236 |
| 8 | 496 | **512** |

- Only the n=8 value is improved (496 → 512); all others match best-known. The 512-cap in n=8 is the headline finite-dimensional discovery. | Fig. 4a + body.
- FunSearch discovered a **program** (Fig. 4b `priority`) that generates the set of **512 eight-dimensional vectors**; manual simplification yields explicit construction `build_512_cap` (Fig. 4c). | Fig. 4b,c.
- Exact size of largest cap set known **only for n ≤ 6**. | Body (Extremal combinatorics).
- Search space "quickly becomes enormous," stated as **"around 3^1600 for n = 8"** (pdftotext rendered the superscript as "31,600"; the intended value is 3^1600, i.e. astronomically large). | Body. [FLAG: exact string worth double-checking if a manuscript cites this number.]
- Previously best-known n=8 construction relied on a complex combination of lower-dimensional cap sets (refs 33,34); FunSearch found it "from scratch" without being taught how to combine cap sets. | Body.
- Construction properties similar to the **Hill cap** (refs 35,36), which gives the **optimal 112-cap in Z_3^6**. | Body + Fig. 4 caption.

### Cap set capacity C — lower bounds (Fig. 5a) — VERIFIED against figure image
Capacity C = sup_n c_n^{1/n}. Upper bound **C ≤ 2.756** (breakthrough, ref 31). Paper contributes lower bounds via constant-weight admissible sets A(n,w); I(n,w) = full-size admissible set.
| Bound on C | Admissible set ingredient | Source |
|---|---|---|
| 2.2101 | I(90, 89) | Ref. 37 |
| 2.2173 | I(10, 5) | Ref. 34 |
| 2.2180 | I(11, 7) | Ref. 38 |
| 2.2184 | I(12, 7) | **FunSearch** |
| 2.2194 | I(15, 10) | **FunSearch** |
| 2.2202 | A(24, 17) | **FunSearch** |

- Prior SOTA lower bound = **2.2180** (ref 38, via SAT solvers). FunSearch's I(12,7) improves it to **2.2184**. | Body.
- FunSearch full-size **I(15,10)** → C ≥ **2.219486** (table shows 2.2194). | Body.
- FunSearch partial admissible set **A(24,17) of size 237,984** → new lower bound **2.2202**. Described as "largest improvement in 20 years to the asymptotic lower bound" / "great improvement compared to research in the last 20 years," but still far from upper bound 2.756. | Body.
- Trivial representation of A(24,17) = "more than 200,000 vectors," but generating program is "a few lines of code." | Discussion.
- Discovered `priority` (Fig. 5b) for I(12,7) treats coordinate triples {0,4,8},{1,5,9},{2,6,10},{3,7,11} symmetrically → led to searching "symmetric" admissible sets (smaller search space, higher dims/weights). | Fig. 5b + body.

### Online bin packing (Table 1) — fraction of excess bins over L2 lower bound, lower is better — VERIFIED against table image
Columns: OR1, OR2, OR3, OR4 (OR-Library, ref 23), Weibull 5k, Weibull 10k, Weibull 100k (ref 24).
| Heuristic | OR1 | OR2 | OR3 | OR4 | Weibull 5k | Weibull 10k | Weibull 100k |
|---|---|---|---|---|---|---|---|
| First fit | 6.42% | 6.45% | 5.74% | 5.23% | 4.23% | 4.20% | 4.00% |
| Best fit | 5.81% | 6.06% | 5.37% | 4.94% | 3.98% | 3.90% | 3.79% |
| **FunSearch** | **5.30%** | **4.19%** | **3.11%** | **2.47%** | **0.68%** | **0.32%** | **0.03%** |

- FunSearch outperforms both first fit and best fit **across ALL datasets and instance sizes**. | Table 1 + body.
- Heuristic trained only on OR1-sized instances; **generalizes** to larger instances, performing even better and widening the gap to best fit. | Body.
- On Weibull 100k, FunSearch is **only 0.03% off the L2 lower bound** on the optimum. | Body (matches table).
- Baselines: **first fit** = first bin with enough space; **best fit** = bin with least available space where item still fits. FunSearch evolves the `heuristic`, starting from best fit. | Body.
- Discovered strategy (Fig. 6): assign item to least-capacity bin only if fit is very tight; otherwise place where more space remains — avoids leaving unfillable small gaps. | Fig. 6.

### System / hyperparameters
| Value | Location | Context |
|---|---|---|
| k = 2 | Body + Methods | # programs sampled per prompt; two functions beat one, diminishing returns beyond |
| ~10^6 | Body | Total number of LLM samples used for paper's results |
| 15 samplers, 150 CPU evaluators | Body | Typical setup; 150 = 5 CPU servers × 32 evaluators in parallel |
| Every 4 h | Methods | Island reset interval: discard programs from worst m/2 islands, reseed from best of surviving m/2 |
| 60% | Methods (Robustness) | Fraction of I(12,7) experiments finding a full-size admissible set; every run improves prior best capacity bound |
| 4 out of 140 | Methods (Robustness) | Experiments that discovered the size-512 cap set (n=8 direct construction is "particularly challenging") |
| Boltzmann / softmax selection | Methods, Eq. (1) | Cluster sampling prob P_i = exp(s_i/T_cluster)/Σ; T_cluster = T0(1 − (n mod N)/N) |
| Within-cluster: favor shorter programs | Methods | prob ∝ exp(ℓ̃_i / T_program), ℓ_i = negative char length |

---

## Scope & limitations (explicit)
FunSearch works best when: (1) an **efficient evaluator** is available; (2) a **"rich" scoring signal** exists (real-valued improvement, not a binary pass/fail); (3) a **skeleton with an isolated part to evolve** can be provided.

## Does NOT claim / boundaries
- **Theorem proving falls OUTSIDE scope** — "it is unclear how to provide a rich enough scoring signal" for generating proofs (refs 52–54). (Contrasts with MAX-SAT, where # satisfied clauses is a usable signal.)
- The LLM "does not use much context about the problem"; it "should instead be seen as a source of diverse (syntactically correct) programs with occasionally interesting ideas." The discoveries come from LLM + evolution + evaluator, not from LLM reasoning alone.
- **No fine-tuning / no training** of the LLM; API inference only. Frozen off-the-shelf model.
- Lower bound on cap set capacity (2.2202) is "still far from the upper bound" (2.756) — no claim to close the gap.
- Did **not** explore semantic-preserving applications (e.g., performance-improving code edits) in the main text — only claims FunSearch "could be" effective there.
- A fixed skeleton "may constrain the space of programs that can be discovered" — acknowledged tradeoff, argued to help overall by focusing LLM on the critical part.
- Robustness caveat: because of LLM/evolutionary randomness, some problems need many independent repetitions to beat prior best (n=8 cap set: 4/140).

## Section map
Abstract → Intro (easy-to-evaluate vs hard-to-solve; NP-complete/max-independent-set/MAX-CSP examples; FunSearch overview & 4 ingredients: best-shot prompting, skeleton evolving only critical logic, island-based evolution, asynchronous scaling) → Components: Specification, Pretrained LLM, Evaluation, Programs database, Prompt, Distributed approach → Extremal combinatorics: Cap sets (Fig. 3 = Z_3^2 example, Fig. 4), Admissible sets (Fig. 5) → Bin packing (Table 1, Fig. 6) → Discussion (Kolmogorov complexity / concise-program inductive bias; interpretability; symmetry discovery; 3 problem characteristics) → Methods (Distributed system; Prompt building; Evolutionary method & program selection incl. Eq. 1; Robustness; Related work: LLMs / Genetic programming / Program superoptimization & SW engineering) → Data & Code availability (OR-Library only external data; code at github.com/google-deepmind/funsearch; uses Codey via API + StarCoder; launchpad library + sandbox) → Extended Data Figs 1–3 (best-shot prompt example; island evolution; clusters within islands).

Additional discoveries deferred to Supplementary Information Appendix B: **corners problem** and **Shannon capacity of cycle graphs** (not detailed in main text).
