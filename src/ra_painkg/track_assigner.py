"""Dual-track assignment: classify genes into inflammatory (A) vs nociceptive (B).

Track A (免疫-炎症): genes involved in RA synovial inflammation
Track B (伤害感受-疼痛传导): genes involved in peripheral and central pain signaling
"""

import logging
import pandas as pd
from pathlib import Path
from typing import Dict, List, Set, Optional

from .config import OUTPUT_TRACK_ASSIGNMENTS, CORE_PAIN_GENES

logger = logging.getLogger(__name__)


class TrackAssigner:
    """Assign pain genes to Track A (inflammation) and/or Track B (nociception)."""

    # Track A: inflammation-focused categories
    TRACK_A_CATEGORIES = {
        "inflammatory_cytokines",
        "cytokine_receptors",
        "jak_stat",
        "nfkb",
        "complement",
        "prostaglandin",
        "ra_specific",
    }

    # Track B: nociception-focused categories
    TRACK_B_CATEGORIES = {
        "nociceptor_transduction",
        "voltage_gated_sodium",
        "voltage_gated_calcium",
        "neuropeptide_signaling",
        "neurotrophin_signaling",
        "opioid_system",
        "gaba_glycine",
        "serotonin",
        "endocannabinoid",
    }

    # Categories that span both tracks
    DUAL_CATEGORIES = {
        "mapk_signaling",
        "kinase_signaling",
        "transcription_factors",
        "anesthetic_targets",
    }

    # Manual overrides for genes that belong in specific tracks
    MANUAL_TRACK_A = {
        # Genes primarily involved in inflammation
        "PADI4", "PTPN22", "HLA-DRB1", "MMP1", "MMP3", "MMP9",
        "CD80", "CD86", "CD28", "CTLA4", "IL23R", "IL17A", "IL17F",
        "TNFSF11", "CSF1", "CCL2", "CCL5", "CXCL8",
    }

    MANUAL_TRACK_B = {
        # Genes primarily involved in nociception
        "TRPV1", "TRPA1", "TRPM3", "TRPM8",
        "SCN9A", "SCN10A", "SCN11A",
        "OPRM1", "OPRD1", "OPRK1",
        "PENK", "PDYN", "POMC",
        "TAC1", "CALCA", "CALCB",
        "GABRA1", "GABRA2", "GABRG2",
        "GLRA1", "GLRB",
        "HTR1A", "HTR2A", "HTR3A",
        "CNR1", "CNR2", "FAAH",
    }

    def __init__(self):
        self.assignments: Dict[str, Dict[str, bool]] = {}

    def _get_category(self, gene: str) -> Optional[str]:
        """Find which category a gene belongs to."""
        gene_upper = gene.upper()
        for cat, genes in CORE_PAIN_GENES.items():
            if gene_upper in {g.upper() for g in genes}:
                return cat
        return None

    def assign(self, genes: List[str]) -> pd.DataFrame:
        """Assign each gene to Track A, Track B, or both.

        Returns DataFrame with columns: gene, track_a_inflammation, track_b_nociception
        """
        rows = []
        for gene in genes:
            cat = self._get_category(gene)
            gene_upper = gene.upper()

            # Manual overrides take precedence
            if gene_upper in {g.upper() for g in self.MANUAL_TRACK_A}:
                track_a, track_b = True, False
            elif gene_upper in {g.upper() for g in self.MANUAL_TRACK_B}:
                track_a, track_b = False, True
            elif cat is None:
                track_a, track_b = False, False
            elif cat in self.TRACK_A_CATEGORIES:
                track_a, track_b = True, False
            elif cat in self.TRACK_B_CATEGORIES:
                track_a, track_b = False, True
            elif cat in self.DUAL_CATEGORIES:
                track_a, track_b = True, True
            else:
                track_a, track_b = False, False

            self.assignments[gene] = {
                "track_a_inflammation": track_a,
                "track_b_nociception": track_b,
            }
            rows.append({
                "gene": gene,
                "track_a_inflammation": track_a,
                "track_b_nociception": track_b,
            })

        df = pd.DataFrame(rows)
        n_a = df["track_a_inflammation"].sum()
        n_b = df["track_b_nociception"].sum()
        n_both = ((df["track_a_inflammation"]) & (df["track_b_nociception"])).sum()
        logger.info(f"Track assignments: A={n_a}, B={n_b}, Dual={n_both}")
        return df

    def save(self, df: pd.DataFrame, path: Optional[Path] = None):
        path = path or OUTPUT_TRACK_ASSIGNMENTS
        df.to_csv(path, index=False)
        logger.info(f"Track assignments saved to {path}")
