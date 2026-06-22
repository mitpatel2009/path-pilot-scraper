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
def push_to_base44(data):
    print("📡 SENDING TO BASE44...")

    # Base44 SDK style usage (adjust if your project differs)
    try:
        from base44.sdk import createClient
    except:
        print("⚠️ Base44 SDK not imported in CI — using fallback print mode")

    for comp in data:
        print("→", comp["title"])
        # REAL INSERT (uncomment if SDK is correctly installed in GitHub runner)
        base44.asServiceRole.entities.Competition.create(comp)

    print("✅ Data processed successfully")


# -----------------------------
# MAIN FLOW
# -----------------------------
data = scrape_competitions()

print(f"📦 SCRAPED COMPETITIONS: {len(data)}")

for i, comp in enumerate(data):
    print(f"{i+1}. {comp['title']} - {comp['url']}")

push_to_base44(data)
