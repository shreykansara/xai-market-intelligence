import urllib.request
import json

BASE_URL = "http://localhost:5000"

for endpoint in ["/api/stage1/files/delete", "/api/stage2/records/delete", "/api/stage3/articles/delete"]:
    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=json.dumps({"dates": ["2099-01-01"]}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    res = urllib.request.urlopen(req)
    data = json.loads(res.read().decode())
    print(f"{endpoint} -> {data}")
    assert data["success"] is True

print("All delete endpoints with dates array verified!")
