# AI-Based Explainable Market Intelligence — Complete Codebase Architecture & Code Walkthrough

This document provides a comprehensive, exhaustive walkthrough of the entire **AI-Based Explainable Market Intelligence** codebase. It covers the mathematical foundations, system architecture, data generation, real-time news ingestion microservices, fact decomposition, machine learning algorithms, descriptive flowcharts, and provides an in-depth function-by-function and line-by-line explanation of every module.

---

## Table of Contents
1. [High-Level System Architecture & Operating Mechanics](#1-high-level-system-architecture--operating-mechanics)
2. [Hierarchical Clustering & Multi-Level News Labelling](#2-hierarchical-clustering--multi-level-news-labelling)
3. [Real News Ingestion, Fact Decomposition & Seed Transfer](#3-real-news-ingestion-fact-decomposition--seed-transfer)
4. [End-to-End Mathematical & Machine Learning Formulations](#4-end-to-end-mathematical--machine-learning-formulations)
5. [Granular File-by-File, Module-by-Module Code Walkthrough](#5-granular-file-by-file-module-by-module-code-walkthrough)
   - [5.1 Core ML & Analysis Package (`src/marketintel/`)](#51-core-ml--analysis-package-srcmarketintel)
     - [`config.py`](#srcmarketintelconfigpy)
     - [`embeddings.py`](#srcmarketintelembeddingspy)
     - [`data_loader.py`](#srcmarketinteldata_loaderpy)
     - [`analysis.py`](#srcmarketintelanalysispy)
     - [`atomic_io.py`](#srcmarketintelatomic_iopy)
     - [`fact_extraction.py`](#srcmarketintelfact_extractionpy)
     - [`seed_inference.py`](#srcmarketintelseed_inferencepy)
     - [`ingestion.py`](#srcmarketintelingestionpy)
   - [5.2 Offline Training & Data Generation Pipeline (`scripts/`)](#52-offline-training--data-generation-pipeline-scripts)
     - [`hidden_ground_truth.py`](#scriptshidden_ground_truthpy)
     - [`generate_news.py`](#scriptsgenerate_newspy)
     - [`generate_startups.py`](#scriptsgenerate_startupspy)
     - [`discover_subclusters.py`](#scriptsdiscover_subclusterspy)
     - [`simulate_profit_history.py`](#scriptssimulate_profit_historypy)
     - [`derive_sensitivity_profiles.py`](#scriptsderive_sensitivity_profilespy)
     - [`train_interaction_matrix.py`](#scriptstrain_interaction_matrixpy)
   - [5.3 Validation & Ingestion Scripts (`scripts/`)](#53-validation--ingestion-scripts-scripts)
     - [`validate_umbrella_case.py`](#scriptsvalidate_umbrella_casepy)
     - [`validate_fact_decomposition.py`](#scriptsvalidate_fact_decompositionpy)
     - [`validate_scope_fix.py`](#scriptsvalidate_scope_fixpy)
     - [`ingest_news.py`](#scriptsingest_newspy)
   - [5.4 Application Servers & Frontend](#54-application-servers--frontend)
     - [`server.py`](#serverpy)
     - [`ingestion_service.py`](#ingestion_servicepy)
     - [`app.py`](#apppy)
     - [`web/index.html`](#webindexhtml)
6. [Submodule Interaction Matrix & Descriptive System Flowcharts](#6-submodule-interaction-matrix--descriptive-system-flowcharts)
   - [6.1 Global Submodule Dependency & Interaction Flowchart](#61-global-submodule-dependency--interaction-flowchart)
   - [6.2 Detailed Flowchart: Offline Training & Sensitivity Modeling](#62-detailed-flowchart-offline-training--sensitivity-modeling)
   - [6.3 Detailed Flowchart: Real-Time News Ingestion & Fact Processing](#63-detailed-flowchart-real-time-news-ingestion--fact-processing)
   - [6.4 Detailed Flowchart: Online CVP Inference & Two-Tier Scoring Engine](#64-detailed-flowchart-online-cvp-inference--two-tier-scoring-engine)
   - [6.5 Submodule Input/Output Contract & Tensor Shape Matrix](#65-submodule-inputoutput-contract--tensor-shape-matrix)

---

## 1. High-Level System Architecture & Operating Mechanics

### 1.1 The Core Problem
Early-stage startups possess **no historical sales or operational track records**. When macroeconomic shifts, supply disruptions, regulatory changes, or technological breakthroughs occur, founders and investors have no systematic, quantifiable, or traceable way to forecast how those external events will impact the company.

### 1.2 System Solution Overview
The system models business sensitivity across **11 strategic dimensions**:
- **6 PESTLE Dimensions**: Political, Economic, Social, Technological, Legal, Environmental.
- **5 Porter's Five Forces**: Threat of New Entrants, Supplier Power, Buyer Power, Threat of Substitutes, Competitive Rivalry.

The architecture comprises two main subsystems:
1. **Offline Training & Exposure Pipeline**: Uses a seed corpus of 1000 multi-dimensional fabricated news events and 20 diverse reference startups. By simulating 180-day financial histories with delayed shocks and recovering sensitivity via sub-cluster lagged ridge regression, it trains a bilinear interaction matrix $\mathbf{W} \in \mathbb{R}^{384 \times 384}$ using Kernel Dual Ridge Regression.
2. **Online Real News Ingestion & Fact Decomposition Microservice**: Pulls real headlines from RSS feeds and GDELT, decomposes complex articles into atomic neutral facts via a local LLM (Ollama `llama3.2:3b`), and transfers scores from the seed corpus using a similarity-gated nearest-neighbor voting mechanism with per-class-best-match geographic scope inference.

---

## 2. Hierarchical Clustering & Multi-Level News Labelling

The system guarantees full traceability by structuring news into a **three-tier labeling hierarchy**:

```
Level 0: Raw Article Generation (Continuous Soft Multi-Dimensional Relevance + Polarity)
   │
   ├── Level 1: Dimension Filtering (Hard thresholding at relevance > 0.3)
   │      │
   │      └── Level 2: Sub-Cluster Discovery (Unsupervised Agglomerative Clustering)
   │             │
   │             └── Level 3: Centroid N-Gram Label Extraction (Human-readable Sub-Topic Naming)
```

### Level 0: Soft Multi-Dimensional Ground Truth & Polarity
- **PESTLE Vector**: 6 continuous values in $[0.0, 1.0]$.
- **Porter's Vector**: 5 continuous values in $[0.0, 1.0]$.
- **Polarity**: Binary directional state ($+1.0$ for `"positive"`, $-1.0$ for `"negative"`).
- **Scope**: Geographic tag (`"LPU"`, `"Phagwara"`, `"Jalandhar"`, `"Kapurthala"`, `"Punjab"`, `"India"`, `"World"`).
- **Cross-Dimensional Relevance**: A single event can carry simultaneous relevance across multiple dimensions (e.g., an import tariff is both Political $0.90$ and Economic $0.80$, while increasing Supplier Power $0.60$).

### Level 1: Dimension Partitioning & Cross-Membership
- Clustering is executed independently for each of the 11 dimensions.
- An article is included in a dimension's cluster pool if:
  $$\text{relevance}(a, d) > \text{SUBCLUSTER\_RELEVANCE\_THRESHOLD} \quad (0.30)$$
- **Cross-Membership**: Because an article can be relevant to several dimensions, it is assigned independently to sub-clusters in each relevant dimension.

### Level 2: Semantic Sub-Clustering via Agglomerative Clustering
For all article embeddings in a dimension:
1. **Distance Metric**: Cosine distance ($1 - \mathbf{u}^\top \mathbf{v}$) over $L_2$-normalized 384-d vectors.
2. **Linkage Criterion**: `average` linkage (UPGMA).
3. **Adaptive Cluster Count Selection (`best_clustering`)**:
   - Tests candidate cluster counts $k \in [3, 4, 5, 6, 7]$.
   - Computes Cosine Silhouette Scores $S(k)$.
   - **Tuning Heuristic**: Rather than a naive $\arg\max_k S(k)$ (which is heavily biased toward over-splitting short texts into singletons), the algorithm chooses the **smallest $k$** that achieves at least **90% (`tolerance = 0.90`)** of the peak silhouette score:
     $$k^* = \min \{ k \mid S(k) \ge 0.90 \cdot \max_{j} S(j) \}$$

### Level 3: Sub-Cluster Label Generation (`label_cluster`)
Sub-cluster names are synthesized unsupervised from the articles closest to each cluster's semantic center:
1. **Centroid Computation**:
   $$\mathbf{c} = \frac{1}{|C|} \sum_{i \in C} \mathbf{e}_i$$
2. **Representative Retrieval**: Computes cosine similarities $\mathbf{e}_i^\top \mathbf{c}$ and retrieves the top 3 nearest articles.
3. **Keyword Extraction & Stopword Pruning**:
   - Extracts all alphabetic tokens (`[A-Za-z']+`) from the 3 titles.
   - Discards short tokens ($\le 3$ characters) and 30+ domain stopwords (`the`, `with`, `amid`, `across`, `into`, etc.).
4. **N-Gram Synthesis**:
   - Identifies the top 2 most frequent title keywords via `Counter` and capitalizes them (e.g., `"Tariffs Rattle"`, `"Visa Immigration"`, `"Recession Fears"`, `"Monsoon Sowing"`).
   - If no words qualify, falls back to the exact title of the nearest article.

---

## 3. Real News Ingestion, Fact Decomposition & Seed Transfer

The system incorporates a complete live news pipeline (`src/marketintel/ingestion.py`) that operates on real global news while remaining separate from the fabricated training corpus.

### 3.1 The Unit of Analysis: Atomic Facts vs. Articles
Real news articles often contain mixed claims with divergent business implications (e.g., a tax bill that increases high-income brackets while cutting middle-income brackets).
- **Fact Decomposition (`src/marketintel/fact_extraction.py`)**: Uses a local Ollama LLM (`llama3.2:3b`) to decompose raw headlines/articles into distinct, independently-scorable atomic facts.
- **Stylistic Neutralization**: Strips loaded editorial framing, opinion, and rhetorical flourishes while preserving exact numbers, thresholds, dates, and named entities.
- **Fallback Guarantee**: If Ollama is offline or times out, the extractor safely falls back to treating the input text as a single unmodified fact.
- **Provenance Separation**: `data/real_articles.json` stores container metadata (headline, source URL, timestamp, child fact IDs), while `data/real_facts.json` and `data/real_fact_embeddings.npy` store the individual scorable fact records.

### 3.2 Semantic Deduplication
- Newly extracted facts are compared against facts published within the rolling **48-hour window** (`DEDUP_WINDOW_HOURS`).
- If cosine similarity $\ge 0.92$ (`DEDUP_SIMILARITY_THRESHOLD`), the fact is recognized as a duplicate story from another outlet. It increments `mention_count` and updates `last_seen` without creating a duplicate record.

### 3.3 The Relevance Gate
- Global news feeds contain general topics (sports, local crimes, celebrity news) irrelevant to business market scanning.
- **Gate Calibration**: The system computes the 5th percentile of the maximum dimension relevance across the 1000 seed articles (yielding a cutoff threshold of $\approx 0.58$).
- **Noise Filtering**: Any real fact whose maximum inferred relevance across all 11 dimensions is below this threshold is rejected, prevented from entering the downstream pipeline, and logged to `data/ingestion_excluded.jsonl`.

### 3.4 Seed Corpus Transfer & Scope Bias Elimination
Because no human-labeled real dataset exists, real facts infer their properties from the 1000-article seed corpus (`src/marketintel/seed_inference.py`):
1. **Relevance & Polarity**: Computed via similarity-weighted voting across the $k=10$ nearest seed neighbors.
2. **Geographic Scope (Per-Class-Best-Match)**:
   - *The Bias Problem*: In naive pooled $k$-NN voting, majority classes in the seed corpus (`India`=300, `Punjab`=150) frequently won out over smaller classes (`World`=250, `LPU`=50) simply due to density, causing foreign stories to be misclassified as Indian.
   - *The Solution*: For each of the 7 scope classes, the algorithm finds only that class's **single closest seed article**. The fact is assigned whichever class's single best match has the highest cosine similarity. This prevents population volume from distorting geographic attribution.

---

## 4. End-to-End Mathematical & Machine Learning Formulations

### 4.1 The Bilinear Interaction Operator $W$
The interaction between a business positioning vector $\mathbf{z} \in \mathbb{R}^{384}$ and an event vector $\mathbf{x} \in \mathbb{R}^{384}$ is defined as:
$$\text{gate}(\mathbf{x}, \mathbf{z}) = \mathbf{x}^\top \mathbf{W} \mathbf{z}$$

### 4.2 Kernel Dual Ridge Regression
With $N = 20 \text{ startups} \times 11 \text{ dimensions} = 220$ training instances and $384 \times 384 = 147,456$ parameters, solving in the primal space would be severely ill-conditioned.

1. **Combined News Vector** for startup $s$ and dimension $d$:
   $$\mathbf{a}_{s, d} = \sum_{j \in \text{Linked}(s)} \text{relevance}(j, d) \cdot \text{polarity}(j) \cdot \mathbf{x}_j$$
2. **Prediction Equivalence**:
   $$\hat{y}_{s, d} = \mathbf{a}_{s, d}^\top \mathbf{W} \mathbf{z}_s = \text{vec}(\mathbf{a}_{s, d} \mathbf{z}_s^\top)^\top \text{vec}(\mathbf{W})$$
3. **Dual Kernel Gram Matrix**:
   Applying the tensor contraction identity $(\mathbf{a}_1 \otimes \mathbf{b}_1)^\top (\mathbf{a}_2 \otimes \mathbf{b}_2) = (\mathbf{a}_1^\top \mathbf{a}_2)(\mathbf{b}_1^\top \mathbf{b}_2)$:
   $$\mathbf{K}_{ij} = (\mathbf{a}_i^\top \mathbf{a}_j) \cdot (\mathbf{z}_i^\top \mathbf{z}_j)$$
4. **Dual Closed-Form Solution**:
   $$\boldsymbol{\alpha} = (\mathbf{K} + \lambda \mathbf{I}_{N})^{-1} \mathbf{y}$$
   $$\mathbf{W} = \sum_{i=1}^N \alpha_i (\mathbf{a}_i \mathbf{z}_i^\top)$$
   where $\lambda = \text{RIDGE\_ALPHA} = 0.20$ (selected via leave-one-startup-out cross-validation).

### 4.3 Sub-Cluster Lagged Profile Recovery
To generate grounded training targets without hand-authoring:
1. **Profit Simulation**:
   $$\text{Profit}_s(t) = \text{Base}_s + g_s \cdot t + \epsilon(t) + \sum_{a \in \text{News}} \text{Shock}(a, s, t - \tau_s)$$
2. **Sub-Cluster Design Matrix** $\mathbf{X}_\tau \in \mathbb{R}^{180 \times M}$ (~35–55 features):
   $$\mathbf{X}_\tau[t, m] = \sum_{a \in \text{News on } t - \tau, a \in m} \text{relevance}(a, d) \cdot \text{polarity}(a)$$
3. **Lagged Ridge Regression**:
   Regresses $\Delta \text{Profit}(t)$ on $\mathbf{X}_\tau[t]$ with unpenalized intercept:
   $$\boldsymbol{\beta}_\tau = (\mathbf{X}_\tau^\top \mathbf{X}_\tau + \lambda_{\text{profile}} \mathbf{I})^{-1} \mathbf{X}_\tau^\top \Delta \text{Profit}$$
4. **Dimension Rollup & Rescaling**:
   Selects $\tau^* = \arg\max_\tau R^2(\tau)$, sums sub-cluster coefficients to parent dimensions, and scales the maximum magnitude to $100.0$.

---

## 5. Granular File-by-File, Module-by-Module Code Walkthrough

---

### 5.1 Core ML & Analysis Package (`src/marketintel/`)

#### `src/marketintel/config.py`
- **Lines 1–27**: Defines canonical lists `PESTLE_DIMS` and `PORTERS_DIMS` and display label maps `PESTLE_LABELS` and `PORTERS_LABELS`.
- **Lines 28–39**: Defines `SCOPES` and `SCOPE_WEIGHTS`, establishing realistic geographic distributions.
- **Line 41**: Sets `EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"`.
- **Lines 43–51**: Resolves project root and paths for all data artifacts (`data/news.json`, `data/startups.json`, `data/subclusters.json`, `data/interaction_matrix.npy`, `data/profit_history.json`).
- **Lines 53–59**: Defines `SUBCLUSTER_RELEVANCE_THRESHOLD = 0.3` and `SUBCLUSTER_K_RANGE = [3, 4, 5, 6, 7]`.
- **Lines 61–74**: Configures profile regression penalty `PROFILE_REGRESSION_ALPHA = 4.0`, time horizon `N_PROFIT_DAYS = 180`, and `CANDIDATE_LAGS = [1, 3, 7, 14]`.
- **Lines 76–92**: Sets dataset scale `N_NEWS_ARTICLES = 1000`, `RIDGE_ALPHA = 0.2`, and `NEAR_ZERO_FRACTION = 0.10`.
- **Lines 94–141**: Real news ingestion settings: paths for `real_articles.json`, `real_facts.json`, `real_fact_embeddings.npy`, `ingestion_state.json`, `ingestion_samples.jsonl`, and `ingestion_excluded.jsonl`. Sets `DEDUP_WINDOW_HOURS = 48`, `DEDUP_SIMILARITY_THRESHOLD = 0.92`, `OLLAMA_HOST = "http://localhost:11434"`, `OLLAMA_MODEL = "llama3.2:3b"`, `SEED_NEIGHBOR_K = 10`, and `RELEVANCE_GATE_PERCENTILE = 5`.

#### `src/marketintel/embeddings.py`
- `get_model()`: Cached wrapper with `@lru_cache(maxsize=1)` loading `SentenceTransformer(EMBEDDING_MODEL_NAME)`.
- `embed_texts(texts: list[str]) -> np.ndarray`: Encodes batches of text with `normalize_embeddings=True` ($L_2$ unit vectors).
- `embed_text(text: str) -> np.ndarray`: Encodes a single text string returning a 1D vector of shape `(384,)`.

#### `src/marketintel/data_loader.py`
- `load_news()`: Loads `news.json` and `news_embeddings.npy`.
- `load_startups()`: Loads `startups.json` and `startup_embeddings.npy`.
- `news_by_id(news)`: Returns dictionary mapping `id` to article object.
- `load_interaction_matrix()`: Loads `interaction_matrix.npy` ($384 \times 384$).
- `load_subclusters()`: Loads `subclusters.json`.
- `load_real_facts()`: Loads `real_facts.json` and `real_fact_embeddings.npy` (returns empty lists if not present).
- `load_real_articles()`: Loads `real_articles.json`.

#### `src/marketintel/analysis.py`
- `polarity_sign(article: dict) -> float`: Returns `1.0` if polarity is `"positive"` else `-1.0`.
- `compute_gates(news_embeddings, cvp_embedding, W)`: Vectorized calculation `news_embeddings @ (W @ cvp_embedding)`.
- `subcluster_breakdown_for_dim(news, gates, dim, score_field, dim_subclusters, top_n_articles=5)`:
  - Multiplies $\text{relevance} \times \text{polarity} \times \text{gate}$ for assigned articles.
  - Groups contributions by sub-cluster, identifies top 5 articles per cluster, and sorts clusters by descending absolute score.
- `dimension_breakdowns(...)`: Computes sub-cluster breakdowns across all requested dimensions.
- `raw_dimension_scores(breakdown)`: Sums sub-cluster raw scores to parent dimension scores.
- `normalize_for_display(raw_scores)`: Linearly rescales scores so the largest absolute value equals $100.0$.
- `near_zero_dims(raw_pestle, raw_porters, fraction)`: Identifies dimensions whose score is $<10\%$ of the maximum magnitude.
- `score_submission(news, news_embeddings, cvp_embedding, W, subclusters)`: Full analysis coordinator returning display scores, breakdowns, and negligible flags.

#### `src/marketintel/atomic_io.py`
- `atomic_write_json(path: Path, data) -> None`: Dumps JSON to `path.tmp` and executes atomic `tmp_path.replace(path)`.
- `atomic_write_npy(path: Path, array: np.ndarray) -> None`: Saves NumPy array to a binary `.tmp` stream and renames it atomically over the target.

#### `src/marketintel/fact_extraction.py`
- `EXTRACTION_PROMPT`: Structured prompt instructing the LLM to extract distinct factual claims, preserve specifics (numbers, dates, entities), strip rhetorical framing, and output a raw JSON array of strings.
- `_call_ollama(text: str) -> str`: Dispatches POST request to `{OLLAMA_HOST}/api/generate` with timeout handling.
- `_parse_facts(raw_response: str) -> list[str] | None`: Uses regex `r"\[.*\]"` with `re.DOTALL` to parse the JSON array from the response.
- `extract_facts(text: str) -> list[str]`: Main entry point returning extracted fact strings; catches network/parsing errors and safely falls back to `[text]`.

#### `src/marketintel/seed_inference.py`
- `nearest_neighbors(embedding, seed_embeddings, k=10)`: Computes dot products, finds top $k$ neighbors, clips similarities to $\ge 0$, and normalizes weights to sum to 1.
- `infer_relevance(seed_news, top_idx, weights)`: Computes weighted average of neighbor relevance scores across all 11 dimensions.
- `infer_categorical(seed_news, top_idx, weights, field)`: Performs weighted plurality voting among neighbors for discrete fields (`polarity`).
- `calibrate_relevance_threshold(seed_news, percentile=5)`: Computes the 5th percentile of maximum dimension relevance across the seed dataset.
- `group_indices_by_scope(seed_news)`: Partitions seed article indices by their geographic scope.
- `infer_scope_best_match(embedding, seed_embeddings, scope_indices)`: Evaluates maximum similarity within each scope partition and assigns the scope associated with the highest individual match.

#### `src/marketintel/ingestion.py`
- `fetch_rss(url, since)` / `fetch_gdelt(since)`: Fetches items from RSS feeds and the GDELT DOC 2.0 API published after the `since` cursor.
- `find_duplicate_fact(new_embedding, facts, fact_embeddings, now)`: Searches facts within the 48-hour window for cosine similarity $\ge 0.92$.
- `run_ingestion_once(verbose=True)`: Complete ingestion coordinator executing fetch, fact decomposition, dedup, relevance gating, seed scoring, and atomic saving.

---

### 5.2 Offline Training & Data Generation Pipeline (`scripts/`)

#### `scripts/hidden_ground_truth.py`
- `HIDDEN_TEMPLATES`: Defines domain-grounded hidden sensitivity profiles across all 20 reference startups.
- `shock_lag_days`: Deterministically assigns lag values cycling through $[1, 3, 7, 14]$ days ($i \pmod 4$).

#### `scripts/generate_news.py`
- `TEMPLATES`: Parameterized news templates covering diverse PESTLE and Porter's dimensions.
- `build_scores(base, dims, rng)`: Adds uniform noise ($\pm 0.08$) to active dimensions and background noise ($0.02 - 0.12$) to inactive dimensions.
- `generate_articles(n, rng)`: Generates 1000 synthetic news articles with scopes, polarities, dates, and score vectors.
- `main()`: Persists `data/news.json` and generates `data/news_embeddings.npy` (shape $1000 \times 384$).

#### `scripts/generate_startups.py`
- `STARTUPS`: Definitions of 20 Indian startup concepts with detailed CVPs.
- `pick_linked_articles(hidden, news, rng)`: Links 3 to 5 matching seed articles to each startup based on dominant hidden dimensions.
- `main()`: Writes `data/startups.json` and embeds CVPs into `data/startup_embeddings.npy` ($20 \times 384$).

#### `scripts/discover_subclusters.py`
- `best_clustering(embeddings, k_range, tolerance=0.9)`: Agglomeratively clusters dimension embeddings and selects the smallest $k$ achieving $90\%$ of peak silhouette score.
- `label_cluster(articles, embeddings, member_idx)`: Finds the 3 articles closest to the centroid, prunes stopwords, and returns the top 2 frequent title keywords.
- `discover_for_dimension(news, embeddings, score_field, dim)`: Filters articles with relevance $>0.30$ and executes clustering and labeling.
- `main()`: Generates and saves `data/subclusters.json`.

#### `scripts/simulate_profit_history.py`
- `simulate_one(hidden, news, rng)`: Generates 180-day baseline profit series with trend, Gaussian noise ($\sigma = 4\%$), and delayed financial shocks from relevant news events.
- `main()`: Writes synthetic financial histories to `data/profit_history.json`.

#### `scripts/derive_sensitivity_profiles.py`
- `build_feature_columns(subclusters)`: Creates indexed feature columns for all (dimension, sub-cluster) pairs.
- `build_daily_signal(news, subclusters, columns, n_days)`: Builds the $(180 \times M)$ daily event signal matrix.
- `fit_lag_ridge(profit, signal, lag, alpha)`: Solves lagged ridge regression on daily profit differences $\Delta \text{Profit}$.
- `derive_profile(profit, signal, columns)`: Selects optimal lag via $R^2$, rolls sub-cluster coefficients up to dimensions, and normalizes.
- `main()`: Updates `data/startups.json` with derived profiles and prints validation metrics against hidden ground truth.

#### `scripts/train_interaction_matrix.py`
- `build_training_examples(...)`: Constructs 220 $(startup, dimension)$ training tuples with combined news vectors $\mathbf{a}_{s, d}$ and CVP vectors $\mathbf{z}_s$.
- `fit_interaction_matrix(combined_vecs, cvp_vecs, targets, alpha)`: Solves Kernel Dual Ridge Regression using $\mathbf{K} = (\mathbf{A}\mathbf{A}^\top) \odot (\mathbf{Z}\mathbf{Z}^\top)$ and constructs $\mathbf{W} \in \mathbb{R}^{384 \times 384}$.
- `main()`: Fits $\mathbf{W}$ ($\alpha=0.20$) and saves `data/interaction_matrix.npy`.

---

### 5.3 Validation & Ingestion Scripts (`scripts/`)

#### `scripts/validate_umbrella_case.py`
- Runs a synthetic umbrella-retailer CVP through the full scoring pipeline.
- Asserts that the rain/monsoon sub-cluster scores $>0$, the drought sub-cluster scores $<0$, and the unrelated deforestation sub-cluster scores near-zero ($\le 10\%$).

#### `scripts/validate_fact_decomposition.py`
- Tests `extract_facts()` on a multi-clause tax reform article.
- Validates that the article decomposes into two separate facts with opposing polarities.

#### `scripts/validate_scope_fix.py`
- Evaluates real facts stored in `data/real_facts.json` against the relevance gate and per-class-best-match scope rule.
- Confirms the exclusion of non-business noise (e.g., sports studies) and reports the rebalanced geographic distribution.

#### `scripts/ingest_news.py`
- CLI script calling `run_ingestion_once(verbose=True)` for manual execution or cron scheduling.

---

### 5.4 Application Servers & Frontend

#### `server.py`
- **FastAPI Application**: Backend adapting the ML pipeline to HTTP.
- `data_ready()`: Verifies required data artifacts exist.
- `get_state()`: In-memory cache holding news, embeddings, interaction matrix $\mathbf{W}$, and sub-clusters.
- `POST /api/analyze`: Accepts JSON payload `{"cvp": "..."}`, generates CVP embedding, runs `score_submission()`, and returns serialized display scores and breakdowns.
- `GET /`: Serves `web/index.html`.
- Mounts `/static` for static frontend assets.

#### `ingestion_service.py`
- **FastAPI Microservice**: Standalone ingestion scheduler running on port 8502.
- `lifespan`: Spawns an `asyncio` background task that runs `run_ingestion_once()` on startup and repeats every 30 minutes.
- Uses `asyncio.to_thread` to ensure blocking network and embedding tasks do not stall the event loop.
- `GET /health`: Returns last run timestamp, success status, and counts of articles fetched and facts extracted/excluded/added.

#### `app.py`
- Legacy Streamlit implementation featuring dual Plotly radar charts, color-coded vertices, and hierarchical drill-down accordions.

#### `web/index.html`
- Self-contained, zero-build web interface.
- Custom dark-mode styling utilizing CSS design tokens (`Space Grotesk` and `IBM Plex Mono`).
- Uses local vendored Plotly.js (`/static/vendor/plotly.min.js`).
- Features a two-state UI (input card and results dashboard) with side-by-side PESTLE and Porter's radar charts and interactive dimension drill-down accordions.

---

## 6. Submodule Interaction Matrix & Descriptive System Flowcharts

This section provides comprehensive flowcharts formatted in clean ASCII / Unicode block architecture (guaranteed to render perfectly in every markdown editor, browser, and terminal) alongside syntax-validated Mermaid diagrams.

---

### 6.1 Global Submodule Dependency & Interaction Flowchart

```
========================================================================================================================
                                     GLOBAL SYSTEM SUBMODULE INTERACTION MAP
========================================================================================================================

                                         +-----------------------------+
                                         |      src/marketintel/       |
                                         |          config.py          |
                                         | (Dimensions, Paths, Params) |
                                         +--------------+--------------+
                                                        |
         +----------------------------------------------+----------------------------------------------+
         |                                              |                                              |
         v                                              v                                              v
+------------------+                          +-------------------+                          +-------------------+
| src/marketintel/ |                          | src/marketintel/  |                          | src/marketintel/  |
|  embeddings.py   |                          |  data_loader.py   |                          |   atomic_io.py    |
| (all-MiniLM-L6)  |                          | (Safe JSON / NPY) |                          | (Safe .tmp write) |
+--------+---------+                          +---------+---------+                          +---------+---------+
         |                                              |                                              |
         +----------------------+-----------------------+----------------------------------------------+
                                |
+-------------------------------+--------------------------------------------------------------------------------------+
| OFFLINE TRAINING & SENSITIVITY MODELING PIPELINE                                                                     |
|                                                                                                                      |
|   1. generate_news.py ──────► data/news.json & data/news_embeddings.npy (1000 x 384)                                |
|            |                                                                                                         |
|            +──────────────────────┐                                                                                  |
|            v                      v                                                                                  |
|   2. generate_startups.py   3. discover_subclusters.py ──────► data/subclusters.json (Agglomerative + Silhouette)    |
|            |                                                         |                                               |
|            v                                                         |                                               |
|   4. simulate_profit_history.py (hidden_ground_truth.py) ──► data/profit_history.json (180 days daily revenue series)|
|            |                                                         |                                               |
|            +─────────────────────────────────────────────────────────+                                               |
|            v                                                                                                         |
|   5. derive_sensitivity_profiles.py (Lagged Ridge on Delta Profit) ──► Overwrites data/startups.json                 |
|            |                                                                                                         |
|            v                                                                                                         |
|   6. train_interaction_matrix.py (Dual Kernel Ridge Regression) ──► data/interaction_matrix.npy (384 x 384 W)       |
+----------------------------------------------------------------------------------------------------------------------+
                                |
                                +----------------------------------------------------------------+
                                |                                                                |
                                v                                                                v
+-------------------------------------------------------------+ +------------------------------------------------------+
| ONLINE ANALYSIS & SCORING PIPELINE (server.py)              | | REAL-TIME NEWS INGESTION TRACK (ingestion_service.py)|
|                                                             | |                                                      |
| [web/index.html]                                            | | [Sources: BBC, Al Jazeera, Google News, GDELT]       |
|       │                                                     | |       │                                              |
|       ▼ HTTP POST /api/analyze {"cvp": "..."}               | |       ▼ fetch_rss() / fetch_gdelt()                  |
| [server.py]                                                 | | [src/marketintel/ingestion.py]                       |
|       │                                                     | |       │                                              |
|       ▼ embed_text(cvp) -> (384,) ndarray                   | |       ▼ extract_facts()                              |
| [src/marketintel/embeddings.py]                             | | [src/marketintel/fact_extraction.py] (Ollama LLM)    |
|       │                                                     | |       │                                              |
|       ▼ score_submission()                                  | |       ▼ find_duplicate_fact() (48h Window, >= 0.92)  |
| [src/marketintel/analysis.py]                               | | [src/marketintel/ingestion.py]                       |
|       │                                                     | |       │                                              |
|       ├─► compute_gates() [gates = news_emb @ (W @ cvp_emb)]| |       ▼ calibrate_relevance_threshold() (5th perc)   |
|       ├─► subcluster_breakdown_for_dim()                    | | [src/marketintel/seed_inference.py]                  |
|       ├─► raw_dimension_scores() & normalize_for_display()  | |       │                                              |
|       └─► near_zero_dims() [flag < 10% max magnitude]       | |       ├─► infer_relevance() & infer_categorical()    |
|       │                                                     | |       └─► infer_scope_best_match() (Per-Class Best)  |
|       ▼ HTTP 200 JSON Response                              | |       │                                              |
| [web/index.html] -> Plotly Radar Charts & Drilldown View    | |       ▼ atomic_write_json() & atomic_write_npy()     |
|                                                             | | [data/real_articles.json & real_facts.json]          |
+-------------------------------------------------------------+ +------------------------------------------------------+
========================================================================================================================
```

---

### 6.2 Detailed Flowchart: Offline Training & Sensitivity Modeling

```
+----------------------------------------------------------------------------------------------------------------------+
| STEP 1: GENERATE SEED NEWS & EMBEDDINGS (scripts/generate_news.py)                                                   |
|                                                                                                                      |
|  [Templates + Entity Sampling] ──► 1000 Articles (Title, Body, Scope, Polarity, 11-Dim Relevance Scores)            |
|                                         │                                                                            |
|                                         ▼                                                                            |
|                             embed_texts(texts) via all-MiniLM-L6-v2                                                  |
|                                         │                                                                            |
|                                         ▼                                                                            |
|                 Saves: data/news.json (744 KB) & data/news_embeddings.npy (1000 x 384)                               |
+----------------------------------------------------------------------------------------------------------------------+
                                                  │
                                                  ├──────────────────────────────────────────────┐
                                                  ▼                                              ▼
+------------------------------------------------------------------+ +-------------------------------------------------+
| STEP 2: GENERATE STARTUPS (scripts/generate_startups.py)         | | STEP 3: DISCOVER SUB-CLUSTERS                   |
|                                                                  | | (scripts/discover_subclusters.py)               |
|  [20 Startup CVP Definitions]                                    | |                                                 |
|               │                                                  | | For each of the 11 dimensions:                  |
|               ▼                                                  | |   1. Filter news where relevance > 0.30         |
|  Link 3-5 justifying news articles matching dominant dimensions  | |   2. AgglomerativeClustering(k in [3..7], cosine)|
|               │                                                  | |   3. Pick smallest k within 90% max silhouette  |
|               ▼                                                  | |   4. Centroid -> Top 3 titles -> Top 2 keywords |
|  embed_texts(cvp_list) ──► (20, 384) L2-normalized array         | |                                                 |
|               │                                                  | | Saves: data/subclusters.json                    |
|               ▼                                                  | |        (k, labels, article assignment mapping)  |
|  Saves: data/startups.json & data/startup_embeddings.npy         | +-------------------------------------------------+
+------------------------------------------------------------------+                          │
                                                  │                                           │
                                                  ▼                                           │
+----------------------------------------------------------------------------------+          │
| STEP 4: SIMULATE 180-DAY PROFIT HISTORIES (scripts/simulate_profit_history.py)   |          │
|                                                                                  |          │
|  For each startup:                                                               |          │
|    Profit(t) = BaseRevenue + Trend*t + GaussianNoise(4%)                         |          │
|    On day (t_news + shock_lag_days):                                             |          │
|       Inject shock: sum(Relevance * HiddenSensitivity / 100) * Polarity * Scale  |          │
|                                                                                  |          │
|  Saves: data/profit_history.json (20 startups x 180 daily revenue observations)  |          │
+----------------------------------------------------------------------------------+          │
                                                  │                                           │
                                                  └────────────────────┬──────────────────────┘
                                                                       ▼
+----------------------------------------------------------------------------------------------------------------------+
| STEP 5: DERIVE SENSITIVITY PROFILES VIA SUB-CLUSTER LAGGED RIDGE (scripts/derive_sensitivity_profiles.py)            |
|                                                                                                                      |
|  1. Construct Daily Event Signal Matrix X_tau (180 x M sub-cluster features)                                         |
|  2. For candidate lags in [1, 3, 7, 14] days:                                                                        |
|        Solve Ridge: Delta_Profit = X_tau @ beta + beta_0   (alpha = 4.0, intercept unpenalized)                     |
|        Select optimal lag tau* = argmax R^2                                                                          |
|  3. Roll up sub-cluster coefficients to 11 parent dimensions & rescale max magnitude to 100.0                        |
|  4. Validate: Recovered lags match 20/20 true lags; pooled correlation vs hidden templates = ~0.90                   |
|                                                                                                                      |
|  Overwrites: Derived PESTLE & Porter's sensitivity profiles into data/startups.json                                  |
+----------------------------------------------------------------------------------------------------------------------+
                                                                       │
                                                                       ▼
+----------------------------------------------------------------------------------------------------------------------+
| STEP 6: TRAIN BILINEAR INTERACTION MATRIX W (scripts/train_interaction_matrix.py)                                    |
|                                                                                                                      |
|  1. Form 220 training examples: Combined News Vectors a_sd (384-d), Startup CVP z_s (384-d), Targets y_sd            |
|  2. Compute Dual Kernel Gram Matrix: K_ij = (a_i . a_j) * (z_i . z_j)  [Hadamard product of Gram matrices]           |
|  3. Solve Dual Weights: alpha = (K + 0.2 * I)^(-1) @ y                                                               |
|  4. Assemble Bilinear Operator: W = sum_j (alpha_j * outer(a_j, z_j))  in R^(384 x 384)                              |
|                                                                                                                      |
|  Saves: data/interaction_matrix.npy (1.18 MB matrix)                                                                 |
+----------------------------------------------------------------------------------------------------------------------+
```

---

### 6.3 Detailed Flowchart: Real-Time News Ingestion & Fact Processing

```
========================================================================================================================
                          REAL-TIME NEWS INGESTION & FACT PROCESSING PIPELINE
========================================================================================================================

                                  [ Trigger: ingestion_service.py (Every 30 min) ]
                                  [        OR scripts/ingest_news.py (Manual)    ]
                                                         │
                                                         ▼
                                 +-----------------------------------------------+
                                 | Fetch from Free, Keyless Global News Feeds:   |
                                 | - BBC World RSS                               |
                                 | - Al Jazeera RSS                              |
                                 | - Google News Topic WORLD RSS                 |
                                 | - GDELT DOC 2.0 API (via gdeltdoc)            |
                                 +-----------------------+-----------------------+
                                                         │
                                                         ▼
                                 +-----------------------------------------------+
                                 | Fact Decomposition (fact_extraction.py):      |
                                 | POST to local Ollama LLM (llama3.2:3b)        |
                                 | Prompt: Extract atomic, neutral claims        |
                                 +-----------------------+-----------------------+
                                                         │
                                    ┌────────────────────┴────────────────────┐
                          [Ollama Success]                          [Ollama Offline / Timeout]
                                    │                                         │
                                    ▼                                         ▼
                     [Parsed Array of Fact Strings]             [Fallback: Use full title as 1 fact]
                                    │                                         │
                                    └────────────────────┬────────────────────┘
                                                         │
                                                         ▼
                                 +-----------------------------------------------+
                                 | Embed Fact via Sentence-Transformers:         |
                                 | embed_text(fact) -> (384,) L2-normalized      |
                                 +-----------------------+-----------------------+
                                                         │
                                                         ▼
                                 +-----------------------------------------------+
                                 | 48-Hour Semantic Deduplication:               |
                                 | Compare vs. stored facts in rolling 48h window|
                                 +-----------------------+-----------------------+
                                                         │
                                    ┌────────────────────┴────────────────────┐
                       [Cosine Sim >= 0.92]                      [Cosine Sim < 0.92]
                                    │                                         │
                                    ▼                                         ▼
                     [Increment mention_count]                  +-------------------------------+
                     [Update last_seen timestamp]               | Seed Corpus k-NN Transfer:    |
                     [Link to parent article]                   | Dot-product vs 1000 seed embs |
                                                                | Retrieve top 10 neighbors     |
                                                                +---------------+---------------+
                                                                                │
                                                                                ▼
                                                                +-------------------------------+
                                                                | Compute Inferred Relevance:   |
                                                                | Soft-weighted vote across 11  |
                                                                | dimensions                    |
                                                                +---------------+---------------+
                                                                                │
                                                                                ▼
                                                                +-------------------------------+
                                                                | Relevance Gate Check:         |
                                                                | Max relevance >= 5th perc     |
                                                                | seed threshold (~0.58)?       |
                                                                +---------------+---------------+
                                                                                │
                                                   ┌────────────────────────────┴────────────────────────────┐
                                              [Passed Gate]                                             [Failed Gate]
                                                   │                                                         │
                                                   ▼                                                         ▼
                                    +------------------------------+                          [Discard from downstream]
                                    | 1. Infer Polarity:           |                          [Append to excluded log: ]
                                    |    Weighted plurality vote   |                          [ingestion_excluded.jsonl]
                                    |                              |
                                    | 2. Infer Scope:              |
                                    |    Per-Class-Best-Match      |
                                    |    (Highest individual sim   |
                                    |     among 7 scope partitions)|
                                    +--------------+---------------+
                                                   │
                                                   ▼
                                    +------------------------------+
                                    | Assemble Structured Records: |
                                    | - fact_XXXXX record          |
                                    | - article_XXXXX record       |
                                    +--------------+---------------+
                                                   │
                                                   ▼
                                    +------------------------------+
                                    | Atomic IO Persistence:       |
                                    | atomic_write_json() & npy()  |
                                    | - data/real_articles.json    |
                                    | - data/real_facts.json       |
                                    | - data/real_fact_embeddings  |
                                    +------------------------------+
========================================================================================================================
```

---

### 6.4 Detailed Flowchart: Online CVP Inference & Two-Tier Scoring Engine

```
========================================================================================================================
                               ONLINE CVP INFERENCE & EXPLAINABLE DRILL-DOWN FLOW
========================================================================================================================

 [ User / Founder ]
        │
        │ 1. Pastes CVP text (e.g. "Mobile app providing Punjab farmers real-time soil moisture and crop advice...")
        ▼
 [ web/index.html (Client Frontend) ]
        │
        │ 2. Dispatches JSON payload: POST /api/analyze { "cvp": "..." }
        ▼
 [ server.py (FastAPI Server on Port 8000) ]
        │
        │ 3. embed_text(cvp)
        ▼
 [ src/marketintel/embeddings.py ]
        │
        │ 4. Returns 384-dimensional unit vector z_cvp
        ▼
 [ server.py ]
        │
        │ 5. Calls score_submission(news, news_embeddings, z_cvp, W, subclusters)
        ▼
 [ src/marketintel/analysis.py (Analysis Engine) ]
        │
        ├────────────────────────────────────────────────────────────────────────────────────────┐
        │                                                                                        │
        ▼                                                                                        ▼
 [ Vectorized Interaction Gate ]                                          [ Sub-Cluster Contribution Breakdown ]
   gate_i = news_emb_i @ (W @ z_cvp)                                        For each dimension d in (PESTLE + Porter's):
   Evaluates all 1000 articles at once                                         For each article i in dimension's sub-clusters:
   Produces (1000,) scalar gate array                                            contribution = relevance_i * polarity_i * gate_i
        │                                                                        Group by sub-cluster id -> Sum raw scores
        │                                                                        Sort top 5 contributing articles per cluster
        └────────────────────────────────────────────────────────────────────────────────────────┘
                                                         │
                                                         ▼
                                         [ Dimension Roll-Up & Scaling ]
                                         - Raw Dimension Score = Sum of its Sub-Cluster Scores
                                         - normalize_for_display(): Scale largest magnitude to 100.0
                                         - near_zero_dims(): Flag dimensions with |score| < 10% max magnitude
                                                         │
                                                         ▼
 [ server.py (Serialization) ]
        │
        │ 6. serialize_breakdown(): Orders dimensions by descending absolute impact
        │ 7. Returns HTTP 200 JSON Response
        ▼
 [ web/index.html (Browser UI) ]
        │
        ├─► Renders PESTLE Radar Chart (Hexagon: Green=Positive, Red=Negative, Grey=Negligible)
        ├─► Renders Porter's Five Forces Radar Chart (Pentagon)
        ├─► Renders Impact Dimension Accordions (sorted by absolute exposure)
        └─► Expands Sub-Clusters with visual contribution progress bars and specific justifying news articles
========================================================================================================================
```

---

### 6.5 Submodule Input/Output Contract & Tensor Shape Matrix

| Submodule | Function / Entry Point | Input Parameters & Types | Output Return & Types | Consumed File(s) | Produced / Modified File(s) |
|---|---|---|---|---|---|
| **`embeddings.py`** | `get_model()` | None | `SentenceTransformer` instance | Local model cache | None |
| **`embeddings.py`** | `embed_texts(texts)` | `texts: list[str]` | `np.ndarray` of shape `(N, 384)`, $L_2$-normalized | None | None |
| **`embeddings.py`** | `embed_text(text)` | `text: str` | `np.ndarray` of shape `(384,)`, $L_2$-normalized | None | None |
| **`data_loader.py`** | `load_news()` | None | `tuple[list[dict], np.ndarray (1000, 384)]` | `data/news.json`, `data/news_embeddings.npy` | None |
| **`data_loader.py`** | `load_startups()` | None | `tuple[list[dict], np.ndarray (20, 384)]` | `data/startups.json`, `data/startup_embeddings.npy` | None |
| **`data_loader.py`** | `load_interaction_matrix()` | None | `np.ndarray` of shape `(384, 384)` | `data/interaction_matrix.npy` | None |
| **`data_loader.py`** | `load_subclusters()` | None | `dict` containing 11 dimension clusters | `data/subclusters.json` | None |
| **`data_loader.py`** | `load_real_facts()` | None | `tuple[list[dict], np.ndarray (N, 384)]` | `data/real_facts.json`, `data/real_fact_embeddings.npy` | None |
| **`atomic_io.py`** | `atomic_write_json(path, data)` | `path: Path, data: Any` | `None` (atomic file replacement) | None | Target JSON file via `.tmp` |
| **`atomic_io.py`** | `atomic_write_npy(path, array)` | `path: Path, array: np.ndarray` | `None` (atomic file replacement) | None | Target `.npy` file via `.tmp` |
| **`analysis.py`** | `compute_gates(news_emb, cvp_emb, W)` | `news_emb: (N, 384)`, `cvp_emb: (384,)`, `W: (384, 384)` | `np.ndarray` of shape `(N,)` | None | None |
| **`analysis.py`** | `subcluster_breakdown_for_dim(...)` | `news: list`, `gates: (N,)`, `dim: str`, `score_field: str`, `dim_subclusters: dict` | `list[dict]` sorted by `abs(raw_score)` | None | None |
| **`analysis.py`** | `score_submission(news, news_emb, cvp_emb, W, subclusters)` | All datasets + embeddings + interaction matrix | `dict` (display scores, breakdowns, near-zero set) | None | None |
| **`fact_extraction.py`** | `extract_facts(text)` | `text: str` (article headline or text) | `list[str]` (one or more neutral atomic claims) | None | None |
| **`seed_inference.py`** | `nearest_neighbors(emb, seed_embs, k=10)` | `emb: (384,)`, `seed_embs: (1000, 384)` | `tuple[top_idx: (10,), weights: (10,)]` | None | None |
| **`seed_inference.py`** | `infer_relevance(seed_news, top_idx, weights)` | Neighbor indices and weights | `dict[str, float]` across all 11 dimensions | None | None |
| **`seed_inference.py`** | `calibrate_relevance_threshold(seed_news)` | `seed_news: list[dict]` | `float` (5th percentile threshold $\approx 0.58$) | None | None |
| **`seed_inference.py`** | `infer_scope_best_match(emb, seed_embs, scope_idx)` | `emb: (384,)`, `seed_embs: (1000, 384)`, `scope_idx: dict` | `tuple[best_scope: str, best_sim: float]` | None | None |
| **`ingestion.py`** | `run_ingestion_once(verbose=True)` | `verbose: bool` | `dict` (ingestion metrics summary) | RSS & GDELT, `data/ingestion_state.json` | `data/real_articles.json`, `data/real_facts.json`, `data/real_fact_embeddings.npy`, logs |
| **`discover_subclusters.py`** | `best_clustering(embs, k_range)` | `embs: (M, 384)`, `k_range: list[int]` | `tuple[best_k: int, labels: ndarray, silhouette: float]` | None | None |
| **`discover_subclusters.py`** | `label_cluster(articles, embs, member_idx)` | Cluster members and embeddings | `str` (2-word capitalized n-gram label) | None | None |
| **`derive_sensitivity_profiles.py`** | `fit_lag_ridge(profit, signal, lag, alpha=4.0)` | `profit: (180,)`, `signal: (180, M)`, `lag: int` | `tuple[r_squared: float, coef: (M,)]` | None | None |
| **`train_interaction_matrix.py`** | `fit_interaction_matrix(A, Z, targets, alpha=0.2)` | `A: (220, 384)`, `Z: (220, 384)`, `targets: (220,)` | `tuple[W: (384, 384), predictions: (220,)]` | None | `data/interaction_matrix.npy` |
| **`server.py`** | `POST /api/analyze` | `AnalyzeRequest { cvp: str }` | `JSON` payload with display scores & breakdowns | In-memory cached artifacts | None |
| **`ingestion_service.py`** | `GET /health` | None | `JSON` status of last ingestion run | None | None |
