# Blind digest: cheetham2024gnome

**Full citation (from PDF front matter):** Cheetham, Anthony K.; Seshadri, Ram. "Artificial Intelligence Driving Materials Discovery? Perspective on the Article: Scaling Deep Learning for Materials Discovery." *Chem. Mater.* 2024, 36 (8), 3490–3495. DOI 10.1021/acs.chemmater.4c00643. CC-BY 4.0. Received Mar 4, 2024; Published Apr 8, 2024.

**Document type:** A *Perspective* article — a critical commentary/critique. It is NOT primary research; it reports no new experiments or calculations of its own beyond database inspection and manual crystallographic analysis of a random subset.

---

## Thesis / problem

This is a critique of the GNoME paper (Merchant et al., *Nature* 2023, "Scaling Deep Learning for Materials Discovery" — its ref 1). The GNoME paper claimed to "enable the discovery of 2.2 million structures below the current convex hull ... representing an order-of-magnitude expansion in stable materials known to humanity."

The authors' core argument: **the GNoME output is a list of *proposed compounds*, not new *materials*.** They "examine the claims of this work here, unfortunately finding scant evidence for compounds that fulfill the trifecta of novelty, credibility, and utility" (Abstract, lines 65-68). They propose that impactful new-materials predictions must lie within a triangle of being (a) **credible** (experimentally realizable), (b) **novel** (not a trivial extension of known compounds), and (c) **useful** (some demonstrated utility) — and argue GNoME predictions largely fail all three. Key sub-arguments:
- The predictions are of *crystalline inorganic compounds*, not "materials" broadly (which would exclude polymers, glasses, MOFs, heterostructures, composites) — the "order-of-magnitude expansion in stable materials" label is overreach (lines 117-148).
- Many entries lack **novelty** — they are trivial adaptations / already-known structure types identifiable in the ICSD (Inorganic Crystal Structure Database).
- Many entries lack **credibility** — they arise from DFT-at-0 K artifacts: artificial ordering of ions (lanthanides, Zr/Hf) that would in reality be disordered, producing spuriously low-symmetry / non-centrosymmetric structures and superstructures. Also anion-excess compositions (e.g. F2 molecules) from gas-phase chemical-potential errors.
- Many entries lack **utility** — no functionality demonstrated; large numbers involve radioactive/impractical elements.
- The **remedy**: incorporate domain expertise in materials synthesis and crystallography; connect predictions to known literature to filter non-novel candidates.

Notably, the tone is ultimately constructive: they "applaud" a 10x-larger repository of compounds, believe "the underlying approach is sound" because "the computational approach delivers credible overall compositions," and are "confident that the tools of AI and ML have a bright future in the field."

## Method (perspective/critique reasoning)

1. **Manual inspection of the GNoME Explorer archive** — examined the first 250 of the 2047 entries for signs of lacking novelty (not comprehensive, explicitly to "get a sense of any underlying issues").
2. **Space-group statistical analysis** — computed space-group frequency distribution of the 384,870 Stable Structure database entries (Table 1) and compared it to the ICSD distribution (as analyzed by Urusov & Nadezhina, ref 16).
3. **Random sampling** — selected 10 random compounds from the 384,870 Stable Structure entries and manually searched the ICSD to find their known structure analogues (Table 2, Figure 1).
4. Domain-expert crystallographic reasoning applied to individual example compounds (rewriting formulae, comparing lattice parameters to known phases).

---

## FACTS TABLE (exhaustive — every number in the paper)

| Value | Location | Context |
|---|---|---|
| 2.2 million | Intro, line 80 (quoting Merchant) | structures below the current convex hull claimed by GNoME |
| "Almost 400,000" | Intro, line 83 | structures deemed stable, listed in the Stable Structure database (quoting GNoME) |
| "more than 2000" | Intro, line 85-86 | new compounds placed in the GNoME Explorer archive |
| 2047 | Sec "General Comments," line 222-223 | exact number of entries in the GNoME Explorer compilation |
| first 250 | Sec "General Comments," line 221-222 | number of GNoME Explorer entries the authors examined |
| **384,870** | Table 1 header (line 275); repeated lines 409, 483, 545, 564, 634 | exact number of entries in the Stable Structure database (the paper's canonical count) |
| "almost 400,000" | Conclusions, line 544 | restatement of the Stable Structure list size |
| — Table 1 space-group occurrences (of 384,870) — | Table 1, lines 288-340 | Most abundant space groups in Stable Structure DB |
| Pm: 49037 / 12.7% | Table 1 | most common space group |
| P1: 39382 / 10.2% | Table 1 | |
| Amm2: 26467 / 6.88% | Table 1 | |
| Cm: 19913 / 5.17% | Table 1 | |
| C2/m: 12954 / 3.37% | Table 1 | |
| R3m: 11241 / 2.92% | Table 1 | |
| C2: 11201 / 2.91% | Table 1 | |
| P-1 (P1̄): 10463 / 2.72% | Table 1 | |
| R-3m: 8834 / 2.30% | Table 1 | |
| P-6: 8563 / 2.22% | Table 1 | |
| P-62m: 7652 / 1.99% | Table 1 | |
| Imm2: 7394 / 1.92% | Table 1 | |
| P3m1: 6903 / 1.79% | Table 1 | |
| P-3m1: 6379 / 1.66% | Table 1 | |
| P-6m2: 6038 / 1.57% | Table 1 | |
| Pnma: 6005 / 1.56% | Table 1 | ranked 16th in Stable Structure DB |
| ~16% (~8% each) | Space Group Analysis, lines 414-416 | ICSD top two space groups (Pnma, P21/c) combined share |
| 1.56% | line 417 | Pnma share in Stable Structure DB (ranked 16th) |
| 0.7% | line 418 | P21/c share in Stable Structure DB (an order of magnitude below ICSD) |
| ~34% | line 421 | combined share of the top FOUR Stable Structure space groups (all non-centrosymmetric) |
| top 24 / only 1 / ~1% | lines 422-423 | ICSD has only one non-centrosymmetric space group in its top 24, accounting for ~1% |
| 27 | Sec (vii), line 382 | proposed actinium (Ac3+) compounds in GNoME Explorer |
| "approximately 6754" | line 382-383 | Ac compounds in the larger Stable Structure database |
| < 1 milligram / per ton uranium | lines 385-387 | natural 227Ac yield from uranium ore |
| 21.77 years | line 387 | half-life of 227Ac |
| 18,138 | Sec (vii), line 396 | compounds of radioactive elements (Pm, Ac, Pa) in the large Stable Structure database |
| "more than 18,000" | Conclusions, line 602 | restatement (Pm, Ac, Pa) |
| 23,529 | Sec (vii), line 400 | further entries containing highly radioactive Tc, Np, Pu |
| 10 | Table 2 (line 449); Sec "Randomly Selected," line 482 | randomly selected compounds compared to ICSD |
| every one of the 10 | Sec (i), line 505-506 | all 10 random entries were identified in the ICSD |
| "in only one case" | Sec (ii), line 514 | only one random entry had the same space group as its ICSD analogue |
| 14 (rare-earths) + yttrium | Conclusions, line 611 | rare-earth elements with similar chemistries |
| "ten times larger" | Intro, line 113 | the repository of known compounds is now ~10x larger (authors applaud) |
| ICSD 640826 | Figure 1 caption, line 587-588 | ICSD id for known Zr4Ir4N structure |
| various individual lattice parameters | Secs (ii)-(vi), Table 2 discussion | e.g. LaB6 a≈4.1 Å; K3Nd(AsO4)2 a=9.8, b=5.8, c=7.6 Å, β=91.87°; TbSmSeO2 a≈3.91, c≈6.92 Å; DyHo2Rh9 a=5.26, c=17.58 Å; Ho3Co a=6.92, b=9.29, c=6.21 Å; Tb5Ir3 a=10.905, c=6.299 Å; etc. (crystallographic detail, not headline counts) |

**"736": DOES NOT APPEAR** anywhere in this paper. Confirmed by exhaustive grep — zero occurrences. The paper's canonical large count is **384,870**; the actinium-related counts are **27 / 6754 / 18,138 / 23,529**; there is no 736 in any form.

## Normative phrase: "experimentally realizable" vs any "realized" count

- The paper uses the phrase **"experimentally realizable"** as a *criterion*, not a measured count: "the proposed structure and composition of matter should be experimentally realizable" (lines 143-146), one leg of its credibility/novelty/utility triangle (the "trifecta"). This is normative/aspirational — it describes what a good prediction *should* be, not how many were realized.
- The paper reports **NO count of experimentally realized / synthesized compounds.** It never states that N of the GNoME/Stable-Structure entries were independently synthesized or validated. Its entire thesis is precisely the opposite: that "no functionality has been demonstrated for the 384,870 compositions ... they cannot yet be regarded as materials" (lines 563-565) and "we have yet to find any strikingly novel compounds in the GNoME and Stable Structure listings" (lines 631-632).

## Scope & explicit limitations (stated by the authors)

- Inspection was **"not done comprehensively since this would be too time-consuming"** — only the first 250 of 2047 GNoME Explorer entries examined (lines 219-222).
- Random-sampling analysis used only **10 compounds** out of 384,870 (small sample; explicitly acknowledged as selective/random rather than exhaustive).
- Authors acknowledge there "must be some new structure types predicted" and "some among the 384,870 compositions" that are novel — they simply "have yet to find" them; they do not claim to have proven none exist (lines 555-556, 631-634).
- They concede the underlying computational approach "delivers credible overall compositions" and "is sound" (lines 636-637) — the critique is about presentation, novelty filtering, disorder/entropy handling, and the "materials" labeling, not a wholesale rejection of the method.

## Does NOT claim / boundaries

- **Does NOT report any count of "independently experimentally realized" (synthesized/validated) compounds.** It provides no such number. It argues qualitatively that *predicted ≠ validated/realized materials* and that predicted compounds have not been shown to have utility, but attaches no numeric realized-count to that argument.
- Does not perform its own DFT or synthesis — the analysis is database inspection + manual crystallographic comparison against ICSD.
- Does not evaluate all entries — conclusions are drawn from small samples (250 and 10) plus aggregate space-group statistics over the full 384,870.
- Does not claim the GNoME method is worthless; explicitly the opposite in several places.
- **The number "736" is not present**, so any downstream claim attributing a "736 experimentally realized/verified" figure (or any 736-based statistic) to THIS paper would be unsupported by it.

## Section map

1. **Abstract** (lines 55-68) — trifecta of novelty/credibility/utility; "scant evidence."
2. **Introduction** (lines 72-148, pp. 3490-3491) — GNoME claims (2.2M / ~400k / 2000 / 2047); "material" vs "crystalline inorganic compound"; the credible/novel/useful triangle.
3. **General Comments About the GNoME Explorer Database** (lines 216-403, pp. 3491-3492) — examined first 250 of 2047 entries; observations (i)-(vii): (i) disorganized presentation, (ii) nomenclature issues (Ac(ErB8)3 example), (iii) improbable oxidation states / F2 molecules (TbSmF30), (iv) obvious analogues (K3Nd(AsO4)2), (v) improbable rare-earth ordering (TbSmSeO2), (vi) intermetallic ordering (DyHo2Rh9, TbHo2Tm9Co4, Tb16Ho(ErIr4)3), (vii) radioactive elements (27 Ac in Explorer / 6754 in Stable DB; 18,138 Pm+Ac+Pa; 23,529 Tc+Np+Pu).
4. **Space Group Analysis** (lines 404-461, p. 3492) — Table 1 (384,870 entries); comparison to ICSD; top-four all non-centrosymmetric (~34%); DFT-0K ordering explanation; cross-reference (ref 17) to a commentary on the A-Lab / Szymanski *Nature* 2023 robotic-synthesis paper (ref 18).
5. **Randomly Selected Examples from the Stable Structure Database** (lines 465-529, p. 3493) — Table 2 (10 compounds); conclusions (i)-(v): all 10 found in ICSD, usually higher symmetry; pseudosymmetry; Ga2Nb20Os8 → σ-phase; Cu8P4SrTm → CaCu4P2; Hf4Ir8N4NbZr11 → Zr4Ir2N (Figure 1); Ac4P8S28Tl8 → La analogue.
6. **Conclusions** (lines 539-641, p. 3494) — eliminate radioactive materials (>18,000); disorder/finite-T challenges; embed solid-state chemistry (RE/Y similarity, Zr/Hf similarity); Pauling's Fifth Rule (Rule of Parsimony); "proposed compounds" not "materials"; Li-ion conductor caveat (soft vs hard anions); constructive close.
7. **Figure 1** (p. 3494) — known Zr4Ir4N (ICSD 640826) vs proposed Hf4Ir8N4NbZr11.
8. **Author Information / Notes / Biographies / Acknowledgments / References** (pp. 3494-3495) — 29 references.
