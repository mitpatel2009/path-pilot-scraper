import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = "https://www.studentcompetitions.com/competitions"

BASE44_API_KEY = os.getenv("BASE44_API_KEY")

if not BASE44_API_KEY:
    print("❌ Missing BASE44_API_KEY")
    exit(1)

print("Fetching website...")


# -----------------------------
# SCRAPE
# -----------------------------
def scrape():
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(BASE_URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    data = []
    seen = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        title = a.get_text(strip=True)

        if "/competitions/" in href and title and len(title) > 3:
            url = href if href.startswith("http") else "https://www.studentcompetitions.com" + href

            if url in seen:
                continue

            seen.add(url)

            data.append({
                "title": title,
                "url": url,
                "is_scraped": True
            })

    return data


# -----------------------------
# PUSH TO BASE44
# -----------------------------
import requests

BASE44_API_URL = "https://api.base44.com"  # your Base44 endpoint

def push_to_base44(data, api_key):
    print("📡 Pushing to Base44 via HTTP...")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    for comp in data:
        payload = {
            "title": comp["title"],
            "url": comp["url"],
            "is_scraped": True
        }

        res = requests.post(
            f"{BASE44_API_URL}/entities/Competition",
            json=payload,
            headers=headers
        )

        print("→", comp["title"], res.status_code)

    print("✅ Done pushing")


# -----------------------------
# SYNC LOG
# -----------------------------
def write_sync_log(base44, count):
    base44.asServiceRole.entities.CompetitionSync.create({
        "last_sync_at": datetime.utcnow().isoformat(),
        "competitions_imported": count,
        "status": "Success"
    })


# -----------------------------
# MAIN
# -----------------------------
def main():
    data = scrape()

    push_to_base44(data, BASE44_API_KEY)


main()
