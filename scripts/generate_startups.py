"""Generate 20 fabricated LPU-based startups (identity + CVP only - no ground-truth
sensitivity profile), link each to 3-5 justifying news articles from data/news.json,
embed each CVP, and save everything to data/.

The PESTLE/Porter's sensitivity profile is no longer hand-authored here: it's
derived later, from a fabricated profit history, by simulate_profit_history.py +
derive_sensitivity_profiles.py. Article linking still uses the hidden generation
template (see hidden_ground_truth.py) to pick plausible justifying articles, but
that template's actual values are never written to data/startups.json.

Must run AFTER generate_news.py (needs data/news.json to pick linked articles).
Run: python scripts/generate_startups.py
"""
import json
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from marketintel.config import (  # noqa: E402
    DATA_DIR,
    NEWS_PATH,
    PESTLE_DIMS,
    PORTERS_DIMS,
    STARTUP_EMBEDDINGS_PATH,
    STARTUPS_PATH,
)
from marketintel.embeddings import embed_texts  # noqa: E402

from hidden_ground_truth import HIDDEN_TEMPLATES  # noqa: E402

SEED = 7

STARTUPS = [
    dict(
        name="RupeeRail", domain="fintech",
        cvp=(
            "RupeeRail gives gig and blue-collar workers instant, collateral-free micro-loans "
            "underwritten from real-time earnings data, repaid automatically as they get paid. "
            "We plug directly into gig platforms' payout APIs so workers never have to fill out a loan form."
        ),
    ),
    dict(
        name="LedgerLoop", domain="fintech / SaaS",
        cvp=(
            "LedgerLoop is GST-compliant accounting software built for India's SMEs, auto-filing returns "
            "and reconciling bank statements without an accountant. Founders can close their books in "
            "minutes instead of days."
        ),
    ),
    dict(
        name="CoverNest", domain="fintech / insurtech",
        cvp=(
            "CoverNest sells bite-sized health and crop micro-insurance policies through a WhatsApp "
            "chatbot, priced from as little as fifty rupees a month for families with no prior insurance "
            "history. We underwrite using alternative data instead of paperwork."
        ),
    ),
    dict(
        name="SkillSprout", domain="edtech",
        cvp=(
            "SkillSprout teaches job-ready digital skills in Punjabi, Hindi, and six other regional "
            "languages through short, mobile-first video courses. We partner with local ITIs and "
            "placement cells to guarantee interviews on completion."
        ),
    ),
    dict(
        name="CampusOS", domain="edtech / SaaS",
        cvp=(
            "CampusOS is a single operations platform that runs admissions, fee collection, hostel "
            "allotment, and attendance for mid-size Indian universities. We replace five disconnected "
            "legacy systems with one dashboard IT teams actually enjoy using."
        ),
    ),
    dict(
        name="ExamAnt", domain="edtech",
        cvp=(
            "ExamAnt lets coaching institutes run secure, AI-proctored mock tests for competitive exams "
            "like NEET and JEE at a fraction of the cost of physical test centers. Instant, item-level "
            "analytics tell students exactly which concepts to revise."
        ),
    ),
    dict(
        name="Krishimitra", domain="agritech",
        cvp=(
            "Krishimitra combines a low-cost soil sensor with a Punjabi-language advisory app to tell "
            "farmers exactly when to irrigate and fertilize their wheat and rice fields. Early users cut "
            "water usage by a third without losing yield."
        ),
    ),
    dict(
        name="AgriChain Direct", domain="agritech",
        cvp=(
            "AgriChain Direct connects Punjab farmers straight to urban retail chains, cutting out three "
            "layers of mandi middlemen and getting farmers 15-20% better prices. Retailers get fresher "
            "produce with full traceability back to the farm."
        ),
    ),
    dict(
        name="FarmYield Finance", domain="agritech / fintech",
        cvp=(
            "FarmYield Finance underwrites crop loans using satellite imagery and weather data instead of "
            "land titles, so smallholder farmers without formal collateral can still get affordable "
            "credit. Repayment schedules flex automatically around harvest cycles."
        ),
    ),
    dict(
        name="Wattlefy", domain="D2C hardware",
        cvp=(
            "Wattlefy is a plug-and-play smart energy monitor that shows Indian households exactly which "
            "appliances are driving up their electricity bill, in real time on their phone. We've helped "
            "early customers cut their bills by up to 18%."
        ),
    ),
    dict(
        name="PureDrop", domain="D2C hardware",
        cvp=(
            "PureDrop builds affordable, locally manufactured water purifiers designed for the hard, "
            "high-TDS groundwater common across Punjab and neighboring states. We sell direct-to-consumer "
            "online, skipping the usual dealer markup."
        ),
    ),
    dict(
        name="MotoCharge", domain="D2C hardware",
        cvp=(
            "MotoCharge makes home and street-corner charging docks built specifically for India's "
            "exploding two-wheeler EV market. Our modular design lets a single dock serve three different "
            "scooter brands out of the box."
        ),
    ),
    dict(
        name="DeskLoop", domain="SaaS",
        cvp=(
            "DeskLoop is payroll and HR software built for how Indian SMEs actually run - full PF, ESI, "
            "and TDS compliance out of the box, with a WhatsApp-first employee experience instead of yet "
            "another app to install."
        ),
    ),
    dict(
        name="RouteIQ", domain="SaaS / logistics",
        cvp=(
            "RouteIQ plugs into any delivery fleet's existing app and re-optimizes routes in real time "
            "using live traffic and weather data, cutting fuel spend by up to 12%. No hardware, no fleet "
            "replacement - just a lighter API integration."
        ),
    ),
    dict(
        name="ClauseCraft", domain="SaaS / legaltech",
        cvp=(
            "ClauseCraft uses AI to flag risky clauses in vendor and employment contracts in under a "
            "minute, giving founders lawyer-grade review without the lawyer-grade bill. We've reviewed "
            "over ten thousand contracts across seed-stage startups."
        ),
    ),
    dict(
        name="PulseDesk", domain="SaaS",
        cvp=(
            "PulseDesk is a customer support helpdesk that uses AI to triage, tag, and draft first-"
            "response replies to tickets automatically, cutting average resolution time in half. We're "
            "built for lean support teams who can't hire their way out of ticket backlogs."
        ),
    ),
    dict(
        name="VitalsBridge", domain="healthtech",
        cvp=(
            "VitalsBridge pairs a low-cost wearable with a monitoring dashboard so clinics can track "
            "chronic patients' vitals between visits and catch problems before they become emergencies. "
            "We're already integrated with three hospital chains in North India."
        ),
    ),
    dict(
        name="TeleCare Punjab", domain="healthtech",
        cvp=(
            "TeleCare Punjab connects patients in rural Punjab to qualified doctors over voice and video "
            "in Punjabi, with a nurse-assisted kiosk model for patients who don't own a smartphone. We "
            "already run kiosks in over 40 villages."
        ),
    ),
    dict(
        name="MedStock AI", domain="healthtech / SaaS",
        cvp=(
            "MedStock AI forecasts hospital pharmacy demand down to the SKU level, so procurement teams "
            "stop overstocking slow-moving drugs while avoiding stockouts on critical ones. One mid-size "
            "hospital cut wastage by 22% in its first quarter with us."
        ),
    ),
    dict(
        name="GlowLine Cosmeceuticals", domain="healthtech / D2C",
        cvp=(
            "GlowLine sells dermatologist-formulated skincare made and tested for Indian skin types and "
            "climate, sold directly online without the markup of international brands. Every batch is "
            "manufactured in our own FDA-registered facility."
        ),
    ),
]


def dims_by_magnitude(hidden: dict):
    items = []
    for d in PESTLE_DIMS:
        items.append(("pestle_scores", d, hidden["pestle"][d]))
    for d in PORTERS_DIMS:
        items.append(("porters_scores", d, hidden["porters"][d]))
    items.sort(key=lambda x: -abs(x[2]))
    return items


def pick_linked_articles(hidden: dict, news: list[dict], rng: random.Random) -> list[str]:
    dims = dims_by_magnitude(hidden)[:3]
    linked: list[str] = []
    for i, (score_field, dim, value) in enumerate(dims):
        desired_polarity = "positive" if value >= 0 else "negative"
        candidates = [a for a in news if a[score_field][dim] > 0.55]
        matching = [a for a in candidates if a["polarity"] == desired_polarity]
        pool = matching if matching else candidates
        if not pool:
            continue
        num_pick = 2 if i < 2 else 1
        picks = rng.sample(pool, k=min(num_pick, len(pool)))
        for p in picks:
            if p["id"] not in linked:
                linked.append(p["id"])

    # Fallback: ensure at least 3 links using the single most dominant dimension.
    if len(linked) < 3 and dims:
        score_field, dim, _ = dims[0]
        ranked = sorted(news, key=lambda a: -a[score_field][dim])[:30]
        for a in ranked:
            if len(linked) >= 3:
                break
            if a["id"] not in linked:
                linked.append(a["id"])

    return linked[:5]


def main():
    rng = random.Random(SEED)

    with open(NEWS_PATH, encoding="utf-8") as f:
        news = json.load(f)

    startups = []
    for i, s in enumerate(STARTUPS):
        hidden = HIDDEN_TEMPLATES[s["name"]]
        linked_ids = pick_linked_articles(hidden, news, rng)
        startups.append({
            "id": f"startup_{i + 1:02d}",
            "name": s["name"],
            "domain": s["domain"],
            "cvp": s["cvp"],
            "linked_article_ids": linked_ids,
        })

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(STARTUPS_PATH, "w", encoding="utf-8") as f:
        json.dump(startups, f, indent=2)
    print(f"Wrote {STARTUPS_PATH} ({len(startups)} startups, no sensitivity profile yet)")

    print("Embedding startup CVPs...")
    embeddings = embed_texts([s["cvp"] for s in startups])
    np.save(STARTUP_EMBEDDINGS_PATH, embeddings)
    print(f"Wrote {STARTUP_EMBEDDINGS_PATH} shape={embeddings.shape}")


if __name__ == "__main__":
    main()
