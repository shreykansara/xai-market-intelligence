#!/usr/bin/env python3
"""
STAGE 1: GDELT Raw Zipped CSV Export Fetcher
---------------------------------------------
Downloads raw GDELT daily event export zip files (e.g. 20260101.export.CSV.zip)
from the GDELT archive between two inclusive dates specified via CLI parameters.

Usage Examples:
  # Fetch news for a single day:
  python fetch_gdelt_zipped.py --start-date 2026-01-01 --end-date 2026-01-01

  # Fetch news for an entire month (inclusive):
  python fetch_gdelt_zipped.py --start-date 2026-08-01 --end-date 2026-08-31 --output-dir ../gdelt_data
"""

import argparse
import logging
import os
import sys
import urllib.request
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("Stage1Fetcher")

GDELT_BASE_URL = "http://data.gdeltproject.org/events"


def parse_date(date_str: str) -> datetime:
    """Parses date string in YYYY-MM-DD or YYYYMMDD format."""
    clean_str = date_str.replace("-", "").strip()
    try:
        return datetime.strptime(clean_str, "%Y%m%d")
    except ValueError:
        logger.error(f"Invalid date format: '{date_str}'. Expected YYYY-MM-DD or YYYYMMDD.")
        sys.exit(1)


def generate_date_range(start_dt: datetime, end_dt: datetime) -> list:
    """Generates inclusive list of datetimes between start_dt and end_dt."""
    if start_dt > end_dt:
        logger.error(f"Start date ({start_dt.strftime('%Y-%m-%d')}) cannot be after end date ({end_dt.strftime('%Y-%m-%d')}).")
        sys.exit(1)

    dates = []
    curr = start_dt
    while curr <= end_dt:
        dates.append(curr)
        curr += timedelta(days=1)
    return dates


def download_gdelt_zip(dt: datetime, output_dir: Path, extract: bool = False) -> Path:
    """
    Downloads raw daily zipped GDELT CSV export file for a given date.
    URL pattern: http://data.gdeltproject.org/events/YYYYMMDD.export.CSV.zip
    """
    date_str = dt.strftime("%Y%m%d")
    filename = f"{date_str}.export.CSV.zip"
    target_zip_path = output_dir / filename
    download_url = f"{GDELT_BASE_URL}/{filename}"

    if target_zip_path.exists() and target_zip_path.stat().st_size > 1000:
        logger.info(f"Local file already exists: '{target_zip_path.name}'. Skipping download.")
        return target_zip_path

    logger.info(f"Downloading GDELT export zip for {dt.strftime('%Y-%m-%d')} from '{download_url}'...")
    
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
    }

    try:
        req = urllib.request.Request(download_url, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
            with open(target_zip_path, "wb") as f:
                f.write(data)
        logger.info(f"Successfully downloaded '{filename}' ({len(data) / (1024*1024):.2f} MB).")
    except Exception as e:
        logger.error(f"Failed to download GDELT file for {date_str}: {e}")
        if target_zip_path.exists():
            target_zip_path.unlink()
        return None

    if extract and target_zip_path.exists():
        try:
            logger.info(f"Extracting '{filename}'...")
            with zipfile.ZipFile(target_zip_path, "r") as z:
                z.extractall(output_dir)
            logger.info(f"Extracted CSV contents to '{output_dir}'.")
        except Exception as e:
            logger.error(f"Failed to extract zip file: {e}")

    return target_zip_path


def main():
    parser = argparse.ArgumentParser(
        description="Stage 1: Fetch GDELT raw export CSV zip files between inclusive dates."
    )
    parser.add_argument(
        "--start-date",
        type=str,
        required=True,
        help="Start date YYYY-MM-DD or YYYYMMDD (inclusive).",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        required=True,
        help="End date YYYY-MM-DD or YYYYMMDD (inclusive).",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="../gdelt_data",
        help="Directory to store downloaded zip files (default: ../gdelt_data).",
    )
    parser.add_argument(
        "--extract",
        action="store_true",
        help="Extract unzipped CSV files after downloading.",
    )

    args = parser.parse_args()

    start_dt = parse_date(args.start_date)
    end_dt = parse_date(args.end_date)
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    date_list = generate_date_range(start_dt, end_dt)
    logger.info(f"=== STAGE 1: FETCHING GDELT ZIPPED CSV EXPORTS ===")
    logger.info(f"Date Range : {start_dt.strftime('%Y-%m-%d')} to {end_dt.strftime('%Y-%m-%d')} ({len(date_list)} days inclusive)")
    logger.info(f"Output Path: {output_dir}")

    successful_downloads = 0
    for dt in date_list:
        res = download_gdelt_zip(dt, output_dir, extract=args.extract)
        if res:
            successful_downloads += 1

    logger.info(f"SUCCESS: Downloaded/verified {successful_downloads}/{len(date_list)} zip files in '{output_dir}'.")


if __name__ == "__main__":
    main()
