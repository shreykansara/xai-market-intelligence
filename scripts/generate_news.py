"""Generate 1000 fabricated news articles with PESTLE/Porter's ground-truth score
vectors, then embed each article's text and save everything to data/.

Run: python scripts/generate_news.py
"""
import json
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.config import (  # noqa: E402
    DATA_DIR,
    N_NEWS_ARTICLES,
    NEWS_EMBEDDINGS_PATH,
    NEWS_PATH,
    PESTLE_DIMS,
    PORTERS_DIMS,
    SCOPE_WEIGHTS,
)
from marketintel.embeddings import embed_texts  # noqa: E402

SEED = 42
TODAY = datetime(2026, 8, 24)

SECTORS = [
    "fintech", "edtech", "agritech", "healthtech", "e-commerce", "D2C hardware",
    "SaaS", "logistics", "renewable energy", "textiles", "manufacturing", "EV",
    "food delivery", "gaming", "real estate",
]
TECHS = [
    "generative AI", "5G", "blockchain", "IoT sensors", "cloud computing",
    "quantum computing", "autonomous drones", "AR/VR", "robotic process automation",
    "edge computing",
]
COMPANIES = [
    "Nimbus Retail", "Verdant Foods", "Quantify Labs", "Orbit Mobility", "Bluepeak Systems",
    "Craterra Agritech", "Finlume", "Medivue Health", "Sundial Energy", "Loomcraft Textiles",
    "Nexbyte Robotics", "Harborline Logistics", "Pixelforge Games", "Trueledger Finance",
    "Greenspan Renewables",
]
COUNTRIES = [
    "the United States", "China", "the United Kingdom", "Germany", "Japan", "Brazil",
    "the UAE", "Australia", "South Korea", "France", "Canada", "Singapore",
]
INDIAN_CITIES = ["Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Chennai", "Pune", "Ahmedabad", "Kolkata"]
PUNJAB_TOWNS = ["Amritsar", "Ludhiana", "Patiala", "Bathinda", "Mohali", "Ferozepur", "Moga"]
REGULATIONS = [
    "the Digital Personal Data Protection Act", "the Consumer Protection (E-Commerce) Rules",
    "the GST compliance framework", "Startup India norms", "the FDI policy", "the new Labour Codes",
]

# Each template: scopes ("any" or list), title, body (list of sentence templates),
# pestle base scores (0-1), porters base scores (0-1), polarity_bias (P(positive)).
TEMPLATES = [
    dict(scopes="any", polarity_bias=0.15,
         title="New tariffs rattle {sector} supply chains in {region}",
         body=["Authorities in {region} announced fresh import tariffs affecting {sector} companies.",
               "Industry groups warn the move could raise costs by {pct}% within {year}."],
         pestle=dict(political=0.9, economic=0.8), porters=dict(supplier_power=0.6, threat_new_entrants=0.3)),
    dict(scopes=["India", "Punjab"], polarity_bias=0.55,
         title="Election results in {region} signal new trade stance",
         body=["Following the latest elections, {region} is expected to shift trade policy direction.",
               "Analysts say the {sector} sector will be watching closely for follow-through."],
         pestle=dict(political=0.9, economic=0.3, social=0.2), porters=dict()),
    dict(scopes=["World", "India"], polarity_bias=0.1,
         title="Diplomatic tension rises between India and {country}",
         body=["A diplomatic dispute between India and {country} has escalated this week.",
               "Trade flows tied to {sector} could be disrupted if talks stall further."],
         pestle=dict(political=0.95, economic=0.4), porters=dict()),
    dict(scopes=["India", "Punjab"], polarity_bias=0.85,
         title="Government unveils subsidy package for {sector} startups",
         body=["A new subsidy package worth crores was announced to boost {sector} startups in {region}.",
               "Founders say the incentive could accelerate hiring and product launches over the next {year}."],
         pestle=dict(political=0.7, economic=0.6), porters=dict(threat_new_entrants=0.5)),
    dict(scopes=["LPU", "Phagwara", "Jalandhar", "Kapurthala"], polarity_bias=0.6,
         title="{region} municipal body revises local business policy",
         body=["The municipal body in {region} passed a policy update affecting small businesses.",
               "Local {sector} operators are assessing how the change affects daily operations."],
         pestle=dict(political=0.6, social=0.3), porters=dict()),
    dict(scopes=["World", "India"], polarity_bias=0.35,
         title="Visa and immigration rules tighten for tech workers heading to {country}",
         body=["New immigration rules in {country} will affect thousands of {sector} professionals.",
               "Companies reliant on cross-border talent are reassessing hiring plans."],
         pestle=dict(political=0.8, social=0.4), porters=dict()),
    dict(scopes=["World", "India"], polarity_bias=0.8,
         title="India signs trade agreement with {country} covering {sector}",
         body=["India and {country} finalized a trade agreement with direct implications for {sector}.",
               "Officials expect the deal to ease cross-border operations within {year}."],
         pestle=dict(political=0.85, economic=0.7), porters=dict(supplier_power=0.4, threat_new_entrants=0.3)),
    dict(scopes=["India", "Punjab"], polarity_bias=0.1,
         title="Protests in {region} disrupt local commerce",
         body=["Widespread protests in {region} have disrupted normal business activity.",
               "{sector} businesses report delayed shipments and reduced footfall."],
         pestle=dict(political=0.8, social=0.5), porters=dict()),
    dict(scopes=["India"], polarity_bias=0.5,
         title="RBI adjusts repo rate by {bps} basis points",
         body=["The Reserve Bank of India changed the repo rate by {bps} basis points this quarter.",
               "The move is expected to ripple through borrowing costs for {sector} firms."],
         pestle=dict(economic=0.9, political=0.2), porters=dict()),
    dict(scopes=["India", "World"], polarity_bias=0.4,
         title="Rupee moves sharply against the dollar amid global volatility",
         body=["The rupee shifted noticeably against the US dollar this week.",
               "Import-heavy {sector} businesses are recalculating margins as a result."],
         pestle=dict(economic=0.85), porters=dict()),
    dict(scopes=["India"], polarity_bias=0.3,
         title="Inflation data shows {pct}% rise in consumer prices",
         body=["Fresh data shows consumer prices rose {pct}% year-on-year.",
               "Household spending on {sector} products may soften in response."],
         pestle=dict(economic=0.9, social=0.3), porters=dict()),
    dict(scopes=["India", "World"], polarity_bias=0.6,
         title="India's GDP growth outlook revised for {year}",
         body=["Economists revised India's GDP growth forecast for {year}.",
               "The {sector} sector is seen as a key contributor to the updated outlook."],
         pestle=dict(economic=0.9), porters=dict()),
    dict(scopes=["India", "Punjab"], polarity_bias=0.85,
         title="Funding surge hits {sector} startups in {region}",
         body=["Venture funding into {sector} startups based in {region} jumped sharply this quarter.",
               "Several new entrants are reportedly preparing to launch competing products."],
         pestle=dict(economic=0.6, technological=0.3),
         porters=dict(threat_new_entrants=0.7, competitive_rivalry=0.5)),
    dict(scopes=["World"], polarity_bias=0.1,
         title="Recession fears grow across major economies",
         body=["Growing recession fears are weighing on major global economies.",
               "{sector} companies with international exposure are bracing for softer demand."],
         pestle=dict(economic=0.95, political=0.3), porters=dict()),
    dict(scopes=["India", "Punjab"], polarity_bias=0.15,
         title="Fuel prices climb again in {region}",
         body=["Fuel prices rose again in {region}, adding pressure to logistics costs.",
               "{sector} companies that depend on transport are passing costs to consumers."],
         pestle=dict(economic=0.8, social=0.4), porters=dict()),
    dict(scopes=["Punjab", "Jalandhar", "Kapurthala"], polarity_bias=0.45,
         title="Mandi prices shift for key crops near {region}",
         body=["Mandi prices for key crops shifted noticeably near {region} this week.",
               "Agritech platforms serving local farmers are adjusting their forecasts."],
         pestle=dict(economic=0.7, social=0.2), porters=dict()),
    dict(scopes=["India", "World"], polarity_bias=0.75,
         title="Survey: {pct}% of Gen Z now prefer {sector} subscription models",
         body=["A new survey found {pct}% of Gen Z consumers prefer subscription-based {sector} products.",
               "Brands are being pushed to redesign pricing to match the shift."],
         pestle=dict(social=0.8, technological=0.3), porters=dict(buyer_power=0.5)),
    dict(scopes=["LPU", "Phagwara"], polarity_bias=0.8,
         title="LPU campus enrollment rises {pct}% this term",
         body=["Lovely Professional University reported a {pct}% rise in enrollment this term.",
               "Local businesses around {region} expect a boost in campus-adjacent demand."],
         pestle=dict(social=0.7), porters=dict()),
    dict(scopes=["Punjab", "India"], polarity_bias=0.3,
         title="Youth migration trend continues out of {region}",
         body=["A continuing wave of youth migration out of {region} is reshaping the local workforce.",
               "{sector} employers in the region report growing difficulty hiring locally."],
         pestle=dict(social=0.8, economic=0.3), porters=dict()),
    dict(scopes=["India", "Punjab"], polarity_bias=0.8,
         title="Public health campaign launches across {region}",
         body=["A large-scale public health awareness campaign launched across {region}.",
               "Healthtech providers see the campaign as a tailwind for adoption."],
         pestle=dict(social=0.7, environmental=0.2), porters=dict()),
    dict(scopes=["Punjab", "Jalandhar", "Kapurthala"], polarity_bias=0.75,
         title="Cultural festival season boosts local commerce in {region}",
         body=["Festival season brought a visible boost to local commerce in {region}.",
               "{sector} vendors reported some of their strongest sales of the year."],
         pestle=dict(social=0.6, economic=0.3), porters=dict()),
    dict(scopes=["India", "World"], polarity_bias=0.55,
         title="Gig economy and remote work reshape {sector} hiring",
         body=["Remote work and gig platforms continue to reshape hiring within {sector}.",
               "Companies are rethinking benefits and retention strategy as a result."],
         pestle=dict(social=0.7, technological=0.3), porters=dict(buyer_power=0.3)),
    dict(scopes=["India", "LPU"], polarity_bias=0.7,
         title="Education policy reform targets {sector} skilling",
         body=["A new education policy reform introduces {sector}-focused skilling programs.",
               "Universities including LPU are expected to update curricula within {year}."],
         pestle=dict(social=0.6, political=0.4), porters=dict()),
    dict(scopes="any", polarity_bias=0.85,
         title="{tech} adoption surges across the {sector} industry",
         body=["Adoption of {tech} is surging across the {sector} industry.",
               "Early movers say it is already changing how they compete for customers."],
         pestle=dict(technological=0.9, economic=0.2),
         porters=dict(threat_substitutes=0.4, threat_new_entrants=0.4)),
    dict(scopes=["India", "Punjab", "Jalandhar"], polarity_bias=0.85,
         title="5G rollout reaches {region}",
         body=["Telecom operators extended 5G coverage to {region} this month.",
               "{sector} businesses in the area expect faster digital adoption as a result."],
         pestle=dict(technological=0.8), porters=dict()),
    dict(scopes=["India", "World"], polarity_bias=0.4,
         title="Draft AI regulation released for public comment",
         body=["Regulators released a draft AI regulation open for public comment.",
               "{sector} companies using {tech} are reviewing compliance implications."],
         pestle=dict(technological=0.6, political=0.5, legal=0.5), porters=dict()),
    dict(scopes=["India", "World"], polarity_bias=0.05,
         title="Cybersecurity breach hits {sector} platform",
         body=["A cybersecurity breach was disclosed at a major {sector} platform.",
               "Regulators are reviewing whether {regulation} was violated."],
         pestle=dict(technological=0.8, legal=0.3), porters=dict()),
    dict(scopes="any", polarity_bias=0.8,
         title="{company} launches new {tech}-powered product for {sector}",
         body=["{company} unveiled a new {tech}-powered product targeting the {sector} market.",
               "Competitors are expected to respond with similar offerings within {year}."],
         pestle=dict(technological=0.7), porters=dict(competitive_rivalry=0.5, threat_substitutes=0.3)),
    dict(scopes=["LPU", "India"], polarity_bias=0.85,
         title="LPU research team announces breakthrough in {tech}",
         body=["A research team at LPU announced a breakthrough involving {tech}.",
               "The work could have downstream applications for {sector} companies."],
         pestle=dict(technological=0.7, social=0.2), porters=dict()),
    dict(scopes=["India", "World"], polarity_bias=0.7,
         title="Cloud infrastructure investment accelerates in {region}",
         body=["Major cloud providers announced new infrastructure investment in {region}.",
               "{sector} startups expect lower hosting costs as capacity expands."],
         pestle=dict(technological=0.7, economic=0.4), porters=dict()),
    dict(scopes=["World", "India"], polarity_bias=0.35,
         title="Open-source alternative disrupts established {sector} tools",
         body=["A widely adopted open-source alternative is disrupting established {sector} tools.",
               "Incumbent vendors are cutting prices to retain customers."],
         pestle=dict(technological=0.6), porters=dict(threat_substitutes=0.8, competitive_rivalry=0.4)),
    dict(scopes=["India"], polarity_bias=0.55,
         title="Data protection law enforcement begins for {sector} firms",
         body=["Enforcement of {regulation} begins this quarter for {sector} firms.",
               "Compliance teams are racing to update data-handling practices."],
         pestle=dict(legal=0.9, technological=0.3, political=0.3), porters=dict()),
    dict(scopes=["India"], polarity_bias=0.5,
         title="Court ruling clarifies rules for {sector} businesses",
         body=["A court ruling this week clarified regulatory obligations for {sector} businesses.",
               "Legal experts say the decision reduces ambiguity going into {year}."],
         pestle=dict(legal=0.9, political=0.2), porters=dict()),
    dict(scopes=["India"], polarity_bias=0.45,
         title="Compliance deadline for {regulation} shifts",
         body=["The compliance deadline for {regulation} was revised this week.",
               "{sector} companies are reassessing internal timelines accordingly."],
         pestle=dict(legal=0.8, economic=0.2), porters=dict()),
    dict(scopes=["India", "World"], polarity_bias=0.3,
         title="Patent dispute clouds {sector} product launch",
         body=["A patent dispute is clouding a major {sector} product launch.",
               "Analysts say the outcome could reshape competitive positioning in the category."],
         pestle=dict(legal=0.7, technological=0.3), porters=dict(threat_substitutes=0.3)),
    dict(scopes=["India", "Punjab"], polarity_bias=0.55,
         title="Labour law reform affects {sector} employers in {region}",
         body=["A labour law reform passed this month directly affects {sector} employers in {region}.",
               "HR teams are updating contracts ahead of the new requirements."],
         pestle=dict(legal=0.7, social=0.4, political=0.3), porters=dict()),
    dict(scopes=["India", "Punjab"], polarity_bias=0.85,
         title="Licensing rules eased for {sector} startups",
         body=["Regulators eased licensing requirements for {sector} startups in {region}.",
               "Founders expect faster time-to-market as a result."],
         pestle=dict(legal=0.7, political=0.3), porters=dict(threat_new_entrants=0.7)),
    dict(scopes=["Punjab", "India", "World"], polarity_bias=0.1,
         title="Heatwave grips {region}, straining infrastructure",
         body=["An intense heatwave is gripping {region}, straining power and water infrastructure.",
               "{sector} operations dependent on outdoor logistics are seeing delays."],
         pestle=dict(environmental=0.9, social=0.3), porters=dict()),
    dict(scopes=["Punjab", "Jalandhar", "Kapurthala"], polarity_bias=0.2,
         title="Stubble-burning penalties tighten near {region}",
         body=["Authorities tightened stubble-burning penalties for farmland near {region}.",
               "Agritech firms are positioning new services as compliant alternatives."],
         pestle=dict(environmental=0.9, legal=0.3, political=0.2), porters=dict()),
    dict(scopes=["India", "World"], polarity_bias=0.8,
         title="Renewable energy policy push targets {sector} adoption",
         body=["A new renewable energy policy push specifically targets {sector} adoption.",
               "Incentives are expected to lower switching costs within {year}."],
         pestle=dict(environmental=0.8, political=0.4, economic=0.3), porters=dict()),
    dict(scopes=["Punjab"], polarity_bias=0.1,
         title="Water scarcity concerns grow across {region}",
         body=["Water scarcity concerns are growing across {region}, affecting agricultural output.",
               "{sector} businesses tied to farming are revising seasonal projections downward."],
         pestle=dict(environmental=0.8, economic=0.4, social=0.3), porters=dict()),
    dict(scopes=["World"], polarity_bias=0.6,
         title="Global climate summit produces new commitments",
         body=["A global climate summit concluded with new emissions commitments.",
               "{sector} companies with export exposure are reviewing sustainability roadmaps."],
         pestle=dict(environmental=0.8, political=0.5), porters=dict()),
    dict(scopes=["India", "World"], polarity_bias=0.7,
         title="Sustainability certification gains traction among {sector} buyers",
         body=["Sustainability certification is gaining traction among {sector} buyers.",
               "Vendors without certification report growing pressure to catch up."],
         pestle=dict(environmental=0.6, social=0.3), porters=dict(buyer_power=0.3)),
    dict(scopes="any", polarity_bias=0.85,
         title="{company} closes mega funding round for {sector} expansion",
         body=["{company} closed a mega funding round earmarked for {sector} expansion.",
               "Rivals are expected to accelerate fundraising in response."],
         pestle=dict(economic=0.4), porters=dict(competitive_rivalry=0.7, threat_new_entrants=0.5)),
    dict(scopes="any", polarity_bias=0.2,
         title="Price war erupts among {sector} platforms",
         body=["A price war has erupted among leading {sector} platforms.",
               "Margins across the category are coming under pressure."],
         pestle=dict(economic=0.3), porters=dict(competitive_rivalry=0.9, buyer_power=0.5)),
    dict(scopes="any", polarity_bias=0.15,
         title="Component shortage hits {sector} supply chains",
         body=["A global component shortage is hitting {sector} supply chains hard.",
               "Lead times have stretched well beyond typical planning windows."],
         pestle=dict(economic=0.4), porters=dict(supplier_power=0.9)),
    dict(scopes=["World", "India"], polarity_bias=0.35,
         title="Supplier consolidation reshapes {sector} sourcing",
         body=["A wave of supplier consolidation is reshaping sourcing options for {sector} firms.",
               "Buyers report fewer vendors to negotiate with."],
         pestle=dict(economic=0.3), porters=dict(supplier_power=0.8)),
    dict(scopes=["India", "World"], polarity_bias=0.3,
         title="Discount wars intensify across {sector} e-commerce",
         body=["Discount wars are intensifying across {sector} e-commerce platforms.",
               "Customer acquisition costs are climbing even as prices fall."],
         pestle=dict(economic=0.3), porters=dict(buyer_power=0.8, competitive_rivalry=0.5)),
    dict(scopes="any", polarity_bias=0.4,
         title="Subscription fatigue drives {sector} customers toward alternatives",
         body=["Subscription fatigue is driving {sector} customers toward cheaper alternatives.",
               "Retention teams are testing new pricing tiers to compensate."],
         pestle=dict(social=0.3), porters=dict(buyer_power=0.7, threat_substitutes=0.4)),
    dict(scopes=["India", "World"], polarity_bias=0.5,
         title="Consolidation wave hits {sector} amid slowing growth",
         body=["A consolidation wave is sweeping through {sector} as growth slows.",
               "Smaller players are being acquired by larger incumbents."],
         pestle=dict(economic=0.3), porters=dict(competitive_rivalry=0.6)),
]


def region_for_scope(scope: str, rng: random.Random) -> str:
    if scope == "LPU":
        return rng.choice(["the LPU campus", "Lovely Professional University"])
    if scope == "Phagwara":
        return "Phagwara"
    if scope == "Jalandhar":
        return "Jalandhar"
    if scope == "Kapurthala":
        return "Kapurthala"
    if scope == "Punjab":
        return rng.choice(["Punjab"] * 3 + PUNJAB_TOWNS)
    if scope == "India":
        return rng.choice(["India"] * 3 + INDIAN_CITIES)
    return rng.choice(COUNTRIES + ["global markets"])


def eligible_templates(scope: str):
    return [t for t in TEMPLATES if t["scopes"] == "any" or scope in t["scopes"]]


def fill(template_str: str, ctx: dict) -> str:
    return template_str.format(**ctx)


def clip01(x: float) -> float:
    return max(0.0, min(1.0, x))


def build_scores(base: dict, dims: list[str], rng: random.Random) -> dict:
    scores = {}
    for d in dims:
        if d in base:
            scores[d] = round(clip01(base[d] + rng.uniform(-0.08, 0.08)), 3)
        else:
            scores[d] = round(rng.uniform(0.02, 0.12), 3)
    return scores


def weighted_scope(rng: random.Random) -> str:
    scopes = list(SCOPE_WEIGHTS.keys())
    weights = list(SCOPE_WEIGHTS.values())
    return rng.choices(scopes, weights=weights, k=1)[0]


def generate_articles(n: int, rng: random.Random) -> list[dict]:
    articles = []
    for i in range(n):
        scope = weighted_scope(rng)
        candidates = eligible_templates(scope)
        tmpl = rng.choice(candidates)

        ctx = dict(
            region=region_for_scope(scope, rng),
            sector=rng.choice(SECTORS),
            tech=rng.choice(TECHS),
            company=rng.choice(COMPANIES),
            country=rng.choice(COUNTRIES),
            regulation=rng.choice(REGULATIONS),
            pct=rng.randint(2, 38),
            bps=rng.randint(10, 75),
            year=rng.choice([2026, 2027]),
        )

        title = fill(tmpl["title"], ctx)
        body = " ".join(fill(s, ctx) for s in tmpl["body"])

        polarity = "positive" if rng.random() < tmpl["polarity_bias"] else "negative"
        days_ago = rng.randint(0, 180)
        date = (TODAY - timedelta(days=days_ago)).strftime("%Y-%m-%d")

        pestle_scores = build_scores(tmpl["pestle"], PESTLE_DIMS, rng)
        porters_scores = build_scores(tmpl["porters"], PORTERS_DIMS, rng)

        articles.append({
            "id": f"news_{i + 1:04d}",
            "title": title,
            "date": date,
            "body": body,
            "polarity": polarity,
            "scope": scope,
            "pestle_scores": pestle_scores,
            "porters_scores": porters_scores,
        })
    return articles


def main():
    rng = random.Random(SEED)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Generating {N_NEWS_ARTICLES} fabricated news articles...")
    articles = generate_articles(N_NEWS_ARTICLES, rng)

    with open(NEWS_PATH, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2)
    print(f"Wrote {NEWS_PATH}")

    print("Embedding article text (title + body) with sentence-transformers...")
    texts = [f"{a['title']}. {a['body']}" for a in articles]
    embeddings = embed_texts(texts)
    import numpy as np
    np.save(NEWS_EMBEDDINGS_PATH, embeddings)
    print(f"Wrote {NEWS_EMBEDDINGS_PATH} shape={embeddings.shape}")


if __name__ == "__main__":
    main()
