"""GDELT 2.0 bulk export file access - the source for the historical World/India
backfill (see gdelt_backfill.py), as distinct from the live ingestion_service.py
(RSS + GDELT DOC 2.0 API, ~3 months lookback only). Bulk files
(data.gdeltproject.org/gdeltv2/) are published every 15 minutes going back to
2015 and are the only free, no-key source with multi-year depth.

Of GDELT's three bulk file types (Events, Mentions, GKG), only the GKG (Global
Knowledge Graph) file is used - Events/Mentions are pure structured/coded data
(CAMEO event codes, actor codes) with no article text at all, not even in the
Extras field. Verified directly by downloading and inspecting real files (today's,
a 2024 sample, and a 2022 sample) before building this, rather than assumed:
  - GKG's "Extras" column (index 26) contains a <PAGE_TITLE>...</PAGE_TITLE> tag
    with the real page title GDELT's own crawler extracted - present in 99.9% of
    records checked across all three sample dates. This is genuine headline-
    quality text, not a degraded substitute.
  - For the rare record missing it, this falls back to deriving a pseudo-title
    from the URL's slug (de-hyphenated path segment) - zero extra network calls,
    consistent with this project's no-scraping convention (see README's "Current
    scope").
  - GKG's "V1 Locations" column (index 9) carries each mentioned location's
    country code (2-letter FIPS, e.g. "IN" for India) - used for tier filtering
    (see matches_tier below) without needing a separate geocoding step.

GKG column indices (V2.1 format, no header row - positional):
  0 GKGRECORDID   1 DATE   2 SourceCollectionIdentifier   3 SourceCommonName
  4 DocumentIdentifier (URL)   5 Counts (V1)   6 V2Counts   7 V1Themes
  8 V2Themes   9 V1Locations   10 V2Locations   11 V1Persons   12 V2Persons
  13 V1Organizations   14 V2Organizations   15 V2Tone   16 Dates   17 GCAM
  18 SharingImage   19-21 media embeds   22 Quotations   23 AllNames
  24 Amounts   25 TranslationInfo   26 Extras (contains <PAGE_TITLE>)
"""
import html
import re
import zipfile
from datetime import datetime, timedelta, timezone
from io import BytesIO

import urllib.request

from .config import GDELT_BULK_BASE_URL

GKG_INTERVAL_MINUTES = 15
USER_AGENT = "Mozilla/5.0 (compatible; MarketIntelBot/0.1)"
PAGE_TITLE_PATTERN = re.compile(r"<PAGE_TITLE>(.*?)</PAGE_TITLE>", re.DOTALL)

# Column indices into a tab-split GKG row.
COL_DATE = 1
COL_URL = 4
COL_V1_LOCATIONS = 9
COL_EXTRAS = 26


def gkg_timestamps(start: datetime, end: datetime):
    """Every 15-minute-aligned GKG file timestamp in [start, end)."""
    t = start
    step = timedelta(minutes=GKG_INTERVAL_MINUTES)
    while t < end:
        yield t
        t += step


def gkg_url_for(timestamp: datetime) -> str:
    return f"{GDELT_BULK_BASE_URL}/{timestamp:%Y%m%d%H%M%S}.gkg.csv.zip"


def download_gkg_file(timestamp: datetime, timeout: int = 30) -> bytes | None:
    """Downloads one 15-minute GKG zip file's raw bytes. Returns None (not a
    raised exception) on any network failure - a single missing/unreachable
    file is common over a run spanning months and must not abort the whole
    backfill; callers should log and skip, matching how the live ingestion
    pipeline already treats a single source's fetch failure."""
    url = gkg_url_for(timestamp)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except Exception:
        return None


def _extract_title(fields: list[str]) -> tuple[str | None, str]:
    """Real page title from the Extras field's <PAGE_TITLE> tag, falling back to
    a de-slugified URL path segment for the rare record missing it. Returns
    (title, source) where source is "page_title" or "slug"; title is None if
    neither yields usable text.

    HTML-unescaped before returning - GDELT's crawler stores the raw HTML
    entity-encoded title verbatim (e.g. "&#x2013;" for an em-dash, "&#x20B9;"
    for the rupee sign), and a retroactive audit of real pilot data found this
    corrupts numeric grounding checks downstream: an entity like "&#x2013;"
    contains the literal digit run "2013", which can coincidentally satisfy a
    fabricated fact's number check even though no real number was ever stated.
    Decoding at the source fixes it for every consumer, not just grounding.py."""
    extras = fields[COL_EXTRAS] if len(fields) > COL_EXTRAS else ""
    match = PAGE_TITLE_PATTERN.search(extras)
    if match and match.group(1).strip():
        return html.unescape(match.group(1).strip()), "page_title"

    url = fields[COL_URL] if len(fields) > COL_URL else ""
    path = url.rstrip("/").rsplit("/", 1)[-1]
    path = re.sub(r"\.\w{2,5}$", "", path)  # strip a trailing file extension
    slug_text = re.sub(r"[-_]+", " ", path).strip()
    if slug_text and not slug_text.isdigit():
        return html.unescape(slug_text), "slug"
    return None, "none"


def _extract_country_codes(fields: list[str]) -> set[str]:
    """2-letter FIPS country codes from every location mentioned in the
    article (V1 Locations, semicolon-separated entries of
    type#name#country#adm1#lat#lon#featureid)."""
    locs = fields[COL_V1_LOCATIONS] if len(fields) > COL_V1_LOCATIONS else ""
    codes = set()
    for entry in locs.split(";"):
        parts = entry.split("#")
        if len(parts) >= 3 and parts[2]:
            codes.add(parts[2])
    return codes


def parse_gkg_bytes(raw_zip_bytes: bytes) -> list[dict]:
    """Unzips one GKG file and returns one dict per record: title, title_source,
    published (UTC datetime), url, country_codes (set of FIPS codes). Records
    with no usable title text at all (extremely rare - see _extract_title) are
    skipped rather than stored with an empty title."""
    records = []
    with zipfile.ZipFile(BytesIO(raw_zip_bytes)) as zf:
        name = zf.namelist()[0]
        with zf.open(name) as f:
            for raw_line in f:
                line = raw_line.decode("utf-8", errors="replace").rstrip("\n")
                if not line:
                    continue
                fields = line.split("\t")
                title, title_source = _extract_title(fields)
                if title is None:
                    continue
                date_str = fields[COL_DATE] if len(fields) > COL_DATE else ""
                try:
                    published = datetime.strptime(date_str, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
                except ValueError:
                    continue
                records.append({
                    "title": title,
                    "title_source": title_source,
                    "published": published,
                    "url": fields[COL_URL] if len(fields) > COL_URL else "",
                    "country_codes": _extract_country_codes(fields),
                })
    return records


def matches_tier(record: dict, tier: str) -> bool:
    """"world" keeps every record (broad, unfiltered - the relevance gate right
    after embedding is what actually thins this down, per the reordered batch
    pipeline). "india" keeps only records mentioning a location with FIPS
    country code "IN". Filtering happens at this stage - BEFORE embedding -
    specifically so the (much more expensive) embedding/gate/decomposition
    steps only ever run on the tier actually being collected."""
    if tier == "world":
        return True
    if tier == "india":
        return "IN" in record["country_codes"]
    raise ValueError(f"Unknown tier: {tier!r}")


def fetch_and_filter(timestamp: datetime, tier: str) -> list[dict] | None:
    """Downloads and parses one GKG file, returning only records matching
    `tier`. Returns None (not []) if the download itself failed, so callers can
    tell "nothing survived the tier filter" apart from "couldn't fetch this
    file at all" for logging/retry purposes."""
    raw = download_gkg_file(timestamp)
    if raw is None:
        return None
    records = parse_gkg_bytes(raw)
    return [r for r in records if matches_tier(r, tier)]
