import urllib.request
import json

retail_data = [
    {"period": "2026-07-W2 (Jul 08-14)", "revenue": 118500, "change_pct": -16.8, "notes": "Tariff Escalation Anticipation & Pre-emptive Port Ingestion"},
    {"period": "2026-07-W4 (Jul 22-28)", "revenue": 104200, "change_pct": -12.1, "notes": "Red Sea Maritime Shipping Disruptions & Logistics Delays"},
    {"period": "2026-08-W2 (Aug 05-11)", "revenue": 132400, "change_pct": 27.1, "notes": "Digital-First Neighbourhood Format Launch & Retail Store Unveiling"},
    {"period": "2026-08-W4 (Aug 19-25)", "revenue": 134100, "change_pct": 1.3, "notes": "Standard Consumer Energy Tax Holiday & Mid-Quarter Equilibrium"}
]

req = urllib.request.Request(
    "http://127.0.0.1:5000/api/match_revenue_clusters",
    data=json.dumps({"revenue_series": retail_data}).encode(),
    headers={"Content-Type": "application/json"}
)
res = urllib.request.urlopen(req)
d = json.loads(res.read())

print("=== PESTLE CATEGORIES AUDIT ===")
for cat in d["audit_categories"]["pestle"]:
    score_pct = int(round(cat["assigned_score"] * 100))
    print(f"[{cat['name']}] Score: {score_pct}% ({cat['severity_level']}) | News Count: {len(cat['news_items'])}")
    print(f"  Dominant Fluctuation: {cat.get('dominant_fluctuation')}")
    print(f"  Rationale: {cat.get('overall_rationale')[:110]}...")
    if cat["news_items"]:
        top_n = cat["news_items"][0]
        print(f"  Top News: \"{top_n['headline']}\" ({top_n['published_date']}, {top_n['location_affected']})")
        print(f"  Link: {top_n['source_link']}")

print("\n=== PORTER CATEGORIES AUDIT ===")
for cat in d["audit_categories"]["porter"]:
    score_pct = int(round(cat["assigned_score"] * 100))
    print(f"[{cat['name']}] Score: {score_pct}% ({cat['severity_level']}) | News Count: {len(cat['news_items'])}")
    print(f"  Dominant Fluctuation: {cat.get('dominant_fluctuation')}")
    print(f"  Rationale: {cat.get('overall_rationale')[:110]}...")
    if cat["news_items"]:
        top_n = cat["news_items"][0]
        print(f"  Top News: \"{top_n['headline']}\" ({top_n['published_date']}, {top_n['location_affected']})")
        print(f"  Link: {top_n['source_link']}")
