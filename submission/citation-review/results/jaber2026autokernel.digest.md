# Digest: jaber2026autokernel

**Title:** AutoKernel: Autonomous GPU Kernel Optimization via Iterative Agent-Driven Search
**Authors:** Jaber Jaber, Osama Jaber (RightNow AI)
**Venue/ID:** arXiv:2603.21331v1 [cs.LG], 22 Mar 2026 (11 pages)
**Code:** https://github.com/RightNow-AI/autokernel

> NOTE (read blind): Header footer reads "37th Conference on Neural Information Processing Systems (NeurIPS 2023)" while the arXiv stamp is 22 Mar 2026 — an obvious NeurIPS style-template leftover, not a real 2023 venue. Both authors share the surname Jaber.

---

## Thesis / Problem

Writing high-performance GPU kernels is labor-intensive expert work (a single tensor-core matmul may need weeks of tuning). Vendor libraries (cuBLAS, cuDNN) lag behind architectural innovation (grouped-query attention, SwiGLU, RoPE, RMSNorm shipped before library support). The paper's premise: the workflow of an expert kernel engineer is *itself a simple loop* — write a candidate, benchmark it, keep improvements, discard regressions, repeat — and this loop can be mechanized with an autonomous LLM agent. AutoKernel operates on **complete PyTorch models**: profile → rank bottlenecks by Amdahl's law → iteratively refine Triton/CUDA C++ kernels over hundreds of experiments with no human intervention.

## Method — Empirical/benchmark validation + iterative agent-driven search? **YES to both.**

- **Iterative agent-driven search (YES):** Algorithm 1 is an explicit keep/revert hill-climbing loop. Each iteration: LLM agent edits ONE kernel file (`A.edit(kbest, history, roofline)`), git-commits, runs benchmark; keep if `pass AND t' > 1.01·tbest`, else `git reset --hard HEAD~1`. ~40 iter/hour, 300–400 experiments per overnight (10-hour) run. This is a *simple greedy loop* driven by an LLM agent — deliberately NOT multi-agent, NOT RL, NOT evolutionary (contrasted against those in Related Work / Table 1).
- **Reliable empirical/benchmark validation (YES):** The evaluation function is a **correctness-gated performance benchmark, not validation loss.** A fixed 5-stage correctness harness (smoke → shape sweep → numerical stability → determinism → edge cases) must pass BEFORE any speedup is recorded; throughput is then measured empirically via Triton `do_bench` and CUDA event timing (200 iters/config, trimmed mean dropping top/bottom 10%). Key design firewall: "Fixed evaluation, mutable code" — the agent never modifies the benchmark, preventing eval-gaming.
- Explicitly transplants Karpathy's autoresearch keep/revert paradigm from LLM-training code to kernel code: search space = possible kernel implementations, evaluation = correctness-gated benchmark.

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| 60–80% of total GPU time | §1 (L41-42) | Matmuls in attention/FFN consume this share |
| >9,000 / 9,200+ lines Python | Abstract, §1 contrib, §3 | System size (9,200 across 14 core scripts) |
| 909-line agent instruction doc (program.md) | Abstract, §3, §3.3 | Agent instructions / six-tier playbook |
| 18 starter kernels (9 Triton + 9 CUDA C++) | Abstract, §1, §3, §5 | Dual-backend starter set |
| 250 standardized problems | Abstract, §1, §8 | KernelBench suite size |
| 9 kernel types | Abstract, §1, §6 | Coverage of transformer ops |
| 5.29× over eager (RMSNorm) | Abstract, §7.1, Table 4 | H100 Triton, at 8192² (largest size) |
| 2.82× over eager (softmax) | Abstract, Table 4 | H100, at 8192² |
| 2.21× over eager (cross-entropy) | Abstract, Table 4 | H100, at 8192×32k |
| 2.83× / 3.44× / 2.94× vs torch.compile | Abstract, Table 4 | RMSNorm / softmax / cross-ent respectively |
| 1st place vectorsum_v2 B200 leaderboard | Abstract, §7.2 | Community deployment; latency 44.086µs |
| 44.086 / 44.249 / 46.553 µs | §7.2 | 1st (AutoKernel) / 2nd / 3rd place latencies |
| FP4 matmul 1.63× to 2.15× over CUTLASS | Abstract, §7.2, Table 5 | Community-reported, single prompt (~3 min) |
| up to 2,898 TFLOPS | §7.2, Table 5 | FP4 Triton at 2048×18432×3072 |
| <20% of cases matched PyTorch baseline | §1 (L60-62) | KernelBench (Ouyang 2025) one-shot frontier LLM result |
| ~90 seconds per iteration (30s+30s+30s) | Abstract, §3.3 | correctness / perf bench / agent reasoning |
| 300–400 experiments / overnight (10-hr) run | Abstract, §1, §3.3 | at 40 experiments/hour |
| 20 optimizations, 700 experiments, 2 days, 1 GPU | §1 (L72), §2.4 | Karpathy autoresearch (630-line training script, 5-min eval) |
| 1.5× on 60% kernel → 1.25× end-to-end | §1 (L78-79) | Amdahl illustration |
| 1.5× on 5% kernel → 1.03× end-to-end | §1 (L79) | Amdahl illustration |
| FP16 matmul <25 lines matching cuBLAS | §2.1 | Triton (Tillet 2019) claim |
| 2.27× inference / 1.41× training, 180+ models | §2.1 (L187-188) | TorchInductor (Ansel 2024) |
| 1–5 s compilation | §2.1, §5 | Triton JIT |
| 2–4× wallclock speedup | §2.2 | FlashAttention (Dao 2022) |
| 50–73% theoretical peak on A100 | §2.2 | FlashAttention-2 (Dao 2023) |
| 840 TFLOPS on H100 (85% util) | §2.2 | FlashAttention-3 (Shah 2024), TMA/WGMMA/FP8 |
| 2.3× average speedup (SYCL) | §2.3 | KernelFoundry (Wiedemann 2026), MAP-Elites QD |
| 3.12× average speedup, ICLR 2026 accept | §2.3 | CUDA-L1 (Li 2026), SFT + contrastive RL |
| 100% faster-than-torch.compile (L1,L2), 92% (L3) | §2.3 | CUDA Agent (Dai 2026), large-scale agentic RL |
| 1.32× average speedup | §2.3 | Astra (Wei 2025), multi-agent |
| 5.44× on Level 1 | §2.3 | KernelSkill (Sun 2026), dual-level memory |
| profile.py = 1,125 lines; 5 warmup / 10 profiled | §3.1 | torch.profiler with shape recording |
| extract.py = 648 lines | §3.2 | Kernel extractor |
| orchestrate.py = 842 lines | §3.4 | Amdahl (1967) orchestrator |
| bench.py = 1,416 lines | §4 | 5-stage correctness harness |
| t' > 1.01·tbest keep threshold | Algorithm 1 (L313) | 1% improvement gate |
| Move-on: 5 reverts / 90% peak / 2 hr / 2× speedup | §3.4 (L454-456), §7.3 | Orchestrator transition criteria |
| Smoke test 128×128, <1 s | §4 Stage 1 | Catches compile/shape/gross bugs |
| Shape sweep 8–10 configs × 3 dtypes | §4 Stage 2 | FP16, BF16, FP32 |
| Tolerances FP16 1e-2 / BF16 2e-2 / FP32 1e-4 | §4 (L476) | dtype-specific atol |
| Non-power-of-2 dims 1023, 4097, 1537 | §4 Stage 5 | Edge-case masking bugs |
| 4 model defs: GPT-2 124M, LLaMA 160M/7B, BERT-base 110M, custom | §6 | Ship self-contained, no transformers dep |
| H100 80GB HBM3, 132 SMs, CC 9.0, CUDA 12.8 | §7 | Eval hardware |
| 200 iters/config, trimmed mean (drop top/bottom 10%) | §7 | Timing methodology, CUDA events |
| 7 kernel types, 34 configs, <10 min wall-clock | §7 | Full eval; all 34 pass, zero failures |
| 2,788 GB/s = 83% of H100 3,352 GB/s peak | §7.1 | RMSNorm at 8192² |
| Cross-entropy 2,070 GB/s; softmax 2,800 GB/s | §7.1 | Memory-bound peaks |
| Beat torch.compile on 12 of 16 configs (Table 4) | §7.1 | Not all — matmul lags |
| Matmul Triton starter 278 TFLOPS = 28% of 989.5 TFLOPS peak | §7.1, §7.3 | Well below cuBLAS; matmul "remains hard" |
| Matmul beats torch.compile 1.55× at 2048³ | §7.1, Table 4 | But 0.43× vs eager (loses to cuBLAS) |
| cuBLAS 800+ TFLOPS | §7.3 | Matmul reference ceiling |
| RMSNorm tiers: 10–30% (T1), 10–20% (T2), 5–10% (T3), plateau 30–50 exp | §7.3 | Loop dynamics example |
| Model example: matmul 62% / RMSNorm 5% of GPU time | §7.3 | Amdahl prioritization |
| bridge.py 674 / bench_kb.py 726 / scorer.py 351 lines | §8 | KernelBench integration components |
| fast_p at 7 thresholds 1.0×–5.0× | §8 | Batch scorer metric |
| 50–300 iterative experiments per KernelBench problem | §8 | vs typical one-shot scoring |
| export_hf.py = 868 lines | §9 | HuggingFace Kernels (HuggingFace 2025) export |

### Table 4 raw (H100 FP16, µs; Ours-vs-Eager / vs-Compiled; Throughput)
- matmul 2048³: 28.1 / 101.2 / 65.3 → 0.43× / 1.55× → 263 TF/s
- matmul 4096³: 182.8 / 257.8 / 494.2 → 0.37× / 0.52× → 278 TF/s
- matmul 8192³: 1679.5 / 1916.1 / 5773.1 → 0.29× / 0.33× → 190 TF/s
- softmax 4096²: 58.9 / 96.1 / 40.1 → 1.47× / 2.40× → 1675 GB/s
- softmax 8192²: 270.4 / 330.0 / 95.9 → 2.82× / 3.44× → 2800 GB/s
- layernorm 4096×5120: 45.6 / 105.5 / 42.5 → 1.07× / 2.48× → 1974 GB/s
- layernorm 8192×4096: 64.7 / 166.8 / 51.9 → 1.25× / 3.21× → 2586 GB/s
- rmsnorm 4096²: 142.8 / 99.9 / 39.1 → 3.65× / 2.56× → 1716 GB/s
- rmsnorm 8192×4096: 262.4 / 138.1 / 51.2 → 5.12× / 2.70× → 2619 GB/s
- rmsnorm 8192²: 509.6 / 272.1 / 96.3 → 5.29× / 2.83× → 2788 GB/s
- cross_ent 4096×32k: 295.6 / 386.3 / 134.9 → 2.19× / 2.86× → 1943 GB/s
- cross_ent 8192×32k: 559.7 / 745.1 / 253.3 → 2.21× / 2.94× → 2070 GB/s
- reduce 8192²: 60.7 / 185.2 / 62.2 → 0.98× / 2.98× → 2156 GB/s
- reduce 16384×4096: 50.4 / 185.9 / 52.8 → 0.95× / 3.52× → 2542 GB/s
- rotary 2×32×2k×128: 211.4 / 106.9 / 117.4 → 1.80× / 0.91× → 576 GB/s
- rotary 2×32×4k×128: 394.9 / 136.0 / 223.0 → 1.77× / 0.61× → 607 GB/s

### Table 5 raw (FP4 matmul, community-reported, H100; Triton vs CUTLASS)
- 128×3072×3072: 186 vs 100 TF → 1.86×
- 128×18432×3072: 1105 vs 550 TF → 2.01×
- 1024×3072×3072: 1477 vs 686 TF → 2.15×
- 1024×18432×3072: 2777 vs 1609 TF → 1.73×
- 2048×3072×3072: 1662 vs 964 TF → 1.72×
- 2048×18432×3072: 2898 vs 1777 TF → 1.63×
- 4096×3072×3072: 2443 vs 1405 TF → 1.74×

## Scope & Limitations (author-stated)

- Inherits code-generation ceiling of the underlying LLM; complex techniques (software pipelining, custom PTX emission, multi-CTA cooperative strategies) "may exceed current agent abilities" (ceiling rises as frontier models improve).
- Currently optimizes **individual kernels on a single GPU**; distributed kernels and multi-device memory management are **out of scope**.
- Future work: population-based search across GPU instances; learned search policies on historical experiment data; SASS/throughput-counter-guided mutations; cross-kernel fusion discovery.

## Does NOT claim / boundaries (important for citation accuracy)

- Does **NOT** claim to beat cuBLAS on matmul — explicitly: "Matmul remains hard," Triton starter = 278 TFLOPS (28% peak), loses to eager cuBLAS (0.29–0.43×). Matmul improvement is stated as the *target* for the agent loop, not a solved result.
- Does **NOT** use multi-agent, RL, evolutionary, or learned-policy architecture — deliberately a single agent in a tight keep/revert loop ("simplicity over sophistication").
- Community results (B200 vectorsum leaderboard win; FP4 vs CUTLASS) are **community-reported / user-reported**, NOT the authors' own controlled measurement. Table 5 FP4 is explicitly "A community user reported... single agent prompt (~3 min)."
- The headline Table 4 speedups (5.29× etc.) are the authors' own H100 measurements of the **starter kernels** (before the iterative loop), reported at the largest tested size; §7.3 describes the loop dynamics separately but reports no post-loop end-state speedup numbers for these kernels.
- The agent optimizes but does **not** modify the benchmark (fixed-eval firewall).
- Not a benchmark paper on KernelBench itself; it *integrates with* KernelBench and notes it runs 50–300 iterative experiments per problem vs the typical one-shot scoring (no aggregate KernelBench score reported).

## Section map

- §1 Introduction (Can LLMs write GPU kernels?; Our approach; Key insight; Contributions ×6)
- §2 Related Work — 2.1 GPU Kernel Languages/Compilers; 2.2 Optimized Kernel Libraries; 2.3 LLM-based Kernel Generation (Table 1 comparison); 2.4 Autonomous Research Agents
- §3 System Design — 3.1 Model Profiling (Phase A); 3.2 Kernel Extraction; 3.3 Agent Optimization Loop (Phase B, Algorithm 1); 3.4 Multi-Kernel Orchestration (Amdahl Eq. 1)
- §4 Five-Stage Correctness Verification (Figure 2, Table 2 matmul shape sweep)
- §5 Dual Backend: Triton and CUDA C++
- §6 Kernel Coverage (Table 3 nine kernel types)
- §7 Experimental Evaluation — 7.1 Kernel Performance (Table 4); 7.2 Community Deployment Results (Table 5); 7.3 Optimization Loop Dynamics
- §8 KernelBench Integration
- §9 HuggingFace Kernels Export
- §10 Design Rationale (simplicity; fixed-eval firewall; git tracking; roofline-guided; TSV logging)
- §11 Limitations and Future Work
- §12 Conclusion
- References (Amdahl 1967, Andrews & Witteveen 2025, Ansel 2024, Dai 2026, Dao 2022, Dao 2023, HuggingFace 2025, Karpathy 2026, Li 2026, NVIDIA 2024, Ouyang 2025, Shah 2024, Sun 2026, Thakkar 2023, Tillet 2019, Wang 2025, Wei 2025, Wiedemann 2026, Williams 2009, Zhang 2025)
