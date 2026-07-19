# yamada2025aiscientistv2 — FULL-TEXT blind digest (READ)

**Paper:** "The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree
Search," Yamada, Lange, Lu, Hu, Lu, Foerster, Clune, Ha (Sakana AI / UBC / Vector / FLAIR Oxford),
arXiv 2504.08066v1, 10 Apr 2025. **Obtained:** arXiv PDF → vault
`ai_scientist/1_AI_Scientist_Core/Reference/Yamada 2025 - The AI Scientist-v2 Agentic Tree Search.pdf`
(69 pp). Read in full (blind agent v2reader) + orchestrator Tier-2 cross-check against lu2026 digest.

## Method
Template-free end-to-end discovery: idea gen w/ Semantic Scholar in-loop; an Experiment Progress
Manager over 4 stages; a **parallelized agentic tree search** (each node = script+plan+error+metrics
+LLM/VLM feedback+buggy status); a VLM reviewer; single-pass writing + reflection. Contrast to v1
(Lu 2024): v1 = template-based, linear; v2 = domain-general, tree-based, parallel, VLM.

## FACTS TABLE (key)
| Fact | Value | Loc |
|---|---|---|
| Title / core method | "…via Agentic Tree Search" | L3-5, L19 |
| Workshop | ICLR 2025 "I Can't Believe It's Not Better" (**ICBINB**) | L368, L373 |
| Submitted / pool | **3** submitted of **43** reviewed | L96, L389 |
| Accepted | **1 of 3**; avg **6.33/10** (6,6,7); ~**top 45%**; later **withdrawn** | L98, L370, L393-401 |
| IRB | UBC H24-02652 | L420 |
| Backbones | Claude 3.5 Sonnet (code), GPT-4o (feedback/summary), o1-style (writing) | Table 2 |
| **Balanced accuracy** | **NONE — no BA / 0.69 / reviewer-accuracy figure anywhere** (grep-verified) | — |
| Self-stated limits | workshop-level only, "nor …reach workshop-level consistently"; aims for *at least one* survivable paper, "not what fraction" | L636-638, L455-457 |
| Nature | **No mention of any Nature version of itself** (arXiv preprint; open-source repo AI-Scientist-v2) | grep |

## Adjudication — C129 (footnote identity)
Manuscript footnote: "(2024)/(2026) variants are template-based and agentic-tree-search
('AI Scientist-v2') modes, the latter its peer-reviewed Nature version [lu2026]."
- **VERDICT: ACCURATE** for what this paper is cited to support. The v2 = **agentic tree search**,
  **workshop-level** identity is verbatim-supported (title L3-5; abstract L19; ICBINB acceptance).
  The "(2024)=template / (2026)=tree-search" dichotomy is correct.
- The "peer-reviewed Nature version" half rests on **lu2026**, not this paper (v2 never mentions
  Nature; it is a 2025 arXiv preprint). Verified separately: lu2026 IS the Nature VoR of the
  AI-Scientist line whose template-free code repo is literally AI-Scientist-v2, so the footnote's
  equivalence holds. No change needed.

## Reverse findings — resolution (Tier-2)
- **"Balanced accuracy 0.69" not in this paper (v2reader flagged HIGH).** RESOLVED OK: the
  manuscript attributes 0.69 to **lu2026**, not v2, and lu2026 DOES contain it (digest: Table 1 p.915
  "Automated Reviewer pre-cutoff BA 0.69±0.04"; Methods p.919 "69% vs 66%"). No misattribution.
- **ICLR/ICBINB workshop peer review** appears in BOTH v2 and lu2026; manuscript sources Table 1 to
  lu2026, which reports it (70% workshop vs 32% main; 3 of 43; top 45%; 1 of 3; withdrawn). OK.
- **Optional precision (not applied):** manuscript could name the workshop "ICBINB", or add
  6.33 / 1-of-3 / withdrawn nuance. Current framing is accurate and already hedges the uncalibrated
  internal reviewer gate (main.tex L166), so not required.
- **Self-stated reliability limits (MED):** v2 is emphatic acceptance is workshop-level, not
  consistent. Manuscript's "π=Tree search / Loop closed Yes(tree)" is defensible and paired with the
  "uncalibrated V_s gate" caveat, so it does not overstate. OK.
