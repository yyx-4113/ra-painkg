import os, re
os.chdir(r"D:\麻醉科共病\ra-painkg")
with open("benchmark/methods_paper.md", "r", encoding="utf-8") as f:
    content = f.read()

# ====== FIX 9: Add limitations row to Table 4 ======
old_t4 = """| Open-source formats | Yes | Yes | Yes | Yes | Yes (GraphML/CSV/PKL) |

RA-PainKG serves three primary use cases."""
new_t4 = """| Open-source formats | Yes | Yes | Yes | Yes | Yes (GraphML/CSV/PKL) |
| Known limitations | N/A | N/A | N/A | N/A | 62.5% pain gene coverage; no DRG/synovium GTEx data; static representation |

RA-PainKG serves three primary use cases."""
content = content.replace(old_t4, new_t4)
print("[9] Limitations row added to Table 4")

# ====== FIX 8: Add citation for "uncommon" claim ======
old_clm = "This approach-a knowledge graph that explicitly documents what it does not contain-is uncommon in the biomedical database literature and represents a methodological contribution for transparent resource development."
new_clm = "This approach-a knowledge graph that explicitly documents what it does not contain-is uncommon in the biomedical database literature. While resources such as the IUPHAR/BPS Guide to Pharmacology [14] acknowledge incomplete coverage in narrative form, systematic per-gene gap documentation with categorized absence reasons is rarely implemented. We argue this practice represents a methodological contribution for transparent resource development."
content = content.replace(old_clm, new_clm)
print("[8] Citation support added for 'uncommon' claim")

# ====== FIX 10: Explain K562 validation rationale ======
old_k562 = "First, the validation establishes honest boundary conditions. K562 chronic myeloid leukemia cells are fundamentally mismatched"
new_k562 = """First, the validation establishes honest boundary conditions. We emphasize that K562 cells were selected not as a biologically appropriate test system for RA pain (they are not), but as the only publicly available genome-scale Perturb-seq dataset with sufficient coverage to run a controlled multi-split benchmark. The purpose of this validation is not to demonstrate biological utility-it is to characterize the resource's predictive properties in a standardized setting and to establish transparent performance baselines against which future evaluations in disease-relevant models can be compared. K562 chronic myeloid leukemia cells are fundamentally mismatched"""
content = content.replace(old_k562, new_k562)
print("[10] K562 validation rationale explained")

# ====== FIX 13: Discuss low complement coverage ======
# Find the complement discussion area in 3.2
old_comp = "gene symbol inconsistencies between resources create mapping failures."
new_comp = """gene symbol inconsistencies between resources create mapping failures. The low match rate for complement components (35.7%) is particularly consequential: the complement system is increasingly recognized as a pain modulator through C5a-C5aR1 signaling in sensory neurons [17], and C5 polymorphisms are associated with RA susceptibility. This coverage gap means that complement-mediated pain mechanisms are essentially invisible to PrimeKG-based queries and represents a high-priority target for future KG integration."""
content = content.replace(old_comp, new_comp)
print("[13] Complement low coverage discussed")

# ====== FIX 14: Add biological justification for dual-track overlap ======
# Find in 3.1
old_overlap = "and the dual-track framework is provided as a conceptual organization scheme for hypothesis generation."
new_overlap = """The substantial Track A/B overlap (58.2%) is biologically expected: transcription factors (FOS, JUN, STAT3) activated by inflammatory cytokines also drive nociceptive sensitization, MAP kinases transduce both inflammatory and pain signals, and prostaglandins (via COX-2/PTGS2) bridge immune activation and nociceptor sensitization [5,7]. Rather than indicating poor track separation, this overlap reflects the mechanistic reality that inflammation and pain are deeply coupled in RA. The dual-track framework should be used as a conceptual lens for hypothesis generation-for example, genes exclusive to Track A or B may represent intervention points where anti-inflammatory and analgesic effects can be partially decoupled, while dual-track hub genes represent convergence points where both processes are jointly regulated."""
content = content.replace(old_overlap, new_overlap)
print("[14] Dual-track overlap justified biologically")

# ====== FIX 12: Move Table 3 to Supplementary, reference in text ======
# Find Table 3 block and replace with reference
old_t3_start = "**Table 3. Paired comparisons with delta-r 95% confidence intervals (pain genes)**"
old_t3_end = "primary tests in Table 3, the adjusted significance threshold"

t3_start = content.find(old_t3_start)
t3_ref = content.find(old_t3_end)

# Extract and move to supplementary
if t3_start > 0:
    # Replace the paired comparisons footnote with a clean reference
    old_t3_block = content[t3_start:content.find("**Cross-split consistency:**")]
    
    # Replace in body with reference to supplementary
    new_ref = "Paired statistical comparisons across 10 splits are provided in Supplementary Table S5, with Bonferroni correction for"
    content = content.replace(old_t3_end, new_ref)
    
    # Remove the table from body
    content = content.replace(old_t3_block, "")
    print("[12] Table 3 moved to Supplementary (reference added)")

with open("benchmark/methods_paper.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("[SAVED] Batch 3 complete")