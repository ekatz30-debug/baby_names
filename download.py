import io
import re
import zipfile
import requests

url = "https://www.ssa.gov/oact/babynames/names.zip"

# Browser-like headers so the SSA server allows the download
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}

response = requests.get(url, headers=headers)
response.raise_for_status()

# Read each yearly text file from the zip in memory and write to a single CSV
with zipfile.ZipFile(io.BytesIO(response.content)) as z, open("ssa-baby-names.csv", "w", encoding="utf-8") as out:
    out.write("year,name,sex,count\n")
    for filename in sorted(z.namelist()):
        match = re.match(r"yob(\d{4})\.txt$", filename)
        if match:
            year = match.group(1)
            text = z.read(filename).decode("utf-8")
            for line in text.splitlines():
                if line:
                    out.write(f"{year},{line}\n")
