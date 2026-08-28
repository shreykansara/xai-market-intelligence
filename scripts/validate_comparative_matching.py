"""Validates comparative_matching.py (CLAUDE.md's GDELT bulk backfill section)
BEFORE it ever touches real backfill data, per instructions:

  1. Three hand-picked, independently verifiable real rate/tax changes - confirm
     the mechanism retrieves the correct prior value and computes the correct
     direction for each:
       - India: GST on mobile phones raised from 12% to 18% (GST Council, April 2020).
       - India: RBI repo rate cut from 6.50% to 6.25% (Monetary Policy Committee, Feb 2025).
       - UK: standard VAT rate raised from 17.5% to 20% (effective Jan 2011).
  2. A deliberately similar-but-different pair - two different tax categories
     (mobile phones vs. textiles), both GST, both India, phrased as near-
     identically as possible, changing around the same time - confirm the
     entity check stops them from cross-matching (a textile-GST fact must NOT
     be compared against a mobile-phone-GST prior just because the
     surrounding language is nearly identical). Run twice: (2a) with real
     embeddings of the closest-phrasing pair found, reporting their actual
     cosine similarity honestly (it turned out to land just under the match
     threshold on its own for this specific phrasing - see the printed note);
     and (2b) a synthetic worst case that forces similarity to the maximum
     (1.0, by reusing one embedding for both facts) so the entity check is
     unambiguously the only thing standing between a match and a rejection,
     proving it's load-bearing rather than redundant with the similarity gate.

Run: python scripts/validate_comparative_matching.py
"""
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.comparative_matching import resolve_comparative_fact  # noqa: E402
from marketintel.config import COMPARATIVE_MATCH_SIMILARITY_THRESHOLD  # noqa: E402
from marketintel.embeddings import embed_text  # noqa: E402

EARLIER = datetime(2020, 1, 1, tzinfo=timezone.utc)
LATER = EARLIER + timedelta(days=90)


def make_stored_fact(fact_id: str, text: str, entities: list[str], published: datetime) -> dict:
    return {"id": fact_id, "fact_text": text, "entities": entities, "published": published.isoformat()}


REAL_RATE_CHANGE_CASES = [
    dict(
        name="India GST on mobile phones (12% -> 18%, GST Council, Apr 2020)",
        prior_text="GST on mobile phones is set at 12%",
        prior_entities=["GST on mobile phones", "India"],
        current_text="GST on mobile phones is set at 18%",
        current_entities=["GST on mobile phones", "India"],
        expected_direction="increase",
    ),
    dict(
        name="India RBI repo rate (6.50% -> 6.25%, MPC, Feb 2025)",
        prior_text="The Reserve Bank of India's repo rate is 6.50%",
        prior_entities=["Reserve Bank of India", "repo rate"],
        current_text="The Reserve Bank of India's repo rate is 6.25%",
        current_entities=["Reserve Bank of India", "repo rate"],
        expected_direction="decrease",
    ),
    dict(
        name="UK standard VAT rate (17.5% -> 20%, effective Jan 2011)",
        prior_text="The UK standard VAT rate is 17.5%",
        prior_entities=["UK", "VAT"],
        current_text="The UK standard VAT rate is 20%",
        current_entities=["UK", "VAT"],
        expected_direction="increase",
    ),
]


def run_real_rate_change_cases() -> list[bool]:
    print("=== 1. Real, independently verifiable rate/tax changes ===\n")
    results = []
    for case in REAL_RATE_CHANGE_CASES:
        prior_embedding = embed_text(case["prior_text"])
        prior_fact = make_stored_fact("prior_1", case["prior_text"], case["prior_entities"], EARLIER)

        current_embedding = embed_text(case["current_text"])
        result = resolve_comparative_fact(
            fact_text=case["current_text"],
            entities=case["current_entities"],
            embedding=current_embedding,
            published=LATER,
            stored_facts=[prior_fact],
            stored_embeddings=[prior_embedding],
        )

        matched_correctly = result["matched_prior_fact_id"] == "prior_1"
        direction_correct = result["computed_direction"] == case["expected_direction"]
        passed = matched_correctly and direction_correct
        results.append(passed)

        print(f"{case['name']}")
        print(f"  prior:   {case['prior_text']!r}")
        print(f"  current: {case['current_text']!r}")
        print(f"  matched_prior_fact_id={result['matched_prior_fact_id']} "
              f"similarity={result['match_similarity']:.4f} "
              f"computed_direction={result['computed_direction']}")
        print(f"  {'PASS' if passed else 'FAIL'}: retrieved the correct prior value and direction "
              f"(expected {case['expected_direction']})\n")

    return results


def run_similar_but_different_case() -> bool:
    print("=== 2a. Similar-but-different pair, natural phrasing (must NOT cross-match) ===\n")

    mobile_text = "Officials confirmed the GST slab applicable to mobile phones is now 18 percent nationwide"
    mobile_entities = ["GST on mobile phones", "India"]
    mobile_embedding = embed_text(mobile_text)
    mobile_prior = make_stored_fact("mobile_prior", mobile_text, mobile_entities, EARLIER)

    textile_text = "Officials confirmed the GST slab applicable to textiles is now 18 percent nationwide"
    textile_entities = ["GST on textiles", "India"]
    textile_embedding = embed_text(textile_text)

    raw_similarity = float(mobile_embedding @ textile_embedding)
    print(f"Stored prior fact: {mobile_text!r} (entities={mobile_entities})")
    print(f"Incoming fact:      {textile_text!r} (entities={textile_entities})")
    print(f"Raw embedding cosine similarity between the two (near-identical phrasing, only the "
          f"taxed good differs): {raw_similarity:.4f}")

    result = resolve_comparative_fact(
        fact_text=textile_text,
        entities=textile_entities,
        embedding=textile_embedding,
        published=LATER,
        stored_facts=[mobile_prior],
        stored_embeddings=[mobile_embedding],
    )

    did_not_cross_match_a = result["matched_prior_fact_id"] is None
    print(f"matched_prior_fact_id={result['matched_prior_fact_id']} "
          f"match_similarity={result['match_similarity']:.4f} "
          f"computed_direction={result['computed_direction']}")

    if raw_similarity >= COMPARATIVE_MATCH_SIMILARITY_THRESHOLD and did_not_cross_match_a:
        note = "genuinely adversarial here: similarity alone would have matched, but the entity check blocked it"
    else:
        note = (f"similarity ({raw_similarity:.4f}) already fell short of the "
                f"{COMPARATIVE_MATCH_SIMILARITY_THRESHOLD} threshold for this specific phrasing, so this pair alone "
                f"doesn't prove the entity check is load-bearing - see test 2b for that")
    print(f"{'PASS' if did_not_cross_match_a else 'FAIL'}: did not cross-match ({note})\n")

    print("=== 2b. Synthetic worst case: IDENTICAL embedding, different entities ===\n")
    print("Forces similarity to 1.0 (the theoretical maximum) so the only thing standing between a "
          "match and a rejection is the entity check - proves it's load-bearing rather than redundant "
          "with the similarity gate, regardless of what any specific real-world phrasing happens to embed to.\n")

    identical_prior = make_stored_fact("identical_prior", mobile_text, mobile_entities, EARLIER)
    result_b = resolve_comparative_fact(
        fact_text=textile_text,
        entities=textile_entities,
        embedding=mobile_embedding,  # deliberately reuse the SAME embedding - similarity will be 1.0
        published=LATER,
        stored_facts=[identical_prior],
        stored_embeddings=[mobile_embedding],
    )
    did_not_cross_match_b = result_b["matched_prior_fact_id"] is None
    print(f"matched_prior_fact_id={result_b['matched_prior_fact_id']} "
          f"match_similarity={result_b['match_similarity']:.4f} computed_direction={result_b['computed_direction']}")
    print(f"{'PASS' if did_not_cross_match_b else 'FAIL'}: did not cross-match even at similarity=1.0 "
          f"(entity check is genuinely load-bearing)\n")

    return did_not_cross_match_a and did_not_cross_match_b


def main():
    rate_change_results = run_real_rate_change_cases()
    cross_match_result = run_similar_but_different_case()

    all_results = rate_change_results + [cross_match_result]
    print("=== VALIDATION SUMMARY ===")
    print(f"Real rate/tax change cases: {sum(rate_change_results)}/{len(rate_change_results)} passed")
    print(f"Similar-but-different (no cross-match) case: {'PASS' if cross_match_result else 'FAIL'}")
    print(f"\n{sum(all_results)}/{len(all_results)} total checks passed.")
    if not all(all_results):
        print("Do not run this mechanism against real backfill data until every check above passes.")


if __name__ == "__main__":
    main()
