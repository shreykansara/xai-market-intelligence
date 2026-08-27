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
2. **Fabricated startup dataset** (`data/startups.json`) — 20 LPU-based
   startups spanning fintech, edtech, agritech, D2C hardware, SaaS, and
   healthtech. Each has a CVP and 3-5 linked news article IDs. Their
   PESTLE/Porter's sensitivity profile is *not* hand-authored — it's
   recovered from a fabricated profit history (below), and that recovered
   profile is what supervises the interaction matrix. CVPs are embedded
   with the same model.
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
   political/economic sensitivity) but **never exposed to the learning
   pipeline** — only used to fabricate a daily profit/revenue series
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
   matrix. In practice this recovers the true shock lag for all 20
   startups and correlates at ~0.90 with the hidden templates even at
   sub-cluster granularity.
5. **Interaction matrix** (`data/interaction_matrix.npy`) — a single shared
   (384x384) matrix `W`, fit once in batch. For a (news, CVP) pair,
   `gate = news_embedding · W · cvp_embedding` is one scalar capturing how
   strongly that business reacts to that news in general — direction and
   magnitude — independent of which dimension is involved. `W` is fit by
   ridge regression against the 20 startups' *derived* sensitivity vectors
   (20 startups × 11 dimensions = 220 training examples), solved in the
   ridge *dual* via the kernel trick, since the 384×384 = ~147k parameters
   vastly outnumber the 220 examples. The regularization strength was
   chosen by leave-one-startup-out cross-validation, not by in-sample fit
   (in-sample error only keeps falling as regularization drops toward zero
   in a system this underdetermined, which would just pick a `W` that
   memorizes the 20 startups).
6. **Analysis** — for a submitted CVP, every one of the 1000 news articles
   gets a `gate` from `W`. Within each dimension, `gate` combines with an
   article's own labeled relevance and polarity to give its signed
   contribution to whichever sub-cluster it belongs to; summing a
   dimension's sub-cluster totals gives that dimension's raw score. Each
   chart's 6 or 5 raw scores are then independently rescaled so the
   largest magnitude hits 100, sign preserved. (`analysis.py` also flags
   dimensions whose raw magnitude is under 10% of the submission's
   strongest as negligible; the current frontend's two-color helping/
   hurting design doesn't surface that flag, but a near-zero dimension
   still reads as such by its small radius/small score.)
7. **Output** — two Plotly radar charts (indigo fill, green/red vertices for
   direction) side by side, with the news breakdown underneath: one section
   per dimension (ranked by |score|, click to expand), sub-grouped by
   sub-cluster, down to the specific bordered article rows driving each
   score - so every number stays traceable back to a real, inspectable
   fabricated article, at both the dimension and the sub-topic level.

8. **Real news ingestion** (`scripts/ingest_news.py`, `data/real_news.json` +
   `real_news_embeddings.npy`) — a separate, parallel track from the
   fabricated dataset above, not yet wired into the CVP analysis. Pulls
   world-level headlines from four free, no-key sources: BBC World and Al
   Jazeera's own RSS feeds, Google News RSS (queried by topic - `WORLD` -
   not scoped to any one outlet), and the GDELT DOC 2.0 API via the
   open-source `gdeltdoc` package (*not* GDELT Cloud, a separate paid
   product). Reuters isn't used: its public RSS was discontinued in 2020
   and programmatic access now requires a paid license. Only title, publish
   timestamp, link, and derived tags are stored — never article body text,
   and no vector database. Each run is incremental per source (a small
   `data/ingestion_state.json` cursor tracks the last-seen publish time) and
   safe to overlap: every new headline is embedded and compared by cosine
   similarity against the last 48 hours of stored headlines, and anything
   ≥0.92 similar is folded into the existing record (`mention_count`
   incremented) instead of creating a duplicate — verified in practice by
   cross-source stories (the same event covered by two or three wires)
   landing in one record. GDELT's free endpoint is rate-limited and
   occasionally times out; a failed source is logged and skipped for that
   run rather than aborting the others.

   **Labeling is one mechanism for all three fields** (`src/marketintel/
   seed_inference.py`): relevance, polarity, *and* geographic scope are all
   inferred by the same similarity-weighted vote among a headline's 10
   nearest neighbors in the fabricated seed corpus - the only hand-labeled
   data anywhere in the system. There's no per-source scope tagging and no
   trained polarity classifier; every field is read off the same
   nearest-neighbor lookup. A sample of each run's newly stored headlines
   (with their inferred relevance, polarity, and scope) is printed and
   appended to `data/ingestion_samples.jsonl` for manual spot-checking.

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
server.py                          FastAPI backend - adapts the existing analysis pipeline to
                                    HTTP/JSON (POST /api/analyze) and serves web/
web/
  index.html                       The whole frontend: two-state page (input / results), inline
                                    CSS + JS, Plotly.js-driven radar charts
  vendor/plotly.min.js             Vendored Plotly.js (copied from the plotly Python package's
                                    bundled asset) - no CDN dependency
src/marketintel/
  config.py                        Dimension names, scopes, file paths, constants
  embeddings.py                    sentence-transformers wrapper
  data_loader.py                   Loads generated news/startup/subcluster/real-news data + W
  analysis.py                      Gate/sub-cluster contribution scoring + roll-up + drill-down data
  seed_inference.py                Relevance/polarity via pooled k-NN vote, a relevance-gate
                                    threshold, and scope via per-class-best-match - all looked
                                    up against the fabricated seed corpus, for real headlines
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
  train_interaction_matrix.py      Fits data/interaction_matrix.npy (W) from the derived profiles
  validate_umbrella_case.py        Sanity-checks the sub-cluster pipeline end to end (see below)
  ingest_news.py                   Scheduled real-world ingestion (see below) - independent of
                                    the fabricated-data scripts above
  validate_scope_fix.py            Before/after audit of the scope fix against a stored batch
                                    (see below) - not part of the regular pipeline
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

## Real news ingestion

Independent of the fabricated-data pipeline above and not required to run
the app. Requires `data/news.json` and `news_embeddings.npy` to already
exist - that's the seed corpus every inference (relevance, polarity, scope)
is looked up against:

```bash
python scripts/ingest_news.py
```

Re-run it every 1-4 hours to keep up with the wires - it's incremental and
safe to overlap. Pick whatever scheduler is available:

```bash
# cron (Linux/Mac), every 2 hours
0 */2 * * *  cd /path/to/project && .venv/bin/python scripts/ingest_news.py >> data/ingest.log 2>&1
```

```powershell
# Windows Task Scheduler (PowerShell), every 2 hours
schtasks /create /tn "MarketIntelIngest" /tr "'C:\path\to\project\.venv\Scripts\python.exe' 'C:\path\to\project\scripts\ingest_news.py'" /sc hourly /mo 2
```

Check `data/ingestion_samples.jsonl` after the first few runs - it's a
running log of newly stored headlines with their inferred relevance,
polarity, and scope, meant for eyeballing before trusting this data
downstream. Scope is meaningfully better since the relevance-gate + best-
match fix, but still worth scrutinizing - see "How it works" above.
`data/ingestion_excluded.jsonl` logs everything the relevance gate rejected
(headline, timestamp, max relevance) - review it occasionally to make sure
the gate isn't excluding things it shouldn't.

To directly compare the old scope mechanism against the new one on a
concrete batch (rather than just reading the samples), run
`python scripts/validate_scope_fix.py` while `data/real_news.json` still
holds records classified under the old logic.

## Current scope

This phase is intentionally limited to what's described above:

- No CSV/XLSX upload — next phase.
- No stakeholder/supplier/competitor confirmation screen.
- The CVP analysis pipeline (`server.py`) still scores against the
  fabricated news dataset only - real ingested headlines
  (`data/real_news.json`) aren't wired into it yet.
- Real ingestion is world-level sources only (BBC World, Al Jazeera, Google
  News, GDELT). No India/Punjab-specific regional feeds yet - that's next,
  and should also make scope inference (below) meaningfully more accurate
  by giving real local headlines to match against.
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
- Real news storage is flat JSON + `.npy` (matching the fabricated dataset's
  structure) - no vector database yet.

See `CLAUDE.md` for the full project context and longer-term roadmap.
