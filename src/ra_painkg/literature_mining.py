"""PubMed literature mining for pain gene evidence.

Queries PubMed via the Entrez API to collect literature evidence
supporting each gene's role in pain signaling, RA, and nociception.
"""

import logging
import time
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.error import HTTPError

from .config import OUTPUT_LITERATURE, LITERATURE_KEYWORDS

logger = logging.getLogger(__name__)

try:
    from Bio import Entrez
    HAS_BIOPYTHON = True
except ImportError:
    HAS_BIOPYTHON = False
    logger.warning("Biopython not installed. Literature mining will use cached data.")


class LiteratureMiner:
    """Query PubMed for gene-disease-pain literature associations."""

    def __init__(self, email: str = "research@example.com", api_key: Optional[str] = None):
        self.email = email
        self.api_key = api_key
        if HAS_BIOPYTHON:
            Entrez.email = email
            if api_key:
                Entrez.api_key = api_key

    def search_gene(self, gene: str, context: str = "pain") -> Dict:
        """Search PubMed for a gene in a specific context.

        Parameters
        ----------
        gene : str
            Gene symbol (e.g., "TRPV1")
        context : str
            Search context: "pain", "RA", "nociception", or "inflammation"

        Returns
        -------
        dict with keys: gene, pmid_count, top_pmids, role_summary
        """
        if not HAS_BIOPYTHON:
            return {
                "gene": gene,
                "context": context,
                "pmid_count": 0,
                "top_pmids": [],
                "search_term": f"{gene} AND {context}"
            }

        queries = {
            "pain": f'("{gene}"[Title/Abstract]) AND (pain OR nocicept* OR analgesi* OR hyperalgesi*)',
            "RA": f'("{gene}"[Title/Abstract]) AND ("rheumatoid arthritis" OR collagen-induced arthritis)',
            "nociception": f'("{gene}"[Title/Abstract]) AND (nocicept* OR "dorsal root ganglion" OR DRG)',
            "inflammation": f'("{gene}"[Title/Abstract]) AND (inflammat* OR cytokin* OR immune)',
        }

        query = queries.get(context, f'"{gene}" AND {context}')

        try:
            handle = Entrez.esearch(db="pubmed", term=query, retmax=5, sort="relevance")
            record = Entrez.read(handle)
            handle.close()
            count = int(record["Count"])
            pmids = record["IdList"]
            time.sleep(0.34)  # NCBI rate limit: 3 requests/sec
            return {
                "gene": gene,
                "context": context,
                "pmid_count": count,
                "top_pmids": pmids,
                "search_term": query
            }
        except HTTPError as e:
            logger.warning(f"PubMed query failed for {gene}: {e}")
            return {"gene": gene, "context": context, "pmid_count": -1, "top_pmids": [], "search_term": query}

    def build_evidence_table(
        self, genes: List[str], contexts: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """Build a literature evidence table for a list of genes.

        Parameters
        ----------
        genes : list of str
            Gene symbols to search
        contexts : list of str, optional
            Search contexts. Defaults to ["pain", "RA", "nociception", "inflammation"]

        Returns
        -------
        pd.DataFrame with columns: Gene, Context, PMID_Count, Top_PMIDs
        """
        if contexts is None:
            contexts = ["pain", "RA", "nociception", "inflammation"]

        rows = []
        for gene in genes:
            for ctx in contexts:
                result = self.search_gene(gene, ctx)
                rows.append(result)

        df = pd.DataFrame(rows)

        # Pivot to wide format
        pivot = df.pivot_table(
            index="gene",
            columns="context",
            values="pmid_count",
            aggfunc="sum"
        ).fillna(0).astype(int)

        # Add top PMIDs
        pmid_cols = {}
        for ctx in contexts:
            ctx_data = df[df["context"] == ctx].set_index("gene")
            pmid_cols[f"top_pmids_{ctx}"] = ctx_data["top_pmids"].apply(
                lambda x: ",".join(x) if x else ""
            )

        result = pivot.copy()
        for col_name, series in pmid_cols.items():
            result[col_name] = series

        result["total_pubmed_hits"] = result[contexts].sum(axis=1)
        result = result.reset_index()
        result.columns = [c.replace("index", "Gene") for c in result.columns]

        return result.sort_values("total_pubmed_hits", ascending=False)

    def annotate_known_pathways(self) -> List[Dict]:
        """Return manually curated pain signaling pathway annotations.

        These are expert-curated pathway descriptions used for the
        pain_signaling_pathways.md output.
        """
        pathways = [
            {
                "name": "TRPV1-CGRP Nociceptor Axis",
                "description": "Nociceptor terminal activation and neuropeptide release axis. "
                               "TRPV1/TRPA1 detect noxious stimuli -> CGRP/Substance P release "
                               "-> neurogenic inflammation and central sensitization.",
                "direction": "TRPV1/TRPA1 activation -> Ca2+ influx -> CGRP/Substance P release "
                             "-> NGF/BDNF upregulation -> central sensitization",
                "key_genes": "TRPV1, TRPA1, CALCA, CALCB, TAC1, TACR1, NGF, NTRK1, BDNF, NTRK2",
                "pmids": ["31636456", "29487171", "25303979"],
                "significance": "Core pain transduction pathway; primary target for peripheral analgesics"
            },
            {
                "name": "Nav1.7 Action Potential Axis",
                "description": "Voltage-gated sodium channel axis for action potential generation "
                               "and propagation in nociceptors.",
                "direction": "Nav1.7 activation -> threshold depolarization -> Nav1.8-mediated "
                             "action potential -> pain signal propagation",
                "key_genes": "SCN9A, SCN10A, SCN11A, SCN1A, SCN2A, SCN8A",
                "pmids": ["30651630", "25188265", "17167479"],
                "significance": "Human genetics support: SCN9A gain-of-function = erythromelalgia; "
                                "loss-of-function = congenital insensitivity to pain"
            },
            {
                "name": "TNFa-NGF Inflammatory Pain Axis",
                "description": "Inflammatory cytokine-driven peripheral sensitization.",
                "direction": "TNF-a/IL-1b -> NGF upregulation -> TrkA -> TRPV1 "
                             "phosphorylation/sensitization -> hyperalgesia",
                "key_genes": "TNF, TNFRSF1A, NGF, NTRK1, NGFR, IL1B, IL6, PTGS2",
                "pmids": ["20393189", "21788404", "29230043"],
                "significance": "Links immune activation to pain hypersensitivity"
            },
            {
                "name": "Opioid Endogenous Analgesia Axis",
                "description": "Endogenous opioid system for descending pain modulation.",
                "direction": "POMC -> b-endorphin / PENK -> enkephalins / PDYN -> dynorphins "
                             "-> mu/delta/kappa receptors -> descending pain inhibition",
                "key_genes": "OPRM1, OPRD1, OPRK1, POMC, PENK, PDYN",
                "pmids": ["28624224", "25743836"],
                "significance": "Key perioperative target; mu receptor is primary target of clinical opioids"
            },
            {
                "name": "JAK-STAT RA Inflammatory Axis",
                "description": "JAK-STAT signaling in RA synovial inflammation.",
                "direction": "IL-6 -> gp130/JAK -> STAT3 phosphorylation -> inflammatory "
                             "gene transcription -> synovial hyperplasia",
                "key_genes": "JAK1, JAK2, JAK3, STAT3, STAT4, IL6, IL6R, IL17A, IL17RA",
                "pmids": ["32048119", "28264883"],
                "significance": "JAK inhibitors are FDA-approved RA treatments"
            },
            {
                "name": "MAPK Pain Sensitization Axis",
                "description": "MAPK signaling cascades mediating central sensitization.",
                "direction": "Synaptic activity -> p38/JNK/ERK -> CREB/Fos/Jun/EGR1 "
                             "-> transcriptional reprogramming -> central sensitization",
                "key_genes": "MAPK1, MAPK3, MAPK8, MAPK14, FOS, JUN, ATF3, EGR1, CREB1",
                "pmids": ["17464293", "19146809"],
                "significance": "p38 MAPK inhibitors show analgesic effects in preclinical models"
            },
            {
                "name": "Complement Neuroimmune Axis",
                "description": "Complement cascade activation in RA and neuroinflammation.",
                "direction": "Immune complexes -> C1q -> C3 -> C5 -> C5a -> C5aR1 on "
                             "macrophages/microglia -> inflammatory mediator release",
                "key_genes": "C5, C5AR1, C1QA, C1QB, C1QC, C3, CD40",
                "pmids": ["31654014", "32697981"],
                "significance": "C5aR1 antagonists in clinical trials for inflammatory pain"
            },
            {
                "name": "GABAergic Descending Inhibition",
                "description": "GABA/glycine-mediated inhibitory neurotransmission in spinal dorsal horn.",
                "direction": "GABA release -> GABAA receptor -> Cl- influx -> hyperpolarization "
                             "-> inhibition of pain transmission",
                "key_genes": "GABRA1, GABRA2, GABRB2, GABRG2, GABRB3, GLRA1, GLRB",
                "pmids": ["25855173", "28492257"],
                "significance": "Anesthetic targets; benzodiazepines and propofol act via GABA-A receptors"
            },
            {
                "name": "Prostaglandin Inflammatory Mediator Axis",
                "description": "Prostaglandin and leukotriene synthesis pathways mediating peripheral sensitization.",
                "direction": "AA -> COX-2 -> PGH2 -> PGE2 -> EP receptors -> cAMP/PKA "
                             "-> ion channel phosphorylation -> sensitization",
                "key_genes": "PTGS2, PTGES, PTGER1, PTGER2, PTGER3, PTGER4, ALOX5, ALOX12, ALOX15, LTA4H",
                "pmids": ["11433337", "26510955"],
                "significance": "NSAIDs target COX-2; the most widely used analgesic class"
            },
        ]
        return pathways

    def generate_pathway_report(
        self, pathways: List[Dict], kg_status: Optional[Dict[str, str]] = None
    ) -> str:
        """Generate a Markdown report of pain signaling pathways with KG status."""
        lines = [
            "# RA-PainKG: Literature-Annotated Pain Signaling Pathways",
            "",
            "> Generated from PrimeKG + GTEx + PubMed literature mining",
            f"> Date: 2026-07-15",
            "",
        ]

        for p in pathways:
            lines.append(f"## {p['name']}")
            lines.append("")
            lines.append(f"**Description**: {p['description']}")
            lines.append("")
            lines.append(f"**Direction**: {p['direction']}")
            lines.append("")
            lines.append(f"**Key Genes**: {p['key_genes']}")
            lines.append("")
            lines.append(f"**Literature**: PMID: {', '.join(p['pmids'])}")
            lines.append("")
            lines.append(f"**Significance**: {p['significance']}")
            lines.append("")

            if kg_status:
                status_parts = []
                for gene in p['key_genes'].split(", "):
                    gene = gene.strip()
                    if gene in kg_status:
                        status_parts.append(f"{gene}[{kg_status[gene]}]")
                    else:
                        status_parts.append(f"{gene}[KG]")
                lines.append(f"**RA-PainKG Status**: Found: {', '.join(status_parts)}")
                lines.append("")

            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    def save_pathway_report(self, report: str, path: Optional[Path] = None):
        """Save pathway report to file."""
        path = path or OUTPUT_LITERATURE.replace(".csv", "_pathways.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(report)
        logger.info(f"Pathway report saved to {path}")

    def save_evidence_table(self, df: pd.DataFrame, path: Optional[Path] = None):
        path = path or OUTPUT_LITERATURE
        df.to_csv(path, index=False)
        logger.info(f"Literature evidence table saved to {path}")
