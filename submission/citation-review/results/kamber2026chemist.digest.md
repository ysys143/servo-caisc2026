# Digest: kamber2026chemist (BLIND first-pass)

**Title:** How Claude performs on NMR prediction and structure elucidation — Assessing Claude Opus 4.7 against ChemDraw 25.0.2 and MestReNova 17.0.0
**Author:** David Kamber (Anthropic)
**Published:** June 5, 2026 · 13 pages · Anthropic technical report / blog-style paper

---

## Thesis / Problem

Tests whether a frontier general-purpose LLM (Claude) can perform **NMR spectral analysis** as well as the dedicated NMR software chemists rely on today. Spectral analysis is framed as one of the most time-consuming steps in synthetic chemistry; the goal is to see if Claude can offload it. Evaluated in **two directions**:
- **Forward prediction** (structure → NMR): draw expected structure, predict its ¹H/¹³C spectrum, compare to measured.
- **Inverse prediction / structure elucidation** (NMR → structure): given a spectrum, determine the structure.

## Method — IMPORTANT: physical characterization?

**YES. This paper is entirely about PHYSICAL CHARACTERIZATION via NMR and mass spec (MS).** It is a direct spectral-analysis / structure-elucidation study.

- What is evaluated: **Claude models vs. specialized NMR software.** Three Claude models (Opus 4.7, Opus 4.6, Sonnet 4.6) benchmarked against two dedicated packages — **ChemDraw 25.0.2** and **MestReNova 17.0.0**.
- Data source: compounds hand-curated from **ChemRxiv synthetic-chemistry preprints** with full ¹H and ¹³C characterization in the SI. A chemist read each preprint, kept compounds with complete self-consistent NMR + HRMS data, and manually transcribed the peak lists. Compounds locked BEFORE any predictions (to avoid selection bias); rotamer mixtures excluded.
- Forward task: each tool given a SMILES, asked to predict ¹H and ¹³C shifts (+ multiplicity + J-coupling constants where applicable) in the original report's solvent. Claude queried 3× per compound (run-to-run variability); ChemDraw/MestReNova deterministic, run once.
- Matching: predicted peaks matched one-to-one to experimental atoms by minimum |Δδ| (**Hungarian assignment**). ¹H multiplets reported as ranges >0.3 ppm dropped from shift-error calc but kept for multiplicity.
- Inverse task: Claude (Opus 4.7) given NMR + **HRMS** data, asked 3× to return up to 3 ranked SMILES candidates (stereochemistry excluded — 1D NMR cannot fix absolute config). Uses standard readouts a chemist would paste into chat (routine mass spec + NMR run, no setup).

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| Claude Opus 4.7, Opus 4.6, Sonnet 4.6 | Summary (l.25) | three Claude models tested |
| ChemDraw 25.0.2, MestReNova 17.0.0 | Title/subtitle (l.5–6) | two dedicated NMR software compared |
| 20 compounds | Summary/Eval (l.26, 88, 136) | forward shift/coupling prediction set |
| 4 scaffold classes × 5 compounds = 20 | Eval (l.136) | forward-task structure |
| 15 compounds | Intro/Eval (l.88, 137) | inverse structure-elucidation set |
| Opus 4.7 ¹H MAE = 0.079 ppm | Forward (l.179), Takeaway (l.301–304) | lowest ¹H error of any tool tested |
| Opus 4.7 ¹³C MAE = 1.37 ppm | Forward (l.181), Takeaway (l.300) | comparable to MestReNova |
| MestReNova ¹³C MAE = 1.48 ppm | Forward (l.181–182), Takeaway (l.300) | vs Opus 4.7's 1.37; "comparable" |
| ±0.20 ppm (¹H), ±1.0 ppm (¹³C) | Forward (l.176–177), Fig 4 | headline tolerance windows |
| 401 ¹H atoms, 225 ¹³C atoms | Forward (l.175) | fixed denominators for scoring |
| MestReNova ¹H coverage 267/401 atoms | Forward (l.187) | partial — >0.3 ppm multiplets skipped; not directly comparable |
| ~0.5 Hz mean \|ΔJ\| (all 3 Claude models) | Forward (l.202–203), Fig 8 | J-coupling accuracy |
| 80–84% of J pairs within ±0.5 Hz (Claude) | Forward (l.203) | Claude J-coupling pass rate |
| 1.9–2.0 Hz mean \|ΔJ\| (classical tools) | Forward (l.203) | ChemDraw/MestReNova J error |
| 26–35% within ±0.5 Hz (classical tools) | Forward (l.204) | classical J pass rate |
| 12.4 Hz geminal coupling in 5 of 31 J calls (ChemDraw) | Forward (l.205–206) | ChemDraw template-default artifact |
| aromatic vicinal couplings ~7.0–7.1 Hz | Forward (l.206) | ChemDraw defaults |
| 33 anchored experimental J pair-points | Fig 8 (l.263) | across the 20 compounds |
| NH proton experimental window 6.8–7.9 ppm | Forward (l.189) | slow-exchange NH; Opus 4.7 drifts upfield; Sonnet 4.6 misplaces to 10–13 ppm |
| 15 inverse problems, 3 attempts each | Inverse (l.270) | up to 3 ranked SMILES per attempt |
| 8 simpler targets: Q1–Q5, Q9, Q10, Q14 | Inverse (l.273–274) | HRMS + 1D NMR only |
| 7 denser targets: Q6–Q8, Q11–Q13, Q15 | Inverse (l.274–275) | + starting-material SMILES |
| Q6, Q8, Q12, Q15 → correct on all 3 attempts | Inverse (l.289–290) | denser targets w/ SM SMILES |
| Q7, Q11, Q13 → correct on 2 of 3 attempts | Inverse (l.290–291) | denser targets w/ SM SMILES |
| Simpler scaffolds recovered on every attempt | Intro/Inverse (l.120, 286) | from HRMS + spectra alone |
| Solvents assessed: DMSO-d₆, CDCl₃, D₂O | Limitations (l.324) | limited solvent coverage |
| Not assessed: methanol-d₄, benzene-d₆, acetone-d₆ | Limitations (l.324–325) | out of scope |
| 4 ChemRxiv preprint references | References (l.328–343) | Kordubailo (fused pyridazines), Heymans/Evano (maleimides from ynamides), Strong/Stoltz (Michael spirocyclization), Leitch/Wang (α-C(sp3) silylation) |

**Scaffold classes (forward):** P1 chloropyridazines (slow-exchange NH on aminopyridazine, DMSO-d₆); P2 Boc-N-aryl maleimides + N-Boc ynamides; P3 spiroketones (spirobicyclic ketones w/ phenacyl or acetyl pendants, diastereotopic CH₂); P4 α-silyl methanesulfonamides (shielded silicon-α carbons).

**Directional headline results:** ¹H shift + multiplicity: Opus 4.7 most accurate. ¹³C shift: Opus 4.7 ≈ MestReNova. J-coupling: all Claude models uniformly beat both classical tools. Peak coverage: ChemDraw widest (its main strength). Opus 4.7 most stable across replicates.

## Scope & Limitations (stated by paper)

- Assessment is **small**: 20 forward compounds / 4 scaffolds, 15 inverse — each scaffold contributes a single class of failure modes; numerical rankings "indicative rather than precise."
- Slow-exchange NH heteroaromatics sampled only via chloropyridazines (hydroxypyridines, aminothiazoles, other DMSO-d₆ NH-active scaffolds untested).
- **2D NMR (COSY, HSQC, HMBC) and stereochemistry are OUT OF SCOPE by design** — 1D NMR alone cannot fix configuration. The novelty claim is doing inverse elucidation from **1D data only**, where dedicated packages normally need 2D.
- Solvent coverage limited to DMSO-d₆, CDCl₃, D₂O.

## Does NOT claim / boundaries

- Does NOT claim to handle stereochemistry or absolute configuration.
- Does NOT use 2D NMR at all (explicitly excluded).
- ChemDraw has NO inverse/structure-elucidation capability; MestReNova assigns peaks to a known structure but does not generate candidates from a peak list — so the inverse comparison is Claude vs. a gap the classical tools don't fill, not a head-to-head.
- Does NOT claim general chemistry autonomy — scope is spectral prediction + 1D structure elucidation only.
- MestReNova ¹H numbers computed on partial coverage; paper explicitly cautions they are "not directly comparable."

## Section Map

1. Summary (p.2)
2. Introduction (p.3) — forward vs inverse directions; headline findings
3. Evaluation (p.5) — dataset construction
   - Selection protocol (p.5)
   - Forward prediction: structure → NMR (p.6) — Figs 2–8
   - Inverse prediction: NMR → structure (p.11) — Fig 9
4. Takeaway (p.12)
5. Limitations (p.13)
6. References (p.13) — 4 ChemRxiv preprints

**Figures:** Fig 1 (four scaffold classes); Fig 2 (MAE/RMSE ¹H & ¹³C + coverage); Fig 3 (|Δδ| distribution boxplots); Fig 4 (% within tolerance + per-compound win rate); Fig 5 (signed shift bias by scaffold); Fig 6 (atom-level error spread σ per tool×scaffold); Fig 7 (¹H multiplicity agreement); Fig 8 (J-coupling tolerance-band heatmap); Fig 9 (structure-elucidation results, 15 problems).
