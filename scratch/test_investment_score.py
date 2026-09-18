import json
import urllib.request
import time

time.sleep(1)

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

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print("STATUS:", resp.status)
        prognosis = data.get("investment_prognosis")
        print("INVESTMENT PROGNOSIS:")
        print("  Score:", prognosis.get("score"))
        print("  Tier:", prognosis.get("tier"), f"({prognosis.get('tier_label')})")
        print("  Recommendation:", prognosis.get("recommendation"))
        print("  Verdict:", prognosis.get("verdict"))
        print("  Trailing Momentum:", prognosis.get("growth_rate_trailing"))
        print("  Acceleration:", prognosis.get("acceleration_rate"))
        print("  Factors:", json.dumps(prognosis.get("factors"), indent=2))
        print("  Catalysts:", prognosis.get("catalysts"))
        print("  Deterrents:", prognosis.get("deterrents"))
except Exception as e:
    print("ERROR:", e)
