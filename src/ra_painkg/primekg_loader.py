"""Load and query the PrimeKG knowledge graph dataset."""

import zipfile
import pandas as pd
import networkx as nx
from pathlib import Path
from typing import Optional, Dict, List, Set, Tuple
import logging

from .config import PRIMEKG_CSV, PRIMEKG_ZIP, DATA_DIR

logger = logging.getLogger(__name__)


class PrimeKGLoader:
    """Load and manage PrimeKG knowledge graph data."""

    def __init__(self, csv_path: Optional[Path] = None):
        self.csv_path = csv_path or PRIMEKG_CSV
        self._df: Optional[pd.DataFrame] = None
        self._graph: Optional[nx.DiGraph] = None
        self._node_index: Dict[str, int] = {}
        self._index_node: Dict[int, str] = {}

    def extract_zip(self, zip_path: Optional[Path] = None) -> Path:
        """Extract PrimeKG zip archive to data directory."""
        zip_path = zip_path or PRIMEKG_ZIP
        if not zip_path.exists():
            raise FileNotFoundError(f"PrimeKG zip not found: {zip_path}")

        logger.info(f"Extracting {zip_path}...")
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(DATA_DIR)
        logger.info(f"Extraction complete. CSV at {self.csv_path}")
        return self.csv_path

    def load(self, chunksize: int = 1_000_000) -> pd.DataFrame:
        """Load PrimeKG CSV into memory.

        Uses chunked reading for the ~1GB CSV file.
        """
        if not self.csv_path.exists():
            raise FileNotFoundError(
                f"PrimeKG CSV not found: {self.csv_path}. "
                f"Run extract_zip() first if you have the .zip file."
            )

        logger.info(f"Loading PrimeKG from {self.csv_path}...")
        chunks = []
        total_rows = 0

        for chunk in pd.read_csv(self.csv_path, chunksize=chunksize, low_memory=False):
            chunks.append(chunk)
            total_rows += len(chunk)
            logger.debug(f"  Loaded {total_rows:,} rows...")

        self._df = pd.concat(chunks, ignore_index=True)
        logger.info(f"Loaded {len(self._df):,} edges from PrimeKG")

        # Build node index
        all_nodes = set(self._df["x_id"].unique()) | set(self._df["y_id"].unique())
        for i, node_id in enumerate(sorted(all_nodes)):
            self._node_index[str(node_id)] = i
            self._index_node[i] = str(node_id)

        return self._df

    @property
    def df(self) -> pd.DataFrame:
        if self._df is None:
            self.load()
        return self._df

    def query_nodes_by_type(
        self, node_type: str, column: str = "x_type"
    ) -> Set[str]:
        """Get all node IDs of a given type."""
        x_nodes = set(self.df[self.df["x_type"] == node_type]["x_id"].astype(str))
        y_nodes = set(self.df[self.df["y_type"] == node_type]["y_id"].astype(str))
        return x_nodes | y_nodes

    def query_nodes_by_name_keyword(
        self, keyword: str, name_col: str = "x_name", case_sensitive: bool = False
    ) -> pd.DataFrame:
        """Find nodes whose name contains a keyword."""
        df = self.df
        if case_sensitive:
            mask_x = df["x_name"].str.contains(keyword, na=False)
            mask_y = df["y_name"].str.contains(keyword, na=False)
        else:
            mask_x = df["x_name"].str.lower().str.contains(keyword.lower(), na=False)
            mask_y = df["y_name"].str.lower().str.contains(keyword.lower(), na=False)
        return df[mask_x | mask_y]

    def get_subgraph_by_relation(
        self, relation: str
    ) -> nx.DiGraph:
        """Extract subgraph containing all edges of a given relation type."""
        sub = self.df[self.df["relation"] == relation]
        g = nx.DiGraph()
        for _, row in sub.iterrows():
            g.add_edge(
                str(row["x_id"]), str(row["y_id"]),
                relation=row["relation"],
                x_name=row.get("x_name", ""),
                y_name=row.get("y_name", ""),
                x_type=row.get("x_type", ""),
                y_type=row.get("y_type", ""),
            )
        return g

    def build_full_digraph(self) -> nx.DiGraph:
        """Build the complete PrimeKG as a NetworkX directed graph."""
        if self._graph is not None:
            return self._graph

        logger.info("Building full PrimeKG DiGraph...")
        g = nx.DiGraph()
        for _, row in self.df.iterrows():
            g.add_edge(
                str(row["x_id"]), str(row["y_id"]),
                relation=row.get("relation", ""),
                x_type=row.get("x_type", ""),
                y_type=row.get("y_type", ""),
            )

        # Add node attributes
        node_info = {}
        for _, row in self.df.iterrows():
            x_id = str(row["x_id"])
            if x_id not in node_info:
                node_info[x_id] = {
                    "node_name": row.get("x_name", ""),
                    "node_type": row.get("x_type", ""),
                    "node_source": row.get("x_source", ""),
                }
            y_id = str(row["y_id"])
            if y_id not in node_info:
                node_info[y_id] = {
                    "node_name": row.get("y_name", ""),
                    "node_type": row.get("y_type", ""),
                    "node_source": row.get("y_source", ""),
                }

        nx.set_node_attributes(g, node_info)
        self._graph = g
        logger.info(
            f"Built DiGraph: {g.number_of_nodes():,} nodes, "
            f"{g.number_of_edges():,} edges"
        )
        return g

    def get_node_type_distribution(self) -> Dict[str, int]:
        """Count nodes by type."""
        type_counts = {}
        for node, data in self.build_full_digraph().nodes(data=True):
            nt = data.get("node_type", "unknown")
            type_counts[nt] = type_counts.get(nt, 0) + 1
        return dict(sorted(type_counts.items(), key=lambda x: -x[1]))

    def get_relation_distribution(self) -> Dict[str, int]:
        """Count edges by relation type."""
        rel_counts = {}
        for _, _, data in self.build_full_digraph().edges(data=True):
            rel = data.get("relation", "unknown")
            rel_counts[rel] = rel_counts.get(rel, 0) + 1
        return dict(sorted(rel_counts.items(), key=lambda x: -x[1]))
