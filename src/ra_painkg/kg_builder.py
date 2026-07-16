"""Knowledge graph construction: from seed nodes to expanded RA-PainKG.

Builds a directed knowledge graph by:
1. Extracting seed node neighborhoods from PrimeKG
2. Expanding via multi-hop walks
3. Applying tissue-specific expression filtering
4. Assigning dual-track (inflammation/nociception) labels
5. Computing subgraphs for Track A, Track B, and gene-only views
"""

import logging
import pickle
import json
import networkx as nx
import pandas as pd
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple

from .primekg_loader import PrimeKGLoader
from .seed_nodes import SeedNodeFinder
from .gtex_filter import GTExFilter
from .track_assigner import TrackAssigner
from .config import (
    OUTPUT_GRAPHML, OUTPUT_PKL, OUTPUT_NODES, OUTPUT_EDGES,
    OUTPUT_FINAL_GRAPHML, OUTPUT_FINAL_PKL,
    OUTPUT_NODES_FINAL, OUTPUT_EDGES_FINAL,
    OUTPUT_TRACK_A, OUTPUT_TRACK_B, OUTPUT_GENES_ONLY,
    OUTPUT_SEED_NODES, OUTPUT_SUMMARY,
)

logger = logging.getLogger(__name__)


class KGBuilder:
    """Build and manage the RA-PainKG knowledge graph."""

    def __init__(
        self,
        loader: PrimeKGLoader,
        gtex_filter: Optional[GTExFilter] = None,
    ):
        self.loader = loader
        self.gtex = gtex_filter
        self.graph: Optional[nx.DiGraph] = None
        self.seed_finder: Optional[SeedNodeFinder] = None
        self.track_assigner = TrackAssigner()

    def build_from_seeds(
        self,
        seed_nodes: Dict[str, Set[str]],
        expansion_hops: int = 2,
    ) -> nx.DiGraph:
        """Build knowledge graph by expanding from seed nodes.

        Parameters
        ----------
        seed_nodes : dict
            Mapping of seed category -> set of node IDs
        expansion_hops : int
            Number of neighborhood expansion hops from seed nodes

        Returns
        -------
        NetworkX DiGraph with all nodes and edges within the expansion
        """
        logger.info(f"Building KG with {expansion_hops}-hop expansion...")

        full_graph = self.loader.build_full_digraph()

        # Collect all seed node IDs
        all_seeds = set()
        for category, nodes in seed_nodes.items():
            all_seeds.update(nodes)

        logger.info(f"Total unique seed nodes: {len(all_seeds)}")

        # Multi-hop expansion
        current_nodes = all_seeds & set(full_graph.nodes())
        expanded_nodes = set(current_nodes)

        for hop in range(expansion_hops):
            neighbors = set()
            for node in current_nodes:
                if node in full_graph:
                    neighbors.update(full_graph.successors(node))
                    neighbors.update(full_graph.predecessors(node))
            new_nodes = neighbors - expanded_nodes
            expanded_nodes.update(new_nodes)
            current_nodes = new_nodes
            logger.info(f"  Hop {hop + 1}: +{len(new_nodes)} nodes (total: {len(expanded_nodes)})")

        # Extract subgraph
        valid_nodes = expanded_nodes & set(full_graph.nodes())
        self.graph = full_graph.subgraph(valid_nodes).copy()

        # Assign categories to nodes
        self._categorize_nodes(all_seeds)

        logger.info(
            f"Built KG: {self.graph.number_of_nodes():,} nodes, "
            f"{self.graph.number_of_edges():,} edges"
        )
        return self.graph

    def _categorize_nodes(self, seed_ids: Set[str]):
        """Add category and track attributes to all nodes."""
        if self.graph is None:
            return

        for node in self.graph.nodes():
            data = self.graph.nodes[node]
            node_name = str(data.get("node_name", "")).upper()
            node_type = data.get("node_type", "")

            # Check if seed
            is_seed = str(node) in seed_ids

            # Determine track for gene/protein nodes
            if node_type == "gene/protein" or node_type == "protein":
                track_info = self.track_assigner.assignments.get(
                    node_name, {"track_a_inflammation": False, "track_b_nociception": False}
                )
                track = "dual" if (track_info["track_a_inflammation"] and track_info["track_b_nociception"]) else \
                        "A" if track_info["track_a_inflammation"] else \
                        "B" if track_info["track_b_nociception"] else "none"
            else:
                track_info = {"track_a_inflammation": False, "track_b_nociception": False}
                track = "none"

            self.graph.nodes[node].update({
                "category": "seed" if is_seed else "other",
                "is_seed": is_seed,
                "track": track,
                "track_a": track_info["track_a_inflammation"],
                "track_b": track_info["track_b_nociception"],
            })

    def expand_graph(
        self,
        additional_relations: Optional[List[str]] = None,
        max_additional_edges: int = 50000,
    ) -> nx.DiGraph:
        """Expand the graph by adding additional relations from PrimeKG.

        Adds edges between existing nodes using specified relation types.
        """
        if self.graph is None:
            raise ValueError("Build graph first with build_from_seeds()")

        if additional_relations is None:
            additional_relations = [
                "protein_protein", "drug_protein", "disease_protein",
                "pathway_protein", "bioprocess_protein",
            ]

        existing_nodes = set(self.graph.nodes())
        full_graph = self.loader.build_full_digraph()

        added = 0
        for relation in additional_relations:
            edges_df = self.loader.df[self.loader.df["relation"] == relation]
            for _, row in edges_df.iterrows():
                x_id, y_id = str(row["x_id"]), str(row["y_id"])
                if x_id in existing_nodes and y_id in existing_nodes:
                    if not self.graph.has_edge(x_id, y_id):
                        self.graph.add_edge(
                            x_id, y_id,
                            relation=relation,
                        )
                        added += 1
                        if added >= max_additional_edges:
                            break
            if added >= max_additional_edges:
                break

        logger.info(f"Expanded with {added} additional edges")
        return self.graph

    def filter_by_tissue_expression(
        self,
        track: str = "A",
        min_tpm: float = 1.0,
    ) -> Set[str]:
        """Filter gene nodes by tissue expression in a track."""
        if self.gtex is None:
            logger.warning("GTEx filter not available, skipping tissue filtering")
            return set()

        gene_nodes = {
            node for node, data in self.graph.nodes(data=True)
            if data.get("node_type") in ("gene/protein", "protein")
        }

        gene_names = {
            str(self.graph.nodes[n].get("node_name", ""))
            for n in gene_nodes
        }

        passing = self.gtex.filter_genes_by_tissue(
            list(gene_names), track, min_tpm
        )
        return passing

    def extract_track_subgraph(self, track: str) -> nx.DiGraph:
        """Extract subgraph for a specific track."""
        if self.graph is None:
            raise ValueError("Build graph first")

        if track == "A":
            track_nodes = {
                node for node, data in self.graph.nodes(data=True)
                if data.get("track_a", False) or data.get("track") in ("A", "dual")
            }
        elif track == "B":
            track_nodes = {
                node for node, data in self.graph.nodes(data=True)
                if data.get("track_b", False) or data.get("track") in ("B", "dual")
            }
        else:
            raise ValueError(f"Unknown track: {track}")

        return self.graph.subgraph(track_nodes).copy()

    def extract_genes_only(self) -> nx.DiGraph:
        """Extract gene/protein-only subgraph."""
        if self.graph is None:
            raise ValueError("Build graph first")

        gene_nodes = {
            node for node, data in self.graph.nodes(data=True)
            if data.get("node_type") in ("gene/protein", "protein")
        }
        return self.graph.subgraph(gene_nodes).copy()

    def get_largest_component(self) -> nx.DiGraph:
        """Get the largest weakly connected component."""
        if self.graph is None:
            raise ValueError("Build graph first")
        largest = max(nx.weakly_connected_components(self.graph), key=len)
        return self.graph.subgraph(largest).copy()

    def save_graph(
        self,
        graph: Optional[nx.DiGraph] = None,
        prefix: str = "RA_PainKG",
    ):
        """Save graph in multiple formats: GraphML, Pickle, CSV."""
        g = graph or self.graph
        if g is None:
            return

        output_dir = OUTPUT_GRAPHML.parent
        output_dir.mkdir(parents=True, exist_ok=True)

        # GraphML
        graphml_path = output_dir / f"{prefix}.graphml"
        nx.write_graphml(g, str(graphml_path))
        logger.info(f"Saved GraphML: {graphml_path} ({graphml_path.stat().st_size / 1e6:.1f} MB)")

        # Pickle
        pkl_path = output_dir / f"{prefix}.pkl"
        with open(pkl_path, "wb") as f:
            pickle.dump(g, f)
        logger.info(f"Saved Pickle: {pkl_path} ({pkl_path.stat().st_size / 1e6:.1f} MB)")

        # CSV exports
        nodes_path = output_dir / f"{prefix}_nodes.csv"
        edges_path = output_dir / f"{prefix}_edges.csv"

        nodes_df = pd.DataFrame([
            {"node_index": i, **{k: v for k, v in data.items()}}
            for i, (node, data) in enumerate(g.nodes(data=True))
        ])
        nodes_df.to_csv(nodes_path, index=False)

        edges_df = pd.DataFrame([
            {"source": u, "target": v, **data}
            for u, v, data in g.edges(data=True)
        ])
        edges_df.to_csv(edges_path, index=False)
        logger.info(f"Saved CSV: {nodes_path}, {edges_path}")

    def save_all(self):
        """Save all graph variants."""
        if self.graph is None:
            return

        # Full graph
        self.save_graph(self.graph, "RA_PainKG")

        # Largest component (final)
        largest = self.get_largest_component()
        self.save_graph(largest, "RA_PainKG_final")

        # Track subgraphs
        for track in ["A", "B"]:
            sub = self.extract_track_subgraph(track)
            self.save_graph(sub, f"RA_PainKG_track{track}")

        # Genes only
        genes_only = self.extract_genes_only()
        self.save_graph(genes_only, "RA_PainKG_genes_only")

    def build_summary(self) -> Dict:
        """Generate a JSON summary of the knowledge graph."""
        if self.graph is None:
            return {}

        # Node type distribution
        node_types = {}
        for _, data in self.graph.nodes(data=True):
            nt = data.get("node_type", "unknown")
            node_types[nt] = node_types.get(nt, 0) + 1

        # Edge relation distribution
        edge_rels = {}
        for _, _, data in self.graph.edges(data=True):
            rel = data.get("relation", "unknown")
            edge_rels[rel] = edge_rels.get(rel, 0) + 1

        # Track statistics
        track_a = sum(1 for _, d in self.graph.nodes(data=True) if d.get("track_a"))
        track_b = sum(1 for _, d in self.graph.nodes(data=True) if d.get("track_b"))
        dual = sum(
            1 for _, d in self.graph.nodes(data=True)
            if d.get("track_a") and d.get("track_b")
        )

        # Seed node stats
        seed_stats = {}
        if self.seed_finder:
            for cat, nodes in self.seed_finder.seed_nodes.items():
                seed_stats[cat] = len(nodes)

        summary = {
            "graph_name": "RA-PainKG",
            "version": "1.0",
            "date": "2026-07-15",
            "data_sources": ["PrimeKG", "GTEx v8", "PubMed literature mining"],
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "node_type_distribution": dict(
                sorted(node_types.items(), key=lambda x: -x[1])
            ),
            "edge_relation_distribution": dict(
                sorted(edge_rels.items(), key=lambda x: -x[1])
            ),
            "seed_nodes": seed_stats,
            "track_genes": {
                "track_a_inflammation": track_a,
                "track_b_nociception": track_b,
                "dual_track": dual,
            },
        }
        return summary

    def save_summary(self, summary: Dict, path: Optional[Path] = None):
        path = path or OUTPUT_SUMMARY
        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        logger.info(f"Summary saved to {path}")
