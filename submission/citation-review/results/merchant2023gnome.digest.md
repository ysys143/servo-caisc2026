# Blind digest: merchant2023gnome

**Full citation (from paper):** Merchant, A., Batzner, S., Schoenholz, S. S., Aykol, M., Cheon, G. & Cubuk, E. D. "Scaling deep learning for materials discovery." *Nature* **624**, 80–85 (7 December 2023). https://doi.org/10.1038/s41586-023-06735-9. Google DeepMind / Google Research. Open access.

---

## Thesis / problem

Discovery of energetically favourable inorganic crystals has been bottlenecked by expensive trial-and-error and by the failure of prior machine-learning methods to accurately estimate stability (decomposition energy relative to the convex hull of competing phases). The paper shows that graph neural networks (GNNs) trained at scale via large-scale active learning — with DFT in the loop as a "data flywheel" — reach unprecedented generalization and improve the efficiency of materials discovery by roughly an order of magnitude. This lets GNoME discover 2.2 million structures below the current convex hull and expand the count of stable materials by an order of magnitude, and the resulting large first-principles dataset unlocks accurate, zero-shot machine-learned interatomic potentials (MLIPs).

## Method (what GNoME actually does)

- **GNoME = "graph networks for materials exploration."** All GNoME models are GNNs predicting the total energy of a crystal (message-passing formulation, shallow MLPs with swish/SiLU nonlinearities). Two model types:
  - **Structural models** — take a full crystal (lattice, structure, atom types); edges drawn when interatomic distance < 4.0 Å.
  - **Compositional models** — take only a reduced chemical formula (no structural info); paired with AIRSS (ab initio random structure searching) to generate 100 random structures per candidate composition for DFT evaluation.
- **Candidate generation:** (i) modifications of known crystals with adjusted ionic-substitution probabilities, plus a new **symmetry-aware partial substitutions (SAPS)** framework enabling incomplete replacements; (ii) random structure search (AIRSS) for the compositional pipeline. Produces >10^9 (paper writes "more than 109", i.e. 10^9) candidates over the course of active learning.
- **Active learning / data flywheel:** GNoME filters candidates by predicted energy against a stability threshold; filtered candidates are evaluated by DFT (VASP, PBE functional, PAW potentials, MP-consistent settings). DFT results both verify stability AND become new training data + new substitution seeds for the next round. Repeated for **six rounds**.
- **Uncertainty:** deep ensembles of **n = 10** graph networks; volume-based test-time augmentation (20 isotropic lattice scalings from 80% to 120%, aggregated by minimum reduction).
- **Downstream MLIP:** a NequIP potential (E(3)-equivariant, implemented in JAX/e3nn-jax) is pretrained on ionic-relaxation snapshots from the GNoME dataset for zero-shot force/energy prediction and MD.

---

## FACTS TABLE (exhaustive)

### Headline counts

| value / finding | exact location | context / EXACT wording |
|---|---|---|
| **2.2 million** structures below the current convex hull | Abstract (p.80); Intro (p.81); "Discovered stable crystals" (p.82); Conclusion (p.84) | "the discovery of 2.2 million structures below the current convex hull". Elsewhere: "GNoME models found 2.2 million crystal structures stable with respect to the Materials Project." These are DFT-predicted (PBE) stable. |
| **381,000** new entries on the updated convex hull | Intro (p.81); Fig.1b caption; "Discovered stable crystals" (p.82); Methods | "the updated convex hull consists of 381,000 new entries". Fig.1b: "led to 381,000 new stable materials, almost an order of magnitude larger than previous work." The 2.2M are stable vs prior work; of these, 381,000 sit on the *updated* (recomputed) convex hull as newly discovered. |
| **421,000** total stable crystals | Intro (p.81) | "381,000 new entries for a total of 421,000 stable crystals, representing an-order-of-magnitude expansion from all previous discoveries." (i.e. 40,000 prior + 381,000 new ≈ 421,000). |
| **48,000** computationally stable materials (prior baseline) | Abstract (p.80); Intro (p.80); Methods (p.499-domain) | "Building on 48,000 stable crystals identified in continuing studies". Intro: prior computational approaches "improve to 48,000 computationally stable materials according to our own recalculations". |
| **20,000** computationally stable structures in ICSD (out of ~200,000 entries) | Intro (p.80) | "Experimental approaches over the decades have catalogued 20,000 computationally stable structures (out of a total of 200,000 entries) in the ICSD." |
| **~69,000** materials in initial MP-2018 training snapshot | Methods, "Graph networks" (p.82) | "Initial models are trained on a snapshot of the Materials Project from 2018 of approximately 69,000 materials." |
| order-of-magnitude expansion in stable materials "known to humanity" | Abstract (p.80) | "Our work represents an order-of-magnitude expansion in stable materials known to humanity." |

### The 736 experimentally-realized count (CRITICAL — multiple phrasings)

| value / finding | exact location | context / EXACT wording |
|---|---|---|
| **736** independently experimentally realized | Abstract (p.80) | "Of the stable structures, 736 have already been independently experimentally realized." |
| **736** independently experimentally verified | Fig.1 caption, panel c (p.81) | "736 structures have been independently experimentally verified, with six examples shown50–55." (six examples: K2BiCl5, Li4MgGe2S7, Mo5GeB2, KV3Se3, Rb2HfSi3O9, Tm5Pd9P7) |
| **736** ICSD matches independently obtained through GNoME | "Validation through experimental matching and r2SCAN" (p.82) | "Of the experimental structures aggregated in the ICSD, 736 match structures that were independently obtained through GNoME." |
| **736** matches; **184** of these are novel discoveries since project start | Methods, "Definition of experimental match" (p.500-methods) | "Overall, we found 736 matches, providing experimental confirmation for the GNoME structures. **184 of these structures correspond to novel discoveries since the start of the project.**" |
| Matching pipeline: 4,235 composition matches → 4,180 parsed for structure → 736 structure matches | Methods, "Definition of experimental match" | ICSD queried **January 2023**. "By rounding to nearest integer formulas, we found 4,235 composition matches with materials discovered by GNoME. Of these, 4,180 are successfully parsed for structure. ... Overall, we found 736 matches ... likely to yield a lower bound." Strict compositional match; conservative. |

**NOTE on mechanism (important for citation accuracy):** The 736 are *matches between GNoME-predicted stable structures and entries already present in / added to the ICSD experimental database* (queried Jan 2023), i.e. experimental structures created independently/concurrently by other researchers — NOT crystals synthesized by the GNoME authors. Only **184** of the 736 correspond to materials that were *novel discoveries since the start of the project*. The paper frames this as "experimental confirmation"/"validation," a lower bound, using a strict compositional match.

### A second concurrent-validation statistic (distinct from the 736)

| value / finding | exact location | context |
|---|---|---|
| 3,182 compositions added to MP since snapshot; **2,202** available in GNoME database; **91%** match on structure | "Validation..." (p.82) | "of the 3,182 compositions added to the Materials Project since the snapshot, 2,202 are available in the GNoME database and 91% match on structure." This is validation vs concurrent MP additions, separate from the ICSD/736 count. |

### Model accuracy / hit-rate numbers

| value / finding | exact location | context |
|---|---|---|
| Final GNoME energy MAE = **11 meV atom⁻¹** | Intro (p.81); "Active learning" (p.82); Methods | "Final GNoME models accurately predict energies to 11 meV atom−1." Achieved after active learning (on relaxed structures). |
| Initial MP-2018 model MAE = **21 meV atom⁻¹** (structural) | "Graph networks" (p.82); Methods "Active learning" | "the improved networks achieve a MAE of 21 meV atom−1" (before scaling / start of active learning). |
| Prior benchmark MAE = **28 meV atom⁻¹** | "Graph networks" (p.82) | "Previous work benchmarked this task at a mean absolute error (MAE) of 28 meV atom−1 (ref.37)." |
| Compositional model precision (hit rate) = **33% per 100 trials** (composition only) | Intro (p.81); "Active learning" (p.82) | "33% per 100 trials with composition only, compared with 1% in previous work17." |
| Structural precision (hit rate) = **above 80%** with structure | Intro (p.81); "Active learning" (p.82) | "improve the precision of stable predictions (hit rate) to above 80% with structure". |
| Prior hit rate = **1%** (ref.17, OQMD) | Intro (p.81) | "compared with 1% in previous work17." |
| Starting hit rates: structural **< 6%**, compositional **< 3%** | "Active learning" (p.82) | "the hit rate for both structural and compositional frameworks start at less than 6% and 3%, respectively". |
| Discovery rates during active learning: **3%–10%** | Methods "Active learning" | "Filtration and subsequent evaluation with DFT led to discovery rates between 3% and 10%, depending on the threshold used for discovery." |
| Compositional GNN MAE **60 meV atom⁻¹** (MP, ref.25); reduced to **40 meV atom⁻¹** with ≥10 AIRSS runs | Methods "Training..." (p.499); Methods "Active learning" | "state-of-the-art generalization on the Materials Project (MAE of 60 meV atom−1 (ref.25))"; "compositional GNN error is reduced to 40 meV atom−1" (≥10 AIRSS runs), then precision raised to 33%. |

### Diversity / prototype numbers

| value / finding | exact location | context |
|---|---|---|
| **> 45,500** novel prototypes (5.6× increase from 8,000 of MP) | "Discovered stable crystals" (p.82); Fig.2c caption | "more than 45,500 novel prototypes in Fig.2c (a 5.6 times increase from 8,000 of the Materials Project)". Measured by XtalFinder (AFLOW). |
| GNoME displaces **at least 5,000** 'stable' materials from MP and OQMD | "Discovered stable crystals" (p.82) | "GNoME displaces at least 5,000 'stable' materials from the Materials Project and the OQMD." (i.e. prior 'stable' entries pushed off the hull.) |
| **232,477** of 381,000 stable structures attributable to a SAPS substitution | Methods "SAPS" | "A total of 232,477 out of the 381,000 stable structures can be attributed to a SAPS substitution." |

### r2SCAN validation (higher-fidelity functional)

| value / finding | exact location | context |
|---|---|---|
| **84%** of discovered binary & ternary crystals retain negative phase-separation energies under r2SCAN | Fig.2d caption; "Validation..." (p.82-83) | "84% of the discovered binaries and ternary materials also present negative phase-separation energies (as visualized in Fig.2d, comparable with a 90% ratio in the Materials Project ...)." Fig.2d: "84% of discovered binary and ternary crystals retain negative phase separations with more accurate functionals." (Unstable: 16%.) |
| **90%** ratio for Materials Project (comparison) | "Validation..." (p.83) | "comparable with a 90% ratio in the Materials Project but operating at a larger scale." |
| **86.8%** of tested quaternaries remain stable on r2SCAN convex hull | "Validation..." (p.83) | "86.8% of tested quaternaries also remain stable on the r2SCAN convex hull." |

### Composition families of interest

| value / finding | exact location | context |
|---|---|---|
| Layered materials: ~**1,000** (MP) → ~**52,000** (GNoME) | "Composition families..." (p.83) | "approximately 1,000 layered materials are stable compared with the Materials Project, whereas this number increases to about 52,000 with GNoME-based discoveries." |
| Li-ion conductors: **528** among GNoME discoveries (**25×** increase vs ref.46 original study) | "Composition families..." (p.83) | "we find 528 promising Li-ion conductors among GNoME discoveries, a 25 times increase compared with the original study46." |
| Li/Mn transition-metal oxides: **15** extra stable candidates vs the original **9** | "Composition families..." (p.83) | "GNoME has discovered an extra 15 candidates stable relative to the Materials Project compared with the original nine." |

### Interatomic potentials / MD (Fig.3)

| value / finding | exact location | context |
|---|---|---|
| **623** never-before-seen / unseen compositions for GNoME-driven MD superionic classification | "Screening solid-state ionic conductors" (p.83); Fig.3a caption; Methods "MD simulations" | "molecular-dynamics simulations on 623 never-before-seen compositions"; Fig.3a "tested on 623 unseen compositions"; Methods: "This results in 623 materials for which GNoME-driven molecular dynamics simulations are run." |
| Superionic threshold: σ at 1,000 K > **10^1.18 mS cm⁻¹** | Methods "AIMD conductivity experiments" | "we classify a material as having superionic behaviour if the conductivity σ at the temperature of 1,000 K, as measured by AIMD, satisfies σ1,000K > 10^1.18 mScm−1." (following ref.69) |
| Pretrained NequIP potential: **16.24 million** parameters | Methods "Methods for creating figures..." | "The pretrained potential has 16.24 million parameters." |
| Inference ~**14 ms** on A100 for 50-atom system; ~**12 ns day⁻¹** throughput (2-fs step) | Methods | "Inference on an A100 GPU on a 50-atom system takes approximately 14 ms, enabling a throughput of approximately 12 ns day−1 at a 2-fs time step." |
| Zero-shot GNoME potential outperforms SOTA NequIP trained on hundreds of structures; beats general-purpose M3GNet, CHGNet | "Zero-shot scaling..." (p.83); Fig.3c,d | Transferability tested train@400 K → eval@1,000 K; zero-shot GNoME "outperforms even a state-of-the-art NequIP model trained on hundreds of structures." |

### DFT / dataset / snapshot details (Methods)

| value / finding | exact location | context |
|---|---|---|
| MP snapshot = **March 2021**; OQMD snapshot = **June 2021** | Methods "Snapshots..." | "We use the data from the Materials Project as of March 2021 and the OQMD as of June 2021." Candidates also described as "derived from snapshots of databases made in March 2021" (p.82). |
| Revised comparison snapshot (MP/OQMD/WBM) = **July 2023**; ~**216,000** DFT calcs at consistent settings | Methods "Snapshots..." | "another snapshot ... was taken in July 2023. Approximately 216,000 DFT calculations were performed at consistent settings". |
| External (non-GNoME) stable crystals grew **35,000 → 48,000** from 2021 to 2023 | Methods "Snapshots..." | "From 2021 to 2023, the number of stable crystals external to GNoME expanded from 35,000 to 48,000, relatively small in comparison with the 381,000 new stable crystal structures ... in this paper." |
| Train/test split = **85% / 15%** via MD5 composition hash | Methods "Composition-based hashing" | "assign examples to the training (85%) and test (15%) sets" using MD5 hash of reduced formula, modulo 100, threshold at 85. |
| DFT: VASP, PBE functional, PAW potentials, **520 eV** plane-wave cutoff, DFT+U | Methods "VASP calculations" | MP-consistent settings; 520 eV cutoff; Hubbard U on subset of transition metals. |
| Structural model radial cutoff **4.0 Å**; interatomic-potential cutoff **5.0 Å** | Methods "Graph networks" | Edges drawn when atoms closer than cutoff. |
| AIRSS: always generate **100** structures per composition within 50 meV of predicted stable | Methods "AIRSS structure generation" | "we always generate 100 AIRSS structures for every composition that is otherwise predicted to be within 50 meV of stable". |
| Active-learning filtration threshold = **50 meV atom⁻¹** | Methods "Model-based filtration" | "a threshold of 50 meV atom−1 was used for active learning to improve the recall of stable crystal discovery." |
| Neural scaling: predictions improve as a **power law** with data | Intro (p.81); "Scaling laws and generalization" (p.82) | "our neural networks predictions improve as a power law with the amount of data" (refs 28,38). |
| Emergent OOD generalization: accurate predictions for structures with **5+ unique elements** despite training stopping at 4 | Intro (p.81); Fig.1d,e | "GNoME enables accurate predictions of structures with 5+ unique elements (despite omission from training)". |

---

## Scope & explicit limitations

- **"Stable" = DFT (PBE) stability vs the convex hull** (decomposition / phase-separation energy relative to competing phases). NOT experimental synthesis. The authors explicitly note GNoME materials "could be bumped off the convex hull by future discoveries," and GNoME itself displaces ≥5,000 previously-'stable' MP/OQMD entries.
- **r2SCAN check shows PBE stability is imperfect:** only 84% of binaries/ternaries and 86.8% of quaternaries remain stable under the more accurate r2SCAN functional — i.e. ~14–16% flip to unstable at higher fidelity.
- **"Experimentally realized/verified" (736) is a database-matching claim, not synthesis by the authors:** matches to ICSD experimental entries (queried Jan 2023), strict compositional match, described as a conservative "lower bound." Only 184 of the 736 are novel discoveries since the project began.
- **Open problems the authors flag (Conclusion):** transition of findings to applications; greater understanding of phase transitions via competing polymorphs; dynamic stability from vibrational profiles; configurational entropies; and ultimately **synthesizability** (explicitly listed as not resolved).
- **AIRSS failure:** for many compositions, most of the 100 AIRSS initializations fail to converge; "Prospective analysis was not able to uncover why most AIRSS initializations fail for certain compositions, and future work is needed."
- **Compositional models are weak for discovery** on their own (noisy formation-energy labels; must be paired with AIRSS).

## Does NOT claim / boundaries

- Does NOT claim the authors synthesized 736 (or any) new materials in a lab — realization/verification is via ICSD matching to independently created crystals.
- Does NOT claim all 2.2 million (or 381,000) are experimentally validated — only 736 have any experimental match, and only 184 of those are project-era novel discoveries.
- Does NOT claim r2SCAN- or experiment-level stability for the full set; PBE convex-hull stability is the operating definition, with r2SCAN as a spot-check on subsets.
- Does NOT claim dynamic/vibrational stability or synthesizability (explicitly listed as open).
- The "order-of-magnitude" claims refer to (a) discovery efficiency and (b) the count of stable materials known — not to experimental yield.

## Section map

- **Abstract** (p.80): headline counts — 48,000 baseline, 2.2M below hull, order-of-magnitude expansion, 736 experimentally realized, hundreds of millions of first-principles calcs, MLIPs + zero-shot ionic conductivity.
- **Intro** (p.80–81): prior baselines (20,000 ICSD / 48,000 recalculated), the 2.2M / 381,000 / 421,000 counts, 11 meV MAE, 80%/33% vs 1% hit rates, >10^9 candidates, power-law scaling, 5+ element OOD.
- **Fig.1** (p.81): discovery flywheel; 381,000; 736 verified (six examples, refs 50–55); scaling panels.
- **Overview of generation and filtration** (p.81): two frameworks (structural + compositional/AIRSS), SAPS.
- **GNoME (model)** (p.81–82): GNN architecture; MP-2018 69,000; MAE 28→21 meV.
- **Active learning** (p.82): six rounds; hit rates <6%/<3% → >80%/33%; 11 meV.
- **Scaling laws and generalization** (p.82): power-law test loss; OOD from random search.
- **Discovered stable crystals** (p.82): 2.2M; 381,000 on hull; ≥5,000 displaced; 45,500 prototypes (5.6× from 8,000).
- **Validation through experimental matching and r2SCAN** (p.82–83): March 2021 snapshots; 736 ICSD matches; 3,182→2,202 (91%) MP concurrent; 84%/90%; 86.8% quaternaries.
- **Composition families of interest** (p.83): layered 1,000→52,000; Li-ion 528 (25×); Li/Mn oxides +15 vs 9.
- **Scaling up learned interatomic potentials / Zero-shot scaling** (p.83–84): NequIP pretraining; transferability 400 K→1,000 K; beats M3GNet/CHGNet.
- **Screening solid-state ionic conductors** (p.83): 623 unseen compositions; superionic threshold.
- **Conclusion** (p.84): order-of-magnitude summary; open problems (phase transitions, dynamic stability, entropy, synthesizability).
- **References** (p.84–85): refs 1–56 main; 57–71 in Methods.
- **Methods** (p.85+): datasets/snapshots (March/June 2021, July 2023, 216,000 DFT); substitution patterns; SAPS (232,477); oxidation-state relaxations; AIRSS; model training (60→40 meV compositional; n=10 ensembles; 85/15 hash); DFT/VASP (520 eV); r2SCAN; experimental-match definition (4,235→4,180→736, 184 novel); figure-scaling methodology; NequIP details (16.24M params, 14 ms inference); MD (623 materials); data/code availability (materialsproject.org/gnome; github.com/google-deepmind/materials_discovery).
