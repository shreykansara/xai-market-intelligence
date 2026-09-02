# Explainable Market Intelligence

Founders and investors currently rely on manual market scanning to understand
how real-world events affect a business, with no systematic or traceable way
to connect a specific happening to a specific company's outcome. Early-stage
startups make this worse — they have no sales history of their own to learn
from.

This is a working prototype: paste a business CVP / description and get back
two radar charts — a **hexagon for PESTLE** and a **pentagon for Porter's Five
Forces** — showing how sensitive the business is on each dimension, with a
drill-down into the specific sub-topics and fabricated news events behind
each score.

## How it works

1. **Fabricated news dataset** (`data/news.json`) — 1000 fabricated articles
   from the last 6 months, spread across LPU, Phagwara, Jalandhar,
   Kapurthala, Punjab, India, and World scopes. Each article has independent
   0-1 soft scores for all 6 PESTLE dimensions and all 5 Porter's forces
   (an article can score high on more than one at once), plus a polarity
   (positive/negative). Article text is embedded with the local
   `all-MiniLM-L6-v2` model via `fastembed` (ONNX Runtime, not PyTorch - see
   "Hosting requirements" below for why).
2. **Fabricated startup dataset** (`data/startups.json`) — 50 LPU-based
   startups (grew from an original 20 — see "Current scope" below) spanning
   fintech, edtech, agritech, D2C hardware, SaaS, healthtech, cleantech,
   logistics, proptech, foodtech, EV/mobility, cybersecurity, HRtech,
   insurtech, B2B marketplaces, and gaming/media. Each has a CVP and 3-5
   linked news article IDs. Their PESTLE/Porter's sensitivity profile is
   *not* hand-authored — it's recovered from a fabricated profit history
   (below), and that recovered profile is what supervises the interaction
   matrix. CVPs are embedded with the same model.
3. **Sub-clusters under each dimension** (`data/subclusters.json`) — a second,
   unsupervised hierarchy level under each of the 11 PESTLE/Porter's
   dimensions. `scripts/discover_subclusters.py` takes every article above a
   relevance threshold (0.3) for a dimension and agglomeratively clusters
   their embeddings into a handful of sub-clusters (cosine distance, cluster
   count picked per dimension by silhouette score — using the smallest count
   that gets within 90% of the best score in range, not a raw argmax, since
   argmax on this kind of short-text embedding is biased toward always
   picking the largest count offered). Each cluster gets a short label
   afterward, derived from the titles nearest its centroid, purely for
   display — the clustering itself never sees hand-authored labels. An
   article can land in a different sub-cluster under each dimension it's
   relevant to. Two levels deep only for now (see "Current scope" below).
4. **Fabricated profit history → derived sensitivity profile** — each
   startup also gets a hidden PESTLE/Porter's sensitivity template and a
   hidden shock lag (`scripts/hidden_ground_truth.py`), domain-consistent
   by design (e.g. an import-dependent hardware startup gets high hidden
   political/economic sensitivity), plus a fixed-seed independent Gaussian
   perturbation (std=25/dimension) on top of that domain base representing
   realistic idiosyncratic per-startup variation (added after diagnosing
   that hand-authored "domain-consistent" templates alone had an effective
   rank of only ~4/11 — every startup in a domain got essentially the same
   archetypal shape, just rescaled, which capped how much any downstream
   model could ever discriminate between businesses — see "Current scope"
   below). None of this is **ever exposed to the learning pipeline** —
   only used to fabricate a daily profit/revenue series
   (`data/profit_history.json`, 180 days: baseline trend + noise + shocks
   injected some days later whenever a relevant, hidden-sensitive news
   article runs). `scripts/derive_sensitivity_profiles.py` then recovers
   each startup's sensitivity profile purely from that profit series, at
   *sub-cluster* granularity (~35-55 features rather than 11): for a
   handful of candidate lag windows (1/3/7/14 days) it ridge-regresses
   daily profit changes against the preceding day's per-sub-cluster
   relevance (weighted by polarity) - ridge, not plain least squares,
   since ~180 daily observations can't support that many features
   unregularized - keeps the lag with the best fit (highest R²), and sums
   each lag's sub-cluster coefficients back up to their parent dimension
   (11 values, rescaled so the largest magnitude hits 100) as the derived
   profile. It then validates the recovery by correlating each derived
   profile against its hidden template — a sanity check on the recovery
   pipeline itself, printed before training ever touches the shared
   matrix. In practice this recovers the true shock lag for all 50
   startups and correlates at ~0.85-0.88 with the hidden templates even at
   sub-cluster granularity.
5. **Interaction matrix** (`data/interaction_matrix.npy`) — a single shared
   (384x384) matrix `W`, fit once in batch. For a (news, CVP) pair,
   `gate = news_embedding · W · (cvp_embedding - cvp_mean)` is one scalar
   capturing how strongly that business reacts to that news in general —
   direction and magnitude — independent of which dimension is involved.
   `cvp_mean` (`data/cvp_mean.npy`) is the mean of all training CVP
   embeddings, subtracted before every fit and every inference-time query —
   see "Current scope" below for why this centering step exists; it's load-
   bearing, not cosmetic. `W` is fit by ridge regression against the 50
   startups' *derived* sensitivity vectors (50 startups × 11 dimensions =
   550 training examples), solved in the ridge *dual* via the kernel trick,
   since the 384×384 = ~147k parameters vastly outnumber the 550 examples.
   The regularization strength was chosen by leave-one-startup-out
   cross-validation, not by in-sample fit (in-sample error only keeps
   falling as regularization drops toward zero in a system this
   underdetermined, which would just pick a `W` that memorizes the
   startups).
6. **Analysis** — for a submitted CVP, every fabricated seed article *and*
   every currently-stored real fact gets a `gate` from `W` (`src/marketintel
   /live_facts.py` folds the two corpora together before scoring - see
   below). Within each dimension, `gate` combines with an item's own
   relevance and polarity to give its signed contribution to whichever
   sub-cluster it belongs to; summing a dimension's sub-cluster totals gives
   that dimension's raw score. Each chart's 6 or 5 raw scores are then
   independently rescaled so the largest magnitude hits 100, sign preserved.
   (`analysis.py` also flags dimensions whose raw magnitude is under 10% of
   the submission's strongest as negligible; the current frontend's
   two-color helping/hurting design doesn't surface that flag, but a
   near-zero dimension still reads as such by its small radius/small score.)
7. **Output** — two Plotly radar charts (cobalt fill, green/red vertices for
   direction, themed to match the page's current light/dark mode) side by
   side, with the news breakdown underneath: one section
   per dimension (ranked by |score|, click to expand), sub-grouped by
   sub-cluster, down to the specific bordered rows driving each score -
   real ingested facts marked with a small "LIVE" badge, distinct from
   fabricated seed articles - so every number stays traceable back to a
   real, inspectable article, at both the dimension and the sub-topic
   level.

8. **Merging real facts into the live score** (`src/marketintel/
   live_facts.py`) — real facts were never part of the original sub-cluster
   discovery (that ran once, offline, against the fabricated corpus only;
   facts arrive continuously afterward), so each is assigned to its nearest
   EXISTING sub-cluster by cosine similarity to that sub-cluster's centroid
   (computed once from the fabricated corpus + its discovery output, cached
   for the process's lifetime) - not by re-running discovery. Real facts are
   then folded into the same `news` list and embedding matrix the fabricated
   corpus uses, so `analysis.py`'s gate/contribution math needs zero
   changes: real facts already have the same `pestle_scores`/
   `porters_scores`/`polarity`/`scope` shape as fabricated articles. **They
   count EQUALLY** to fabricated seed articles in the score - not down-
   weighted, not recency-weighted. Reasoning: `W` was trained purely on the
   fabricated corpus, so a real fact's gate score is already only as
   trustworthy as the seed corpus's ability to generalize to it; down-
   weighting on top of that would be an extra, unjustified parameter with
   no evidence behind it (recency-weighting was considered too, and
   rejected for the same reason - there's no observed real outcome yet to
   calibrate a decay constant against). Revisit once real fact volume is
   large enough to check empirically whether down-weighting is actually
   warranted. Real facts are re-loaded fresh on every `/api/analyze`
   request (not cached), since `ingestion_service.py` keeps appending to
   them independently of the analysis server's process. At current volume
   (tens to low hundreds of real facts vs. 1000 fabricated), a real fact's
   contribution is correctly computed and ranked within its cluster, but
   usually doesn't crack the UI's top-5-per-cluster display cutoff -
   confirmed by inspecting full, untruncated cluster rankings directly
   (real facts landing at position ~45 of ~47 by contribution magnitude,
   exactly where their weaker - not absent - signal should place them) -
   not a display bug, just how little real data exists relative to the
   fabricated corpus so far.

9. **Real news ingestion** (`src/marketintel/ingestion.py`, run by either
   `ingestion_service.py` or `scripts/ingest_news.py` - see "Real news
   ingestion" below) — a separate, parallel dataset from the fabricated one
   above, now merged into scoring per item 8. Pulls world-level headlines
   from four free, no-key sources: BBC World and Al Jazeera's own
   RSS feeds, Google News RSS (queried by topic - `WORLD` - not scoped to
   any one outlet), and the GDELT DOC 2.0 API via the open-source
   `gdeltdoc` package (*not* GDELT Cloud, a separate paid product). Reuters
   isn't used: its public RSS was discontinued in 2020 and programmatic
   access now requires a paid license. GDELT's free endpoint is
   rate-limited and occasionally times out; a failed source is logged and
   skipped for that run rather than aborting the others.

   **The unit of analysis is the fact, not the article.** Each fetched
   article is decomposed into one or more atomic, independently-scorable
   facts (`src/marketintel/fact_extraction.py`) using a free local model via
   Ollama, not a paid API - a tax-policy piece with a bracket increase and a
   separate bracket decrease becomes two fact records with their own
   (likely opposing) polarity, not one blended one. Extraction also
   neutralizes each claim's wording (numbers, thresholds, and named parties
   preserved; loaded framing stripped). Dedup, embedding, the relevance
   gate, and scope classification all now run on facts - the mechanisms
   are unchanged, only the unit they're applied to moved from article to
   fact. The article itself becomes a provenance container only
   (`data/real_articles.json`: headline, source, link, which fact ids came
   out of it) - not scored or embedded itself. If Ollama isn't running or
   the configured model isn't pulled, extraction falls back to treating the
   whole article as a single unmodified fact rather than failing the run -
   see "Real news ingestion" below for how to spin Ollama up. Facts and
   their embeddings live in `data/real_facts.json` /
   `real_fact_embeddings.npy`; only title, publish timestamp, link, and the
   extracted/inferred tags are ever stored - no raw article body text, and
   no vector database.

   **Confirmed working live, and confirmed capable of hallucinating.**
   With Ollama + `llama3.2:3b` actually running, a real headline - "Two
   dead and 10 hurt after car rams into crowd in northern France" -
   correctly split into three separate facts ("Two people died", "10
   people were hurt", "A car rammed into a crowd"), each independently
   scorable, which is exactly the capability this step was built for. But
   a spot-check of the same live run also caught a genuine hallucination:
   given only the headline "Putin Moves to Escalate War in Ukraine as
   Talks at Dead End", extraction produced a fact reading "Ukraine's
   president Volodymyr Zelenskyy has stated that the situation in the
   country is at a stalemate" - a specific named attribution the headline
   never made. This is a real risk with a small model working from a bare
   headline (no article body, so no surrounding context to ground it) and
   is exactly why CLAUDE.md calls for spot-checking extracted facts against
   their source before trusting this at scale
   (`scripts/validate_fact_decomposition.py` prints the most recent
   real facts next to their source headline for this) - it's not
   hypothetical, it already happened on the very first live run.

   **Labeling is one mechanism for all three fields** (`src/marketintel/
   seed_inference.py`): relevance, polarity, *and* geographic scope are all
   inferred by the same similarity-weighted vote among a fact's 10 nearest
   neighbors. There's no per-source scope tagging and no trained polarity
   classifier; every field is read off the same nearest-neighbor lookup.
   **The reference pool itself has since migrated from the fabricated seed
   corpus onto the accumulated real-fact corpus, per PESTLE/Porter's
   dimension and per scope class** (`src/marketintel/real_data_inference.py`)
   - new real facts are now scored primarily against OLDER real facts,
   self-referentially, once a direct coverage check confirms there's enough
   real data (of both polarities) to trust for that specific dimension;
   thin dimensions keep falling back to the fabricated corpus rather than
   cutting over silently. See "Migrated seed-based inference..." in
   `CLAUDE.md`'s "Known gaps" for the exact coverage numbers, which
   dimensions still fall back, and why - this only affects live ingestion,
   not any batch pipeline, which looked up the fabricated corpus
   unchanged. Dedup (cosine similarity ≥0.92 against the last
   48 hours of stored facts) runs at this same fact granularity: the same
   fact reported by multiple outlets collapses into one record with a
   shared `mention_count`, verified in practice by cross-source stories
   landing in one record. A sample of each run's newly stored facts (with
   their source headline alongside, for spot-checking) is printed and
   appended to `data/ingestion_samples.jsonl`.

   **Scope inference was visibly the weak link, and got a two-part fix.**
   On an early live run, real headlines came back distributed India=47,
   World=36, Punjab=25, Jalandhar=7, Phagwara=5, Kapurthala=2, LPU=1 -
   including hyper-local tags landing on headlines like an NFL
   brain-injury study or a Nigerian kidnapping manhunt, neither of which
   has anything to do with Punjab or India. **Why it happened:** scope
   used the same pooled top-k plurality vote as polarity - sum up how
   much of a headline's k nearest seed neighbors belong to each scope
   class, take the class with the most weight. The fabricated seed
   corpus's own scope distribution is skewed toward India/Punjab (see
   `SCOPE_WEIGHTS`: India=300, Punjab=150, vs. LPU=50), and most
   real-world wire headlines don't closely resemble *any* of its
   hyper-local articles - so a weak, ambiguous match just drifted toward
   whichever class had the most seed articles nearby, regardless of
   whether any of them were a good match. There was also no reject
   option: every headline got a scope no matter how irrelevant it was.

   **The fix has two parts** (`src/marketintel/seed_inference.py`):
   1. *A relevance gate, before scope classification.* An incoming
      article's max relevance across all 11 dimensions must clear the
      5th percentile of the fabricated seed corpus's own max-relevance
      distribution or it's excluded entirely - no scope assigned, not
      used downstream - and logged to `data/ingestion_excluded.jsonl`
      (headline, timestamp, max relevance) rather than silently dropped.
   2. *Per-class-best-match instead of pooled voting*, for articles that
      pass the gate. For each of the 7 scope classes, find that class's
      single closest seed article; assign whichever class's best match
      has the highest similarity overall. A class can no longer win by
      having many so-so neighbors nearby - only its single strongest
      example competes, which is what actually removes the
      population-size bias.

   **Validated against the exact batch that surfaced the bug**
   (`scripts/validate_scope_fix.py`, re-run on the stored pre-fix
   embeddings - no re-fetching): the NFL story (max relevance 0.33,
   below the 0.58 threshold) is now correctly excluded. Re-scoring the
   63 articles that still pass the gate (down from 123) shows real
   rebalancing away from the majority classes - Punjab 25→8, Phagwara
   5→0, Jalandhar 7→4 - while India (47→25) remains the largest single
   class. That's not a bug in the fix: even a single-best-match rule is
   not fully population-invariant, since a class with more seed articles
   has more chances to contain *one* that happens to match well, just a
   much weaker effect than pooled voting's linear compounding. The
   Nigerian kidnapping story is a concrete example of the fix's limit,
   not its failure: its max relevance (0.80, comfortably legal/
   technological) means it correctly is *not* excluded, but its scope
   stayed "India" before and after, because the seed corpus doesn't
   carry a strong enough geography-specific signal for generic
   crime/legal content to separate it from India-scoped seed articles on
   that dimension. Relevance and polarity continue to read as
   qualitatively sound; scope is meaningfully better but still not
   reliable, and should stay flagged until a real location signal (e.g.
   NER-based content extraction, explicitly out of scope for this phase
   per CLAUDE.md) replaces nearest-neighbor lookup entirely.

**Validation test case** (`scripts/validate_umbrella_case.py`) — runs a
fabricated umbrella-retailer CVP through the full pipeline and checks that,
within "Environmental," a rain/monsoon sub-cluster scores positively, a
drought/dry-weather sub-cluster scores negatively, and an unrelated
sub-cluster (deforestation/illegal logging) scores close to zero relative to
the others. This is a sanity check on the clustering + regression pipeline as
a whole - getting rain and drought articles to land in *different*
sub-clusters in the first place turned out to be the hard part (short,
templated weather sentences embed very close together regardless of
polarity), which is why a couple of the news templates are phrased the way
they are and why cluster-count selection isn't a plain argmax.

## Project structure

```
server.py                          FastAPI backend for the analysis app - adapts the existing
                                    analysis pipeline to HTTP/JSON (POST /api/analyze) and serves
                                    web/. Runs on its own port (8000), independent of the
                                    ingestion microservice below.
ingestion_service.py               Standalone ingestion microservice - self-schedules the shared
                                    ingestion pipeline (runs on startup, then every 30 min) and
                                    exposes GET /health. Its own port (8502); no ingestion logic
                                    lives here, only scheduling + status (see below).
web/
  index.html                       The whole frontend: three-page flow (landing / upload / analysis)
                                    as one file with JS-toggled states, inline CSS + JS,
                                    Plotly.js-driven radar charts
  vendor/plotly.min.js             Vendored Plotly.js (copied from the plotly Python package's
                                    bundled asset) - no CDN dependency
src/marketintel/
  config.py                        Dimension names, scopes, file paths, constants
  embeddings.py                    fastembed (ONNX Runtime) wrapper - see "Hosting requirements"
  data_loader.py                   Loads generated news/startup/subcluster/real-fact data + W
  analysis.py                      Gate/sub-cluster contribution scoring + roll-up + drill-down data
  seed_inference.py                Relevance/polarity via pooled k-NN vote, a relevance-gate
                                    threshold, and scope via per-class-best-match - all looked
                                    up against the fabricated seed corpus, for real facts
  fact_extraction.py               Decomposes one article into one or more neutral, atomic facts
                                    via a local Ollama model, with a single-fact fallback if
                                    Ollama isn't reachable
  ingestion.py                     The real ingestion pipeline itself (fetch, decompose into
                                    facts, dedup, embed, gate, scope) - the ONE implementation,
                                    imported by both scripts/ingest_news.py and ingestion_service.py
  atomic_io.py                     Temp-file-then-rename writers for real_articles.json /
                                    real_facts.json / real_fact_embeddings.npy /
                                    ingestion_state.json, so a concurrent reader never sees a
                                    half-written file
  comparative_matching.py          Finds the nearest earlier fact about the same subject to
                                    compute a direction for a bare state-value fact
  grounding.py                     Pre-filter (non-content titles) + post-decomposition
                                    grounding check (rejects facts with fabricated numbers)
  real_data_inference.py           Coverage-gated policy layer deciding, per PESTLE/Porter's
                                    dimension and per scope class, whether live ingestion's
                                    k-NN lookup draws from real or fabricated data
  sensitivity_regression.py        Source-agnostic lagged-ridge-regression core (extracted
                                    from derive_sensitivity_profiles.py) - shared by the
                                    fabricated offline pipeline and the sales-upload mode
  sales_upload.py                  Optional second analysis mode: parse/validate an uploaded
                                    CSV/XLSX sales history, check its overlap with the real
                                    news corpus, and derive a profile via sensitivity_regression.py
  news_browser.py                  Read-only browse layer over all three corpora (seed / live /
                                    behind GET /api/news - normalizes their record
                                    shapes and reports which corpora actually feed scoring
scripts/
  generate_news.py                 Builds data/news.json + news_embeddings.npy
  generate_startups.py             Builds data/startups.json (identity only) + embeddings
  discover_subclusters.py          Builds data/subclusters.json (unsupervised, per dimension)
  hidden_ground_truth.py           Hidden per-startup templates + shock lags — NOT used at
                                    inference; only by the two scripts below
  simulate_profit_history.py       Builds data/profit_history.json using the hidden templates
  derive_sensitivity_profiles.py   Recovers each startup's real profile via sub-cluster lag
                                    regression, validates it against the hidden templates,
                                    writes it into data/startups.json
  train_interaction_matrix.py      Fits data/interaction_matrix.npy (W) and data/cvp_mean.npy
                                    from the derived profiles
  validate_umbrella_case.py        Sanity-checks the sub-cluster pipeline end to end (see below)
  ingest_news.py                   Thin CLI wrapper around marketintel.ingestion.run_ingestion_once()
                                    for a one-shot run or an external cron/Task Scheduler entry
  validate_scope_fix.py            Before/after audit of the scope fix against a stored batch
                                    (see below) - not part of the regular pipeline
  validate_fact_decomposition.py   Runs a constructed tax-policy article through fact
                                    extraction and checks it splits into facts with opposing
                                    polarity, not one blended record (see below)
  validate_comparative_matching.py Validates comparative_matching.py against real rate/tax
                                    changes and a similar-but-different pair (see below)
  validate_grounding.py            Validates grounding.py against the two known real
                                    hallucination cases, plus a false-positive check (see below)
  validate_sales_upload.py         Validates the sales-upload mode: column guessing,
                                    validation gate, coverage overlap, and (via a synthetic
                                    overlapping corpus) that the regression itself works
  validate_real_data_migration.py  Validates the seed-inference migration onto real data -
                                    coverage check, gate recalibration, per-dimension blending,
                                    and scope hybrid, all against the live real-fact corpus
data/                              Generated datasets + trained W (gitignored, see below)
```

## Setup

Requires Python 3.10+.

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -e .
```

## Generate the fabricated data

The `data/` folder is gitignored — generate it locally before first run
(this also downloads the `all-MiniLM-L6-v2` ONNX model on first use, ~90MB):

```bash
python scripts/generate_news.py                  # must run first
python scripts/generate_startups.py              # depends on news.json
python scripts/discover_subclusters.py           # depends on news.json
python scripts/simulate_profit_history.py        # depends on generate_startups + news
python scripts/derive_sensitivity_profiles.py    # recovers + validates the profiles
python scripts/train_interaction_matrix.py       # fits W on the derived profiles
python scripts/validate_umbrella_case.py         # optional: sanity-check the whole pipeline
```

`derive_sensitivity_profiles.py` prints a validation report — per-startup
recovered vs. true shock lag, and the correlation between each derived
profile and its hidden generation template. Check that report before
re-running the last step; a `W` trained on a broken recovery isn't worth much.
`validate_umbrella_case.py` is a second, independent check at sub-cluster
granularity (see "How it works" above) — worth running after any change to
the news templates or clustering parameters.

## Running the services

There are two long-running processes, each with its own start command, its
own port, and no dependency on the other. **Each one is safe to run without
the other** - neither command starts, waits for, or health-checks the other,
and the only thing they share is the `data/real_facts.json` file (which the
analysis engine re-reads per request and treats as optional).

**Start ONLY the analysis engine** (the web UI + `/api/analyze`, port 8000):

```bash
uvicorn server:app --port 8000 --reload
```

**Start ONLY the ingestion microservice** (real news collection, port 8502):

```bash
uvicorn ingestion_service:app --port 8502
```

**Start BOTH** - two separate terminals, in either order (the order genuinely
does not matter; see the independence check below):

```bash
# terminal 1
uvicorn server:app --port 8000 --reload
# terminal 2
uvicorn ingestion_service:app --port 8502
```

| | Analysis engine | Ingestion microservice |
|---|---|---|
| File | `server.py` | `ingestion_service.py` |
| Command | `uvicorn server:app --port 8000 --reload` | `uvicorn ingestion_service:app --port 8502` |
| Port | 8000 | 8502 |
| Surface | web UI, `/api/analyze`, `/api/sales/*` | `GET /health` only |
| Schedule | request-driven | one pass on startup, then every 30 min |
| Needs the other? | No | No |

If you only want a one-shot ingestion run rather than an always-on service,
use `python scripts/ingest_news.py` instead (same pipeline, no server, no
port - see "Real news ingestion" below for when to pick which).

**Independence is verified, not just asserted.** Re-checked against real,
separately-launched processes: (a) analysis engine up with ingestion never
started - serves normally, including the sales-upload and CVP-less paths;
(b) ingestion up, analysis engine stopped and restarted underneath it -
ingestion keeps serving, analysis comes back clean; (c) both stopped, then
started ingestion-first and analysis-first - no crash either way, no
startup-order dependency, no tracebacks in any process log.

## Deployment topology

| Component | Host | Notes |
|---|---|---|
| `server.py` (API + analysis) | Render, one free Web Service | Free tier spins down when idle; expect cold-start latency on the first request |
| `web/index.html` + assets | Vercel (static) | No build step; it is a single self-contained file |
| Postgres + pgvector | Supabase (free) | All *growing* data: facts, announcements, embeddings, ingestion runs, and the review queue |

**Ingestion is triggered from the production app itself, not a schedule.**
The "Ingest & review" page (topbar "..." menu) is the live entry point: a
"Run GDELT ingestion now" button for real-time world news, and a JSON upload
for manually-scraped LPU announcements. Both feed the same human-in-the-loop
queue (`review_batches`/`review_items`) - chunk, approve, embed+summarize,
approve again - before anything reaches the scored `facts`/`announcements`
tables. See `src/marketintel/review_pipeline.py`.

A separate bulk/scheduled path exists (`.github/workflows/ingest.yml`,
`scripts/ingest_lpu_data.py` + `scripts/sync_lpu_to_supabase.py`) but is
**deliberately dormant** (its cron trigger is commented out): it writes
straight to the scored tables with no approval step, which would both bypass
the review queue and compete with it for the same daily Groq quota. It's kept
for a possible later return to unattended bulk processing, not deleted.

**What lives in the database vs. what ships as files.** Anything that grows at
runtime is in Postgres (facts + `halfvec(384)` embeddings, announcements,
ingestion run status, exclusions). Static training artifacts stay as deployed
files, because they are regenerated wholesale by offline scripts and never
mutated at runtime: `subclusters.json`, `startups.json`,
`interaction_matrix.npy`, `cvp_mean.npy`.

Apply the schema once with:

```bash
psql "$DATABASE_URL" -f db/schema.sql     # idempotent, safe to re-run
```

## Operational risks

These are accepted tradeoffs of running entirely on free tiers, documented
because each has bitten this project or plausibly will. None is a bug to
silently work around.

**1. Supabase pauses free projects after 7 days of low activity, and recovery
is manual.** A paused project must be resumed from the Supabase dashboard
before anything works; the API simply fails until someone clicks resume.
Restoration is possible within a 1-year window.

**There is currently no automatic keep-alive.** The bulk ingestion workflow
that used to write to the database every 30 minutes is now deliberately
dormant (see "Deployment topology" above) - ingestion is triggered manually,
from the "Ingest & review" page, so database activity now tracks actual usage
of the app rather than a schedule. If nobody visits the app or runs an
ingestion for 7+ days, Supabase's pause condition can trigger. Two ways to
handle this, neither implemented yet: visit the app (or `POST
/api/review/gdelt/start`) periodically yourself, or re-enable the dormant
GitHub Actions cron purely as a heartbeat (uncomment its `schedule` trigger -
even a run that finds nothing to do still writes to the database).

**2. Render free-tier spin-down.** The API sleeps when idle, so the first
request after a quiet period pays a cold start (~50s).

### Hosting requirements

LLM calls (fact decomposition and LPU classification) go through
`config.LLM_PROVIDER`, which selects between the hosted **Groq API** and a
**local Ollama** model. Both call sites route through it; prompts, parsing,
grounding and comparative matching are identical either way.

**Under `LLM_PROVIDER = "groq"` there is no persistent local model process.**
Fact extraction needs only outbound HTTPS to `api.groq.com` plus a
`GROQ_API_KEY` environment variable. That removes the RAM-heavy always-on
process that previously had to sit alongside the two services, so the app can
run on a small instance sized for FastAPI and the sentence-transformer
embedder rather than for a multi-GB language model. (No Oracle-Cloud-specific
constraint was ever recorded in this repo, so there is nothing to retract —
this simply documents the current, lighter requirement.)

**Still required regardless of provider:** `all-MiniLM-L6-v2` runs locally for
embeddings, via **`fastembed`** (ONNX Runtime) — not `sentence-transformers`
(PyTorch). This was a real, measured constraint, not a preference: with
`sentence-transformers`, a plain FastAPI process running one real embedding
call sat at **~500 MB RSS**, against Render free tier's **512 MB hard limit**
— a ~2% margin that would OOM-kill the service under real concurrent load.
Measured again with `fastembed` in its place (same model, same weights, same
384-dim output, via ONNX Runtime instead of PyTorch — no `torch` dependency at
all): **~252 MB RSS**, a ~51% margin. Switching to Groq removes the
*generative* model from the host; this swap is what makes the *embedding*
model safe to keep running there too.

```bash
export GROQ_API_KEY=...       # read from the environment, never stored in the repo
```

**Choose the provider by workload — this is measured, not assumed:**

| Workload | Volume | Recommended | Why |
|---|---|---|---|
| Live ingestion | a few articles / 30 min | `groq` | Far below any quota; faster per call; no local RAM |
| Bulk LPU ingestion | 44,695 announcements | `ollama` | Groq's free tier makes it **~343 days** vs **~9.4 days** locally |

Groq's free tier allows 1,000 requests/day and 200,000 tokens/day
(`openai/gpt-oss-20b`). At ~1,590 tokens and 2 requests per announcement, the
**token** cap binds roughly 4× harder than the request cap and is what makes
bulk ingestion impractical on the free tier. See "Groq feasibility" in
CLAUDE.md for the full arithmetic.

### Browsing what's actually been collected

The topbar "..." menu → **"Browse news data"** opens a read-only view of every
news item the system holds, across all three corpora, backed by
`GET /api/news` (`src/marketintel/news_browser.py`). It shows a count and date
range per corpus plus, importantly, whether that corpus **currently feeds
analysis**:

| Corpus | File | Feeds `/api/analyze`? |
|---|---|---|
| Fabricated seed | `data/news.json` | Yes |
| Live ingested | `data/real_facts.json` | Yes |

Each corpus is labelled with whether it feeds scoring, so a corpus that is
stored but not wired into the serving path could never look equivalent to one
that is. Filter by corpus, free text, scope, polarity, or top PESTLE/Porter's
dimension; filtering and paging are server-side.

### What the analysis engine serves

This serves the app at `http://localhost:8000` as a three-page flow - a
landing page ("Get started"), an upload page (CVP textarea + optional
CSV/XLSX sales-history upload on one page), and the analysis results -
all one file with JS-toggled states, no reload between them. Styled with
the "Cobalt Grid" theme (light by default, dark via the topbar toggle,
choice persisted in the browser's `localStorage`).

**Runs standalone, with or without ingestion.** `server.py` only requires the
fabricated data pipeline above - it does NOT require `ingestion_service.py`
(or any real data) to be running. If `data/real_facts.json` /
`real_fact_embeddings.npy` are missing, empty, corrupted, or mutually
inconsistent (a stale embeddings file with a different row count than the
facts list), `/api/analyze` degrades to seed-only analysis rather than
raising - every response carries `"live_facts_count"` and `"seed_only"` so
this is visible to the caller, not silently indistinguishable from a normal
result. This was a real, previously-unhandled bug (an empty `real_facts.json`
crashed with an unhandled `JSONDecodeError` -> 500) - see `CLAUDE.md`'s
"Known gaps" for the fix and the three scenarios proving the two processes
are genuinely independent.

## Real news ingestion

Independent of the fabricated-data pipeline above and not required to run
the app. Requires `data/news.json` and `news_embeddings.npy` to already
exist - that's the seed corpus every inference (relevance, polarity, scope)
is looked up against. The pipeline itself (`src/marketintel/ingestion.py`)
is the same code either way - pick whichever of the two ways to run it fits:

**Grounding safeguards and comparative-fact matching**
(`src/marketintel/grounding.py` / `comparative_matching.py`) - a non-content
pre-filter before any Ollama call, a post-decomposition check rejecting facts
with fabricated numbers, HTML-unescaping of fetched titles, and
comparative-fact matching for bare state-value facts. Both modules were
originally written for a historical GDELT bulk backfill (since removed) and
were kept because this live path depends on them. The pipeline's step order
is unchanged - fetch -> decompose -> dedup -> seed transfer -> relevance
gate -> write - only the new checks are inserted at the right points within
it. Rejections are logged separately: `data/ingestion_noncontent.jsonl` (pre-
filter), `data/ingestion_ungrounded.jsonl` (grounding check),
`data/ingestion_unmatched_directional.jsonl` (comparative matches that
found no qualifying prior value).

**Fact extraction needs Ollama running locally** (optional, but recommended -
without it, every article decomposes into exactly one unmodified fact):

```bash
# one-time setup
ollama pull llama3.2:3b   # or whatever OLLAMA_MODEL is set to in config.py
ollama serve              # leave running; defaults to http://localhost:11434
```

(On Windows, the installer registers Ollama as a background service that
starts automatically - `ollama serve` will then just report the port's
already in use, which means it's already running; no need to start it
again.)

If Ollama isn't reachable when `ingest_news.py` or `ingestion_service.py`
runs, `fact_extraction.py` logs a warning and falls back to a single fact per
article rather than failing the run - decomposition quality degrades to a
no-op, ingestion doesn't stop.

**On CPU-only hardware, give it real time.** `OLLAMA_TIMEOUT_SECONDS`
defaults to 120, not something smaller - a cold first call was observed
taking ~80s on CPU-only hardware (~32s just loading the model's weights
into memory) with no GPU acceleration. A tighter timeout doesn't fail
cleanly here, it silently degrades every extraction to the single-fact
fallback even with Ollama installed and working - which looks identical to
"Ollama isn't running" in the logs unless you're checking for it. If
extraction is still timing out after the model's warmed up (i.e. after the
first call), that's a real problem worth investigating, not something to
paper over with a bigger number.

**Option A - `ingestion_service.py`, a standalone microservice.** Runs one
ingestion pass immediately on startup, then every 30 minutes for as long as
the process stays up (a plain `asyncio` loop, no external scheduler), on its
own port so it never conflicts with `server.py` (this is the same command
listed under "Running the services" above, repeated here for context):

```bash
uvicorn ingestion_service:app --port 8502
```

`GET http://localhost:8502/health` reports the last run's start/finish
timestamps, articles fetched, facts extracted/excluded/added, and whether it
succeeded or errored - the only HTTP surface this service exposes; there's
no way to trigger a run or change anything from outside it.

**Option B - `scripts/ingest_news.py`, a one-shot CLI**, for a manual run or
an external cron/Task Scheduler entry instead of a long-running process:

```bash
python scripts/ingest_news.py
```

```bash
# cron (Linux/Mac), every 2 hours
0 */2 * * *  cd /path/to/project && .venv/bin/python scripts/ingest_news.py >> data/ingest.log 2>&1
```

```powershell
# Windows Task Scheduler (PowerShell), every 2 hours
schtasks /create /tn "MarketIntelIngest" /tr "'C:\path\to\project\.venv\Scripts\python.exe' 'C:\path\to\project\scripts\ingest_news.py'" /sc hourly /mo 2
```

Either way, every write to `data/real_articles.json`, `data/real_facts.json`,
`real_fact_embeddings.npy`, and `data/ingestion_state.json` goes through
`atomic_io.py` (write to a temp file, then rename over the original) - so a
concurrent reader of those files never observes a partially-written one,
whether that reader is another process or a future version of `server.py`
that consumes real facts.

Check `data/ingestion_samples.jsonl` after the first few runs - it's a
running log of newly stored facts (with their source headline alongside) and
their inferred relevance, polarity, and scope, meant for eyeballing before
trusting this data downstream - the fact-extraction step in particular
should be spot-checked against its source for hallucinated or dropped
details (`scripts/validate_fact_decomposition.py` does this for a
constructed test case, and against a sample of whatever's currently stored).
Scope is meaningfully better since the relevance-gate + best-match fix, but
still worth scrutinizing - see "How it works" above.
`data/ingestion_excluded.jsonl` logs everything the relevance gate rejected
(fact text, source headline, timestamp, max relevance) - review it
occasionally to make sure the gate isn't excluding things it shouldn't.

`python scripts/validate_scope_fix.py` re-scores scope for whatever's
currently in `data/real_facts.json` and reports any drift against what's on
record - a general audit, not tied to one specific historical batch anymore.
`python scripts/validate_fact_decomposition.py` runs a constructed
two-claim tax-policy article through extraction and checks it actually
splits into two facts with opposing polarity (requires Ollama to be running
for a meaningful result - otherwise it reports itself as inconclusive rather
than a false pass).

## Sales history upload

An OPTIONAL second analysis mode, layered on top of the CVP flow rather than
replacing it - the CVP text box stays required and its result is always
computed and shown. Uploading a CSV/XLSX of your own daily revenue history
adds a second, richer result derived from regressing that history against
a news corpus, instead of estimating sensitivity purely from similarity to
comparable fabricated businesses.

> **Current default: `config.SALES_REGRESSION_NEWS_SOURCE = "fabricated"`.**
> This is a TIME-BOXED demo override, not the production setting - the real
> news corpus is presently too sparse (~2 days of coverage) for the
> overlap gate below to ever pass, so this flag makes the regression run
> against the fabricated seed corpus instead, so it actually produces
> output today. Every result computed this way is labeled to the caller
> (`news_source: "fabricated"`) and rendered behind a mandatory,
> impossible-to-miss banner on the analysis page - never presented as
> derived from real live news. Flip the flag back to `"real"` once real
> coverage grows; see CLAUDE.md for the full reasoning.

**The flow, and why it's two confirmed steps, not one:**

1. `POST /api/sales/upload` (multipart file) - parses the sheet and
   BEST-GUESSES which column is the date and which is the revenue/sales
   metric (by column name first, then by content). This guess is always
   returned for review, never trusted silently - the frontend shows it as
   two pre-filled dropdowns you can correct before anything is computed.
2. `POST /api/sales/confirm` `{upload_id, date_col, value_col}` - validates
   volume and quality (at least 90 distinct valid daily observations,
   duplicate-date rows under 5% of the sheet, at least 50% date-range
   density) and, if that passes, immediately computes the derived profile.
   A failure here returns a plain-language reason and the frontend falls
   back to CVP-only - it never runs the regression on data that doesn't
   clear the bar.
3. Pass the resulting `upload_id` as `sales_upload_id` in a normal
   `POST /api/analyze {"cvp": ..., "sales_upload_id": ...}` call. The
   response's `sales_derived` field is `null` unless a valid, sufficiently-
   overlapping profile exists; when present, `primary_result: "sales"`
   tells the frontend to lead with it, with the CVP-similarity result
   still shown alongside, explicitly labeled as the lower-confidence
   comparison (`cvp_result_label`).

**The regression itself is the same mechanism the offline training pipeline
uses** (`src/marketintel/sensitivity_regression.py`, extracted out of
`scripts/derive_sensitivity_profiles.py` so both paths call one
implementation) - lagged ridge regression of daily profit changes against
the preceding day's per-sub-cluster relevance-times-polarity signal, same
math, different inputs (a real uploaded series against either the real news
corpus or, under today's demo default above, the fabricated corpus).
`sales_upload.derive_sales_profile()` is the single entry point that
dispatches between the two based on `SALES_REGRESSION_NEWS_SOURCE` - callers
don't hardcode which news pool to use.

**Two gates specific to the real-data path, both reported explicitly rather
than silently degrading:**

- **Per-dimension coverage** - the regression's feature columns are
  restricted to only the PESTLE/Porter's dimensions currently trusted for
  real data (the same `real_data_inference.assess_dimension_coverage()`
  check live ingestion uses - see "Real news ingestion" above for the
  current pass/fail table). Uncovered dimensions are reported explicitly
  in the response (`uncovered_dimensions`) rather than silently defaulted
  to zero, which would misleadingly read as "no sensitivity" instead of
  "not enough real data yet."
- **Upload<->real-news-coverage overlap** - a regression can only use days
  where BOTH the uploaded sales history and the real news corpus have
  data. `compute_coverage_overlap()` computes this window explicitly and
  requires at least 90 days of it (the same bar as the upload's own
  volume check) before running anything. **Given the real news corpus
  currently spans only a couple of days** (it's early - see "Real news
  ingestion" above), this will presently report insufficient overlap for
  almost any realistic historical sales upload, and correctly fall back
  to the CVP-only result with an explicit message - this is expected
  behavior given how little real history has accumulated so far, not a
  bug, and should resolve naturally as the corpus grows.

`python scripts/validate_sales_upload.py` validates all of this (9/9
checks): column guessing on a realistic messy sheet, the validation gate
correctly rejecting a too-short upload and accepting a clean one, the
overlap check running correctly against the actual live real-fact corpus
(confirming the expected graceful "insufficient" result today), and - to
prove the regression mechanism itself works, not just that it fails
gracefully - a constructed synthetic real-news corpus with genuine 120-day
overlap and a known injected political-tariff signal, which the regression
correctly recovers (right lag, right sign, R²=0.88).

**Explicitly out of scope for this pass**: uploaded sales data is kept in
an ephemeral, in-process store (`server.py`'s `_uploads` dict) - never
written to a shared file, never folded into the reference pool other
users' CVP-similarity analysis draws on, and never used to retrain `W`
(a real consent/data-use decision, not a default). Only one date column +
one numeric metric column is supported - no multi-metric uploads yet.

## Current scope

This phase is intentionally limited to what's described above:

- CSV/XLSX sales-history upload now exists as an OPTIONAL second analysis
  mode (see "Sales history upload" below) - CVP input remains required
  and unchanged as the default path. Single date column + single numeric
  metric column only; no multi-metric uploads yet. Uploaded data is never
  folded into the shared reference pool or used to retrain `W`.
- No stakeholder/supplier/competitor confirmation screen.
- The CVP analysis pipeline (`server.py`) now scores against the fabricated
  seed corpus AND real ingested facts together (see item 8 above). What's
  still fabricated-only: sub-cluster discovery, the per-startup regression,
  and training the shared matrix `W` itself - decomposing 1000 already-
  atomic, template-generated fabricated articles into "facts" wouldn't be
  meaningful, and retraining that whole foundation is out of scope
  regardless. Real facts only ever get assigned into sub-clusters that
  already exist from that one-time fabricated-only discovery run.
- Live ingestion (`ingestion_service.py`) is world-level sources only (BBC
  World, Al Jazeera, Google News, GDELT DOC API), and covers only forward
  time from when it started running - there is no historical depth. A
  historical GDELT bulk backfill was built and then removed (see CLAUDE.md
  for the reasoning: ~4.2 months of estimated processing for the scoped-down
  run, ~14.6% fabricated-number rate in what it had collected, and it was
  never wired into scoring). Jalandhar/Kapurthala/Phagwara depth remains
  thin for the same reason: GDELT almost certainly doesn't tag these at
  usable granularity, and scraping local newspaper archives is out of scope.
  LPU/university-level data is sourced separately, not part of this
  pipeline.
- Real headline relevance and polarity are inferred by pooled nearest-
  neighbor lookup, and scope by a separate per-class-best-match lookup with
  a relevance gate in front of it - not a trained classifier or
  content-based location extraction in any case. The reference pool for
  this lookup (live ingestion only - see below) is now the accumulated real
  corpus itself, per dimension/scope class once there's enough of it -
  see "Real news ingestion" above for the coverage numbers and which
  dimensions still fall back to the fabricated corpus.
- Geographic scope is stored per article but doesn't yet weight the scoring.
- **`W` remains trained entirely on fabricated data, and this is NOT
  changed by the real-data seed-inference migration above.** Migrating
  `seed_inference.py`'s k-NN lookups onto real data only changes how new
  real facts get their relevance/polarity/scope LABELED - it has no effect
  on the shared interaction matrix `W` itself, which was fit once, offline,
  against the 50 fabricated startups' derived sensitivity profiles and
  their linked fabricated news articles (see "How it works" above). Every
  `/api/analyze` prediction is therefore still indirectly shaped by
  fabricated data through `W`, regardless of how well-labeled real facts
  are. This won't be fixed until real company financial history exists to
  retrain `W` against (the same role `data/profit_history.json` currently
  plays, but from actual observed outcomes instead of a fabricated
  simulation) - not attempted here, and not a small change: it would mean
  re-deriving sensitivity profiles from real financial data, not just
  swapping a lookup table the way this round of changes did.
- `W` is trained once in batch on the fabricated startups, not updated
  online from real observed outcomes — there aren't any yet.
- The dimension hierarchy is two levels deep (dimension → sub-cluster) only.
  A third level (e.g. rainfall → increased/decreased) needs meaningfully
  more articles and startups behind it than this fabricated scale supports -
  revisit once real data volume justifies it.
- `ingestion_service.py` has no authentication and no way to trigger a run
  or change its schedule from outside the process - by design, for now. It's
  meant to run standalone on a trusted local machine, not be exposed.
- Fact extraction mostly has only a headline to work with (the sources
  above are RSS/API feeds, not full article scrapes - fetching and parsing
  arbitrary article pages is a meaningfully bigger scope not attempted
  here). In practice, live testing with Ollama + `llama3.2:3b` actually
  running still produced real multi-fact splits from headlines alone (a
  casualty headline splitting into separate death/injury/event facts), so
  this happens more than "rarely" - but it also produced a confirmed
  hallucination (a specific named attribution invented from a headline
  that never made it) on the very first live run, precisely because a bare
  headline gives the model so little to ground itself in. Both outcomes
  are documented in "How it works" above with the exact examples. Spot-
  check before trusting this at scale, per CLAUDE.md - the mechanism is
  real, not a rubber stamp.
- Storyline/event-chain linking across facts over time isn't built yet -
  it's the reason articles keep a `fact_ids` list rather than being
  discarded once decomposed, but nothing consumes that linkage yet.
- Real news storage is flat JSON + `.npy` (matching the fabricated dataset's
  structure) - no vector database yet.
- GDELT DOC 2.0's free endpoint is genuinely intermittent - confirmed
  working (fetched real articles) in multiple runs this session, and
  connection-timed-out in others, on the same network. Already handled
  (logged and skipped for that run, doesn't abort the other three
  sources); not something to "fix" so much as a real characteristic of a
  free, unauthenticated, rate-limited public API.
- The 50 fabricated startups' CVP text carries explicit LPU framing
  throughout, and `W`/`cvp_mean.npy` have since been retrained against it
  (see below) - no longer a stale-artifact concern.
- **Different CVPs producing near-identical output was diagnosed and
  fixed** across several rounds: `W`'s effective rank was originally only
  ~5/384; growing 20→50 startups barely helped (~6); the deeper cause was
  the hidden ground-truth *target* profiles themselves having effective
  rank only ~3.4-4.3/11 (fixed by adding fixed-seed per-dimension Gaussian
  noise, std=25, to each hidden template - see "How it works" above); and
  the actual remaining cause was `W`'s dominant singular direction being
  ~88% aligned with the mean of all training CVP embeddings - i.e. the
  "generic business pitch text" component every CVP shares, which ridge
  regression spent a large share of `W`'s capacity modeling in this
  heavily underdetermined system. Fixed by mean-centering CVP embeddings
  before every fit and every inference call. Verified on a 5-CVP
  discrimination test: real-business-to-real-business output cosine
  similarity dropped from a collapsed 0.90-0.99 to a properly varied
  -0.31 to 0.68, at a training-fit MAE cost of only 27.9 → 29.1.
- **New regression surfaced by that work**: `scripts/validate_umbrella_case.py`'s
  deforestation-near-zero check now fails narrowly (score ~50% over its
  threshold). Confirmed this is NOT caused by the CVP-centering fix or the
  hidden-template noise perturbation - it reproduces identically with both
  disabled, so it predates this round of changes (most likely introduced
  by the earlier 20→50 startup expansion). The rain-positive and
  drought-negative checks in the same test still pass. Not yet
  root-caused or fixed.

See `CLAUDE.md` for the full project context and longer-term roadmap.
