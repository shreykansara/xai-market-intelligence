from pathlib import Path

PESTLE_DIMS = ["political", "economic", "social", "technological", "legal", "environmental"]
PESTLE_LABELS = {
    "political": "Political",
    "economic": "Economic",
    "social": "Social",
    "technological": "Technological",
    "legal": "Legal",
    "environmental": "Environmental",
}

PORTERS_DIMS = [
    "threat_new_entrants",
    "supplier_power",
    "buyer_power",
    "threat_substitutes",
    "competitive_rivalry",
]
PORTERS_LABELS = {
    "threat_new_entrants": "Threat of New Entrants",
    "supplier_power": "Supplier Power",
    "buyer_power": "Buyer Power",
    "threat_substitutes": "Threat of Substitutes",
    "competitive_rivalry": "Competitive Rivalry",
}

# Geographic scopes, weighted roughly toward broader coverage (realistic distribution
# for 1000 fabricated news articles: more India/World-level events than hyper-local ones).
SCOPES = ["LPU", "Phagwara", "Jalandhar", "Kapurthala", "Punjab", "India", "World"]
SCOPE_WEIGHTS = {
    "LPU": 50,
    "Phagwara": 70,
    "Jalandhar": 100,
    "Kapurthala": 80,
    "Punjab": 150,
    "India": 300,
    "World": 250,
}

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
NEWS_PATH = DATA_DIR / "news.json"
NEWS_EMBEDDINGS_PATH = DATA_DIR / "news_embeddings.npy"
STARTUPS_PATH = DATA_DIR / "startups.json"
STARTUP_EMBEDDINGS_PATH = DATA_DIR / "startup_embeddings.npy"
INTERACTION_MATRIX_PATH = DATA_DIR / "interaction_matrix.npy"
PROFIT_HISTORY_PATH = DATA_DIR / "profit_history.json"

N_PROFIT_DAYS = 180
# Candidate lag windows (days) searched when deriving each startup's sensitivity
# profile from its fabricated profit history - see scripts/derive_sensitivity_profiles.py.
CANDIDATE_LAGS = [1, 3, 7, 14]

N_NEWS_ARTICLES = 1000
TOP_K_STARTUPS = 3

# Ridge regularization strength for fitting the shared interaction matrix W.
# The system is heavily underdetermined (384*384 parameters vs. 20 startups *
# 11 dimensions = 220 training examples), so regularization is load-bearing,
# not cosmetic. Chosen via leave-one-startup-out cross-validation (held-out
# MAE bottoms out near alpha=0.3 and rises on both sides - see
# scripts/train_interaction_matrix.py), not by in-sample fit, since in-sample
# error only keeps improving toward zero as alpha -> 0 in an underdetermined
# system and would otherwise pick an alpha that memorizes the 20 startups.
RIDGE_ALPHA = 0.3

# Fraction of the largest raw |score| among a submission's 11 dimensions
# below which a dimension is considered negligible ("no effect") and greyed
# out on the radar chart instead of colored helping/hurting.
NEAR_ZERO_FRACTION = 0.10
