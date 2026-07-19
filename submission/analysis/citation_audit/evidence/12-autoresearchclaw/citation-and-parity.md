# AutoResearchClaw: citation and parity audit

## Scope and reading record

- Audited source: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/AutoResearchClaw - Self-Reinforcing Autonomous Research with Human-AI Collaboration.pdf` only.
- The source metadata reports 23 pages, arXiv `2605.20025v1`, dated 19 May 2026. The registered SHA-256 is `be1d9a2c31d05052009ce1850b4573d9ae2010bc001bb2486c686647729ca491` and matches the audit manifest.
- I read the extracted text in page order and checked the rendered page set for all pages 1--23. Page references below are PDF page numbers, not extracted-text line numbers.
- No other PDF was opened and no API/model call was used.

## Citation inventory and manuscript occurrence

### Inventory

The core inventory entry is `submission/analysis/citation_audit/core14-manifest.json`, source index 12:

| Field | Inventory value | Audit result |
|---|---|---|
| system | `autoresearchclaw` / AutoResearchClaw | matches title and paper body |
| citation key | `liu2026autoresearchclaw` | matches `submission/references.bib` title, authors, arXiv id, and year |
| source | the PDF named above | exact target |
| page count | 23 | confirmed by PDF metadata and page-by-page read |
| version status | `exact` | consistent with manifest SHA and `v1` in the PDF |
| manuscript link IDs | `[]` | no EN or KO citation-link record exists |
| frozen supplementary description | present in manifest | audited sentence by sentence below |

`submission/references.bib:68-73` contains the bibliography record, but the citation-link inventory has no `EN-*` or `KO-*` occurrence for this source. `submission/analysis/multicoder/systems_desc.json:14` repeats the same frozen description used by the multicoder coding surface. `submission/analysis/multicoder/target_systems.md:28` lists the catalog label `AutoResearchClaw (Liu 2026)` but is not a manuscript citation occurrence.

### Manuscript occurrence

- `submission/main.tex` has no occurrence of `AutoResearchClaw`, `autoresearchclaw`, or `liu2026autoresearchclaw` in the manuscript text or citation commands.
- `submission/main_ko.tex` likewise has no occurrence of this system or citation key.
- The only relevant main-manuscript citation context is a general multi-citation list in `main.tex:69` and `main_ko.tex:88`, but it does not include `liu2026autoresearchclaw`; therefore it cannot be treated as a source occurrence.
- Verdict: **bibliographic inventory present, manuscript citation absent, frozen catalog description present**. The empty `manuscript_link_ids` is internally consistent with the source files.

## Frozen description: sentence-level evidence

Frozen description (manifest and `systems_desc.json`):

> A multi-domain research system using structured multi-agent debate. A hypothesis stage (innovator, pragmatist, contrarian) and a results stage (optimist, skeptic, methodologist) produce and interpret hypotheses; a self-healing executor decides per run to proceed, refine, or pivot (regenerating the hypothesis), running in a sandbox. A hallucination-verification layer fact-checks numbers and citations; experiments use an external benchmark rather than wet-lab. A cross-project failure memory turns past mistakes into guards, and a seven-level human-intervention mode (full-auto to step-by-step) is supported.

| ID | Frozen claim | Direct PDF support | Risk / judgment |
|---|---|---|---|
| F1 | “multi-domain research system” | pp. 7-8 describe the 20-topic scientific extension across HEP, systems biology, and statistics; p. 8 says the design reproduces experiments across heterogeneous scientific fields. The core 25-topic benchmark is ML (p. 6). | **Supported with scope caveat.** “Multi-domain” is supported by the extension, but the main baseline comparison is ML-only. Do not imply broad real-world scientific coverage beyond the reported benchmark domains. |
| F2 | “structured multi-agent debate” | pp. 3-4 specify two debate panels, each with K=3 agents and a synthesizer; p. 3 names the hypothesis-stage roles and p. 4 names the result-stage roles. | **Supported.** “Structured” is directly evidenced by role assignments, K=3, and structured artifacts. |
| F3 | hypothesis roles: innovator, pragmatist, contrarian | p. 3 names all three roles and says the synthesizer distills 2-4 falsifiable hypotheses with testability criteria and baselines. | **Supported.** |
| F4 | results roles: optimist, skeptic, methodologist | p. 4 names all three roles and describes strong-finding, significance/confound, reproducibility/data-leakage checks. | **Supported.** |
| F5 | self-healing executor with proceed/refine/pivot decisions | pp. 4-5 describe failure diagnosis, targeted repair, and three decisions: Proceed, Refine, Pivot. The abstract and pp. 2-3 also characterize failures as information. | **Supported, but the frozen wording omits Proceed semantics.** “Decides per run to proceed, refine, or pivot” is accurate. |
| F6 | Pivot can regenerate the hypothesis | p. 5 says Pivot moves to a new direction based on failure evidence and regenerates the hypothesis; Algorithm 1 on p. 16 repeats the pivot branch. | **Supported.** |
| F7 | executor runs in a sandbox | pp. 5-6 describe Docker isolation, non-root execution, resource limits, network policy, and execution-phase network disablement; Table 1 p. 3 marks sandbox security supported. | **Supported.** This is computational sandbox execution, not evidence of safe deployment in every environment. |
| F8 | hallucination-verification layer fact-checks numbers and citations | pp. 5-6 describe a verified result registry tying claims to executed outputs and a four-layer citation pipeline: DOI resolution, metadata validation, content relevance, and LLM relevance classification. p. 9 ablation shows removing verification permits fabricated values. | **Supported, but “hallucination-verification” is a compressed label.** The paper claims prevention/blocking of unsupported numbers and hallucinated citations within its pipeline; it does not establish perfect fact-checking. |
| F9 | experiments use an external benchmark rather than wet-lab | pp. 6-8 define ARC-Bench: 25 ML topics plus 20 computational scientific-domain topics. Table 1 p. 3 marks real experiment execution supported, so “rather than wet-lab” is accurate for the reported evaluation, but “external benchmark” is imprecise: ARC-Bench is introduced by the paper, not an independently external benchmark. | **Needs tightening.** Prefer “experiments are evaluated on the paper’s ARC-Bench computational benchmark; no wet-lab validation is reported.” |
| F10 | cross-project failure memory turns mistakes into guards | pp. 5-6 describe a persistent lesson store, structured failure lessons, guard generation, and time-decayed weighting. Appendix A pp. 13-16 defines lesson records, guard types, and injection into later runs. | **Mostly supported.** “Cross-project” is stronger than the paper’s recurring “cross-run” language. The paper says lessons from previous runs; it does not clearly establish independent projects as the storage boundary. Prefer “cross-run failure memory.” |
| F11 | seven-level human-intervention mode | pp. 5 and 8, Table 3 p. 6, and Appendix E p. 20 enumerate seven regimes: Full-Auto, Gate-Only, CoPilot, Thorough, Step-by-Step, Pre-Experiment, Post-Experiment. | **Supported, but terminology matters.** These are seven intervention regimes/modes, not necessarily seven ordered levels. |
| F12 | range full-auto to step-by-step | p. 8 and Appendix E p. 20 explicitly define Full-Auto as zero interventions and Step-by-Step as every stage; Table 3 reports the same endpoints. | **Supported.** |

## Important quantitative and scope checks

- The abstract and pp. 2, 6, and 9 report a **54.7%** improvement against AI Scientist v2. Table 2 p. 6 gives CoPilot 0.648 versus AI Scientist v2 0.419; `(0.648-0.419)/0.419 = 54.7%` after rounding. This is a relative improvement for the 25-topic experiment-stage score, not a universal research-quality or scientific-discovery improvement.
- The same table gives Full-Auto 0.596 and CoPilot 0.648. The frozen description does not include the 54.7% number, so it avoids this numerical scope risk.
- The seven-mode HITL result is reported on 10 topics, with CoPilot 87.5% accept rate versus Full-Auto 25.0% and Step-by-Step 50.0% (Table 3 p. 6). The paper inconsistently describes CoPilot as 19 targeted interventions in the prose on p. 8 while Table 3 lists 6 interventions; this is a source-internal discrepancy. Do not add intervention counts to the frozen description without resolving it.
- The paper itself states limitations: the T10 full-auto run passes numeric verification while being scientifically uninformative (pp. 9, 21); 11 of 13 invalid canonical HITL runs fail at stage 17 (p. 21); and safeguards do not guarantee correct conclusions or submission-ready formatting (p. 22). These limitations constrain any stronger wording about “fact-checking,” “prevents,” or autonomous scientific validity.

## Citation scope

Because the target paper is not cited anywhere in `main.tex` or `main_ko.tex`, there is currently no manuscript claim whose citation scope can be validated as a formal `\citep{liu2026autoresearchclaw}` attribution. The catalog description is source-grounded, but it is not citation-linked in the manuscript inventory.

If the system is later cited, the citation should be attached only to claims directly supported by this PDF, with scope qualifiers:

1. Use the citation for the five mechanisms, role names, Pivot/Refine behavior, benchmark setup, and seven intervention regimes.
2. Qualify benchmark claims by dataset, evaluation mode, comparator, and intervention condition.
3. Do not use this paper as evidence for wet-lab discovery, general human-level research autonomy, perfect hallucination prevention, or cross-project learning unless a future source passage explicitly supports those claims.
4. Replace “external benchmark” with “the paper’s ARC-Bench computational benchmark” to avoid implying an independently sourced benchmark.
5. Replace “cross-project failure memory” with “persistent cross-run failure memory” unless project-level persistence is documented elsewhere.

## English/Korean parity

There is no AutoResearchClaw frozen-description counterpart in `main_ko.tex`; both language manuscripts lack the source citation and system occurrence. Consequently, the current EN/KO parity status is **N/A for manuscript text, but complete for absence**: neither language makes the claim, and neither language cites the source.

The catalog source `submission/analysis/multicoder/systems_desc.json` is English-only. No Korean translation of this frozen description was found in the audited manuscript surfaces. If a Korean catalog or manuscript description is added later, it must preserve these distinctions:

- “multi-domain” = ML plus the reported HEP/biology/statistics computational extension, not wet-lab breadth;
- `Pivot/Refine/Proceed` = three decisions, with Pivot able to regenerate a direction/hypothesis;
- verification = registry and four-layer citation checks, not a guarantee of truth;
- benchmark = ARC-Bench introduced and used by the paper, not necessarily external;
- memory = cross-run, unless cross-project persistence is separately evidenced;
- seven modes = seven intervention regimes, with Full-Auto and Step-by-Step as endpoints.

## Verdict

**MINOR REVISION / citation inventory gap.** The frozen description is substantively faithful to the 23-page PDF. F1-F8 and F11-F12 are supported; F9 should be narrowed from “external benchmark,” and F10 should be narrowed from “cross-project” to “cross-run.” The bibliography record is present, but there is no EN/KO manuscript occurrence or citation-link record, so this source currently contributes no cited manuscript claim. The paper’s own benchmark and verification limitations should block stronger autonomous-discovery or perfect-integrity wording.

EVIDENCE_COMPLETE: yes
