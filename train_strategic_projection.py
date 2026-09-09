#!/usr/bin/env python3
"""
Strategic Vector Linear Projection Model Training Script
---------------------------------------------------------
Trains a linear projection matrix W (768 x 11) and bias b (11)
to project 768-D dense news contextual text embeddings upfront into
the 11-D Strategic PESTLE + Porter's 5 Forces vector space.

Data Source: enriched_news_202608.csv (~42,329 records)
Splits: Train (80%), Validation (10%), Test (10%)
"""

import csv
import json
import logging
import math
import sys
import time
from pathlib import Path
import numpy as np
from sklearn.linear_model import Ridge, LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

LOG_FILE_PATH = Path(__file__).parent / "training_output.log"

def log_msg(msg: str):
    print(msg, flush=True)
    try:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(f"{msg}\n")
            f.flush()
    except Exception:
        pass

CSV_PATH = Path(__file__).parent / "enriched_news_202608.csv"
NPZ_SAVE_PATH = Path(__file__).parent / "strategic_projection_matrix.npz"
JSON_SAVE_PATH = Path(__file__).parent / "strategic_projection_matrix.json"

DIMENSION_NAMES = [
    "Political (PESTLE)",
    "Economic (PESTLE)",
    "Social (PESTLE)",
    "Technological (PESTLE)",
    "Legal (PESTLE)",
    "Environmental (PESTLE)",
    "Threat of New Entrants (Porter)",
    "Bargaining Power of Buyers (Porter)",
    "Bargaining Power of Suppliers (Porter)",
    "Threat of Substitutes (Porter)",
    "Competitive Rivalry (Porter)",
]

DIMENSION_KEYS = [
    "political",
    "economic",
    "social",
    "technological",
    "legal",
    "environmental",
    "threat_of_new_entrants",
    "bargaining_power_of_buyers",
    "bargaining_power_of_suppliers",
    "threat_of_substitutes",
    "competitive_rivalry",
]


def load_dataset(csv_path: Path):
    """Loads feature matrix X (768-D) and target matrix Y (11-D) from CSV."""
    print(f"[StrategicModelTrainer] Loading dataset from '{csv_path}'...", flush=True)
    if not csv_path.exists():
        print(f"[StrategicModelTrainer] ERROR: CSV file '{csv_path}' does not exist.", flush=True)
        sys.exit(1)

    X_list = []
    Y_list = []
    skipped = 0

    start_time = time.time()
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, r in enumerate(reader):
            if (idx + 1) % 10000 == 0:
                print(f"[StrategicModelTrainer] Loaded {idx + 1} rows...", flush=True)
            try:
                c_emb = json.loads(r.get("contextual_embedding", "[]"))
                s_emb = json.loads(r.get("strategic_embedding", "[]"))

                if len(c_emb) == 768 and len(s_emb) == 11:
                    X_list.append(c_emb)
                    Y_list.append(s_emb)
                else:
                    skipped += 1
            except Exception:
                skipped += 1

    X = np.array(X_list, dtype=np.float32)
    Y = np.array(Y_list, dtype=np.float32)

    elapsed = time.time() - start_time
    print(
        f"[StrategicModelTrainer] Successfully loaded {len(X)} valid samples in {elapsed:.2f}s. (Skipped/invalid: {skipped})",
        flush=True
    )
    print(f"[StrategicModelTrainer] Feature Matrix X Shape: {X.shape} | Target Matrix Y Shape: {Y.shape}", flush=True)
    return X, Y


def compute_cosine_similarity(Y_true: np.ndarray, Y_pred: np.ndarray) -> float:
    """Computes mean row-wise cosine similarity between true and predicted 11-D vectors."""
    norm_true = np.linalg.norm(Y_true, axis=1, keepdims=True) + 1e-8
    norm_pred = np.linalg.norm(Y_pred, axis=1, keepdims=True) + 1e-8
    
    Y_true_norm = Y_true / norm_true
    Y_pred_norm = Y_pred / norm_pred
    
    dot = np.sum(Y_true_norm * Y_pred_norm, axis=1)
    return float(np.mean(dot))


def evaluate_model(name: str, model, X: np.ndarray, Y: np.ndarray, clip_bounds=(0.05, 0.95)):
    """Evaluates model performance metrics on given dataset split."""
    if hasattr(model, "predict"):
        Y_raw = model.predict(X)
    else:
        # Assuming model is a tuple (W, b)
        W, b = model
        Y_raw = np.dot(X, W) + b

    Y_pred = np.clip(Y_raw, clip_bounds[0], clip_bounds[1])

    mse = mean_squared_error(Y, Y_pred)
    mae = mean_absolute_error(Y, Y_pred)
    r2 = r2_score(Y, Y_pred)
    cos_sim = compute_cosine_similarity(Y, Y_pred)

    return {
        "model_name": name,
        "mse": float(mse),
        "mae": float(mae),
        "r2": float(r2),
        "cosine_similarity": float(cos_sim),
        "Y_pred": Y_pred,
    }


def main():
    log_msg("=== STRATEGIC 11-D VECTOR PROJECTION MODEL TRAINING ===")
    
    # 1. Load Data
    X, Y = load_dataset(CSV_PATH)
    n_samples = len(X)
    
    # 2. Train / Val / Test Split (80% / 10% / 10%)
    np.random.seed(42)
    indices = np.arange(n_samples)
    np.random.shuffle(indices)

    n_train = int(n_samples * 0.80)
    n_val = int(n_samples * 0.10)
    n_test = n_samples - n_train - n_val

    train_idx = indices[:n_train]
    val_idx = indices[n_train : n_train + n_val]
    test_idx = indices[n_train + n_val :]

    X_train, Y_train = X[train_idx], Y[train_idx]
    X_val, Y_val = X[val_idx], Y[val_idx]
    X_test, Y_test = X[test_idx], Y[test_idx]

    log_msg(
        f"Data Splits -> Train: {len(X_train)} samples | Val: {len(X_val)} samples | Test: {len(X_test)} samples"
    )

    # 3. Model Training & Hyperparameter Tuning
    alphas = [1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0, 1000.0]
    best_alpha = None
    best_val_score = -float("inf")
    best_ridge_model = None

    log_msg("\n--- Tuning Linear Matrix Multiplication (Ridge Regression) ---")
    for alpha in alphas:
        ridge = Ridge(alpha=alpha, random_state=42)
        ridge.fit(X_train, Y_train)
        
        val_eval = evaluate_model(f"Ridge (alpha={alpha})", ridge, X_val, Y_val)
        log_msg(
            f"Alpha {alpha:7.4f} -> Val MSE: {val_eval['mse']:.5f} | Val MAE: {val_eval['mae']:.5f} | Val R2: {val_eval['r2']:.4f} | Val CosSim: {val_eval['cosine_similarity']:.4f}"
        )

        if val_eval["r2"] > best_val_score:
            best_val_score = val_eval["r2"]
            best_alpha = alpha
            best_ridge_model = ridge

    log_msg(f"\nBest Linear Projection Matrix Alpha: {best_alpha}")

    # Extract W (768 x 11) and bias b (11)
    W_linear = best_ridge_model.coef_.T  # Shape: (768, 11)
    b_linear = best_ridge_model.intercept_  # Shape: (11,)
    chosen_model = (W_linear, b_linear)
    model_type_name = "Linear Matrix Multiplication (Y = X @ W + b)"

    log_msg(f"\n=== FINAL TEST SET EVALUATION ({model_type_name}) ===")
    test_eval = evaluate_model(model_type_name, chosen_model, X_test, Y_test)
    
    log_msg(f"Test Set Mean Squared Error (MSE) : {test_eval['mse']:.5f}")
    log_msg(f"Test Set Mean Absolute Error (MAE): {test_eval['mae']:.5f}")
    log_msg(f"Test Set R2 Variance Explained    : {test_eval['r2']:.4f} ({test_eval['r2']*100:.1f}%)")
    log_msg(f"Test Set Vector Cosine Similarity  : {test_eval['cosine_similarity']:.4f} ({test_eval['cosine_similarity']*100:.1f}%)")

    # 5. Per-Dimension Performance Breakdown
    log_msg("\n=== PER-DIMENSION PERFORMANCE BREAKDOWN (TEST SET) ===")
    Y_test_pred = test_eval["Y_pred"]
    
    header = f"{'Dimension Index & Name':<42} | {'MSE':<7} | {'MAE':<7} | {'R2 Score':<8} | {'CosSim':<7}"
    log_msg(header)
    log_msg("-" * 80)
    for dim_i in range(11):
        dim_y_true = Y_test[:, dim_i]
        dim_y_pred = Y_test_pred[:, dim_i]

        d_mse = mean_squared_error(dim_y_true, dim_y_pred)
        d_mae = mean_absolute_error(dim_y_true, dim_y_pred)
        d_r2 = r2_score(dim_y_true, dim_y_pred)

        norm_t = np.linalg.norm(dim_y_true) + 1e-8
        norm_p = np.linalg.norm(dim_y_pred) + 1e-8
        d_sim = np.dot(dim_y_true, dim_y_pred) / (norm_t * norm_p)

        dim_line = f"Dim {dim_i:2d}: {DIMENSION_NAMES[dim_i]:<35} | {d_mse:.4f}  | {d_mae:.4f}  | {d_r2:.4f}   | {d_sim:.4f}"
        log_msg(dim_line)

    # 6. Save Weight Matrix W (768 x 11) and Bias b (11)
    log_msg(f"\nSaving projection matrix weights to '{NPZ_SAVE_PATH}' and '{JSON_SAVE_PATH}'...")

    np.savez_compressed(
        NPZ_SAVE_PATH,
        W=W_linear,
        b=b_linear,
        alpha=best_alpha,
        test_mse=test_eval["mse"],
        test_mae=test_eval["mae"],
        test_r2=test_eval["r2"],
        test_cosine_sim=test_eval["cosine_similarity"],
    )

    json_export = {
        "model_type": "Linear Matrix Projection (Y = X @ W + b)",
        "input_dim": 768,
        "output_dim": 11,
        "alpha": float(best_alpha),
        "metrics": {
            "test_mse": round(test_eval["mse"], 6),
            "test_mae": round(test_eval["mae"], 6),
            "test_r2": round(test_eval["r2"], 6),
            "test_cosine_similarity": round(test_eval["cosine_similarity"], 6),
        },
        "dimension_keys": DIMENSION_KEYS,
        "dimension_names": DIMENSION_NAMES,
        "bias": [round(float(val), 6) for val in b_linear],
        "weight_matrix_shape": [768, 11],
        "weight_matrix": [[round(float(val), 6) for val in row] for row in W_linear],
    }

    with open(JSON_SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(json_export, f, indent=2)

    log_msg("Training and export completed successfully!")


if __name__ == "__main__":
    main()
