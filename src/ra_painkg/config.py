"""Configuration and constants for the RA-PainKG pipeline."""

from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

# PrimeKG files
PRIMEKG_CSV = DATA_DIR / "prime_kg.csv"
PRIMEKG_ZIP = DATA_DIR / "primekg_dataset.zip"

# GTEx file
GTEX_TPM = DATA_DIR / "GTEx_median_tpm.gct.gz"

# Output files
OUTPUT_GRAPHML = OUTPUT_DIR / "RA_PainKG.graphml"
OUTPUT_PKL = OUTPUT_DIR / "RA_PainKG.pkl"
OUTPUT_NODES = OUTPUT_DIR / "RA_PainKG_nodes.csv"
OUTPUT_EDGES = OUTPUT_DIR / "RA_PainKG_edges.csv"
OUTPUT_FINAL_GRAPHML = OUTPUT_DIR / "RA_PainKG_final.graphml"
OUTPUT_FINAL_PKL = OUTPUT_DIR / "RA_PainKG_final.pkl"
OUTPUT_NODES_FINAL = OUTPUT_DIR / "RA_PainKG_nodes_final.csv"
OUTPUT_EDGES_FINAL = OUTPUT_DIR / "RA_PainKG_edges_final.csv"
OUTPUT_TRACK_A = OUTPUT_DIR / "RA_PainKG_trackA.graphml"
OUTPUT_TRACK_B = OUTPUT_DIR / "RA_PainKG_trackB.graphml"
OUTPUT_GENES_ONLY = OUTPUT_DIR / "RA_PainKG_genes_only.graphml"
OUTPUT_SUMMARY = OUTPUT_DIR / "RA_PainKG_summary.json"
OUTPUT_STATS = OUTPUT_DIR / "graph_statistics.json"
OUTPUT_SEED_NODES = OUTPUT_DIR / "seed_nodes.csv"
OUTPUT_TRACK_ASSIGNMENTS = OUTPUT_DIR / "track_assignments.csv"
OUTPUT_CENTRALITY = OUTPUT_DIR / "gene_centrality.csv"
OUTPUT_GTEX_EXPR = OUTPUT_DIR / "pain_genes_gtex_expression.csv"
OUTPUT_LITERATURE = OUTPUT_DIR / "pain_gene_literature_evidence.csv"
OUTPUT_PATHWAYS = OUTPUT_DIR / "pain_signaling_pathways.md"

# RA-related MeSH/disease terms
RA_DISEASE_KEYWORDS = [
    "rheumatoid arthritis", "RA", "collagen-induced arthritis",
    "autoimmune arthritis", "inflammatory arthritis"
]

# Pain-related phenotype/process keywords
PAIN_PHENOTYPE_KEYWORDS = [
    "pain", "nociception", "hyperalgesia", "allodynia",
    "analgesia", "chronic pain", "inflammatory pain",
    "neuropathic pain", "central sensitization", "peripheral sensitization"
]

# Pain-related biological process keywords
PAIN_BP_KEYWORDS = [
    "nociception", "pain perception", "sensory perception of pain",
    "inflammatory response", "cytokine-mediated signaling",
    "neuropeptide signaling", "synaptic transmission",
    "ion transmembrane transport", "sodium ion transport",
    "calcium ion transport", "G protein-coupled receptor signaling",
    "opioid signaling", "prostaglandin biosynthetic process"
]

# Pain-related pathway keywords
PAIN_PATHWAY_KEYWORDS = [
    "TRP", "MAPK", "JAK-STAT", "NF-kappa B", "TNF",
    "neuroactive ligand-receptor", "calcium signaling",
    "serotonergic synapse", "dopaminergic synapse",
    "inflammatory mediator", "arachidonic acid",
    "complement and coagulation"
]

# Core pain genes (literature-curated)
CORE_PAIN_GENES = {
    "nociceptor_transduction": [
        "TRPV1", "TRPA1", "TRPM3", "TRPM8", "ASIC1", "ASIC2", "ASIC3", "ASIC4",
        "P2RX3", "P2RX4", "P2RX7", "PIEZO1", "PIEZO2"
    ],
    "voltage_gated_sodium": [
        "SCN9A", "SCN10A", "SCN11A", "SCN1A", "SCN2A", "SCN3A", "SCN8A"
    ],
    "voltage_gated_calcium": [
        "CACNA1A", "CACNA1B", "CACNA1H", "CACNA1I", "CACNA2D1"
    ],
    "neuropeptide_signaling": [
        "TAC1", "TACR1", "CALCA", "CALCB", "CALCRL", "RAMP1", "VIP", "NPY"
    ],
    "neurotrophin_signaling": [
        "NGF", "BDNF", "NTRK1", "NTRK2", "NGFR", "NTF3", "NTF4"
    ],
    "opioid_system": [
        "OPRM1", "OPRD1", "OPRK1", "OPRL1", "POMC", "PENK", "PDYN", "PNOC"
    ],
    "inflammatory_cytokines": [
        "TNF", "IL1B", "IL6", "IL1A", "IL1RN", "CCL2", "CCL5", "CXCL8",
        "IL17A", "IL17F", "IL23A", "CSF1"
    ],
    "cytokine_receptors": [
        "TNFRSF1A", "TNFRSF1B", "IL1R1", "IL6R", "IL6ST", "IL17RA", "IL23R"
    ],
    "mapk_signaling": [
        "MAPK1", "MAPK3", "MAPK8", "MAPK9", "MAPK14", "MAPK11",
        "FOS", "JUN", "ATF3", "EGR1", "CREB1"
    ],
    "jak_stat": [
        "JAK1", "JAK2", "JAK3", "TYK2", "STAT1", "STAT3", "STAT4", "STAT5A", "STAT5B"
    ],
    "nfkb": [
        "NFKB1", "NFKB2", "RELA", "RELB", "REL", "IKBKB", "IKBKG", "CHUK"
    ],
    "prostaglandin": [
        "PTGS2", "PTGS1", "PTGES", "PTGES2", "PTGER1", "PTGER2", "PTGER3", "PTGER4",
        "ALOX5", "ALOX12", "ALOX15", "LTA4H"
    ],
    "complement": [
        "C1QA", "C1QB", "C1QC", "C2", "C3", "C5", "C5AR1", "C6", "C7", "C8A", "C9"
    ],
    "gaba_glycine": [
        "GABRA1", "GABRA2", "GABRA3", "GABRA5", "GABRB2", "GABRB3",
        "GABRG2", "GABRD", "GLRA1", "GLRB", "SLC6A1"
    ],
    "serotonin": [
        "HTR1A", "HTR1B", "HTR2A", "HTR2C", "HTR3A", "HTR7", "SLC6A4"
    ],
    "endocannabinoid": [
        "CNR1", "CNR2", "FAAH", "MGLL", "NAPE-PLD", "DAGLA", "DAGLB"
    ],
    "kinase_signaling": [
        "AKT1", "AKT2", "MTOR", "PIK3CA", "SRC", "FYN", "LYN", "PRKCA", "PRKCD",
        "PRKCB", "PRKCE", "PRKCZ", "SYK", "BTK", "JAK1", "TYK2"
    ],
    "transcription_factors": [
        "FOS", "JUN", "ATF3", "EGR1", "CREB1", "NFKB1", "RELA", "STAT3",
        "SP1", "CEBPB", "NR3C1", "PPARG", "HIF1A"
    ],
    "ra_specific": [
        "PADI4", "PTPN22", "HLA-DRB1", "HLA-DQA1", "CD40", "CTLA4",
        "TRAF1", "TNFRSF14", "MMP1", "MMP3", "MMP9", "ACPA",
        "CD80", "CD86", "CD28", "ICOS", "RANKL", "TNFSF11"
    ],
    "anesthetic_targets": [
        "GABRA1", "GABRB2", "GABRG2", "GLRA1", "GLRB",
        "ADRA2A", "ADRA2B", "ADRA2C", "KCNK2", "KCNK3", "KCNK9",
        "SCN5A", "SCN10A", "GRIN1", "GRIN2A", "GRIN2B", "CHRNA4", "CHRNB2"
    ]
}

# Tissue-specific expression thresholds
TISSUE_MAP_TRACK_A = ["synovium", "whole_blood", "spleen", "lymph_node"]
TISSUE_MAP_TRACK_B = ["drg", "spinal_cord", "brain", "nerve_tibial"]

# GTEx tissue column name mapping
GTEX_TISSUE_COLUMNS = {
    "Brain - Spinal cord (cervical c-1)": "spinal_cord",
    "Nerve - Tibial": "nerve_tibial",
    "Whole Blood": "whole_blood",
    "Spleen": "spleen",
}

# PubMed literature evidence keywords
LITERATURE_KEYWORDS = {
    "pain signaling": "pain AND signaling AND pathway",
    "nociceptor": "nociceptor AND TRP AND channel",
    "inflammatory pain": "inflammatory AND pain AND cytokine",
    "central sensitization": "central AND sensitization AND spinal",
    "opioid analgesia": "opioid AND receptor AND analgesia AND perioperative",
    "RA pain mechanism": "rheumatoid AND arthritis AND pain AND mechanism",
}
