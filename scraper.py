import requests
from bs4 import BeautifulSoup
import json

SCRAPE_URL = "https://www.studentcompetitions.com/competitions"

def scrape():
    print("Fetching website...")

    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(SCRAPE_URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    data = []
    seen = set()

    for a in soup.find_all("a", href=True):
        title = a.get_text(strip=True)
        href = a["href"]

        if "/competitions/" in href and title:
            url = href if href.startswith("http") else "https://www.studentcompetitions.com" + href

            if url not in seen:
                seen.add(url)
                data.append({
                    "title": title,
                    "url": url,
                    "description": "",
                    "is_scraped": True
                })

    return data


data = scrape()

print(f"📦 SCRAPED COMPETITIONS: {len(data)}")

for i, c in enumerate(data):
    print(i+1, c["title"], "-", c["url"])

# 👉 IMPORTANT: output JSON for Base44 function (NOT DB write here)
with open("data.json", "w") as f:
    json.dump(data, f)

print("✅ Saved output for Base44 ingestion")
