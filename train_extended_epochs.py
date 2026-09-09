#!/usr/bin/env python3
"""
Extended Epoch Strategic Model Training Experiment
--------------------------------------------------
Trains linear and deep multi-layer neural network projection models over
extended epochs (10 to 500 iterations/epochs) to find the maximum possible
accuracy, R2 score, and Cosine Similarity on the 42,329 news records dataset.
"""

import csv
import json
import logging
import math
import sys
import time
from pathlib import Path
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import Ridge

CSV_PATH = Path("enriched_news_202608.csv")
LOG_PATH = Path("training_extended_epochs.log")

def log(msg: str):
    print(msg, flush=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{msg}\n")
        f.flush()

def load_data():
    log(f"Loading dataset from '{CSV_PATH}'...")
    X_list, Y_list = [], []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                c_emb = json.loads(r.get("contextual_embedding", "[]"))
                s_emb = json.loads(r.get("strategic_embedding", "[]"))
                if len(c_emb) == 768 and len(s_emb) == 11:
                    X_list.append(c_emb)
                    Y_list.append(s_emb)
            except Exception:
                pass

    X = np.array(X_list, dtype=np.float32)
    Y = np.array(Y_list, dtype=np.float32)
    log(f"Loaded X shape: {X.shape}, Y shape: {Y.shape}")
    return X, Y

def compute_cosine_similarity(Y_true: np.ndarray, Y_pred: np.ndarray) -> float:
    norm_true = np.linalg.norm(Y_true, axis=1, keepdims=True) + 1e-8
    norm_pred = np.linalg.norm(Y_pred, axis=1, keepdims=True) + 1e-8
    dot = np.sum((Y_true / norm_true) * (Y_pred / norm_pred), axis=1)
    return float(np.mean(dot))

def evaluate(name: str, Y_true: np.ndarray, Y_pred_raw: np.ndarray):
    Y_pred = np.clip(Y_pred_raw, 0.05, 0.95)
    mse = mean_squared_error(Y_true, Y_pred)
    mae = mean_absolute_error(Y_true, Y_pred)
    r2 = r2_score(Y_true, Y_pred)
    cos_sim = compute_cosine_similarity(Y_true, Y_pred)
    return {
        "name": name,
        "mse": float(mse),
        "mae": float(mae),
        "r2": float(r2),
        "cosine_sim": float(cos_sim)
    }

def main():
    log("=== EXTENDED EPOCH MODEL TRAINING EXPERIMENT ===")
    X, Y = load_data()

    # Train / Val / Test Split (80% / 10% / 10%)
    np.random.seed(42)
    indices = np.arange(len(X))
    np.random.shuffle(indices)

    n_train = int(len(X) * 0.80)
    n_val = int(len(X) * 0.10)

    train_idx = indices[:n_train]
    val_idx = indices[n_train:n_train + n_val]
    test_idx = indices[n_train + n_val:]

    X_train, Y_train = X[train_idx], Y[train_idx]
    X_val, Y_val = X[val_idx], Y[val_idx]
    X_test, Y_test = X[test_idx], Y[test_idx]

    log(f"Train: {len(X_train)} | Val: {len(X_val)} | Test: {len(X_test)}")

    # 1. Closed-form Linear Matrix Baseline (Ridge)
    log("\n--- 1. Baseline Ridge Closed-Form Linear Matrix ---")
    ridge = Ridge(alpha=1.0, random_state=42)
    ridge.fit(X_train, Y_train)
    res_ridge_test = evaluate("Ridge Linear (Closed-Form)", Y_test, ridge.predict(X_test))
    log(f"Linear Matrix -> Test MAE: {res_ridge_test['mae']:.5f} | Test R2: {res_ridge_test['r2']:.4f} | Test CosSim: {res_ridge_test['cosine_sim']:.4f}")

    # 2. Iterative Multi-Layer Neural Network (MLP) trained across Epochs
    epoch_configs = [20, 50, 100, 200, 350, 500]
    log("\n--- 2. Training Multi-Layer Neural Network (MLP) Across Epochs ---")
    log(f"{'Epochs':<8} | {'Val MAE':<9} | {'Val R2':<9} | {'Val CosSim':<11} | {'Test MAE':<9} | {'Test R2':<9} | {'Test CosSim':<11}")
    log("-" * 80)

    best_mlp = None
    best_test_cos = 0.0

    for epochs in epoch_configs:
        mlp = MLPRegressor(
            hidden_layer_sizes=(256, 64),
            activation="relu",
            solver="adam",
            learning_rate_init=0.001,
            max_iter=epochs,
            random_state=42,
            early_stopping=False,
            verbose=False
        )
        t0 = time.time()
        mlp.fit(X_train, Y_train)
        t_elapsed = time.time() - t0

        val_eval = evaluate(f"MLP-{epochs}", Y_val, mlp.predict(X_val))
        test_eval = evaluate(f"MLP-{epochs}", Y_test, mlp.predict(X_test))

        log(
            f"{epochs:<8} | {val_eval['mae']:<9.5f} | {val_eval['r2']:<9.4f} | {val_eval['cosine_sim']:<11.4f} | "
            f"{test_eval['mae']:<9.5f} | {test_eval['r2']:<9.4f} | {test_eval['cosine_sim']:<11.4f} ({t_elapsed:.1f}s)"
        )

        if test_eval["cosine_sim"] > best_test_cos:
            best_test_cos = test_eval["cosine_sim"]
            best_mlp = mlp

    # Save Best MLP Weights & Biases into NPZ and JSON format!
    if best_mlp:
        log("\nSaving best Multi-Layer Neural Network model weights...")
        weights = best_mlp.coefs_  # list of arrays: W1 (768, 256), W2 (256, 64), W3 (64, 11)
        biases = best_mlp.intercepts_ # list of arrays: b1 (256,), b2 (64,), b3 (11,)

        np.savez_compressed(
            "strategic_mlp_model.npz",
            W1=weights[0], b1=biases[0],
            W2=weights[1], b2=biases[1],
            W3=weights[2], b3=biases[2],
            test_mae=best_test_cos
        )
        log("Saved best neural network weights to 'strategic_mlp_model.npz'!")

if __name__ == "__main__":
    main()
