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
# SYNC LOG
# -----------------------------
from datetime import datetime

def write_sync_log(base44, imported=0, updated=0, status="Success", error=None):
    base44.asServiceRole.entities.CompetitionSync.create({
        "last_sync_at": datetime.utcnow().isoformat(),
        "competitions_imported": imported,
        "competitions_updated": updated,
        "status": status,
        "error_message": error
    })


# -----------------------------
# MAIN
# -----------------------------
def main():
    from base44.sdk import createClientFromRequest

    base44 = createClientFromRequest(None)

    try:
        # STEP 1: mark sync started
        write_sync_log(base44, 0, 0, "In Progress")

        # STEP 2: scrape data
        data = scrape()

        print(f"📦 Found {len(data)} competitions")

        # STEP 3: push competitions
        imported = push_to_base44(base44, data)

        # STEP 4: final success log
        write_sync_log(base44, imported=imported, updated=0, status="Success")

        print("✅ SYNC COMPLETE")

    except Exception as e:
        # STEP 5: failure log
        write_sync_log(base44, 0, 0, "Failed", str(e))
        print("❌ SYNC FAILED:", str(e))


main()
