#!/usr/bin/env python3
"""
MASTER PIPELINE CONTROLLER & STAGE ORCHESTRATOR
------------------------------------------------
Controls stage-by-stage execution of the Market Intelligence news pipeline with
manual triggers and automatic stage-to-stage garbage collection.

Pipeline Flow:
  STAGE 1: Fetch raw GDELT zip exports for date range (stores in gdelt_data/)
  STAGE 2: Scrape & filter irrelevant news (stores in stage2_filter/filtered_news.csv, THEN PURGES Stage 1 raw zip files)
  STAGE 3: Project 11-D vectors & upload to Database (inserts into PostgreSQL/Supabase, THEN PURGES Stage 2 filtered CSV files)

Usage Examples:
  # Run Stage 1 manually for a date range:
  python pipeline_controller.py --stage 1 --start-date 2026-09-01 --end-date 2026-09-05

  # Run Stage 2 manually (filters raw zip files, then automatically purges Stage 1 zip files):
  python pipeline_controller.py --stage 2 --auto-purge

  # Run Stage 3 manually (uploads to PostgreSQL/Supabase, then automatically purges Stage 2 CSV files):
  python pipeline_controller.py --stage 3 --db-url "YOUR_POSTGRES_OR_SUPABASE_URI" --auto-purge

  # Run Full Interactive Menu:
  python pipeline_controller.py
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
STAGE1_SCRIPT = BASE_DIR / "stage1_fetcher" / "fetch_gdelt_zipped.py"
STAGE2_SCRIPT = BASE_DIR / "stage2_filter" / "filter_gdelt_news.py"
STAGE3_SCRIPT = BASE_DIR / "stage3_enrich_and_store" / "deploy_pgvector.py"
PREPARE_SCRIPT = BASE_DIR / "prepare_db_dataset.py"


def print_banner():
    print("=" * 75)
    print("      AI MARKET INTELLIGENCE: MASTER STAGE PIPELINE CONTROLLER")
    print("=" * 75)


def run_stage_1(start_date: str, end_date: str, output_dir: str = "gdelt_data"):
    print(f"\n[PIPELINE CONTROLLER] >>> Triggering STAGE 1 (Fetch GDELT Raw Zips)...")
    cmd = [
        sys.executable, str(STAGE1_SCRIPT),
        "--start-date", start_date,
        "--end-date", end_date,
        "--output-dir", output_dir
    ]
    res = subprocess.run(cmd)
    if res.returncode == 0:
        print(f"[PIPELINE CONTROLLER] Stage 1 Completed! Raw files stored in '{output_dir}/'.")
        print("Ready for Stage 2 conversion whenever you press/run Stage 2.")
    else:
        print("[PIPELINE CONTROLLER] Stage 1 failed.")


def run_stage_2(input_dir: str = "gdelt_data", output_csv: str = "stage2_filter/filtered_news.csv", auto_purge: bool = True):
    print(f"\n[PIPELINE CONTROLLER] >>> Triggering STAGE 2 (Filter & Scrape Irrelevant News)...")
    cmd = [
        sys.executable, str(STAGE2_SCRIPT),
        "--input-dir", input_dir,
        "--output", output_csv,
        "--workers", "8"
    ]
    if auto_purge:
        cmd.append("--purge-processed-inputs")

    res = subprocess.run(cmd)
    if res.returncode == 0:
        print(f"[PIPELINE CONTROLLER] Stage 2 Completed! Clean news stored in '{output_csv}'.")
        if auto_purge:
            print(f"[PIPELINE CONTROLLER] AUTO-PURGE: Processed Stage 1 raw zip files in '{input_dir}' were deleted to save disk space.")
        print("Ready for Stage 3 DB deployment whenever you press/run Stage 3.")
    else:
        print("[PIPELINE CONTROLLER] Stage 2 failed.")


def run_stage_3(input_csv: str = "stage2_filter/filtered_news.csv", db_url: str = None, auto_purge: bool = True):
    print(f"\n[PIPELINE CONTROLLER] >>> Triggering STAGE 3 (11-D Projection & DB Export)...")
    
    # First, prepare DB-ready CSV (strip 768-D vectors, compute 11-D impact scores)
    db_ready_csv = Path(input_csv).parent / f"db_ready_{Path(input_csv).name}"
    prep_cmd = [
        sys.executable, str(PREPARE_SCRIPT),
        "--input", input_csv,
        "--output", str(db_ready_csv)
    ]
    print(f"[PIPELINE CONTROLLER] Formatting 11-D strategic vectors into '{db_ready_csv.name}'...")
    res_prep = subprocess.run(prep_cmd)
    if res_prep.returncode != 0:
        print("[PIPELINE CONTROLLER] Stage 3 preparation failed.")
        return

    # Second, upload to PostgreSQL / Supabase
    db_url_effective = db_url or os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
    cmd = [
        sys.executable, str(STAGE3_SCRIPT),
        "--db-url", db_url_effective,
        "--csv", str(db_ready_csv)
    ]
    if auto_purge:
        cmd.append("--purge-processed-inputs")

    res = subprocess.run(cmd)
    if res.returncode == 0:
        print(f"[PIPELINE CONTROLLER] Stage 3 Completed! Data is live in PostgreSQL/Supabase!")
        if auto_purge:
            # Delete both Stage 2 filtered CSV and db_ready CSV
            for p in [Path(input_csv), db_ready_csv]:
                try:
                    if p.exists():
                        p.unlink()
                except Exception:
                    pass
            print(f"[PIPELINE CONTROLLER] AUTO-PURGE: Processed Stage 2 intermediate CSV files were deleted. Storage freed up!")
    else:
        print("[PIPELINE CONTROLLER] Stage 3 database deployment failed.")


def interactive_menu():
    print_banner()
    while True:
        print("\nSELECT PIPELINE STAGE TO TRIGGER:")
        print("  [1] Stage 1: Fetch Raw GDELT Zip Files (Store in gdelt_data/)")
        print("  [2] Stage 2: Filter Irrelevant News (Process Stage 1 -> Auto-Purge Stage 1 Zips)")
        print("  [3] Stage 3: Project 11-D & Upload to DB (Process Stage 2 -> Auto-Purge Stage 2 CSVs)")
        print("  [4] Run All Stages Sequentially (Stage 1 -> Stage 2 -> Stage 3 with Auto-Purge)")
        print("  [Q] Quit")
        
        choice = input("\nEnter choice (1/2/3/4/Q): ").strip().upper()
        
        if choice == "1":
            s_date = input("Enter start date (YYYY-MM-DD): ").strip()
            e_date = input("Enter end date (YYYY-MM-DD): ").strip()
            if s_date and e_date:
                run_stage_1(s_date, e_date)
        elif choice == "2":
            run_stage_2(auto_purge=True)
        elif choice == "3":
            url = input("Enter PostgreSQL / Supabase DB URL (Press Enter for default env): ").strip()
            run_stage_3(db_url=url if url else None, auto_purge=True)
        elif choice == "4":
            s_date = input("Enter start date (YYYY-MM-DD): ").strip()
            e_date = input("Enter end date (YYYY-MM-DD): ").strip()
            url = input("Enter PostgreSQL / Supabase DB URL (Press Enter for default env): ").strip()
            if s_date and e_date:
                run_stage_1(s_date, e_date)
                run_stage_2(auto_purge=True)
                run_stage_3(db_url=url if url else None, auto_purge=True)
        elif choice == "Q":
            print("Exiting Pipeline Controller. Bye!")
            break


def main():
    parser = argparse.ArgumentParser(
        description="Master Stage Pipeline Controller with Manual Triggers & Auto-Purging."
    )
    parser.add_argument("--stage", type=int, choices=[1, 2, 3], help="Stage number to run (1, 2, or 3).")
    parser.add_argument("--start-date", type=str, help="Start date YYYY-MM-DD for Stage 1.")
    parser.add_argument("--end-date", type=str, help="End date YYYY-MM-DD for Stage 1.")
    parser.add_argument("--db-url", type=str, help="PostgreSQL / Supabase connection URL for Stage 3.")
    parser.add_argument("--auto-purge", action="store_true", default=True, help="Auto-purge previous stage files upon completion (default: True).")

    args = parser.parse_args()

    if args.stage is None:
        interactive_menu()
    else:
        if args.stage == 1:
            if not args.start_date or not args.end_date:
                print("Error: Stage 1 requires --start-date and --end-date.")
                sys.exit(1)
            run_stage_1(args.start_date, args.end_date)
        elif args.stage == 2:
            run_stage_2(auto_purge=args.auto_purge)
        elif args.stage == 3:
            run_stage_3(db_url=args.db_url, auto_purge=args.auto_purge)


if __name__ == "__main__":
    main()
