import urllib.request
import json

BASE_URL = "http://localhost:5000"

def test_delete_endpoints():
    # 1. Test Stage 2 records query
    req = urllib.request.urlopen(f"{BASE_URL}/api/stage2/records?page=1&per_page=5")
    s2_data = json.loads(req.read().decode())
    print(f"Stage 2 Records Total: {s2_data.get('total')}")
    assert s2_data["success"] is True

    # 2. Test Stage 2 Files (batches)
    req = urllib.request.urlopen(f"{BASE_URL}/api/stage2/files")
    s2_files = json.loads(req.read().decode())
    print(f"Stage 2 Batches Count: {s2_files.get('count')}")
    assert s2_files["success"] is True

    # 3. Test Stage 3 Articles query
    req = urllib.request.urlopen(f"{BASE_URL}/api/stage3/articles?limit=5")
    s3_data = json.loads(req.read().decode())
    print(f"Stage 3 Articles Count: {s3_data.get('count')}")
    assert s3_data["success"] is True

    print("All endpoints responding correctly!")

if __name__ == "__main__":
    test_delete_endpoints()
