import urllib.request
import json

req = urllib.request.urlopen("http://localhost:5000/api/stage1/next-date")
data = json.loads(req.read().decode())
print("Next date response:", data)
assert data["success"] is True
assert data["latest_date"] == "2026-09-01"
assert data["next_date"] == "2026-09-02"
print("[OK] Next date successfully verified as 2026-09-02!")
