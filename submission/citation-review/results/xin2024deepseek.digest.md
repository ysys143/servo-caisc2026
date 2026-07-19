# Digest: xin2024deepseek

**Full title:** DeepSeek-Prover-V1.5: Harnessing Proof Assistant Feedback for Reinforcement Learning and Monte-Carlo Tree Search
**Authors:** Huajian Xin, Z.Z. Ren, Junxiao Song, Zhihong Shao, et al. — DeepSeek-AI
**Venue/ID:** arXiv:2408.08152v1 [cs.CL], 15 Aug 2024 (preprint)
**Code:** https://github.com/deepseek-ai/DeepSeek-Prover-V1.5
(Digest based ONLY on this paper.)

---

## Thesis / Problem

Formal theorem proving in **Lean 4** is hard for LLMs: proofs must satisfy the rigorous formal
specifications of a verification system, and even GPT-4 struggles. Two paradigms exist —
proof-step generation (predict one tactic, verify, repeat, usually with tree search) and
whole-proof generation (emit an entire proof, computationally cheap). The predecessor
DeepSeek-Prover-V1 used whole-proof generation but suffered **compounding errors** (Ross et al.,
2011): no access to intermediate tactic states during long-horizon generation.

The paper's contribution is a **unified approach** combining both paradigms via a
**truncate-and-resume mechanism**, plus RL from proof-assistant feedback and a new MCTS variant
(RMaxTS). Result: a 7B model that is state-of-the-art among open-source formal provers.

## Method — Proof-kernel validation (IMPORTANT for audit)

**YES — DeepSeek-Prover-V1.5 validates every generated proof against the Lean 4 proof
assistant/kernel, which returns a DETERMINISTIC pass/fail.** This is central, not incidental:

- **Verification:** Generated Lean 4 code is submitted to "the Lean prover"/"Lean 4 theorem
  prover" for verification. If the proof is correct and complete, the procedure terminates; if an
  error is detected, the code is truncated at the **first error message** (lines 116-123). At
  evaluation, "generated proofs are then verified using the Lean 4 theorem prover" importing
  Mathlib4 and Aesop, subject to a **300-second time limit** (lines 498-501).
- **Binary reward = pass/fail:** "each generated proof receives a reward of 1 if verified as
  correct, and 0 otherwise" (line 367); Figure 2 calls these "binary (0-1) rewards" from the Lean
  prover (line 248). MCTS extrinsic reward is likewise R_extrinsic = 1 for completed proofs, 0 for
  unsolved (line 738).
- The paper frames the **compiler as a "world model"/"compiler oracle"** providing environmental
  supervision in an AlphaZero-like pipeline (lines 1375-1378). Verification is done via the Lean
  **REPL** enhanced with LeanDojo data-extraction tools (lines 337-338), on a cluster of thousands
  of CPU cores, each verification in a sandboxed process (lines 823-825).

**RL (RLPAF):** After SFT, applies **GRPO** (Shao et al., 2024) — Group Relative Policy
Optimization, no critic model, chosen over PPO. Reward supervision comes solely from Lean
verification results (0/1). ~4.5k filtered theorem statements as prompts; 32 candidate proofs per
theorem; KL penalty vs. reference (SFT) model (lines 352-383). Produces DeepSeek-Prover-V1.5-RL.

**MCTS + proof-assistant feedback (RMaxTS):** Standard MCTS (Coulom 2006; Browne et al. 2012) —
Selection, Expansion, Simulation, Backpropagation, with Simulation folded into Expansion because
whole-proof generation is itself a rollout (lines 669-673). Key pieces:
- **Truncate-and-resume** as a tactic-level state-action abstraction: parse generated proof into
  tactics, truncate at earliest verification error, insert successful tactics as tree nodes,
  resume generation from a chosen node with the Lean tactic state appended as a comment block
  (lines 530-665). Unlike game MCTS, one expansion can insert a whole *path* of nodes (lines 724-729).
- **RMaxTS** = RMax (Brafman & Tennenholtz 2002) applied to MCTS, an intrinsic-reward / reward-free
  exploration strategy to fight extreme reward sparsity. Intrinsic reward = indicator that at least
  one new node was added to the tree (Eq. 3, line 760); resembles ZeroRMax (Jin et al. 2020) — driven
  solely by intrinsic reward. Uses **Discounted UCB (DUCB)** (Garivier & Moulines 2011) with
  discount γ = 0.99 for non-stationary rewards, not standard UCB1 (lines 769-818).

**Training pipeline:** Pre-training (DeepSeek-Prover-V1.5-Base, extends DeepSeekMath-Base 7B on
Lean/Isabelle/Metamath corpora) -> SFT (thought-augmented CoT comments via DeepSeek-Coder V2 236B +
tactic-state insertion) -> RL (GRPO/RLPAF). Inference: single-pass sampling OR MCTS.

---

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| 63.5% | abstract (l.16), l.284, l.1040, l.1241 | miniF2F-test SOTA, RL + RMaxTS, 32×6400 mixture (non-CoT & CoT) strategy |
| 25.3% | abstract (l.16), l.288, l.1147 | ProofNet-test SOTA, RL + RMaxTS (also 25.3% "all") |
| 60.2% | l.283, l.911, l.987 | miniF2F-test, RL single-pass whole-proof generation (best single-pass) |
| 50.0% | l.283, l.912, l.945 | DeepSeek-Prover-**V1** miniF2F single-pass (baseline, 16×4096); V1.5 gain = **+10.2 pp** |
| 10.2 pp | l.283, l.912 | Absolute improvement of V1.5 (60.2%) over V1 (50.0%) on miniF2F single-pass |
| 21.6% / 23.7% | l.286-287, l.1113 | ProofNet single-pass RL: 21.6% validation, 23.7% test |
| 25.4% / 25.3% | l.288, l.1146 | ProofNet RL + RMaxTS: 25.4% validation, 25.3% test (4×6400) |
| 22.6% | l.920, l.1115 | ProofNet "all" single-pass RL |
| 51.6% | l.283-284 region, l.464, l.524, l.984 | miniF2F Pass@128, RL CoT (avg accuracy); best Pass@128 |
| 18.2% | l.467, l.524 | ProofNet Pass@128, RL CoT (avg accuracy) |
| 54.9% | l.917, l.985 | miniF2F, RL, 3200 whole-proof samplings |
| 54.5% | l.918, l.1016 | InternLM2-StepProver miniF2F (64×3200 tree searches) — prior SOTA V1.5 surpasses |
| 62.7% | l.915, l.1039, l.1164, l.1238 | miniF2F-test, RL + RMaxTS, 16×6400 (before mixture) |
| 21.7% | l.923-924 | ProofNet, V1.5 at 3200 whole-proof attempts; **+3.6%** over InternLM2-StepProver |
| 3.6% | l.924 | ProofNet improvement over prior SOTA (InternLM2-StepProver) at 3200 attempts |
| 13.8% | l.922, l.1127 | ReProver ProofNet-test (prior SOTA baseline) |
| 18.1% | l.922, l.1128 | InternLM2-StepProver ProofNet-test (prior SOTA baseline) |
| 7 billion parameters | l.1365 | DeepSeek-Prover-V1.5 model size |
| 7B (DeepSeekMath-Base) | l.1366-1367 | Base model DeepSeek-Prover-V1.5-Base extends DeepSeekMath-Base 7B |
| 244 + 244 | l.478 | miniF2F: 244 validation + 244 test problems |
| 185 + 186 | l.482 | ProofNet: 185 validation + 186 test problems |
| Lean 4.9.0 | l.479, l.485 | Both benchmarks manually converted from Lean 3 to Lean 4.9.0 |
| 9,645k sequences | l.316 | SFT proof dataset size |
| 9B tokens | l.349 | SFT training token count |
| 2,048 (batch) / 1e-4 (LR) | l.349 | SFT batch size / constant learning rate |
| 100 warm-up steps | l.350 | SFT training warm-up |
| 4,096 tokens | l.351 | SFT maximum context length |
| ~4.5k | l.361 | Unique theorem statements retained for RL after filtering |
| 5e-6 (LR) | l.381 | RL constant learning rate |
| 0.02 | l.381 | RL KL penalty coefficient |
| 32 candidates | l.382 | GRPO group size per theorem; max length 2,048 |
| 512 (batch) | l.383 | RL training batch size |
| γ = 0.99 | l.816 | DUCB discount factor (applied to tree-search iterations) |
| 300 seconds | l.501 | Lean verification time limit per proof |
| temp 1, top-p 0.95, 2048 tok | l.497-498 | Inference sampling parameters |
| A100-40G, vLLM | l.496 | Single-GPU deployment, vLLM framework (Kwon et al. 2023) |
| 256 runners / batch 512 | l.822 | Root parallelization: MCTS runners per node |
| 32 thread workers | l.829 | Tree parallelization per search tree |
| DeepSeek-Coder V2 236B | l.262, l.313, l.326 | Used to annotate NL chain-of-thought comments on Lean code |
| 29.7% ± 0.5% / 9.7% ± 0.7% | l.447-449, Fig.3 | Base (3-shot) Pass@128: miniF2F / ProofNet |
| 49.8% / 50.4% (miniF2F) | l.454-455 | SFT Pass@128 non-CoT / CoT |
| 15.9% / 15.9% (ProofNet) | l.457-458 | SFT Pass@128 non-CoT / CoT |
| 50.5% / 51.6% (miniF2F) | l.463-464 | RL Pass@128 non-CoT / CoT |
| 17.5% / 18.2% (ProofNet) | l.466-467 | RL Pass@128 non-CoT / CoT |
| 33.6% | l.937 | TheoremLlama miniF2F single-pass baseline (128) |

## Scope & Limitations (paper's own)

- Authors focus on the **exploration** aspect of RL (RMaxTS); the **exploitation** side — proof
  search per se — is left "unexplored." Future work: train a **critic model** to assess incomplete
  proofs / prune branches, doing temporal credit assignment (lines 1382-1388).
- Model already shows "some understanding of file-level context"; future work is multi-theorem,
  file-level real-world theorem proving (miniCTX; Hu et al. 2024) (lines 1389-1394).
- Benchmarks limited to miniF2F (high-school competition, algebra/number theory emphasis) and
  ProofNet (undergraduate: real/complex analysis, linear/abstract algebra, topology). Lean 4 only.

## Does NOT claim / boundaries

- Does NOT claim general mathematical discovery or novel-theorem generation — it proves *given*
  formal statements from fixed benchmarks.
- Does NOT rely on a learned/neural reward model for RL — reward is the **rigorous, exact Lean
  verifier** (0/1), explicitly contrasted (l.364-367) with typical trained reward models.
- Does NOT claim to close all problems: best miniF2F-test is 63.5%, ProofNet 25.3% — most ProofNet
  problems remain unsolved.
- Does NOT operate in natural language / informal proof space at evaluation — output is Lean 4 code
  checked by the compiler.
- The RMaxTS intrinsic reward is reward-**free** exploration (ZeroRMax-like); extrinsic reward only
  fires on full proof completion.

## Section Map

1. **Introduction** (1.1 Contributions; 1.2 Summary of Evaluations & Metrics) — l.86-289
2. **Model Training** — 2.1 Pre-training; 2.2 SFT (data curation, thought-augmented generation,
   prompt augmentation with tactic state, training setting); 2.3 RL from Proof Assistant Feedback
   (prompts, rewards, GRPO, training setting); 2.4 Evaluation (benchmarks, prompting, metric,
   training-stage & CoT vs non-CoT comparisons) — l.291-527
3. **Exploration-oriented MCTS** — 3.1 Tactic-level Tree Abstraction (truncate/resume); 3.2 MCTS
   (Selection/Expansion/Backpropagation); 3.3 Intrinsic Rewards (RMaxTS, DUCB); 3.4 Parallelization;
   3.5 Comparison with Existing Methods — l.529-867
4. **Experimental Results** — 4.1 Main Results (Tables 1-2); 4.2 Re-examining training strategies at
   large scale (Table 3, CoT/non-CoT/mixture); 4.3 Ablation on RMaxTS (Figure 5) — l.869-1362
5. **Conclusion, Limitation, and Future Work** — l.1364-1394
- References [1]-[62] — l.1396-1558
- Appendix A (non-CoT/CoT prompting examples); Appendix B (example miniF2F solutions) — l.1562-1854
