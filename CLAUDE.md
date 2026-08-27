# AI-Based Explainable Market Intelligence

## Problem
Founders and investors rely on manual market scanning to understand how
real-world events affect a business, with no systematic or traceable way
to connect a specific happening to a specific company's outcome. Early-
stage startups make this worse — no sales history of their own to learn
from.

## Use cases
1. **Startup founders** — identify which factors affect their product, to
   shape branding and go-to-market strategy.
2. **Investors** — gauge how risky a given market/category is before
   deciding whether to invest.

## Architecture — two subsystems

### 1. Offline training pipeline (`scripts/`)
Builds everything the online system depends on, from fabricated data —
no manual ground-truth labeling anywhere except the original seed
generation itself.
- `generate_news.py` — 1,000 fabricated articles, each with soft
  multi-dimensional PESTLE (6) and Porter's (5) relevance vectors,
  polarity, geographic scope, embedded with all-MiniLM-L6-v2.
- `generate_startups.py` — 50 fabricated LPU-incubated startups (grew
  from 20 across 10 new domain archetypes — see "Known gaps" below),
  each with a CVP, embedded, linked to 3-5 relevant seed articles.
- `hidden_ground_truth.py` — hidden per-startup sensitivity templates
  used only to generate realistic profit shocks — not exposed to the
  learning pipeline, so recovery can be validated against them. Each
  hand-authored domain-consistent base template also gets a fixed-seed
  independent Gaussian perturbation (std=25) per dimension, representing
  realistic idiosyncratic per-startup variation on top of the shared
  domain archetype — see "Known gaps" below for why.
- `discover_subclusters.py` — unsupervised agglomerative clustering
  (cosine distance, average linkage, silhouette-tuned k) within each of
  the 11 dimensions, producing human-readable sub-cluster labels from
  centroid-nearest article keywords. Two levels: dimension -> sub-cluster.
- `simulate_profit_history.py` — 180-day fabricated profit series per
  startup, with shocks injected at a lag (1/3/7/14 days) tied to the
  hidden template.
- `derive_sensitivity_profiles.py` — per-startup lagged ridge regression
  recovering each startup's real sensitivity profile from its profit
  history and the news timeline (not hand-authored). Validated against
  the hidden template.
- `train_interaction_matrix.py` — fits the shared bilinear interaction
  matrix W (384x384) via kernel dual ridge regression (needed because
  147,456 parameters from 550 training instances is ill-conditioned in
  the primal space). `gate(news, cvp) = news_embedding^T W (cvp_embedding
  - cvp_mean)`. CVP embeddings are mean-centered before fitting and at
  inference (the mean is persisted to `data/cvp_mean.npy`) — see "Known
  gaps" below for the diagnosed reason this centering step exists.

### 2. Online system
- **`server.py`** — FastAPI backend. `/api/analyze` takes a CVP, embeds
  it, computes gates against news via W, combines with each article's
  relevance/polarity, rolls sub-cluster scores up to the two radar
  charts (PESTLE hexagon, Porter's pentagon), serves `web/index.html`.
- **`ingestion_service.py`** — standalone FastAPI microservice, own port
  (8502), runs the real-news pipeline on startup and every 30 minutes:
  fetch -> fact decomposition -> dedup -> seed transfer (relevance,
  then polarity/scope) -> relevance gate -> atomic write. Relevance has
  to be inferred from the seed corpus before it can be gated on — the
  gate reads a value seed transfer just produced, so seed transfer runs
  first; verified against the actual code (`ingestion.py`), not just
  asserted here. Exposes `GET /health`.
- **Real news sources**: Google News RSS, GDELT DOC 2.0 (classic, free,
  no key — not "GDELT Cloud", which is a separate paid product), BBC
  World RSS, Al Jazeera RSS. Reuters is not used (public RSS discontinued
  2020, now paid-only).
- **Fact decomposition** (`fact_extraction.py`) — local Ollama
  (`llama3.2:3b`) splits articles into distinct, independently-scorable,
  neutrally-reworded atomic facts (e.g. a tax bill's bracket increase and
  bracket decrease become two facts with opposing polarity, not one
  blended record). Falls back to treating the whole text as one fact if
  Ollama is unavailable.
- **No manual labeling of real data, anywhere** (`seed_inference.py`) —
  relevance and polarity inferred via similarity-weighted k-NN (k=10)
  against the seed corpus; geographic scope inferred via per-class-
  best-match (each of the 7 scope classes' single closest seed match
  wins) specifically to prevent majority classes (India, Punjab) from
  winning on population size alone.
- **Relevance gate** — real facts scoring below the 5th percentile of
  the seed corpus's own max-relevance distribution (~0.58) are excluded
  before scope classification, logged to `ingestion_excluded.jsonl`, not
  silently dropped. This is what filters out off-topic noise (sports,
  crime stories) that has no PESTLE/Porter's relevance at all.
- **Dedup** — cosine similarity >= 0.92 within a 48h window collapses
  re-reported stories into one record with an incremented mention_count.

## UI
Two-state single page (`web/index.html`), sharp corners throughout (0px
radius, no exceptions), near-black graphite background, deep indigo-
violet brand accent used sparingly (CTA + chart fill only), green/red
direction encoding, Space Grotesk + IBM Plex Mono. State 1: CVP input.
State 2: side-by-side PESTLE hexagon / Porter's pentagon radar charts
(Plotly), with per-dimension drill-down accordions into sub-clusters and
their contributing articles, each row badged "LIVE" when it's a real
ingested fact rather than a fabricated seed article. The original
Streamlit version (`app.py`) was fully replaced by this page and no
longer exists in the repo.

## Known gaps / in progress
- **Real ingested facts are now merged into the live scoring path**
  (`src/marketintel/live_facts.py`, wired into `server.py`). Each real
  fact is assigned to its nearest existing sub-cluster by centroid
  cosine similarity (never re-running discovery), weighted EQUALLY to
  seed articles in the gate/contribution formula (reasoning documented
  in `live_facts.py` - W was trained on the seed corpus alone, so a real
  fact's gate score is only as trustworthy as the seed corpus's ability
  to generalize to it; there's no evidence yet that real facts need
  down- or recency-weighting on top of that). Fabricated corpus + `W` +
  sub-clusters are cached per-process; real facts are reloaded fresh on
  every request since `ingestion_service.py` keeps appending to them
  independently. Surfaced in the drill-down with a "LIVE" badge. At
  current volume (single digits to low hundreds of real facts vs. 1000
  fabricated), a real fact's contribution is correctly computed and
  ranked but usually doesn't crack a cluster's top-5 display cutoff —
  confirmed by checking full (unturncated) cluster rankings directly,
  not a bug, just a reflection of how little real data exists so far.
- Relevance-gate-vs-seed-transfer ordering verified correct in the
  actual code (`ingestion.py`): relevance is inferred via seed transfer,
  THEN gated on. The pipeline description above used to list these in
  the reverse order — that was a doc bug, now fixed; the code was never
  wrong.
- Scope-fix validation (`scripts/validate_scope_fix.py`) now hard-
  asserts against the exact two original failure headlines (constructed
  inline, not searched for in whatever's currently stored). The NFL
  story is asserted excluded; the Nigerian kidnapping story is asserted
  NOT excluded (it has genuine, if narrow, "technological" relevance at
  0.80 — asserting it should be excluded would just be factually wrong).
  Its scope still comes back "India", which remains a known, undecided
  limitation, not something the relevance gate was ever meant to fix.
- **Startup CVP text carries explicit LPU framing** (all 50 read
  "incubated at LPU" / "founded by LPU alumni" / equivalent). `W` has
  since been retrained multiple times on this text (see below), so this
  is no longer a stale-artifact concern.
- **Fixed: different CVPs were producing near-identical output
  patterns.** Root-caused through several rounds, each verified against
  the actual numbers rather than assumed fixed:
  1. `W`'s effective rank was only ~5/384 even with well-separated raw
     CVP embeddings, ruling out the embedding pipeline as the cause.
  2. Growing from 20 to 50 startups (10 new domain archetypes) raised
     `W`'s effective rank only marginally (~5 -> ~6) and barely moved
     real-CVP-to-real-CVP output similarity (still 0.97-0.99).
  3. The deeper cause: the hidden ground-truth *target* profiles
     themselves had effective rank only ~3.4-4.3 out of 11 dimensions —
     hand-authoring templates "domain-consistent by design" meant every
     startup in a domain got essentially the same archetypal shape, just
     rescaled. Fixed by adding fixed-seed independent Gaussian noise
     (std=25/dim) to each hidden template (see `hidden_ground_truth.py`),
     raising target effective rank to ~8.6 and `W`'s to ~10.2 — a real
     improvement, but real-CVP output similarity *still* didn't drop
     meaningfully (0.90-0.99), proving the bottleneck was elsewhere too.
  4. The actual remaining cause: `W`'s dominant singular direction (24%
     of its energy) was ~88% cosine-aligned with the *mean* of all
     training CVP embeddings — the "generic business pitch text"
     component every CVP shares regardless of domain. In a system this
     underdetermined (147,456 parameters, 550 examples), ridge
     regression's minimum-norm solution spent a large share of `W`
     modeling that shared, uninformative axis. **Fix**: mean-center CVP
     embeddings before fitting and at every inference call (persisted to
     `data/cvp_mean.npy`, wired through `analysis.compute_gates` /
     `score_submission`). Verified on a 5-CVP discrimination test
     (disaster sensors / fintech loans / skincare D2C / legal SaaS /
     gibberish): real-business-to-real-business output cosine similarity
     dropped from a collapsed 0.90-0.99 to a properly varied -0.31 to
     0.68, at a training-fit MAE cost of only 27.9 -> 29.1 (target
     std ~50.7). This is the actual success criterion — genuinely
     different businesses now produce genuinely different profiles.
  5. **New, narrower regression surfaced by this work**:
     `scripts/validate_umbrella_case.py`'s deforestation-near-zero check
     now fails narrowly (score -48.3 vs. a ±32.0 threshold — about 50%
     over). Verified this is NOT caused by the centering fix or the
     noise-perturbation step — it reproduces identically with both
     disabled, so it predates this session's changes (most likely
     introduced by the earlier 20->50 startup expansion, not otherwise
     diagnosed). The rain-positive and drought-negative checks still pass
     cleanly. Not yet fixed — flagged here rather than silently left
     failing.
- Ollama + llama3.2:3b are now installed and confirmed working end to
  end (`scripts/validate_fact_decomposition.py` produced 4 real facts
  with correctly opposing polarity from a live model, not the fallback).
  This environment is CPU-only, though: a cold inference call took ~80s
  (~32s just loading weights), which is why `OLLAMA_TIMEOUT_SECONDS` is
  120, not the original 30 - that had been causing spurious single-fact
  fallbacks even with Ollama installed and reachable.
- BBC World RSS, Al Jazeera RSS, and Google News RSS all confirmed
  reachable. GDELT DOC 2.0's free endpoint is genuinely intermittent
  from this environment - confirmed working (250 articles fetched) in
  earlier runs this session, connection-timed-out on a later check. It's
  already handled gracefully (logged and skipped for that run, doesn't
  abort the other sources) - this is a real characteristic of the free
  tier, not a bug to fix.
- No paid API keys or paid dependencies anywhere in the stack (checked;
  every dependency in `pyproject.toml` is free/open-source, and every
  "API" reference in the code is to Ollama, GDELT's free tier, or RSS).

## Explored but not yet built
- **Hypothetical-category impact scoring** — construct a representative
  embedding for a hypothetical event category (e.g. "political event
  favoring domestic manufacturing") and run it through the existing
  gate/contribution mechanism against the 50 fabricated startups, to see
  who benefits/suffers. Cheap to build — reuses the existing pipeline
  entirely, no new architecture needed.
- **Storyline / event-chain escalation modeling** — linking atomic facts
  into ongoing storylines over time (e.g. leak -> distress -> protest ->
  resignation) and predicting the next stage in a known escalation
  script. Genuinely new capability (event-linking/clustering-over-time
  layer), not an extension of existing code. Scoped to calendar-anchored
  "scheduled" events first if pursued — "shock" events (coups, scandals)
  are closer to irreducible uncertainty and a much harder bet. Not
  started.

## Open technical decisions
- ~~How real facts should be weighted against fabricated seed data~~ —
  decided: equal weighting (see `live_facts.py` for the reasoning).
  Revisit once real fact volume is large enough to check empirically
  whether they need down-weighting.
- Whether/when to move real-fact storage to a vector database (still
  flat files; fine at current volume).
- Whether the 5th-percentile relevance threshold needs retuning based on
  what fraction of real ingested articles it's excluding in practice.
- Real facts' scope classification is still unreliable (see the real
  news ingestion section above) - no decided fix yet beyond the
  already-shipped relevance-gate + per-class-best-match improvements.
- ~~Different CVPs producing near-identical output patterns~~ — fixed
  via CVP mean-centering (see "Known gaps" above). Discrimination is now
  properly varied (-0.31 to 0.68 cosine similarity across 5 genuinely
  different real-business CVPs, down from a collapsed 0.90-0.99).
- The umbrella-case deforestation-near-zero regression (see "Known
  gaps" above) is unresolved — needs its own investigation into the
  sub-cluster/regression pipeline, separate from the CVP-discrimination
  work above.