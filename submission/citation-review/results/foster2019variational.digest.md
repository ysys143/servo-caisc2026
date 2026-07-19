# Digest: foster2019variational

**Full title:** Variational Bayesian Optimal Experimental Design
**Authors:** Adam Foster, Martin Jankowiak, Eli Bingham, Paul Horsfall, Yee Whye Teh, Tom Rainforth, Noah Goodman
**Venue:** NeurIPS 2019 (33rd Conf. on Neural Information Processing Systems, Vancouver, Canada)
**ID:** arXiv:1903.05480v3 [stat.ML], 14 Jan 2020, 28 pages
**Affiliations:** Univ. of Oxford (Statistics), Uber AI Labs, Stanford Univ.

---

## Thesis / Problem

Bayesian optimal experimental design (BOED) chooses experiment designs `d` to maximize the **expected information gain (EIG)** about parameters of interest `theta`. The central obstacle: computing/estimating the EIG is hard because it is a **nested (doubly-intractable) expectation** -- neither the posterior `p(theta|y,d)` nor the marginal `p(y|d)` is available in closed form, so conventional Monte Carlo cannot be applied, and nested MC (NMC) has poor convergence (O(T^-1/3) vs O(T^-1/2) for conventional MC). The paper's goal is to make EIG estimation fast and accurate so BOED becomes practical, especially for sequential/adaptive experiments that must run in real time.

## Method -- CONFIRMED: this IS variational EIG estimation for BOED

**YES.** The paper proposes VARIATIONAL methods to estimate/approximate the EXPECTED INFORMATION GAIN (EIG) in Bayesian optimal experimental design. This is the paper's core contribution, stated in the abstract ("we introduce several classes of fast EIG estimators by building on ideas from amortized variational inference") and the title. It introduces **four variational EIG estimators**, each a variational bound (or bounded-error approximation) on the EIG, trained by stochastic gradient methods, exploiting amortized variational inference so information is shared across outcome values `y` (rather than a separate inner estimate per sample as in NMC). The four estimators:

1. **mu_post (variational posterior)** -- learns amortized posterior approximation `q_p(theta|y,d)`; **lower** bound on EIG; Eq (6); works with implicit likelihoods; tight iff `q_p = p(theta|y,d)`; tightness = expected forward KL. Generalizes the Barber-Agakov [3] MI bound to the design setting.
2. **mu_marg (variational marginal)** -- learns marginal approximation `q_m(y|d)`; **upper** bound; Eq (9); requires explicit likelihood; tight iff `q_m = p(y|d)`.
3. **mu_VNMC (variational NMC)** -- learns proposal `q_v(theta|y,d)` for an importance-sampling estimate of `p(y|d)`; **upper** bound (Eq 10/11); the **only** consistent one -- asymptotically unbiased as L->infinity even when the variational family does not contain the true posterior. Standard NMC is a special case (proposal = prior).
4. **mu_m+l (variational marginal + likelihood)** -- learns both `q_m(y|d)` and `q_l(y|theta,d)`; Eq (12); works with implicit likelihoods; **NOT a bound** (neither upper nor lower in general); error bounded by Lemma 2.

Design optimization over `d` (given a base EIG estimator) uses **Bayesian optimization**. Implementation provided in the **Pyro** probabilistic programming system.

## FACTS TABLE (exhaustive)

| value | location | context |
|---|---|---|
| EIG(d) = E_p(y|d)[H[p(theta)] - H[p(theta|y,d)]] | Eq (1), Intro | definition of expected information gain |
| IG(y,d) = H[p(theta)] - H[p(theta|y,d)] | Eq (2), Sec 2 | information gain (entropy reduction prior->posterior) |
| EIG = mutual information between theta and y given d | Sec 2 (after Eq 3) | equivalent interpretation |
| d* = arg max_d EIG(d) | Sec 2 | Bayesian optimal design |
| NMC rate O(T^-1/3) | Intro, Sec 2 | best achievable rate for nested MC (Rainforth et al. [33]) |
| NMC RMSE O(N^-1/2 + M^-1) | Sec 2 | consistent as N,M->infinity |
| optimal to set M proportional to sqrt(N) (NMC) | Sec 2 | yields overall O(T^-1/3) |
| conventional MC rate O(T^-1/2) | Intro | contrast baseline |
| variational estimators rate O(T^-1/2) | Abstract, Sec 4, Thm 1 | when variational family contains target; T=O(N+K), N proportional to K |
| mu_VNMC converges to EIG at O((NM)^-1/3) | Sec 4 | when M proportional to sqrt(N), second (bias-removal) stage |
| VNMC total cost T = O(KL + NM), typically M >> L | Sec 4 | two-stage cost |
| four EIG estimators introduced | Abstract, Sec 3 | mu_post, mu_marg, mu_VNMC, mu_m+l |
| error decomposition into 3 terms (I MC variance, II bound-gap after K steps, III tightest-bound gap) | Sec 4 | triangle-inequality breakdown |
| Polyak-Ruppert averaged SGD of [28] | Thm 1, Sec 4 | gives K^-1/2 optimization rate |
| Table 1 -- summary of estimators | p.5 | columns: Implicit / Bound / Consistent / Eq |
| mu_post: Implicit yes, Lower bound, Consistent no, Eq (6) | Table 1 | |
| mu_marg: Implicit no, Upper bound, Consistent no, Eq (9) | Table 1 | |
| mu_VNMC: Implicit no, Upper bound, Consistent yes, Eq (11) | Table 1 | |
| mu_m+l: Implicit yes, (no bound), Consistent no, Eq (12) | Table 1 | |
| mu_NMC (baseline): Implicit no, Upper, Consistent yes, Eq (4) | Table 1 | |
| mu_laplace (baseline): Implicit no, no bound, not consistent, Eq (75) | Table 1 | |
| mu_LFIRE (baseline): Implicit yes, no bound, not consistent, Eq (76) | Table 1 | |
| mu_DV (baseline): Implicit yes, Lower, not consistent, Eq (77) | Table 1 | |
| Table 2 -- bias^2 & variance, 5 runs, 4 benchmarks | p.6 | bold = lowest empirical MSE |
| A/B test -- mu_post bias^2 1.33e-2, var 7.15e-3 | Table 2 | Gaussian linear model |
| A/B test -- mu_marg 7.45e-2, 6.41e-3 | Table 2 | |
| A/B test -- mu_VNMC 3.44e-3, 3.38e-3 | Table 2 | |
| A/B test -- mu_NMC 4.70e0, 3.47e-1 | Table 2 | NMC far worse |
| A/B test -- mu_laplace 1.92e-4, 1.47e-3 | Table 2 | Laplace best here (Gaussian -> exact) |
| A/B test -- mu_LFIRE 2.29e0, 6.20e-1 | Table 2 | |
| A/B test -- mu_DV 4.34e0, 8.85e-1 | Table 2 | |
| Preference -- mu_post 4.26e-2, 8.53e-3; mu_marg 1.10e-3, 1.99e-3; mu_VNMC 4.17e-3, 9.04e-3 | Table 2 | economics / revealed preference |
| Mixed effects -- mu_post 2.34e-3, 2.92e-3; mu_m+l 6.90e-6, 1.84e-5 (best) | Table 2 | implicit likelihood; mu_m+l best |
| Extrapolation -- mu_post 1.24e-4, 5.16e-5; mu_m+l 7.84e-6, 4.11e-5 | Table 2 | implicit likelihood |
| "All our methods outperformed NMC" | Sec 6.1 | key empirical claim |
| optimal K/T between 0.5 and 0.9 gives lowest RMSE | Sec 6.2, Fig 1d | budget split, N+K=5000 fixed |
| theta dim = 2, y dim = 10 (A/B test) | Sec 6.2 | explains mu_post > mu_marg |
| 100 trials (Fig 1), 10 independent runs (Figs 3,4,8) | Fig captions | error bars +/-1 std err |
| Mechanical Turk: 36 possible designs, 8 participants x 10 questions per run | Sec 6.3, App D.2 | adaptive psychology experiment (stylized faces) |
| 30s turnaround per design step | App D.2 | online adaptive loop |
| 9 characters, 2 feature dims x 3 levels | Fig 7, App D | stylized-face stimuli |
| CES model with latent rho, alpha, u; designs d in [0,100]^6 | Sec 6.3, App D.3 | economics utility-inference experiment |
| computation budgets: 10s (A/B, preference, extrapolation), 60s (mixed effects) per estimator | App D | Table 2 timing |
| Death process (epidemiology), design (t1,t2), log-normal prior on rate b | App E.1 | additional experiment; LogNormal posterior ~1e-3 error |
| Laplace error ~30% higher than posterior method (death process) | App E.1, Fig 10 | |
| Barber & Agakov [3] used mu_post-type bound for MI over noisy channels | Sec 3 | prior use; "connection to experiment design not previously made" |
| Poole et al. [31] variational MI bounds; mu_marg bound studied there in MI context | Sec 3, Sec 5 | "not utilized for BOED before" |
| Donsker-Varadhan (DV) bound [11], used by Belghazi et al. [4] (MINE) | Sec 5, App C | baseline mu_DV |
| LFIRE method of Thomas et al. [41], via Kleinegesse & Gutmann [18] | Sec 5 | implicit-likelihood baseline mu_LFIRE |
| Pyro implementation | Abstract, Sec 1, App D | docs.pyro.ai/en/stable/contrib.oed.html |
| BOED application domains: psychology [30], Bayesian optimization [16], active learning [15], bioinformatics [42], neuroscience [38] | Sec 1 | prior BOED applications |
| EPSRC grant EP/N509711/1; ERC grant 617071 | Acknowledgements | funding |

## Scope & Limitations

- **Assumptions of Theorem 1 are strong** (strong convexity of `f`, Lipschitz gradients/Hessian); the paper explicitly notes they "may well not hold in practice." SGD may converge to a **local** optimum phi-dagger rather than global phi-star, adding asymptotic bias (Sec 4, App B).
- Estimators mu_post, mu_marg, mu_m+l **converge to a biased estimate** if the variational family does not contain the target distribution (only mu_VNMC is guaranteed consistent).
- mu_marg and mu_VNMC **require explicit (evaluable) likelihoods**; mu_post and mu_m+l handle implicit likelihoods.
- mu_m+l is **not a bound** in the general case (only a lower bound in the special coupled case `q_m = E_p(theta)[q_l]`, App A.4).
- Reverse-KL posterior approximation (as in ELBO) can cause **mode-dropping / discontinuous, design-dependent bias** in EIG (App G) -- motivates their forward-KL / directly-EIG-tied training.

## Does NOT claim / boundaries

- Does **not** propose a new design-optimization algorithm -- it uses existing Bayesian optimization; explicitly states "our focus is on the base EIG estimator."
- Does **not** claim variational estimators are universally best -- Laplace wins for the Gaussian linear (A/B) model where its approximation is exact.
- Not about generic variational inference of posteriors for their own sake; the variational objectives are **directly tied to EIG estimation** (contrasted with ELBO-based approaches like EDDI / Ma et al. [26]).
- No claim of guaranteed global optimization; no claim the strong-convexity assumptions hold generally.
- Not an LLM / AI-agent / automated-science paper -- this is a statistics/ML methods paper on information-theoretic experimental design.

## Section Map

- **Sec 1 Introduction** -- BOED, EIG definition (Eq 1), nested-expectation problem, contribution overview
- **Sec 2 Background** -- BOED framework, EIG as mutual information (Eq 3), NMC estimator (Eq 4), sequential BOED (Eq 5)
- **Sec 3 Variational Estimators** -- the four estimators (mu_post, mu_marg, mu_VNMC, mu_m+l), Lemmas 1 & 2, Table 1, sequential use, estimator-selection guide
- **Sec 4 Convergence rates** -- 3-term error decomposition, Theorem 1 (O(T^-1/2)), VNMC bias removal
- **Sec 5 Related work** -- NMC, Laplace [22,25], LFIRE [18,41], Donsker-Varadhan / MINE [4,11], Poole et al. [31]
- **Sec 6 Experiments** -- 6.1 EIG accuracy (Table 2, 4 benchmarks), 6.2 convergence rates (Fig 1-2), 6.3 end-to-end sequential (Mechanical Turk psychology + CES economics)
- **Sec 7 Discussion**
- **Appendices A-G** -- A proofs of estimators/bounds; B Theorem 1 proof; C extended related work; D full experiment details; E death-process experiment; F control-variate consistent estimator; G forward vs reverse KL
