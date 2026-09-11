#!/usr/bin/env python3
"""
PostgreSQL pgvector Master Database Deployment Script
------------------------------------------------------
Deploys schema and uploads both:
  1. 500 Benchmark Companies (500_companies_analysis.json) - 11-D & 384-D vector CVP matching.
  2. News Articles (db_ready_news_202607.csv & db_ready_news_202608.csv) - 11-D vector market events.

Supports both local PostgreSQL Docker containers and Cloud Supabase instances.

Requirements:
  pip install psycopg2-binary pgvector

Usage Examples:
  # Deploy to local PostgreSQL Docker container (default: postgresql://postgres:postgres@localhost:5432/postgres)
  python deploy_pgvector.py

  # Deploy to Supabase Cloud or custom URL:
  python deploy_pgvector.py --db-url "postgresql://postgres.xxx:YOUR_PASSWORD@aws-0-us-east-1.pooler.supabase.com:5432/postgres"
"""

import argparse
import csv
import json
import logging
import os
import re
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("PgvectorDeployer")

SCHEMA_SQL_PATH = Path(__file__).parent / "schema.sql"
DEFAULT_COMPANIES_JSON = Path(__file__).parent.parent / "500_companies_analysis.json"


def read_schema_sql() -> str:
    if SCHEMA_SQL_PATH.exists():
        with open(SCHEMA_SQL_PATH, "r", encoding="utf-8") as f:
            return f.read()
    else:
        logger.error(f"Schema SQL file '{SCHEMA_SQL_PATH}' not found.")
        sys.exit(1)


def upload_benchmark_companies(cursor, companies_json_path: Path):
    if not companies_json_path.exists():
        logger.warning(f"Companies JSON file '{companies_json_path}' not found. Skipping company upload.")
        return

    logger.info(f"Loading 500 Benchmark Companies from '{companies_json_path.name}'...")
    with open(companies_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    companies_list = data if isinstance(data, list) else data.get("companies", [])
    logger.info(f"Uploading {len(companies_list)} benchmark companies into 'benchmark_companies' table...")

    from psycopg2.extras import execute_values

    insert_sql = """
        INSERT INTO benchmark_companies (
            id, company, sector, target_customer, statement_of_need, product_name,
            product_category, statement_of_key_benefit, cvp, pestle_json, porters_json,
            strategic_embedding_11d, cvp_embedding_384d
        ) VALUES %s
        ON CONFLICT (id) DO UPDATE SET
            company = EXCLUDED.company,
            sector = EXCLUDED.sector,
            target_customer = EXCLUDED.target_customer,
            statement_of_need = EXCLUDED.statement_of_need,
            product_name = EXCLUDED.product_name,
            product_category = EXCLUDED.product_category,
            statement_of_key_benefit = EXCLUDED.statement_of_key_benefit,
            cvp = EXCLUDED.cvp,
            pestle_json = EXCLUDED.pestle_json,
            porters_json = EXCLUDED.porters_json,
            strategic_embedding_11d = EXCLUDED.strategic_embedding_11d,
            cvp_embedding_384d = EXCLUDED.cvp_embedding_384d;
    """

    batch = []
    for c in companies_list:
        comp_id = c.get("id") or f"comp_{hash(c.get('company', ''))}"
        s_11d = c.get("strategic_embedding_11d", [0.05] * 11)
        c_384d = c.get("cvp_embedding_384d", [0.0] * 384)

        vec_11d_str = f"[{','.join(f'{v:.4f}' for v in s_11d)}]"
        vec_384d_str = f"[{','.join(f'{v:.4f}' for v in c_384d)}]"

        batch.append((
            comp_id,
            c.get("company", ""),
            c.get("sector", ""),
            c.get("target_customer", ""),
            c.get("statement_of_need", ""),
            c.get("product_name", ""),
            c.get("product_category", ""),
            c.get("statement_of_key_benefit", ""),
            c.get("cvp", ""),
            json.dumps(c.get("pestle", {})),
            json.dumps(c.get("porters", {})),
            vec_11d_str,
            vec_384d_str
        ))

    execute_values(cursor, insert_sql, batch)
    logger.info(f"SUCCESS: Uploaded {len(batch)} benchmark companies to 'benchmark_companies' table!")


def normalize_date_iso(date_str: str) -> str:
    """Normalizes any date string (YYYY-MM-DD, DD-MM-YYYY, YYYYMMDD) into standard ISO YYYY-MM-DD format for PostgreSQL."""
    if not date_str:
        return "2026-01-01"
    clean = str(date_str).strip()
    if len(clean) == 8 and clean.isdigit():
        return f"{clean[:4]}-{clean[4:6]}-{clean[6:8]}"
    if re.match(r"^\d{1,2}[-/]\d{1,2}[-/]\d{4}$", clean):
        parts = re.split(r"[-/]", clean)
        day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
        return f"{year:04d}-{month:02d}-{day:02d}"
    if re.match(r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}$", clean):
        parts = re.split(r"[-/]", clean)
        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
        return f"{year:04d}-{month:02d}-{day:02d}"
    return clean


def upload_news_articles(cursor, csv_files: list, batch_size: int = 1000):
    from psycopg2.extras import execute_values

    insert_sql = """
        INSERT INTO news_articles (id, published_date, headline, strategic_embedding_11d, source_link, location_affected, impact_score)
        VALUES %s
        ON CONFLICT (id) DO UPDATE SET
            headline = EXCLUDED.headline,
            strategic_embedding_11d = EXCLUDED.strategic_embedding_11d,
            source_link = EXCLUDED.source_link,
            location_affected = EXCLUDED.location_affected,
            impact_score = EXCLUDED.impact_score;
    """

    total_uploaded = 0
    for csv_path_str in csv_files:
        csv_path = Path(csv_path_str).resolve()
        if not csv_path.exists():
            logger.warning(f"File '{csv_path}' not found. Skipping.")
            continue

        logger.info(f"Uploading news records from '{csv_path.name}'...")
        batch = []
        file_count = 0

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rec_id = row.get("id")
                date_str = normalize_date_iso(row.get("date"))
                headline = row.get("headline", "")
                vec_str = row.get("strategic_embedding_11d", "[0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05]")
                link = row.get("source_link", "")
                loc = row.get("location_affected", "World")
                impact = float(row.get("impact_score", 0.05))

                if rec_id and date_str:
                    batch.append((rec_id, date_str, headline, vec_str, link, loc, impact))
                    file_count += 1

                if len(batch) >= batch_size:
                    execute_values(cursor, insert_sql, batch)
                    total_uploaded += len(batch)
                    batch = []

            if batch:
                execute_values(cursor, insert_sql, batch)
                total_uploaded += len(batch)

        logger.info(f"Uploaded {file_count} news records from '{csv_path.name}'.")

    logger.info(f"SUCCESS: Uploaded {total_uploaded} news records to 'news_articles' table.")


def deploy_to_postgresql(db_url: str, companies_json: Path, csv_files: list, batch_size: int = 1000, purge_inputs: bool = False):
    try:
        import psycopg2
    except ImportError:
        logger.error(
            "psycopg2 is not installed. Please install it using: pip install psycopg2-binary pgvector"
        )
        sys.exit(1)

    logger.info(f"Connecting to PostgreSQL database...")
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cursor = conn.cursor()
        logger.info("Connected to PostgreSQL successfully!")
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL at '{db_url}': {e}")
        logger.info("\n=== HOW TO FIX THIS ===")
        logger.info("If running Docker locally, execute this 1-liner to start PostgreSQL with pgvector:")
        logger.info("  docker run -d --name pgvector -e POSTGRES_PASSWORD=postgres -p 5432:5432 pgvector/pgvector:pg16\n")
        sys.exit(1)

    # 1. Create Schema
    logger.info("Initializing database schema & HNSW vector indexes...")
    schema_sql = read_schema_sql()
    cursor.execute(schema_sql)
    logger.info("Schema initialized successfully!")

    # 2. Upload Benchmark Companies
    upload_benchmark_companies(cursor, companies_json)

    # 3. Upload News Articles
    upload_news_articles(cursor, csv_files, batch_size=batch_size)

    cursor.close()
    conn.close()
    logger.info("\nMASTER DEPLOYMENT COMPLETE! Both 500 Companies and News Datasets are live in PostgreSQL!")

    if purge_inputs:
        logger.info("Purging processed intermediate news CSV files...")
        purged = 0
        for csv_path_str in csv_files:
            p = Path(csv_path_str).resolve()
            try:
                if p.exists():
                    p.unlink()
                    purged += 1
            except Exception as e:
                logger.warning(f"Could not delete intermediate CSV '{p}': {e}")
        logger.info(f"AUTO-PURGE COMPLETE: Deleted {purged} intermediate news CSV file(s). Storage freed up!")


def main():
    parser = argparse.ArgumentParser(
        description="Deploy 500 Benchmark Companies & News Datasets into PostgreSQL with pgvector."
    )
    parser.add_argument(
        "--db-url",
        type=str,
        default=os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres"),
        help="PostgreSQL connection string.",
    )
    parser.add_argument(
        "--companies-json",
        type=str,
        default=str(DEFAULT_COMPANIES_JSON),
        help="Path to 500_companies_analysis.json.",
    )
    parser.add_argument(
        "--csv",
        nargs="+",
        default=["stage3_enrich_and_store/db_ready_news_202607.csv", "stage3_enrich_and_store/db_ready_news_202608.csv"],
        help="Paths to DB-ready news CSV files.",
    )
    parser.add_argument(
        "--purge-processed-inputs",
        action="store_true",
        help="Automatically delete intermediate news CSV files after successful database deployment.",
    )

    args = parser.parse_args()
    deploy_to_postgresql(args.db_url, Path(args.companies_json), args.csv, purge_inputs=args.purge_processed_inputs)


if __name__ == "__main__":
    main()
