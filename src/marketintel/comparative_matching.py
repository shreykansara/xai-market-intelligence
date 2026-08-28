"""Comparative-fact matching: for a bare state-value fact with no directional
language of its own (e.g. "GST on mobile phones is 18%"), find the nearest
EARLIER fact about the same specific subject and use it to compute a direction
(increase/decrease) - rather than leaving the fact's polarity ambiguous or
guessing. Only used by the GDELT bulk backfill pipeline (gdelt_bulk.py); the
live ingestion_service.py's per-item order is unchanged and doesn't call this.

Order of operations, per fact:
  (a) If the fact's own text already contains directional/comparative language
      (see HAS_DIRECTION_PATTERN below), it's self-contained - use it as-is,
      no lookup needed. This is why fact_extraction.py's prompt was changed to
      PRESERVE "raised"/"cut"/"from X to Y" as factual content rather than
      neutralizing it away: stripping that language would wrongly turn an
      already-unambiguous fact into a bare value that then needs a lookup.
  (b) Otherwise, search already-stored facts with a STRICTLY EARLIER timestamp
      (never a later one - that would be looking into the future) for the most
      similar match above COMPARATIVE_MATCH_SIMILARITY_THRESHOLD (stricter than
      the general relevance gate, since a wrong match here fabricates a
      direction rather than just mis-scoring relevance). Before accepting a
      similarity match, also require the two facts' entity lists (extracted by
      fact_extraction.py from the same neutral rewrite) to overlap by at least
      ENTITY_JACCARD_THRESHOLD - this is what stops e.g. mobile-phone GST from
      being cross-matched against textile GST just because "GST", "India", and
      "percent" make the surrounding language look similar. A bare non-empty
      intersection isn't enough: validation caught that two facts sharing only
      a broad, incidental entity (both mention "India") but nothing else still
      passed a plain overlap check even though their actual specific subjects
      differed completely - see ENTITY_JACCARD_THRESHOLD's comment below.
  (c) If no temporally-prior candidate clears BOTH the similarity threshold and
      the entity check, the fact is left without a computed direction and
      logged separately (BACKFILL_UNMATCHED_LOG_PATH) - never force a guess.

A numeric value (percentage, currency amount, or bare number) is extracted
from each fact's text via regex for the actual increase/decrease comparison
once a valid prior match is found; if either fact has no cleanly-parseable
single principal value, the match is treated as inconclusive and the fact
still gets logged as unmatched rather than guessing a direction from text
alone.
"""
import re
from datetime import datetime

import numpy as np

from .config import COMPARATIVE_MATCH_SIMILARITY_THRESHOLD

# Words/phrases that make a fact's own direction explicit - if any of these
# appear, the fact is self-contained and skips the prior-match lookup entirely
# (rule (a) above). Deliberately broad: false positives here just mean a
# skipped lookup (harmless - the fact was already unambiguous), false
# negatives mean an unnecessary-but-harmless lookup attempt, since rule (b)/(c)
# only ever proceeds when a genuinely qualifying match is found.
HAS_DIRECTION_PATTERN = re.compile(
    r"\b(raised?|rais(?:ing|ed)|cut|cuts|cutting|increase[sd]?|increasing|"
    r"decrease[sd]?|decreasing|hik(?:e|ed|es|ing)|slash(?:ed|es|ing)?|"
    r"rose|rising|fell|falling|fallen|dropp?ed|dropping|"
    r"up from|down from|higher than|lower than|from \d|to \d)\b",
    re.IGNORECASE,
)

# Matches a percentage, a currency amount, or a bare number - used to pull the
# one principal value out of a bare state-value fact for comparison. Takes the
# FIRST such match in the text, since atomic facts (post-decomposition) should
# only ever be about one number.
NUMERIC_VALUE_PATTERN = re.compile(
    r"(?P<value>-?\d[\d,]*\.?\d*)\s*(?P<unit>%|percent|percentage points?)?"
)


def has_own_direction(fact_text: str) -> bool:
    """Rule (a): does this fact already state its own direction, making a
    prior-value lookup unnecessary?"""
    return bool(HAS_DIRECTION_PATTERN.search(fact_text))


def extract_numeric_value(fact_text: str) -> float | None:
    """Pulls the single principal numeric value out of a fact's text (e.g. "18"
    from "GST on mobile phones is 18%"). Returns None if no number is found -
    callers must treat that as "can't compute a direction", not as zero."""
    match = NUMERIC_VALUE_PATTERN.search(fact_text)
    if not match:
        return None
    raw = match.group("value").replace(",", "")
    try:
        return float(raw)
    except ValueError:
        return None


# Rule (b)'s entity check was originally "do the two entity sets share ANY
# member" - validation (scripts/validate_comparative_matching.py, test 2b)
# caught this as a real bug before it ever touched backfill data: two facts
# about DIFFERENT specific subjects (mobile-phone GST vs. textile GST) still
# shared a generic entity ("India"), which was enough for a bare non-empty
# intersection to call it a match even at similarity=1.0. A broad entity that
# legitimately co-occurs across many unrelated facts must not be able to carry
# a match on its own. Fixed by requiring the two sets to overlap by at least
# this fraction (Jaccard similarity = |intersection| / |union|) rather than
# merely intersecting - two facts about the true same subject share ALL or
# nearly all of their entities (Jaccard 1.0 in every hand-authored real-world
# case tested), while two facts that only share one broad, incidental entity
# alongside a different specific subject land well below this.
ENTITY_JACCARD_THRESHOLD = 0.5


def normalize_entities(entities: list[str]) -> set[str]:
    return {e.strip().lower() for e in entities if e.strip()}


def entities_overlap(a: list[str], b: list[str], threshold: float = ENTITY_JACCARD_THRESHOLD) -> bool:
    """Rule (b)'s entity check: the two facts' entity sets must overlap by at
    least `threshold` Jaccard similarity - not just share any single member -
    so a broad, incidental entity (a country name, a generic org) can't carry
    a match between two facts about different specific subjects."""
    set_a, set_b = normalize_entities(a), normalize_entities(b)
    if not set_a or not set_b:
        return False
    union = set_a | set_b
    if not union:
        return False
    jaccard = len(set_a & set_b) / len(union)
    return jaccard >= threshold


def find_prior_match(
    embedding: np.ndarray,
    entities: list[str],
    published: datetime,
    stored_facts: list[dict],
    stored_embeddings: list[np.ndarray],
    similarity_threshold: float = COMPARATIVE_MATCH_SIMILARITY_THRESHOLD,
    candidate_pool_idx: list[int] | None = None,
):
    """Rule (b)/(c): among stored_facts with a STRICTLY earlier `published`
    timestamp than this fact's, find the highest-similarity match that also
    clears similarity_threshold AND shares a named entity. Returns
    (matched_fact, similarity) or (None, best_similarity_seen) if nothing
    qualifies - the caller logs the fact as unmatched in the latter case
    rather than forcing a guess.

    candidate_pool_idx optionally restricts which stored_facts indices are even
    considered, before the temporal/entity checks below run - at backfill scale
    (millions of stored facts), scanning every single one for entity overlap on
    every new fact would itself become a real bottleneck over a multi-month
    run. gdelt_backfill.py passes an entity-inverted-index-derived pool here;
    validation (scripts/validate_comparative_matching.py) omits it and gets the
    same result by scanning everything, since a candidate that shares no entity
    at all can never pass entities_overlap regardless."""
    search_space = range(len(stored_facts)) if candidate_pool_idx is None else candidate_pool_idx
    candidate_idx = [
        i for i in search_space
        if datetime.fromisoformat(stored_facts[i]["published"]) < published
        and entities_overlap(stored_facts[i].get("entities", []), entities)
    ]
    if not candidate_idx:
        return None, 0.0

    candidate_matrix = np.array([stored_embeddings[i] for i in candidate_idx])
    sims = candidate_matrix @ embedding
    best_local = int(np.argmax(sims))
    best_sim = float(sims[best_local])
    if best_sim >= similarity_threshold:
        return stored_facts[candidate_idx[best_local]], best_sim
    return None, best_sim


def compute_direction(prior_fact: dict, current_text: str) -> str | None:
    """Compares the prior matched fact's principal value against the current
    fact's, returning "increase", "decrease", or None if either value can't be
    cleanly parsed (never guesses from text alone at this stage - the two
    facts already matched on similarity + entity overlap, so the ONLY thing
    left to determine is which way the number moved)."""
    prior_value = extract_numeric_value(prior_fact["fact_text"])
    current_value = extract_numeric_value(current_text)
    if prior_value is None or current_value is None:
        return None
    if current_value > prior_value:
        return "increase"
    if current_value < prior_value:
        return "decrease"
    return None


def resolve_comparative_fact(
    fact_text: str,
    entities: list[str],
    embedding: np.ndarray,
    published: datetime,
    stored_facts: list[dict],
    stored_embeddings: list[np.ndarray],
    candidate_pool_idx: list[int] | None = None,
) -> dict:
    """Full per-fact resolution per the (a)/(b)/(c) order in the module
    docstring. Returns a dict with:
      - "has_own_direction": bool (rule a)
      - "matched_prior_fact_id": str | None (rule b, the fact this was
        compared against, if any)
      - "match_similarity": float (best similarity seen, whether or not it
        cleared the threshold - useful for tuning COMPARATIVE_MATCH_SIMILARITY_THRESHOLD)
      - "computed_direction": "increase" | "decrease" | None
    Never raises and never forces a guess - "computed_direction": None (with
    "matched_prior_fact_id": None) is the correct, expected outcome whenever
    rule (c) applies, and callers should log that case rather than treat it as
    an error."""
    if has_own_direction(fact_text):
        return {
            "has_own_direction": True,
            "matched_prior_fact_id": None,
            "match_similarity": None,
            "computed_direction": None,
        }

    match, similarity = find_prior_match(
        embedding, entities, published, stored_facts, stored_embeddings, candidate_pool_idx=candidate_pool_idx
    )
    if match is None:
        return {
            "has_own_direction": False,
            "matched_prior_fact_id": None,
            "match_similarity": similarity,
            "computed_direction": None,
        }

    direction = compute_direction(match, fact_text)
    return {
        "has_own_direction": False,
        "matched_prior_fact_id": match["id"],
        "match_similarity": similarity,
        "computed_direction": direction,
    }
