import os
import requests
from bs4 import BeautifulSoup

print("Fetching website...")

BASE44_API_KEY = os.getenv("BASE44_API_KEY")

if not BASE44_API_KEY:
    print("❌ ERROR: Missing BASE44_API_KEY")
    exit(1)

print("✅ API key loaded successfully")

SCRAPE_URL = "https://www.studentcompetitions.com/competitions"


# -----------------------------
# SCRAPING FUNCTION
# -----------------------------
def scrape_competitions():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(SCRAPE_URL, headers=headers)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")

    competitions = []

    # Grab all links that look like competition pages
    for a in soup.find_all("a", href=True):
        href = a["href"]
        title = a.get_text(strip=True)

        if "/competitions/" in href and title and len(title) > 3:
            full_url = href if href.startswith("http") else "https://www.studentcompetitions.com" + href

            competitions.append({
                "title": title,
                "url": full_url,
                "description": "",
                "is_scraped": True
            })

    # remove duplicates
    unique = []
    seen = set()

    for c in competitions:
        if c["url"] not in seen:
            seen.add(c["url"])
            unique.append(c)

    return unique


# -----------------------------
# PUSH TO BASE44
# -----------------------------
from base44.sdk import createClient


def push_to_base44(data):
    print("📡 Sending to Base44 via SDK...")

    base44 = createClient({
        "appId": os.getenv("BASE44_APP_ID"),
        "headers": {
            "api_key": os.getenv("BASE44_API_KEY")
        }
    })

    success = 0

    for comp in data:
        try:
            base44.entities.Competition.create({
                "title": comp["title"],
                "url": comp["url"],
                "is_scraped": True
            })

            print("→", comp["title"])
            success += 1

        except Exception as e:
            print("❌ Error:", str(e))

    print(f"✅ Saved {success}/{len(data)}")


# -----------------------------
# MAIN FLOW
# -----------------------------
data = scrape_competitions()

print(f"📦 SCRAPED COMPETITIONS: {len(data)}")

for i, comp in enumerate(data):
    print(f"{i+1}. {comp['title']} - {comp['url']}")

push_to_base44(data)
