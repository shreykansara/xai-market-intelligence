"""Assigns PESTLE/Porter's relevance scores and a polarity to already-decomposed
atomic facts, using the same local Ollama model fact_extraction.py uses.

Why an LLM rather than the k-NN seed transfer seed_inference.py does: that
mechanism infers a new item's scores by looking up its nearest neighbours in an
ALREADY-SCORED reference corpus. With the fabricated seed corpus removed, no
such reference pool exists any more - there is nothing to take neighbours from.
Scoring therefore has to be derived from each fact's own text, which is what
this module does.

One call classifies EVERY fact from a single announcement together, rather than
one call per fact: at ~16.5k announcements a per-fact call would multiply an
already hours-long run by the average fact count. Batching per announcement also
gives the model the sibling facts as context, which is closer to how a human
would read a notice.

Scores are 0-1 relevance per dimension, deliberately soft/multi-label (the same
shape generate_news.py produced for the fabricated corpus, so everything
downstream - sub-cluster discovery, gating, roll-up - keeps working unchanged).
Most LPU announcements are administrative (exam schedules, office circulars) and
SHOULD score near zero on every market dimension; the prompt says so explicitly,
because a model asked to classify will otherwise reach for a nonzero answer.

If Ollama is unreachable or returns unparseable output, every fact falls back to
all-zero relevance with neutral-negative polarity and is flagged
classification_ok=False, so a failed call is visible in the store rather than
silently indistinguishable from a genuine "this notice has no market relevance"
result.
"""
import json
import re
import time
import urllib.error
import urllib.request

from .config import (
    OLLAMA_HOST,
    OLLAMA_MAX_ATTEMPTS,
    OLLAMA_MODEL,
    OLLAMA_RETRY_BACKOFF_SECONDS,
    OLLAMA_TIMEOUT_SECONDS,
    PESTLE_DIMS,
    PORTERS_DIMS,
    LLM_PROVIDER,
)
from .groq_client import GroqError, GroqRateLimited, call_groq

ALL_DIMS = PESTLE_DIMS + PORTERS_DIMS

CLASSIFICATION_PROMPT = """You are scoring university announcements for their relevance to business/market analysis frameworks.

For EACH numbered statement below, give a relevance score from 0.0 to 1.0 for each of these 11 dimensions, plus an overall polarity.

PESTLE dimensions:
- political: government, regulation, policy, public administration
- economic: funding, costs, prices, jobs, trade, economic conditions
- social: people, culture, demographics, education, community, student life
- technological: technology, research, innovation, digital systems, engineering
- legal: law, compliance, contracts, rules, formal legal process
- environmental: climate, sustainability, energy, pollution, physical environment

Porter's Five Forces dimensions:
- threat_new_entrants: new competitors/players entering a market or field
- supplier_power: suppliers, vendors, input providers and their leverage
- buyer_power: customers, students-as-customers, clients and their leverage
- threat_substitutes: alternative options replacing an existing offering
- competitive_rivalry: competition between existing players, rankings, contests

Rules:
- MOST university announcements are routine administration (exam schedules, viva notices, office circulars, holiday notices). These have NO market relevance: score them at or near 0.0 on every dimension. Do not invent relevance that isn't there.
- Only give a score above 0.5 when the statement genuinely and directly concerns that dimension.
- polarity must be exactly "positive" or "negative": does this read as a favourable/opportunity-creating development, or an unfavourable/restrictive/problematic one? If genuinely neutral, choose based on the closest fit.
- Return ONLY a JSON array with one object per numbered statement, in the same order, each shaped exactly like:
  {{"n": 1, "political": 0.0, "economic": 0.0, "social": 0.0, "technological": 0.0, "legal": 0.0, "environmental": 0.0, "threat_new_entrants": 0.0, "supplier_power": 0.0, "buyer_power": 0.0, "threat_substitutes": 0.0, "competitive_rivalry": 0.0, "polarity": "positive"}}
- No other text, no markdown fences, no explanation.

Statements:
{statements}

JSON array:"""


def _blank_scores() -> tuple[dict, dict]:
    return ({d: 0.0 for d in PESTLE_DIMS}, {d: 0.0 for d in PORTERS_DIMS})


def _call_model(prompt: str) -> str:
    """Transport only - the classification prompt above is unchanged. Which
    transport runs is config.LLM_PROVIDER (see that flag for why)."""
    if LLM_PROVIDER == "ollama":
        return _call_ollama_legacy(prompt)
    return call_groq(prompt, temperature=0.2)


def _call_ollama_legacy(prompt: str) -> str:
    """Previous local-Ollama transport, kept for reference. Not in the runtime path."""
    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        # Same reasoning as fact_extraction.py: low temperature buys JSON
        # schema compliance on a nested schema, not truthfulness.
        "options": {"temperature": 0.2},
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_HOST}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT_SECONDS) as resp:
        return json.loads(resp.read().decode("utf-8")).get("response", "")


def _clamp(value) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return 0.0


def _parse(raw_response: str, n_facts: int) -> list[dict] | None:
    """Pulls the first [...] block out (the model sometimes wraps it in prose or
    a fence) and maps it back onto the input facts BY ORDER, not by trusting the
    model's own "n" field - a wrong/duplicated index would otherwise silently
    misattribute one fact's scores to another."""
    match = re.search(r"\[.*\]", raw_response, re.DOTALL)
    if not match:
        return None
    try:
        items = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    if not isinstance(items, list) or not items:
        return None

    results = []
    for i in range(n_facts):
        item = items[i] if i < len(items) and isinstance(items[i], dict) else {}
        pestle = {d: _clamp(item.get(d, 0.0)) for d in PESTLE_DIMS}
        porters = {d: _clamp(item.get(d, 0.0)) for d in PORTERS_DIMS}
        polarity = str(item.get("polarity", "")).strip().lower()
        results.append({
            "pestle_scores": pestle,
            "porters_scores": porters,
            "polarity": polarity if polarity in ("positive", "negative") else "negative",
            # A fact the model simply didn't return a row for is marked failed
            # rather than being handed silent all-zero scores.
            "classification_ok": i < len(items) and isinstance(items[i], dict),
        })
    return results


def classify_facts(fact_texts: list[str], attempts: int = OLLAMA_MAX_ATTEMPTS) -> list[dict]:
    """Scores every fact from one announcement in a single Ollama call. Always
    returns exactly len(fact_texts) records, in the same order - callers never
    need a separate failure path, but should surface classification_ok=False
    rather than treating a failed call as a genuine all-zero result.

    Retries on both observed failure modes (timeout, malformed JSON). A batch
    that times out is retried in HALVES rather than whole: the cost driver here
    is the number of statements to score, so splitting an oversized batch is
    what actually makes the call finish, and it still returns scores for every
    fact instead of writing the whole batch off."""
    if not fact_texts:
        return []

    for attempt in range(1, attempts + 1):
        statements = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(fact_texts))
        try:
            raw = _call_model(CLASSIFICATION_PROMPT.format(statements=statements))
            parsed = _parse(raw, len(fact_texts))
            if parsed is not None:
                return parsed
            reason = "unparseable JSON"
        except GroqRateLimited as exc:
            # Persistent rate limiting degrades to "unclassified" rather than
            # stalling the run - the flag makes the zeros mean "not scored",
            # never "genuinely no market relevance".
            print(f"  [lpu_classification] persistently rate limited ({exc}) - "
                  f"{len(fact_texts)} fact(s) left unclassified.")
            pestle, porters = _blank_scores()
            return [
                {"pestle_scores": dict(pestle), "porters_scores": dict(porters),
                 "polarity": "negative", "classification_ok": False}
                for _ in fact_texts
            ]
        except (GroqError, urllib.error.URLError, TimeoutError, OSError) as exc:
            reason = f"call failed ({exc})"
            # A batch too large to score in time won't get smaller by retrying
            # it whole - split it and score each half independently.
            if len(fact_texts) > 1:
                mid = len(fact_texts) // 2
                print(f"  [lpu_classification] {reason} - splitting batch of "
                      f"{len(fact_texts)} into {mid} + {len(fact_texts) - mid}")
                return classify_facts(fact_texts[:mid], attempts) + classify_facts(fact_texts[mid:], attempts)

        if attempt < attempts:
            print(f"  [lpu_classification] attempt {attempt}/{attempts} {reason} - retrying")
            time.sleep(OLLAMA_RETRY_BACKOFF_SECONDS * (2 ** (attempt - 1)))

    print(f"  [lpu_classification] all {attempts} attempts failed - {len(fact_texts)} fact(s) left unclassified.")
    pestle, porters = _blank_scores()
    return [
        {"pestle_scores": dict(pestle), "porters_scores": dict(porters),
         "polarity": "negative", "classification_ok": False}
        for _ in fact_texts
    ]
