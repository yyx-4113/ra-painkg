"""KG Converter: RA-PainKG / STRING / GO to GEARS-compatible adjacency matrix."""

import logging
import numpy as np
import networkx as nx
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Set
from scipy.sparse import csr_matrix

logger = logging.getLogger(__name__)


class KGToAdjacency:
    """Convert knowledge graphs to GEARS-compatible adjacency matrices."""

    def __init__(self, gene_vocabulary=None):
        self.gene_vocab = gene_vocabulary
        self.gene_to_idx = {}
        if gene_vocabulary:
            self.gene_to_idx = {g.upper(): i for i, g in enumerate(gene_vocabulary)}

    def set_vocabulary(self, gene_list):
        self.gene_vocab = gene_list
        self.gene_to_idx = {g.upper(): i for i, g in enumerate(gene_list)}
        logger.info("Gene vocabulary: %d genes", len(self.gene_to_idx))

    def from_ra_painkg(self, graphml_path, edge_types=None, include_track=None):
        if edge_types is None:
            edge_types = ["protein_protein"]
        logger.info("Loading RA-PainKG from %s", graphml_path)
        g = nx.read_graphml(str(graphml_path))
        gene_nodes = {
            n for n, d in g.nodes(data=True)
            if d.get("node_type") in ("gene/protein", "protein")
        }
        if include_track:
            if include_track == "A":
                gene_nodes = {n for n in gene_nodes if g.nodes[n].get("track_a")}
            elif include_track == "B":
                gene_nodes = {n for n in gene_nodes if g.nodes[n].get("track_b")}
            elif include_track == "dual":
                gene_nodes = {n for n in gene_nodes
                              if g.nodes[n].get("track_a") and g.nodes[n].get("track_b")}
        n_vocab = len(self.gene_vocab)
        adj = np.zeros((n_vocab, n_vocab), dtype=np.float32)
        kg_map = {}
        for node in gene_nodes:
            name = str(g.nodes[node].get("node_name", "")).upper()
            if name in self.gene_to_idx:
                kg_map[node] = name
        logger.info("  KG genes: %d, matched to vocab: %d", len(gene_nodes), len(kg_map))
        ec = 0
        for u, v, data in g.edges(data=True):
            if data.get("relation", "") not in edge_types:
                continue
            if u in kg_map and v in kg_map:
                i = self.gene_to_idx[kg_map[u]]
                j = self.gene_to_idx[kg_map[v]]
                adj[i, j] = 1.0
                adj[j, i] = 1.0
                ec += 1
        logger.info("  Edges: %d, density: %.6f", ec, adj.sum() / (n_vocab * n_vocab))
        return csr_matrix(adj)

    def from_combined(self, graphml_path):
        logger.info("Building combined multi-relation adjacency from %s", graphml_path)
        g = nx.read_graphml(str(graphml_path))
        n_vocab = len(self.gene_vocab)
        weights = {
            "protein_protein": 1.0,
            "pathway_protein": 0.5,
            "bioprocess_protein": 0.3,
            "drug_protein": 0.0,
        }
        adj = np.zeros((n_vocab, n_vocab), dtype=np.float32)
        kg_map = {}
        for node, data in g.nodes(data=True):
            if data.get("node_type") in ("gene/protein", "protein"):
                name = str(data.get("node_name", "")).upper()
                if name in self.gene_to_idx:
                    kg_map[node] = name
        for u, v, data in g.edges(data=True):
            w = weights.get(data.get("relation", ""), 0.0)
            if w == 0.0:
                continue
            if u in kg_map and v in kg_map:
                i = self.gene_to_idx[kg_map[u]]
                j = self.gene_to_idx[kg_map[v]]
                adj[i, j] = max(adj[i, j], w)
                adj[j, i] = max(adj[j, i], w)
        logger.info("  Combined adjacency: %d edges", int((adj > 0).sum() / 2))
        return csr_matrix(adj)

    def from_go_bp(self, gene_go_annotations=None):
        n_vocab = len(self.gene_vocab)
        if gene_go_annotations and Path(gene_go_annotations).exists():
            go_df = pd.read_csv(gene_go_annotations, sep="\t")
            gene_to_gos = {}
            for _, row in go_df.iterrows():
                gene = str(row.get("gene", row.get("symbol", ""))).upper()
                go_term = str(row.get("go_id", row.get("GO", "")))
                if gene in self.gene_to_idx and go_term:
                    gene_to_gos.setdefault(gene, set()).add(go_term)
            adj = np.zeros((n_vocab, n_vocab), dtype=np.float32)
            genes_list = list(gene_to_gos.keys())
            for a in range(len(genes_list)):
                for b in range(a + 1, len(genes_list)):
                    if gene_to_gos[genes_list[a]] & gene_to_gos[genes_list[b]]:
                        i = self.gene_to_idx[genes_list[a]]
                        j = self.gene_to_idx[genes_list[b]]
                        adj[i, j] = adj[j, i] = 1.0
            logger.info("  GO BP edges: %d", int(adj.sum() / 2))
            return csr_matrix(adj)
        logger.warning("No GO annotations provided. Using identity adjacency.")
        return csr_matrix(np.eye(n_vocab, dtype=np.float32))


class KGComparer:
    """Compare multiple KG adjacency matrices."""

    def __init__(self):
        self.adjs = {}

    def add(self, name, adj):
        self.adjs[name] = adj

    def compute_overlap(self, kg_a, kg_b):
        a = self.adjs[kg_a].toarray()
        b = self.adjs[kg_b].toarray()
        ae = set(zip(*np.where(a > 0)))
        be = set(zip(*np.where(b > 0)))
        na = len(ae) // 2
        nb = len(be) // 2
        inter = len(ae & be) // 2
        union = len(ae | be) // 2
        return {
            "kg_a": kg_a, "kg_b": kg_b,
            "edges_a": na, "edges_b": nb,
            "intersection": inter, "union": union,
            "jaccard": inter / union if union else 0,
        }

    def summary_table(self):
        rows = []
        for name, adj in self.adjs.items():
            arr = adj.toarray()
            e = int((arr > 0).sum() / 2)
            d = e / (arr.shape[0] ** 2) if arr.shape[0] else 0
            rows.append({
                "KG": name,
                "Genes": arr.shape[0],
                "Edges": e,
                "Density": round(d, 6),
                "Mean_degree": round(2 * e / arr.shape[0], 1) if arr.shape[0] else 0,
            })
        return pd.DataFrame(rows)
