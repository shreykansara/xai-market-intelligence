"""Retroactive audit: re-checks every fact currently in
data/backfill_facts.json against the grounding safeguards
(src/marketintel/grounding.py), which were added AFTER the pilot week run
started and so were never applied to facts already collected. Reports how
many would have been rejected, and prints a sample of them (alongside their
source title) for manual spot-checking - confirming they're genuinely bad,
not false positives - before the pilot week counts as having cleared its
spot-check gate (CLAUDE.md's GDELT backfill section).

ALSO samples from ACCEPTED facts (grounded=True) that contain at least one
number, specifically to check for the grounding check's own known
limitation (see grounding.py's is_grounded docstring): a "grounded" verdict
only means the number appears somewhere in the source text as a substring -
it does NOT verify the number is attached to the same subject/unit/context
as the fact's claim. A short bare number could coincidentally appear in the
source for an unrelated reason (a different quantity, a date, a score) and
still count as "grounded" under the current substring check. Each sampled
accepted fact is printed with its source title so this can be checked by
eye; the summary reports how many of the sample show this coincidental-match
pattern.

This does NOT modify data/backfill_facts.json - it's a read-only audit, not
a cleanup pass. Deciding whether to re-run the pilot with the safeguards
active, or to filter the existing store, is a separate decision for after
this audit is reviewed.

Run: python scripts/audit_grounding_retroactive.py [--sample-size N]
"""
import argparse
import json
import random
import sys
from pathlib import Path

# Decoded titles can now contain real non-ASCII characters (rupee sign, em-dash,
# etc.) that HTML-unescaping (see grounding.py) correctly restores from entity
# codes like "&#x20B9;" - Windows' default console codepage can't print a lot
# of that.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.config import BACKFILL_ARTICLES_PATH, BACKFILL_FACTS_PATH  # noqa: E402
from marketintel.grounding import extract_numbers, is_grounded, is_likely_non_content  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample-size", type=int, default=15, help="How many rejected facts to print for spot-check")
    args = parser.parse_args()

    if not BACKFILL_FACTS_PATH.exists() or not BACKFILL_ARTICLES_PATH.exists():
        print(f"{BACKFILL_FACTS_PATH} and/or {BACKFILL_ARTICLES_PATH} don't exist yet - nothing to audit.")
        return

    with open(BACKFILL_FACTS_PATH, encoding="utf-8") as f:
        facts = json.load(f)
    with open(BACKFILL_ARTICLES_PATH, encoding="utf-8") as f:
        articles = json.load(f)
    articles_by_id = {a["id"]: a for a in articles}

    print(f"Auditing {len(facts)} fact(s) from {len(articles)} article(s)...\n")

    ungrounded_rejections = []
    accepted_with_numbers = []  # grounded=True facts that DO contain a number - candidates for
                                 # the coincidental-match spot-check (facts with no numbers at
                                 # all have nothing to check and aren't interesting here)
    noncontent_rejections = []  # articles whose title would have been pre-filtered (informational only -
                                 # these facts were already stored under the old pipeline, since the
                                 # pre-filter didn't exist yet when they were collected)
    seen_noncontent_titles = set()

    for fact in facts:
        article = articles_by_id.get(fact.get("parent_article_id"))
        source_title = article["title"] if article else None
        if source_title is None:
            continue  # shouldn't happen, but don't crash the audit over a missing link

        if source_title not in seen_noncontent_titles:
            is_junk, reason = is_likely_non_content(source_title)
            if is_junk:
                noncontent_rejections.append({"title": source_title, "reason": reason})
            seen_noncontent_titles.add(source_title)

        grounded, ungrounded_numbers = is_grounded(fact["fact_text"], source_title)
        if not grounded:
            ungrounded_rejections.append({
                "fact_id": fact["id"],
                "fact_text": fact["fact_text"],
                "source_title": source_title,
                "ungrounded_numbers": ungrounded_numbers,
            })
        elif extract_numbers(fact["fact_text"]):
            accepted_with_numbers.append({
                "fact_id": fact["id"],
                "fact_text": fact["fact_text"],
                "source_title": source_title,
                "numbers": extract_numbers(fact["fact_text"]),
            })

    print("=== SUMMARY ===")
    print(f"Facts that would be rejected by the grounding check (ungrounded numbers): "
          f"{len(ungrounded_rejections)}/{len(facts)} ({100 * len(ungrounded_rejections) / max(len(facts), 1):.2f}%)")
    print(f"Accepted facts containing a number (candidates for the coincidental-match check): "
          f"{len(accepted_with_numbers)}/{len(facts)}")
    print(f"Distinct source titles that would have been pre-filtered as non-content: "
          f"{len(noncontent_rejections)}/{len(seen_noncontent_titles)} "
          f"({100 * len(noncontent_rejections) / max(len(seen_noncontent_titles), 1):.2f}%)")

    print(f"\n=== Sample of {min(args.sample_size, len(ungrounded_rejections))} rejected facts "
          f"(spot-check: are these genuinely bad, or false positives?) ===\n")
    for rejected in ungrounded_rejections[:args.sample_size]:
        print(f"  fact:              {rejected['fact_text']!r}")
        print(f"  source title:      {rejected['source_title']!r}")
        print(f"  ungrounded number(s): {rejected['ungrounded_numbers']}")
        print()

    print(f"=== Sample of {min(args.sample_size, len(accepted_with_numbers))} ACCEPTED facts "
          f"(spot-check: is each number's context/unit/subject actually the same as the source's, "
          f"or just a coincidental bare-number match?) ===\n")
    rng = random.Random(42)
    accepted_sample = rng.sample(accepted_with_numbers, min(args.sample_size, len(accepted_with_numbers)))
    for accepted in accepted_sample:
        print(f"  fact:         {accepted['fact_text']!r}")
        print(f"  source title: {accepted['source_title']!r}")
        print(f"  number(s):    {accepted['numbers']}")
        print()
    print(
        "(Manually judge each pair above: does the source title state that number for the SAME "
        "subject/unit/context the fact claims, or does it just happen to contain that digit "
        "sequence for an unrelated reason? See the module docstring for why this is a real, "
        "documented limitation of a substring-based grounding check.)\n"
    )

    if noncontent_rejections:
        print(f"=== Sample of {min(args.sample_size, len(noncontent_rejections))} titles the pre-filter "
              f"would have rejected before decomposition ===\n")
        for rejected in noncontent_rejections[:args.sample_size]:
            print(f"  title: {rejected['title']!r}  (reason: {rejected['reason']})")


if __name__ == "__main__":
    main()
