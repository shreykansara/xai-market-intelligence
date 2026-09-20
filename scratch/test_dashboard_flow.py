import urllib.request
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def post_json(path, data, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def get_json(path, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"{BASE_URL}{path}", headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def run_tests():
    email = f"exec_dash_{int(time.time())}@venture.ai"
    print(f"[1] Registering user {email}...")
    reg_res = post_json("/api/auth/register", {
        "email": email,
        "password": "VenturePassword2026!",
        "full_name": "Marcus Aurelius Vance",
        "company_name": "Vance Growth Capital",
        "role": "investor"
    })
    assert reg_res["success"], f"Register failed: {reg_res}"
    token = reg_res["token"]
    print(f"    -> Success. Token obtained (len {len(token)})")

    print("[2] Saving sample CVP analysis for dashboard...")
    save_cvp = post_json("/api/user/analyses", {
        "title": "Tata Motors EV Fleet Strategy",
        "analysis_type": "cvp",
        "input_data": {
            "cvp_text": "Electric vehicle commercial fleet mobility platform"
        },
        "results_data": {
            "cvp_text": "Electric vehicle commercial fleet mobility platform",
            "pestle_vector": [0.25, 0.3, 0.28, 0.4, 0.22, 0.2],
            "porter_vector": [0.3, 0.35, 0.25, 0.28, 0.32],
            "nearest_cvps": [{"company": "Tata Motors", "similarity_pct": 94.5}]
        }
    }, token=token)
    assert save_cvp["success"], f"CVP save failed: {save_cvp}"
    print(f"    -> CVP saved with ID {save_cvp.get('analysis', {}).get('id')}")

    print("[3] Saving sample Revenue analysis for dashboard...")
    save_rev = post_json("/api/user/analyses", {
        "title": "Inditex Global Retail Sensitivity",
        "analysis_type": "revenue_sensitivity",
        "input_data": {
            "revenue_series": [100, 115, 95, 120]
        },
        "results_data": {
            "top_recommendation": "Diversify supplier footprint to mitigate logistics spikes",
            "pestle_vector": [0.35, 0.4, 0.3, 0.28, 0.25, 0.22],
            "porter_vector": [0.4, 0.38, 0.32, 0.35, 0.3],
            "nearest_cvps": [{"company": "Inditex / Zara", "similarity_pct": 91.2}]
        }
    }, token=token)
    assert save_rev["success"], f"Revenue save failed: {save_rev}"
    print(f"    -> Revenue saved with ID {save_rev.get('analysis', {}).get('id')}")

    print("[4] Saving sample AI strategy consultation thread...")
    save_chat = post_json("/api/user/conversations", {
        "title": "Inditex vs Fast Retailing Due Diligence",
        "session_id": f"sess_{int(time.time())}",
        "messages": [
            {"role": "user", "content": "How does Inditex withstand macro tariffs?"},
            {"role": "assistant", "content": "Inditex maintains a near-shore agile supply chain model."}
        ]
    }, token=token)
    assert save_chat["success"], f"Chat save failed: {save_chat}"
    print(f"    -> Conversation saved with ID {save_chat.get('conversation', {}).get('id')}")

    print("[5] Querying user analyses and conversations...")
    anas = get_json("/api/user/analyses", token=token)
    assert len(anas["analyses"]) == 2, f"Expected 2 analyses, got {len(anas['analyses'])}"
    convs = get_json("/api/user/conversations", token=token)
    assert len(convs["conversations"]) == 1, f"Expected 1 conversation, got {len(convs['conversations'])}"
    print(f"    -> Successfully verified 2 analyses and 1 conversation in DB.")

    print("[6] Fetching /dashboard HTML endpoint...")
    req = urllib.request.Request(f"{BASE_URL}/dashboard")
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8")
        assert "view-user-dashboard" in html, "view-user-dashboard not found in /dashboard"
        assert "Executive Suite" in html, "Executive Suite badge not found"
        assert "dash-kpi-cvp-count" in html, "dash-kpi-cvp-count not found"
        assert "dash-analyses-feed" in html, "dash-analyses-feed not found"
        print(f"    -> /dashboard returned {len(html)} bytes with complete executive dashboard markup.")

    print("\nALL EXECUTIVE DASHBOARD & URL ROUTING END-TO-END VERIFICATIONS PASSED!")

if __name__ == "__main__":
    run_tests()
