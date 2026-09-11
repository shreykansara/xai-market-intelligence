#!/usr/bin/env python3
"""
Multi-Stage Online Inspection Dashboard Server (Flask Edition)
--------------------------------------------------------------
Provides separate online inspection interfaces for Level 1 (Raw GDELT), Level 2 (Filtered News),
Level 3 (Live Database & 11-D Vectors), and Pipeline Stage Controls.

Usage:
  python server.py
  (Opens web dashboard at http://localhost:5000)
"""

import csv
import io
import json
import zipfile
import logging
import os
import re
import sys
import subprocess
import threading
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory, render_template_string
import numpy as np

# Import Hugging Face Cloud Embedding API
from cloud_embeddings import get_cloud_text_embedding

BASE_DIR = Path(__file__).parent.resolve()
WEB_DIR = BASE_DIR / "web"
GDELT_DATA_DIR = BASE_DIR / "gdelt_data"
STAGE2_DIR = BASE_DIR / "stage2_filter"
STAGE3_DIR = BASE_DIR / "stage3_enrich_and_store"
WEIGHTS_PATH = BASE_DIR / "strategic_projection_matrix.npz"

app = Flask(__name__, static_folder=str(WEB_DIR), static_url_path="")

# Load Matrix Projection Weights for Live 11-D Vector Projection
W_MATRIX = None
B_BIAS = None
if WEIGHTS_PATH.exists():
    try:
        data = np.load(WEIGHTS_PATH)
        W_MATRIX = data["W"].astype(np.float32)
        B_BIAS = data["b"].astype(np.float32)
        print(f"[Server] Loaded Projection Matrix W: {W_MATRIX.shape}, Bias b: {B_BIAS.shape}")
    except Exception as e:
        print(f"[Server] Warning: Failed to load projection matrix: {e}")

DEFAULT_SUPABASE_URL = "postgresql://postgres.fqmrguogcptkpsbhdmgo:efO5FSkBGg8iQlws@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres"


# Import ChatbotEngine for End-User Chatbot UI
from chatbot_engine import ChatbotEngine, GroqOllamaProvider
chatbot_engine = ChatbotEngine()


@app.route("/")
def index():
    """End-User Facing Omniscope Market Intelligence Chatbot UI."""
    return send_from_directory(str(WEB_DIR), "index.html")


@app.route("/admin")
@app.route("/admin/console")
def admin_console():
    """Dedicated Platform Administrator Stage Console UI."""
    return send_from_directory(str(WEB_DIR), "admin.html")


# ==========================================
# END-USER CHATBOT & CVP API ENDPOINTS
# ==========================================
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json or {}
    message = data.get("message", "")
    business_context = data.get("business_context") or data.get("context")
    groq_key = data.get("groq_key")
    chat_history = data.get("chat_history", [])

    if not message:
        return jsonify({"error": "Message is required"}), 400

    try:
        response = chatbot_engine.process_message(
            user_message=message,
            user_business_context=business_context,
            groq_key_override=groq_key,
            chat_history=chat_history
        )
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Global Ingestion Progress State for Level 1
STAGE1_PROGRESS = {
    "status": "idle",
    "progress_pct": 0,
    "current_date": "",
    "processed_files": 0,
    "total_files": 0,
    "total_size_mb": 0.0,
    "total_raw_articles": 0,
    "message": ""
}


def run_stage1_ingestion_background(s_date_str: str, e_date_str: str, db_url: str):
    global STAGE1_PROGRESS
    try:
        s_clean = s_date_str.replace("-", "").strip()
        e_clean = e_date_str.replace("-", "").strip()
        start_dt = datetime.strptime(s_clean, "%Y%m%d")
        end_dt = datetime.strptime(e_clean, "%Y%m%d")
        
        dates = []
        curr = start_dt
        while curr <= end_dt:
            dates.append(curr)
            curr += timedelta(days=1)
            
        total_days = len(dates)
        STAGE1_PROGRESS = {
            "status": "running",
            "progress_pct": 0,
            "current_date": start_dt.strftime("%Y-%m-%d"),
            "processed_files": 0,
            "total_files": total_days,
            "total_size_mb": 0.0,
            "total_raw_articles": 0,
            "message": f"Starting zero-disk in-memory stream ingestion for {total_days} date(s)..."
        }
        
        total_size_bytes = 0
        total_raw_count = 0

        # Connect to Supabase PostgreSQL database
        import psycopg2
        import psycopg2.extras
        db_conn = psycopg2.connect(db_url or DEFAULT_SUPABASE_URL, connect_timeout=15)
        db_conn.autocommit = True
        db_cur = db_conn.cursor()

        # Ensure schema tables exist in Supabase
        db_cur.execute("""
            CREATE TABLE IF NOT EXISTS raw_gdelt_exports (
                id VARCHAR(255) PRIMARY KEY,
                export_date DATE NOT NULL,
                filename VARCHAR(255) NOT NULL,
                file_size_bytes BIGINT NOT NULL DEFAULT 0,
                raw_articles_count INTEGER NOT NULL DEFAULT 0,
                status VARCHAR(50) DEFAULT 'INGESTED',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            ALTER TABLE raw_gdelt_exports ADD COLUMN IF NOT EXISTS raw_articles_count INTEGER NOT NULL DEFAULT 0;

            CREATE TABLE IF NOT EXISTS raw_gdelt_news (
                id VARCHAR(255) PRIMARY KEY,
                global_event_id VARCHAR(100) NOT NULL,
                published_date DATE NOT NULL,
                actor1_name VARCHAR(255),
                actor2_name VARCHAR(255),
                event_code VARCHAR(50),
                action_geo_country VARCHAR(100),
                source_url TEXT NOT NULL,
                status VARCHAR(50) DEFAULT 'RAW',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_raw_news_date ON raw_gdelt_news (published_date DESC);
        """)

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            )
        }

        for idx, dt in enumerate(dates):
            date_fmt = dt.strftime("%Y-%m-%d")
            date_str = dt.strftime("%Y%m%d")
            zip_filename = f"{date_str}.export.CSV.zip"
            download_url = f"http://data.gdeltproject.org/events/{zip_filename}"

            STAGE1_PROGRESS["current_date"] = date_fmt
            STAGE1_PROGRESS["message"] = f"Streaming & unzipping GDELT export for {date_fmt} in-memory..."
            
            # Fetch zip file directly into RAM buffer
            req = urllib.request.Request(download_url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as resp:
                zip_bytes = resp.read()

            file_size = len(zip_bytes)
            total_size_bytes += file_size

            # Unzip and parse CSV rows in RAM
            raw_tuples = []
            with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
                for fname in z.namelist():
                    with z.open(fname) as f:
                        text_stream = io.TextIOWrapper(f, encoding='latin-1', errors='replace')
                        reader = csv.reader(text_stream, delimiter='\t')
                        for row in reader:
                            if len(row) >= 58:
                                global_event_id = row[0].strip()
                                actor1 = row[6].strip()[:255] if row[6] else ""
                                actor2 = row[16].strip()[:255] if row[16] else ""
                                event_code = row[26].strip()[:50] if row[26] else ""
                                geo_country = (row[52] or row[53] or "").strip()[:100]
                                source_url = row[57].strip() if row[57] else ""
                                
                                if source_url.startswith("http") and global_event_id:
                                    raw_tuples.append((
                                        f"gdelt_raw_{global_event_id}",
                                        global_event_id,
                                        date_fmt,
                                        actor1,
                                        actor2,
                                        event_code,
                                        geo_country,
                                        source_url,
                                        "RAW"
                                    ))

            # Direct Batch Insert into Supabase raw_gdelt_news table
            if raw_tuples:
                insert_query = """
                    INSERT INTO raw_gdelt_news 
                    (id, global_event_id, published_date, actor1_name, actor2_name, event_code, action_geo_country, source_url, status)
                    VALUES %s
                    ON CONFLICT (id) DO NOTHING;
                """
                psycopg2.extras.execute_values(db_cur, insert_query, raw_tuples, page_size=2000)
                total_raw_count += len(raw_tuples)

            # Record Ingestion Export Log in Supabase
            db_cur.execute("""
                INSERT INTO raw_gdelt_exports (id, export_date, filename, file_size_bytes, raw_articles_count, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    file_size_bytes = EXCLUDED.file_size_bytes,
                    raw_articles_count = EXCLUDED.raw_articles_count,
                    status = EXCLUDED.status;
            """, (
                f"gdelt_zip_{date_str}",
                date_fmt,
                zip_filename,
                file_size,
                len(raw_tuples),
                "INGESTED"
            ))

            STAGE1_PROGRESS["processed_files"] = idx + 1
            STAGE1_PROGRESS["total_size_mb"] = round(total_size_bytes / (1024 * 1024), 2)
            STAGE1_PROGRESS["total_raw_articles"] = total_raw_count
            STAGE1_PROGRESS["progress_pct"] = int(((idx + 1) / total_days) * 100)
            STAGE1_PROGRESS["message"] = f"Ingested {len(raw_tuples):,} raw news events for {date_fmt} directly into database."

        db_cur.close()
        db_conn.close()

        STAGE1_PROGRESS["status"] = "completed"
        STAGE1_PROGRESS["progress_pct"] = 100
        STAGE1_PROGRESS["message"] = (
            f"Zero-Disk Ingestion Complete! Fetched {total_days} GDELT archive(s) ({STAGE1_PROGRESS['total_size_mb']} MB) "
            f"and appended {total_raw_count:,} raw news events directly into Supabase database."
        )
    except Exception as e:
        STAGE1_PROGRESS["status"] = "error"
        STAGE1_PROGRESS["message"] = f"Ingestion Error: {str(e)}"


# ==========================================
# LEVEL 1 API: STAGE 1 RAW DATA INSPECTOR
# ==========================================
@app.route("/api/stage1/files", methods=["GET"])
def get_stage1_files():
    files = []
    if GDELT_DATA_DIR.exists():
        for p in sorted(GDELT_DATA_DIR.glob("*"), reverse=True):
            if p.is_file():
                files.append({
                    "filename": p.name,
                    "size_mb": round(p.stat().st_size / (1024 * 1024), 2),
                    "modified": p.stat().st_mtime
                })
    return jsonify({"success": True, "files": files, "count": len(files)})


@app.route("/api/stage1/ingest", methods=["POST"])
def trigger_stage1_ingest():
    data = request.json or {}
    s_date = data.get("start_date")
    e_date = data.get("end_date")
    db_url = data.get("db_url", DEFAULT_SUPABASE_URL)

    if not s_date or not e_date:
        return jsonify({"success": False, "error": "start_date and end_date required"}), 400

    if STAGE1_PROGRESS["status"] == "running":
        return jsonify({"success": False, "error": "Ingestion is already running."}), 400

    t = threading.Thread(target=run_stage1_ingestion_background, args=(s_date, e_date, db_url), daemon=True)
    t.start()
    return jsonify({"success": True, "message": f"Ingestion started for {s_date} to {e_date}."})


@app.route("/api/stage1/progress", methods=["GET"])
def get_stage1_progress():
    return jsonify(STAGE1_PROGRESS)


@app.route("/api/stage1/trigger", methods=["POST"])
def trigger_stage1():
    data = request.json or {}
    s_date = data.get("start_date")
    e_date = data.get("end_date")
    if not s_date or not e_date:
        return jsonify({"success": False, "error": "start_date and end_date required"}), 400

    cmd = [
        sys.executable, str(BASE_DIR / "pipeline_controller.py"),
        "--stage", "1", "--start-date", s_date, "--end-date", e_date
    ]
    try:
        subprocess.Popen(cmd)
        return jsonify({"success": True, "message": f"Stage 1 download triggered for {s_date} to {e_date}."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==========================================
# LEVEL 2 API: STAGE 2 FILTERED NEWS INSPECTOR
# ==========================================
@app.route("/api/stage2/records", methods=["GET"])
def get_stage2_records():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))
    search = request.args.get("search", "").lower()
    location_filter = request.args.get("location", "")

    csv_candidates = list(STAGE2_DIR.glob("*.csv")) + [BASE_DIR / "filtered_news.csv"]
    records = []
    
    for csv_file in csv_candidates:
        if csv_file.exists():
            try:
                with open(csv_file, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for r in reader:
                        headline = r.get("headline", "")
                        loc = r.get("location_affected", "")
                        
                        if search and search not in headline.lower():
                            continue
                        if location_filter and location_filter != loc:
                            continue
                            
                        records.append({
                            "id": r.get("id"),
                            "date": r.get("date"),
                            "headline": headline,
                            "text_snippet": r.get("text", "")[:300],
                            "source_link": r.get("source_link"),
                            "location_affected": loc
                        })
            except Exception:
                pass

    total = len(records)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated = records[start_idx:end_idx]

    return jsonify({
        "success": True,
        "records": paginated,
        "total": total,
        "page": page,
        "pages": max(1, (total + per_page - 1) // per_page)
    })


@app.route("/api/stage2/trigger", methods=["POST"])
def trigger_stage2():
    cmd = [
        sys.executable, str(BASE_DIR / "pipeline_controller.py"),
        "--stage", "2", "--auto-purge"
    ]
    try:
        subprocess.Popen(cmd)
        return jsonify({"success": True, "message": "Stage 2 Irrelevant News Filtering triggered with Auto-Purge."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==========================================
# LEVEL 3 API: STAGE 3 DB & 11-D VECTOR INSPECTOR
# ==========================================
@app.route("/api/stage3/db-status", methods=["GET"])
def get_stage3_db_status():
    db_url = request.args.get("db_url", DEFAULT_SUPABASE_URL)
    try:
        import psycopg2
        conn = psycopg2.connect(db_url, connect_timeout=5)
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM benchmark_companies;")
        comp_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM news_articles;")
        news_count = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "connected": True,
            "benchmark_companies_count": comp_count,
            "news_articles_count": news_count,
            "db_provider": "Supabase PostgreSQL (pgvector)"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "connected": False,
            "error": str(e)
        })


@app.route("/api/stage3/companies", methods=["GET"])
def get_stage3_companies():
    db_url = request.args.get("db_url", DEFAULT_SUPABASE_URL)
    limit = int(request.args.get("limit", 20))
    search = request.args.get("search", "").lower()
    
    try:
        import psycopg2
        conn = psycopg2.connect(db_url, connect_timeout=5)
        cur = conn.cursor()
        
        query = "SELECT id, company, sector, product_name, cvp, strategic_embedding_11d::text FROM benchmark_companies "
        params = []
        if search:
            query += "WHERE LOWER(company) LIKE %s OR LOWER(sector) LIKE %s "
            params.extend([f"%{search}%", f"%{search}%"])
        query += "LIMIT %s;"
        params.append(limit)
        
        cur.execute(query, params)
        rows = cur.fetchall()
        
        companies = []
        for r in rows:
            vec_11d = []
            try:
                vec_11d = json.loads(r[5])
            except Exception:
                pass
                
            companies.append({
                "id": r[0],
                "company": r[1],
                "sector": r[2],
                "product_name": r[3],
                "cvp": r[4],
                "strategic_11d": vec_11d
            })
            
        cur.close()
        conn.close()
        return jsonify({"success": True, "companies": companies, "count": len(companies)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/api/stage3/news", methods=["GET"])
def get_stage3_news():
    db_url = request.args.get("db_url", DEFAULT_SUPABASE_URL)
    limit = int(request.args.get("limit", 20))
    location = request.args.get("location", "")
    min_impact = float(request.args.get("min_impact", 0.20))
    
    try:
        import psycopg2
        conn = psycopg2.connect(db_url, connect_timeout=5)
        cur = conn.cursor()
        
        query = "SELECT id, published_date, headline, location_affected, impact_score, strategic_embedding_11d::text, source_link FROM news_articles WHERE impact_score >= %s "
        params = [min_impact]
        
        if location:
            query += "AND location_affected = %s "
            params.append(location)
            
        query += "ORDER BY published_date DESC, impact_score DESC LIMIT %s;"
        params.append(limit)
        
        cur.execute(query, params)
        rows = cur.fetchall()
        
        news_items = []
        for r in rows:
            vec_11d = []
            try:
                vec_11d = json.loads(r[5])
            except Exception:
                pass
                
            news_items.append({
                "id": r[0],
                "date": str(r[1]),
                "headline": r[2],
                "location_affected": r[3],
                "impact_score": r[4],
                "strategic_11d": vec_11d,
                "source_link": r[6]
            })
            
        cur.close()
        conn.close()
        return jsonify({"success": True, "news_items": news_items, "count": len(news_items)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/api/stage3/project-headline", methods=["POST"])
def project_headline_live():
    """Projects any custom headline live into 11-D PESTLE & Porter scores using Cloud API + Matrix Model."""
    data = request.json or {}
    headline = data.get("headline", "")
    if not headline:
        return jsonify({"success": False, "error": "Headline text required"}), 400

    # Step 1: Fetch Cloud 768-D Vector via Hugging Face API
    c_emb_768d = get_cloud_text_embedding(headline)

    # Step 2: Apply Matrix Multiplication
    if W_MATRIX is not None and B_BIAS is not None:
        x = np.array(c_emb_768d, dtype=np.float32)
        if x.shape[0] != W_MATRIX.shape[0]:
            if x.shape[0] < W_MATRIX.shape[0]:
                x = np.pad(x, (0, W_MATRIX.shape[0] - x.shape[0]))
            else:
                x = x[:W_MATRIX.shape[0]]

        y_raw = np.dot(x, W_MATRIX) + B_BIAS
        y_clipped = np.clip(y_raw, 0.05, 0.95)
        vector_11d = [round(float(v), 4) for v in y_clipped]
    else:
        vector_11d = [0.05] * 11

    dimensions = [
        "Political", "Economic", "Social", "Technological", "Legal", "Environmental",
        "Threat of Entrants", "Buyer Power", "Supplier Power", "Threat of Substitutes", "Rivalry"
    ]
    
    sorted_s = sorted(vector_11d, reverse=True)
    peak = sorted_s[0]
    top2 = sum(sorted_s[:2]) / 2.0
    impact_score = round(float((peak * 0.60) + (top2 * 0.40)), 3)

    return jsonify({
        "success": True,
        "headline": headline,
        "strategic_11d": vector_11d,
        "impact_score": impact_score,
        "driver_breakdown": dict(zip(dimensions, vector_11d))
    })


@app.route("/api/stage3/trigger", methods=["POST"])
def trigger_stage3():
    data = request.json or {}
    db_url = data.get("db_url", DEFAULT_SUPABASE_URL)
    cmd = [
        sys.executable, str(BASE_DIR / "pipeline_controller.py"),
        "--stage", "3", "--db-url", db_url, "--auto-purge"
    ]
    try:
        subprocess.Popen(cmd)
        return jsonify({"success": True, "message": "Stage 3 11-D Matrix Projection & DB Export triggered with Auto-Purge."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    GDELT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    print("Starting AI Market Intelligence Dashboard Server on http://localhost:5000 ...")
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
