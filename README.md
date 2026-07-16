# RA-PainKG: Tissue-Specific Knowledge Graph for RA Pain Signaling

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A tissue-specific, pain-focused knowledge graph integrating PrimeKG, GTEx v8, and PubMed literature curation for rheumatoid arthritis pain signaling research.

## Overview

RA-PainKG contains **18,069 nodes** and **127,226 directed edges** organized into a dual-track framework:
- **Track A (炎症/Inflammation)**: 106 genes in immune-inflammatory signaling
- **Track B (伤害感受/Nociception)**: 122 genes in pain transduction and modulation
- **Dual Track**: 96 genes spanning both domains

## Quick Start

```python
import networkx as nx
import pickle

# Load the knowledge graph
with open("output/RA_PainKG_final.pkl", "rb") as f:
    g = pickle.load(f)

# Get all Track B (nociception) genes
track_b = [n for n, d in g.nodes(data=True) if d.get('track') == 'B']

# Get top hub nodes
bc = nx.betweenness_centrality(g, k=100)
top_hubs = sorted(bc.items(), key=lambda x: -x[1])[:10]
```

## Installation

```bash
git clone https://github.com/[username]/ra-painkg.git
cd ra-painkg
pip install -r requirements.txt
```

## Pipeline Usage

```bash
# Run full pipeline
python -m ra_painkg.pipeline

# Run specific steps
python -m ra_painkg.pipeline --steps kg        # KG construction only
python -m ra_painkg.pipeline --steps analysis  # Network analysis only
python -m ra_painkg.pipeline --steps viz       # Visualization only
```

## Project Structure

```
ra-painkg/
├── src/ra_painkg/         # Python package
│   ├── __init__.py        # Package metadata
│   ├── config.py          # Constants and paths
│   ├── primekg_loader.py  # PrimeKG data loading
│   ├── seed_nodes.py      # Seed node identification
│   ├── literature_mining.py # PubMed literature curation
│   ├── gtex_filter.py     # GTEx tissue expression filtering
│   ├── track_assigner.py  # Dual-track gene assignment
│   ├── kg_builder.py      # Knowledge graph construction
│   ├── network_analysis.py # Centrality and topology analysis
│   ├── visualization.py   # Publication-quality figures
│   └── pipeline.py        # End-to-end pipeline
├── data/                  # Input data (PrimeKG, GTEx)
├── output/                # Generated KG files and figures
├── notebooks/             # Jupyter notebooks for exploration
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Output Files

| File | Description |
|------|-------------|
| `RA_PainKG.graphml` | Full KG in GraphML format |
| `RA_PainKG.pkl` | Full KG as Python pickle |
| `RA_PainKG_nodes.csv` | Node table |
| `RA_PainKG_edges.csv` | Edge table |
| `RA_PainKG_final.graphml` | Largest connected component |
| `RA_PainKG_trackA.graphml` | Track A subgraph |
| `RA_PainKG_trackB.graphml` | Track B subgraph |
| `fig1-6_*.pdf/png` | Publication figures |
| `RA_PainKG_summary.json` | Summary statistics |
| `gene_centrality.csv` | Per-gene centrality metrics |
| `pain_signaling_pathways.md` | Annotated pathway report |

## Data Sources

- **PrimeKG**: Chandak et al. (2023), *Scientific Data*. [DOI: 10.7910/DVN/IXA7BM](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/IXA7BM)
- **GTEx v8**: GTEx Consortium (2020), *Science*. dbGaP: phs000424.v8.p2
- **PubMed**: Manual literature curation for 10 pain signaling pathways

## Citation

If you use RA-PainKG in your research, please cite:

```bibtex
@article{ra-painkg2026,
  title = {RA-PainKG: A Tissue-Specific Knowledge Graph for Rheumatoid Arthritis Pain Signaling},
  author = {[Authors]},
  journal = {Scientific Data},
  year = {2026},
  doi = {[to be assigned]}
}
```

## License

MIT License. See LICENSE file for details.
