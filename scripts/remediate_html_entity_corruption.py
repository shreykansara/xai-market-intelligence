"""One-off remediation for facts/articles collected before gdelt_bulk.py's
HTML-entity-decoding fix (see CLAUDE.md's GDELT backfill section). Two
distinct problems, handled differently:

1. Article-level: the relevance gate (and, separately, the non-content
   pre-filter added afterward) both ran on the RAW, entity-corrupted title.
   For 5 of the 39 entity-affected articles, re-checking against the CLEAN
   (HTML-unescaped) title flips the outcome - either the pre-filter now
   correctly identifies it as non-content, or the relevance score drops
   below threshold. These 5 articles (9 resulting facts) would not exist at
   all under today's pipeline, so they're removed here, not just re-scored -
   keeping them (even correctly re-embedded) would misrepresent what the
   fixed pipeline actually decides. Logged to backfill_excluded.jsonl /
   backfill_noncontent.jsonl exactly like a normal exclusion, not silently
   dropped.

2. Fact-level: for the remaining ~33 affected articles that still legitimately
   belong in the store, their FACTS' own embeddings (used for relevance/
   polarity/scope) come from fact_text, not the article title - and
   fact_text only carried the raw entity artifact through in one single case
   (already covered by removal #1 above, since that article's title also
   failed the pre-filter). So no other fact-level re-embedding is needed;
   this script only re-writes the STORED article title field to its clean,
   decoded form for data hygiene - matching what a fresh run would now
   produce - without touching any fact's already-correct scores.

Read CLAUDE.md before re-running this - it's a one-time fix for a specific,
already-diagnosed corruption, not a general-purpose cleanup tool.

Run: python scripts/remediate_html_entity_corruption.py [--dry-run]
"""
import argparse
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.atomic_io import atomic_write_json, atomic_write_npy  # noqa: E402
from marketintel.config import (  # noqa: E402
    BACKFILL_ARTICLES_PATH,
    BACKFILL_EXCLUDED_LOG_PATH,
    BACKFILL_FACT_EMBEDDINGS_PATH,
    BACKFILL_FACTS_PATH,
    BACKFILL_NONCONTENT_LOG_PATH,
)
from marketintel.data_loader import load_news  # noqa: E402
from marketintel.embeddings import embed_text  # noqa: E402
from marketintel.grounding import is_likely_non_content  # noqa: E402
from marketintel.seed_inference import calibrate_relevance_threshold, infer_relevance, nearest_neighbors  # noqa: E402

ENTITY_PATTERN = re.compile(r"&#?\w+;")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Report what would change without writing anything")
    args = parser.parse_args()

    with open(BACKFILL_ARTICLES_PATH, encoding="utf-8") as f:
        articles = json.load(f)
    with open(BACKFILL_FACTS_PATH, encoding="utf-8") as f:
        facts = json.load(f)
    fact_embeddings = list(np.load(BACKFILL_FACT_EMBEDDINGS_PATH))

    seed_news, seed_embeddings = load_news()
    threshold = calibrate_relevance_threshold(seed_news)

    affected = [a for a in articles if ENTITY_PATTERN.search(a["title"])]
    print(f"{len(affected)} articles have a raw HTML entity in their stored title.\n")

    remove_article_ids = set()
    title_updates = {}  # article_id -> clean title (for ones we KEEP)
    now = datetime.now(timezone.utc)

    for a in affected:
        clean_title = html.unescape(a["title"])
        if clean_title == a["title"]:
            continue

        junk, reason = is_likely_non_content(clean_title)
        emb = embed_text(clean_title)
        top_idx, w = nearest_neighbors(emb, seed_embeddings)
        rel = max(infer_relevance(seed_news, top_idx, w).values())
        would_exist = (not junk) and (rel >= threshold)

        if would_exist:
            title_updates[a["id"]] = clean_title
        else:
            remove_article_ids.add(a["id"])
            print(f"REMOVING {a['id']} {clean_title!r} (junk={junk} reason={reason!r}, "
                  f"clean_relevance={rel:.4f} threshold={threshold:.4f})")

    remove_fact_idx = [i for i, f in enumerate(facts) if f.get("parent_article_id") in remove_article_ids]
    remove_fact_ids = {facts[i]["id"] for i in remove_fact_idx}
    print(f"\n{len(remove_article_ids)} article(s) / {len(remove_fact_ids)} fact(s) to remove.")
    print(f"{len(title_updates)} article(s) getting their stored title cleaned (kept, not removed).")

    if args.dry_run:
        print("\n--dry-run: no files written.")
        return

    # Log removals exactly like a normal exclusion, before actually removing anything.
    excluded_log_entries = []
    for a in affected:
        if a["id"] not in remove_article_ids:
            continue
        clean_title = html.unescape(a["title"])
        junk, reason = is_likely_non_content(clean_title)
        if junk:
            with open(BACKFILL_NONCONTENT_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "title": clean_title, "published": a["published"], "reason": reason,
                    "logged_at": now.isoformat(), "source": "html_entity_remediation",
                }) + "\n")
        else:
            emb = embed_text(clean_title)
            top_idx, w = nearest_neighbors(emb, seed_embeddings)
            rel = max(infer_relevance(seed_news, top_idx, w).values())
            excluded_log_entries.append({
                "title": clean_title, "published": a["published"], "max_relevance": rel,
                "logged_at": now.isoformat(), "source": "html_entity_remediation",
            })
    if excluded_log_entries:
        with open(BACKFILL_EXCLUDED_LOG_PATH, "a", encoding="utf-8") as f:
            for entry in excluded_log_entries:
                f.write(json.dumps(entry) + "\n")

    # Apply title cleanups to articles we're keeping.
    for a in articles:
        if a["id"] in title_updates:
            a["title"] = title_updates[a["id"]]

    # Remove the disqualified articles and their facts (index-aligned with fact_embeddings).
    new_articles = [a for a in articles if a["id"] not in remove_article_ids]
    new_facts, new_embeddings = [], []
    for i, f in enumerate(facts):
        if f["id"] in remove_fact_ids:
            continue
        new_facts.append(f)
        new_embeddings.append(fact_embeddings[i])

    atomic_write_json(BACKFILL_ARTICLES_PATH, new_articles)
    atomic_write_json(BACKFILL_FACTS_PATH, new_facts)
    atomic_write_npy(BACKFILL_FACT_EMBEDDINGS_PATH, np.array(new_embeddings) if new_embeddings else np.empty((0, 384)))

    print(f"\nWrote {len(new_articles)} article(s) (was {len(articles)}), "
          f"{len(new_facts)} fact(s) (was {len(facts)}).")
    print(f"Removals logged to {BACKFILL_EXCLUDED_LOG_PATH} / {BACKFILL_NONCONTENT_LOG_PATH}.")


if __name__ == "__main__":
    main()
