# AI Co-Scientist (Google): citation and parity audit

## Audit scope and source control

- **Source read:** `Towards an AI co-scientist`, the specified 81-page PDF, read from PDF page 1 through PDF page 81 in order. Evidence below is from this PDF only; no cited companion paper or other paper was read for this audit.
- **Target occurrences:** `EN-C018:gottweis2026coscientist` and `KO-C013:gottweis2026coscientist`.
- **Occurrence text:** Both occurrences cite Co-Scientist for the same local claim: a multi-agent hypothesis-generation system with experimental biomedical validation. The English occurrence additionally continues with the manuscript's framework-positioning and diagnostic claims; the Korean occurrence is a shortened translation of that surrounding paragraph.

## What the PDF actually establishes

### System identity and scope

- The abstract calls the system an AI co-scientist, a **multi-agent system built on Gemini 2.0**, intended to formulate novel research hypotheses and proposals aligned to scientist-provided objectives and guidance (PDF p. 1).
- The Introduction says the system searches and reasons over relevant literature, proposes hypotheses and experimental protocols for downstream validation, and provides literature grounding and reasoning (p. 3).
- The same paragraph explicitly says the work does **not** aim to completely automate science. It is built for a “scientist-in-the-loop” collaboration in which scientists specify goals, constraints and desirable attributes, supply ideas, refine outputs, and guide the system through chat (p. 3).
- The paper describes three biomedical applications: drug repurposing, novel treatment-target discovery, and mechanistic explanation of antimicrobial resistance (pp. 3-4). The key-contributions paragraph reports automated evaluation on **15** expert-curated open scientific goals (p. 4).

### Experimental validation and human boundary

- The Evaluation section defines the practical-utility test as **end-to-end wet-lab validations (laboratory experiments)** of system-generated hypotheses/proposals in three biomedical applications (p. 14).
- Crucially, the immediately following sentence states that **all three validations involved expert-in-the-loop guidance and prioritization of experiments** (p. 14). The paper therefore supports “experimental biomedical validation,” but not autonomous system-only validation.
- Figure 1's caption says the three settings are externally and independently validated by in-vitro laboratory experiments and separate co-timed reports (p. 3). The body provides the more precise boundary: the system generates/prioritizes hypotheses, while scientists select or prioritize experiments and the experiments are external laboratory work (pp. 2, 14, 19-20).
- In the AML example, the scientist supplies the goal; the system generates drug-repurposing predictions; scientists review and select candidates; then in-vitro experiments test them (p. 2). The Introduction similarly says predictions were validated using computational biology, expert clinician feedback and in-vitro wet-lab approaches (p. 3).
- For liver fibrosis, the paper reports novel epigenetic targets with anti-fibrotic activity in human hepatic organoids (p. 4; summary diagram and caption p. 2).
- For AMR/cf-PICI, the system independently proposed that cf-PICIs interact with diverse phage tails to expand host range, but this was an **in-silico discovery** that mirrored experimental results already obtained by an independent research group (p. 4). Section 4.7 and Figure 13 describe the conventional experimental pipeline and the AI-assisted hypothesis-development pipeline as separate, with the AI result recapitulating the independent finding in two days (pp. 26-27). The independent study performed the experimental validation; the co-scientist did not run that bacterial wet-lab experiment (p. 26).

### Quantitative and methodological qualifiers

- Across **11** expert-evaluated goals, the co-scientist received average preference rank **2.36**, novelty **3.64/5**, and impact **3.09/5** (p. 17). The paper explicitly labels these subjective expert assessments, not objective ground truth (pp. 17-18).
- The auto-evaluated Elo metric is also not independent ground truth (Figure 6 caption, p. 17). The paper calls the expert study small-scale and says larger studies are needed for reliable conclusions (p. 17).
- The Limitations section says open-access dependence may miss critical prior work and the system does not access the entire published literature because of license/access compliance (p. 27). It also identifies inherited LLM factuality, hallucination, bias and web-search limitations (p. 27).
- The paper says evaluations remain preliminary and require systematic evaluation across broader biomedical and scientific domains (p. 28). It also says therapeutic predictions do not cover drug delivery, bioavailability, pharmacokinetics and complex drug interactions, and that a dedicated translational scientific team is needed for clinical translation (p. 28).
- The paper's operational boundary remains human oversight: future-work text says final decisions are always made by scientists exercising expert judgment (p. 30), and rigorous expert validation/critical appraisal remain paramount (p. 31).

## EN-C018 assessment

**Local cited claim:** “Co-Scientist, a multi-agent hypothesis-generation system with experimental biomedical validation.”

- **Citation fit: CONFIRMED, with required qualification.** “Multi-agent” is directly supported by the abstract and architecture description (p. 1; pp. 7-9). Biomedical experimental validation is directly supported by the Evaluation section's end-to-end wet-lab-validation statement (p. 14), AML in-vitro results (pp. 19-23 and p. 61 onward), and liver-organoid validation (pp. 24-25).
- **Scope:** The cited clause is a compact system-level summary, not a claim that Co-Scientist autonomously performed all experiments. The source requires the human/external boundary to remain visible: all three validations had expert guidance and prioritization (p. 14), and the AMR case is independent-study recapitulation rather than system-run wet-lab validation (pp. 26-27).
- **Overclaim risk:** Low for the clause as written. It would become overclaiming if “experimental biomedical validation” were read as three autonomous system-run wet-lab validations, or as clinical validation. The PDF supports in-vitro/organoid and independent experimental evidence, not clinical efficacy or autonomous end-to-end laboratory control (pp. 14, 26-28, 30-31).
- **Recommended precision:** “a multi-agent hypothesis-generation system with expert-guided biomedical validation, including in-vitro/organoid experiments; its AMR example recapitulates an independent experimental finding.” This is more precise than the current clause but is not necessary to keep the citation substantively valid.
- **Surrounding English paragraph:** The additional English claims about the framework's diagnostic contribution are claims made by the manuscript, not claims established by this Co-Scientist paper. The Co-Scientist citation is attached to the Co-Scientist description only; citation scope should not be read as support for the framework's novelty, V-layer decomposition, or comparative claims.

## KO-C013 assessment

- **Translation parity of the cited clause: CONFIRMED.** The Korean wording preserves the two material predicates: “다중 에이전트 가설 생성 시스템” corresponds to “multi-agent hypothesis-generation system,” and “생물의학 wet-lab 검증” corresponds to “experimental biomedical validation.” It does not add a stronger autonomy, clinical, or quantitative claim.
- **Important Korean nuance:** “wet-lab 검증” is understandable but narrower/different in emphasis from the English “experimental biomedical validation.” The PDF's precise evidence includes in-vitro AML assays, human hepatic organoids, and an AMR in-silico recapitulation backed by an independent study. A parity-improving rendering would be “전문가가 우선순위를 정한 생물의학 실험 검증(AML 세포 및 인간 간 오가노이드의 in-vitro 검증 포함)” if space permits.
- **Human-boundary parity:** The Korean occurrence, like the English one, omits the nearby qualification that all three validations involved expert-in-the-loop guidance and experiment prioritization (p. 14). This is an omission of nuance, not a contradiction. The omission is more material for the AMR example because the source explicitly separates AI in-silico recapitulation from the independent experimental validation (pp. 26-27).
- **Surrounding paragraph parity:** KO-C013 is not a full literal translation of EN-C018's surrounding paragraph. It omits the English sentence that says standard POMDP/NovelSeek classifications code AI Scientist as closed-loop and that the framework locates the failure in biased gating rather than an absent gating layer. It also compresses the concluding comparison. This does not make the Co-Scientist citation invalid, but the bilingual paragraphs are not fully claim-by-claim parallel.
- **Recommended Korean precision:** “생물의학 실험 검증을 받은 다중 에이전트 가설 생성 시스템” is closer to the English; add “전문가의 실험 우선순위 설정을 포함하며, AMR 사례는 독립 연구의 실험 결과를 in-silico로 재현했다” when the human boundary matters.

## Verdict

Both occurrences are **appropriate for the narrow Co-Scientist identification claim**. The citation is not sufficient as a basis for autonomous-science or clinical-validation claims. The main evidence-preserving caveat is that validation was expert-guided and mixed: system-run in-vitro/organoid work for the AML and liver-fibrosis examples, versus in-silico recapitulation of independent experimental work for AMR. EN and KO are locally semantically aligned, but KO is a shortened surrounding translation and both occurrences understate the source's human-intervention boundary.

EVIDENCE_COMPLETE: yes
