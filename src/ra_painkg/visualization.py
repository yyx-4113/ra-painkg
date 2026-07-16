"""Visualization module for RA-PainKG.

Generates publication-quality figures:
- fig1: Top hub nodes by betweenness centrality
- fig2: Degree distribution
- fig3: Track A vs Track B comparison
- fig4: Graph composition (node types, edge relations)
- fig5: Core pain signaling network
- fig6: Pathway subnetworks
"""

import logging
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Tuple

from .config import OUTPUT_DIR

logger = logging.getLogger(__name__)

# Consistent styling
plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
})

COLORS = {
    "track_a": "#E74C3C",       # Red for inflammation
    "track_b": "#3498DB",       # Blue for nociception
    "dual": "#9B59B6",          # Purple for dual
    "other": "#95A5A6",         # Gray for other
    "gene": "#2ECC71",          # Green for gene nodes
    "non_gene": "#BDC3C7",      # Light gray
}


class Visualizer:
    """Generate figures for RA-PainKG publication."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or (OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def fig_top_hubs(
        self,
        analyzer,
        metric: str = "betweenness",
        n: int = 15,
        save: bool = True,
    ):
        """Figure 1: Top hub nodes by centrality metric."""
        top = analyzer.get_top_hubs(metric=metric, n=n)
        top = top.iloc[::-1]  # Reverse for horizontal bar

        fig, ax = plt.subplots(figsize=(10, 6))

        colors = []
        for _, row in top.iterrows():
            if row["track_a"] and row["track_b"]:
                colors.append(COLORS["dual"])
            elif row["track_a"]:
                colors.append(COLORS["track_a"])
            elif row["track_b"]:
                colors.append(COLORS["track_b"])
            else:
                colors.append(COLORS["other"])

        ax.barh(range(len(top)), top[metric], color=colors, edgecolor="white", linewidth=0.5)
        ax.set_yticks(range(len(top)))
        ax.set_yticklabels(top["node_name"], fontsize=9)
        ax.set_xlabel(f"{metric.capitalize()} Centrality")
        ax.set_title(f"Top {n} Hub Nodes by {metric.capitalize()} Centrality")

        # Legend
        legend_patches = [
            mpatches.Patch(color=COLORS["track_a"], label="Track A (Inflammation)"),
            mpatches.Patch(color=COLORS["track_b"], label="Track B (Nociception)"),
            mpatches.Patch(color=COLORS["dual"], label="Dual Track"),
        ]
        ax.legend(handles=legend_patches, loc="lower right", fontsize=8)

        plt.tight_layout()
        if save:
            for fmt in ["pdf", "png"]:
                path = self.output_dir / f"fig1_top_hubs_{metric}.{fmt}"
                fig.savefig(path)
                logger.info(f"Saved {path}")
        plt.close(fig)

    def fig_degree_distribution(
        self,
        graph: nx.DiGraph,
        save: bool = True,
    ):
        """Figure 2: Degree distribution (log-log)."""
        degrees = [d for _, d in graph.degree()]
        degree_counts = pd.Series(degrees).value_counts().sort_index()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Linear scale
        ax1.hist(degrees, bins=50, color=COLORS["other"], edgecolor="white", alpha=0.8)
        ax1.set_xlabel("Degree")
        ax1.set_ylabel("Frequency")
        ax1.set_title("Degree Distribution (Linear)")

        # Log-log scale
        x = degree_counts.index.values
        y = degree_counts.values
        ax2.scatter(x, y, s=10, alpha=0.6, color=COLORS["gene"])
        ax2.set_xscale("log")
        ax2.set_yscale("log")
        ax2.set_xlabel("Degree (log)")
        ax2.set_ylabel("Frequency (log)")
        ax2.set_title("Degree Distribution (Log-Log)")

        # Fit power law
        mask = (x > 0) & (y > 0)
        if mask.sum() > 3:
            coeffs = np.polyfit(np.log10(x[mask]), np.log10(y[mask]), 1)
            x_fit = np.logspace(0, np.log10(max(x)), 50)
            y_fit = 10 ** (coeffs[1]) * x_fit ** coeffs[0]
            ax2.plot(x_fit, y_fit, "r--", linewidth=1.5,
                     label=f"Power-law: = {abs(coeffs[0]):.2f}")
            ax2.legend(fontsize=8)

        plt.tight_layout()
        if save:
            for fmt in ["pdf", "png"]:
                path = self.output_dir / f"fig2_degree_distribution.{fmt}"
                fig.savefig(path)
        plt.close(fig)

    def fig_track_comparison(
        self,
        analyzer,
        save: bool = True,
    ):
        """Figure 3: Track A vs Track B network topology comparison."""
        if analyzer._centrality is None:
            analyzer.compute_centrality()

        df = analyzer._centrality
        track_a = df[df["track_a"]]
        track_b = df[df["track_b"]]

        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        metrics = [
            ("degree", "Degree Centrality"),
            ("betweenness", "Betweenness Centrality"),
            ("pagerank", "PageRank"),
            ("closeness", "Closeness Centrality"),
        ]

        for (metric, title), ax in zip(metrics, axes.flat):
            a_vals = track_a[metric].dropna()
            b_vals = track_b[metric].dropna()

            if len(a_vals) > 0 and len(b_vals) > 0:
                # Violin plot
                positions = [1, 2]
                parts = ax.violinplot(
                    [a_vals, b_vals],
                    positions=positions,
                    showmeans=True,
                    showmedians=True,
                )
                for pc, color in zip(parts["bodies"], [COLORS["track_a"], COLORS["track_b"]]):
                    pc.set_facecolor(color)
                    pc.set_alpha(0.6)

                ax.set_xticks(positions)
                ax.set_xticklabels(["Track A\n(Inflammation)", "Track B\n(Nociception)"])
                ax.set_ylabel(metric.capitalize())
                ax.set_title(title)

                # Add p-value annotation
                from scipy import stats as scipy_stats
                try:
                    stat, pval = scipy_stats.mannwhitneyu(a_vals, b_vals)
                    ax.annotate(
                        f"MWU p={pval:.2e}",
                        xy=(0.5, 0.95),
                        xycoords="axes fraction",
                        ha="center",
                        fontsize=8,
                    )
                except Exception:
                    pass

        fig.suptitle("Track A vs Track B: Network Topology Comparison", fontsize=14, y=1.01)
        plt.tight_layout()
        if save:
            for fmt in ["pdf", "png"]:
                path = self.output_dir / f"fig3_track_comparison.{fmt}"
                fig.savefig(path)
        plt.close(fig)

    def fig_graph_composition(
        self,
        graph: nx.DiGraph,
        save: bool = True,
    ):
        """Figure 4: Graph composition - node types and edge relations."""
        node_types = {}
        edge_rels = {}

        for _, data in graph.nodes(data=True):
            nt = data.get("node_type", "unknown")
            node_types[nt] = node_types.get(nt, 0) + 1

        for _, _, data in graph.edges(data=True):
            rel = data.get("relation", "unknown")
            edge_rels[rel] = edge_rels.get(rel, 0) + 1

        # Sort and take top categories
        node_types = dict(sorted(node_types.items(), key=lambda x: -x[1])[:10])
        edge_rels = dict(sorted(edge_rels.items(), key=lambda x: -x[1])[:10])

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Node types pie
        colors_nt = plt.cm.Set3(np.linspace(0, 1, len(node_types)))
        wedges, texts, autotexts = ax1.pie(
            node_types.values(),
            labels=None,
            autopct="%1.1f%%",
            colors=colors_nt,
            pctdistance=0.75,
        )
        ax1.set_title(f"Node Types (n={graph.number_of_nodes():,})")
        ax1.legend(
            wedges,
            [f"{k.replace('_', ' ')} ({v:,})" for k, v in node_types.items()],
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            fontsize=7,
        )

        # Edge relations horizontal bar
        labels = list(edge_rels.keys())
        values = list(edge_rels.values())
        colors_er = plt.cm.viridis(np.linspace(0.2, 0.9, len(labels)))

        ax2.barh(range(len(labels)), values, color=colors_er, edgecolor="white")
        ax2.set_yticks(range(len(labels)))
        ax2.set_yticklabels([l.replace("_", " ") for l in labels], fontsize=8)
        ax2.set_xlabel("Count")
        ax2.set_title(f"Edge Relations (n={graph.number_of_edges():,})")
        ax2.invert_yaxis()

        plt.tight_layout()
        if save:
            for fmt in ["pdf", "png"]:
                path = self.output_dir / f"fig4_graph_composition.{fmt}"
                fig.savefig(path)
        plt.close(fig)

    def fig_core_network(
        self,
        graph: nx.DiGraph,
        top_n: int = 50,
        save: bool = True,
    ):
        """Figure 5: Core pain signaling network visualization."""
        # Select top hub nodes
        if hasattr(graph, "nodes"):
            bc = nx.betweenness_centrality(graph, k=min(200, graph.number_of_nodes()))
            top_nodes = sorted(bc, key=bc.get, reverse=True)[:top_n]
            sub = graph.subgraph(top_nodes).copy()
        else:
            sub = graph

        fig, ax = plt.subplots(figsize=(16, 14))

        # Layout
        pos = nx.spring_layout(sub, k=2, iterations=50, seed=42)

        # Node colors
        node_colors = []
        node_sizes = []
        for node in sub.nodes():
            data = sub.nodes[node]
            if data.get("track_a") and data.get("track_b"):
                node_colors.append(COLORS["dual"])
            elif data.get("track_a"):
                node_colors.append(COLORS["track_a"])
            elif data.get("track_b"):
                node_colors.append(COLORS["track_b"])
            else:
                node_colors.append(COLORS["other"])

            # Size by degree
            deg = sub.degree(node)
            node_sizes.append(max(20, min(300, deg * 5)))

        # Draw
        nx.draw_networkx_edges(
            sub, pos, alpha=0.15, edge_color="#888888",
            arrows=True, arrowsize=5, ax=ax,
        )
        nx.draw_networkx_nodes(
            sub, pos,
            node_color=node_colors,
            node_size=node_sizes,
            alpha=0.85,
            edgecolors="white",
            linewidths=0.5,
            ax=ax,
        )

        # Label top hubs only
        top_10 = sorted(bc, key=bc.get, reverse=True)[:10]
        labels = {n: sub.nodes[n].get("node_name", n) for n in top_10 if n in sub.nodes()}
        nx.draw_networkx_labels(sub, pos, labels, font_size=8, ax=ax)

        # Legend
        legend_patches = [
            mpatches.Patch(color=COLORS["track_a"], label="Track A (Inflammation)"),
            mpatches.Patch(color=COLORS["track_b"], label="Track B (Nociception)"),
            mpatches.Patch(color=COLORS["dual"], label="Dual Track"),
        ]
        ax.legend(handles=legend_patches, loc="upper right", fontsize=10)

        ax.set_title("RA-PainKG Core Signaling Network", fontsize=14)
        ax.axis("off")
        plt.tight_layout()
        if save:
            for fmt in ["pdf", "png"]:
                path = self.output_dir / f"fig5_core_network.{fmt}"
                fig.savefig(path)
        plt.close(fig)

    def fig_pathway_subnetworks(
        self,
        graph: nx.DiGraph,
        pathways: List[Dict],
        save: bool = True,
    ):
        """Figure 6: Pathway subnetworks grid."""
        n_pathways = min(len(pathways), 6)
        n_cols = 3
        n_rows = (n_pathways + n_cols - 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
        if n_rows == 1:
            axes = axes.reshape(1, -1)

        for idx, (pathway, ax) in enumerate(zip(pathways[:n_pathways], axes.flat)):
            # Extract pathway genes and their subgraph
            pathway_genes = set()
            for g in pathway["key_genes"].split(", "):
                pathway_genes.add(g.strip().upper())

            # Find matching nodes
            pathway_nodes = set()
            for node, data in graph.nodes(data=True):
                node_name = str(data.get("node_name", "")).upper()
                if node_name in pathway_genes:
                    pathway_nodes.add(node)

            if len(pathway_nodes) < 2:
                ax.text(0.5, 0.5, "Insufficient nodes",
                        ha="center", va="center", transform=ax.transAxes)
                ax.set_title(pathway["name"][:40], fontsize=9)
                ax.axis("off")
                continue

            sub = graph.subgraph(pathway_nodes).copy()
            pos = nx.spring_layout(sub, k=1.5, seed=42)

            node_colors = []
            for node in sub.nodes():
                data = sub.nodes[node]
                if data.get("track_a") and data.get("track_b"):
                    node_colors.append(COLORS["dual"])
                elif data.get("track_a"):
                    node_colors.append(COLORS["track_a"])
                elif data.get("track_b"):
                    node_colors.append(COLORS["track_b"])
                else:
                    node_colors.append(COLORS["gene"])

            nx.draw_networkx(
                sub, pos, ax=ax,
                node_color=node_colors,
                node_size=200,
                edge_color="#cccccc",
                arrows=True,
                arrowsize=6,
                font_size=7,
                labels={n: sub.nodes[n].get("node_name", n) for n in sub.nodes()},
            )
            ax.set_title(pathway["name"], fontsize=9)
            ax.axis("off")

        # Hide unused subplots
        for ax in axes.flat[n_pathways:]:
            ax.axis("off")

        fig.suptitle("Pain Signaling Pathway Subnetworks", fontsize=14, y=1.01)
        plt.tight_layout()
        if save:
            for fmt in ["pdf", "png"]:
                path = self.output_dir / f"fig6_pathway_subnetworks.{fmt}"
                fig.savefig(path)
        plt.close(fig)

    def generate_all(
        self,
        analyzer,
        graph: nx.DiGraph,
        pathways: Optional[List[Dict]] = None,
    ):
        """Generate all six figures."""
        logger.info("Generating all figures...")
        self.fig_top_hubs(analyzer, metric="betweenness", save=True)
        self.fig_degree_distribution(graph, save=True)
        self.fig_track_comparison(analyzer, save=True)
        self.fig_graph_composition(graph, save=True)
        self.fig_core_network(graph, save=True)
        if pathways:
            self.fig_pathway_subnetworks(graph, pathways, save=True)
        logger.info("All figures generated")
