import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

out = Path("./gdelt_data")
out.mkdir(exist_ok=True)

start = datetime(2026, 1, 1)
end   = datetime(2026, 8, 31)

d = start
while d <= end:
    url  = f"http://data.gdeltproject.org/events/{d.strftime('%Y%m%d')}.export.CSV.zip"
    dest = out / f"{d.strftime('%Y%m%d')}.export.CSV.zip"
    if not dest.exists():
        print(f"Downloading {d.date()} …")
        urllib.request.urlretrieve(url, dest)
    d += timedelta(days=1)   