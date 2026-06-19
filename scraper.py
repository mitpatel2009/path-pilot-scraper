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
import requests

BASE_URL = "https://api.base44.com"  # (or your Base44 app endpoint)

def push_to_base44(data):
    print("📡 PUSHING TO BASE44 VIA HTTP API...")

    headers = {
        "Authorization": f"Bearer {BASE44_API_KEY}",
        "Content-Type": "application/json"
    }

    for comp in data:
        payload = {
            "title": comp["title"],
            "url": comp["url"],
            "description": "",
            "is_scraped": True
        }

        res = requests.post(
            f"{BASE_URL}/entities/Competition",
            json=payload,
            headers=headers
        )

        print("→", comp["title"], res.status_code)

    print("✅ DONE PUSHING")

# -----------------------------
# MAIN FLOW
# -----------------------------
data = scrape_competitions()

print(f"📦 SCRAPED COMPETITIONS: {len(data)}")

for i, comp in enumerate(data):
    print(f"{i+1}. {comp['title']} - {comp['url']}")

push_to_base44(data)
