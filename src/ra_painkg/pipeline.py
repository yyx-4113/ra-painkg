"""Main pipeline: end-to-end RA-PainKG construction and analysis.

Usage:
    python -m ra_painkg.pipeline          # Full pipeline
    python -m ra_painkg.pipeline --steps kg  # KG construction only
    python -m ra_painkg.pipeline --steps analysis  # Analysis only
    python -m ra_painkg.pipeline --steps viz  # Visualization only
"""

import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from .config import PROJECT_ROOT, DATA_DIR, OUTPUT_DIR
from .primekg_loader import PrimeKGLoader
from .seed_nodes import SeedNodeFinder
from .literature_mining import LiteratureMiner
from .gtex_filter import GTExFilter
from .track_assigner import TrackAssigner
from .kg_builder import KGBuilder
from .network_analysis import NetworkAnalyzer
from .visualization import Visualizer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("pipeline")


def step_load_data():
    """Step 1: Load PrimeKG and build full graph."""
    logger.info("=" * 60)
    logger.info("STEP 1: Loading PrimeKG")
    logger.info("=" * 60)

    loader = PrimeKGLoader()
    csv_path = DATA_DIR / "prime_kg.csv"

    if not csv_path.exists():
        zip_path = DATA_DIR / "primekg_dataset.zip"
        if zip_path.exists():
            loader.extract_zip(zip_path)
        else:
            raise FileNotFoundError(
                f"PrimeKG data not found. Place prime_kg.csv or primekg_dataset.zip in {DATA_DIR}"
            )

    df = loader.load()
    logger.info(f"PrimeKG loaded: {len(df):,} edges")

    # Build full digraph (optional, can be slow)
    # loader.build_full_digraph()

    return loader


def step_seed_nodes(loader):
    """Step 2: Identify seed nodes."""
    logger.info("=" * 60)
    logger.info("STEP 2: Identifying Seed Nodes")
    logger.info("=" * 60)

    finder = SeedNodeFinder(loader)
    seed_nodes = finder.run_all()
    finder.save_seed_nodes()
    return finder, seed_nodes


def step_build_kg(loader, seed_nodes):
    """Step 3: Build knowledge graph."""
    logger.info("=" * 60)
    logger.info("STEP 3: Building Knowledge Graph")
    logger.info("=" * 60)

    # Try to load GTEx for tissue filtering
    gtex = None
    gtex_path = DATA_DIR / "GTEx_median_tpm.gct.gz"
    if gtex_path.exists():
        try:
            gtex = GTExFilter(gtex_path)
            gtex.load()
            logger.info("GTEx data loaded for tissue filtering")
        except Exception as e:
            logger.warning(f"GTEx loading failed: {e}")

    builder = KGBuilder(loader, gtex)
    builder.seed_finder = SeedNodeFinder(loader)

    # Build with 2-hop expansion
    graph = builder.build_from_seeds(seed_nodes, expansion_hops=2)

    # Expand with additional relations
    builder.expand_graph(max_additional_edges=50000)

    return builder, graph


def step_track_assignment(graph):
    """Step 4: Assign dual-track labels."""
    logger.info("=" * 60)
    logger.info("STEP 4: Track Assignment")
    logger.info("=" * 60)

    assigner = TrackAssigner()

    # Collect gene node names
    gene_names = set()
    for node, data in graph.nodes(data=True):
        if data.get("node_type") in ("gene/protein", "protein"):
            name = str(data.get("node_name", "")).upper()
            if name:
                gene_names.add(name)

    df = assigner.assign(sorted(gene_names))
    assigner.save(df)
    return assigner


def step_network_analysis(graph):
    """Step 5: Network topology analysis."""
    logger.info("=" * 60)
    logger.info("STEP 5: Network Analysis")
    logger.info("=" * 60)

    analyzer = NetworkAnalyzer(graph)

    # Compute centrality
    centrality_df = analyzer.compute_centrality()
    analyzer.save_centrality()

    # Save statistics
    analyzer.save_statistics()

    # Print top hubs
    top = analyzer.get_top_hubs(metric="betweenness", n=10)
    logger.info("Top 10 hubs by betweenness:")
    for _, row in top.iterrows():
        track_info = ""
        if row["track_a"] and row["track_b"]:
            track_info = " [Track A+B]"
        elif row["track_a"]:
            track_info = " [Track A]"
        elif row["track_b"]:
            track_info = " [Track B]"
        logger.info(f"  {row['node_name']}: {row['betweenness']:.6f}{track_info}")

    # Track comparison
    comparison = analyzer.compare_tracks()
    logger.info(f"Track comparison: A={comparison['track_a_genes']} genes, "
                 f"B={comparison['track_b_genes']} genes")

    return analyzer


def step_literature_mining(graph):
    """Step 6: Literature mining for pain genes."""
    logger.info("=" * 60)
    logger.info("STEP 6: Literature Mining")
    logger.info("=" * 60)

    miner = LiteratureMiner()

    # Collect gene names from the graph
    gene_names = set()
    for node, data in graph.nodes(data=True):
        if data.get("node_type") in ("gene/protein", "protein"):
            name = str(data.get("node_name", ""))
            if name and (data.get("track_a") or data.get("track_b")):
                gene_names.add(name)

    # Build evidence table (using cached PubMed counts when offline)
    top_genes = sorted(gene_names)[:50]  # Limit for API calls
    evidence_df = miner.build_evidence_table(top_genes)
    miner.save_evidence_table(evidence_df)

    # Generate pathway report
    pathways = miner.annotate_known_pathways()

    # Build KG status for pathway genes
    kg_status = {}
    for node, data in graph.nodes(data=True):
        name = str(data.get("node_name", ""))
        if name:
            parts = []
            parts.append("KG")
            if data.get("track_a"):
                parts.append("TrackA")
            if data.get("track_b"):
                parts.append("TrackB")
            kg_status[name] = ",".join(parts)

    report = miner.generate_pathway_report(pathways, kg_status)
    miner.save_pathway_report(report)

    return pathways


def step_visualization(analyzer, graph, pathways):
    """Step 7: Generate figures."""
    logger.info("=" * 60)
    logger.info("STEP 7: Visualization")
    logger.info("=" * 60)

    viz = Visualizer()
    viz.generate_all(analyzer, graph, pathways)


def step_save_outputs(builder, analyzer, graph, summary):
    """Step 8: Save all outputs."""
    logger.info("=" * 60)
    logger.info("STEP 8: Saving Outputs")
    logger.info("=" * 60)

    builder.graph = graph
    builder.save_all()
    builder.save_summary(summary)

    # Generate per-node centrality summary
    analyzer.save_centrality()

    logger.info("All outputs saved to: " + str(OUTPUT_DIR))


def run_pipeline(steps: str = "all"):
    """Run the full RA-PainKG pipeline.

    Parameters
    ----------
    steps : str
        Pipeline steps to run: "all", "kg", "analysis", "viz", or comma-separated
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    run_all = steps == "all"
    step_set = set(steps.split(",")) if not run_all else set()

    loader = None
    builder = None
    graph = None
    analyzer = None
    pathways = None

    # Step 1: Load data
    if run_all or "data" in step_set or "kg" in step_set:
        loader = step_load_data()

    # Step 2: Seed nodes
    if run_all or "seeds" in step_set or "kg" in step_set:
        _, seed_nodes = step_seed_nodes(loader)
    else:
        seed_nodes = None

    # Step 3: Build KG
    if run_all or "kg" in step_set:
        builder, graph = step_build_kg(loader, seed_nodes)

    # Step 4: Track assignment
    if run_all or "track" in step_set:
        step_track_assignment(graph)

    # Step 5: Network analysis
    if run_all or "analysis" in step_set:
        if graph is None:
            raise ValueError("Graph not available. Run kg step first.")
        analyzer = step_network_analysis(graph)

    # Step 6: Literature mining
    if run_all or "literature" in step_set:
        if graph is None:
            raise ValueError("Graph not available. Run kg step first.")
        pathways = step_literature_mining(graph)

    # Step 7: Visualization
    if run_all or "viz" in step_set:
        if graph is None or analyzer is None:
            raise ValueError("Graph and analyzer required. Run kg and analysis first.")
        if pathways is None:
            pathways = LiteratureMiner().annotate_known_pathways()
        step_visualization(analyzer, graph, pathways)

    # Step 8: Save
    if run_all or "save" in step_set:
        summary = builder.build_summary() if builder else {}
        step_save_outputs(builder, analyzer, graph, summary)

    logger.info("Pipeline complete!")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="RA-PainKG Pipeline")
    parser.add_argument(
        "--steps", type=str, default="all",
        help="Pipeline steps: all, kg, analysis, viz, or comma-separated"
    )
    args = parser.parse_args()
    run_pipeline(steps=args.steps)
