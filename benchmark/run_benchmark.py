"""Run GEARS perturbation prediction benchmark: GO vs RA-PainKG vs STRING."""

import sys, logging, argparse, json, numpy as np
from pathlib import Path
from scipy.sparse import csr_matrix

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from benchmark.kg_converter import KGToAdjacency, KGComparer
from benchmark.evaluation import compute_metrics, generate_benchmark_report
from benchmark.gears_wrapper import compare_kgs

logging.basicConfig(level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S")
logger = logging.getLogger("run_benchmark")


def generate_synthetic_data(n_cells=500, n_genes=200, n_perturbations=20, seed=42):
    rng = np.random.RandomState(seed)
    W_true = rng.randn(n_genes, n_genes) * 0.1
    W_true = W_true * (rng.rand(n_genes, n_genes) < 0.05)
    perturb_genes = rng.randint(0, n_genes, n_perturbations)
    perturb_idx = rng.randint(0, n_perturbations, n_cells)
    base_expr = rng.randn(n_cells, n_genes)
    de = np.zeros((n_cells, n_genes))
    for i in range(n_cells):
        pg = perturb_genes[perturb_idx[i]]
        de[i] = W_true[pg] + rng.randn(n_genes) * 0.05
    kg_adj = np.zeros((n_genes, n_genes))
    for i in range(n_genes):
        for j in range(i+1, n_genes):
            if rng.rand() < 0.02:
                kg_adj[i,j] = kg_adj[j,i] = 1.0
    gene_vocab = ["GENE_" + str(i) for i in range(n_genes)]
    return {"base_expr": base_expr, "de": de, "perturb_idx": perturb_idx,
            "perturb_genes": perturb_genes, "gene_vocab": gene_vocab,
            "kg_adj_ground_truth": kg_adj, "W_true": W_true}


def run_synthetic_benchmark(results_dir):
    logger.info("=== Synthetic Data Benchmark ===")
    data = generate_synthetic_data(500, 200, 20)
    n_train = 400
    train_expr = data["base_expr"][:n_train]
    train_perturb = data["perturb_idx"][:n_train]
    train_labels = data["de"][:n_train]
    test_expr = data["base_expr"][n_train:]
    test_perturb = data["perturb_idx"][n_train:]
    test_labels = data["de"][n_train:]
    rng = np.random.RandomState(42)

    kg_adjs = {}
    kg_adjs["GroundTruth"] = csr_matrix(data["kg_adj_ground_truth"])
    rand_adj = np.zeros((200, 200))
    n_edges = int(data["kg_adj_ground_truth"].sum() / 2)
    all_pairs = [(i,j) for i in range(200) for j in range(i+1,200)]
    chosen = rng.choice(len(all_pairs), n_edges, replace=False)
    for idx in chosen:
        i,j = all_pairs[idx]
        rand_adj[i,j] = rand_adj[j,i] = 1.0
    kg_adjs["Random"] = csr_matrix(rand_adj)
    kg_adjs["Identity"] = csr_matrix(np.eye(200))

    results = compare_kgs(kg_adjs, data["gene_vocab"],
        train_expr, np.array(train_perturb), train_labels,
        test_expr, np.array(test_perturb), test_labels,
        hidden_dim=64, results_dir=Path(results_dir))

    report = generate_benchmark_report(results)
    print("\n=== Synthetic Benchmark Results ===")
    print(report.to_string(index=False))
    return results


def main():
    parser = argparse.ArgumentParser(description="RA-PainKG GEARS Benchmark")
    parser.add_argument("--data_dir", default="benchmark/data")
    parser.add_argument("--kg_dir", default="output")
    parser.add_argument("--results_dir", default="benchmark/results")
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()
    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    if args.quick:
        run_synthetic_benchmark(results_dir)
    else:
        logger.info("Full benchmark requires Perturb-seq data. Use --quick for synthetic test.")
        run_synthetic_benchmark(results_dir)

    logger.info("Benchmark complete. Results in %s", results_dir)


if __name__ == "__main__":
    main()
