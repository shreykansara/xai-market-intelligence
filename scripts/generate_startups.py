"""Generate 20 fabricated LPU-based startups with ground-truth PESTLE/Porter's
sensitivity profiles, link each to 3-5 justifying news articles from data/news.json,
embed each CVP, and save everything to data/.

Must run AFTER generate_news.py (needs data/news.json to pick linked articles).
Run: python scripts/generate_startups.py
"""
import json
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.config import (  # noqa: E402
    DATA_DIR,
    NEWS_PATH,
    PESTLE_DIMS,
    PORTERS_DIMS,
    STARTUP_EMBEDDINGS_PATH,
    STARTUPS_PATH,
)
from marketintel.embeddings import embed_texts  # noqa: E402

SEED = 7

STARTUPS = [
    dict(
        name="RupeeRail", domain="fintech",
        cvp=(
            "RupeeRail gives gig and blue-collar workers instant, collateral-free micro-loans "
            "underwritten from real-time earnings data, repaid automatically as they get paid. "
            "We plug directly into gig platforms' payout APIs so workers never have to fill out a loan form."
        ),
        pestle=dict(political=-60, economic=-30, social=40, technological=50, legal=-70, environmental=5),
        porters=dict(threat_new_entrants=-50, supplier_power=-20, buyer_power=-30, threat_substitutes=-40, competitive_rivalry=-60),
    ),
    dict(
        name="LedgerLoop", domain="fintech / SaaS",
        cvp=(
            "LedgerLoop is GST-compliant accounting software built for India's SMEs, auto-filing returns "
            "and reconciling bank statements without an accountant. Founders can close their books in "
            "minutes instead of days."
        ),
        pestle=dict(political=10, economic=15, social=10, technological=55, legal=65, environmental=0),
        porters=dict(threat_new_entrants=-55, supplier_power=5, buyer_power=-25, threat_substitutes=-35, competitive_rivalry=-60),
    ),
    dict(
        name="CoverNest", domain="fintech / insurtech",
        cvp=(
            "CoverNest sells bite-sized health and crop micro-insurance policies through a WhatsApp "
            "chatbot, priced from as little as fifty rupees a month for families with no prior insurance "
            "history. We underwrite using alternative data instead of paperwork."
        ),
        pestle=dict(political=-35, economic=-25, social=60, technological=45, legal=-55, environmental=-20),
        porters=dict(threat_new_entrants=-45, supplier_power=-15, buyer_power=-20, threat_substitutes=-30, competitive_rivalry=-40),
    ),
    dict(
        name="SkillSprout", domain="edtech",
        cvp=(
            "SkillSprout teaches job-ready digital skills in Punjabi, Hindi, and six other regional "
            "languages through short, mobile-first video courses. We partner with local ITIs and "
            "placement cells to guarantee interviews on completion."
        ),
        pestle=dict(political=20, economic=25, social=70, technological=50, legal=-10, environmental=0),
        porters=dict(threat_new_entrants=-50, supplier_power=5, buyer_power=-30, threat_substitutes=-40, competitive_rivalry=-55),
    ),
    dict(
        name="CampusOS", domain="edtech / SaaS",
        cvp=(
            "CampusOS is a single operations platform that runs admissions, fee collection, hostel "
            "allotment, and attendance for mid-size Indian universities. We replace five disconnected "
            "legacy systems with one dashboard IT teams actually enjoy using."
        ),
        pestle=dict(political=15, economic=10, social=35, technological=55, legal=20, environmental=0),
        porters=dict(threat_new_entrants=-40, supplier_power=0, buyer_power=-20, threat_substitutes=-30, competitive_rivalry=-45),
    ),
    dict(
        name="ExamAnt", domain="edtech",
        cvp=(
            "ExamAnt lets coaching institutes run secure, AI-proctored mock tests for competitive exams "
            "like NEET and JEE at a fraction of the cost of physical test centers. Instant, item-level "
            "analytics tell students exactly which concepts to revise."
        ),
        pestle=dict(political=0, economic=15, social=45, technological=65, legal=-15, environmental=10),
        porters=dict(threat_new_entrants=-55, supplier_power=0, buyer_power=-25, threat_substitutes=-50, competitive_rivalry=-60),
    ),
    dict(
        name="Krishimitra", domain="agritech",
        cvp=(
            "Krishimitra combines a low-cost soil sensor with a Punjabi-language advisory app to tell "
            "farmers exactly when to irrigate and fertilize their wheat and rice fields. Early users cut "
            "water usage by a third without losing yield."
        ),
        pestle=dict(political=25, economic=20, social=50, technological=55, legal=10, environmental=75),
        porters=dict(threat_new_entrants=-35, supplier_power=-40, buyer_power=-20, threat_substitutes=-25, competitive_rivalry=-30),
    ),
    dict(
        name="AgriChain Direct", domain="agritech",
        cvp=(
            "AgriChain Direct connects Punjab farmers straight to urban retail chains, cutting out three "
            "layers of mandi middlemen and getting farmers 15-20% better prices. Retailers get fresher "
            "produce with full traceability back to the farm."
        ),
        pestle=dict(political=-20, economic=45, social=35, technological=30, legal=-45, environmental=20),
        porters=dict(threat_new_entrants=-30, supplier_power=-25, buyer_power=-35, threat_substitutes=-20, competitive_rivalry=-40),
    ),
    dict(
        name="FarmYield Finance", domain="agritech / fintech",
        cvp=(
            "FarmYield Finance underwrites crop loans using satellite imagery and weather data instead of "
            "land titles, so smallholder farmers without formal collateral can still get affordable "
            "credit. Repayment schedules flex automatically around harvest cycles."
        ),
        pestle=dict(political=-30, economic=-35, social=55, technological=50, legal=-50, environmental=-65),
        porters=dict(threat_new_entrants=-40, supplier_power=-10, buyer_power=-20, threat_substitutes=-30, competitive_rivalry=-35),
    ),
    dict(
        name="Wattlefy", domain="D2C hardware",
        cvp=(
            "Wattlefy is a plug-and-play smart energy monitor that shows Indian households exactly which "
            "appliances are driving up their electricity bill, in real time on their phone. We've helped "
            "early customers cut their bills by up to 18%."
        ),
        pestle=dict(political=-55, economic=-60, social=30, technological=40, legal=-25, environmental=45),
        porters=dict(threat_new_entrants=-30, supplier_power=-70, buyer_power=-35, threat_substitutes=-30, competitive_rivalry=-35),
    ),
    dict(
        name="PureDrop", domain="D2C hardware",
        cvp=(
            "PureDrop builds affordable, locally manufactured water purifiers designed for the hard, "
            "high-TDS groundwater common across Punjab and neighboring states. We sell direct-to-consumer "
            "online, skipping the usual dealer markup."
        ),
        pestle=dict(political=15, economic=10, social=40, technological=25, legal=-15, environmental=-40),
        porters=dict(threat_new_entrants=-35, supplier_power=-30, buyer_power=-30, threat_substitutes=-25, competitive_rivalry=-45),
    ),
    dict(
        name="MotoCharge", domain="D2C hardware",
        cvp=(
            "MotoCharge makes home and street-corner charging docks built specifically for India's "
            "exploding two-wheeler EV market. Our modular design lets a single dock serve three different "
            "scooter brands out of the box."
        ),
        pestle=dict(political=-45, economic=-50, social=35, technological=45, legal=-20, environmental=60),
        porters=dict(threat_new_entrants=-40, supplier_power=-65, buyer_power=-25, threat_substitutes=-30, competitive_rivalry=-40),
    ),
    dict(
        name="DeskLoop", domain="SaaS",
        cvp=(
            "DeskLoop is payroll and HR software built for how Indian SMEs actually run - full PF, ESI, "
            "and TDS compliance out of the box, with a WhatsApp-first employee experience instead of yet "
            "another app to install."
        ),
        pestle=dict(political=5, economic=10, social=10, technological=40, legal=40, environmental=0),
        porters=dict(threat_new_entrants=-45, supplier_power=0, buyer_power=-20, threat_substitutes=-30, competitive_rivalry=-55),
    ),
    dict(
        name="RouteIQ", domain="SaaS / logistics",
        cvp=(
            "RouteIQ plugs into any delivery fleet's existing app and re-optimizes routes in real time "
            "using live traffic and weather data, cutting fuel spend by up to 12%. No hardware, no fleet "
            "replacement - just a lighter API integration."
        ),
        pestle=dict(political=0, economic=20, social=5, technological=55, legal=0, environmental=25),
        porters=dict(threat_new_entrants=-40, supplier_power=0, buyer_power=-30, threat_substitutes=-35, competitive_rivalry=-50),
    ),
    dict(
        name="ClauseCraft", domain="SaaS / legaltech",
        cvp=(
            "ClauseCraft uses AI to flag risky clauses in vendor and employment contracts in under a "
            "minute, giving founders lawyer-grade review without the lawyer-grade bill. We've reviewed "
            "over ten thousand contracts across seed-stage startups."
        ),
        pestle=dict(political=5, economic=10, social=5, technological=50, legal=60, environmental=0),
        porters=dict(threat_new_entrants=-40, supplier_power=0, buyer_power=-25, threat_substitutes=-45, competitive_rivalry=-50),
    ),
    dict(
        name="PulseDesk", domain="SaaS",
        cvp=(
            "PulseDesk is a customer support helpdesk that uses AI to triage, tag, and draft first-"
            "response replies to tickets automatically, cutting average resolution time in half. We're "
            "built for lean support teams who can't hire their way out of ticket backlogs."
        ),
        pestle=dict(political=-10, economic=-15, social=0, technological=55, legal=-15, environmental=0),
        porters=dict(threat_new_entrants=-35, supplier_power=0, buyer_power=-25, threat_substitutes=-50, competitive_rivalry=-65),
    ),
    dict(
        name="VitalsBridge", domain="healthtech",
        cvp=(
            "VitalsBridge pairs a low-cost wearable with a monitoring dashboard so clinics can track "
            "chronic patients' vitals between visits and catch problems before they become emergencies. "
            "We're already integrated with three hospital chains in North India."
        ),
        pestle=dict(political=-20, economic=-30, social=55, technological=50, legal=-35, environmental=10),
        porters=dict(threat_new_entrants=-30, supplier_power=-45, buyer_power=-20, threat_substitutes=-25, competitive_rivalry=-35),
    ),
    dict(
        name="TeleCare Punjab", domain="healthtech",
        cvp=(
            "TeleCare Punjab connects patients in rural Punjab to qualified doctors over voice and video "
            "in Punjabi, with a nurse-assisted kiosk model for patients who don't own a smartphone. We "
            "already run kiosks in over 40 villages."
        ),
        pestle=dict(political=25, economic=10, social=65, technological=35, legal=-30, environmental=-15),
        porters=dict(threat_new_entrants=-35, supplier_power=-10, buyer_power=-20, threat_substitutes=-25, competitive_rivalry=-30),
    ),
    dict(
        name="MedStock AI", domain="healthtech / SaaS",
        cvp=(
            "MedStock AI forecasts hospital pharmacy demand down to the SKU level, so procurement teams "
            "stop overstocking slow-moving drugs while avoiding stockouts on critical ones. One mid-size "
            "hospital cut wastage by 22% in its first quarter with us."
        ),
        pestle=dict(political=0, economic=15, social=20, technological=50, legal=15, environmental=0),
        porters=dict(threat_new_entrants=-40, supplier_power=-15, buyer_power=-20, threat_substitutes=-30, competitive_rivalry=-45),
    ),
    dict(
        name="GlowLine Cosmeceuticals", domain="healthtech / D2C",
        cvp=(
            "GlowLine sells dermatologist-formulated skincare made and tested for Indian skin types and "
            "climate, sold directly online without the markup of international brands. Every batch is "
            "manufactured in our own FDA-registered facility."
        ),
        pestle=dict(political=10, economic=15, social=45, technological=15, legal=-10, environmental=-25),
        porters=dict(threat_new_entrants=-50, supplier_power=-20, buyer_power=-35, threat_substitutes=-30, competitive_rivalry=-60),
    ),
]


def dims_by_magnitude(startup: dict):
    items = []
    for d in PESTLE_DIMS:
        items.append(("pestle_scores", d, startup["pestle"][d]))
    for d in PORTERS_DIMS:
        items.append(("porters_scores", d, startup["porters"][d]))
    items.sort(key=lambda x: -abs(x[2]))
    return items


def pick_linked_articles(startup: dict, news: list[dict], rng: random.Random) -> list[str]:
    dims = dims_by_magnitude(startup)[:3]
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
        linked_ids = pick_linked_articles(s, news, rng)
        startups.append({
            "id": f"startup_{i + 1:02d}",
            "name": s["name"],
            "domain": s["domain"],
            "cvp": s["cvp"],
            "pestle_profile": s["pestle"],
            "porters_profile": s["porters"],
            "linked_article_ids": linked_ids,
        })

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(STARTUPS_PATH, "w", encoding="utf-8") as f:
        json.dump(startups, f, indent=2)
    print(f"Wrote {STARTUPS_PATH} ({len(startups)} startups)")

    print("Embedding startup CVPs...")
    embeddings = embed_texts([s["cvp"] for s in startups])
    np.save(STARTUP_EMBEDDINGS_PATH, embeddings)
    print(f"Wrote {STARTUP_EMBEDDINGS_PATH} shape={embeddings.shape}")


if __name__ == "__main__":
    main()
