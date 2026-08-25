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

N_NEWS_ARTICLES = 1000
TOP_K_STARTUPS = 3
