import os
from pathlib import Path


def _load_env_file(path: Path) -> None:
    """Minimal .env loader - stdlib only, no python-dotenv dependency (this
    project uses urllib over requests for the same reason: one fewer thing to
    install for a few lines of parsing).

    A real environment variable ALWAYS wins over the file, so an export in the
    shell, a CI secret, or a systemd Environment= line overrides .env rather
    than being silently clobbered by a stale checked-out value.

    Supports `KEY=value`, `export KEY=value`, `#` comments, blank lines, and
    optional surrounding single/double quotes. Anything it can't parse is
    skipped rather than raising - a malformed .env must never stop the app
    from starting, since most of the system doesn't need a key at all.
    """
    try:
        if not path.is_file():
            return
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            if line.startswith("export "):
                line = line[len("export "):].lstrip()
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip()
            if not key:
                continue
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
                value = value[1:-1]
            os.environ.setdefault(key, value)  # setdefault = real env wins
    except OSError:
        return

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

# Fully-qualified for fastembed (embeddings.py) - fastembed's model registry
# indexes by the HuggingFace repo id, unlike sentence-transformers' short-name
# resolution. Same model, same 384-dim output either way.
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"

# Load .env as early as possible: config is imported by everything, so doing it
# here means any entry point (server.py, ingestion_service.py, the scripts) gets
# GROQ_API_KEY without each one remembering to load it. .env is gitignored;
# .env.example is the committed template.
_load_env_file(ROOT_DIR / ".env")
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

# Which news pool the OPTIONAL sales-history-upload regression
# (sales_upload.derive_sales_profile) draws on: "real" (the accumulated real
# ingested-fact corpus, data/real_facts.json) or "fabricated" (the 1000-article
# fabricated seed corpus, data/news.json - the same corpus scripts/
# derive_sensitivity_profiles.py already regresses fabricated startups against).
# Intended, production value is "real". Set to "fabricated" as a TIME-BOXED,
# pragmatic fix for a live class demo (today's real-news corpus is far too
# sparse to ever clear the upload<->real-news overlap bar - see CLAUDE.md's
# "Known gaps" - so the "real" path would just fall back to CVP-only every
# time). Flip this single flag back to "real" once real coverage grows enough
# to demo meaningfully; every result computed under "fabricated" is labeled as
# demo/sample-data to the caller (never silently presented as derived from the
# user's live news feed - see sales_upload.py and web/index.html).
SALES_REGRESSION_NEWS_SOURCE = "fabricated"  # "real" | "fabricated"

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
# Grounding safeguards (src/marketintel/grounding.py) - a different kind of
# filter from INGESTION_EXCLUDED_LOG_PATH above (relevance-gate exclusions),
# so rejections are logged separately rather than pooled: NONCONTENT logs
# titles rejected before any Ollama call, UNGROUNDED logs facts rejected
# after decomposition for stating a number not traceable to the source.
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

# --- LPU announcements corpus (src/marketintel/lpu_ingestion.py) ---
# The ONLY news corpus in the system: ~16.5k real LPU announcements/notices
# scraped into data/lpudata/ as several overlapping snapshot files, deduped
# by their own `id` on load. Every fact derived from them is tagged
# scope="LPU" and is_lpu=True by construction - these are university
# announcements, not wire news, so there is no scope inference to do.
LPU_RAW_DIR = DATA_DIR / "lpudata"
LPU_ANNOUNCEMENTS_PATH = DATA_DIR / "lpu_announcements.json"
LPU_FACTS_PATH = DATA_DIR / "lpu_facts.json"
LPU_FACT_EMBEDDINGS_PATH = DATA_DIR / "lpu_fact_embeddings.npy"
# Checkpoint for the ingestion run: a full pass is measured in hours even with
# a single bundled decomposition+classification call per announcement (see
# fact_pipeline.py), so it must survive interruption and resume from the last
# flushed announcement rather than starting over.
LPU_STATE_PATH = DATA_DIR / "lpu_ingestion_state.json"
LPU_CHECKPOINT_EVERY = 25
LPU_SCOPE = "LPU"
# Max characters of (title + body) handed to Ollama for atomic breakdown.
# Measured directly on this corpus: decomposition costs ~3s at 128 chars, ~5s
# at 400, ~7s at 700 and ~12s at 2,200 - but the longest bodies (up to 9,013
# chars) blow past OLLAMA_TIMEOUT_SECONDS entirely, and a timeout is far worse
# than a truncation because the fallback stores the whole announcement as ONE
# unsplit fact - the exact compound record this pipeline exists to avoid. Two
# of the first eight announcements timed out this way and consumed 61% of that
# run's wall time. LPU notices put the substance in the title and opening
# lines (the tail is typically block/room lists, signatures and boilerplate),
# so capping here costs little and buys both speed and reliable atomicity.
LPU_MAX_DECOMPOSITION_CHARS = 1200
# Grounding safeguards (src/marketintel/grounding.py), reused UNCHANGED from
# the live ingestion path - it did not previously run on the LPU path at all,
# which was a real, unresolved gap (LPU used a different, unverified
# mechanism than the rest of the system). NONCONTENT logs announcements
# skipped before any Groq call (empty/junk title); UNGROUNDED logs facts
# rejected after decomposition for stating a number not traceable to the
# source announcement text.
LPU_NONCONTENT_LOG_PATH = DATA_DIR / "lpu_ingestion_noncontent.jsonl"
LPU_UNGROUNDED_LOG_PATH = DATA_DIR / "lpu_ingestion_ungrounded.jsonl"

# --- Groq API (src/marketintel/groq_client.py) ---
# Replaces the local Ollama model as the LLM transport for BOTH fact
# decomposition and LPU classification. The API key is read from the
# GROQ_API_KEY environment variable at call time - never stored here, never
# committed. Only the transport changed: prompts, JSON parsing, grounding and
# comparative matching are untouched.
GROQ_BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
# Which transport the LLM calls actually use: "groq" (hosted API) or "ollama"
# (local model). Selectable rather than a one-way swap because the right answer
# genuinely differs by workload, measured not assumed:
#   - BULK ingestion (44,695 LPU announcements, ~1,590 tokens each): Groq's free
#     tier caps at 200K tokens/day, making the full run ~343 DAYS versus ~9.4
#     days on local Ollama. The free tier's token cap binds ~4x harder than its
#     request cap. Use "ollama" for bulk.
#   - LIVE ingestion (a handful of articles per 30-minute cycle): nowhere near
#     any cap, and Groq is far faster per call with no local RAM cost. Use "groq".
LLM_PROVIDER = "groq"
# llama-3.1-8b-instant is NOT on Groq's current free tier - verified against
# their published limits table. These are the general-purpose chat models that
# are: openai/gpt-oss-20b and -120b, qwen/qwen3.6-27b and 3.8-27b (all 30 RPM /
# 1K RPD / 8K TPM / 200K TPD), and groq/compound (30 RPM / 250 RPD / 70K TPM).
GROQ_MODEL = "openai/gpt-oss-20b"
GROQ_FREE_TIER_RPD = 1000
GROQ_FREE_TIER_TPD = 200_000
GROQ_TIMEOUT_SECONDS = 60
GROQ_MAX_ATTEMPTS = 4
# Start pausing when this few requests remain in the current window, instead of
# sprinting into a 429 - a voluntary pause costs less than a rejected request
# plus its mandated retry-after wait.
GROQ_RATE_LIMIT_SAFETY_MARGIN = 2

# --- Legacy Ollama settings (no longer the runtime path) ---
# Kept because the retry/attempt constants below are still used by the shared
# retry logic, and because removing OLLAMA_* entirely would break the older
# ingestion.py call sites for no benefit. Nothing in the runtime path starts
# an Ollama process any more.
# Every announcement must actually be processed by the model; a silent
# fallback is not an acceptable outcome at corpus scale. A single call fails
# for two observed reasons, both transient and both retryable:
#   1. TIMEOUT on a long input - retrying the same oversized text just times
#      out again, so each retry also SHRINKS the input (see the shrink factor
#      below), which reliably converts a timeout into a successful call.
#   2. Malformed JSON from llama3.2:3b - a plain retry usually succeeds,
#      since the failure is sampling noise rather than a systematic refusal.
# Attempts are per call, with exponential backoff between them.
OLLAMA_MAX_ATTEMPTS = 4
OLLAMA_RETRY_BACKOFF_SECONDS = 2.0
# Each retry after a timeout keeps this fraction of the previous input.
OLLAMA_RETRY_SHRINK_FACTOR = 0.6

# --- Real-data seed inference (src/marketintel/real_data_inference.py) ---
# The live ingestion path (ingestion.py) migrates its k-NN
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

# Comparative-fact matching (src/marketintel/comparative_matching.py): a bare
# state-value fact ("GST on mobile phones is 18%") only gets compared against a
# candidate PRIOR fact if their similarity clears this threshold - deliberately
# stricter than RELEVANCE_GATE_PERCENTILE's cutoff (~0.58 on the same cosine
# scale), since a wrong comparative match silently fabricates a direction/
# polarity rather than just mis-scoring relevance. Tune from validation
# results (scripts/validate_comparative_matching.py), not by eyeballing.
COMPARATIVE_MATCH_SIMILARITY_THRESHOLD = 0.85
