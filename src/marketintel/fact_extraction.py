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
import time
import urllib.error
import urllib.request

from .config import (
    OLLAMA_HOST,
    OLLAMA_MAX_ATTEMPTS,
    OLLAMA_MODEL,
    OLLAMA_RETRY_BACKOFF_SECONDS,
    OLLAMA_RETRY_SHRINK_FACTOR,
    OLLAMA_TIMEOUT_SECONDS,
    LLM_PROVIDER,
)
from .groq_client import GroqError, GroqRateLimited, call_groq

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


def _call_model(text: str) -> str:
    """Transport only - the prompt and _parse_facts() are unchanged from the
    Ollama implementation. Which transport runs is config.LLM_PROVIDER; see
    that flag for the measured reason bulk and live workloads want different
    answers, and groq_client.py for the rate-limit handling."""
    prompt = EXTRACTION_PROMPT.format(text=text)
    if LLM_PROVIDER == "ollama":
        return _call_ollama_legacy(text)
    return call_groq(prompt, temperature=0.2)


def _call_ollama_legacy(text: str) -> str:
    """The previous local-Ollama transport, kept only for reference/offline
    fallback experiments. Nothing in the runtime path calls this."""
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


def extract_facts_with_status(text: str, attempts: int = OLLAMA_MAX_ATTEMPTS) -> tuple[list[dict], bool]:
    """Returns (facts, ok). `ok` is False ONLY if every attempt failed, in which
    case facts degrades to [{"text": text, "entities": []}] - the whole input
    stored unsplit, which is a compound record, not an atomic one. Callers that
    care about atomicity should record that distinction rather than infer it.

    Retries exist because both observed failure modes are transient:
      - a TIMEOUT on a long input, which retrying verbatim would just repeat -
        so each retry shrinks the input (OLLAMA_RETRY_SHRINK_FACTOR), turning
        an input the model can't finish in time into one it can;
      - malformed JSON, which is sampling noise and usually succeeds on retry.
    """
    attempt_text = text
    for attempt in range(1, attempts + 1):
        try:
            raw_response = _call_model(attempt_text)
            facts = _parse_facts(raw_response)
            if facts is not None:
                return facts, True
            reason = "unparseable JSON"
        except GroqRateLimited as exc:
            # groq_client has already waited out every retry-after it was
            # given. Degrading here (unsplit single fact) is the documented
            # graceful path - it keeps ingestion moving instead of stalling
            # the whole run behind a quota that won't reset for hours.
            print(f"  [fact_extraction] persistently rate limited ({exc}) - "
                  "storing the input UNSPLIT (not atomic).")
            return [{"text": text, "entities": []}], False
        except GroqError as exc:
            reason = f"call failed ({exc})"
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            reason = f"call failed ({exc})"
            # Only a timeout is plausibly caused by input size; shrink so the
            # next attempt is materially cheaper rather than identical.
            shrunk = int(len(attempt_text) * OLLAMA_RETRY_SHRINK_FACTOR)
            if shrunk > 120:
                cut = attempt_text[:shrunk].rfind(" ")
                attempt_text = attempt_text[:cut] if cut > shrunk // 2 else attempt_text[:shrunk]

        if attempt < attempts:
            print(f"  [fact_extraction] attempt {attempt}/{attempts} {reason} - retrying "
                  f"({len(attempt_text)} chars)")
            time.sleep(OLLAMA_RETRY_BACKOFF_SECONDS * (2 ** (attempt - 1)))

    print(f"  [fact_extraction] all {attempts} attempts failed - storing the input UNSPLIT (not atomic).")
    return [{"text": text, "entities": []}], False


def extract_facts_detailed(text: str) -> list[dict]:
    """Returns one or more {"text": neutral fact string, "entities": [...]} records
    extracted from `text`. Retries internally (see extract_facts_with_status) and
    falls back to [{"text": text, "entities": []}] only if every attempt failed -
    callers always get a non-empty list back and don't need a separate failure
    path. Use extract_facts_with_status() when the failure itself matters."""
    facts, _ok = extract_facts_with_status(text)
    return facts


def extract_facts(text: str) -> list[str]:
    """Backward-compatible wrapper for callers that only need the fact text (the
    live ingestion.py path) - entities are consumed by that path's
    comparative_matching.py, so unchanged callers don't need to know the schema grew."""
    return [f["text"] for f in extract_facts_detailed(text)]
