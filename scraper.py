import os
import requests
from bs4 import BeautifulSoup

print("Fetching website...")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Missing Supabase credentials")
    exit(1)

print("✅ API keys loaded")


SCRAPE_URL = "https://www.studentcompetitions.com/competitions"


def scrape_competitions():
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(SCRAPE_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    competitions = []
    seen = set()

    for a in soup.find_all("a", href=True):
        title = a.get_text(strip=True)
        href = a["href"]

        if "/competitions/" in href and "/category/" not in href and len(title) > 3:
            url = href if href.startswith("http") else "https://www.studentcompetitions.com" + href

            if url not in seen:
                seen.add(url)
                competitions.append({
                    "title": title,
                    "url": url,
                    "description": "",
                    "is_scraped": True
                })

    return competitions


def push_to_supabase(data):
    print("📡 Sending to Supabase...")

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    url = f"{SUPABASE_URL}/rest/v1/competitions"

    for comp in data:
        payload = {
            "title": comp["title"],
            "url": comp["url"],
            "description": comp["description"],
            "is_scraped": True
        }

        r = requests.post(url, json=payload, headers=headers)

        print(comp["title"], r.status_code, r.text)


# MAIN FLOW
data = scrape_competitions()

print(f"📦 SCRAPED COMPETITIONS: {len(data)}")

for i, comp in enumerate(data):
    print(f"{i+1}. {comp['title']} - {comp['url']}")

push_to_supabase(data)
