"""Bundled fact decomposition + classification: ONE Groq call per source text
returns atomic facts (text, entities) AND their PESTLE/Porter's scores +
polarity together, instead of the two separate calls
fact_extraction.extract_facts_detailed() + lpu_classification.classify_facts()
previously made.

Why bundle: with no seed corpus left (news.json/real_facts.json both deleted),
there is no nearest-neighbour reference pool for seed_inference.py-style k-NN
classification - scores have to come from the model directly, the same
conclusion lpu_classification.py already reached. Splitting that into a
decomposition call and a separate classification call doubles Groq usage for
no accuracy benefit, since the model is perfectly capable of returning both in
one structured response. This module is the answer to "resolve the
classification mechanism explicitly": it is now the ONE mechanism, used
identically for every historical source (LPU today; GDELT once its scope is
defined) - there is no separate, LPU-only classification path any more.

Grounding is layered on TOP of this, unchanged: is_likely_non_content() is a
pre-filter before any call, and is_grounded() is a post-decomposition check
per fact against the real source text - both reused verbatim from
grounding.py, which fact_extraction.py's live-ingestion siblings already use.
This module doesn't duplicate that logic; callers (lpu_ingestion.py) apply it
around this module's output, the same layering ingestion.py already has.
"""
import json
import re
import time
import urllib.error

from .config import (
    GROQ_MAX_ATTEMPTS,
    OLLAMA_RETRY_BACKOFF_SECONDS,
    OLLAMA_RETRY_SHRINK_FACTOR,
    PESTLE_DIMS,
    PORTERS_DIMS,
)
from .groq_client import GroqError, GroqRateLimited, call_groq

BUNDLED_PROMPT = """You are analyzing a real-world text for a business/market intelligence system.

## Step 1: Extract atomic facts
Identify each DISTINCT factual claim in the text that could be scored independently. A different number, a different direction of change, or a different affected party each count as a separate claim.
Rewrite each claim in neutral, plain language: strip loaded framing, opinion, and rhetorical language (e.g. "disastrous", "critics say", "long-overdue") - but KEEP every specific: numbers, thresholds, dates, and named parties must be preserved exactly as given.
Directional/comparative language ("raised", "cut", "increased", "decreased", "from X to Y") is factual content to KEEP, not rhetorical framing to strip - only remove it if the source genuinely never states a direction.
If the text only contains one claim, return just that one claim, neutrally rewritten.

## Step 2: For EACH extracted claim, also provide:
- entities: the specific named entities it's about (people, organizations, places, specifically-named policies/products/programs), using the same names as your neutral rewrite.
- A relevance score from 0.0 to 1.0 for EACH of these 11 dimensions:

PESTLE:
- political: government, regulation, policy, public administration
- economic: funding, costs, prices, jobs, trade, economic conditions
- social: people, culture, demographics, education, community
- technological: technology, research, innovation, digital systems, engineering
- legal: law, compliance, contracts, rules, formal legal process
- environmental: climate, sustainability, energy, pollution, physical environment

Porter's Five Forces:
- threat_new_entrants: new competitors/players entering a market or field
- supplier_power: suppliers, vendors, input providers and their leverage
- buyer_power: customers, clients and their leverage
- threat_substitutes: alternative options replacing an existing offering
- competitive_rivalry: competition between existing players, rankings, contests

- polarity: exactly "positive" or "negative" - does this read as a favourable/opportunity-creating development, or an unfavourable/restrictive/problematic one? If genuinely neutral, choose based on the closest fit.

## Rules
- MOST routine/administrative text (schedules, procedural notices, circulars) has NO market relevance: score it at or near 0.0 on every dimension. Do not invent relevance that isn't there.
- Only give a score above 0.5 when the claim genuinely and directly concerns that dimension.
- Return ONLY a JSON array, one object per claim, shaped EXACTLY like:
  {{"text": "...", "entities": ["...", "..."], "political": 0.0, "economic": 0.0, "social": 0.0, "technological": 0.0, "legal": 0.0, "environmental": 0.0, "threat_new_entrants": 0.0, "supplier_power": 0.0, "buyer_power": 0.0, "threat_substitutes": 0.0, "competitive_rivalry": 0.0, "polarity": "positive"}}
- No other text, no markdown fences, no explanation.

Text:
\"\"\"{text}\"\"\"

JSON array:"""


def _clamp(value) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return 0.0


def _blank_scores() -> tuple[dict, dict]:
    return ({d: 0.0 for d in PESTLE_DIMS}, {d: 0.0 for d in PORTERS_DIMS})


def _parse(raw_response: str) -> list[dict] | None:
    """Pulls the first [...] block out (tolerating prose/markdown-fence
    wrapping) and normalizes each item. Unlike the old two-step parsers, a
    missing/malformed individual item is dropped rather than kept as a
    zero-score placeholder - a fact with no text isn't a fact, and there is no
    positional field-count to preserve (this call produces its OWN facts,
    it isn't scoring a fixed pre-existing list)."""
    match = re.search(r"\[.*\]", raw_response, re.DOTALL)
    if not match:
        return None
    try:
        raw_items = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    if not isinstance(raw_items, list):
        return None

    facts = []
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        text = str(item.get("text", "")).strip()
        if not text:
            continue
        entities = [str(e).strip() for e in (item.get("entities") or []) if str(e).strip()]
        pestle = {d: _clamp(item.get(d, 0.0)) for d in PESTLE_DIMS}
        porters = {d: _clamp(item.get(d, 0.0)) for d in PORTERS_DIMS}
        polarity = str(item.get("polarity", "")).strip().lower()
        facts.append({
            "text": text,
            "entities": entities,
            "pestle_scores": pestle,
            "porters_scores": porters,
            "polarity": polarity if polarity in ("positive", "negative") else "negative",
        })
    return facts or None


def extract_and_classify_with_status(text: str, attempts: int = GROQ_MAX_ATTEMPTS) -> tuple[list[dict], bool]:
    """Returns (facts, ok). `ok` is False only if every attempt failed, in
    which case facts degrades to ONE record covering the whole input, all-zero
    scores, empty entities - this single fallback simultaneously represents a
    decomposition failure (unsplit) AND a classification failure (unscored),
    since one call now does both jobs; callers should record `ok` as both
    decomposition_ok and classification_ok rather than treating them as
    independently-failable any more.

    Retries mirror fact_extraction.extract_facts_with_status: a timeout
    shrinks the input on retry (retrying an oversized prompt verbatim just
    times out again); malformed JSON is retried verbatim (sampling noise);
    persistent rate-limiting degrades immediately rather than exhausting the
    attempt budget against a quota that won't reset for hours.
    """
    attempt_text = text
    for attempt in range(1, attempts + 1):
        try:
            raw_response = call_groq(BUNDLED_PROMPT.format(text=attempt_text), temperature=0.2)
            facts = _parse(raw_response)
            if facts is not None:
                return facts, True
            reason = "unparseable JSON"
        except GroqRateLimited as exc:
            print(f"  [fact_pipeline] persistently rate limited ({exc}) - "
                  "storing the input UNSPLIT and UNCLASSIFIED.")
            break
        except GroqError as exc:
            reason = f"call failed ({exc})"
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            reason = f"call failed ({exc})"
            shrunk = int(len(attempt_text) * OLLAMA_RETRY_SHRINK_FACTOR)
            if shrunk > 120:
                cut = attempt_text[:shrunk].rfind(" ")
                attempt_text = attempt_text[:cut] if cut > shrunk // 2 else attempt_text[:shrunk]

        if attempt < attempts:
            print(f"  [fact_pipeline] attempt {attempt}/{attempts} {reason} - retrying "
                  f"({len(attempt_text)} chars)")
            time.sleep(OLLAMA_RETRY_BACKOFF_SECONDS * (2 ** (attempt - 1)))
        else:
            print(f"  [fact_pipeline] all {attempts} attempts failed ({reason}) - "
                  "storing the input UNSPLIT and UNCLASSIFIED.")

    pestle, porters = _blank_scores()
    return [{"text": text, "entities": [], "pestle_scores": pestle, "porters_scores": porters,
             "polarity": "negative"}], False
