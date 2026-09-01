"""Fact decomposition: turns one fetched article's text into one or more atomic,
independently-scorable fact records, using a free local generative model via
Ollama (https://ollama.com) - not a paid API. Runs between fetching and
embedding in the ingestion pipeline (src/marketintel/ingestion.py), changing
the unit everything downstream operates on from "one article" to "one or more
atomic facts": a tax policy piece with a bracket increase and a separate
bracket decrease becomes two fact records, not one blended one.

Each extracted fact also carries a list of named entities (people,
organizations, places, and specifically-named policies/products/programs)
preserved from the neutral rewrite - used downstream by
comparative_matching.py to confirm two facts are about the same specific
subject before ever treating one as the "prior value" for the other (e.g.
telling mobile-phone GST apart from textile GST even when the surrounding
language is otherwise similar).

Directional/comparative language ("raised", "cut", "increased", "decreased",
"from X to Y") is factual content to KEEP, not rhetorical framing to strip -
only editorializing/opinion language (e.g. "disastrous", "long-overdue",
"critics say") gets neutralized. This distinction matters because
comparative_matching.py only bothers doing a prior-value lookup for facts
that DON'T already state their own direction; a fact that already says
"raised from 12% to 18%" is unambiguous on its own and needs no lookup, but
stripping the direction out during neutralization would wrongly turn it into
a bare state value that then requires one.

Ollama is expected to already be running locally with OLLAMA_MODEL pulled
(`ollama pull llama3.2:3b`, or whatever OLLAMA_MODEL is set to). If it's
unreachable, times out, or returns something that can't be parsed as the
expected JSON array, this falls back to treating the whole input text as a
single fact with no entities, unmodified - decomposition quality degrades to
a no-op, but ingestion doesn't stop. Every fallback is printed so it's
visible in the ingestion log rather than silently changing behavior.
"""
import json
import re
import urllib.error
import urllib.request

from .config import OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_TIMEOUT_SECONDS

EXTRACTION_PROMPT = """You are extracting atomic, independently-scorable factual claims from a news article or headline.

Rules:
- Identify each DISTINCT factual claim that could be scored independently. A different number, a different direction of change, or a different affected party each count as a separate claim.
- Rewrite each claim in neutral, plain language: strip loaded framing, opinion, and rhetorical language (e.g. "disastrous", "critics say", "long-overdue") - but KEEP every specific: numbers, thresholds, dates, and named parties must be preserved exactly as given.
- Directional and comparative language is factual content, NOT rhetorical framing - always keep it. Words like "raised", "cut", "increased", "decreased", "hiked", "slashed", and phrases like "from X to Y" or "up from X" must be preserved exactly when the source text states them. Only remove them if the source genuinely never states a direction at all.
- For each claim, also list the specific named entities it's about (people, organizations, places, and specifically-named policies/products/programs - e.g. "GST on mobile phones", "Reserve Bank of India", "Punjab"). Use the same names as they appear in your neutral rewrite.
- If the text only contains one claim, return just that one claim, neutrally rewritten, with its own entity list.
- Return ONLY a JSON array of objects, one per claim, each shaped exactly like {{"text": "...", "entities": ["...", "..."]}}. No other text, no markdown code fences, no explanation.

Text:
\"\"\"{text}\"\"\"

JSON array of {{"text": ..., "entities": [...]}} objects:"""


def _call_ollama(text: str) -> str:
    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": EXTRACTION_PROMPT.format(text=text),
        "stream": False,
        # Lower than Ollama's default (~0.8): the extraction output is now a
        # nested JSON schema (objects with "text"/"entities", not bare
        # strings), and at default temperature llama3.2:3b would sometimes
        # return malformed items (a bare string where an object was expected,
        # or an object missing "text") - measured directly at ~7% of calls in
        # a real GDELT smoke test. Re-tested at temperature=0.2
        # against a fresh sample and got 6/6 well-formed responses. This does
        # NOT fix hallucination on sparse/low-content titles (a separate,
        # unresolved issue - see CLAUDE.md) - a side-by-side test
        # found the model fabricated MORE confidently at low temperature for
        # one genuinely content-free title, rather than correctly returning
        # an empty array as it did at default temperature. Low temperature
        # buys schema compliance, not truthfulness.
        "options": {"temperature": 0.2},
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_HOST}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT_SECONDS) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    return body.get("response", "")


def _parse_facts(raw_response: str) -> list[dict] | None:
    """The model is asked for a bare JSON array of {"text", "entities"} objects, but
    local models don't always comply - pull out the first [...] block (in case it's
    wrapped in prose or a markdown fence) and parse that, rather than requiring an
    exact match. Also tolerates an older-style array of bare strings (no entities)
    by treating each string as {"text": s, "entities": []}, so a model that ignores
    the object-schema instruction still degrades gracefully instead of failing."""
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
        if isinstance(item, dict):
            text = str(item.get("text", "")).strip()
            entities = item.get("entities") or []
            entities = [str(e).strip() for e in entities if str(e).strip()]
        else:
            text = str(item).strip()
            entities = []
        if text:
            facts.append({"text": text, "entities": entities})
    return facts or None


def extract_facts_detailed(text: str) -> list[dict]:
    """Returns one or more {"text": neutral fact string, "entities": [...]} records
    extracted from `text`. Falls back to [{"text": text, "entities": []}] if Ollama
    is unreachable, times out, or its output can't be parsed - callers always get a
    non-empty list back and don't need a separate failure path."""
    try:
        raw_response = _call_ollama(text)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"  [fact_extraction] Ollama unreachable ({exc}) - using original text as a single fact.")
        return [{"text": text, "entities": []}]

    facts = _parse_facts(raw_response)
    if facts is None:
        print("  [fact_extraction] could not parse Ollama's response as a JSON array - using original text as a single fact.")
        return [{"text": text, "entities": []}]
    return facts


def extract_facts(text: str) -> list[str]:
    """Backward-compatible wrapper for callers that only need the fact text (the
    live ingestion.py path) - entities are consumed by that path's
    comparative_matching.py, so unchanged callers don't need to know the schema grew."""
    return [f["text"] for f in extract_facts_detailed(text)]
