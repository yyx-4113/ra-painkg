"""GTEx tissue expression cross-filtering for pain-relevant tissues.

Filters gene nodes to retain only those with detectable expression (TPM > 1)
in tissue types relevant to pain signaling:
- Track A (inflammation): synovium, whole blood, spleen
- Track B (nociception): DRG (proxied by spinal cord), nerve (tibial)
"""

import gzip
import logging
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Set, Optional

from .config import (
    GTEX_TPM, GTEX_TISSUE_COLUMNS, TISSUE_MAP_TRACK_A, TISSUE_MAP_TRACK_B,
    OUTPUT_GTEX_EXPR
)

logger = logging.getLogger(__name__)


class GTExFilter:
    """Filter genes by tissue-specific expression from GTEx data."""

    # GTEx column -> normalized tissue label
    TISSUE_MAP = GTEX_TISSUE_COLUMNS
    TRACK_A_TISSUES = TISSUE_MAP_TRACK_A
    TRACK_B_TISSUES = TISSUE_MAP_TRACK_B

    def __init__(self, gct_path: Optional[Path] = None):
        self.gct_path = gct_path or GTEX_TPM
        self._df: Optional[pd.DataFrame] = None
        self._gene_expr: Dict[str, Dict[str, float]] = {}

    def load(self) -> pd.DataFrame:
        """Load GTEx median TPM data from GCT format."""
        if not self.gct_path.exists():
            raise FileNotFoundError(f"GTEx file not found: {self.gct_path}")

        logger.info(f"Loading GTEx data from {self.gct_path}...")

        # Parse GCT format (tab-separated, header lines followed by data)
        open_func = gzip.open if self.gct_path.suffix == ".gz" else open
        with open_func(self.gct_path, "rt") as f:
            # Skip version line
            version = f.readline().strip()
            # Read dimensions
            dims = f.readline().strip().split("\t")
            n_rows, n_cols = int(dims[0]), int(dims[1])
            # Read header
            header = f.readline().strip().split("\t")

        # Read data
        self._df = pd.read_csv(
            self.gct_path,
            sep="\t",
            skiprows=2,
            compression="gzip" if self.gct_path.suffix == ".gz" else None,
        )
        self._df.columns = header

        # Set index to gene symbol or Ensembl ID
        if "Description" in self._df.columns:
            self._df = self._df.set_index("Description")
        else:
            self._df = self._df.set_index(self._df.columns[0])

        # Drop non-numeric columns (Name, etc.)
        numeric_cols = self._df.select_dtypes(include=[np.number]).columns
        self._df = self._df[numeric_cols]

        logger.info(f"Loaded GTEx: {self._df.shape[0]} genes x {self._df.shape[1]} tissues")

        # Build gene expression lookup
        for gene in self._df.index:
            self._gene_expr[gene] = {}
            for col in self._df.columns:
                self._gene_expr[gene][col] = float(self._df.loc[gene, col])

        return self._df

    @property
    def df(self) -> pd.DataFrame:
        if self._df is None:
            self.load()
        return self._df

    def get_expression(self, gene: str, tissue: str) -> float:
        """Get median TPM for a gene in a tissue."""
        if not self._gene_expr:
            self.load()
        gene_upper = gene.upper()
        for stored_gene in self._gene_expr:
            if stored_gene.upper() == gene_upper:
                tissue_data = self._gene_expr[stored_gene]
                # Try exact match first
                if tissue in tissue_data:
                    return tissue_data[tissue]
                # Try partial match
                for t, v in tissue_data.items():
                    if tissue.lower() in t.lower():
                        return v
                return 0.0
        return 0.0

    def get_max_track_expression(
        self, gene: str, track: str = "A"
    ) -> float:
        """Get maximum TPM across a track's tissue set."""
        tissues = self.TRACK_A_TISSUES if track == "A" else self.TRACK_B_TISSUES
        max_tpm = 0.0
        for tissue_code in tissues:
            # Map tissue code to GTEx column
            for gtex_col, mapped in self.TISSUE_MAP.items():
                if mapped == tissue_code:
                    tpm = self.get_expression(gene, gtex_col)
                    max_tpm = max(max_tpm, tpm)
        return max_tpm

    def filter_genes_by_tissue(
        self,
        genes: List[str],
        track: str = "A",
        min_tpm: float = 1.0,
    ) -> Set[str]:
        """Filter genes by minimum expression in track-specific tissues.

        Parameters
        ----------
        genes : list of str
            Gene symbols to filter
        track : str
            "A" for inflammation tissues, "B" for nociception tissues
        min_tpm : float
            Minimum TPM threshold

        Returns
        -------
        Set of gene symbols passing the expression filter
        """
        passing = set()
        for gene in genes:
            max_tpm = self.get_max_track_expression(gene, track)
            if max_tpm >= min_tpm:
                passing.add(gene)

        logger.info(
            f"Track {track}: {len(passing)}/{len(genes)} genes pass "
            f"TPM >= {min_tpm} filter"
        )
        return passing

    def build_expression_matrix(
        self, genes: List[str], tissues: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """Build a gene x tissue expression matrix."""
        if tissues is None:
            tissues = list(self.TISSUE_MAP.keys())

        rows = []
        for gene in genes:
            row = {"gene_symbol": gene}
            for gtex_col, tissue_label in self.TISSUE_MAP.items():
                tpm = self.get_expression(gene, gtex_col)
                row[tissue_label] = tpm
            rows.append(row)

        df = pd.DataFrame(rows)
        return df.set_index("gene_symbol")

    def save_expression_data(
        self, df: pd.DataFrame, path: Optional[Path] = None
    ):
        """Save expression matrix to CSV."""
        path = path or OUTPUT_GTEX_EXPR
        df.to_csv(path)
        logger.info(f"GTEx expression data saved to {path}")
