# AI-Based Explainable Market Intelligence — Comprehensive Codebase Architecture & Code Walkthrough

This document provides a deep, granular walkthrough of the entire **AI-Based Explainable Market Intelligence** codebase. It breaks down the mathematical foundations, system architecture, data generation, machine learning algorithms, and provides an exhaustive line-by-line / block-by-block explanation of every module and function.

---

## Table of Contents
1. [High-Level System Architecture & Operating Mechanics](#1-high-level-system-architecture--operating-mechanics)
2. [Hierarchical Clustering & Multi-Level News Labelling](#2-hierarchical-clustering--multi-level-news-labelling)
3. [End-to-End Mathematical & ML Formulations](#3-end-to-end-mathematical--ml-formulations)
4. [File-by-File, Module-by-Module, Function-by-Function Codebase Walkthrough](#4-file-by-file-module-by-module-function-by-function-codebase-walkthrough)
   - [4.1 `src/marketintel/config.py`](#41-srcmarketintelconfigpy)
   - [4.2 `src/marketintel/embeddings.py`](#42-srcmarketintelembeddingspy)
   - [4.3 `src/marketintel/data_loader.py`](#43-srcmarketinteldata_loaderpy)
   - [4.4 `src/marketintel/analysis.py`](#44-srcmarketintelanalysispy)
   - [4.5 `scripts/hidden_ground_truth.py`](#45-scriptshidden_ground_truthpy)
   - [4.6 `scripts/generate_news.py`](#46-scriptsgenerate_newspy)
   - [4.7 `scripts/generate_startups.py`](#47-scriptsgenerate_startupspy)
   - [4.8 `scripts/discover_subclusters.py`](#48-scriptsdiscover_subclusterspy)
   - [4.9 `scripts/simulate_profit_history.py`](#49-scriptssimulate_profit_historypy)
   - [4.10 `scripts/derive_sensitivity_profiles.py`](#410-scriptsderive_sensitivity_profilespy)
   - [4.11 `scripts/train_interaction_matrix.py`](#411-scriptstrain_interaction_matrixpy)
   - [4.12 `scripts/validate_umbrella_case.py`](#412-scriptsvalidate_umbrella_casepy)
   - [4.13 `app.py`](#413-apppy)
5. [Data Pipeline Flow & Transformation Lifecycle](#5-data-pipeline-flow--transformation-lifecycle)

---

## 1. High-Level System Architecture & Operating Mechanics

### 1.1 The Core Problem
Early-stage startups have **no sales or financial history** to learn from. However, founders and investors need to know how macroeconomic, industry, regulatory, and environmental events will impact a specific company based purely on its **Core Value Proposition (CVP)** / positioning.

Traditional systems either:
1. Assign broad, static categorical scores with zero traceability, or
2. Rely on black-box sentiment classification without company-specific context.

### 1.2 The System Solution
This system solves the problem using an **explainable, two-tower bilinear interaction architecture** across 11 strategic dimensions:
- **6 PESTLE Dimensions**: Political, Economic, Social, Technological, Legal, Environmental.
- **5 Porter's Five Forces**: Threat of New Entrants, Supplier Power, Buyer Power, Threat of Substitutes, Competitive Rivalry.

```
+----------------------------------------------------------------------------------------------------+
|                                           OFFLINE PIPELINE                                         |
|                                                                                                    |
|  1. generate_news.py                 2. generate_startups.py           3. discover_subclusters.py  |
|     [1000 News + Embeddings]            [20 Startups + CVPs]              [Agglomerative Clusters]  |
|               │                                   │                                   │            |
|               ▼                                   ▼                                   │            |
|  4. simulate_profit_history.py  ◄─────────────────┴───────────────────────────────────┤            |
|     [Inject Hidden Shocks into 180-day Daily Profit Series]                           │            |
|               │                                                                       │            |
|               ▼                                                                       ▼            |
|  5. derive_sensitivity_profiles.py ───────────────────────────────────────────────────┘            |
|     [Sub-cluster Lagged Ridge Regression recovers Startup Profiles from Profit Changes]             |
|               │                                                                                    |
|               ▼                                                                                    |
|  6. train_interaction_matrix.py                                                                    |
|     [Kernel Dual Ridge Regression trains 384x384 Interaction Matrix W]                             |
+-------------------------------------------------+--------------------------------------------------+
                                                  │
                                                  ▼
+-------------------------------------------------+--------------------------------------------------+
|                                           ONLINE INFERENCE                                         |
|                                                                                                    |
|  User CVP Text ──► embed_text() ──► cvp_embedding (384-d)                                          |
|                                            │                                                       |
|                                            ▼                                                       |
|                     gate(news_i, CVP) = news_emb_i · W · cvp_embedding                             |
|                                            │                                                       |
|                                            ▼                                                       |
|          contribution = relevance(news_i, dim) × polarity(news_i) × gate(news_i, CVP)              |
|                                            │                                                       |
|                                            ▼                                                       |
|           Sub-cluster Totals ──► Dimension Roll-up ──► Normalization (Max 100)                     |
|                                            │                                                       |
|                                            ▼                                                       |
|                Streamlit UI: Hexagon & Pentagon Radar Charts + Drill-Down Explanations             |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Hierarchical Clustering & Multi-Level News Labelling

The core explainability mechanism relies on **hierarchical multi-level structuring and labeling** of every single news article. Here is how news labeling works across every level:

```
Level 0: Raw Article Generation (Continuous Soft Multi-Dimensional Relevance + Polarity)
   │
   ├── Level 1: Dimension Filtering (Hard thresholding at relevance > 0.3)
   │      │
   │      └── Level 2: Sub-Cluster Discovery (Unsupervised Agglomerative Clustering)
   │             │
   │             └── Centroid N-Gram Label Extraction (Human-readable Sub-Topic Naming)
```

### Level 0: Multi-Dimensional Soft Ground Truth & Polarity
Unlike traditional classification where an article is pigeonholed into a single category (e.g., "Political"), real-world events have multi-faceted effects.
- **PESTLE Vector**: 6 continuous values in $[0.0, 1.0]$.
- **Porter's Vector**: 5 continuous values in $[0.0, 1.0]$.
- **Polarity**: Binary directional state ($+1.0$ for `"positive"`, $-1.0$ for `"negative"`).
- **Scope**: Geographic tag (`"LPU"`, `"Phagwara"`, `"Jalandhar"`, `"Kapurthala"`, `"Punjab"`, `"India"`, `"World"`).

*Example*: A tariff announcement in Punjab receives high scores on both **Political** ($0.90$) and **Economic** ($0.80$), along with **Supplier Power** ($0.60$) and **Threat of New Entrants** ($0.30$).

### Level 1: Dimension Partitioning & Cross-Membership
Clustering is performed **independently per dimension**.
- For each dimension $d \in \text{PESTLE} \cup \text{Porter's}$, the system selects all articles satisfying:
  $$\text{relevance}(a, d) > \text{SUBCLUSTER\_RELEVANCE\_THRESHOLD} \quad (0.30)$$
- **Cross-Membership**: Because an article can be relevant to multiple dimensions, it participates in the clustering of multiple dimensions and can be assigned to different sub-clusters under each.

### Level 2: Semantic Sub-Clustering via Agglomerative Clustering
For all article embeddings belonging to a dimension:
1. **Distance Metric**: Cosine distance ($1 - \cos(\mathbf{u}, \mathbf{v})$) between $L_2$-normalized 384-dimensional `all-MiniLM-L6-v2` embeddings.
2. **Linkage Criterion**: `average` linkage (UPGMA).
3. **Adaptive Cluster Count Selection (`best_clustering`)**:
   - Tests candidate cluster counts $k \in [3, 4, 5, 6, 7]$.
   - Computes the Cosine Silhouette Score $S(k)$.
   - **Tuning Heuristic**: Rather than a naive $\arg\max_k S(k)$ (which suffers from severe short-text bias toward splitting into near-singletons), the algorithm chooses the **smallest $k$** that achieves at least **90% (`tolerance = 0.90`)** of the maximum silhouette score:
     $$k^* = \min \{ k \mid S(k) \ge 0.90 \cdot \max_{j} S(j) \}$$

### Level 3: Sub-Cluster Label Generation (`label_cluster`)
Sub-cluster names are **not hardcoded**; they are derived unsupervised from the articles closest to each cluster's semantic center:
1. **Centroid Calculation**:
   $$\mathbf{c} = \frac{1}{|C|} \sum_{i \in C} \mathbf{e}_i$$
2. **Representative Article Retrieval**:
   Computes cosine similarity between all cluster members and the centroid $\mathbf{c}$. Retrieves the top 3 closest articles.
3. **Keyword Extraction & Stopword Pruning**:
   - Collects titles of the 3 nearest articles.
   - Extracts all alphabetic tokens (`[A-Za-z']+`).
   - Discards short tokens ($\le 3$ characters) and 30+ domain stopwords (`the`, `with`, `amid`, `across`, `into`, etc.).
4. **N-Gram Synthesis**:
   - Counts word occurrences using `Counter`.
   - Takes the top 2 most frequent title keywords and capitalizes them (e.g., `"Tariffs Rattle"`, `"Visa Immigration"`, `"Recession Fears"`, `"Monsoon Sowing"`).
   - If no words qualify, falls back to the exact title of the nearest article.

---

## 3. End-to-End Mathematical & ML Formulations

### 3.1 The Bilinear Interaction Operator $W$
The interaction between a business concept (CVP) and an event (News) is parameterized by a matrix $\mathbf{W} \in \mathbb{R}^{384 \times 384}$.

For any news embedding $\mathbf{x} \in \mathbb{R}^{384}$ and CVP embedding $\mathbf{z} \in \mathbb{R}^{384}$:
$$\text{gate}(\mathbf{x}, \mathbf{z}) = \mathbf{x}^\top \mathbf{W} \mathbf{z}$$

### 3.2 Dual Ridge Regression Formulation
Fitting $\mathbf{W}$ directly in the primal space would require solving a $(384 \times 384) = 147,456$-dimensional linear regression over only $N = 20 \times 11 = 220$ training instances.

To solve this efficiently and prevent rank degeneracy:
1. **Combined News Vector** for startup $s$ and dimension $d$:
   $$\mathbf{a}_{s, d} = \sum_{j \in \text{Linked}(s)} \text{relevance}(j, d) \cdot \text{polarity}(j) \cdot \mathbf{x}_j$$
2. **Kronecker / Outer Product Equivalence**:
   The prediction is:
   $$\hat{y}_{s, d} = \mathbf{a}_{s, d}^\top \mathbf{W} \mathbf{z}_s = \text{vec}(\mathbf{a}_{s, d} \mathbf{z}_s^\top)^\top \text{vec}(\mathbf{W})$$
3. **Dual Kernel Gram Matrix**:
   Using the tensor contraction identity $(\mathbf{a}_1 \otimes \mathbf{b}_1)^\top (\mathbf{a}_2 \otimes \mathbf{b}_2) = (\mathbf{a}_1^\top \mathbf{a}_2)(\mathbf{b}_1^\top \mathbf{b}_2)$:
   $$\mathbf{K}_{ij} = (\mathbf{a}_i^\top \mathbf{a}_j) \cdot (\mathbf{z}_i^\top \mathbf{z}_j)$$
4. **Dual Solve**:
   $$\boldsymbol{\alpha} = (\mathbf{K} + \lambda \mathbf{I}_{N})^{-1} \mathbf{y}$$
   $$\mathbf{W} = \sum_{i=1}^N \alpha_i (\mathbf{a}_i \mathbf{z}_i^\top)$$
   where $\lambda = \text{RIDGE\_ALPHA} = 0.20$.

### 3.3 Sub-Cluster Lagged Profile Recovery
To generate realistic, non-handcrafted training targets $\mathbf{y}$, the system:
1. Simulates daily revenue/profit series over 180 days with hidden shock delays:
   $$\text{Profit}_s(t) = \text{Base}_s + g_s \cdot t + \epsilon(t) + \sum_{a \in \text{News}} \text{Shock}(a, s, t - \tau_s)$$
2. Forms a design matrix $\mathbf{X}_\tau \in \mathbb{R}^{T \times M}$ where each column corresponds to a specific sub-cluster $(\text{dimension}, \text{subcluster\_id})$:
   $$\mathbf{X}_\tau[t, m] = \sum_{a \in \text{News published on } t - \tau, a \in m} \text{relevance}(a, d) \cdot \text{polarity}(a)$$
3. Solves the lagged Ridge Regression on daily profit differences $\Delta \text{Profit}(t)$:
   $$\boldsymbol{\beta}_\tau = (\mathbf{X}_\tau^\top \mathbf{X}_\tau + \lambda_{\text{profile}} \mathbf{I})^{-1} \mathbf{X}_\tau^\top \Delta \text{Profit}$$
4. Finds the optimal lag $\tau^* = \arg\max_\tau R^2(\tau)$, sums the sub-cluster coefficients up to each dimension, and scales the vector to $[-100, +100]$.

---

## 4. File-by-File, Module-by-Module, Function-by-Function Codebase Walkthrough

---

### 4.1 `src/marketintel/config.py`

#### Purpose
The single source of truth for configuration constants, dimension definitions, paths, and hyperparameters.

#### Line-by-Line / Block Explanation
- **Lines 1–27**: Defines the 6 `PESTLE_DIMS` and 5 `PORTERS_DIMS` lists, along with human-readable display label dictionaries `PESTLE_LABELS` and `PORTERS_LABELS`.
- **Lines 28–39**: Defines `SCOPES` (geographic tags) and `SCOPE_WEIGHTS`. Reflects real-world news distributions with broader scopes (`"India"`, `"World"`) weighted higher than hyper-local ones (`"LPU"`, `"Phagwara"`).
- **Line 41**: `EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"` specifies the sentence-transformers model.
- **Lines 43–51**: Constructs platform-agnostic `pathlib.Path` objects for all project directories and data files (`data/news.json`, `data/news_embeddings.npy`, `data/startups.json`, `data/subclusters.json`, `data/interaction_matrix.npy`, `data/profit_history.json`).
- **Lines 53–59**: 
  - `SUBCLUSTER_RELEVANCE_THRESHOLD = 0.3`: Threshold above which an article participates in a dimension's clustering.
  - `SUBCLUSTER_K_RANGE = [3, 4, 5, 6, 7]`: Number of candidate clusters evaluated per dimension.
- **Lines 61–74**:
  - `PROFILE_REGRESSION_ALPHA = 4.0`: Regularization penalty for sub-cluster profile recovery.
  - `N_PROFIT_DAYS = 180`: Length of simulated profit time-series.
  - `CANDIDATE_LAGS = [1, 3, 7, 14]`: Candidate delay windows in days.
- **Lines 76–87**:
  - `N_NEWS_ARTICLES = 1000`: Number of fabricated news events.
  - `TOP_K_STARTUPS = 3`: Reference startup retrieval count.
  - `RIDGE_ALPHA = 0.2`: Regularization parameter for the interaction matrix $W$, chosen via leave-one-startup-out cross-validation.
- **Lines 89–92**:
  - `NEAR_ZERO_FRACTION = 0.10`: Dimensions with magnitude $< 10\%$ of the maximum dimension score are marked as negligible / neutral.

---

### 4.2 `src/marketintel/embeddings.py`

#### Purpose
Provides cached access to the sentence-transformers model and utilities for generating $L_2$-normalized vector representations.

#### Functions
- `get_model()`
  - Uses `@lru_cache(maxsize=1)` so the ~90MB `all-MiniLM-L6-v2` neural model is only loaded into memory once during the application lifecycle.
- `embed_texts(texts: list[str]) -> np.ndarray`
  - Encodes a batch of string inputs with `normalize_embeddings=True` (ensuring $\|\mathbf{v}\|_2 = 1.0$ so that dot products equal cosine similarities).
- `embed_text(text: str) -> np.ndarray`
  - Encodes a single string input, returning a 1D NumPy array of shape `(384,)`.

---

### 4.3 `src/marketintel/data_loader.py`

#### Purpose
Centralized, safe IO routines for loading datasets, embeddings, matrices, and sub-cluster JSON hierarchies.

#### Functions
- `load_news() -> tuple[list[dict], np.ndarray]`: Reads `data/news.json` and loads `data/news_embeddings.npy`.
- `load_startups() -> tuple[list[dict], np.ndarray]`: Reads `data/startups.json` and loads `data/startup_embeddings.npy`.
- `news_by_id(news: list[dict]) -> dict[str, dict]`: Constructs a fast $O(1)$ lookup hashmap mapping `article["id"]` to article objects.
- `load_interaction_matrix() -> np.ndarray`: Loads `data/interaction_matrix.npy` (shape $384 \times 384$).
- `load_subclusters() -> dict`: Reads `data/subclusters.json`.

---

### 4.4 `src/marketintel/analysis.py`

#### Purpose
The core inference engine that executes the multi-level scoring, gating, sub-cluster aggregation, and normalization pipeline for any query CVP.

#### Functions
- `polarity_sign(article: dict) -> float`
  - Converts `"positive"` to `+1.0` and `"negative"` to `-1.0`.
- `compute_gates(news_embeddings: np.ndarray, cvp_embedding: np.ndarray, W: np.ndarray) -> np.ndarray`
  - Vectorized matrix computation: `news_embeddings @ (W @ cvp_embedding)`.
  - Computes $\text{gate}_i = \mathbf{x}_i^\top \mathbf{W} \mathbf{z}$ for all 1000 articles simultaneously in milliseconds.
- `subcluster_breakdown_for_dim(news, gates, dim, score_field, dim_subclusters, top_n_articles=5) -> list[dict]`
  - Iterates over all news articles. If the article has an assignment in `dim_subclusters["assignments"]`, calculates:
    $$\text{contribution}_i = \text{relevance}_i \times \text{polarity\_sign}_i \times \text{gate}_i$$
  - Aggregates contributions into their respective sub-clusters.
  - Returns a list of sub-clusters sorted by descending absolute raw score, with the top 5 contributing articles per cluster.
- `dimension_breakdowns(news, gates, dims, score_field, subclusters) -> dict`
  - Runs `subcluster_breakdown_for_dim` across all dimensions in `dims`.
- `raw_dimension_scores(breakdown: dict) -> dict`
  - Sums sub-cluster scores up to parent dimension scores: $\text{RawScore}(d) = \sum_{c \in C_d} \text{RawScore}(c)$.
- `normalize_for_display(raw_scores: dict) -> dict`
  - Scales dimension scores so the largest absolute value equals $100.0$, preserving positive/negative signs.
- `near_zero_dims(raw_pestle: dict, raw_porters: dict, fraction: float = NEAR_ZERO_FRACTION) -> set[str]`
  - Calculates global max magnitude across all 11 dimensions. Returns any dimension whose score is $< 10\%$ of the maximum, flagging them as negligible.
- `score_submission(news, news_embeddings, cvp_embedding, W, subclusters) -> dict`
  - Coordinates the complete analysis workflow and returns the display-ready dictionary.

---

### 4.5 `scripts/hidden_ground_truth.py`

#### Purpose
Defines domain-grounded hidden sensitivity profiles and shock lags for all 20 reference startups. **Never imported during model training or inference**; solely used by `simulate_profit_history.py` to generate synthetic financial records and by `derive_sensitivity_profiles.py` to benchmark recovery accuracy.

#### Logic & Structure
- `HIDDEN_TEMPLATES`: A dictionary of 20 startups mapping to specific domain-consistent sensitivities. For example:
  - `RupeeRail` (fintech micro-loans): High negative legal ($-70$) and political ($-60$) exposure; high positive technological ($+50$) exposure.
  - `Wattlefy` (hardware smart energy): High negative supplier power ($-70$) and economic ($-60$) sensitivity.
- `shock_lag_days`: Deterministically assigned by cycling through `[1, 3, 7, 14]` across startups ($i \pmod 4$) to thoroughly test all lag recovery regimes.

---

### 4.6 `scripts/generate_news.py`

#### Purpose
Synthesizes 1000 realistic news events with multi-dimensional PESTLE/Porter's relevance scores, assigns dates and polarities, and computes their 384-dimensional embeddings.

#### Key Components & Functions
- **Entity Vocabularies** (`SECTORS`, `TECHS`, `COMPANIES`, `COUNTRIES`, `INDIAN_CITIES`, `PUNJAB_TOWNS`, `REGULATIONS`): Realistic Indian and global business entities used for dynamic template filling.
- `TEMPLATES`: Comprehensive catalog of parameterized news story templates containing base scores, polarity probabilities, and geographic applicability.
- `clip01(x: float) -> float`: Clamps values to $[0.0, 1.0]$.
- `build_scores(base: dict, dims: list[str], rng: random.Random) -> dict`: Injects uniform jitter ($\pm 0.08$) into defined base scores and fills non-active dimensions with low baseline noise ($0.02 - 0.12$).
- `weighted_scope(rng: random.Random) -> str`: Selects geographic scope based on realistic distribution weights (`SCOPE_WEIGHTS`).
- `generate_articles(n: int, rng: random.Random) -> list[dict]`: Assembles $N$ articles with unique IDs (`news_0001` to `news_1000`), formatted dates over the preceding 180 days, filled text, and score vectors.
- `main()`: Generates articles, writes `data/news.json`, computes sentence embeddings for all `"title. body"` strings, and writes `data/news_embeddings.npy`.

---

### 4.7 `scripts/generate_startups.py`

#### Purpose
Creates the 20 reference startups with CVPs, finds justifying news articles from `data/news.json` for each startup, embeds their CVPs, and saves them to `data/startups.json`.

#### Functions
- `STARTUPS`: List of 20 detailed Indian startup concepts spanning fintech, edtech, agritech, SaaS, healthtech, and D2C hardware.
- `dims_by_magnitude(hidden: dict)`: Identifies the top 3 dominant dimensions for a startup based on its hidden template.
- `pick_linked_articles(hidden: dict, news: list[dict], rng: random.Random) -> list[str]`:
  - Finds news articles with $>0.55$ relevance matching the startup's dominant dimensions and polarity direction.
  - Links 3 to 5 articles per startup to serve as realistic supervisory anchors for training $W$.
- `main()`: Writes `data/startups.json` (identity only, no sensitivity profiles yet) and saves `data/startup_embeddings.npy`.

---

### 4.8 `scripts/discover_subclusters.py`

#### Purpose
Discovers unsupervised sub-clusters under each of the 11 dimensions using Agglomerative Clustering and extracts human-readable labels from centroid-adjacent article titles.

#### Functions
- `best_clustering(embeddings: np.ndarray, k_range: list[int], tolerance: float = 0.9)`:
  - Runs `AgglomerativeClustering(n_clusters=k, metric="cosine", linkage="average")` for each candidate $k$.
  - Evaluates cosine silhouette scores.
  - Selects the smallest $k$ whose silhouette score reaches $90\%$ of the maximum observed score.
- `label_cluster(articles: list[dict], embeddings: np.ndarray, member_idx: np.ndarray) -> str`:
  - Calculates the cluster centroid embedding.
  - Finds the 3 closest articles by cosine similarity.
  - Tokenizes titles, prunes stopwords and short tokens, and takes the top 2 most frequent title keywords as the cluster label.
- `discover_for_dimension(news, embeddings, score_field, dim)`:
  - Filters articles where `article[score_field][dim] > 0.30`.
  - Executes clustering and naming, returning the cluster count $k$, labels dictionary, and article assignment mapping.
- `main()`: Executes discovery across all 11 dimensions and writes `data/subclusters.json`.

---

### 4.9 `scripts/simulate_profit_history.py`

#### Purpose
Simulates 180 days of daily profit time-series for each startup, injecting delayed financial shocks whenever a relevant news article occurs.

#### Functions
- `polarity_sign(article: dict) -> float`: Helper returning $+1.0$ or $-1.0$.
- `simulate_one(hidden: dict, news: list[dict], rng: np.random.Generator) -> list[dict]`:
  - Generates linear baseline revenue: $\text{Base} \sim U(80k, 250k)$, daily drift $\sim U(-150, 400)$.
  - Injects Gaussian noise ($\sigma = 4\%$ of baseline).
  - Identifies news published on day $t_{\text{pub}}$. Injects shock into day $t_{\text{pub}} + \tau_{\text{shock}}$:
    $$\text{Shock} = \left( \sum_{d} \text{relevance}(a, d) \cdot \frac{\text{hidden\_weight}(d)}{100} \right) \cdot \text{polarity}(a) \cdot \text{ShockScale}$$
- `main()`: Generates time series for all 20 startups and writes `data/profit_history.json`.

---

### 4.10 `scripts/derive_sensitivity_profiles.py`

#### Purpose
Reconstructs each startup's sensitivity profile from its 180-day profit series via sub-cluster-level lagged Ridge Regression, validates recovery against hidden templates, and updates `data/startups.json`.

#### Functions
- `build_feature_columns(subclusters: dict) -> list[tuple]`:
  - Builds ordered feature columns for all (dimension, sub-cluster ID) pairs (~35–55 features).
- `build_daily_signal(news, subclusters, columns, n_days) -> np.ndarray`:
  - Constructs a $(180 \times M)$ daily event signal matrix where each cell represents the summed $\text{relevance} \times \text{polarity}$ of articles in that sub-cluster published on that day.
- `fit_lag_ridge(profit: np.ndarray, signal: np.ndarray, lag: int, alpha: float)`:
  - Regresses $\Delta \text{Profit}(t) = \text{Profit}(t) - \text{Profit}(t-1)$ against $\text{Signal}(t - \text{lag})$ with an unpenalized intercept $\beta_0$.
  - Uses $\lambda = 4.0$ (`PROFILE_REGRESSION_ALPHA`). Returns $R^2$ fit and regression coefficients.
- `roll_up_to_dimensions(coef: np.ndarray, columns: list[tuple]) -> np.ndarray`:
  - Sums sub-cluster coefficients into their parent dimension totals.
- `derive_profile(profit, signal, columns)`:
  - Iterates over candidate lags $[1, 3, 7, 14]$, selects $\tau^* = \arg\max R^2(\tau)$, rolls coefficients up, and rescales max magnitude to $100.0$.
- `main()`:
  - Recovers profiles for all 20 startups and writes them to `data/startups.json`.
  - Calculates correlation between recovered profiles and hidden ground truth, verifying lag recovery accuracy (typically achieving 20/20 lag matches and pooled correlation $\sim 0.90$).

---

### 4.11 `scripts/train_interaction_matrix.py`

#### Purpose
Trains the $384 \times 384$ bilinear interaction matrix $\mathbf{W}$ using Kernel Dual Ridge Regression on the recovered sensitivity profiles and linked news articles.

#### Functions
- `build_training_examples(startups, startup_embeddings, news_lookup, news_embeddings_by_id)`:
  - For each of the $20 \times 11 = 220$ (startup, dimension) pairs:
    - Constructs combined news vector $\mathbf{a}_{s, d} = \sum_{j \in \text{Linked}} \text{relevance}(j, d) \cdot \text{polarity}(j) \cdot \mathbf{x}_j$.
    - Sets startup CVP vector $\mathbf{z}_s$.
    - Sets target $y_{s, d} = \text{Profile}(s, d)$.
- `fit_interaction_matrix(combined_vecs, cvp_vecs, targets, alpha)`:
  - Computes Gram matrices: $\mathbf{K}_{\text{news}} = \mathbf{A} \mathbf{A}^\top$, $\mathbf{K}_{\text{cvp}} = \mathbf{Z} \mathbf{Z}^\top$.
  - Computes full dual kernel $\mathbf{K} = \mathbf{K}_{\text{news}} \odot \mathbf{K}_{\text{cvp}}$ (Hadamard product).
  - Solves $\boldsymbol{\alpha} = (\mathbf{K} + \alpha \mathbf{I})^{-1} \mathbf{y}$.
  - Reconstructs $\mathbf{W} = \sum_{j=1}^N \alpha_j (\mathbf{a}_j \mathbf{z}_j^\top)$.
- `main()`: Fits $\mathbf{W}$ with $\alpha = 0.2$, logs training MAE and correlation, and saves `data/interaction_matrix.npy`.

---

### 4.12 `scripts/validate_umbrella_case.py`

#### Purpose
End-to-end integration test of the clustering and regression pipeline using a synthetic umbrella-retailer CVP:
- Rain/monsoon sub-cluster must score **positive** ($> 0$).
- Drought/dry weather sub-cluster must score **negative** ($< 0$).
- Unrelated sub-cluster (deforestation / illegal logging) must score **near-zero** ($\le 10\%$ of max score).

#### Functions
- `matches_any(title: str, keywords: list[str]) -> bool`: Case-insensitive title keyword matcher.
- `find_cluster(clusters: list[dict], keywords: list[str])`: Locates sub-clusters by keyword matching across top member article titles.
- `main()`: Embeds umbrella CVP, executes `score_submission`, verifies all three conditions, and prints pass/fail diagnostics.

---

### 4.13 `app.py`

#### Purpose
Streamlit web interface featuring real-time CVP embedding, dual Plotly radar charts, and interactive sub-cluster drill-down explorers.

#### Functions & Components
- `@st.cache_resource` and `@st.cache_data`: Caches the transformer model, news data, interaction matrix, and sub-cluster JSON in memory for instant responses.
- `data_ready() -> bool`: Verifies required artifacts exist in `data/` before launching.
- `make_radar(dims, labels, values, near_zero, title) -> go.Figure`:
  - Constructs Plotly `Scatterpolar` radar charts.
  - Dynamically colors vertices: Green (`#2ca02c`) for positive/helping, Red (`#d62728`) for negative/hurting, Grey (`#9e9e9e`) for negligible.
  - Custom hover templates show exact signed sensitivity scores.
- `render_dimension_drilldown(breakdown, dims, labels, key_prefix)`:
  - Interactive radio selector for picking dimensions.
  - Visual horizontal contribution bars showing sub-cluster scores.
  - Expandable accordions displaying top driving articles, complete with dates, scopes, and individual contribution values.
- `st.text_area & st.button("Analyze")`: User input handling with persistent results stored in `st.session_state` to prevent state loss on UI interactions.

---

## 5. Data Pipeline Flow & Transformation Lifecycle

The end-to-end transformation of data from raw strings to final radar visual displays follows this exact sequence:

```
+---------------------------------------------------------------------------------------------------------+
| STEP 1: News Generation & Embedding                                                                     |
| Text templates + random context -> data/news.json (1000 articles)                                       |
| SentenceTransformer("all-MiniLM-L6-v2") -> data/news_embeddings.npy (1000 x 384, L2 normalized)         |
+---------------------------------------------------------------------------------------------------------+
                                                    │
                                                    ▼
+---------------------------------------------------------------------------------------------------------+
| STEP 2: Sub-Cluster Discovery & Label Extraction                                                        |
| For each dimension: filter articles with relevance > 0.3                                                |
| AgglomerativeClustering(cosine, average) with silhouette tolerance -> data/subclusters.json             |
| Extract top 2 frequent words from nearest 3 centroid titles -> "Tariffs Rattle", "Monsoon Sowing", etc.  |
+---------------------------------------------------------------------------------------------------------+
                                                    │
                                                    ▼
+---------------------------------------------------------------------------------------------------------+
| STEP 3: Profit Simulation & Sensitivity Profile Recovery                                                |
| Hidden templates inject delayed shocks -> data/profit_history.json (20 startups x 180 days)             |
| Sub-cluster lagged Ridge regression on delta profit -> data/startups.json (derived profiles)            |
+---------------------------------------------------------------------------------------------------------+
                                                    │
                                                    ▼
+---------------------------------------------------------------------------------------------------------+
| STEP 4: Interaction Matrix Training                                                                     |
| Combined news vectors (220 x 384) + CVP vectors (220 x 384) + derived targets                           |
| Kernel Dual Ridge Solve (K = K_news * K_cvp, alpha=0.2) -> data/interaction_matrix.npy (384 x 384)      |
+---------------------------------------------------------------------------------------------------------+
                                                    │
                                                    ▼
+---------------------------------------------------------------------------------------------------------+
| STEP 5: Online Inference (Streamlit app.py)                                                             |
| User enters CVP -> cvp_embedding (384-d)                                                                |
| compute_gates: G = News_embeddings @ (W @ cvp_embedding)                                                |
| Sub-cluster contributions: relevance * polarity * gate                                                  |
| Dimension roll-up -> Max-100 scaling -> Radar charts + Sub-cluster drill-down accordions                |
+---------------------------------------------------------------------------------------------------------+
```
