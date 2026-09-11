# Stage 2: Irrelevant News Filtering Engine

Processes raw GDELT zip/CSV exports from Stage 1, scrapes article page titles and body text, and eliminates irrelevant, duplicate, off-topic, or non-business news stories.

## Usage

```bash
# Filter a single GDELT raw zip file
python filter_gdelt_news.py --input ../gdelt_data/20260101.export.CSV.zip --output filtered_news_20260101.csv

# Filter all zip files in a folder (limit to 5000 items)
python filter_gdelt_news.py --input-dir ../gdelt_data --output filtered_news_202608.csv --limit 5000 --workers 8
```

## Input & Output Format

* **Input**: Raw GDELT CSV export files or `.export.CSV.zip` archives.
* **Output CSV Columns**: `id`, `date`, `headline`, `text`, `source_link`, `location_affected`.
