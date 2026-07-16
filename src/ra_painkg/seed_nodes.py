"""Seed node identification for RA-PainKG.

Identifies seed nodes from PrimeKG using keyword-based queries
for RA disease terms, pain phenotypes, pain genes, and pain-related
biological processes.
"""

import pandas as pd
import logging
from typing import Dict, List, Set, Tuple
from pathlib import Path

from .config import (
    RA_DISEASE_KEYWORDS, PAIN_PHENOTYPE_KEYWORDS,
    PAIN_BP_KEYWORDS, PAIN_PATHWAY_KEYWORDS, CORE_PAIN_GENES,
    OUTPUT_SEED_NODES
)
from .primekg_loader import PrimeKGLoader

logger = logging.getLogger(__name__)


class SeedNodeFinder:
    """Identify seed nodes for knowledge graph expansion."""

    def __init__(self, loader: PrimeKGLoader):
        self.loader = loader
        self.seed_nodes: Dict[str, Dict] = {}

    def find_ra_disease_nodes(self) -> Set[str]:
        """Find RA-related disease nodes."""
        ra_nodes = set()
        for keyword in RA_DISEASE_KEYWORDS:
            result = self.loader.query_nodes_by_name_keyword(
                keyword, name_col="x_name"
            )
            x_nodes = set(result[result["x_type"] == "disease"]["x_id"].astype(str))
            y_nodes = set(result[result["y_type"] == "disease"]["y_id"].astype(str))
            ra_nodes |= x_nodes | y_nodes

        logger.info(f"Found {len(ra_nodes)} RA disease seed nodes")
        self.seed_nodes["ra_disease"] = [
            {"node_id": nid} for nid in ra_nodes
        ]
        return ra_nodes

    def find_pain_phenotype_nodes(self) -> Set[str]:
        """Find pain-related phenotype/effect nodes."""
        pain_nodes = set()
        for keyword in PAIN_PHENOTYPE_KEYWORDS:
            result = self.loader.query_nodes_by_name_keyword(
                keyword, name_col="x_name"
            )
            x_nodes = set(
                result[
                    result["x_type"].isin(["effect/phenotype", "biological_process"])
                ]["x_id"].astype(str)
            )
            y_nodes = set(
                result[
                    result["y_type"].isin(["effect/phenotype", "biological_process"])
                ]["y_id"].astype(str)
            )
            pain_nodes |= x_nodes | y_nodes

        logger.info(f"Found {len(pain_nodes)} pain phenotype seed nodes")
        self.seed_nodes["pain_phenotype"] = [
            {"node_id": nid} for nid in pain_nodes
        ]
        return pain_nodes

    def find_pain_gene_nodes(self) -> Set[str]:
        """Find pain-related gene/protein nodes using core gene symbols."""
        all_pain_genes = set()
        for category, genes in CORE_PAIN_GENES.items():
            all_pain_genes.update(g.upper() for g in genes)

        gene_nodes = set()
        df = self.loader.df
        gene_mask = (df["x_type"] == "gene/protein") | (df["y_type"] == "gene/protein")

        for gene_symbol in all_pain_genes:
            x_nodes = set(
                df[
                    gene_mask
                    & (
                        df["x_name"].str.upper().str.strip() == gene_symbol
                    )
                ]["x_id"].astype(str)
            )
            y_nodes = set(
                df[
                    gene_mask
                    & (
                        df["y_name"].str.upper().str.strip() == gene_symbol
                    )
                ]["y_id"].astype(str)
            )
            gene_nodes |= x_nodes | y_nodes

        logger.info(f"Found {len(gene_nodes)} pain gene seed nodes "
                     f"(from {len(all_pain_genes)} searched symbols)")
        self.seed_nodes["pain_gene_protein"] = [
            {"node_id": nid} for nid in gene_nodes
        ]
        return gene_nodes

    def find_pain_bp_nodes(self) -> Set[str]:
        """Find pain-related biological process nodes."""
        bp_nodes = set()
        for keyword in PAIN_BP_KEYWORDS:
            result = self.loader.query_nodes_by_name_keyword(
                keyword, name_col="x_name"
            )
            x_nodes = set(
                result[result["x_type"] == "biological_process"]["x_id"].astype(str)
            )
            y_nodes = set(
                result[result["y_type"] == "biological_process"]["y_id"].astype(str)
            )
            bp_nodes |= x_nodes | y_nodes

        logger.info(f"Found {len(bp_nodes)} pain BP seed nodes")
        self.seed_nodes["pain_biological_process"] = [
            {"node_id": nid} for nid in bp_nodes
        ]
        return bp_nodes

    def find_pain_pathway_nodes(self) -> Set[str]:
        """Find pain-related pathway nodes."""
        pathway_nodes = set()
        for keyword in PAIN_PATHWAY_KEYWORDS:
            result = self.loader.query_nodes_by_name_keyword(
                keyword, name_col="x_name"
            )
            x_nodes = set(
                result[result["x_type"] == "pathway"]["x_id"].astype(str)
            )
            y_nodes = set(
                result[result["y_type"] == "pathway"]["y_id"].astype(str)
            )
            pathway_nodes |= x_nodes | y_nodes

        logger.info(f"Found {len(pathway_nodes)} pain pathway seed nodes")
        self.seed_nodes["pain_pathway"] = [
            {"node_id": nid} for nid in pathway_nodes
        ]
        return pathway_nodes

    def run_all(self) -> Dict[str, Set[str]]:
        """Run all seed node identification steps."""
        logger.info("=== Identifying Seed Nodes ===")
        results = {
            "ra_disease": self.find_ra_disease_nodes(),
            "pain_phenotype": self.find_pain_phenotype_nodes(),
            "pain_gene_protein": self.find_pain_gene_nodes(),
            "pain_biological_process": self.find_pain_bp_nodes(),
            "pain_pathway": self.find_pain_pathway_nodes(),
        }
        total = sum(len(v) for v in results.values())
        logger.info(f"Total seed nodes: {total}")
        return results

    def save_seed_nodes(self, path: Path = None):
        """Save seed node list to CSV."""
        path = path or OUTPUT_SEED_NODES
        rows = []
        for category, nodes in self.seed_nodes.items():
            for node in nodes:
                rows.append({
                    "node_index": node.get("node_index", ""),
                    "node_id": node["node_id"],
                    "node_type": node.get("node_type", ""),
                    "node_name": node.get("node_name", ""),
                    "node_source": category,
                })

        df = pd.DataFrame(rows)
        df.to_csv(path, index=False)
        logger.info(f"Saved {len(df)} seed nodes to {path}")
