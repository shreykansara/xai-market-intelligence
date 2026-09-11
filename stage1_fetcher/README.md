# Stage 1: GDELT Raw Zipped CSV Fetcher

Downloads raw GDELT daily event export zip files (`YYYYMMDD.export.CSV.zip`) from the official GDELT archives between two specified inclusive dates.

## Usage

```bash
# Fetch news for a single date
python fetch_gdelt_zipped.py --start-date 2026-01-01 --end-date 2026-01-01

# Fetch news for a full month (inclusive)
python fetch_gdelt_zipped.py --start-date 2026-08-01 --end-date 2026-08-31 --output-dir ../gdelt_data

# Fetch and automatically extract zip files
python fetch_gdelt_zipped.py --start-date 2026-08-01 --end-date 2026-08-05 --extract
```

## Parameters

* `--start-date`: Start date (`YYYY-MM-DD` or `YYYYMMDD`, inclusive).
* `--end-date`: End date (`YYYY-MM-DD` or `YYYYMMDD`, inclusive).
* `--output-dir`: Output directory path to save `.zip` files (default: `../gdelt_data`).
* `--extract`: Optional flag to extract raw `.CSV` files from downloaded `.zip` archives.
