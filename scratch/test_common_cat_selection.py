import urllib.request
import json

url = "http://127.0.0.1:5000/api/match_revenue_clusters"
payload = {
    "revenue_series": [
        {"period": "2026-07-01 to 2026-07-07", "revenue": 120000},
        {"period": "2026-07-08 to 2026-07-14", "revenue": 145000},
        {"period": "2026-07-15 to 2026-07-21", "revenue": 140000},
        {"period": "2026-07-22 to 2026-07-28", "revenue": 168000}
    ]
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    print("API STATUS:", resp.status)
    print("Matched News Count:", len(data["matched_news"]))
    for idx, mn in enumerate(data["matched_news"]):
        print(f"\n[Period {idx+1}] {mn['period']} (Chg: {mn['change_pct']:+.1f}%)")
        print(f"  Cluster Common Category: {mn.get('cluster_common_category')} ({mn.get('cluster_common_pct')}%)")
        print(f"  Selected Category:       {mn.get('category')}")
        print(f"  Headline:                {mn['news_headline']}")
        print(f"  Filter Rationale:        {mn['filter_rationale']}")
