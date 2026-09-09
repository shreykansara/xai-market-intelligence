# Comprehensive Architecture & Methodological Improvement Guide
**AI-Based Explainable Market Intelligence System**

---

## 1. System Overview & Component Architecture

The **AI-Based Explainable Market Intelligence System** is an end-to-end platform designed to analyze business ideas, Customer Value Propositions (CVPs), historical revenue trends, and external macroeconomic news events (GDELT). It maps companies and news into an **11-Dimensional Strategic Vector Space** representing:
- **PESTLE Macro-Environment (6-D)**: Political, Economic, Social, Technological, Legal, Environmental.
- **Porter's 5 Forces Micro-Environment (5-D)**: Threat of New Entrants, Bargaining Power of Buyers, Bargaining Power of Suppliers, Threat of Substitutes, Competitive Rivalry.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                SYSTEM ARCHITECTURE MAP                                 │
└────────────────────────────────────────────────────────────────────────────────────────┘

 [ USER INTERFACE ]  ◄── HTTP/REST ──►  [ SERVER API (server.py) ]
  • Strategic Radar Canvas               • Route Handlers (/api/chat, /api/placements)
  • CVP vs Sales Input Modes             • Dynamic Data Filtering & Aggregation
  • Interactive News Timeline            • CORS & JSON Response Formatting
                                                        │
                                                        ▼
                                       [ CHATBOT ENGINE (chatbot_engine.py) ]
                                        • VectorPlacementEngine (11-D Mapping)
                                        • MarketKnowledgeBase (In-Memory Index)
                                        • Nearest-Neighbor Cosine Distance
                                        • Groq/Ollama LLM Provider
                                                        │
                                   ┌────────────────────┴────────────────────┐
                                   ▼                                         ▼
                   [ 500 BENCHMARK COMPANIES ]                     [ ENRICHED NEWS ENGINE ]
                    500_companies_analysis.json                     enrich_news.py
                    • Structured CVP Statements                     • Article Scraping
                    • 11-D Strategic Vectors                        • Semantic Concept Anchors
                    • 384-D CVP Text Vectors                        • GDELT Event Parsing
```

---

## 2. Codebase Detailed Breakdown

### A. Backend Server Layer: [`server.py`](file:///c:/Users/Shrey/Projects/AI-Based%20Explainable%20Market%20Intelligence/server.py)
Built using Python's native `http.server`, this module serves the REST API endpoints and static web assets:
- **`GET /api/companies`**: Serves the 500 benchmark company dataset along with sector breakdowns.
- **`POST /api/placements`**: Accepts user CVP statements or 11-D strategic inputs and returns nearest-neighbor company matches with visual coordinates.
- **`POST /api/chat`**: Handles conversational queries, performing hybrid RAG retrieval across benchmark companies and enriched GDELT news items before calling Groq/Ollama LLMs.
- **`GET /api/events`**: Serves filtered GDELT news events with location and 11-D strategic embeddings.

### B. Analytical Engine & Vector Index: [`chatbot_engine.py`](file:///c:/Users/Shrey/Projects/AI-Based%20Explainable%20Market%20Intelligence/chatbot_engine.py)
Contains the core analytical and vector comparison algorithms:
1. **`VectorPlacementEngine`**:
   - `compute_11d_vector(text)`: Maps arbitrary business descriptions or headlines onto the 11-dimensional strategic space ($[0.05 \dots 0.95]$) using **Semantic Concept Activation Anchors**.
   - `compute_384d_text_embedding(text)`: Computes a 384-dimensional text feature vector via word/n-gram hashing and L2 normalization.
   - `find_nearest_neighbors(...)`: Executes multi-vector similarity search against all 500 benchmark companies using a hybrid formula:
     $$\text{Combined Similarity} = 0.70 \cdot \text{Sim}_{11\text{D}} + 0.30 \cdot \text{Sim}_{384\text{D}}$$
2. **`MarketKnowledgeBase`**:
   - Loads [`500_companies_analysis.json`](file:///c:/Users/Shrey/Projects/AI-Based%20Explainable%20Market%20Intelligence/500_companies_analysis.json) and [`enriched_news_202608.csv`](file:///c:/Users/Shrey/Projects/AI-Based%20Explainable%20Market%20Intelligence/enriched_news_202608.csv) into memory for microsecond vector retrieval.
3. **`GroqOllamaProvider`**:
   - Provides unified access to external Groq API (`llama-3.3-70b-versatile`, `llama-3.1-8b-instant`) with automatic fallback to local Ollama models (`llama3.2`).

### C. Offline News Scraping & Enrichment: [`enrich_news.py`](file:///c:/Users/Shrey/Projects/AI-Based%20Explainable%20Market%20Intelligence/enrich_news.py)
- Processes raw GDELT news files (`gdelt_data/gdelt_202608.csv`).
- Scrapes full article content via `fetch_article_content()`.
- Calculates **Semantic Concept Activation** for PESTLE & Porter's Forces to assign non-noisy, discriminative 11-D scores.
- Implements **checkpointing and auto-resume**: inspects existing output CSV files on startup, skips completed rows, and saves batch progress every 10 items.

### D. Benchmark Dataset: [`500_companies_analysis.json`](file:///c:/Users/Shrey/Projects/AI-Based%20Explainable%20Market%20Intelligence/500_companies_analysis.json)
- Contains 500 pre-analyzed global companies spanning technology, healthcare, automotive, retail, and energy sectors.
- Each record holds structured CVP fields (`target_customer`, `statement_of_need`, `product_name`, `product_category`, `statement_of_key_benefit`), an 11-D strategic vector, and a 384-D text embedding vector.

---

## 3. Critical Analysis & Methodological Improvements

Below is an honest, deep-dive analysis of your current approaches across three core modules, along with state-of-the-art alternative methodologies tailored to your exact business goals.

---

### Module 1: Company CVP Similarity & Strategic Benchmark Matching

#### Current Approach
- Computes a single 384-D text embedding for the **entire concatenated CVP sentence** (*"For [Target] who [Need], the [Product] is a [Category] that [Benefit]"*) and calculates Cosine Similarity against the 500 benchmark company CVP embeddings.
- Combines $384\text{-D}$ text similarity ($30\%$) with $11\text{-D}$ strategic vector distance ($70\%$) to find nearest matches and project PESTLE/Porter scores.

#### Limitations of Current Approach
1. **Template Wording Dilution**: Boilerplate words (*"For"*, *"who"*, *"is a"*, *"that"*) dominate the single vector space, creating artificial baseline similarity across unrelated businesses.
2. **Confounding Problem Need with Solution Benefit**: A company solving the same *customer problem* using a different *technology stack* gets penalized because the product names and benefits differ in text space.

#### Proposed Superior Alternatives

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        PROPOSED MULTI-ASPECT ASPECT MATCHING                           │
└────────────────────────────────────────────────────────────────────────────────────────┘

  User CVP ──►  [ Need Sub-Vector ]    ──► Cosine Sim vs Benchmark Needs    ┐
           ──►  [ Benefit Sub-Vector ] ──► Cosine Sim vs Benchmark Benefits ├─► Weighted Sum
           ──►  [ Category Sub-Vector] ──► Cosine Sim vs Categories       ┘
```

1. **Multi-Aspect Weighted Sub-Embedding (Recommended & Immediate)**:
   - Divide the CVP into 3 distinct embedding vectors:
     - $\vec{v}_{\text{need}}$ (Customer Need)
     - $\vec{v}_{\text{benefit}}$ (Key Benefit)
     - $\vec{v}_{\text{category}}$ (Product Category)
   - Compute component-wise similarity:
     $$\text{CVP\_Sim} = 0.45 \cdot \cos(\vec{v}_{\text{need}}^{\text{user}}, \vec{v}_{\text{need}}^{\text{bench}}) + 0.35 \cdot \cos(\vec{v}_{\text{benefit}}^{\text{user}}, \vec{v}_{\text{benefit}}^{\text{bench}}) + 0.20 \cdot \cos(\vec{v}_{\text{category}}^{\text{user}}, \vec{v}_{\text{category}}^{\text{bench}})$$
   - **Why it's better**: Eliminates boilerplate noise, allows matching on *problem space* vs. *solution space*, and enables explainable UI breakdowns (*"88% Need Match, 45% Tech Match"*).

2. **Domain-Adapted Contrastive Fine-Tuned Embeddings (e.g., BGE-M3 / Instructor-Large)**:
   - Replace n-gram feature hashing with multi-task instruction embeddings (e.g. `BAAI/bge-m3` or `hkunlp/instructor-large`).
   - Prefix text with explicit domain instructions:
     - `Instruction: "Represent the business market demand problem for competitive retrieval:"`
   - **Why it's better**: Captures semantic intent rather than raw word overlaps.

3. **Hierarchical Taxonomy + Soft Max Margin Matching**:
   - First filter benchmark companies by a 2-level industry taxonomy graph (e.g. *SaaS -> Enterprise Cybersecurity*), then run fine-grained 11-D strategic vector distance inside the target cluster.
   - **Why it's better**: Prevents an AI cybersecurity startup from being matched to a physical security lock manufacturer simply because both use the word "security".

---

### Module 2: News Article Similarity & 11-D Strategic Space Placement

#### Current Approach
- Uses a single text embedding (`contextual_embedding`) per news article to determine article-to-article similarity.
- Assigns 11-D PESTLE/Porter strategic scores using Semantic Concept Activation Anchors and LLM contextual extraction.

#### Limitations of Current Approach
1. **Static vs. Temporal Topic Drift**: News similarity is purely static. A news item about "semiconductor tariffs" in 2024 is treated as identical in context to one in 2026, ignoring market evolution.
2. **Entity-Agnostic Clustering**: Standard text embeddings lump together articles mentioning the same country or industry, missing whether the event was a *positive subsidy* or a *negative restriction*.

#### Proposed Superior Alternatives

1. **Knowledge Graph Triplet Extraction (Subject - Predicate - Object)**:
   - Parse GDELT news events into structured semantic triplets:
     $$\langle \text{Actor1: US Trade Ministry}, \text{Action: Imposes 25\% Tariff}, \text{Actor2: Chip Manufacturers} \rangle$$
   - Vectorize the graph triplets using Graph Convolutional Networks (GCN) or TransE embeddings instead of raw text paragraphs.
   - **Why it's better**: Disambiguates causal direction (e.g. *who* is imposing the tariff on *whom*), resulting in far more precise 11-D strategic force assignment.

2. **Temporal-Decayed Dense Vector Clustering (BERTopic + HDBSCAN + Exponential Time Decay)**:
   - Group news articles into dynamic micro-clusters using **BERTopic** combined with **HDBSCAN**.
   - Apply a temporal decay kernel to news similarity:
     $$\text{Similarity}_{\text{temporal}}(A_1, A_2) = \cos(\vec{v}_{A1}, \vec{v}_{A2}) \cdot \exp\left(-\lambda \cdot |t_1 - t_2|\right)$$
   - **Why it's better**: Ensures that current market shocks carry higher relevance while keeping historical baseline context available.

---

### Module 3: Causal Sales Impact Attribution & News Subcluster Sentiment Correlation

#### Current Vision
- Cluster similar news into subclusters (e.g., a political subcluster).
- Check if $\ge 70\%$ of the news items in that subcluster coincide with a positive business sales change.
- If $\ge 70\%$, classify the subcluster as **"Pro-Business" / Positive Factor**; if $< 70\%$, treat it as non-correlated / neutral.

#### Critical Analysis of the Current 70% Threshold Vision
1. **Correlation $\neq$ Causation**: A simultaneous rise in sales during a news cluster may be driven by seasonal holiday demand or internal marketing campaigns rather than the external news event.
2. **Lagging Indicator Mismatch**: Revenue/sales numbers are **lagging indicators** (reported monthly or quarterly), whereas news events are **instantaneous leading indicators**. A news event in January might impact revenue in March.
3. **Information Loss from Hard Thresholding (70%)**: A 68% positive correlation is discarded as "0% relevant", while a 71% correlation is treated as 100% truth. Hard binary cutoffs mask subtle strategic trends.

#### Proposed Superior Alternatives (State-of-the-Art Causal Attribution)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        CAUSAL SALES ATTRIBUTION PIPELINE                               │
└────────────────────────────────────────────────────────────────────────────────────────┘

  [ Event Windows (t_0) ] ──► [ Synthetic Control Counterfactual ] ──► Causal Impact Δ
           │                                                                 │
           ▼                                                                 ▼
  [ Revenue Time Series ] ──► [ Bayesian Structural Time Series ]  ──► Probability Score
```

1. **Bayesian Structural Time Series (BSTS) & CausalImpact (Recommended)**:
   - Use Google's `CausalImpact` model framework (available in Python via `causalimpact` / `statsmodels`).
   - Predict what the company's sales **would have been** in the absence of the news cluster (the *counterfactual baseline* $\hat{y}_t$) using historical trend and control market data.
   - Calculate the true causal impact:
     $$\Delta y_t = y_t - \hat{y}_t$$
   - **Why it's better**: Proves whether the news event *actually caused* the revenue shift or if sales were already on an upward trend.

2. **Lead-Lag Cross-Correlation Windowing**:
   - Calculate the **Normalized Cross-Correlation Function (XCF)** between the news cluster sentiment intensity $S(t)$ and business revenue $R(t)$ across multiple time lags $\tau \in [-90 \text{ days}, +90 \text{ days}]$:
     $$r(\tau) = \frac{\sum (S(t) - \bar{S})(R(t+\tau) - \bar{R})}{\sigma_S \sigma_R}$$
   - **Why it's better**: Identifies the exact time delay (e.g., *"Political tariff news affects sales with a 45-day delay"*).

3. **Continuous Bayesian Factor Relevance Score (Replacing 70% Hard Cutoff)**:
   - Instead of a hard 70% binary check, output a continuous **Posterior Probability of Causal Association**:
     $$P(\text{Factor Relevant} \mid \Delta \text{Sales}, \text{Cluster Density}) = \frac{P(\Delta \text{Sales} \mid \text{Cluster}) \cdot P(\text{Cluster})}{P(\Delta \text{Sales})}$$
   - Display a confidence metric (e.g., *"84% Causal Confidence (High Positive Impact)"*) rather than a rigid Yes/No binary.

4. **Counterfactual LLM Causal Attribution with Event Shocks**:
   - Feed the event window sales delta + news cluster summaries into LLM with a structured causal prompt:
     - *"Given a +14% sales bump during [Date Range] and news events [X, Y, Z], evaluate whether external events vs internal seasonality drove the bump."*
   - Returns explainable strategic rationales directly to the user.

---

## 4. Summary Matrix of Recommended Upgrades

| Module | Current Approach | Proposed Best Alternative | Key Advantage |
| :--- | :--- | :--- | :--- |
| **CVP Matching** | Single full-sentence vector embedding | **Multi-Aspect Weighted Sub-Embeddings** (`Need`, `Benefit`, `Category`) | Removes boilerplate noise & matches exact customer problem space. |
| **News Embedding** | Static single text vector | **GDELT Knowledge Graph Triplet Embeddings** + BERTopic | Distinguishes causal action direction & entity relationships. |
| **Sales Impact** | Hard 70% subcluster correlation check | **Bayesian Structural Time Series (`CausalImpact`)** + Lead-Lag Lags | Proves true causality vs seasonality & identifies exact time delays. |

---

> [!NOTE]
> All backend files ([`chatbot_engine.py`](file:///c:/Users/Shrey/Projects/AI-Based%20Explainable%20Market%20Intelligence/chatbot_engine.py), [`enrich_news.py`](file:///c:/Users/Shrey/Projects/AI-Based%20Explainable%20Market%20Intelligence/enrich_news.py), [`server.py`](file:///c:/Users/Shrey/Projects/AI-Based%20Explainable%20Market%20Intelligence/server.py)) and datasets ([`500_companies_analysis.json`](file:///c:/Users/Shrey/Projects/AI-Based%20Explainable%20Market%20Intelligence/500_companies_analysis.json)) can be incrementally updated to incorporate these multi-aspect and causal impact models.
