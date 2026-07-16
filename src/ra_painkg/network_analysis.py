"""Network topology analysis for RA-PainKG.

Computes centrality metrics, identifies hub/bottleneck nodes,
and compares network topology between Track A (inflammation) and
Track B (nociception).
"""

import logging
import json
import networkx as nx
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .config import OUTPUT_CENTRALITY, OUTPUT_STATS

logger = logging.getLogger(__name__)


class NetworkAnalyzer:
    """Analyze network topology and centrality of RA-PainKG."""

    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self._centrality: Optional[pd.DataFrame] = None

    def compute_centrality(
        self,
        metrics: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """Compute centrality metrics for all nodes.

        Parameters
        ----------
        metrics : list of str
            Metrics to compute. Options: betweenness, degree, closeness,
            eigenvector, pagerank. Default: all.

        Returns
        -------
        DataFrame with node_index, node_name, and centrality columns
        """
        if metrics is None:
            metrics = ["betweenness", "degree", "closeness", "eigenvector", "pagerank"]

        logger.info(f"Computing centrality metrics: {metrics}")

        # For large graphs, use approximations
        n = self.graph.number_of_nodes()
        results = []

        for i, (node, data) in enumerate(self.graph.nodes(data=True)):
            row = {
                "node_index": i,
                "node_name": str(data.get("node_name", node)),
                "category": data.get("category", "other"),
                "track_a": data.get("track_a", False),
                "track_b": data.get("track_b", False),
                "primekg_tissue": data.get("node_type", "") in ("gene/protein", "protein"),
            }
            results.append(row)

        df = pd.DataFrame(results)

        # Betweenness centrality (approximate for large graphs)
        if "betweenness" in metrics:
            logger.info("  Computing betweenness centrality...")
            if n > 5000:
                k = min(500, n)
                bc = nx.betweenness_centrality(self.graph, k=k, weight=None)
            else:
                bc = nx.betweenness_centrality(self.graph, weight=None)
            df["betweenness"] = df["node_index"].apply(
                lambda i: bc.get(results[i]["node_name"], 0.0)
            )

        # Degree centrality
        if "degree" in metrics:
            logger.info("  Computing degree centrality...")
            dc = nx.degree_centrality(self.graph)
            df["degree"] = df["node_index"].apply(
                lambda i: dc.get(results[i]["node_name"], 0.0)
            )

        # Closeness centrality
        if "closeness" in metrics:
            logger.info("  Computing closeness centrality...")
            try:
                cc = nx.closeness_centrality(self.graph)
                df["closeness"] = df["node_index"].apply(
                    lambda i: cc.get(results[i]["node_name"], 0.0)
                )
            except Exception as e:
                logger.warning(f"Closeness centrality failed: {e}")
                df["closeness"] = 0.0

        # Eigenvector centrality
        if "eigenvector" in metrics:
            logger.info("  Computing eigenvector centrality...")
            try:
                ec = nx.eigenvector_centrality_numpy(self.graph)
                df["eigenvector"] = df["node_index"].apply(
                    lambda i: ec.get(results[i]["node_name"], 0.0)
                )
            except Exception as e:
                logger.warning(f"Eigenvector centrality failed: {e}")
                df["eigenvector"] = 0.0

        # PageRank
        if "pagerank" in metrics:
            logger.info("  Computing PageRank...")
            pr = nx.pagerank(self.graph, alpha=0.85)
            df["pagerank"] = df["node_index"].apply(
                lambda i: pr.get(results[i]["node_name"], 0.0)
            )

        self._centrality = df
        logger.info(f"Centrality computed for {len(df)} nodes")
        return df

    def get_top_hubs(
        self, metric: str = "betweenness", n: int = 20
    ) -> pd.DataFrame:
        """Get top N hub nodes by a centrality metric."""
        if self._centrality is None:
            self.compute_centrality()
        return self._centrality.nlargest(n, metric)[
            ["node_name", metric, "track_a", "track_b"]
        ]

    def get_gene_centrality(
        self, gene_nodes_only: bool = True
    ) -> pd.DataFrame:
        """Get centrality metrics for gene nodes only."""
        if self._centrality is None:
            self.compute_centrality()
        df = self._centrality
        if gene_nodes_only:
            df = df[df["primekg_tissue"]]
        return df.sort_values("betweenness", ascending=False)

    def compare_tracks(self) -> Dict:
        """Compare network topology between Track A and Track B."""
        if self._centrality is None:
            self.compute_centrality()

        track_a = self._centrality[self._centrality["track_a"]]
        track_b = self._centrality[self._centrality["track_b"]]

        comparison = {
            "track_a_genes": len(track_a),
            "track_b_genes": len(track_b),
            "track_a_top_betweenness": track_a.nlargest(10, "betweenness")[
                "node_name"
            ].tolist(),
            "track_b_top_betweenness": track_b.nlargest(10, "betweenness")[
                "node_name"
            ].tolist(),
            "track_a_mean_degree": float(track_a["degree"].mean()),
            "track_b_mean_degree": float(track_b["degree"].mean()),
            "track_a_mean_betweenness": float(track_a["betweenness"].mean()),
            "track_b_mean_betweenness": float(track_b["betweenness"].mean()),
        }
        return comparison

    def get_graph_statistics(self) -> Dict:
        """Compute comprehensive graph-level statistics."""
        g = self.graph
        stats = {
            "total_nodes": g.number_of_nodes(),
            "total_edges": g.number_of_edges(),
            "density": nx.density(g),
            "is_directed": g.is_directed(),
        }

        # Node type distribution
        node_types = {}
        for _, data in g.nodes(data=True):
            nt = data.get("node_type", "unknown")
            node_types[nt] = node_types.get(nt, 0) + 1
        stats["node_types"] = node_types

        # Edge relation distribution
        edge_rels = {}
        for _, _, data in g.edges(data=True):
            rel = data.get("relation", "unknown")
            edge_rels[rel] = edge_rels.get(rel, 0) + 1
        stats["edge_relation_types"] = edge_rels

        # Seed node counts
        stats["ra_disease_nodes"] = sum(
            1 for _, d in g.nodes(data=True)
            if d.get("category") == "seed" and "disease" in str(d.get("node_type", ""))
        )
        stats["pain_phenotype_nodes"] = sum(
            1 for _, d in g.nodes(data=True)
            if d.get("category") == "seed" and "phenotype" in str(d.get("node_type", ""))
        )
        stats["pain_gene_nodes"] = sum(
            1 for _, d in g.nodes(data=True)
            if d.get("track_a") or d.get("track_b")
        )

        # Track stats
        stats["track_a_genes"] = int(self._centrality["track_a"].sum()) if self._centrality is not None else 0
        stats["track_b_genes"] = int(self._centrality["track_b"].sum()) if self._centrality is not None else 0

        # Genes with tissue expression
        stats["genes_with_tissue_expression"] = sum(
            1 for _, d in g.nodes(data=True)
            if d.get("node_type") in ("gene/protein", "protein")
        )

        # Largest connected component
        if g.number_of_nodes() > 0:
            largest_cc = max(nx.weakly_connected_components(g), key=len)
            stats["largest_cc_size"] = len(largest_cc)
        else:
            stats["largest_cc_size"] = 0

        return stats

    def save_centrality(self, path: Optional[Path] = None):
        if self._centrality is not None:
            path = path or OUTPUT_CENTRALITY
            self._centrality.to_csv(path, index=False)
            logger.info(f"Centrality saved to {path}")

    def save_statistics(self, path: Optional[Path] = None):
        path = path or OUTPUT_STATS
        stats = self.get_graph_statistics()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)
        logger.info(f"Statistics saved to {path}")
