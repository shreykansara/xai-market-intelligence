import zipfile
import csv
import io
import sys
import hashlib
from pathlib import Path


def get_url_hash(url: str) -> str:
    """Normalizes URL and generates an MD5 hash key for fast memory deduplication."""
    clean_url = url.strip().lower()
    return hashlib.md5(clean_url.encode("utf-8")).hexdigest()


def should_keep_record(row: list) -> bool:
    """
    Determines whether a GDELT record should be added to the output CSV file.
    
    Filtering Rules:
    1. Global / Worldwide News: If related to the entire world (e.g. global temperature,
       global economy, climate change, world-scale event) -> KEEP.
       Otherwise, the news must affect/mention India.
    2. International News: If related to specific foreign countries, KEEP ONLY IF it
       mentions/affects India (e.g., "USA imposes tariffs on India", "oil spills coming to India").
       Discard news specific to foreign countries that does NOT involve India.
    3. Intra-national (Domestic India) News: If news is domestic/national within India,
       it must be related to Punjab in some way. Otherwise DISCARD.
    4. Intra-Punjab News: If news is coming from within Punjab, it must be related to
       LPU, Kapurthala, Jalandhar, or Phagwara. Otherwise DISCARD.
    """
    if not row or len(row) < 1:
        return False

    # Extract key GDELT fields safely
    actor1_name = row[6] if len(row) > 6 else ""
    actor1_cc = row[7] if len(row) > 7 else ""
    actor2_name = row[16] if len(row) > 16 else ""
    actor2_cc = row[17] if len(row) > 17 else ""
    actor1_geo = row[37] if len(row) > 37 else ""
    actor1_adm1 = row[39] if len(row) > 39 else ""
    actor2_geo = row[45] if len(row) > 45 else ""
    actor2_adm1 = row[47] if len(row) > 47 else ""
    action_geo = row[52] if len(row) > 52 else ""
    action_cc = row[53] if len(row) > 53 else ""
    action_adm1 = row[54] if len(row) > 54 else ""
    source_url = row[-1] if len(row) > 0 else ""

    full_text = f"{actor1_name} {actor2_name} {actor1_geo} {actor2_geo} {action_geo} {source_url}".lower()

    # Rule 1: Global / World News Check
    global_keywords = [
        "global", "worldwide", "world news", "global warming", "climate change",
        "united nations", "unsec", "who", "wto", "imf", "world bank",
        "international space station", "g20", "g7", "pandemic", "earth"
    ]
    is_global = any(kw in full_text for kw in global_keywords) or action_geo.lower() in ["world", "global"]
    if is_global:
        return True

    # Check if India is mentioned or affected
    india_keywords = [
        "india", "indian", "bharat", "modi", "delhi", "new delhi", "mumbai",
        "punjab", "lpu", "jalandhar", "kapurthala", "phagwara"
    ]
    india_codes = ["IND", "IN"]
    affects_india = (
        any(kw in full_text for kw in india_keywords) or
        actor1_cc in india_codes or
        actor2_cc in india_codes or
        action_cc in india_codes
    )

    # If it's not global and does NOT affect India -> Discard
    if not affects_india:
        return False

    # Rule 2: International News Check
    foreign_actors = (
        (actor1_cc and actor1_cc not in india_codes) or
        (actor2_cc and actor2_cc not in india_codes) or
        (action_cc and action_cc not in india_codes)
    )
    
    # Check if the news is Domestic / Intra-national inside India (no foreign actors involved)
    is_domestic_india = not foreign_actors and affects_india

    # Rule 3 & Rule 4: Intra-national (within India) and Intra-Punjab checks
    punjab_keywords = [
        "punjab", "punjabi", "in23", "lpu", "jalandhar", "kapurthala", "phagwara"
    ]
    punjab_adm1_codes = ["IN23", "IN.23"]
    is_punjab = (
        any(kw in full_text for kw in punjab_keywords) or
        action_adm1 in punjab_adm1_codes or
        actor1_adm1 in punjab_adm1_codes or
        actor2_adm1 in punjab_adm1_codes
    )

    if is_domestic_india:
        # Rule 3: If domestic inside India, it must be related to Punjab
        if not is_punjab:
            return False

    # Rule 4: If news is within Punjab, it must be related to LPU, Kapurthala, Jalandhar, or Phagwara
    if is_punjab:
        target_locations = [
            "lpu", "lovely professional university", "lovely professional",
            "kapurthala", "jalandhar", "phagwara"
        ]
        is_target_punjab_location = any(loc in full_text for loc in target_locations)
        if not is_target_punjab_location:
            return False

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python convert.py YYYYMM  (e.g. python convert.py 202601)")
        sys.exit(1)

    month = sys.argv[1]
    out_dir = Path("./gdelt_data")
    files = sorted(out_dir.glob(f"{month}*.export.CSV.zip"))

    if not files:
        print(f"No files found for month {month}")
        sys.exit(1)

    dest = out_dir / f"gdelt_{month}.csv"

    # Start fresh every run (no append)
    dest.unlink(missing_ok=True)

    seen_urls = set()
    total_records = 0
    kept_records = 0
    duplicate_records = 0

    with open(dest, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile, delimiter="\t")
        
        for zfile in files:
            if not zipfile.is_zipfile(zfile):
                continue
            with zipfile.ZipFile(zfile) as zf:
                with zf.open(zf.namelist()[0]) as csv_file:
                    text_stream = io.TextIOWrapper(csv_file, encoding="utf-8", newline="")
                    reader = csv.reader(text_stream, delimiter="\t")
                    
                    for row in reader:
                        total_records += 1
                        
                        # 1. Filter based on location & topic criteria
                        if should_keep_record(row):
                            url = row[-1] if len(row) > 0 else ""
                            if url:
                                url_hash = get_url_hash(url)
                                # 2. Deduplication check based on article link (SOURCEURL)
                                if url_hash in seen_urls:
                                    duplicate_records += 1
                                    continue
                                seen_urls.add(url_hash)

                            writer.writerow(row)
                            kept_records += 1
                    
                    text_stream.close()

    print(f"Done: {len(files)} files processed.")
    print(
        f"Total Records: {total_records:,} | "
        f"Duplicates Skipped: {duplicate_records:,} | "
        f"Unique Kept: {kept_records:,} → {dest.name}"
    )


if __name__ == "__main__":
    main()