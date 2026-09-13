import urllib.request
import json

BASE_URL = "http://localhost:5000"

def test_get_stage1_files():
    req = urllib.request.urlopen(f"{BASE_URL}/api/stage1/files")
    data = json.loads(req.read().decode())
    print("Stage 1 Files:", data)
    assert data["success"] is True
    # Verify no synthetic files like "GDELT Events Archive..." exist
    for f in data.get("files", []):
        assert "GDELT Events Archive" not in f["filename"], f"Synthetic file found: {f['filename']}"
        assert f["remaining_count"] > 0, f"Completed file not purged: {f}"

def test_db_status():
    req = urllib.request.urlopen(f"{BASE_URL}/api/stage3/db-status")
    data = json.loads(req.read().decode())
    print("DB Status:", data)
    assert data["success"] is True

if __name__ == "__main__":
    test_get_stage1_files()
    test_db_status()
    print("All tests passed!")
