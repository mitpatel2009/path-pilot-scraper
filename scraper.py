import os
import requests
from bs4 import BeautifulSoup

print("Fetching website...")

BASE44_API_KEY = "2aebdf0279d048d1b5bd81d8446694e9"

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
import os
import requests

SUPABASE_URL = "https://pkcumisiyejzgpcmmkyl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBrY3VtaXNpeWVqemdwY21ta3lsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE4NTM5NzksImV4cCI6MjA5NzQyOTk3OX0.KKfOD62-rugYsZdkvT-BjEc5yxKJynMLFRttYMC-Pwc"

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
        print(comp["title"], r.status_code)


# -----------------------------
# MAIN FLOW
# -----------------------------
data = scrape_competitions()

print(f"📦 SCRAPED COMPETITIONS: {len(data)}")

for i, comp in enumerate(data):
    print(f"{i+1}. {comp['title']} - {comp['url']}")

push_to_base44(data)
