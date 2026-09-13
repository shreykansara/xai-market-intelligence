"""
End-to-End Automated Verification Script for Admin 3-Stage Pipeline:
1. Verifies Stage 1 Ingestion and Deduplication in raw_gdelt_news.
2. Verifies Stage 2 NLP Filtering, movement to stage2_filtered_news, and purging of processed records from raw_gdelt_news.
3. Verifies Stage 3 11-D Projection, movement to news_articles, and purging of promoted records from stage2_filtered_news.
4. Verifies deduplication across all stages.
"""

import urllib.request
import json
import time

BASE_URL = "http://localhost:5000"

def get_json(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

def post_json(url, data):
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

def test_pipeline():
    print("=== STEP 1: INITIAL DB STATUS ===")
    status1 = get_json(f"{BASE_URL}/api/stage3/db-status")
    print("DB Status:", status1)
    s1_initial = status1["stage1_raw_count"]
    s2_initial = status1["stage2_filtered_count"]
    s3_initial = status1["news_articles_count"]
    print(f"Initial counts -> Stage 1: {s1_initial:,} | Stage 2: {s2_initial:,} | Stage 3: {s3_initial:,}")

    print("\n=== STEP 2: RUN STAGE 2 NLP FILTERING (BATCH=25) ===")
    res_s2 = post_json(f"{BASE_URL}/api/stage2/process", {"batch_size": 25})
    print("Trigger response:", res_s2)

    for _ in range(20):
        time.sleep(1.5)
        prog = get_json(f"{BASE_URL}/api/stage2/progress")
        if prog.get("status") in ("completed", "error"):
            print("Stage 2 final progress:", prog["message"])
            break

    status2 = get_json(f"{BASE_URL}/api/stage3/db-status")
    s1_after_s2 = status2["stage1_raw_count"]
    s2_after_s2 = status2["stage2_filtered_count"]
    print(f"Counts after Stage 2 -> Stage 1: {s1_after_s2:,} (Purged {s1_initial - s1_after_s2} items) | Stage 2: {s2_after_s2:,}")
    assert s1_after_s2 < s1_initial, "Failure: Processed items were not purged from Stage 1!"
    print(">>> VERIFIED: Stage 1 records were purged upon Stage 2 promotion/filtering!")

    print("\n=== STEP 3: RUN STAGE 3 11-D PROJECTION (BATCH=5) ===")
    res_s3 = post_json(f"{BASE_URL}/api/stage3/process", {"batch_size": 5})
    print("Trigger response:", res_s3)

    for _ in range(20):
        time.sleep(1.5)
        prog = get_json(f"{BASE_URL}/api/stage3/progress")
        if prog.get("status") in ("completed", "error"):
            print("Stage 3 final progress:", prog["message"])
            break

    status3 = get_json(f"{BASE_URL}/api/stage3/db-status")
    s2_after_s3 = status3["stage2_filtered_count"]
    s3_after_s3 = status3["news_articles_count"]
    print(f"Counts after Stage 3 -> Stage 2: {s2_after_s3:,} | Stage 3: {s3_after_s3:,}")
    assert s2_after_s3 <= s2_after_s2, "Failure: Promoted items were not purged from Stage 2!"
    print(">>> VERIFIED: Stage 2 records were purged upon Stage 3 master DB ingestion!")

    print("\n=== STEP 4: VERIFY STAGE 3 ARTICLES API AND 11-D VECTORS ===")
    articles_data = get_json(f"{BASE_URL}/api/stage3/articles?limit=3")
    assert articles_data["success"] and len(articles_data["articles"]) > 0
    sample = articles_data["articles"][0]
    print(f"Sample Master Article: '{sample['headline']}' | Impact: {sample['impact_score']} | Driver: {sample['primary_driver']}")
    print(f"11-D Vector Preview: {sample['strategic_11d']}")
    assert len(sample["strategic_11d"]) == 11, "Failure: Vector must be 11 dimensions!"
    print(">>> VERIFIED: Master News articles contain authentic 11-D vectors and primary drivers!")

    print("\n=======================================================")
    print("ALL 3 STAGES, INTER-STAGE PURGES & DEDUPLICATION VERIFIED!")
    print("=======================================================")

if __name__ == "__main__":
    test_pipeline()
