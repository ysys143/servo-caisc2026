# Digest — jumper2021alphafold

**Citation:** Jumper, J. et al. "Highly accurate protein structure prediction with AlphaFold." *Nature* 596, 583–589 (26 August 2021). DOI 10.1038/s41586-021-03819-2. Open access. Received 11 May 2021; accepted 12 July 2021; published online 15 July 2021.

Read fully and BLIND (no knowledge of what any manuscript claims about this paper).

---

## Thesis / Problem

Predicting a protein's 3D structure from its amino acid sequence alone (the structure-prediction component of the "protein folding problem") has been an open problem for >50 years. Existing methods fall far short of atomic accuracy, especially when no homologous structure is available. The paper presents AlphaFold, "the first computational method that can regularly predict protein structures with atomic accuracy even in cases in which no similar structure is known," validated in the blind CASP14 assessment.

## Method — IS THIS A SPECIALIZED PREDICTOR? (audit's central question)

**YES. AlphaFold is a specialized single-task predictor: it maps an input (amino-acid sequence + MSA of homologues + optional templates) to one output (3D atomic coordinates of the protein). It is NOT a hypothesis-generation-and-search discovery loop.**

- Input → output is a single feedforward prediction task. The network "directly predicts the 3D coordinates of all heavy atoms for a given protein" from the primary sequence and aligned homologue sequences.
- Architecture (Fig. 1e): genetic/structure database search → MSA + pair representations → **Evoformer trunk (48 blocks)** → **structure module (8 blocks, shared weights)** → 3D structure. Followed by an Amber force-field relaxation (cleanup only; does not improve accuracy metrics).
- **"Recycling" is internal iterative refinement of ONE prediction, not a discovery/experiment cycle.** The whole network's output is fed recursively back into the same modules three times (four passes total). This is analogous to iterative refinement in computer vision — it refines a single structural hypothesis; it does NOT propose experiments, query external oracles, or run a generate-evaluate-select loop over candidate hypotheses.
- **No generation-and-search loop, no experimental loop, no autonomous discovery cycle.** The paper describes "the network searches and rearranges secondary structure elements for many layers" (T1064) — this is internal representation refinement across network depth, purely metaphorical "search," entirely inside the forward pass. There is no external tool use, no lab automation, no hypothesis iteration.
- Self-distillation (training-time only): a trained network predicts structures for ~350,000 Uniclust30 sequences, high-confidence subset added to training data, then retrain from scratch. This is a training procedure, not an inference-time discovery loop.

**CONFIRMED: single prediction task, no generation-and-search / experiment loop.**

---

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| Nature 596, 583–589 (26 Aug 2021) | header | Publication venue/pages |
| DOI 10.1038/s41586-021-03819-2 | p.583 | Article DOI |
| ~100,000 unique proteins | Abstract | # protein structures experimentally determined to date |
| billions of known protein sequences | Abstract | Sequence-structure gap |
| >50 years | Abstract | How long structure prediction has been an open problem |
| CASP14 | Abstract | 14th Critical Assessment of protein Structure Prediction; the blind test AlphaFold was validated in |
| **0.96 Å r.m.s.d.95** (95% CI 0.85–1.16 Å) | p.584 | AlphaFold median backbone accuracy (Cα r.m.s.d. at 95% residue coverage) on CASP14 |
| **2.8 Å r.m.s.d.95** (95% CI 2.7–4.0 Å) | p.584 | Next best method's median backbone accuracy on CASP14 |
| ~1.4 Å | p.584 | Width of a carbon atom (comparison point) |
| 1.5 Å r.m.s.d.95 (95% CI 1.2–1.6 Å) | p.584 | AlphaFold all-atom accuracy |
| 3.5 Å r.m.s.d.95 (95% CI 3.1–4.2 Å) | p.584 | Best alternative method all-atom accuracy |
| n = 87 protein domains | Fig. 1a | CASP14 dataset size |
| top-15 entries, out of 146 entries | Fig. 1a | AlphaFold shown vs top-15 of 146 CASP14 entrants |
| 10,000 bootstrap samples | Fig. 1a | CI estimation method |
| 2,180-residue single chain (T1044, PDB 6VR4) | p.584, Fig. 1d | Long protein predicted with correct domain packing, no structural homologues |
| median 1.46 Å (95% CI 1.40–1.56 Å), n = 3,144 chains | Fig. 2a | Recent-PDB backbone r.m.s.d. (template-filtered set) |
| lDDT-Cα = 0.997 × pLDDT − 1.17, Pearson r = 0.76, n = 10,795 | Fig. 2c | pLDDT confidence vs true accuracy fit |
| TM-score = 0.98 × pTM + 0.07, Pearson r = 0.85, n = 10,795 | Fig. 2d | pTM vs true TM-score fit |
| 48 blocks (no shared weights) | Fig. 3a, p.586 | Evoformer trunk depth |
| 8 blocks (shared weights) | Fig. 3d | Structure module depth |
| recycling three times (4 iterations) | p.585, Fig. 4b | Iterative refinement of whole network |
| 192 intermediate structures | p.587 | 4 recycling × 48 Evoformer blocks (trajectory analysis) |
| ~350,000 (exactly 355,993) sequences from Uniclust30 | p.587, Methods | Self-distillation predicted-structure dataset |
| decreases below ~30 sequences | p.588, Fig. 5a | MSA depth threshold where accuracy drops substantially |
| ~100 sequences | p.588 | MSA depth above which further gains are small |
| BFD: 65,983,866 families / 2,204,359,010 sequences | Methods | Big Fantastic Database scale (custom-built, released publicly) |
| PDB training cut-off 30 April 2018 (max release date) | Methods | Training set date limit |
| crop 256 residues, batch 128, 128 TPU v3 cores | Methods | Training config |
| ~10 million samples to convergence | Methods | Training length |
| ~1 week initial + ~4 days fine-tuning | Methods | Training wall-clock |
| 5 models (different seeds, some w/ templates) | Methods | Ensemble trained |
| No ensembling (V100): 0.6 min @256 res, 1.1 min @384 res, 2.1 h @2,500 res | Methods | Inference timings (open-source, XLA) |
| With ensembling: 4.8 min @256, 9.2 min @384, 18 h @2,500 | Methods | CASP14-config timings |
| ~1 GPU minute per model for 384 residues | Discussion | Headline speed figure |
| 8× faster without ensembling | Methods | Speedup |
| Remove BFD −0.4 GDT; remove MGnify −0.7 GDT; remove both −6.1 GDT | Methods | MSA source ablation |
| 10,795 protein sequences | Methods | Final recent-PDB test set size |
| CASP14 = May–July 2020 | p.584 | Assessment period; entered as team "AlphaFold2", different model from CASP13 AlphaFold (ref 10) |

## Scope & Limitations (as stated by the paper)

- **MSA-dependent:** accuracy decreases substantially when median MSA alignment depth < ~30 sequences (Fig. 5a).
- **Weak on heterotypic-contact-dominated chains:** much weaker for proteins with few intra-chain/homotypic contacts relative to heterotypic contacts — e.g. bridging domains in larger complexes whose shape comes almost entirely from other chains (details in companion paper, ref 39).
- **Monomer-focused:** predicts single protein structures; full hetero-complex prediction is left to "a future system."
- Amber relaxation does not improve accuracy metrics (GDT / lDDT-Cα); it only removes stereochemical violations.

## Does NOT Claim / Boundaries

- Does NOT explicitly predict ligands, ions, or cofactors (e.g. correctly places side chains around a zinc-binding site "even though it does not explicitly predict the zinc ion," Fig. 1c). Ligand/ion/stoichiometry effects are handled only implicitly.
- Does NOT run molecular-dynamics simulation of folding; it is not a physics-simulation method (though it uses physical/geometric inductive biases).
- Does NOT perform any autonomous scientific discovery, hypothesis generation, experiment design, or closed-loop iteration — it is a structure predictor.
- Does NOT claim experimental work was done (Reporting Summary: "no experimental work is described in this study; the results are the output of a computational method").
- Does NOT claim to solve the full "protein folding problem" — explicitly scoped to the *structure prediction component*.

## Section Map

- Abstract (p.583) — problem, claim, CASP14 headline.
- Intro (p.583–584) — physical vs evolutionary approaches; first method to near-experimental accuracy; CASP14 accuracy numbers (Fig. 1); recent-PDB generalization (Fig. 2).
- "The AlphaFold network" (p.584–585) — two-stage architecture overview; recycling.
- "Evoformer" (p.585–586) — trunk block, triangle updates, MSA/pair communication (Fig. 3).
- "End-to-end structure prediction" (p.586–587) — structure module, residue gas, IPA, FAPE loss, Amber relaxation.
- "Training with labelled and unlabelled data" (p.587) — self-distillation, BERT-style MSA masking.
- "Interpreting the neural network" (p.587) — per-block structure trajectories, ablations (Fig. 4).
- "MSA depth and cross-chain contacts" (p.588) — limitations (Fig. 5).
- "Related work" (p.588) — prior neural/evolutionary methods.
- "Discussion" (p.588–589) — bioinformatics+physical synthesis; utility (molecular replacement, cryo-EM); GPU-minutes speed; proteome-scale (companion paper, ref 39).
- Methods (p.589+) — IPA, inputs/databases (jackhmmer, HHBlits, BFD), training regimen, inference regimen, metrics (lDDT, GDT, TM-score, r.m.s.d.95), test-set construction, data/code availability, Reporting Summary.
