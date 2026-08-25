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
   healthtech. Each has a CVP, a ground-truth signed sensitivity profile
   (-100 to 100 per PESTLE/Porter's dimension), and 3-5 linked news article
   IDs that justify that profile. CVPs are embedded with the same model.
3. **Analysis** — the submitted CVP is embedded and compared via cosine
   similarity against all 20 startup embeddings. The top 3 most similar
   startups' PESTLE and Porter's vectors are blended (similarity-weighted
   average) to produce the final scores, and their linked articles are
   ranked by which dimension they contribute most to.
4. **Output** — two Plotly radar charts (direction shown by color: green =
   helping, red = hurting) plus a ranked list of the news events driving each
   score, so every number stays traceable back to a real, inspectable
   fabricated article.

## Project structure

```
app.py                       Streamlit UI — the whole frontend
src/marketintel/
  config.py                  Dimension names, scopes, file paths, constants
  embeddings.py               sentence-transformers wrapper
  data_loader.py               Loads generated news/startup data + embeddings
  analysis.py                 Similarity, blending, and explainability ranking
scripts/
  generate_news.py            Builds data/news.json + news_embeddings.npy
  generate_startups.py        Builds data/startups.json + startup_embeddings.npy
data/                         Generated datasets (gitignored, see below)
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
python scripts/generate_news.py       # must run first
python scripts/generate_startups.py   # depends on news.json
```

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

See `CLAUDE.md` for the full project context and longer-term roadmap.
