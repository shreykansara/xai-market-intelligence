import urllib.request

BASE_URL = "http://localhost:5000"

def test_admin_assets():
    # 1. Check admin.html
    req = urllib.request.urlopen(f"{BASE_URL}/admin")
    html = req.read().decode('utf-8')
    assert "s1-files-select-all" in html, "Missing s1-files-select-all"
    assert "s1-files-bulk-bar" in html, "Missing s1-files-bulk-bar"
    assert "s2-files-bulk-bar" in html, "Missing s2-files-bulk-bar"
    assert "s2-records-bulk-bar" in html, "Missing s2-records-bulk-bar"
    assert "s3-batches-bulk-bar" in html, "Missing s3-batches-bulk-bar"
    assert "s3-articles-bulk-bar" in html, "Missing s3-articles-bulk-bar"
    assert "btn-danger-mini" in html, "Missing btn-danger-mini"
    print("[OK] admin.html served with all bulk action bars and select all checkboxes!")

    # 2. Check admin-controller.js
    req = urllib.request.urlopen(f"{BASE_URL}/modules/admin-controller.js")
    js = req.read().decode('utf-8')
    assert "toggleSelectAll" in js, "Missing toggleSelectAll"
    assert "deleteStage1File" in js, "Missing deleteStage1File"
    assert "deleteSelectedStage1Files" in js, "Missing deleteSelectedStage1Files"
    assert "convertSelectedStage1Files" in js, "Missing convertSelectedStage1Files"
    assert "deleteStage2Batch" in js, "Missing deleteStage2Batch"
    assert "deleteStage3Article" in js, "Missing deleteStage3Article"
    print("[OK] admin-controller.js served with full delete & bulk actions logic!")

    # 3. Check api-client.js
    req = urllib.request.urlopen(f"{BASE_URL}/modules/api-client.js")
    api_js = req.read().decode('utf-8')
    assert "deleteStage1Files" in api_js, "Missing deleteStage1Files"
    assert "deleteStage2Records" in api_js, "Missing deleteStage2Records"
    assert "deleteStage3Articles" in api_js, "Missing deleteStage3Articles"
    print("[OK] api-client.js served with all delete endpoints!")

if __name__ == "__main__":
    test_admin_assets()
    print("ALL FRONTEND ASSET CHECKS PASSED SUCCESSFULLY!")
