import urllib.request
import json

req = urllib.request.Request(
    "http://localhost:5000/api/stage2/records/delete",
    data=json.dumps({"dates": ["2099-01-01"]}).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)
res = urllib.request.urlopen(req)
data = json.loads(res.read().decode())
print("Response:", data)
assert data["success"] is True, f"Failed: {data}"
print("Postgres date cast verified successfully!")
