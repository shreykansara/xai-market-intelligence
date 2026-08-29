"""Grounding safeguards against fact-decomposition hallucination, used only by
the GDELT bulk backfill (gdelt_backfill.py) - not the live ingestion.py path.

Two independent layers, deliberately different in kind:

1. is_likely_non_content() - a PRE-FILTER that runs BEFORE any Ollama call,
   on the raw fetched title. Rejects obvious section labels / non-news junk
   (all-caps with no sentence structure, very short with no verb and no
   numbers, or a known-junk keyword) so they never reach the model at all.
   This is a cheap heuristic, not a guarantee - it catches clear cases
   ("COMMUNITY CALENDAR") but plenty of low-content-but-not-obviously-junk
   titles will still get through to decomposition.

2. is_grounded() - the REAL safeguard, run AFTER decomposition on every
   extracted fact. Every number the fact states (a percentage, a currency
   amount, a bare figure, a year) must appear - verbatim or near-verbatim -
   somewhere in the original source title the model was given. A fact
   inventing a number the source never mentioned (the diagnosed case: the
   headline "COMMUNITY CALENDAR" produced a fabricated "GST... from 18% to
   8%" claim, with neither "18" nor "8" appearing anywhere in the source)
   gets rejected here regardless of whether the pre-filter caught it.
   Deliberately independent of Ollama's request temperature - lowering
   temperature (fact_extraction.py) fixed JSON schema compliance but was
   shown NOT to fix hallucination, and in one case made it worse; this check
   doesn't rely on the model behaving better, it verifies the output against
   the source directly.

A fact with NO numeric claims at all (e.g. "the government announced a new
policy" with no figures) has nothing for is_grounded() to check and is
treated as grounded by default - this safeguard specifically targets
fabricated NUMBERS, which is what the diagnosed failure cases actually
produced, not text-level hallucination in general (a real, standing
limitation - see CLAUDE.md).

Both functions HTML-unescape their input before extracting numbers or
checking keywords. gdelt_bulk.py now decodes titles at the source, but a
retroactive audit against already-collected pilot data found a confirmed,
concrete false accept caused by NOT doing this: a title reading "...&#x2013;
Latest News..." (an undecoded em-dash entity) contains the literal digit run
"2013" - which coincidentally satisfied a fabricated fact's "20%" claim as
"grounded" even though the source had nothing to do with the fact's subject
at all (a generic magazine masthead vs. a fabricated Punjab water-supply
policy). Decoding here too means this module gives correct answers
regardless of whether the caller already decoded its input.
"""
import html
import re

# A decimal point is only consumed as part of the number if at least one digit
# follows it (\.\d+, not \.?\d*) - otherwise a sentence-ending period after a
# bare integer (e.g. "...at the age of 34.") gets swallowed into the "number"
# as "34.", which then fails to match a source that correctly has no trailing
# period (e.g. a headline reading "...dies aged 34"). Confirmed as a real
# false-rejection bug during live ingestion spot-checking, not just a
# theoretical risk - a genuinely well-grounded fact was rejected over this.
NUMBER_PATTERN = re.compile(r"\d[\d,]*(?:\.\d+)?%?")

# Case-insensitive substring match against the raw title - deliberately small
# and specific rather than an exhaustive taxonomy; broadened as real
# false-negative cases turn up in spot-checks.
JUNK_KEYWORD_PATTERNS = [
    "community calendar", "calendar", "digest", "roundup", "round-up",
    "round up", "prop picks", "best bets", "today in history",
    "trivia night", "classifieds", "obituaries", "horoscope", "crossword",
    "sudoku", "weather forecast", "traffic report", "tv listings",
    "lottery numbers", "box scores",
]

# A small set of common verb forms (including common irregulars), used as a
# weak "does this look like a sentence, not a label" signal alongside the
# suffix heuristic in _looks_like_verb. Not a POS tagger - just enough to
# distinguish "X raises Y" from "COMMUNITY CALENDAR".
COMMON_VERB_WORDS = {
    "is", "are", "was", "were", "be", "been", "being",
    "has", "have", "had", "does", "did", "do",
    "will", "would", "can", "could", "should", "may", "might", "must",
    "says", "said", "wins", "won", "loses", "lost", "cuts", "cut",
    "raises", "raised", "hikes", "hiked", "slashes", "slashed",
    "announces", "announced", "launches", "launched", "dies", "died",
    "kills", "killed", "bans", "banned", "approves", "approved",
    "rejects", "rejected", "signs", "signed", "passes", "passed",
    "confirms", "confirmed", "reports", "reported", "claims", "claimed",
    "plans", "planned", "warns", "warned", "vows", "vowed", "calls", "called",
    "meets", "met", "visits", "visited", "attacks", "attacked",
    "strikes", "struck", "suggests", "suggested", "accelerates",
    "accelerated", "expands", "expanded", "returns", "returned",
    "hosts", "hosted", "sets", "set", "hits", "hit", "faces", "faced",
    "sells", "sold", "buys", "bought", "rises", "rose", "falls", "fell",
    "drops", "dropped", "gains", "gained", "leads", "led",
}


def _looks_like_verb(word: str) -> bool:
    """Weak suffix heuristic for words not in COMMON_VERB_WORDS - only meant
    to reduce false positives on titles using a less common verb, not to be
    a real POS tagger."""
    w = word.lower()
    return len(w) >= 5 and (w.endswith("ed") or w.endswith("ing") or w.endswith("izes") or w.endswith("ises"))


def is_likely_non_content(title: str) -> tuple[bool, str]:
    """Pre-filter: True (with a reason) if `title` looks like an obvious
    section label / non-news junk rather than actual news content, and
    should be skipped before any Ollama call. Returns (False, "") for
    anything not clearly junk - false negatives are expected and fine (the
    grounding check below is the real safeguard); false positives here would
    silently drop real content, so this stays deliberately conservative."""
    stripped = html.unescape(title.strip())
    if not stripped:
        return True, "empty title"

    lower = stripped.lower()
    for pattern in JUNK_KEYWORD_PATTERNS:
        if pattern in lower:
            return True, f"matched junk keyword {pattern!r}"

    words = re.findall(r"[A-Za-z']+", stripped)
    has_lower = any(c.islower() for c in stripped)
    if len(words) >= 2 and not has_lower:
        return True, "all-caps with no sentence structure"

    has_digit = bool(re.search(r"\d", stripped))
    has_verb = any(w.lower() in COMMON_VERB_WORDS or _looks_like_verb(w) for w in words)
    if len(words) <= 5 and not has_digit and not has_verb:
        return True, "very short, no verb, no numbers"

    return False, ""


def extract_numbers(text: str) -> list[str]:
    """Every distinct numeric token (percentage, currency amount, bare
    number, year) in `text`, normalized by stripping thousands-separator
    commas so "3,000" and "3000" compare equal. HTML-unescaped first - an
    undecoded entity like "&#x2013;" contains a spurious digit run ("2013")
    that isn't a real number at all (see module docstring)."""
    return [m.replace(",", "") for m in NUMBER_PATTERN.findall(html.unescape(text))]


def is_grounded(fact_text: str, source_text: str) -> tuple[bool, list[str]]:
    """Checks every number stated in `fact_text` traces back to `source_text`
    (the original title given to the model), verbatim or near-verbatim (a
    fact's "18%" matches a source's "18%" or "18 percent" or "18", and a
    trailing "%" is optional on either side - real headlines write
    percentages inconsistently). Returns (grounded, ungrounded_numbers); a
    non-empty ungrounded_numbers means the fact contains at least one figure
    the source never mentioned and it should be rejected as likely
    fabricated. A fact with no numeric claims at all is considered grounded
    by default - this check specifically targets fabricated NUMBERS, not
    text-level hallucination in general (see module docstring).

    This is a lightweight substring check, not rigorous entity linking - a
    short, coincidentally-matching bare number elsewhere in a long source
    could in principle pass as "grounded" when it isn't really the same
    figure. Acceptable for GDELT bulk titles (short, single-sentence) but
    worth revisiting if this is ever applied to longer source text."""
    fact_numbers = extract_numbers(fact_text)
    if not fact_numbers:
        return True, []

    # Compare against the source's OWN extracted-and-normalized numbers, not a raw
    # substring search against the unnormalized source text - a raw substring check
    # was confirmed (during live ingestion spot-checking) to falsely reject facts
    # whenever the source formatted its number with a thousands-separator comma
    # ("5,000 migrants") that the fact's normalized "5000" could never match as a
    # substring. Extracting from both sides the same way makes the comparison
    # consistent regardless of either side's comma/decimal formatting.
    source_numbers = set(extract_numbers(source_text))
    ungrounded = []
    for num in fact_numbers:
        bare = num.rstrip("%")
        if num in source_numbers or bare in source_numbers:
            continue
        ungrounded.append(num)
    return (len(ungrounded) == 0), ungrounded
