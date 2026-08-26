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
SUBCLUSTERS_PATH = DATA_DIR / "subclusters.json"

# Sub-cluster discovery (scripts/discover_subclusters.py): only articles above
# this relevance threshold for a dimension take part in that dimension's
# clustering, and candidate cluster counts searched per dimension (best picked
# by silhouette score) - two levels deep (dimension -> sub-cluster) for now,
# per CLAUDE.md; a third level needs more fabricated volume than this phase has.
SUBCLUSTER_RELEVANCE_THRESHOLD = 0.3
SUBCLUSTER_K_RANGE = [3, 4, 5, 6, 7]

# Ridge regularization strength for the per-startup lag regression once its
# features move from 11 dimensions to ~35-55 sub-clusters (see
# scripts/derive_sensitivity_profiles.py) - with only ~180 daily observations
# per startup and that many features, unregularized least squares overfits.
# Chosen via a simple train/test time split (first 150 days train, last 30
# held out), not in-sample fit, for the same reason RIDGE_ALPHA above is
# cross-validated rather than eyeballed. Held-out RMSE bottoms out near
# alpha=4 and rises on both sides.
PROFILE_REGRESSION_ALPHA = 4.0

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
# MAE bottoms out near alpha=0.2 and rises on both sides - see
# scripts/train_interaction_matrix.py), not by in-sample fit, since in-sample
# error only keeps improving toward zero as alpha -> 0 in an underdetermined
# system and would otherwise pick an alpha that memorizes the 20 startups.
RIDGE_ALPHA = 0.2

# Fraction of the largest raw |score| among a submission's 11 dimensions
# below which a dimension is considered negligible ("no effect") and greyed
# out on the radar chart instead of colored helping/hurting.
NEAR_ZERO_FRACTION = 0.10

# --- Real news ingestion (scripts/ingest_news.py) ---
# Kept in separate files from the fabricated dataset so real headlines never
# leak into the fabricated startups' training data.
REAL_NEWS_PATH = DATA_DIR / "real_news.json"
REAL_NEWS_EMBEDDINGS_PATH = DATA_DIR / "real_news_embeddings.npy"
INGESTION_STATE_PATH = DATA_DIR / "ingestion_state.json"
INGESTION_SAMPLE_LOG_PATH = DATA_DIR / "ingestion_samples.jsonl"

# Headlines published within this many hours of each other are compared for
# deduplication; anything above the similarity threshold is treated as the
# same underlying event and folded into the existing record instead of
# creating a new one.
DEDUP_WINDOW_HOURS = 48
DEDUP_SIMILARITY_THRESHOLD = 0.92

# Pretrained (not fine-tuned here) sentiment classifier used for real headline
# polarity - a real classifier per CLAUDE.md, not the fabricated dataset's
# template-assigned polarity.
SENTIMENT_MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
