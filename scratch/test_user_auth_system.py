import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from server import app
import user_auth


def test_user_auth_suite():
    client = app.test_client()

    print("\n--- 1. Testing Registration ---")
    test_email = f"founder_test_{int(user_auth.time.time())}@omniscope.ai"
    reg_payload = {
        "email": test_email,
        "password": "SecurePassword123!",
        "full_name": "Arjun Sharma",
        "company_name": "NeuralLogix India",
        "role": "founder"
    }
    res = client.post("/api/auth/register", json=reg_payload)
    print("Register Status:", res.status_code)
    data = res.get_json()
    assert res.status_code == 200, f"Registration failed: {data}"
    assert data["success"] is True
    assert "token" in data
    assert data["user"]["email"] == test_email
    token = data["token"]
    user_id = data["user"]["id"]
    print("User registered with ID:", user_id)

    print("\n--- 2. Testing Duplicate Registration Rejection ---")
    dup_res = client.post("/api/auth/register", json=reg_payload)
    print("Duplicate Register Status:", dup_res.status_code)
    assert dup_res.status_code == 400

    print("\n--- 3. Testing Login ---")
    login_res = client.post("/api/auth/login", json={
        "email": test_email,
        "password": "SecurePassword123!"
    })
    print("Login Status:", login_res.status_code)
    login_data = login_res.get_json()
    assert login_res.status_code == 200
    assert login_data["success"] is True
    assert "token" in login_data

    print("\n--- 4. Testing Invalid Password ---")
    bad_login = client.post("/api/auth/login", json={
        "email": test_email,
        "password": "WrongPassword!"
    })
    assert bad_login.status_code == 401

    print("\n--- 5. Testing /api/auth/me Profile Route ---")
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    print("Auth Me Status:", me_res.status_code)
    me_data = me_res.get_json()
    assert me_res.status_code == 200
    assert me_data["user"]["id"] == user_id
    assert me_data["user"]["full_name"] == "Arjun Sharma"

    print("\n--- 6. Testing CVP Analysis Persistence ---")
    cvp_save_res = client.post("/api/user/analyses", headers={"Authorization": f"Bearer {token}"}, json={
        "analysis_type": "cvp",
        "title": "CVP: EV Smart Fleet Telematics",
        "summary": "Dual radars compared against 500 benchmark companies.",
        "input_data": {"cvp_text": "AI telematics for electric commercial fleets"},
        "results_data": {
            "pestle_vector": [0.35, 0.45, 0.55, 0.85, 0.60, 0.70],
            "porter_vector": [0.40, 0.65, 0.50, 0.35, 0.75],
            "nearest_cvps": [{"company": "Tata Motors", "similarity_pct": 92.4}]
        }
    })
    print("CVP Analysis Save Status:", cvp_save_res.status_code)
    cvp_save_data = cvp_save_res.get_json()
    assert cvp_save_res.status_code == 200
    anl_id = cvp_save_data["analysis"]["id"]
    print("Saved Analysis ID:", anl_id)

    print("\n--- 7. Testing List User Analyses ---")
    list_res = client.get("/api/user/analyses", headers={"Authorization": f"Bearer {token}"})
    print("List Analyses Status:", list_res.status_code)
    list_data = list_res.get_json()
    assert list_res.status_code == 200
    assert len(list_data["analyses"]) >= 1
    assert list_data["analyses"][0]["id"] == anl_id

    print("\n--- 8. Testing Conversation Save & Auto-Save ---")
    conv_save_res = client.post("/api/user/conversations", headers={"Authorization": f"Bearer {token}"}, json={
        "title": "Fleet Strategy Discussion",
        "mode": "cvp",
        "analysis_id": anl_id,
        "messages": [
            {"role": "user", "content": "How do we beat Tata Motors on pricing?", "timestamp": "2026-09-19T14:00:00Z"},
            {"role": "assistant", "content": "Focus on subscription software margins rather than hardware.", "timestamp": "2026-09-19T14:00:02Z"}
        ],
        "context": {"cvp_text": "AI telematics for electric commercial fleets"}
    })
    print("Save Conversation Status:", conv_save_res.status_code)
    conv_data = conv_save_res.get_json()
    assert conv_save_res.status_code == 200
    conv_id = conv_data["conversation"]["id"]
    print("Saved Conversation ID:", conv_id)

    print("\n--- 9. Testing List Conversations ---")
    conv_list_res = client.get("/api/user/conversations", headers={"Authorization": f"Bearer {token}"})
    assert conv_list_res.status_code == 200
    conv_list = conv_list_res.get_json()["conversations"]
    assert len(conv_list) >= 1
    assert conv_list[0]["id"] == conv_id

    print("\n--- 10. Testing Guest Data Migration Sync ---")
    guest_sync_res = client.post("/api/user/sync_guest_data", headers={"Authorization": f"Bearer {token}"}, json={
        "analyses": [{
            "id": "guest_cvp_1",
            "analysis_type": "cvp",
            "title": "Guest Session CVP",
            "summary": "Created before logging in",
            "input_data": {"cvp_text": "Fintech payment rail for MSMEs"},
            "results_data": {"pestle_vector": [0.4, 0.4, 0.4, 0.4, 0.4, 0.4]}
        }],
        "conversations": [{
            "id": "guest_cnv_1",
            "title": "Guest Chat Turn",
            "mode": "cvp",
            "messages": [{"role": "user", "content": "Hello AI", "timestamp": "2026-09-19T14:00:00Z"}]
        }]
    })
    print("Guest Sync Status:", guest_sync_res.status_code)
    sync_data = guest_sync_res.get_json()
    assert guest_sync_res.status_code == 200
    assert sync_data["saved_analyses"] == 1
    assert sync_data["saved_conversations"] == 1

    print("\n--- 11. Testing Logout ---")
    logout_res = client.post("/api/auth/logout")
    assert logout_res.status_code == 200

    print("\nALL BACKEND AUTH & PERSISTENCE TESTS PASSED SUCCESSFULLY! [11/11]")

if __name__ == "__main__":
    test_user_auth_suite()
