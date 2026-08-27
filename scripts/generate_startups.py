"""Generate 50 fabricated LPU-based startups (identity + CVP only - no ground-truth
sensitivity profile), link each to 3-5 justifying news articles from data/news.json,
embed each CVP, and save everything to data/. Grew from 20 to 50 (10 new domain
archetypes on top of the original 6) after 20 unique CVP directions proved far
too few for the shared matrix W to discriminate between businesses - see
hidden_ground_truth.py's module docstring.

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
            "Born out of LPU's startup incubator, RupeeRail gives gig and blue-collar workers instant, "
            "collateral-free micro-loans underwritten from real-time earnings data, repaid automatically "
            "as they get paid. We plug directly into gig platforms' payout APIs so workers never have to "
            "fill out a loan form."
        ),
    ),
    dict(
        name="LedgerLoop", domain="fintech / SaaS",
        cvp=(
            "LedgerLoop, incubated at Lovely Professional University, is GST-compliant accounting "
            "software built for India's SMEs, auto-filing returns and reconciling bank statements "
            "without an accountant. Founders can close their books in minutes instead of days."
        ),
    ),
    dict(
        name="CoverNest", domain="fintech / insurtech",
        cvp=(
            "An LPU-incubated startup, CoverNest sells bite-sized health and crop micro-insurance "
            "policies through a WhatsApp chatbot, priced from as little as fifty rupees a month for "
            "families with no prior insurance history. We underwrite using alternative data instead of "
            "paperwork."
        ),
    ),
    dict(
        name="SkillSprout", domain="edtech",
        cvp=(
            "SkillSprout, born out of LPU's startup incubation cell, teaches job-ready digital skills in "
            "Punjabi, Hindi, and six other regional languages through short, mobile-first video courses. "
            "We partner with local ITIs and placement cells to guarantee interviews on completion."
        ),
    ),
    dict(
        name="CampusOS", domain="edtech / SaaS",
        cvp=(
            "Founded by LPU alumni, CampusOS is a single operations platform that runs admissions, fee "
            "collection, hostel allotment, and attendance for mid-size Indian universities. We replace "
            "five disconnected legacy systems with one dashboard IT teams actually enjoy using."
        ),
    ),
    dict(
        name="ExamAnt", domain="edtech",
        cvp=(
            "An LPU-incubated startup, ExamAnt lets coaching institutes run secure, AI-proctored mock "
            "tests for competitive exams like NEET and JEE at a fraction of the cost of physical test "
            "centers. Instant, item-level analytics tell students exactly which concepts to revise."
        ),
    ),
    dict(
        name="Krishimitra", domain="agritech",
        cvp=(
            "Krishimitra, incubated at LPU, combines a low-cost soil sensor with a Punjabi-language "
            "advisory app to tell farmers exactly when to irrigate and fertilize their wheat and rice "
            "fields. Early users cut water usage by a third without losing yield."
        ),
    ),
    dict(
        name="AgriChain Direct", domain="agritech",
        cvp=(
            "Born out of LPU's startup incubator, AgriChain Direct connects Punjab farmers straight to "
            "urban retail chains, cutting out three layers of mandi middlemen and getting farmers 15-20% "
            "better prices. Retailers get fresher produce with full traceability back to the farm."
        ),
    ),
    dict(
        name="FarmYield Finance", domain="agritech / fintech",
        cvp=(
            "FarmYield Finance, an LPU-incubated startup, underwrites crop loans using satellite imagery "
            "and weather data instead of land titles, so smallholder farmers without formal collateral "
            "can still get affordable credit. Repayment schedules flex automatically around harvest "
            "cycles."
        ),
    ),
    dict(
        name="Wattlefy", domain="D2C hardware",
        cvp=(
            "Founded by LPU alumni, Wattlefy is a plug-and-play smart energy monitor that shows Indian "
            "households exactly which appliances are driving up their electricity bill, in real time on "
            "their phone. We've helped early customers cut their bills by up to 18%."
        ),
    ),
    dict(
        name="PureDrop", domain="D2C hardware",
        cvp=(
            "PureDrop, incubated at Lovely Professional University, builds affordable, locally "
            "manufactured water purifiers designed for the hard, high-TDS groundwater common across "
            "Punjab and neighboring states. We sell direct-to-consumer online, skipping the usual dealer "
            "markup."
        ),
    ),
    dict(
        name="MotoCharge", domain="D2C hardware",
        cvp=(
            "An LPU-incubated startup, MotoCharge makes home and street-corner charging docks built "
            "specifically for India's exploding two-wheeler EV market. Our modular design lets a single "
            "dock serve three different scooter brands out of the box."
        ),
    ),
    dict(
        name="DeskLoop", domain="SaaS",
        cvp=(
            "DeskLoop, born out of LPU's startup incubation cell, is payroll and HR software built for "
            "how Indian SMEs actually run - full PF, ESI, and TDS compliance out of the box, with a "
            "WhatsApp-first employee experience instead of yet another app to install."
        ),
    ),
    dict(
        name="RouteIQ", domain="SaaS / logistics",
        cvp=(
            "Founded by LPU alumni, RouteIQ plugs into any delivery fleet's existing app and re-optimizes "
            "routes in real time using live traffic and weather data, cutting fuel spend by up to 12%. "
            "No hardware, no fleet replacement - just a lighter API integration."
        ),
    ),
    dict(
        name="ClauseCraft", domain="SaaS / legaltech",
        cvp=(
            "ClauseCraft, an LPU-incubated startup, uses AI to flag risky clauses in vendor and "
            "employment contracts in under a minute, giving founders lawyer-grade review without the "
            "lawyer-grade bill. We've reviewed over ten thousand contracts across seed-stage startups."
        ),
    ),
    dict(
        name="PulseDesk", domain="SaaS",
        cvp=(
            "Incubated at Lovely Professional University, PulseDesk is a customer support helpdesk that "
            "uses AI to triage, tag, and draft first-response replies to tickets automatically, cutting "
            "average resolution time in half. We're built for lean support teams who can't hire their "
            "way out of ticket backlogs."
        ),
    ),
    dict(
        name="VitalsBridge", domain="healthtech",
        cvp=(
            "VitalsBridge, born out of LPU's startup incubator, pairs a low-cost wearable with a "
            "monitoring dashboard so clinics can track chronic patients' vitals between visits and catch "
            "problems before they become emergencies. We're already integrated with three hospital "
            "chains in North India."
        ),
    ),
    dict(
        name="TeleCare Punjab", domain="healthtech",
        cvp=(
            "Founded by LPU alumni, TeleCare Punjab connects patients in rural Punjab to qualified "
            "doctors over voice and video in Punjabi, with a nurse-assisted kiosk model for patients who "
            "don't own a smartphone. We already run kiosks in over 40 villages."
        ),
    ),
    dict(
        name="MedStock AI", domain="healthtech / SaaS",
        cvp=(
            "An LPU-incubated startup, MedStock AI forecasts hospital pharmacy demand down to the SKU "
            "level, so procurement teams stop overstocking slow-moving drugs while avoiding stockouts on "
            "critical ones. One mid-size hospital cut wastage by 22% in its first quarter with us."
        ),
    ),
    dict(
        name="GlowLine Cosmeceuticals", domain="healthtech / D2C",
        cvp=(
            "GlowLine, incubated at LPU, sells dermatologist-formulated skincare made and tested for "
            "Indian skin types and climate, sold directly online without the markup of international "
            "brands. Every batch is manufactured in our own FDA-registered facility."
        ),
    ),
    # --- Expansion set: 30 more startups across 10 new domain archetypes - see
    # hidden_ground_truth.py's module docstring for why (20 unique CVP
    # directions were nowhere near enough for W to discriminate between
    # businesses).
    dict(
        name="SolarKhet", domain="cleantech",
        cvp=(
            "An LPU-incubated startup, SolarKhet leases rooftop solar systems to Punjab farms and "
            "agri-processing units on a pay-as-you-save basis, so operators cut diesel and grid costs "
            "with zero upfront investment. We handle installation, maintenance, and financing end to end."
        ),
    ),
    dict(
        name="WindLoop", domain="cleantech",
        cvp=(
            "WindLoop, born out of LPU's startup incubator, sells predictive-maintenance sensors that "
            "detect wind turbine bearing wear weeks before failure, cutting unplanned downtime for wind "
            "farm operators. Our vibration-analysis models are trained on over ten thousand hours of "
            "turbine data."
        ),
    ),
    dict(
        name="GreenGrid Storage", domain="cleantech",
        cvp=(
            "Founded by LPU alumni, GreenGrid Storage builds modular battery storage systems that let "
            "small manufacturers shift energy use away from expensive peak-hour tariffs. A typical "
            "factory customer cuts its electricity bill by 20% within the first quarter."
        ),
    ),
    dict(
        name="CargoLane", domain="logistics",
        cvp=(
            "An LPU-incubated startup, CargoLane matches truck owners with unbooked capacity to shippers "
            "needing intercity freight in North India, cutting empty return trips by half. Shippers get "
            "real-time tracking; truckers get guaranteed loads instead of idle time at transport nagars."
        ),
    ),
    dict(
        name="ColdTrail", domain="logistics",
        cvp=(
            "ColdTrail, incubated at LPU, fits refrigerated trucks and warehouses with IoT temperature "
            "sensors so agri-exporters can prove cold-chain integrity to overseas buyers and catch "
            "spoilage risk before it happens. We've cut rejected shipments for our pilot customers by a "
            "third."
        ),
    ),
    dict(
        name="LastMile Express", domain="logistics",
        cvp=(
            "Born out of LPU's startup incubator, LastMile Express runs a hyperlocal delivery network "
            "purpose-built for tier-2 and tier-3 e-commerce fulfillment, where national courier networks "
            "are slow or absent. Local riders and micro-warehouses let us deliver same-day in cities most "
            "couriers treat as an afterthought."
        ),
    ),
    dict(
        name="BasaiHomes", domain="proptech",
        cvp=(
            "BasaiHomes, an LPU-incubated startup, lets retail investors buy fractional shares of rental "
            "housing in tier-2 cities starting at ten thousand rupees, with rental income and "
            "appreciation split proportionally. We handle property management and legal compliance so "
            "investors never have to visit the property."
        ),
    ),
    dict(
        name="RentEase", domain="proptech",
        cvp=(
            "Founded by LPU alumni, RentEase runs digital rental agreements and deposit escrow "
            "specifically for student housing near university towns, replacing cash deposits and "
            "handwritten agreements with a system both landlords and students actually trust. Disputes "
            "over deposit refunds - the single biggest landlord-tenant complaint - drop to near zero."
        ),
    ),
    dict(
        name="PlotVerify", domain="proptech",
        cvp=(
            "PlotVerify, incubated at Lovely Professional University, cross-checks land records against "
            "satellite imagery and government registries to flag fraudulent or disputed property titles "
            "before a buyer signs. What used to take a lawyer three weeks of manual verification now "
            "takes us under 48 hours."
        ),
    ),
    dict(
        name="TiffinNet", domain="foodtech",
        cvp=(
            "An LPU-incubated startup, TiffinNet connects home cooks to office workers who want fresh, "
            "home-style meals delivered daily instead of restaurant food, on a simple weekly "
            "subscription. Home chefs earn a steady income; subscribers get healthier food than what "
            "delivery apps typically offer."
        ),
    ),
    dict(
        name="HarvestBox", domain="foodtech",
        cvp=(
            "HarvestBox, born out of LPU's startup incubator, delivers a weekly box of fresh produce "
            "sourced directly from Punjab farms to urban households, cutting out the two or three layers "
            "of mandi middlemen that usually eat into both farmer and consumer value. Farmers get paid "
            "within 48 hours of harvest."
        ),
    ),
    dict(
        name="QuickBite Cloud Kitchens", domain="foodtech",
        cvp=(
            "Founded by LPU alumni, QuickBite gives small restaurant brands ready-to-use cloud kitchen "
            "infrastructure - space, equipment, and delivery-platform integration - so they can launch a "
            "delivery-only outlet in a new neighborhood without signing a single lease. Brands can test a "
            "new location for a fraction of what a physical outlet would cost."
        ),
    ),
    dict(
        name="ChargeGrid", domain="mobility / EV",
        cvp=(
            "ChargeGrid, an LPU-incubated startup, installs and operates shared EV charging points in "
            "apartment complexes where individual chargers aren't practical, billing residents per use "
            "through a simple app. Building managers get a new amenity with zero capital outlay."
        ),
    ),
    dict(
        name="SwapStation", domain="mobility / EV",
        cvp=(
            "Incubated at LPU, SwapStation runs a battery-swapping network for electric three-wheelers "
            "and last-mile delivery fleets, so drivers exchange a depleted battery for a charged one in "
            "under two minutes instead of waiting hours to charge. Fleet operators see meaningfully "
            "higher vehicle utilization as a result."
        ),
    ),
    dict(
        name="CampusRide", domain="mobility / EV",
        cvp=(
            "CampusRide, founded by LPU alumni, operates electric shuttle and bike-share fleets for "
            "university and corporate campuses, replacing diesel shuttle buses with a cleaner, "
            "app-booked alternative. Our first deployment cut campus shuttle wait times in half."
        ),
    ),
    dict(
        name="ShieldStack", domain="cybersecurity",
        cvp=(
            "An LPU-incubated startup, ShieldStack gives small and mid-size businesses managed "
            "cybersecurity monitoring - the kind of round-the-clock threat detection only large "
            "enterprises could previously afford - at a flat monthly rate with no security team required "
            "on the client's side."
        ),
    ),
    dict(
        name="PhishGuard", domain="cybersecurity",
        cvp=(
            "PhishGuard, born out of LPU's startup incubator, runs realistic phishing simulations and "
            "bite-sized security training for employees, showing companies exactly who would click a "
            "malicious link before an actual attacker finds out first. Client click-through rates on real "
            "phishing tests drop by more than half within three months."
        ),
    ),
    dict(
        name="DataVault Compliance", domain="cybersecurity",
        cvp=(
            "Founded by LPU alumni, DataVault Compliance automatically audits a company's data-handling "
            "practices against India's new data protection law, flagging gaps before a regulator or a "
            "breach does. What used to require an expensive external compliance audit now runs "
            "continuously in the background."
        ),
    ),
    dict(
        name="HireLoop", domain="HRtech",
        cvp=(
            "HireLoop, incubated at LPU, uses skills-based matching instead of just degree pedigree to "
            "connect tier-2 and tier-3 college graduates with entry-level roles they're actually "
            "qualified for. Employers get a wider, more accurately-matched candidate pool than campus "
            "placement drives alone provide."
        ),
    ),
    dict(
        name="PayrollPe", domain="HRtech",
        cvp=(
            "An LPU-incubated startup, PayrollPe automates payroll and statutory compliance - PF, ESI, "
            "professional tax - specifically for gig-economy platforms paying thousands of workers "
            "irregular amounts on irregular schedules, a case most payroll software wasn't built to "
            "handle."
        ),
    ),
    dict(
        name="CulturePulse", domain="HRtech",
        cvp=(
            "CulturePulse, founded by LPU alumni, runs anonymous, ongoing employee sentiment surveys and "
            "flags attrition risk before an exit interview ever happens, giving HR teams weeks of lead "
            "time instead of a resignation letter with no warning."
        ),
    ),
    dict(
        name="ClaimSwift", domain="insurtech",
        cvp=(
            "ClaimSwift, an LPU-incubated startup, processes two-wheeler insurance claims through "
            "photo-based AI damage assessment, cutting typical claim settlement time from two weeks to "
            "under 48 hours. Insurers reduce manual surveyor visits; riders get paid before they've "
            "finished arranging repairs."
        ),
    ),
    dict(
        name="CropShield", domain="insurtech",
        cvp=(
            "Born out of LPU's startup incubator, CropShield sells parametric weather-index insurance "
            "that pays farmers automatically when rainfall falls outside a pre-agreed range, without "
            "requiring a claims process or a field assessor at all. Payouts land in a farmer's account "
            "within days of the qualifying weather event, not months."
        ),
    ),
    dict(
        name="PetCare Plus", domain="insurtech",
        cvp=(
            "PetCare Plus, incubated at Lovely Professional University, bundles affordable pet health "
            "insurance with on-demand vet telehealth for urban pet owners, a combination that barely "
            "exists in the Indian market today. Members get same-day vet advice included in a plan that "
            "costs less than one emergency vet visit."
        ),
    ),
    dict(
        name="BuildMart Direct", domain="B2B marketplace",
        cvp=(
            "An LPU-incubated startup, BuildMart Direct connects construction material manufacturers "
            "straight to contractors and site buyers, cutting out the distributor markup that typically "
            "adds 15-20% to cement, steel, and tile prices. Contractors get manufacturer-direct pricing "
            "with the same delivery reliability they're used to."
        ),
    ),
    dict(
        name="TexSource", domain="B2B marketplace",
        cvp=(
            "TexSource, founded by LPU alumni, is a sourcing platform that connects small garment "
            "exporters to verified, quality-checked fabric mills, solving the trust problem that usually "
            "forces small exporters to buy through expensive middlemen. Every mill on the platform is "
            "physically audited before listing."
        ),
    ),
    dict(
        name="SparePartHub", domain="B2B marketplace",
        cvp=(
            "SparePartHub, born out of LPU's startup incubator, is an online marketplace for genuine auto "
            "spare parts built specifically for independent mechanics who currently rely on unreliable "
            "local distributors and frequently get counterfeit parts. Every part ships with a verifiable "
            "authenticity certificate."
        ),
    ),
    dict(
        name="QuizArena", domain="gaming / media",
        cvp=(
            "An LPU-incubated startup, QuizArena runs live, regional-language trivia and quiz shows "
            "inside a mobile app, drawing large real-time audiences in Punjabi, Hindi, and five other "
            "languages that most quiz apps ignore entirely."
        ),
    ),
    dict(
        name="StoryStack", domain="gaming / media",
        cvp=(
            "StoryStack, incubated at LPU, publishes vernacular-language webtoons and digital comics for "
            "Indian readers, a format massively popular in Korea and Japan but still nearly absent in "
            "Indian regional languages. Our top titles get re-read multiple times by the same subscriber, "
            "a strong signal for the subscription model we're building."
        ),
    ),
    dict(
        name="CampusLeague", domain="gaming / media",
        cvp=(
            "CampusLeague, founded by LPU alumni, runs and streams intercollegiate esports tournaments "
            "across Indian university campuses, turning informal dorm-room gaming into a structured, "
            "sponsorable competitive circuit. We've run tournaments across more than 40 colleges in our "
            "first year."
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
