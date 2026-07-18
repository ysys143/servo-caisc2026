# DeepScientist: identity and architecture audit

## Audit boundary and source identity

- **Audited source:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/DeepScientist Advancing Frontier-Pushing Scientific Findings.pdf`
- **Title:** *DeepScientist: Advancing Frontier-Pushing Scientific Findings Progressively*.
- **Authors:** Yixuan Weng, Minjun Zhu, Qiujie Xie, Qiyao Sun, Zhen Lin, Sifan Liu, and Yue Zhang; Engineering School, Westlake University.
- **Version/date:** arXiv:2509.26603v1, 30 Sep 2025.
- **Extent:** 19 PDF pages. Pages 1-19 were read sequentially, including figures, tables, references, Appendix A, Appendix B, Appendix C, and the final generated-paper links.
- **SHA-256:** `76c3805b2344c32f3245f0500bcfd8ae129cd221f821da509817121c1485cae8`.
- **Manifest comparison:** exact match to `submission/analysis/citation_audit/core14-manifest.json` for path, hash, page count, and identity. No manuscript citation occurrence is assigned in the manifest.
- **Scope constraint:** Only this PDF and repository-local manifest context were used. No API/model call was made, and no other paper PDF was opened.

## 19-page complete structure and reading record

| PDF pages | Contents |
|---|---|
| 1 | Title, authors, abstract, project/code links, Figure 1, and headline claims: goal-oriented autonomous discovery, Bayesian Optimization, three-stage loop, Findings Memory, 20,000+ GPU hours, about 5,000 ideas, about 1,100 validated, and three SOTA-surpassing tasks. |
| 2 | Introduction: progressive goal-directed improvement of SOTA; shortcomings of undirected recombination; formal objective; three tasks; headline improvements; log analysis, human review, and low innovation success rate. |
| 3 | Related work on replication/optimization, semi-automated assistance, and automated discovery. Section 3.1 defines conceptual method space `I`, latent value function `f`, and expensive Bayesian Optimization. |
| 4 | Figure 2 and Section 3.2 opening. Human findings, papers/repositories, open knowledge, cumulative Findings Memory, and the hierarchical three-stage cycle; Strategize & Hypothesize begins. |
| 5 | Surrogate LLM scores utility/quality/exploration; UCB selection; sandboxed repository implementation with internet access; successful records become Progress Findings; analysis agents run deeper experiments and synthesize papers. Section 4 setup: three SOTA baselines, two 8-H800 servers, model assignments, and three human experts for verification/hallucination filtering. |
| 6 | Table 1, Figure 3, and task results for Agent Failure Attribution, LLM Inference Acceleration, and AI Text Detection, including A2P, ACRA, T-Detect/TDT/PA-Detect and reported metric improvements. |
| 7 | Tables 2-3 and paper-quality evaluation: DeepReviewer comparison with 28 public AI-Scientist papers; five generated papers reviewed by a three-person human program committee; AI-text-detection progression. |
| 8 | Figure 4 and trajectory analysis: idea/implementation/progress counts, success rates, execution-time distributions, embedding setup, parallel scaling setup, and causal analysis of 300 failed implementations. |
| 9 | Figures 5-6: t-SNE of 2,472 AI-text-detection ideas, T-Detect to TDT to PA-Detect trajectory, GPU scaling, shared-memory synchronization, and targeted versus naive GPU-hour comparison. |
| 10 | Scaling interpretation, discussion, conclusion, and start of Ethics Statement. Human-guided exploration and misuse red-teaming are discussed. |
| 11 | Ethics continuation: human verification, selective open-sourcing, withholding Analyze & Report, human accountability, acknowledgements, and start of references. |
| 12-14 | Remaining references, read as part of this PDF and not as separately opened source papers. |
| 15 | Appendix A: human review process/criteria and feedback. Three reviewers independently score confidence, soundness, presentation, contribution, and rating; an Area Chair-style reviewer makes the study decision. Feedback praises ideation but identifies weak empirical rigor. |
| 16 | Appendix B: verification bottleneck, below-3% progress success framing, and three future strategies: hypothesis quality, filtering, and implementation quality. |
| 17 | Appendix B continuation and Appendix C implementation details: theory constraints, Findings Memory, surrogate/acquisition improvements, Docker separation, port API, baseline duplication, CLI re-execution, human inspection, and fixed `K=15`, `wu=1`, `wq=1`, `kappa=1`. |
| 18 | Cost details: about $5 per idea, $20 plus one GPU hour per implementation attempt, $150 per successful analysis/report path, about $100,000 total; three generated-paper callouts. |
| 19 | Appendix C.1 Generated Papers: three arXiv PDF links. Links were recorded but not opened under the single-PDF boundary. |

## Problem statement and context

The paper treats scientific progress as repeated, goal-directed improvement of an existing frontier rather than arbitrary generation. It argues that previous AI Scientist systems can produce novel artifacts but often lack a human-defined challenge and therefore generate recombinations with insufficient scientific value (PDF pp. 1-3). DeepScientist starts from a recognized limitation of a human SOTA method, generates candidate methods, tests them, and uses successful findings to define further limitations and search directions.

Section 3.1 models discovery as Bayesian Optimization over an implicit conceptual method space `I`, with an expensive latent scientific-value function `f(I)` (PDF pp. 3-4). The paper explicitly says conventional Bayesian Optimization does not solve creative hypothesis generation because `I` is not explicitly defined. Its proposed answer is a multi-agent system with surrogate LLM valuation, UCB acquisition, hierarchical fidelity levels, and cumulative memory.

The empirical context is computational machine-learning research, not wet-lab science. The starting methods are All at Once for Agent Failure Attribution, TokenRecycling for LLM Inference Acceleration, and Fast-DetectGPT for AI Text Detection (PDF p. 5, Table 1). The paper reports two servers with eight H800 GPUs each and three human experts supervising output verification and hallucination filtering (PDF p. 5). This is distinct from the later paper-quality evaluation by three LLM researchers and an Area Chair-style decision process (PDF pp. 7, 15).

## Architecture and method

1. **Findings Memory and open knowledge.** The memory is a list-style database of structured records categorized as Idea, Implement, or Progress Findings. It contains papers/code and the system's historical findings; a retrieval model selects Top-K findings when context length requires it (PDF pp. 4-5).
2. **Strategize & Hypothesize.** The system analyzes the memory, identifies limitations, and generates hypotheses. A low-cost LLM Reviewer surrogate assigns utility `vu`, quality `vq`, and exploration `ve` scores from 0 to 100 (PDF pp. 4-5).
3. **Implement & Verify.** UCB combines valuation fields into exploitation and exploration scores, selects a finding, and promotes it to Implement Finding. A coding agent plans and edits an existing SOTA repository in a sandbox with full permissions and internet access, runs experiments, and stores logs/results. A successful baseline-surpassing result is promoted (PDF p. 5).
4. **Analyze & Report.** Specialized agents use MCP tools for ablations, new datasets, parsing, and lifecycle management. A synthesis agent aggregates results and artifacts into a reproducible paper, and the Progress Finding influences later cycles (PDF p. 5).
5. **Iteration and scaling.** Parallel GPU instances share a central memory and synchronize periodically. The paper reports one to eleven progress findings from four to sixteen GPUs in a one-week scaling setup. The AI-text-detection case is presented as progressive T-Detect to TDT to PA-Detect improvement (PDF pp. 6-10).
6. **Implementation controls.** Appendix C separates core logic and coding into Docker containers communicating through a port API. A verified baseline is duplicated into a sandbox; after Claude Code reports completion, the main script is independently re-executed via CLI because about half of initial attempts reportedly failed due to timeouts. Human supervisors manually inspected experimental results (PDF p. 17).

## Frozen supplementary description

Frozen text from `submission/analysis/citation_audit/core14-manifest.json`:

> A system that searches for methods exceeding a target state-of-the-art, formalized as Bayesian optimization over a value function. A surrogate LLM reviewer scores candidate ideas; a coding agent implements them in a sandbox with internet access on top of existing repositories, promoting a candidate only when it beats the baseline. A UCB acquisition function balances exploitation and exploration; a findings memory accumulates unverified, implemented, and SOTA-exceeding results. Across three computational domains it reported exceeding human SOTA; three human experts performed final verification and hallucination filtering.

## Clause-level cross-check

| Frozen clause | Verdict | PDF-grounded assessment |
|---|---|---|
| “searches for methods exceeding a target state-of-the-art” | **Supported** | The objective and three starting SOTA methods are explicit (PDF pp. 2, 5-6). This evidence is limited to the three reported tasks, not universal SOTA superiority. |
| “formalized as Bayesian optimization over a value function” | **Supported, with qualification** | Section 3.1 defines latent black-box `f` over conceptual `I` and motivates BO for costly evaluations (PDF pp. 3-4). The implementation is an LLM-score/UCB heuristic, not an explicitly calibrated conventional posterior surrogate (PDF pp. 4-5). |
| “A surrogate LLM reviewer scores candidate ideas” | **Supported** | The reviewer assigns utility, quality, and exploration scores from 0 to 100 and stores them in Idea Finding records (PDF p. 5). |
| “a coding agent implements them in a sandbox with internet access on top of existing repositories” | **Supported** | Repository-level implementation, sandbox/full permissions, internet access, Docker separation, baseline duplication, and CLI re-execution are stated (PDF pp. 5, 17). |
| “promoting a candidate only when it beats the baseline” | **Supported for the stated promotion rule** | An Implement Finding becomes a Progress Finding only after successful validation surpasses the baseline (PDF p. 5). This is a control-flow criterion, not proof of independent replication of every improvement. |
| “A UCB acquisition function balances exploitation and exploration” | **Supported** | Equation (2) combines utility/quality exploitation with exploration value and `kappa`; Appendix C fixes `wu=1`, `wq=1`, `kappa=1` (PDF pp. 5, 17). |
| “a findings memory accumulates unverified, implemented, and SOTA-exceeding results” | **Supported, slightly compressed** | The paper defines Idea, Implement, and Progress Findings and retains them for later cycles (PDF pp. 4-5). Records include hypotheses and metadata as well as measured results. |
| “Across three computational domains it reported exceeding human SOTA” | **Supported, but name the domains** | The domains/tasks are Agent Failure Attribution, LLM Inference Acceleration, and AI Text Detection; Table 1 and Figure 3 report improvements for each (PDF pp. 5-6). |
| “three human experts performed final verification and hallucination filtering” | **Supported, but distinguish from paper review** | Section 4 and Appendix C state three human experts/supervisors verified outputs, filtered hallucinations, and manually inspected results (PDF pp. 5, 17). Separately, Appendix A describes three LLM researchers reviewing five generated papers (PDF pp. 7, 15). |

## Verdict and corrected description

**Overall verdict: `minor_revision`.** The frozen description is substantively faithful. Precision should be improved by naming the three computational tasks, distinguishing the conceptual Bayesian Optimization framing from the implemented LLM-score/UCB heuristic, and distinguishing operational verification experts from the separate manuscript-quality committee. It should also expose that Findings Memory is an external record/database architecture and that successful records feed later cycles.

Suggested corrected description:

> DeepScientist is a goal-oriented LLM multi-agent system that searches for methods surpassing a target SOTA, framing discovery as Bayesian Optimization over an expensive latent value function. A surrogate LLM Reviewer scores hypotheses for utility, quality, and exploration; UCB selects candidates for repository-level implementation in a sandbox with internet access, promoting them to Progress Findings only after they surpass the baseline. A cumulative Findings Memory retains idea, implementation, and progress records and informs later cycles, while Analyze & Report agents run deeper analyses and synthesize papers. In three computational tasks - Agent Failure Attribution, LLM Inference Acceleration, and AI Text Detection - the paper reports SOTA-surpassing results. Three human experts supervised verification and hallucination filtering; a separate three-reviewer committee assessed the generated papers.

## Evidence completion

- [x] PDF identity, SHA-256, and 19-page extent fixed against the repository manifest.
- [x] Pages 1-19 read sequentially, including figures, tables, references, appendices, and the final links page.
- [x] Problem statement, context, architecture, methods, evaluation, implementation details, ethics, bottlenecks, and conclusion recorded.
- [x] Every clause of the frozen supplementary description assessed against enclosing PDF pages.
- [x] No API/model call made; no other paper PDF opened.

EVIDENCE_COMPLETE: yes
