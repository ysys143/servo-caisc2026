# Robin: identity and architecture evidence

## Audit boundary and reading record

- **Single source read:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/Robin - A Multi-Agent System for Automating Scientific Discovery.pdf`.
- **Source identity:** title page identifies the work as *Robin: A Multi-Agent System for Automating Scientific Discovery*, by Ali Essam Ghareeb, Benjamin Chang, Ludovico Mitchener, Angela Yiu, Caralyn J. Szostkiewicz, Jon M. Laurent, Muhammed T. Razzak, Andrew D. White, Michaela M. Hinks, and Samuel G. Rodriques. The PDF is arXiv:2505.13400v1, dated 19 May 2025 (p. 1).
- **Integrity:** PDF metadata reports 30 pages; SHA-256 is `336d4e3f9065f42918cec8053e020d12c8d8c8031eb4c180764a349d1efa1794`, matching the frozen manifest. No other PDF was opened and no API/model call was made.
- **Full sequential coverage:** pp. 1-2 abstract/introduction and motivation; pp. 3-7 system, experiments, results, discussion; pp. 8-11 implementation and wet-lab/data-analysis methods; pp. 12-14 references; p. 15 end of references and start of supplementary material; pp. 16-23 prompts used by the system; pp. 24-27 supplementary judge/flow-cytometry/RNA-seq figures; pp. 28-30 additional disease candidate lists (S16-S25). Figures, tables, prompts, references, and supplementary figures were included in the read.

## Identity and problem framing

Robin is presented as a multi-agent system for a continuous, lab-in-the-loop therapeutic-discovery workflow. Its motivating problem is the delay in connecting dispersed biomedical knowledge to new therapeutic uses, especially drug repurposing (pp. 1-2). The paper positions prior systems as automating narrower tasks, while claiming that Robin combines hypothesis generation, experimental strategy generation, experimental-data analysis, and hypothesis refinement in one workflow (p. 2).

The concrete demonstration targets dry age-related macular degeneration (dAMD). Given only a disease name, Robin reviews literature, proposes disease mechanisms and assays, proposes drug candidates, and ranks them; scientists then perform the selected physical experiments and upload data for analysis (pp. 2-4). The paper therefore uses **semi-autonomous** and **lab-in-the-loop** language, despite also using broad “fully automating key intellectual steps” framing in the abstract (pp. 1-2).

## Architecture and method

### Agent roles and control flow

1. **Input and assay selection.** A scientist supplies the target disease name. Robin asks general pathology questions, uses Crow reports to identify 10 causal mechanisms, generates an in-vitro model and assay proposal for each, and ranks the reports using an LLM judge and pairwise comparisons (pp. 3-4; Fig. 1, p. 3).
2. **Candidate generation and ranking.** After selecting an assay, Robin generates 30 therapeutic candidates. Falcon produces a deep evaluation report for each candidate, covering rationale and limitations. An LLM-judged tournament ranks candidates by scientific rationale, pharmacology, and supporting methodology; human scientists may review the list and select candidates for lab testing (p. 4).
3. **Physical experiment.** The laboratory step is performed by researchers. In the dAMD demonstration, five initial candidates were tested in an RPE phagocytosis assay; the paper explicitly says the proposed fluorescent outer-segment substrate was replaced by pHrodo beads because of availability (p. 5). A second round tested additional candidates, including ripasudil (pp. 6-7).
4. **Data analysis and feedback.** The scientist uploads raw or semi-processed data and specifies an analysis approach. Finch executes analysis code in Jupyter; up to 10 independent trajectories can be run and meta-analyzed into a consensus conclusion. Robin distills actionable insights and can propose follow-up assays, feeding the next candidate-generation cycle (p. 5).

### Components

- **Crow:** PaperQA2-based concise literature search for experimental strategies and candidate discovery.
- **Falcon:** PaperQA2-based deep literature search and comprehensive candidate evaluation.
- **Finch:** autonomous Jupyter-native bioinformatics/data-analysis agent for flow cytometry and RNA-seq (pp. 3, 8; Fig. 1).
- **Robin orchestration:** implemented with Aviary in a Jupyter notebook; o4-mini synthesizes literature and generates hypotheses, while Claude 3.7 Sonnet acts as the pairwise-comparison judge (p. 8). Although the experiments used an agentic implementation, the authors report that tool order was almost always deterministic and translated it into a streamlined notebook for stability.
- **Judge calibration:** domain experts performed pairwise comparisons; those results were given to Google Gemini 2.5 Pro Preview to generate the judge prompt. The source reports 7.25/10 average top-10 overlap with experts and 88% judge versus 61% human repeat-selection consistency (p. 8; Supplementary Fig. S11, p. 25). This is evidence about ranking concordance/consistency, not autonomous scientific validation.
- **Finch environment:** ReAct-style prompting, an Aviary-controlled Docker environment, and two enabled tools, `edit_cell` and `submit_answer` (p. 8). The source also states that prompt engineering by domain experts is important for reliable results (p. 7).

### Experimental and analytical instantiation

The wet-lab methods use ARPE-19 RPE cells, a 96-well phagocytosis assay, pHrodo beads, flow cytometry, and RNA sequencing (pp. 9-11). Finch performed end-to-end flow-cytometry analysis, but a human scientist independently analyzed the same data and used an additional no-bead background-removal gate (p. 10; Supplementary Figs. S13-S14, pp. 26-27). For RNA-seq, a human performed demultiplexing/alignment and Finch performed differential-expression analysis (p. 10). Thus “bioinformatics agent autonomously analyzes” is accurate only for the stated Finch substeps, not for the entire RNA-seq pipeline.

The first round identified ROCK-inhibitor-related activity. Robin then proposed RNA-seq follow-up; Finch reported three-fold ABCA1 upregulation with adjusted p = 2.13 x 10^-83 in the stated comparison (p. 6; Fig. 3, p. 6; human analysis in Supplementary Fig. S15, p. 28). A later round reported ripasudil as a strong candidate, with a Finch result of 7.5-fold over DMSO, while the human analysis showed a 1.75-fold increase; the authors explicitly call for more doses and longer incubation before definitive comparison (p. 7; Fig. 4, p. 7).

## Frozen supplementary description: clause-by-clause comparison

Frozen source: `submission/analysis/citation_audit/core14-manifest.json`, Robin `supplementary_description`.

| Frozen clause | PDF evidence | Verdict |
|---|---|---|
| “A system for biomedical therapeutic discovery (dry age-related macular degeneration).” | The paper focuses on therapeutics and demonstrates the system on dAMD (pp. 2-7). | **SUPPORTED.** “Biomedical” is appropriately bounded by the dAMD/RPE use case; the paper also shows candidate lists for 10 additional diseases in Supplementary Figs. S16-S25 (pp. 7, 29-30). |
| “Cooperating agents perform literature search and deep evaluation” | Crow performs concise literature review; Falcon performs deep literature review and candidate evaluation; both are coordinated with Robin (pp. 3-4; Fig. 1C, p. 3). | **SUPPORTED, with minor precision.** Crow and Falcon are distinct search modes/agents; “cooperating” is fair at workflow level. |
| “rank candidates via an LLM tournament” | Candidate reports are ranked by pairwise LLM comparisons, with BTL ranking in Methods; the source calls this an LLM-judged tournament (pp. 4, 8). | **SUPPORTED.** The ranking is a surrogate judgment process, not human or experimental validation. |
| “and design assays.” | Robin proposes in-vitro disease models and assays, selects the top-ranked assay, and generates an experimental strategy (pp. 3-4; Fig. 2A, p. 4). | **SUPPORTED, qualified.** “Design” means literature-grounded assay/experimental-strategy proposals; the paper says Robin does not yet produce precise executable protocols (p. 7). |
| “Physical experiments (phagocytosis assays, RNA-seq sequencing and alignment) are performed by humans” | Researchers conduct the phagocytosis experiments and RNA-seq. Human work includes RNA-seq demultiplexing/alignment; Finch performs DGE analysis (pp. 5, 10). | **SUPPORTED.** This is an important autonomy boundary. |
| “while a bioinformatics agent autonomously analyzes flow-cytometry and differential-expression data” | Finch performs flow-cytometry analysis and DGE analysis in Jupyter; human analysis is also performed for flow cytometry, and human alignment precedes Finch’s RNA-seq analysis (p. 10). | **SUPPORTED, but requires qualification.** Correct for Finch’s analysis stages; “autonomously” must not imply autonomous experimental acquisition, complete RNA-seq processing, or absence of human comparison/prompt engineering. |
| “and meta-analyzes multiple trajectories.” | Robin can launch 10 Finch trajectories and meta-analyze outputs; the RNA-seq figure caption reports consensus findings from eight trajectories (p. 5; Fig. 3C, p. 6). | **SUPPORTED.** The description is consistent with both the general capability and the reported eight-trajectory RNA-seq example. |
| “Measured outcomes (e.g., phagocytosis improvement, gene upregulation with reported p-values) feed the next round” | Flow-cytometry results led to RNA-seq and a new candidate round; ABCA1 upregulation and p-value are reported; insights inform follow-up assays and new hypotheses (pp. 5-7). | **SUPPORTED, qualified.** The feedback is mediated by uploaded data, Finch/Robin interpretation, and human laboratory execution; the source does not establish that every measured outcome automatically triggers the next round. |
| “the full manuscript was system-generated” | Abstract says all hypotheses, experimental plans, data analyses, and data figures in the main-text report were produced by Robin. Methods say figures were formatted for readability in publication by a human; acknowledgements mention manuscript review/support (pp. 1, 5-8, 11). | **SUPPORTED only with scope qualification.** The PDF supports system generation of the listed main-text scientific content, but “full manuscript” is broader than the explicit abstract wording and should disclose human formatting, experimental work, alignment, review, and prompt engineering. |
| “and underwent peer review.” | The 30-page PDF contains a research manuscript and acknowledgements, but the source itself does not document a peer-review procedure or venue decision in the text read. | **UNVERIFIED FROM THIS PDF.** Do not treat this clause as source-supported evidence for peer review without an external record; external records were outside this single-PDF audit boundary. |

## Overall identity/architecture verdict

**`minor_revision` for the frozen description; source audit complete.** The description captures the core system and the dAMD demonstration. The main correction is to make the human-in-the-loop and partial-pipeline boundaries explicit: humans conduct the wet-lab work, human analysis validates flow cytometry, humans perform RNA-seq alignment, and domain experts materially shape Finch prompts and the judge prompt. “Full manuscript was system-generated” should be narrowed to the paper’s explicit claim about hypotheses, experimental plans, analyses, and figures in the main text. “Underwent peer review” is not established by this PDF alone and should be marked as externally sourced or removed from a PDF-only evidence summary.

EVIDENCE_COMPLETE: yes
