# Explainable Market Intelligence

Founders and investors currently rely on manual market scanning to understand
how real-world events affect a business, with no systematic or traceable way
to connect a specific happening to a specific company's outcome. Early-stage
startups make this worse — they have no sales history of their own to learn
from.

This is a working prototype: paste a business CVP / description and get back
two radar charts — a **hexagon for PESTLE** and a **pentagon for Porter's Five
Forces** — showing how sensitive the business is on each dimension, with the
specific fabricated news events behind each score visible underneath.

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
3. **Fabricated profit history → derived sensitivity profile** — each
   startup also gets a hidden PESTLE/Porter's sensitivity template and a
   hidden shock lag (`scripts/hidden_ground_truth.py`), domain-consistent
   by design (e.g. an import-dependent hardware startup gets high hidden
   political/economic sensitivity) but **never exposed to the learning
   pipeline** — only used to fabricate a daily profit/revenue series
   (`data/profit_history.json`, 180 days: baseline trend + noise + shocks
   injected some days later whenever a relevant, hidden-sensitive news
   article runs). `scripts/derive_sensitivity_profiles.py` then recovers
   each startup's sensitivity profile purely from that profit series: for
   a handful of candidate lag windows (1/3/7/14 days) it regresses daily
   profit changes against the preceding day's news relevance (weighted by
   polarity), keeps the lag with the best fit (highest R²), and rescales
   that fit's 11 coefficients into the startup's derived profile. It then
   validates the recovery by correlating each derived profile against its
   hidden template — a sanity check on the recovery pipeline itself,
   printed before training ever touches the shared matrix. In practice
   this recovers the true shock lag for all 20 startups and correlates at
   ~0.93 with the hidden templates.
4. **Interaction matrix** (`data/interaction_matrix.npy`) — a single shared
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
5. **Analysis** — for a submitted CVP, every one of the 1000 news articles
   gets a `gate` from `W`, which combines with that article's own labeled
   relevance and polarity to give its signed contribution to each PESTLE/
   Porter's dimension. Summing contributions per dimension across all 1000
   articles gives the raw score for that dimension; each chart's 6 or 5
   raw scores are then independently rescaled so the largest magnitude
   hits 100, sign preserved. A dimension whose raw magnitude is under 10%
   of the submission's strongest dimension is treated as negligible rather
   than styled helping/hurting.
6. **Output** — two Plotly radar charts (green = helping, red = hurting,
   grey = negligible) plus a ranked list of the news articles with the
   largest |contribution| per dimension, so every number stays traceable
   back to a real, inspectable fabricated article.

## Project structure

```
app.py                             Streamlit UI — the whole frontend
src/marketintel/
  config.py                        Dimension names, scopes, file paths, constants
  embeddings.py                    sentence-transformers wrapper
  data_loader.py                   Loads generated news/startup data + W
  analysis.py                      Gate/contribution scoring and explainability ranking
scripts/
  generate_news.py                 Builds data/news.json + news_embeddings.npy
  generate_startups.py             Builds data/startups.json (identity only) + embeddings
  hidden_ground_truth.py           Hidden per-startup templates + shock lags — NOT used at
                                    inference; only by the two scripts below
  simulate_profit_history.py       Builds data/profit_history.json using the hidden templates
  derive_sensitivity_profiles.py   Recovers each startup's real profile via lag regression,
                                    validates it against the hidden templates, writes it into
                                    data/startups.json
  train_interaction_matrix.py      Fits data/interaction_matrix.npy (W) from the derived profiles
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
python scripts/simulate_profit_history.py        # depends on both
python scripts/derive_sensitivity_profiles.py    # recovers + validates the profiles
python scripts/train_interaction_matrix.py       # fits W on the derived profiles
```

`derive_sensitivity_profiles.py` prints a validation report — per-startup
recovered vs. true shock lag, and the correlation between each derived
profile and its hidden generation template. Check that report before
re-running the last step; a `W` trained on a broken recovery isn't worth much.

## Start the server

```bash
streamlit run app.py
```

This opens the app at `http://localhost:8501`. Paste a CVP into the text
area and click **Analyze**.

## Current scope

This phase is intentionally limited to what's described above:

- No CSV/XLSX upload — next phase.
- No stakeholder/supplier/competitor confirmation screen.
- News is fabricated, not real ingestion.
- Geographic scope is stored per article but doesn't yet weight the scoring.
- `W` is trained once in batch on the fabricated startups, not updated
  online from real observed outcomes — there aren't any yet.

See `CLAUDE.md` for the full project context and longer-term roadmap.
