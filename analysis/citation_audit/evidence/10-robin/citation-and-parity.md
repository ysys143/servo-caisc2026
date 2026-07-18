# Robin: citation inventory and English/Korean parity audit

## Audit scope and source control

- **Single audited source:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/Robin - A Multi-Agent System for Automating Scientific Discovery.pdf`.
- **Source identity:** title `Robin: A multi-agent system for automating scientific discovery`; arXiv `2505.13400v1`, dated 19 May 2025; 30 pages. The local SHA-256 is `336d4e3f9065f42918cec8053e020d12c8d8c8031eb4c180764a349d1efa1794`, matching `core14-manifest.json`.
- I read the PDF sequentially from pages 1-30, including the main text, references, methods, prompts, and supplementary figures/captions. Page images were also checked for the architecture/workflow and result figures (especially pp. 1, 3-7, 25, 28, and 30).
- No other PDF was opened. No API or model call was used.

## Citation inventory and manuscript occurrence

| Inventory item | Evidence | Verdict |
|---|---|---|
| BibTeX key | `submission/references.bib` contains `ghareeb2026robin`, titled *A multi-agent system for automating scientific discovery*, Nature 2026, DOI `10.1038/s41586-026-10652-y`, note `arXiv:2505.13400`. | **Present** |
| Core catalog entry | `submission/analysis/citation_audit/core14-manifest.json` index 10 identifies Robin, the exact PDF path/hash/page count, and the frozen supplementary description. | **Present; catalog-only** |
| English manuscript occurrence | No occurrence of `ghareeb2026robin`, Robin, or the Korean name was found in `submission/main.tex` or the generated English manuscript text. | **Absent** |
| Korean manuscript occurrence | No Robin/`ghareeb2026robin` occurrence was found in `submission/main_ko.tex` or the generated Korean manuscript text. | **Absent** |
| Link IDs | The catalog entry has `manuscript_link_ids: []`. | **No linked occurrence** |

**Citation-layer conclusion:** this is not a cited manuscript claim. It is a catalog/frozen-description audit. Therefore there is no English citation occurrence to pair with a Korean occurrence; parity is **`omitted` / catalog-only in both manuscript languages**, rather than `equivalent` or `meaning_shifted`.

## Frozen description, sentence-by-sentence evidence

Frozen text from `core14-manifest.json` (duplicated in `analysis/multicoder/systems_desc.json`):

> A system for biomedical therapeutic discovery (dry age-related macular degeneration). Cooperating agents perform literature search and deep evaluation, rank candidates via an LLM tournament, and design assays. Physical experiments (phagocytosis assays, RNA-seq sequencing and alignment) are performed by humans, while a bioinformatics agent autonomously analyzes flow-cytometry and differential-expression data and meta-analyzes multiple trajectories. Measured outcomes (e.g., phagocytosis improvement, gene upregulation with reported p-values) feed the next round; the full manuscript was system-generated and underwent peer review.

| Frozen sentence/clause | PDF evidence | Assessment |
|---|---|---|
| “A system for biomedical therapeutic discovery (dry age-related macular degeneration).” | The abstract and Introduction frame Robin as a multi-agent scientific-discovery system applied to therapeutics and dAMD (pp. 1-2). The Results explicitly focus on dAMD (pp. 2-7). | **Supported, but scope-limited.** The PDF demonstrates a dAMD therapeutic case study, not biomedical therapeutic discovery in general. The Discussion reports additional disease candidate lists, but not additional wet-lab therapeutic discoveries (p. 7; Supplementary Figs. S16-S25, pp. 29-30). |
| “Cooperating agents perform literature search and deep evaluation, rank candidates via an LLM tournament, and design assays.” | Crow performs concise literature reviews; Falcon performs deep reviews; Finch analyzes experimental data (pp. 2-3, Fig. 1). Robin generates assays and candidate hypotheses, and an LLM judge performs pairwise comparisons/ranking (pp. 3-4; Supplementary Fig. S11, p. 25). The paper says the ranked list can then be reviewed by human scientists (p. 4). | **Supported with a qualification.** “LLM tournament” is a reasonable compression of pairwise LLM-judge ranking, but “cooperating agents” should not imply that all agents independently execute the whole workflow. Assay execution is outside the agents and is conducted by researchers (pp. 2, 5). |
| “Physical experiments (phagocytosis assays, RNA-seq sequencing and alignment) are performed by humans” | The workflow states that researchers conduct experiments and provide resulting data to Robin (p. 2). The phagocytosis experiments and RNA-seq experiment are described as laboratory work with human analysis/handling in the Results and Methods (pp. 4-6, 8-11). Supplementary Figs. S13-S15 explicitly label the human analyses, including flow gating and RNA-seq analysis (pp. 26-28). | **Supported.** “RNA-seq sequencing and alignment” is accurate for the reported experiment and processing, though the broader experimental design and analysis pipeline includes both human and Finch-produced components. |
| “a bioinformatics agent autonomously analyzes flow-cytometry and differential-expression data” | Finch is described as performing autonomous analyses of experimental data (pp. 2-3, Fig. 1C). The paper gives Finch flow-cytometry gating/analysis and RNA-seq differential-expression/GO outputs (pp. 4-6, Figs. 2-3). | **Supported, with bounded autonomy.** The paper itself says Finch is reliant on prompt engineering by domain experts and that adapting it to independent modalities is future work (p. 7). “Autonomously” is valid for the stated analysis calls, but not for an unrestricted end-to-end bioinformatics pipeline. |
| “and meta-analyzes multiple trajectories.” | The Results state that Finch produces consensus findings from eight RNA-seq analysis trajectories, including the same genes consistently up- or down-regulated (p. 6, Fig. 3C). | **Supported.** The frozen wording should ideally specify that this is a consensus/meta-analysis of eight trajectories in the reported RNA-seq example, rather than a general capability established across all analyses. |
| “Measured outcomes (e.g., phagocytosis improvement, gene upregulation with reported p-values) feed the next round” | Robin uses experimental results to interpret outcomes and generate updated hypotheses (pp. 2-3, Fig. 1). Y-27632 phagocytosis results lead to a follow-up RNA-seq proposal; the reported ABCA1 result is a 3-fold upregulation with adjusted `p=2.13×10^-83` (p. 6). Round-2 phagocytosis results support the ripasudil candidate (pp. 6-7). | **Supported for the demonstrated dAMD loop.** “Feed the next round” is directly evidenced for the RNA-seq follow-up and candidate iteration, but it should not be generalized to every output or imply that the physical experiment loop is autonomous: scientists perform/provide the experiments (pp. 2, 5). |
| “the full manuscript was system-generated” | The abstract says that all hypotheses, experimental plans, data analyses, and data figures in the main text were produced by Robin (p. 1). The Methods and Supplementary Material contain human-provided experimental procedures, prompts, and analyses; Supplementary Figs. S13-S15 are explicitly human analyses (pp. 8-11, 26-28). | **Overstated / major revision required.** The PDF supports that the main-text scientific content listed in the abstract was produced by Robin, but not the unqualified claim that the *full manuscript* was system-generated. The frozen wording should preserve the abstract’s narrower scope and distinguish system-generated content from human experimental work, methods, and explicitly human analyses. |
| “and underwent peer review.” | The audited PDF contains the manuscript and its supplementary material, but the 30 pages read here do not state that the manuscript underwent peer review. The source identifies the work as arXiv `v1` dated 19 May 2025 (p. 1). | **Unsupported by this source.** This clause must be removed or separately sourced; it cannot be treated as entailed by the Robin PDF. |

## Citation range and overclaim assessment

1. **No manuscript citation entailment exists:** because `ghareeb2026robin` has no English or Korean occurrence, the frozen description must not be presented as a citation-backed claim in the paper. The BibTeX entry alone does not create a citation occurrence.
2. **Main overclaim:** “the full manuscript was system-generated” expands the PDF abstract’s enumerated claim (“all hypotheses, experimental plans, data analyses, and data figures in the main text”) into a broader authorship claim. The source also documents human analysis and human experimental execution (pp. 2, 6, 8-11, 26-28).
3. **Unsupported provenance claim:** “underwent peer review” is not stated in the audited PDF. It is outside the allowed evidence set for this audit.
4. **Autonomy boundary:** the system is repeatedly characterized as semi-autonomous and lab-in-the-loop, with researchers conducting experiments and supplying data (pp. 1-3). Any description that turns the loop into autonomous physical experimentation would be incorrect.
5. **Result boundary:** the PDF reports a promising ripasudil result in an in-vitro RPE phagocytosis assay and a mechanistic RNA-seq signal; it also says further testing at different doses and longer incubation times is necessary for definitive comparison (p. 7). The frozen description should not imply clinical validation or a completed therapeutic discovery.

## English/Korean parity

| Layer | English | Korean | Parity verdict |
|---|---|---|---|
| Bibliography occurrence | No `ghareeb2026robin` occurrence | No `ghareeb2026robin` occurrence | `omitted` in both |
| Catalog/frozen description | Present in `core14-manifest.json` and `systems_desc.json` | No Korean catalog/frozen-description counterpart | `catalog-only`; no translation counterpart |
| Sentence-level claim parity | Not applicable to manuscript occurrences | Not applicable to manuscript occurrences | No `equivalent` pair exists |

There is therefore no Korean translation that could silently strengthen, weaken, or shift the Robin claim. The material audit issue is source scope, not bilingual divergence.

## Recommended disposition

**Frozen-description verdict: `major_revision`.** Keep the core system identity, the dAMD case, the literature-search/LLM-judge/Finch workflow, the human laboratory boundary, the eight-trajectory RNA-seq consensus, and the demonstrated outcome-to-follow-up loop. Remove the unsupported peer-review clause and narrow the manuscript-generation clause.

Evidence-preserving replacement:

> A semi-autonomous, lab-in-the-loop multi-agent system for biomedical therapeutic discovery, demonstrated on dry age-related macular degeneration. Crow and Falcon conduct concise and deep literature review, respectively, while an LLM judge ranks candidate hypotheses and Robin proposes assays and therapeutic candidates. Human researchers perform the phagocytosis and RNA-seq experiments and provide the resulting data; Finch autonomously analyzes flow-cytometry and differential-expression data, including a consensus analysis across eight RNA-seq trajectories. In the demonstrated loop, measured phagocytosis outcomes and an ABCA1 differential-expression signal informed subsequent candidate generation and follow-up analysis. The PDF states that Robin produced the main-text hypotheses, experimental plans, data analyses, and data figures, while laboratory execution and some analyses remained human-performed.

`EVIDENCE_COMPLETE: yes`
