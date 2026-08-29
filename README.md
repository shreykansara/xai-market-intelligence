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
   `all-MiniLM-L6-v2` sentence-transformer model.
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
7. **Output** — two Plotly radar charts (indigo fill, green/red vertices for
   direction) side by side, with the news breakdown underneath: one section
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

10. **Historical GDELT bulk backfill** (`src/marketintel/gdelt_bulk.py` +
    `gdelt_backfill.py`, run via `scripts/run_gdelt_backfill.py`) - a
    separate, one-off/batch collection process from `ingestion_service.py`
    above, which keeps running independently on its own schedule. Writes to
    its own files (`data/backfill_articles.json` / `backfill_facts.json` /
    `backfill_fact_embeddings.npy`) so the two never contend over the same
    files, and isn't yet merged into the live scoring path (tracked
    separately). See "Historical GDELT backfill" below for the full runbook,
    the timing investigation that shaped its scope, and pilot findings.

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
   neighbors in the fabricated seed corpus - the only hand-labeled data
   anywhere in the system. There's no per-source scope tagging and no
   trained polarity classifier; every field is read off the same
   nearest-neighbor lookup. Dedup (cosine similarity ≥0.92 against the last
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
  index.html                       The whole frontend: two-state page (input / results), inline
                                    CSS + JS, Plotly.js-driven radar charts
  vendor/plotly.min.js             Vendored Plotly.js (copied from the plotly Python package's
                                    bundled asset) - no CDN dependency
src/marketintel/
  config.py                        Dimension names, scopes, file paths, constants
  embeddings.py                    sentence-transformers wrapper
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
  gdelt_bulk.py                    GDELT 2.0 bulk export file access (GKG only) - lists/downloads
                                    15-min files, extracts page title + country tags, tier filter
  gdelt_backfill.py                The historical backfill pipeline itself (reordered vs. the
                                    live path) - checkpointed/resumable, separate data files
                                    from ingestion.py's
  comparative_matching.py          Finds the nearest earlier fact about the same subject to
                                    compute a direction for a bare state-value fact, used only
                                    by the backfill above
  grounding.py                     Pre-filter (non-content titles) + post-decomposition
                                    grounding check (rejects facts with fabricated numbers) -
                                    used only by the backfill above
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
  run_gdelt_backfill.py            CLI entry point for the historical GDELT bulk backfill
                                    (see "Historical GDELT backfill" below)
  validate_comparative_matching.py Validates comparative_matching.py against real rate/tax
                                    changes and a similar-but-different pair, before it ever
                                    touches real backfill data (see below)
  validate_grounding.py            Validates grounding.py against the two known real
                                    hallucination cases, plus a false-positive check (see below)
  audit_grounding_retroactive.py   Read-only audit: re-checks already-collected backfill facts
                                    against grounding.py, reports the rejection rate + samples
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
(this also downloads the `all-MiniLM-L6-v2` model on first use, ~90MB):

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

## Start the server

```bash
uvicorn server:app --reload
```

This serves the app at `http://localhost:8000`. Paste a CVP into the text
area and click **Run analysis** - the results view replaces the input on the
same page, no reload.

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

**Shares its grounding safeguards and comparative-fact matching with the
GDELT bulk backfill** (`src/marketintel/grounding.py` /
`comparative_matching.py`) - both ingestion codepaths call the same
underlying safety logic (a non-content pre-filter before any Ollama call, a
post-decomposition check rejecting facts with fabricated numbers,
HTML-unescaping of fetched titles, and comparative-fact matching for bare
state-value facts) rather than diverging. The live pipeline's own step order
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
own port so it never conflicts with `server.py`:

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

## Historical GDELT backfill

A separate, one-off/batch collection process from `ingestion_service.py`
above - that keeps running independently on its own 30-minute schedule for
ongoing Punjab/LPU-area coverage. This backfill pulls **historical** World/
India data from GDELT 2.0's bulk export files (`data.gdeltproject.org`), not
the DOC 2.0 API (~3 months lookback only) or RSS (no history at all).

**Timing first, before running anything at real scale.** A real pilot (8 GKG
files sampled across one day, measured end-to-end, then extrapolated) found
the full 2-year World(broad)+India backfill would take **~4.7 years**
unattended - dominated almost entirely by Ollama fact decomposition (mean
3.35s/call). Scoped down to **India-tier only** (country-tag filtered before
embedding, not after) - estimated **~4.2 months**. World-broad coverage and
the Punjab-level extension are both deferred; see `CLAUDE.md`'s "Known gaps"
for the full numbers and the options considered.

**Reordered pipeline, distinct from the live per-item order above**: fetch
(GDELT bulk, tier-filtered) -> embed -> relevance gate -> only then fact
decomposition (Ollama) on survivors -> dedup -> seed inference
(relevance/polarity/scope) -> comparative-fact matching -> atomic write. The
gate runs BEFORE decomposition here specifically to avoid spending Ollama
calls on records that were never going to pass it anyway.

**Comparative-fact matching** (`src/marketintel/comparative_matching.py`) -
for a bare state-value fact with no directional language of its own (e.g.
"GST on mobile phones is 18%"), finds the nearest strictly-earlier fact about
the same specific subject and computes a direction, rather than leaving
polarity ambiguous. A fact that already states its own direction ("raised
from 12% to 18%") skips the lookup entirely. Validate this BEFORE it ever
touches real data:

```bash
python scripts/validate_comparative_matching.py
```

Checks 3 real, independently verifiable rate/tax changes (India GST on
mobile phones, RBI repo rate, UK VAT) retrieve the correct prior value and
direction, and that a deliberately similar-but-different pair (mobile-phone
GST vs. textile GST) does NOT cross-match - including a synthetic worst-case
test that forces embedding similarity to 1.0, proving the entity-overlap
check is genuinely load-bearing rather than redundant with the similarity
gate. All 4 checks currently pass.

**Running it**, checkpointed and resumable at the granularity of one
15-minute GKG file (safe to interrupt and re-run with the same arguments):

```bash
# One week pilot, India tier (required before scaling up further):
python scripts/run_gdelt_backfill.py --tier india --start 2026-08-13 --end 2026-08-20

# Full backfill (run this unattended - see the timing estimate above):
python scripts/run_gdelt_backfill.py --tier india --start 2024-08-28 --end 2026-08-28
```

Writes/reads `data/backfill_articles.json`, `data/backfill_facts.json`,
`data/backfill_fact_embeddings.npy`, and `data/backfill_state.json` (progress
checkpoint) - entirely separate from `ingestion_service.py`'s
`real_*` files. `data/backfill_excluded.jsonl` logs everything the relevance
gate rejected; `data/backfill_unmatched_directional.jsonl` logs every bare
state-value fact that found no qualifying prior match for comparative
matching (expected to be common early in a run, before much history has
accumulated to match against).

**Grounding safeguards against hallucination** (`src/marketintel/grounding.py`)
- a pilot smoke test found fact decomposition fabricating specific,
plausible-sounding claims from content-free titles (a "COMMUNITY CALENDAR"
section label produced a fake GST policy change). Two independent layers,
wired into `gdelt_backfill.py`: (1) a pre-filter before any Ollama call,
rejecting obvious non-content titles (section labels, digests, horoscopes,
etc.); (2) a post-decomposition grounding check, rejecting any fact whose
stated numbers (percentages, currency, dates) don't trace back to the source
title - independent of Ollama's temperature setting, since lowering
temperature fixed JSON schema compliance but demonstrably not truthfulness.
Validate this BEFORE trusting pilot output:

```bash
python scripts/validate_grounding.py                  # against the known real failure cases
python scripts/audit_grounding_retroactive.py          # retroactive audit of already-collected facts
```

**A retroactive audit against the pilot's partial output found this is a
much bigger problem than the isolated cases suggested: ~17.9% of all facts
collected so far state at least one fabricated number**, and the pattern
looks like the model injecting real-world facts it memorized during training
(an actual RBI rate history, an actual GST change) into completely unrelated
articles - a movie review, an obituary - rather than random nonsense. The
pilot's original run is being left to finish undisturbed rather than
restarted (a retroactive audit, not a live fix); the safeguards above are
active in the pipeline code for the eventual full-scale run.

The audit also specifically samples ACCEPTED facts to check for a known
limitation of a substring-based grounding check - a number matching the
source by coincidence, not because it's really the same claim - and this
caught a real, fixable bug: GDELT stores titles with HTML entities
undecoded (e.g. literally "&#x2013;" instead of an em-dash), and one such
entity's embedded digits coincidentally "grounded" a fabricated Punjab
policy claim against an unrelated magazine masthead title. Fixed by
HTML-unescaping titles at the source (`gdelt_bulk.py`) and defensively in
`grounding.py` itself; re-sampling 20 fresh accepted facts afterward found
no further instances of this pattern.

**The pilot's spot-check gate is not yet satisfied** - see `CLAUDE.md`'s
"Known gaps" and "Open technical decisions" for exactly what's still
pending before the full India-tier backfill can start.

Separately (lower priority, not blocking): the fact-decomposition
over-splitting error above does NOT reliably fail the relevance gate - in
one measured case, the meaningless fragment scored HIGHER relevance (0.60)
than the coherent half of the same split (0.48), and the batch pipeline's
gate runs once per title before decomposition anyway, with no second gate
after it.

## Current scope

This phase is intentionally limited to what's described above:

- No CSV/XLSX upload — next phase.
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
  World, Al Jazeera, Google News, GDELT DOC API). The historical GDELT bulk
  backfill (see above) adds India-tier depth going backward in time, but is
  a separate store, not yet merged into live scoring.
- The GDELT bulk backfill explicitly does NOT cover Jalandhar, Kapurthala, or
  Phagwara - GDELT almost certainly doesn't tag these at usable granularity,
  and scraping local newspaper archives to fill that gap is out of scope.
  Those three scopes continue to be covered only by the live
  `ingestion_service.py` going forward. LPU/university-level data is sourced
  separately, not part of this pipeline. Merging the backfill's historical
  data into `server.py`'s live scoring path is also out of scope for now -
  tracked as a separate integration gap.
- Real headline relevance and polarity are inferred by pooled nearest-
  neighbor lookup against the fabricated seed corpus; scope by a separate
  per-class-best-match lookup with a relevance gate in front of it - not a
  trained classifier or content-based location extraction in any case, and
  scope is meaningfully improved but still not reliable - see "Real news
  ingestion" above.
- Geographic scope is stored per article but doesn't yet weight the scoring.
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
