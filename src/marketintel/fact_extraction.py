"""Fact decomposition: turns one fetched article's text into one or more atomic,
independently-scorable fact records, using a free local generative model via
Ollama (https://ollama.com) - not a paid API. Runs between fetching and
embedding in the ingestion pipeline (src/marketintel/ingestion.py), changing
the unit everything downstream operates on from "one article" to "one or more
atomic facts": a tax policy piece with a bracket increase and a separate
bracket decrease becomes two fact records, not one blended one.

Ollama is expected to already be running locally with OLLAMA_MODEL pulled
(`ollama pull llama3.2:3b`, or whatever OLLAMA_MODEL is set to). If it's
unreachable, times out, or returns something that can't be parsed as the
expected JSON array, this falls back to treating the whole input text as a
single fact, unmodified - decomposition quality degrades to a no-op, but
ingestion doesn't stop. Every fallback is printed so it's visible in the
ingestion log rather than silently changing behavior.
"""
import json
import re
import urllib.error
import urllib.request

from .config import OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_TIMEOUT_SECONDS

EXTRACTION_PROMPT = """You are extracting atomic, independently-scorable factual claims from a news article or headline.

Rules:
- Identify each DISTINCT factual claim that could be scored independently. A different number, a different direction of change, or a different affected party each count as a separate claim.
- Rewrite each claim in neutral, plain language: strip loaded framing, opinion, and rhetorical language, but KEEP every specific - numbers, thresholds, dates, and named parties must be preserved exactly as given.
- If the text only contains one claim, return just that one claim, neutrally rewritten.
- Return ONLY a JSON array of strings, one per claim. No other text, no markdown code fences, no explanation.

Text:
\"\"\"{text}\"\"\"

JSON array of neutral factual claims:"""


def _call_ollama(text: str) -> str:
    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": EXTRACTION_PROMPT.format(text=text),
        "stream": False,
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


def _parse_facts(raw_response: str) -> list[str] | None:
    """The model is asked for a bare JSON array but local models don't always
    comply - pull out the first [...] block (in case it's wrapped in prose or a
    markdown fence) and parse that, rather than requiring an exact match."""
    match = re.search(r"\[.*\]", raw_response, re.DOTALL)
    if not match:
        return None
    try:
        facts = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    if not isinstance(facts, list):
        return None
    facts = [str(f).strip() for f in facts if str(f).strip()]
    return facts or None


def extract_facts(text: str) -> list[str]:
    """Returns one or more neutral, atomic fact strings extracted from `text`.
    Falls back to [text] unmodified if Ollama is unreachable, times out, or its
    output can't be parsed - callers always get a non-empty list back and don't
    need a separate failure path."""
    try:
        raw_response = _call_ollama(text)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"  [fact_extraction] Ollama unreachable ({exc}) - using original text as a single fact.")
        return [text]

    facts = _parse_facts(raw_response)
    if facts is None:
        print("  [fact_extraction] could not parse Ollama's response as a JSON array - using original text as a single fact.")
        return [text]
    return facts
