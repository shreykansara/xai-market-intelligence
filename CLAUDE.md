# AI-Powered Explainable Market Scanning

## Problem
Founders and investors currently rely on manual market scanning to
understand how real-world events affect a business, with no systematic or
traceable way to connect a specific happening to a specific company's
outcome. Early-stage startups make this worse — they have no sales history
of their own to learn from.

## Core architecture (current understanding)
1. **Absolute embedding layer** — events are embedded via a local
   sentence-transformers model (all-MiniLM-L6-v2 to start).
2. **Soft, multi-dimensional relevance** — events don't get a single
   category. Each one carries independent 0-1 relevance scores across the
   6 PESTLE dimensions and the 5 Porter's Five Forces dimensions, so a
   single event can matter to several dimensions at once (e.g. a tariff
   event scoring high on both political and economic).
3. **Company-relative effect** — the eventual goal is a trained joint
   model (event embedding + business-positioning embedding -> effect).
   The current MVP phase stands in for that with a similarity-and-blend
   approach instead: a submitted CVP is embedded, compared against a set
   of reference companies, and the top 3 most similar companies' known
   sensitivity profiles are blended to produce the result.
4. **Explainability** — every score traces back to the specific news
   events that justified it, not just a number.

## Use cases
1. **Startup founders** — identify which factors affect their product, to
   shape branding and go-to-market strategy.
2. **Investors** — gauge how risky a given market/category is before
   deciding whether to invest.

## Current phase: MVP prototype (fabricated data, no real training yet)
Built via Claude Code in VS Code. Stack: Streamlit + Plotly (Scatterpolar
for the radar charts).

- **Fabricated news dataset** — 1000 articles across the last 6 months.
  Each has a title, date, body text, geographic scope (LPU, Phagwara,
  Jalandhar, Kapurthala, Punjab, India, or World), polarity, a 6-value
  PESTLE relevance vector, an 5-value Porter's relevance vector, and an
  embedding.
- **Fabricated startup dataset** — 20 LPU-based tech startups, diverse
  domains. Each has a CVP, a ground-truth PESTLE sensitivity vector, a
  ground-truth Porter's sensitivity vector, and 3-5 linked news articles
  that justify the profile.
- **Interface** — a single page: the user pastes their CVP and submits.
  Location is fixed to LPU; suppliers/consumers/segment are not collected
  separately, they're implicit in the CVP.
- **Analysis** — embed the submitted CVP, find the top 3 most similar
  fabricated startups by CVP embedding similarity, and blend their
  PESTLE/Porter's vectors (similarity-weighted) into the final scores.
- **Output** — two radar/spider charts: a hexagon (6-axis PESTLE) and a
  pentagon (5-axis Porter's Five Forces), plus the top contributing
  events per dimension underneath.

### Explicitly out of scope for this phase
- CSV/XLSX upload and column mapping (next phase).
- Any stakeholder/supplier/competitor confirmation screen.
- Real news ingestion — still using the fabricated dataset.
- Geographic-scope-based weighting in the scoring logic — the field is
  stored but not yet used.
- The fully trained joint event-business model — the top-3 blend above is
  a deliberate stand-in for it.

## Future direction (beyond the current MVP)
1. CSV/XLSX upload with column mapping to known variables.
2. A real news ingestion pipeline, replacing the fabricated dataset.
3. Train the real joint event-business model on real historical
   (event, company, sales) data, replacing the fabricated-startup blend.
4. Backtest the trained model against known historical cases before
   trusting it.
5. Pilot with the LPU incubation centre using real startups.
6. Dashboard for founders/investors.
7. Real-time alerts and a subscription tier for external companies and
   investors.

## Competitive landscape (context, not exhaustive)
- Institutional alt-data / event-driven investing (RavenPack-style,
  AlphaSense, Exabel, YipitData) — mature, built for public companies
  with liquid data.
- Startup due-diligence AI (CB Insights, similar tools) — explainable
  scoring exists but is focused on internal signals (team, financials,
  patents), not macro/event exposure.
- Generic PESTLE-generator tools — static, one-shot, no real-time events
  or company-specific history.
- The identified gap: explainable, event-driven exposure modeling
  transferred to pre-revenue startups via positioning. A US patent from
  2005/2006 on predicting business impact from classified news events is
  known adjacent prior art worth reviewing before going further.

## Open technical decisions
- Staying with local sentence-transformers for now; revisit fine-tuning
  once real training data exists.
- How to source real historical (event, company, sales) training data
  once moving past the fabricated MVP.
- Model architecture for the eventual real joint event-business
  interaction (two-tower vs. cross-attention).