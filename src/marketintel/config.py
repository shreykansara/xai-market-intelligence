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
# Mean of the training CVP embeddings, subtracted from every CVP embedding
# (training-time and inference-time alike) before it ever meets W - see the
# RIDGE_ALPHA comment below and train_interaction_matrix.py for why this
# centering step exists.
CVP_MEAN_PATH = DATA_DIR / "cvp_mean.npy"
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
# The system is heavily underdetermined (384*384 parameters vs. 50 startups *
# 11 dimensions = 550 training examples), so regularization is load-bearing,
# not cosmetic. Chosen via leave-one-startup-out cross-validation (held-out
# MAE bottoms out near alpha=0.2 and rises on both sides - see
# scripts/train_interaction_matrix.py), not by in-sample fit, since in-sample
# error only keeps improving toward zero as alpha -> 0 in an underdetermined
# system and would otherwise pick an alpha that memorizes the startups.
RIDGE_ALPHA = 0.2

# Why CVP embeddings are mean-centered before ever meeting W (see
# CVP_MEAN_PATH above): diagnosed directly after the 20->50 startup expansion
# and the hidden-template noise perturbation both failed to fix "different
# CVPs produce near-identical output." All 50 real business CVP embeddings
# project onto W's dominant singular direction with the SAME sign and similar
# magnitude (mean -0.42, std only 0.095) - because that direction is ~88%
# cosine-aligned with the mean of all training CVP embeddings, i.e. the
# "generic business pitch text" component every CVP shares regardless of
# domain. In a system this underdetermined (147,456 parameters, 550 training
# examples), ridge regression's minimum-norm solution spends a large share of
# W's capacity (24% of its total energy, pre-fix) modeling that shared
# component - not because it's informative, but because it's the one
# direction present, to some degree, in every training example. Subtracting
# the training CVP mean before fitting (and before every inference-time
# query) removes that shared axis from what W is asked to explain, forcing
# it to explain target variance using only each business's distinctive
# content. Verified empirically: real-CVP-to-real-CVP output cosine
# similarity on a 5-CVP discrimination test dropped from 0.75-0.86
# (collapsed, pre-fix) to a properly varied -0.16-0.51 (post-fix), at a
# training-fit MAE cost of only 27.93 -> 29.14 (target std ~50.7).
CVP_CENTERING_ENABLED = True

# Fraction of the largest raw |score| among a submission's 11 dimensions
# below which a dimension is considered negligible ("no effect") and greyed
# out on the radar chart instead of colored helping/hurting.
NEAR_ZERO_FRACTION = 0.10

# --- Real news ingestion (src/marketintel/ingestion.py) ---
# Kept in separate files from the fabricated dataset so real facts never leak
# into the fabricated startups' training data. The fact is the primary scored
# unit (see fact_extraction.py): one fetched article decomposes into one or
# more atomic facts. Articles are kept only as a provenance container -
# headline, source, link, and which facts came out of it - not scored
# themselves and not embedded.
REAL_ARTICLES_PATH = DATA_DIR / "real_articles.json"
REAL_FACTS_PATH = DATA_DIR / "real_facts.json"
REAL_FACT_EMBEDDINGS_PATH = DATA_DIR / "real_fact_embeddings.npy"
INGESTION_STATE_PATH = DATA_DIR / "ingestion_state.json"
INGESTION_SAMPLE_LOG_PATH = DATA_DIR / "ingestion_samples.jsonl"
INGESTION_EXCLUDED_LOG_PATH = DATA_DIR / "ingestion_excluded.jsonl"
# Grounding safeguards (src/marketintel/grounding.py), ported into the live
# path from the GDELT bulk backfill so both ingestion codepaths share the
# same safety guarantees rather than diverging - see ingestion.py. A
# different kind of filter from INGESTION_EXCLUDED_LOG_PATH above (relevance-
# gate exclusions), logged separately for the same reason BACKFILL_*
# equivalents are.
INGESTION_NONCONTENT_LOG_PATH = DATA_DIR / "ingestion_noncontent.jsonl"
INGESTION_UNGROUNDED_LOG_PATH = DATA_DIR / "ingestion_ungrounded.jsonl"
INGESTION_UNMATCHED_LOG_PATH = DATA_DIR / "ingestion_unmatched_directional.jsonl"

# Facts published within this many hours of each other are compared for
# deduplication; anything above the similarity threshold is treated as the
# same underlying fact (however many outlets reported it) and folded into the
# existing record instead of creating a new one.
DEDUP_WINDOW_HOURS = 48
DEDUP_SIMILARITY_THRESHOLD = 0.92

# A free local model via Ollama (https://ollama.com), not a paid API, used to
# decompose one article into one or more atomic, neutrally-worded facts
# before anything downstream (embedding, the relevance gate, scope
# classification) runs - see fact_extraction.py. If Ollama isn't running or
# this model isn't pulled, extraction falls back to treating the article as a
# single unmodified fact rather than failing the run.
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2:3b"
# On CPU-only hardware (no GPU), even this 3B model can take 60-90s for a single
# generation - a cold first call was observed taking ~80s (~32s just loading
# weights) in testing. 30s was too tight and caused spurious single-fact
# fallbacks on working Ollama installs; 120s gives real inference room to
# finish while still bounding a genuinely hung/unreachable server.
OLLAMA_TIMEOUT_SECONDS = 120

# Every new real fact's relevance and polarity are inferred by
# similarity-weighted vote among its k nearest neighbors in the fabricated
# seed corpus (the only hand-labeled data in the system) - see
# src/marketintel/seed_inference.py. Geographic scope uses a different
# mechanism (see RELEVANCE_GATE_PERCENTILE below) since pooled k-NN voting
# let majority scope classes (India, Punjab) win purely on population size.
SEED_NEIGHBOR_K = 10

# Minimum-relevance gate, run before scope classification: an incoming
# fact's max relevance across all 11 dimensions must clear this
# percentile of the fabricated seed corpus's OWN max-relevance distribution
# (computed once from the 1000 seed articles' hand-labeled scores) or it's
# excluded entirely - no scope assigned, not used downstream. A fact
# that isn't meaningfully close to anything this system models has no
# business being forced into a geographic scope it has no real bearing on.
RELEVANCE_GATE_PERCENTILE = 5

# --- Real-data seed inference (src/marketintel/real_data_inference.py) ---
# The live ingestion path (ingestion.py only - NOT the GDELT bulk backfill,
# which keeps looking up the fabricated corpus untouched) migrates its k-NN
# reference pool from the fabricated seed corpus to the accumulated real-fact
# corpus itself, PER DIMENSION - a dimension only cuts over once the real
# corpus has enough of its own data to support a reliable lookup; thin
# dimensions keep falling back to the fabricated corpus rather than silently
# degrading. Two thresholds gate that per-dimension decision, checked fresh
# against whatever's accumulated so far on every ingestion run (so a
# dimension can - and is expected to - graduate from fabricated to real as
# more data comes in, with no code change needed):
#   - at least this many real facts must exceed SUBCLUSTER_RELEVANCE_THRESHOLD
#     on that dimension (roughly 1.5x SEED_NEIGHBOR_K, so a k=10 nearest-
#     neighbor query has a real chance of actually surfacing on-topic real
#     neighbors, not mostly off-topic ones diluting the signal);
REAL_DATA_MIN_TOTAL_PER_DIM = 15
#   - AND at least this many of EACH polarity class among those, so a
#     polarity vote for a new fact on this dimension isn't structurally
#     incapable of ever producing one of the two labels (e.g. environmental
#     coverage that's 100% negative in the accumulated corpus so far would
#     make "positive environmental news" unrepresentable, regardless of what
#     a new fact actually says) - diagnosed as a real, current gap via a
#     direct coverage check, not a hypothetical.
REAL_DATA_MIN_PER_POLARITY = 3
# Below this many total real facts, the relevance GATE THRESHOLD itself
# (calibrate_relevance_threshold) stays computed from the fabricated corpus
# regardless of per-dimension coverage - a 5th-percentile estimate from
# under ~50 samples is too noisy to trust as a cutoff for everything else.
REAL_DATA_MIN_FACTS_FOR_GATE_RECALIBRATION = 50

# --- GDELT bulk backfill (src/marketintel/gdelt_bulk.py, comparative_matching.py) ---
# A separate, one-off/batch collection process from the live ingestion_service.py
# (which keeps running on its own 30-minute schedule for ongoing Punjab/LPU-area
# coverage). Sourced from GDELT 2.0's bulk export files (data.gdeltproject.org),
# not the DOC 2.0 API (limited to ~3 months of lookback) and not RSS (no history
# at all) - the only free, no-key source with multi-year depth.
GDELT_BULK_BASE_URL = "http://data.gdeltproject.org/gdeltv2"
BACKFILL_ARTICLES_PATH = DATA_DIR / "backfill_articles.json"
BACKFILL_FACTS_PATH = DATA_DIR / "backfill_facts.json"
BACKFILL_FACT_EMBEDDINGS_PATH = DATA_DIR / "backfill_fact_embeddings.npy"
BACKFILL_STATE_PATH = DATA_DIR / "backfill_state.json"
BACKFILL_EXCLUDED_LOG_PATH = DATA_DIR / "backfill_excluded.jsonl"
BACKFILL_UNMATCHED_LOG_PATH = DATA_DIR / "backfill_unmatched_directional.jsonl"
# Grounding safeguards (src/marketintel/grounding.py) - a DIFFERENT kind of
# filter from BACKFILL_EXCLUDED_LOG_PATH above (which logs relevance-gate
# exclusions). BACKFILL_NONCONTENT_LOG_PATH logs titles the pre-filter
# rejected before any Ollama call (section labels, digests, etc.);
# BACKFILL_UNGROUNDED_LOG_PATH logs facts rejected AFTER decomposition
# because they stated a number not traceable to the source title - the
# direct response to a real observed hallucination (see CLAUDE.md).
BACKFILL_NONCONTENT_LOG_PATH = DATA_DIR / "backfill_noncontent.jsonl"
BACKFILL_UNGROUNDED_LOG_PATH = DATA_DIR / "backfill_ungrounded.jsonl"

# Comparative-fact matching (src/marketintel/comparative_matching.py): a bare
# state-value fact ("GST on mobile phones is 18%") only gets compared against a
# candidate PRIOR fact if their similarity clears this threshold - deliberately
# stricter than RELEVANCE_GATE_PERCENTILE's cutoff (~0.58 on the same cosine
# scale), since a wrong comparative match silently fabricates a direction/
# polarity rather than just mis-scoring relevance. Starting point per CLAUDE.md
# instructions; tune from validation results (scripts/validate_comparative_matching.py)
# before this ever touches real backfill data.
COMPARATIVE_MATCH_SIMILARITY_THRESHOLD = 0.85
