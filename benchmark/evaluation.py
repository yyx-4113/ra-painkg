"""Evaluation metrics for GEARS perturbation prediction benchmark."""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import mean_squared_error, r2_score


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Compute regression metrics for perturbation prediction."""
    mask = ~np.isnan(y_true) & ~np.isnan(y_pred)
    yt = y_true[mask]
    yp = y_pred[mask]

    if len(yt) < 2:
        return {"n": len(yt), "mse": np.nan, "rmse": np.nan,
                "pearson_r": np.nan, "spearman_r": np.nan, "r2": np.nan}

    mse = mean_squared_error(yt, yp)
    pr, _ = pearsonr(yt, yp)
    sr, _ = spearmanr(yt, yp)
    r2 = r2_score(yt, yp)

    return {
        "n": len(yt),
        "mse": float(mse),
        "rmse": float(np.sqrt(mse)),
        "pearson_r": float(pr),
        "spearman_r": float(sr),
        "r2": float(r2),
    }


def compute_per_gene_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    gene_list: List[str],
) -> pd.DataFrame:
    """Compute metrics for each gene separately."""
    rows = []
    for i, gene in enumerate(gene_list):
        m = compute_metrics(y_true[i], y_pred[i])
        m["gene"] = gene
        rows.append(m)
    return pd.DataFrame(rows)


def compute_topk_accuracy(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    gene_list: List[str],
    top_k_pct: float = 0.10,
) -> Dict:
    """Compute top-K% accuracy: how often are the top predicted DE genes
    also the top true DE genes?"""
    n_genes = len(gene_list)
    k = max(1, int(n_genes * top_k_pct))

    true_topk_sets = []
    pred_topk_sets = []
    for i in range(y_true.shape[0]):
        true_idx = np.argsort(-np.abs(y_true[i]))[:k]
        pred_idx = np.argsort(-np.abs(y_pred[i]))[:k]
        true_topk_sets.append(set(true_idx))
        pred_topk_sets.append(set(pred_idx))

    overlaps = [len(a & b) / k for a, b in zip(true_topk_sets, pred_topk_sets)]
    return {
        "top_k_pct": top_k_pct,
        "top_k_genes": k,
        "mean_overlap": float(np.mean(overlaps)),
        "median_overlap": float(np.median(overlaps)),
        "n_perturbations": len(overlaps),
    }


def compute_perturbation_specific_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    perturb_genes: List[str],
    perturb_type: str = "all",
) -> pd.DataFrame:
    """Compute metrics grouped by perturbation gene identity."""
    unique_genes = sorted(set(perturb_genes))
    rows = []
    for gene in unique_genes:
        idx = [i for i, g in enumerate(perturb_genes) if g == gene]
        if len(idx) == 0:
            continue
        yt_sub = y_true[idx]
        yp_sub = y_pred[idx]
        m = compute_metrics(yt_sub.flatten(), yp_sub.flatten())
        m["perturb_gene"] = gene
        m["n_perturbations"] = len(idx)
        rows.append(m)
    return pd.DataFrame(rows)


def generate_benchmark_report(
    metric_dicts: Dict[str, Dict],
) -> pd.DataFrame:
    """Generate a clean benchmark report from metric dictionaries."""
    rows = []
    for kg_name, metrics in metric_dicts.items():
        row = {"KG": kg_name}
        row.update(metrics)
        rows.append(row)
    return pd.DataFrame(rows)
