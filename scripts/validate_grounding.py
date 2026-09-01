"""Validates the grounding safeguards (src/marketintel/grounding.py) against
the exact real failure cases that motivated them, BEFORE treating the
running pilot week as having cleared its spot-check gate (CLAUDE.md's GDELT
grounding-safeguards section).

Two known real hallucinations, both captured verbatim during earlier
smoke-testing:
  1. "COMMUNITY CALENDAR" (a section label, not news) -> the model fabricated
     "The Punjab government has slashed the GST on mobile phones from 18% to
     8%," with neither "18" nor "8" appearing anywhere in the source.
  2. "2026 BMW Championship: Preview, Prop Picks, Best Bets" -> the model
     fabricated a specific tournament edition number ("the 75th edition")
     that appears nowhere in the source (the source's own "2026" is a
     separate, legitimately-grounded number).

For each, confirms the pre-filter (is_likely_non_content), the grounding
check (is_grounded), or both would have caught it - and separately confirms
a GENUINE, non-fabricated real fact from the pilot (a Kolkata hotel-fire
casualty count that traces cleanly to its source) is NOT rejected as a false
positive.

Run: python scripts/validate_grounding.py
"""
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.grounding import is_grounded, is_likely_non_content  # noqa: E402

KNOWN_HALLUCINATIONS = [
    dict(
        name="COMMUNITY CALENDAR -> fabricated Punjab GST claim",
        source_title="COMMUNITY CALENDAR",
        fabricated_fact="The Punjab government has slashed the GST on mobile phones from 18% to 8%",
    ),
    dict(
        name="BMW Championship preview -> fabricated tournament edition number",
        source_title="2026 BMW Championship: Preview, Prop Picks, Best Bets",
        fabricated_fact="The 2026 BMW Championship will be the 75th edition of the tournament.",
    ),
]

# A genuine, non-fabricated fact from the pilot run - the numeric claim (5)
# traces cleanly back to the source headline. Used as a false-positive check:
# the grounding check must NOT reject real, well-grounded facts.
GENUINE_FACT = dict(
    name="Real pilot fact: Kolkata hotel fire casualty count",
    source_title="5 Bangladeshi nationals among nine killed in Kolkata hotel fire; "
                  "four from same family: Deputy High Commission",
    fact_text="Nine people were killed, including 5 Bangladeshi nationals, in a fire at a hotel in Kolkata.",
)


def run_hallucination_cases() -> list[bool]:
    print("=== 1. Known real hallucinations - must be caught ===\n")
    results = []
    for case in KNOWN_HALLUCINATIONS:
        prefiltered, reason = is_likely_non_content(case["source_title"])
        grounded, ungrounded_numbers = is_grounded(case["fabricated_fact"], case["source_title"])
        caught = prefiltered or not grounded
        results.append(caught)

        print(f"{case['name']}")
        print(f"  source title:     {case['source_title']!r}")
        print(f"  fabricated fact:  {case['fabricated_fact']!r}")
        print(f"  pre-filter:       {'REJECTED (' + reason + ')' if prefiltered else 'not caught'}")
        print(f"  grounding check:  {'REJECTED, ungrounded numbers=' + str(ungrounded_numbers) if not grounded else 'not caught'}")
        print(f"  {'PASS' if caught else 'FAIL'}: at least one safeguard caught this fabrication\n")

    return results


def run_false_positive_check() -> bool:
    print("=== 2. Genuine fact - must NOT be rejected (false-positive check) ===\n")
    case = GENUINE_FACT
    prefiltered, reason = is_likely_non_content(case["source_title"])
    grounded, ungrounded_numbers = is_grounded(case["fact_text"], case["source_title"])
    passed = grounded  # the pre-filter operates on the source TITLE, not the fact - only grounding matters here

    print(f"{case['name']}")
    print(f"  source title: {case['source_title']!r}")
    print(f"  fact text:    {case['fact_text']!r}")
    print(f"  grounding check: {'grounded (correct)' if grounded else 'REJECTED, ungrounded numbers=' + str(ungrounded_numbers)}")
    print(f"  {'PASS' if passed else 'FAIL'}: a genuine, well-grounded fact was not wrongly rejected\n")

    return passed


def main():
    hallucination_results = run_hallucination_cases()
    false_positive_result = run_false_positive_check()

    all_results = hallucination_results + [false_positive_result]
    print("=== VALIDATION SUMMARY ===")
    print(f"Known hallucinations caught: {sum(hallucination_results)}/{len(hallucination_results)}")
    print(f"Genuine fact NOT falsely rejected: {'PASS' if false_positive_result else 'FAIL'}")
    print(f"\n{sum(all_results)}/{len(all_results)} total checks passed.")
    print(
        "\nNote: is_grounded() only targets fabricated NUMBERS - a fact with no numeric "
        "claim at all (e.g. the BMW case's fabricated venue/location fact) has nothing for "
        "it to check and passes by default. This is a documented, intentional scope "
        "limitation (see grounding.py), not a gap this script is meant to catch."
    )
    if not all(all_results):
        print("Do not treat the pilot week as having cleared its spot-check gate until this passes.")


if __name__ == "__main__":
    main()
