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
  Runs standalone: if `real_facts.json`/`real_fact_embeddings.npy` are
  missing, empty, corrupted, or mutually inconsistent (a stale embeddings
  file), analysis silently falls back to the fabricated seed corpus alone
  rather than raising — see "Known gaps" below for the exact bug this
  fixed and how it's proven independent of `ingestion_service.py`. The
  response carries `live_facts_count` / `seed_only` so a seed-only result
  is visible to the caller, not indistinguishable from a normal one.
- **Optional second analysis mode: sales-history upload** — CVP input
  stays required and unchanged as the default; a caller can additionally
  upload a CSV/XLSX of their own daily revenue history
  (`POST /api/sales/upload` → best-guesses the date/value columns and
  returns them for confirmation, never trusted silently → `POST
  /api/sales/confirm` → validates volume/quality and, if it passes,
  immediately computes a profile derived from regressing the upload
  against the REAL news corpus). If confirmed and the upload<->real-news
  coverage overlap clears the same bar, `POST /api/analyze`'s response
  carries a `sales_derived` result alongside the unchanged CVP result,
  with `primary_result` indicating the sales-derived one takes precedence
  when both exist. See "Known gaps" below for the exact thresholds, the
  regression mechanism (shared with the offline training pipeline, not
  duplicated), and why this presently falls back to CVP-only almost every
  time given how little real news history has accumulated so far.
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
  blended record), also returning each fact's named entities. Falls back
  to treating the whole text as one fact (no entities) if Ollama is
  unavailable.
- **No manual labeling of real data, anywhere** (`seed_inference.py`) —
  relevance and polarity inferred via similarity-weighted k-NN (k=10);
  geographic scope inferred via per-class-best-match (each of the 7 scope
  classes' single closest match wins) specifically to prevent majority
  classes (India, Punjab) from winning on population size alone. The
  reference pool itself is now the accumulated REAL corpus, per dimension
  and per scope class, not the fabricated seed corpus — see
  `real_data_inference.py` and "Known gaps" below for the coverage-gated
  migration (some dimensions still fall back to fabricated data).
- **Relevance gate** — real facts scoring below the 5th percentile of
  the seed corpus's own max-relevance distribution (~0.58) are excluded
  before scope classification, logged to `ingestion_excluded.jsonl`, not
  silently dropped. This is what filters out off-topic noise (sports,
  crime stories) that has no PESTLE/Porter's relevance at all.
- **Dedup** — cosine similarity >= 0.92 within a 48h window collapses
  re-reported stories into one record with an incremented mention_count.
- **Grounding safeguards and comparative-fact matching** (`grounding.py`,
  `comparative_matching.py`) — a non-content pre-filter before any Ollama
  call, a post-decomposition grounding check rejecting fabricated numbers,
  HTML-unescaping of fetched titles, and comparative-fact matching for bare
  state-value facts. Both modules were originally written for the historical
  GDELT bulk backfill (since removed) and were retained because this live
  path depends on them. Step ORDER is fetch -> decompose -> dedup -> seed
  transfer -> gate -> write, with these checks inserted at the appropriate
  points within it.

## UI
Three-page flow (`web/index.html`, still one self-contained file with
three JS-toggled states, no page reloads or backend routing changes),
sharp corners throughout (0px radius, no exceptions), green/red
direction encoding, Space Grotesk + IBM Plex Mono. **Signature motif**:
overlapping hexagon + pentagon line art (the same two shapes as the
PESTLE/Porter's radar charts), used on the landing hero and reused at a
smaller, pulsing scale for the loading state - a deliberate recurring
signature, not a one-off illustration.
- **Theme: "Cobalt Grid"** - supersedes the original single dark
  (near-black graphite, indigo-violet accent) theme entirely; the two
  color systems were not merged. Defined as CSS custom properties, light
  as the default `:root` (bg `#EEF2FA`, surface `#FFFFFF`, cobalt accent
  `#2E4FE8`, text `#101828`/`#475069`, divider `#C7D0EA`) and dark under
  `[data-theme="dark"]` on `<html>` (bg `#0B0E1A`, surface `#161C30`,
  brightened cobalt accent `#6C8CFF` for dark-background contrast, text
  `#EAEEFA`/`#98A3C2`, divider `#2A3252`). A `#theme-toggle` button in
  the topbar switches themes and persists the choice to `localStorage`;
  light is the default for a first visit (no system-preference
  auto-detection). `--accent` (cobalt) is UI chrome only - CTAs,
  rule-line accents, the toggle icon itself - and is never used to
  encode whether a factor is helping or hurting a business; only
  `--positive`/`--negative` carry that meaning, and are themselves
  shifted (not swapped) between themes purely for contrast - a darker
  green/red pair on light surfaces, the original brighter pair on dark
  surfaces. Plotly can't resolve CSS `var()` inside a JS color string,
  so the radar charts read the current theme's resolved colors via
  `getComputedStyle` at draw time and are explicitly re-rendered on
  every theme toggle so an already-open analysis page's charts don't go
  stale after a switch.
- **Page 1 (landing)** — hero headline/subhead, the motif, a single
  "Get started" CTA, and three value-prop cards (explainable, grounded
  in real events, built for founders/investors) each with a simple line
  icon.
- **Page 2 (upload)** — CVP textarea and the optional CSV/XLSX sales
  upload on ONE page, separated by an "or add" divider, not tabbed or
  hidden. Uploading a file always shows the best-guessed date/value
  column mapping for confirmation before anything is computed — never
  submitted on a silent guess. CVP and a confirmed sales upload are each
  INDEPENDENTLY sufficient to run analysis — either one alone enables
  "Run analysis" and produces a result; providing both combines them as
  described below (sales-derived primary, CVP-similarity as the labeled
  comparison). This was tightened from an earlier version that
  unconditionally required CVP text even when a valid upload alone was
  enough — see the "Known gaps" entry on the analysis gate for the fix
  and what it required downstream. Single "Run analysis" button proceeds
  to page 3.
- **Page 4 (news data browser)** — a read-only inspection view over EVERY
  stored news item across all three corpora, reached from the topbar "..."
  menu ("Browse news data"). Backed by `GET /api/news` +
  `src/marketintel/news_browser.py`, which normalizes the three different
  record shapes (fabricated `news.json` articles, live `real_facts.json`
  facts + their parent articles) into one display shape. Summary cards give
  each corpus's count and date coverage plus an explicit `in_scoring` chip
  ("Feeds analysis"), so a corpus that is stored but NOT wired into the
  serving path can never quietly look equivalent to one that is. Filtering
  (corpus, free-text, scope, polarity, top dimension) and paging are
  server-side, so this keeps working as the live corpus grows. This module deliberately has no dependency on the scoring
  pipeline and never mutates or re-scores anything, so browsing can't
  perturb `/api/analyze`.
- **Page 3 (analysis)** — the same PESTLE hexagon / Porter's pentagon
  radar charts (Plotly) and per-dimension drill-down accordions as
  before, unchanged in underlying logic, now preceded by a result-type
  badge reading either "Derived from your sales history" or "Estimated
  from comparable businesses" depending on the backend's own
  `primary_result` field — when a sales-derived result is primary, the
  CVP estimate is still shown below as a smaller, explicitly-marked
  lower-confidence comparison, never dropped. Each article row is
  badged "LIVE" when it's a real ingested fact rather than a fabricated
  seed article - this genuinely reflects `article.is_live` from
  `server.py` (real facts ARE folded into live scoring today, see the
  "real-data seed-inference migration" entry below - confirmed by a
  Playwright test rendering real "LIVE" badges from an actual
  `/api/analyze` response, not a placeholder awaiting a future
  integration). "New analysis" returns to page 2, not page 1 - the
  brand name in the topbar returns to page 1 from anywhere.
The original Streamlit version (`app.py`) was fully replaced by this
page and no longer exists in the repo.

## Known gaps / in progress
- **The historical GDELT bulk backfill was REMOVED entirely (code, data, and
  docs), by decision, not by failure to build it.** What was deleted:
  `gdelt_bulk.py`, `gdelt_backfill.py`, `scripts/run_gdelt_backfill.py`, the
  two backfill-only maintenance scripts (`audit_grounding_retroactive.py`,
  `remediate_html_entity_corruption.py`), all `data/backfill_*` files (695
  articles / 960 facts / embeddings / checkpoint / rejection logs), the
  `BACKFILL_*` and `GDELT_BULK_BASE_URL` config entries, and the backfill
  corpus from the news-browser page. The reasoning it was abandoned on: after
  a real timing measurement the India-tier-only 2-year run was estimated at
  ~4.2 months of continuous unattended processing (World-broad was ~4.7
  years), the pilot had completed only ~24 of 672 quarter-hour files (~3.6%,
  one partial day) before stalling, a retroactive audit found ~14.6% of the
  facts it HAD collected contained a fabricated number, and none of it was
  ever wired into `server.py`'s scoring path - so it was cost without
  delivered value. **What deliberately SURVIVED, and why**: `grounding.py`
  and `comparative_matching.py` were originally written for the backfill but
  had already been consolidated into the live ingestion path (see the
  consolidation entry below), so `ingestion.py` depends on them - deleting
  them would have broken live ingestion. Their docstrings now describe them
  as retained-from-the-backfill rather than backfill-owned, and their
  validation scripts (`validate_grounding.py` 3/3,
  `validate_comparative_matching.py` 4/4) still pass. Verified after removal:
  every surviving module imports, `/api/analyze` and `/api/news` work
  (1,221 items: 1,000 seed + 221 live), and the full frontend flow passes
  with zero console errors. The deleted data was archived outside the repo
  first, since `data/` is gitignored and would otherwise have been
  unrecoverable; the code is recoverable from git history regardless.
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
- **Fixed a real, reproduced 500 in `server.py`: an empty or corrupted
  `real_facts.json`/`real_fact_embeddings.npy` crashed `/api/analyze` with
  an unhandled `JSONDecodeError`.** Diagnosed by direct reproduction rather
  than guessing: `data_loader.load_real_facts()`'s existence check
  (`.exists()`) passed on a 0-byte file, then `json.load()` on it raised
  uncaught, propagating through `live_facts.build_combined_corpus()` into
  `server.py`'s `analyze()` with no handler in between - FastAPI's default
  500. A SEPARATE, non-crashing but real correctness bug was found the same
  way: a stale/truncated `real_fact_embeddings.npy` (fewer rows than facts)
  didn't crash, but WOULD silently drop the excess facts from scoring in
  general (only avoided crashing in the specific truncation pattern tested
  because of how sub-cluster assignment happens to skip un-embedded facts
  before ever indexing into the gates array - not a guarantee for other
  kinds of corruption). Fixed by making `load_real_facts()` treat missing,
  empty, corrupted (`JSONDecodeError`/`ValueError`/`OSError`/`EOFError`),
  and length-mismatched files identically - all degrade to "no real facts
  available," matching the already-correct missing-file behavior. Verified
  by reproducing and re-testing all three (missing/empty/stale) scenarios
  directly against a live server, not just at the unit level. `/api/analyze`
  now also returns `live_facts_count` and `seed_only` so a seed-only result
  is visible to the caller rather than looking identical to a normal one.
- **Consolidated ingestion onto one set of safety guarantees rather than
  letting the live and batch pipelines diverge.** `ingestion.py` (the live
  RSS/GDELT-DOC-API path behind `ingestion_service.py`) now calls the SAME
  `grounding.py` (non-content pre-filter + post-decomposition grounding
  check) and `comparative_matching.py` (bare state-value fact resolution)
  modules originally written for the GDELT bulk backfill, plus HTML-unescapes
  fetched titles at fetch time for the same reason the bulk fetcher did. Explicitly NOT
  retiring either pipeline's orchestration in favor of the other - the two
  ORCHESTRATORS (`ingestion.py` vs. the batch backfill) stayed separate on
  purpose (different sources, and the batch pipeline's gate-before-
  decomposition reordering exists specifically for bulk-volume Ollama cost
  control, which doesn't apply to live per-item polling) - what's shared is
  the underlying SAFEGUARD logic itself, which already lived in standalone,
  source-agnostic modules rather than being embedded in either orchestrator.
  This resolves the duplication the safeguards would otherwise have created
  (grounding/comparative-matching only existing on the batch side) without
  merging two pipelines that have good, already-documented reasons to differ
  in ordering. `ingestion_service.py`'s `/health` now also reports the new
  counts (non-content rejections, ungrounded rejections, comparative match/
  unmatched counts) alongside its existing fields.
- **Sales-history upload built as an ADDITIVE second mode - CVP stays the
  required default, never replaced.** Column mapping is always a guess
  presented for confirmation (`sales_upload.guess_columns()`, by name
  first then by content), never trusted silently. Validation
  (`validate_upload()`) requires at least 90 distinct valid daily
  observations, rejects if duplicate-date rows exceed 5% of the sheet
  (aggregated by sum if within tolerance), and rejects if the observed
  date range is sparser than 50% density (too many gaps to trust a daily
  regression) - failing either falls back to CVP-only with a plain-
  language reason, never runs the regression anyway.
  **The regression mechanism was extracted, not duplicated**:
  `scripts/derive_sensitivity_profiles.py`'s lagged-ridge-regression core
  (feature-column construction, daily signal building, the ridge solve,
  dimension roll-up) now lives in `src/marketintel/sensitivity_regression.py`
  as a source-agnostic function taking any (profit series, news/fact pool)
  pair - re-verified after the extraction to produce IDENTICAL results to
  before (pooled correlation 0.849, 50/50 lag matches, unchanged). The
  fabricated offline pipeline and the new real-upload path both call the
  same functions now, rather than maintaining two copies of the math.
  **Respects the SAME per-dimension coverage gate as live ingestion**
  (`real_data_inference.assess_dimension_coverage()`) - the regression's
  feature columns are restricted to only dimensions currently trusted for
  real data (see the coverage table above), so a company's derived
  profile is never quietly backed by a dimension too thin in real news
  volume; uncovered dimensions are reported explicitly, not silently
  zeroed. **The upload<->real-news-coverage overlap is computed and
  reported explicitly** (`compute_coverage_overlap()`) using the SAME
  90-day minimum as the upload's own volume check, applied to the
  overlap window specifically - a regression can only use days where
  both signals exist at once. **Given the real corpus currently spans
  only ~2 days** (see the timing/coverage numbers elsewhere in this
  document), this overlap check will presently fail for almost any
  realistic historical sales upload, correctly falling back to CVP-only
  with an explicit message rather than running a regression on a
  degenerate window - validated directly against both the actual live
  real-fact corpus (confirms graceful, correct fallback) and a
  constructed synthetic corpus with genuine overlap (confirms the
  regression itself correctly recovers a known injected signal - lag and
  magnitude both matched by construction, R²=0.88) via
  `scripts/validate_sales_upload.py` (9/9 checks passing). A full
  Playwright-driven browser test also confirmed the upload → column-
  guess → confirm → graceful-fallback → CVP-result-rendered flow end to
  end with zero console errors.
  **Explicitly out of scope, per instructions**: uploaded sales data is
  never folded into the shared fabricated/real reference pool other
  users' CVP-similarity analysis draws on (kept in an ephemeral,
  in-process `_uploads` dict in `server.py`, never written to any shared
  file); never used to retrain `W` (a real consent/data-use decision this
  pass does not make); and only a single date column + single numeric
  metric column is supported (no multi-metric uploads).
  **TIME-BOXED demo fallback (`config.SALES_REGRESSION_NEWS_SOURCE`,
  currently `"fabricated"`)**: because the real-news corpus is presently
  too sparse for the overlap check above to ever pass (~2 days of
  coverage), a live class demo needs the regression to actually run and
  produce output today rather than always falling back to CVP-only.
  `sales_upload.derive_sales_profile()` is now the single dispatch point
  that both the intended `"real"` path and this `"fabricated"` path go
  through - a single named config flag decides which, so restoring
  production behavior once real coverage grows is a one-line change
  (flip the flag back to `"real"`), not a rewrite. Under `"fabricated"`,
  the regression runs the identical `sensitivity_regression.py` mechanism
  against the fabricated seed corpus (`news.json`/`news_embeddings.npy` -
  the same corpus `scripts/derive_sensitivity_profiles.py` already
  regresses the 50 fabricated startups against) instead of
  `real_facts.json`, using all 11 dimensions (the fabricated corpus is
  the fully-discovered taxonomy itself, so there's no thin-coverage
  dimension to gate on) and aligning the upload's most recent days onto
  the fabricated corpus's own fixed synthetic calendar window BY
  POSITION - explicitly not a claim that those articles happened on the
  same real calendar days as the uploaded revenue. **Every result
  produced this way is labeled, not just internally flagged**: the
  regression's own `news_source` field ("real" or "fabricated") flows
  through `server.py`'s `/api/sales/confirm` and `/api/analyze` responses
  into `web/index.html`, which renders a full-width, solid amber
  `#sample-data-banner` directly under the analysis page's headline
  whenever `news_source === "fabricated"` (not a tooltip, not fine
  print), plus a distinct amber `.result-type-badge.demo` treatment
  instead of the green "sales" badge (which would otherwise visually
  read as higher-confidence, own-data-derived) and an explicit note in
  both the confirm-mapping message and the result meta text. The CVP-only
  path and the honest thin-real-data fallback (still exercised end to
  end by `scripts/validate_sales_upload.py`, unaffected by this default,
  re-verified 9/9 passing after this change) are both fully intact -
  this flag only changes which news pool a successfully-validated
  sales-derived regression draws on, nothing about when the regression is
  attempted or how CVP-only/real-data-thin fallback is reported.
- **Fixed: the analysis gate required BOTH a non-empty CVP and (optionally)
  a confirmed sales upload, when CVP and a confirmed upload were each meant
  to be independently sufficient on their own** - a valid upload with an
  empty CVP field was rejected with "Paste a CVP first" instead of running
  the sales-derived regression it already had everything it needed for.
  `/api/analyze`'s gate (`server.py`) now requires only `cvp.strip()` OR a
  confirmed upload with a successfully-derived profile - either alone
  passes; matched in `web/index.html`'s "Run analysis" click handler so the
  frontend never blocks a request the backend would accept. **Traced what
  happens downstream with only a confirmed upload and no CVP text**: the
  sales-derived regression itself was already source-agnostic and ran
  correctly, but `embed_text("")` does NOT crash or error - it returns a
  real, normalized 384-dim vector like any other text - so the CVP-
  similarity scoring path would have silently run on a semantically
  meaningless embedding and presented it as a genuine "Estimate based on
  comparable businesses" result (identical for every user who left CVP
  blank). Fixed by adding an explicit `cvp_provided` flag to the response:
  `/api/analyze` now skips `embed_text`/`score_submission` entirely when
  CVP is empty, returning zeroed CVP display values and a real-labels-but-
  no-clusters breakdown (`_blank_breakdown`) instead of a fabricated result;
  the frontend hides the CVP-similarity breakdown section (with an explicit
  "No CVP was provided" note in its place) and the CVP-comparison block
  whenever `cvp_provided` is false, rather than rendering either against
  that meaningless embedding. **Confirmed BOTH-provided behavior is
  unchanged** (checked directly before touching anything, per instructions):
  sales-derived still wins as `primary_result`, the CVP-similarity result
  still renders as the labeled lower-confidence comparison alongside it,
  and the CVP breakdown section still shows (since a real CVP was scored)
  - none of this combination logic needed to change. Verified via
  Playwright against all three input combinations (CVP-only, upload-only
  with empty CVP - the exact reported scenario, and both together), plus a
  direct `/api/analyze` call confirming a 400 with neither input present -
  zero console errors, zero regressions in the CVP-only or both-provided
  paths.
- **`ingestion_service.py` re-confirmed to already be its own standalone,
  continuous, periodic microservice** (own process, own port 8502, fires an
  ingestion pass on startup then every 30 minutes via a plain `asyncio`
  loop, `GET /health`, atomic writes throughout) - this was already true
  before this round of changes; verified rather than assumed. Its
  independence from `server.py` was proven empirically, not just asserted:
  (a) ingestion running, `server.py` stopped and restarted - works cleanly;
  (b) `server.py` running, ingestion stopped - keeps serving (seed-only or
  with whatever real facts already exist on disk) without error; (c) both
  started independently, in either order - no crash, no dependency on
  startup sequence. All three run against real, separately-launched uvicorn
  processes on distinct ports, not simulated.
- **Startup separation formalized and re-verified after the demo-mode and
  CVP-gate changes.** No new independence LOGIC was needed - the two
  processes already had zero cross-imports (checked directly: neither file
  imports the other, and `SALES_REGRESSION_NEWS_SOURCE` is read only by
  `sales_upload.py`/`server.py`, never by `ingestion.py` or
  `ingestion_service.py`), and a distinct ingestion start command
  (`uvicorn ingestion_service:app --port 8502`) already existed in both the
  module docstring and README. What was actually missing was DISCOVERABILITY:
  the two commands lived in unrelated README sections, and the analysis
  engine's was port-implicit (`uvicorn server:app --reload`). Fixed by making
  both commands symmetric and port-explicit (`--port 8000` / `--port 8502`)
  in the docstrings, and adding a single README "Running the services"
  section covering start-only-analysis / start-only-ingestion / start-both,
  with a comparison table and an explicit "each is safe without the other."
  Deliberately did NOT add shell/PowerShell wrapper scripts - the repo has no
  such convention anywhere, and a wrapper that only execs a one-line uvicorn
  command would add a cross-platform maintenance surface for no functional
  gain. Independence re-proven (not assumed to still hold) against real
  separately-launched processes now that the demo-mode toggle and CVP/upload
  gate exist: (a) analysis up, ingestion never started - `/` , `/api/analyze`,
  AND the full sales-upload→confirm→analyze chain with an EMPTY CVP all work
  (`news_source=fabricated`, `primary_result=sales`, `cvp_provided=false`);
  (b) ingestion up, analysis stopped then restarted underneath it - ingestion
  kept serving `/health` throughout, analysis restarted clean; (c) both
  stopped, then started ingestion-first and analysis-first - no crash either
  way. Zero tracebacks across every scenario's process log.
- **Migrated seed-based inference off fabricated data onto the accumulated
  real-fact corpus, per dimension - audited and coverage-checked first,
  not switched wholesale.** Audit found `seed_inference.py`'s functions
  already take their reference pool as an explicit parameter (no internal
  hardcoded fabricated-data dependency) - so the migration only needed to
  change WHAT `ingestion.py` passes in, not `seed_inference.py` itself,
  meaning the batch backfill's call sites (left untouched at the time, and
  since removed entirely) were unaffected. Also confirmed `startups.json`/
  `startup_embeddings.npy` are read at runtime NOWHERE (only by offline
  training scripts) - nothing to migrate there. `server.py`'s own
  `load_news()` call is NOT a seed-inference lookup - it's the primary
  scored corpus itself (combined with real facts and gated via `W` on
  every `/api/analyze` call) - migrating that would mean fabricated news
  stops being scored entirely, a fundamentally bigger change in the same
  spirit as retraining `W`; explicitly out of scope, flagged rather than
  left ambiguous.
  **Coverage check** (`real_data_inference.py`): of the 11 PESTLE/Porter's
  dimensions, only 4 (political, economic, technological,
  competitive_rivalry) currently have enough real facts (≥15 scoring above
  the sub-cluster relevance threshold, with ≥3 of EACH polarity among
  them) to support a reliable k-NN lookup. The other 7 - notably
  "environmental", which had ZERO positive real examples at check time,
  meaning any new environmental-topic fact could never be inferred
  positive no matter what it said - keep falling back to the fabricated
  corpus, dimension by dimension, not silently. All 7 geographic scope
  classes DO have real coverage (even the thinnest, Jalandhar/Phagwara at
  2 each) - scope's per-class-BEST-match mechanism only needs one good
  exemplar per class to work correctly, unlike the pooled k-NN voting
  relevance/polarity use, so its bar is much lower and it migrates for
  every class today.
  **Migration mechanism** (`infer_hybrid`/`infer_scope_hybrid`): for each
  new fact, BOTH pools (real and fabricated) are queried independently;
  each of the 11 relevance dimensions takes its value from whichever pool
  passed coverage for that specific dimension - a real per-dimension
  blend, not one pool winning the whole fact. Polarity (a single field,
  not splittable per dimension) is drawn from whichever pool covers the
  fact's own dominant (highest-relevance) dimension. The relevance GATE
  THRESHOLD recalibrates to the real corpus's own distribution once there
  are enough facts (≥50, currently cleared at 133) for a 5th-percentile
  estimate to be stable - below that it stays fabricated-calibrated, same
  as before. Coverage is re-checked fresh on every ingestion run, so a
  dimension is expected to graduate from fabricated to real as more real
  data accumulates, with no code change needed. Each stored fact now
  carries `inference_source`/`scope_source` fields recording exactly which
  pool it drew from, for spot-checking.
- **Sub-cluster structure still depends on the fabricated corpus - flagged,
  not migrated, per instructions.** `discover_subclusters.py`'s taxonomy
  (dimension → sub-cluster labels/assignments) is built once, offline,
  from the fabricated corpus only; `live_facts.py::compute_subcluster_centroids()`
  reads `news.json`/`news_embeddings.npy` fresh at server startup to place
  new real facts into those existing, fabricated-defined clusters (a real
  runtime dependency on fabricated data, distinct from both the
  seed-inference case above and the frozen-`W` case). Two options, neither
  chosen here: (a) leave as-is - stable cluster IDs/labels, but the
  taxonomy's shape and its labels' vocabulary reflect only the fabricated
  corpus's narrative patterns, and a real-world topic with no good
  fabricated analog gets force-fit into the nearest existing cluster
  regardless of fit; (b) periodically re-run discovery against the
  accumulated real corpus (or a combined pool) - would let the taxonomy
  reflect real-world topic distribution over time, but re-clustering
  changes cluster IDs/labels (breaking continuity with existing fact
  assignments) and hits the exact same per-dimension thinness problem
  found above (the 7 fabricated-only dimensions almost certainly don't
  have enough real volume yet to support meaningful re-clustering either).
  This is a separate decision from the seed-inference migration above -
  not resolved here.
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
- **A real bug in comparative-fact matching's entity check was caught by its
  own validation script before touching any real data**: the first
  implementation accepted any non-empty entity-set intersection as a match,
  which let two facts about genuinely different subjects (mobile-phone GST
  vs. textile GST) cross-match anyway, purely because both happened to also
  mention "India" — confirmed failing even at similarity=1.0 in a synthetic
  worst-case test. Fixed by requiring Jaccard similarity >= 0.5 across entity
  sets rather than any overlap; re-validated at 4/4 (3 real rate/tax changes
  correctly matched with the right direction, plus the cross-match rejection,
  including the synthetic worst case).
- **Fact-decomposition schema compliance degraded when the prompt grew a
  nested JSON schema** (facts now carry entities, for comparative matching) —
  measured directly at ~7% malformed-JSON calls in a real GDELT smoke test (llama3.2:3b returning a bare string where an object was
  expected, or an object missing "text"). Fixed by lowering Ollama's request
  temperature to 0.2 (re-tested at 6/6 well-formed responses on a fresh
  sample). This fixes STRUCTURAL compliance only — a side-by-side test at the
  lower temperature found the model hallucinate MORE confidently on a
  genuinely content-free title (fabricating a tournament venue and edition
  number from a title that was just "Preview, Prop Picks, Best Bets"), where
  at default temperature it had correctly returned an empty array for the
  same title. Low temperature buys schema compliance, not truthfulness.
- **Two new, real fact-decomposition quality issues surfaced during pilot
  spot-checking**, beyond the hallucination already documented above:
  (1) a worse hallucination than previously recorded — the headline
  "COMMUNITY CALENDAR" (a section label, not news) produced a fully
  fabricated claim: "The Punjab government has slashed the GST on mobile
  phones from 18% to 8%," with nothing in the source justifying it;
  (2) an over-splitting error — "KOZYNAP Accelerates Retail Expansion with
  Fully Customized Sleep Solutions" (one coherent claim) was split into two
  facts, the second an incoherent fragment ("with Fully Customized Sleep
  Solutions"). Fact-decomposition over-splitting is NOT fixed (see the
  fragment-relevance finding below); the hallucination has since had a
  safeguard built and validated (below) - it's the reason the pilot's
  spot-check gate isn't being called satisfied yet.
- **Grounding safeguards built against fact hallucination, validated against
  both known real failure cases, and a MUCH larger problem found in the
  process.** Two layers (`src/marketintel/grounding.py`), used only by the
  GDELT backfill, and retained for live ingestion when that was removed:
  (1) a pre-filter before any Ollama call, rejecting obvious
  non-content titles (section labels, digests, horoscopes, etc.) via a
  small keyword list plus a "very short / all-caps / no verb / no numbers"
  heuristic; (2) a post-decomposition grounding check, rejecting any fact
  that states a number (percentage, currency amount, date) not traceable
  verbatim-or-near-verbatim to the source title - independent of Ollama's
  temperature, since temperature was already shown not to fix truthfulness.
  Validated (`scripts/validate_grounding.py`, 3/3 pass) against both known
  hallucinations (COMMUNITY CALENDAR's fake GST claim; the BMW-preview
  title's fabricated tournament edition number) - each caught by at least
  one layer - and confirmed NOT to false-positive on a genuine, correctly-
  grounded real fact from the pilot.
  **Retroactively auditing the pilot's already-collected data (interim -
  day 1 of 7 processed so far, 969 facts) found this is a much bigger
  problem than the isolated cases suggested: ~17.9% of ALL currently-stored
  facts (173/969) contain at least one fabricated number.** The failure
  pattern is more concerning than random noise: titles with real, legitimate
  content but nothing to do with economic policy - a movie review
  ("'Eagles of the Republic' review..."), an obituary, a rhetorical opinion
  piece ("Who Speaks For The River?") - produced SPECIFIC, plausible-
  sounding claims (an RBI repo rate cut to 6.25%, a GST change from 18% to
  12%, a named date) that read like genuine real-world facts because they
  likely ARE facts the model memorized during training - just not ones
  stated anywhere in that source. This is closer to unprompted parametric-
  knowledge injection than nonsense generation, which is exactly why
  lowering temperature didn't help and why the grounding check (verifying
  against the source, not trusting the model to behave) is the right
  mitigation. Per instructions, the pilot's original run was left to finish
  undisturbed (not restarted) and this audit is retroactive
  (`scripts/audit_grounding_retroactive.py`); the safeguards above are
  wired into the live ingestion path, which is where they remain in use. The pilot's spot-check gate is NOT yet being called
  satisfied - the full week needs to finish and this audit needs to be
  re-run against the complete corpus first.
- **The grounding check's own known limitation (a substring match doesn't
  verify a number's context/unit/subject matches the source) produced ONE
  confirmed false accept, found by sampling ACCEPTED facts specifically for
  this pattern, and it was a real, fixable bug, not just a theoretical
  risk.** A fact claiming "the Punjab government has increased the water
  supply to farmers by 20%" was accepted as "grounded" against a source
  title that was just a generic magazine masthead ("The Week Magazine —
  Latest News, Politics, Business & Opinion Updates") — completely
  unrelated. Root cause: GDELT's crawler stores titles with HTML entities
  UNDECODED (e.g. "&#x2013;" for the em-dash literally present as that
  6-character string, not a real dash), and that entity code's digits
  ("2013") coincidentally contain "20" as a substring, which the
  (then-unescaped) grounding check accepted as a match for the fact's "20%".
  Confirmed this affects 39/700 (5.6%) of titles collected so far - not a
  one-off. **Fixed at the source**: `gdelt_bulk.py`'s title extraction now
  HTML-unescapes before returning (fixes this and any future entity-corrupted
  title for every downstream consumer, not just grounding), and
  `grounding.py` also unescapes defensively (so it gives correct answers on
  already-collected data that still has raw entities). Re-validated: the
  specific case now correctly rejects; `scripts/validate_grounding.py` still
  3/3; re-sampling 20 fresh accepted facts post-fix found zero additional
  coincidental matches (every one traced to a genuinely same-context,
  same-subject number in its source) - though this is a sample, not proof
  none remain elsewhere in the corpus.
- **Two real false-rejection bugs in the grounding check, found by porting it
  to the live ingestion path and spot-checking its output there.** (1) The
  number regex treated a sentence-ending period as part of a decimal number
  ("...at the age of 34." extracted as "34.", not "34"), so a fact correctly
  quoting a headline's own figure could fail to match a source with no
  trailing punctuation at that position. (2) `is_grounded` compared the
  fact's comma-stripped number against the RAW, unnormalized source text, so
  a source formatted with a thousands-separator ("5,000 migrants") could
  never match the fact's normalized "5000" as a substring. Both fixed: the
  number regex only consumes a decimal point when followed by a digit, and
  the source is now compared via its OWN extracted-and-normalized numbers
  rather than a raw substring search. Re-validated: `validate_grounding.py`
  still 3/3; re-checking all 47 facts rejected in one live ingestion run
  found 4 were false rejections now correctly accepted (recovered into
  `real_facts.json`, flagged with a `recovery_note` field since their
  entities weren't preserved in the older ungrounded-log format); re-running
  the retroactive audit against the full corpus at the time dropped the
  rejection rate from 173/960 (18.0%) to 140/960 (14.6%) - the corrected,
  more accurate figure, not a sign the underlying hallucination problem was
  smaller than reported. The ungrounded-rejection log (both pipelines) now
  also records each rejected fact's entities, so a future correction like
  this can recover facts without re-running extraction.
- **The over-splitting fragment does NOT reliably fail the relevance gate -
  in one measured case, the opposite happened.** For "KOZYNAP Accelerates
  Retail Expansion with Fully Customized Sleep Solutions" split into two
  facts, the meaningless fragment ("with Fully Customized Sleep Solutions")
  scored max_relevance=0.60 (would PASS the 0.585 gate) while the coherent,
  legitimate half ("KOZYNAP Accelerates Retail Expansion") scored only 0.48
  (would FAIL it). This is also moot for the current architecture regardless
  of relevance score, in any pipeline that gates once per TITLE before
  decomposition with no second gate after it - every fact from a title that
  clears the gate gets stored regardless of that individual fact's own
  relevance. Flagged per instructions rather than
  dismissed; not yet acted on.

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
- **`config.SALES_REGRESSION_NEWS_SOURCE` is currently `"fabricated"`, a
  time-boxed demo override, not the intended production setting.** Flip
  it back to `"real"` once the real-news corpus's coverage grows enough
  to demo meaningfully (see the sales-upload entry above for the full
  reasoning and how the flag is dispatched) - revisit after the next
  real-coverage check.
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
- Whether the fact-decomposition over-splitting issue (see "Known gaps"
  above) needs its own mitigation is undecided — the hallucination half of
  this concern now has a validated safeguard (grounding.py), but
  over-splitting a coherent claim into a fragment is a separate problem the
  grounding check doesn't address.