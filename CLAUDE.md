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

### 3. Historical GDELT bulk backfill (`gdelt_bulk.py`, `gdelt_backfill.py`)
A separate, one-off/batch collection process from `ingestion_service.py`
above, which keeps running independently on its own 30-minute schedule for
ongoing Punjab/LPU-area coverage. Writes to its own files
(`data/backfill_articles.json` / `backfill_facts.json` /
`backfill_fact_embeddings.npy`) so the two processes never contend over the
same files. Not yet merged into `server.py`'s live scoring path (tracked
separately) — see "Known gaps" below for status, the timing investigation
that shaped its scope, and the quality findings from its pilot run.
- **Source**: GDELT 2.0 bulk export files (`data.gdeltproject.org`), not the
  DOC 2.0 API (~3 months lookback only) or RSS (no history at all) — the only
  free, no-key source with multi-year depth. Of the three bulk file types
  (Events, Mentions, GKG), only GKG is used: Events/Mentions are pure
  structured/coded data (CAMEO codes, actor codes) with no article text
  anywhere. GKG's `Extras` column carries a real, crawler-extracted
  `<PAGE_TITLE>` tag — confirmed present in 99.9% of records across three
  sample dates (today, 2024, 2022) by direct inspection — with a URL-slug
  fallback for the rare record missing it.
- **Reordered pipeline, distinct from the live per-item order**: fetch (GDELT
  bulk, tier-filtered) -> embed -> relevance gate -> only then fact
  decomposition (Ollama) on survivors -> dedup -> seed inference
  (relevance/polarity/scope) -> comparative-fact matching -> atomic write.
  The gate runs BEFORE decomposition here specifically to bound the dominant
  Ollama cost to only the records that clear it, unlike the live pipeline.
- **Comparative-fact matching** (`comparative_matching.py`) — for a bare
  state-value fact with no directional language of its own (e.g. "GST on
  mobile phones is 18%"), finds the nearest STRICTLY-EARLIER fact about the
  same specific subject and computes a direction (increase/decrease), rather
  than leaving polarity ambiguous. A fact that already states its own
  direction ("raised from 12% to 18%") skips the lookup entirely — this is
  why `fact_extraction.py`'s prompt was changed to preserve directional
  language as factual content rather than neutralizing it away. A candidate
  match must clear both a similarity threshold (0.85) and an entity-overlap
  check — see "Known gaps" below for a real bug this caught before it ever
  touched backfill data.
- **Checkpointed and resumable** at the granularity of one 15-minute GKG file
  (`data/backfill_state.json`), since even the scoped-down India-tier run is
  measured in months, not hours — an interruption loses at most the window
  since the last checkpoint, never the whole run.

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
- **GDELT bulk backfill: timing estimate forced a scope-down, and a pilot is
  in progress.** A real timing pilot (8 GKG files sampled across one day,
  measured end-to-end through embed -> gate -> Ollama decomposition, then
  extrapolated) found the full 2-year World(broad, unfiltered)+India backfill
  would take **~4.7 years** of continuous unattended processing — dominated
  almost entirely by Ollama fact decomposition (mean 3.35s/call measured
  directly, ~50% of records clearing the relevance gate, ~86.7M raw records
  over 2 years at World-broad scale). This was reported explicitly rather
  than started blindly, per instructions. Decided (user's choice, among
  India-only/no-Ollama/narrower-window options presented): **India-tier
  only, keep Ollama decomposition** — estimated ~4.2 months, still long but
  plausible with the checkpointing above. World-broad and Punjab-level
  extension remain future work, not started.
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
  measured directly at ~7% malformed-JSON calls in a real GDELT backfill
  smoke test (llama3.2:3b returning a bare string where an object was
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
  GDELT backfill: (1) a pre-filter before any Ollama call, rejecting obvious
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
  wired into `gdelt_backfill.py` for the full-scale run once the pilot
  clears its gate. The pilot's spot-check gate is NOT yet being called
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
- **The over-splitting fragment does NOT reliably fail the relevance gate -
  in one measured case, the opposite happened.** For "KOZYNAP Accelerates
  Retail Expansion with Fully Customized Sleep Solutions" split into two
  facts, the meaningless fragment ("with Fully Customized Sleep Solutions")
  scored max_relevance=0.60 (would PASS the 0.585 gate) while the coherent,
  legitimate half ("KOZYNAP Accelerates Retail Expansion") scored only 0.48
  (would FAIL it). This is also moot for the current architecture regardless
  of relevance score: the batch backfill pipeline's relevance gate runs once
  per TITLE, before decomposition, with no second gate after it - so every
  fact from a title that clears the gate gets stored regardless of that
  individual fact's own relevance. Flagged per instructions rather than
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
- GDELT bulk backfill scale: World-broad coverage and the Punjab-level
  extension (via GDELT's sub-national geo-tagging) are both deferred until
  after the India-tier pilot week is spot-checked and, separately, the
  India-tier full 2-year run (~4.2 months estimated) is actually kicked off
  — neither started yet. Revisit whether World-broad is worth pursuing at
  all (even without Ollama decomposition, ~27 days estimated) once India-tier
  results are in hand.
- Whether the fact-decomposition over-splitting issue (see "Known gaps"
  above) needs its own mitigation is undecided — the hallucination half of
  this concern now has a validated safeguard (grounding.py), but
  over-splitting a coherent claim into a fragment is a separate problem the
  grounding check doesn't address.
- **Pilot week's spot-check gate is NOT yet satisfied.** Blocking on: the
  full 7-day India-tier pilot run finishing (in progress, checkpointed/
  resumable, day 1 of 7 done as of the interim audits above), then
  re-running `scripts/audit_grounding_retroactive.py` against the complete
  resulting corpus — spot-checking both a sample of what it rejects
  (confirming genuinely bad, not false positives) AND a sample of what it
  accepts (confirming no coincidental bare-number matches slipped through -
  already done once on interim data, finding and fixing one real bug; needs
  redoing against the complete week). Do not start the full India-tier
  backfill (~4.2 months) until this is done and reported.