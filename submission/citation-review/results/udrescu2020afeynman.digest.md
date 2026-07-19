# Digest: udrescu2020afeynman

**Title:** AI Feynman: a Physics-Inspired Method for Symbolic Regression
**Authors:** Silviu-Marian Udrescu, Max Tegmark (Dept. of Physics & Center for Brains, Minds & Machines, MIT; Tegmark also Theiss Research)
**Venue:** Science Advances 6, eaay2631 (April 15, 2020). arXiv:1905.11481v2 [physics.comp-ph].
**Read basis:** Full paper (15p, pdftotext), read end to end.

---

## Thesis / Problem

Symbolic regression = finding a symbolic (analytic) expression that matches a data table `{x1,...,xn, y}` where `y = f(x1,...,xn)`, for an *unknown* mystery function `f`. The general problem is likely NP-hard (search space of symbol strings grows exponentially with length). Their thesis: functions of practical interest (esp. physics) exhibit **symmetries, separability, compositionality, smoothness, low-order polynomial structure, and known units** that can be discovered and exploited to recursively break hard problems into easier sub-problems. Contribution: a **recursive multidimensional symbolic regression algorithm** that combines neural-network fitting with physics-inspired techniques.

## Method — direct answers to the team-lead's key questions

**Does AI Feynman FIT EQUATIONS TO DATA via symbolic-regression SEARCH? — YES.** It takes a data table as input and searches for a symbolic expression matching it. The core symbolic search is the **brute-force module**, which "simply tries all possible symbolic expressions within some class, in order of increasing complexity" (strings in reverse Polish notation over a fixed symbol alphabet, Table I). Success = a symbolic formula reproducing the data.

**Is the search DETERMINISTIC? — YES, the symbolic search is deterministic (exhaustive enumeration), explicitly contrasted with genetic/stochastic algorithms.** The brute-force module enumerates all syntactically valid strings by increasing length — this is deterministic, not a randomized/evolutionary search. Dimensional analysis (null-space linear algebra) and polynomial fit (solving linear systems for coefficients) are also deterministic. The *only* stochastic component is neural-network training (Adam, random init), but the NN is not the search: it is an interpolator used to *test for* symmetry/separability so variables can be eliminated. The paper repeatedly contrasts itself with Eureqa, a **genetic algorithm** (stochastic search with mutation/selection that can drift/get stuck in local optima). AI Feynman's progress "is virtually guaranteed to be a step in the right direction" — deterministic variable reduction vs. genetic stochastic approximation.

**Is validation EMPIRICAL (fit to data)? — YES.** A module "declares success" when the r.m.s. fitting error drops below a threshold (e.g. brute-force tolerance `εbr = 10^-5`, polyfit `εpol = 10^-4`). Final answer-checking is *symbolic*: a candidate `f'` is deemed correct if algebraic simplification of `f' − f` (Mathematica `Simplify` or sympy `simplify`) yields the symbol "0". So: empirical fit-to-data drives the search; symbolic identity confirms correctness (they have ground-truth equations in the database).

**Cross-problem memory transfer, or fresh each time? — FRESH EACH TIME. No cross-problem memory/learning transfer.** Every mystery is solved from scratch. When the algorithm transforms a mystery (via symmetry/separability/etc.), the sub-problems are passed to "**a fresh instantiation of our full AI Feynman symbolic regression algorithm**" (recursion *within* one problem). A new neural network is trained per mystery ("For each mystery we generated 100,000 data points..."). Nothing learned on one equation is carried to another. The only cross-problem element is manual **hyperparameter tuning**: the 100 basic mysteries were used as a "training set" to tune hyperparameters, which were then frozen (Table II) for the 20 "bonus" mysteries used as a held-out "test set" — but this is human hyperparameter selection, not automated memory/weight transfer between problems.

### Algorithm modules (six strategies, recursively combined)
1. **Dimensional analysis** — uses known physical units (unit vector of 5 integers: m, s, kg, T/kelvin, V) to reduce to dimensionless variables via null-space of the units matrix `M` (`Mp=b`, `MU=0`); reduces variable count.
2. **Polynomial fit** — tests degrees 0..dmax=4 via linear system; declares success if r.m.s. error ≤ εp.
3. **Brute force** — deterministic enumeration of symbol strings (reverse Polish notation), three symbol subsets tried in turn; two variants auto-solve for multiplicative/additive constants; uses a description-length (DL) criterion (Eq. 2, following Wu & Tegmark [30]) to combat overfitting in discrete string space.
4. **Neural-network-based tests** — train NN to interpolate `f`, then test for translational/scaling symmetry (Algorithm 1) and additive/multiplicative separability (Algorithm 2, Eq. 3), and "setting variables equal." Each discovered property reduces variable count and recursively re-launches the full algorithm.
5. **Extra transformations** — apply sqrt/square/log/exp/inverse/trig to dependent & independent variables before bf/polyfit.

Figure 1 = schematic flowchart; Figure 2 = worked example on Newton's gravitation (Eq. I.9.18, 9 variables) reduced by DA → 6 dimensionless vars → NN reveals 2 translational symmetries + multiplicative separability → factorize → polyfit.

---

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| 100 equations | Abstract; §III.A; Tables IV–V | Feynman Lectures equations in database; AI Feynman discovers **all 100 (100%)** |
| 71 (71%) | Abstract; §III.B (line "Eureqa solved 71%") | Prior publicly-available software (Eureqa) cracks only 71 of the 100 basic mysteries |
| **68%** | §IV.A Key findings | States "Eureqa [26] discovered **68%** of the Feynman equations" — **INTERNAL INCONSISTENCY** with the 71% figure quoted in Abstract & §III.B |
| 15% → 90% | Abstract; §III.E; §IV.A | Bonus (harder) test set: Eureqa 15%, AI Feynman 90% ("improve state of the art from 15% to 90%") |
| 20 bonus equations | §III.A, §III.E | "bonus" set from Goldstein, Jackson, Weinberg, Schwartz; selected as famous+complicated; used as held-out test set |
| 2 failures (of 20) | §III.E | AI Feynman failed on: Radiated gravitational wave power; Jackson 2.11 |
| ~2 years / ~100× age of universe | §III.E | Brute-force time the two failures would have required (exceeding 2h limit) |
| 93% | §III.B | AI Feynman success rate when the **dimensional-analysis module is disabled** (still 93%, relying heavily on NN) |
| 66.7% vs 48.9% | §III.E | On the McDermott et al. [41] test set: AI Feynman 66.7%, Eureqa 48.9% |
| 6 simplifying properties | §II | Units, Low-order polynomial, Compositionality, Smoothness, Symmetry, Separability |
| 6 hidden layers | §II.E.1 | NN: feed-forward fully connected, softplus activation; first 3 layers 128 neurons, last 3 layers 64 neurons |
| 100,000 data points | §II.E.1 | Generated per mystery for NN; 80% train / 20% validation |
| 100 epochs, lr 0.005, batch 2048 | §II.E.1 | NN training; RMS-error loss, Adam optimizer, weight decay 10^-2, FastAI package |
| β1 max 0.95 / min 0.85, β2=0.99; lr ratio 20; 10% iters last part | §II.E.1 | NN momentum/lr schedule (Smith & Topin [31,32]) |
| dmax = 4 | §II.C | Polynomial fit tries degrees 0..4 |
| εbr = 10^-5 | Table II | Brute-force tolerance |
| εpol = 10^-4 | Table II | Polynomial fit tolerance |
| ε0NN = 10^-2 | Table II | Validation-error tolerance for NN use |
| εsep = 10·εNN | Table II | Separability tolerance |
| εsym = 7·εNN | Table II | Symmetry tolerance (4σ would suffice if Gaussian; chose 7) |
| λ = Nd^(1/2) | Table II; Eq. 2 | Description-length hyperparameter (accuracy vs complexity) |
| 6.5 GB | §III.A footnote 3 | Size of the Feynman Symbolic Regression Database (FSReD), freely downloadable |
| 10^5 rows | §III.A | Rows per mystery data table; inputs sampled uniformly between 1 and 5 |
| 1–9 independent variables | §III.A | Range of variable count across the 100 equations |
| +,−,∗,/,sqrt,exp,log,sin,cos,arcsin,tanh | §III.A | Elementary functions appearing in the 100 equations |
| 2 hours CPU / mystery | §III.B | Max CPU time allotted per mystery for both methods |
| 4 CPUs, 300 data points | §III.B footnote | Eureqa run configuration (no NN, so extra data doesn't help) |
| 10 data points (typical) | §III.C | Most equations solved by polyfit/bf with only 10 points; some need 100; NN-requiring ones need 10^2–10^6 |
| ε=10^-4 / 10^-2 | §III.D | Noise robustness: most recovered at relative noise ≤10^-4; ~half still solved at 10^-2. Noise added to dependent variable only |
| 1601, 4 years, ~40 failed attempts | §I | Kepler / Mars orbit ellipse framing anecdote [ref 1] |
| github.com/SJ001/AI-Feynman | §II.B footnote; Acknowl. | Public code |
| space.mit.edu/home/tegmark/aifeynman.html | §III.A; Acknowl. | Public database |
| Eureqa (Nutonian) | §III.B; refs [26,27] | Genetic-algorithm competitor; "best competitor by far"; implements Schmidt & Lipson [27] |

## Scope & limitations (stated in paper)

- General symbolic regression is likely **NP-hard** and "remains unsolved"; their method exploits *physics-specific* structure, not a general solver.
- **Excludes** equations involving derivatives or integrals (equations were "prioritized... excluding ones involving derivatives or integrals").
- Performs **worse on arbitrary function compositions** (McDermott [41] set, 66.7%) than on genuine physics formulas, precisely because arbitrary compositions "lack the symmetries, separability, etc." the NN exploits.
- Brute force can take **longer than the age of the universe** for complex reduced expressions (cause of both bonus failures).
- Imperfect NN fitting introduces "**de facto noise**" (~10^-3 to 10^-5) that complicates downstream steps even on clean data; better architectures (target 10^-6) listed as future work.
- Noise tested only on the **dependent variable**, not independent variables; **not yet tested on real-world/experimental data** (both flagged as future work).
- Has **tunable hyperparameters** (Table II) — like most ML methods.

## Does NOT claim / boundaries

- Does **not** claim a general/complete solution to symbolic regression (explicitly NP-hard, structure-dependent).
- Does **not** perform continuous numerical parameter optimization over free constants the way Eureqa does — "This strategy is currently implemented in Eureqa but not AI Feynman" (only auto-solves for simple additive/multiplicative constants in bf). Listed as a possible future upgrade.
- Does **not** transfer learning/memory across different mystery problems (fresh NN + fresh algorithm instantiation per problem/sub-problem).
- Does **not** use a genetic/evolutionary search (that is the competitor Eureqa); its symbolic search is deterministic brute-force enumeration guided by NN-discovered structure.
- Does **not** validate against real measured physics data in this paper — validation is on synthetic data generated from known ground-truth equations, checked by symbolic identity.

## Section map

- **I. Introduction** — symbolic regression definition, Kepler framing, genetic-algorithm background, Eureqa as SOTA.
- **II. Methods** — A. Overall algorithm (Fig 1, 2); B. Dimensional Analysis; C. Polynomial Fit; D. Brute Force (Table I symbols, Eq. 2 DL criterion); E. Neural-network-based tests (1. NN training, 2. Translational symmetry, 3. Separability [Eq. 3], 4. Setting variables equal); F. Extra transformations. Table II = hyperparameters; Table III = unit table.
- **III. Results** — A. FSReD database (Tables IV, V = 100 eqs; Table VI = 20 bonus); B. Method comparison vs Eureqa; C. Dependence on data size; D. Dependence on noise; E. Bonus mysteries + McDermott [41] comparison.
- **IV. Conclusions** — A. Key findings; B. Opportunities for further work.
- **Algorithm 1** (translational symmetry pseudocode), **Algorithm 2** (additive separability pseudocode). References [1]–[41].
