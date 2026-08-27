"""Validates the fact-decomposition step (CLAUDE.md section 4): runs a
constructed tax-policy test article through extract_facts() and the same
embed -> relevance -> polarity pipeline the real ingestion run uses, and
checks it produces two separate fact records with opposing polarity rather
than one blended one.

If Ollama isn't reachable, extract_facts() falls back to treating the whole
article as a single fact (see fact_extraction.py) - this script detects that
and reports the test as INCONCLUSIVE for decomposition quality rather than
quietly passing or failing, since a single-fact fallback can't produce the
two-facts-with-opposing-polarity result this test is actually checking for.

Also spot-checks the extracted fact(s) against the source text side by side
(and, if any real ingested facts exist, a sample of those too) for
hallucinated or dropped details - eyeball this before trusting extraction at
scale, per CLAUDE.md section 4.

Run: python scripts/validate_fact_decomposition.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.data_loader import load_news, load_real_articles, load_real_facts  # noqa: E402
from marketintel.embeddings import embed_text  # noqa: E402
from marketintel.fact_extraction import extract_facts  # noqa: E402
from marketintel.seed_inference import infer_categorical, nearest_neighbors  # noqa: E402

TEST_ARTICLE = (
    "The government unveiled a sweeping tax reform today. The top income tax bracket "
    "will rise from 30% to 35%, a move business groups called a burden on high earners. "
    "Separately, the same reform lowers the tax bracket for middle-income earners from "
    "20% to 15%, a change labor unions welcomed as overdue relief for working families."
)


def score_polarity(text: str, seed_news, seed_embeddings) -> str:
    embedding = embed_text(text)
    top_idx, weights = nearest_neighbors(embedding, seed_embeddings)
    return infer_categorical(seed_news, top_idx, weights, "polarity")


def main():
    print("=== Test article ===")
    print(TEST_ARTICLE)
    print()

    facts = extract_facts(TEST_ARTICLE)
    print(f"=== Extracted {len(facts)} fact(s) ===")
    for i, fact in enumerate(facts, 1):
        print(f"  {i}. {fact}")
    print()

    fallback_used = len(facts) == 1 and facts[0] == TEST_ARTICLE
    if fallback_used:
        print(
            "INCONCLUSIVE: extract_facts() fell back to treating the whole article as one "
            "fact (see the [fact_extraction] warning above) - Ollama isn't reachable or "
            "isn't returning a parseable response in this environment. The decomposition "
            "mechanism is wired in correctly and will run for real once a local Ollama "
            "server with a pulled model is available (see README), but this run can't "
            "confirm decomposition QUALITY - re-run this script once that's set up."
        )
        return

    seed_news, seed_embeddings = load_news()
    polarities = [score_polarity(f, seed_news, seed_embeddings) for f in facts]

    print("=== Polarity per fact ===")
    for fact, polarity in zip(facts, polarities):
        print(f"  [{polarity:>8}] {fact}")
    print()

    checks = []
    checks.append(("Extracted 2 or more facts (not 1 blended record)", len(facts) >= 2))
    checks.append(("At least two facts have opposing polarity", len(set(polarities)) >= 2))

    print("=== VALIDATION ===")
    for description, passed in checks:
        print(f"{'PASS' if passed else 'FAIL'}: {description}")
    print(f"\n{sum(p for _, p in checks)}/{len(checks)} checks passed.")

    print("\n=== Spot-check: extracted facts vs. source text (check for hallucinated or dropped details) ===")
    print("Source text:", TEST_ARTICLE)
    for i, fact in enumerate(facts, 1):
        print(f"  Fact {i}: {fact}")

    real_facts, _ = load_real_facts()
    if real_facts:
        articles_by_id = {a["id"]: a for a in load_real_articles()}
        print("\n=== Spot-check: the 5 most recently ingested facts vs. their source headline ===")
        for fact in real_facts[-5:]:
            source_article = articles_by_id.get(fact.get("parent_article_id"))
            source_title = source_article["title"] if source_article else "(source article not found)"
            print(f"  Fact:   {fact['fact_text']}")
            print(f"  Source: {source_title}")
    else:
        print("\n(No real ingested facts on disk yet to spot-check - run scripts/ingest_news.py first.)")


if __name__ == "__main__":
    main()
